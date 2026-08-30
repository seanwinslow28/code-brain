"""Three-stage council orchestrator: fan-out → cross-rank → chairman."""

import asyncio
import json
import time
import uuid
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path

from council import pricing
from council.client import ClientError, ModelResponse, OpenRouterClient
from council.profiles import Profile
from council.prompts import (
    CHAIRMAN_SYSTEM,
    CROSSRANK_SYSTEM,
    FANOUT_SYSTEM,
    chairman_prompt,
    crossrank_prompt,
    fanout_prompt,
)


# Task 3c reservation inputs, to be Sean-disclosed at the Task 3c STOP.
FANOUT_MAX_TOKENS = 4096
CROSSRANK_MAX_TOKENS = 1024
CHAIRMAN_MAX_TOKENS = 8192
RESPONSE_EMBED_MAX_BYTES = 16384
RANKING_REASONING_EMBED_MAX_BYTES = 4096
_TRUNCATION_MARKER = "\n[truncated for bound]"


@dataclass(frozen=True)
class StageBounds:
    fanout_max_tokens: int
    crossrank_max_tokens: int
    chairman_max_tokens: int
    response_embed_max_bytes: int
    ranking_reasoning_embed_max_bytes: int
    price_policy: Callable[[str], dict]


DEFAULT_STAGE_BOUNDS = StageBounds(
    FANOUT_MAX_TOKENS,
    CROSSRANK_MAX_TOKENS,
    CHAIRMAN_MAX_TOKENS,
    RESPONSE_EMBED_MAX_BYTES,
    RANKING_REASONING_EMBED_MAX_BYTES,
    pricing.provider_price_policy,
)


class CouncilRunError(RuntimeError):
    """A council-stage failure carrying every provider attempt known at the boundary."""

    def __init__(self, message: str, *, stage: str, attempts: list[dict]) -> None:
        super().__init__(message)
        self.stage = stage
        self.attempts = attempts


class FanoutAbort(CouncilRunError):
    """Stage-1 lost enough models that the council cannot continue."""

    def __init__(self, message: str, *, attempts: list[dict]) -> None:
        super().__init__(message, stage="fanout", attempts=attempts)


class ChairmanFailure(CouncilRunError):
    """Stage-3 synthesis failed after earlier attempts may already have billed."""

    def __init__(self, message: str, *, attempts: list[dict]) -> None:
        super().__init__(message, stage="chairman", attempts=attempts)


def _dispatch_kwargs(
    bounds: StageBounds | None,
    *,
    model: str,
    max_tokens: int,
) -> dict:
    if bounds is None:
        return {}
    return {
        "max_tokens": max_tokens,
        "provider": bounds.price_policy(model),
    }


def _truncate_for_prompt(content: str | None, max_bytes: int) -> str:
    """Truncate UTF-8 content on a codepoint boundary, marker included in cap.

    The cap always wins: at caps too small to fit the marker, the marker is dropped
    rather than letting a negative slice EXPAND the content past ``max_bytes``.
    """
    rendered = content if isinstance(content, str) else str(content)
    encoded = rendered.encode("utf-8")
    if len(encoded) <= max_bytes:
        return rendered
    marker = _TRUNCATION_MARKER.encode("utf-8")
    if max_bytes <= len(marker):
        return encoded[:max_bytes].decode("utf-8", errors="ignore")
    prefix = encoded[: max_bytes - len(marker)].decode("utf-8", errors="ignore")
    return prefix + _TRUNCATION_MARKER


@dataclass
class CouncilSession:
    id: str
    profile: str
    tag: str
    user_query: str
    responses: list[dict]                  # [{model_id, content, tokens_in, tokens_out, latency_ms}]
    rankings: list[dict]                   # [{judge_model, ranking, reasoning}]
    chairman_response: ModelResponse
    dropped_models: list[str] = field(default_factory=list)
    ranking_failed_models: list[str] = field(default_factory=list)
    total_tokens_in: int = 0
    total_tokens_out: int = 0
    duration_ms: int = 0
    # Per-provider-attempt usage/cost, separate from user-facing content. Covers EVERY
    # attempt that returned a response — fanout survivors, cross-rank first + parse-retry,
    # and chairman — so measurement can see cross-rank spend (which the totals now include).
    attempts: list[dict] = field(default_factory=list)


def _attempt_record(stage: str, r: ModelResponse) -> dict:
    """A per-attempt usage/cost record (kept separate from user-facing content)."""
    return {
        "stage": stage,
        "requested_model": r.model_id,
        "returned_model_id": r.returned_model_id,
        "generation_id": r.generation_id,
        "tokens_in": r.tokens_in,
        "tokens_out": r.tokens_out,
        "cost": r.cost,
        "finish_reason": r.finish_reason,
    }


def _error_attempt_record(stage: str, requested_model: str, error: Exception) -> dict:
    """An interaction that raised before returning provider usage metadata."""
    return {
        "stage": stage,
        "requested_model": requested_model,
        "returned_model_id": None,
        "generation_id": None,
        "tokens_in": None,
        "tokens_out": None,
        "cost": None,
        "finish_reason": None,
        "error": f"{type(error).__name__}: {error}",
    }


@dataclass(frozen=True)
class _CallbackFailure:
    """Carries a callback failure through fanout's ordered gather result."""

    error: BaseException


def _deliver_attempt(on_attempt: Callable[[dict], None] | None, attempt: dict) -> None:
    if on_attempt is not None:
        on_attempt(attempt)


def _parse_ranking(content: str | None) -> dict | None:
    """Parse and shape-validate the cross-rank JSON. Returns the dict or None on failure.

    The CROSSRANK_SYSTEM contract is a list of unique single-letter labels plus a string
    reasoning. Enforcing that shape here matters beyond tidiness: chairman_prompt executes
    ' > '.join(ranking) and embeds reasoning verbatim, so an unvalidated ranking value
    (e.g. one long string) would expand a bounded judge response into an unbounded
    chairman input. Junk keys are stripped for the same reason.

    A judge can return null content (same upstream cause as the null-content render
    crash fixed 2026-06-18 in cli.py); that must read as an unparseable ranking, not
    an AttributeError that kills the whole council run with exit 3.
    """
    if not isinstance(content, str):
        return None
    try:
        # Strip optional markdown fence if present
        text = content.strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
        data = json.loads(text)
    except (json.JSONDecodeError, IndexError):
        return None
    if not isinstance(data, dict) or "ranking" not in data or "reasoning" not in data:
        return None
    ranking = data["ranking"]
    reasoning = data["reasoning"]
    if (
        not isinstance(ranking, list)
        or not 1 <= len(ranking) <= 8
        or any(
            not isinstance(label, str) or len(label) != 1 or not "A" <= label <= "Z"
            for label in ranking
        )
        or len(set(ranking)) != len(ranking)
        or not isinstance(reasoning, str)
    ):
        return None
    return {"ranking": ranking, "reasoning": reasoning}


async def _fanout(
    client: OpenRouterClient,
    models: tuple[str, ...],
    user_query: str,
    bounds: StageBounds | None,
    on_attempt: Callable[[dict], None] | None,
) -> tuple[list[ModelResponse], list[str], list[dict], list[dict]]:
    """Stage 1: parallel fan-out, capturing each interaction as it resolves."""
    user_msg = fanout_prompt(user_query=user_query)

    async def complete_one(model: str):
        try:
            response = await client.complete(
                model=model,
                system=FANOUT_SYSTEM,
                user=user_msg,
                **_dispatch_kwargs(
                    bounds,
                    model=model,
                    max_tokens=bounds.fanout_max_tokens if bounds else 0,
                ),
            )
        except Exception as error:
            attempt = _error_attempt_record("fanout", model, error)
            try:
                _deliver_attempt(on_attempt, attempt)
            except BaseException as callback_error:
                return _CallbackFailure(callback_error)
            return model, None, attempt
        attempt = _attempt_record("fanout", response)
        try:
            _deliver_attempt(on_attempt, attempt)
        except BaseException as callback_error:
            return _CallbackFailure(callback_error)
        return model, response, attempt

    results = await asyncio.gather(*(complete_one(model) for model in models))
    survivors: list[ModelResponse] = []
    dropped: list[str] = []
    success_attempts: list[dict] = []
    error_attempts: list[dict] = []
    for result in results:
        if isinstance(result, _CallbackFailure):
            raise result.error
        model, response, attempt = result
        if response is None:
            dropped.append(model)
            error_attempts.append(attempt)
        else:
            survivors.append(response)
            success_attempts.append(attempt)
    return survivors, dropped, success_attempts, error_attempts


async def _crossrank_one(
    client: OpenRouterClient,
    judge_model: str,
    user_query: str,
    others: list[dict],
    bounds: StageBounds | None,
    on_attempt: Callable[[dict], None] | None,
) -> tuple[dict | _CallbackFailure | None, list[dict]]:
    """Run one judge's cross-rank.

    Returns the parsed ranking (or None) and every success/error attempt record. Both
    returned-but-unparsed responses and a subsequent ClientError remain accountable.
    """
    user_msg = crossrank_prompt(user_query=user_query, others=others)
    attempts: list[dict] = []
    try:
        first = await client.complete(
            model=judge_model,
            system=CROSSRANK_SYSTEM,
            user=user_msg,
            **_dispatch_kwargs(
                bounds,
                model=judge_model,
                max_tokens=bounds.crossrank_max_tokens if bounds else 0,
            ),
        )
    except Exception as error:
        attempt = _error_attempt_record("crossrank", judge_model, error)
        attempts.append(attempt)
        try:
            _deliver_attempt(on_attempt, attempt)
        except BaseException as callback_error:
            return _CallbackFailure(callback_error), attempts
        if isinstance(error, ClientError):
            return None, attempts
        raise
    attempt = _attempt_record("crossrank", first)
    attempts.append(attempt)
    try:
        _deliver_attempt(on_attempt, attempt)
    except BaseException as callback_error:
        return _CallbackFailure(callback_error), attempts
    parsed = _parse_ranking(first.content)
    if parsed is not None:
        return {"judge_model": judge_model, **parsed}, attempts
    try:
        retry = await client.complete(
            model=judge_model,
            system=CROSSRANK_SYSTEM + "\n\nReturn ONLY a JSON object. No prose, no markdown fence.",
            user=user_msg,
            **_dispatch_kwargs(
                bounds,
                model=judge_model,
                max_tokens=bounds.crossrank_max_tokens if bounds else 0,
            ),
        )
    except Exception as error:
        attempt = _error_attempt_record("crossrank", judge_model, error)
        attempts.append(attempt)
        try:
            _deliver_attempt(on_attempt, attempt)
        except BaseException as callback_error:
            return _CallbackFailure(callback_error), attempts
        if isinstance(error, ClientError):
            return None, attempts
        raise
    attempt = _attempt_record("crossrank", retry)
    attempts.append(attempt)
    try:
        _deliver_attempt(on_attempt, attempt)
    except BaseException as callback_error:
        return _CallbackFailure(callback_error), attempts
    parsed = _parse_ranking(retry.content)
    if parsed is not None:
        return {"judge_model": judge_model, **parsed}, attempts
    return None, attempts


async def _crossrank(
    client: OpenRouterClient,
    responses: list[ModelResponse],
    user_query: str,
    bounds: StageBounds | None,
    on_attempt: Callable[[dict], None] | None,
) -> tuple[list[dict], list[str], list[dict], list[dict]]:
    """Stage 2: each surviving model judges the OTHER N-1 responses.

    Returns rankings, failed judges, success records for the unchanged session shape, and
    all success/error records for failure accounting. Every judge is drained before an
    error is raised, so no attempt callback can fire after this boundary returns. Callback
    failures take precedence in judge order, followed by raw provider exceptions in judge
    order; ``ClientError`` continues to degrade only that judge.
    """
    coros = []
    judge_models = []
    for judge in responses:
        others = [
            {
                "model_id": r.model_id,
                "content": (
                    r.content
                    if bounds is None
                    else _truncate_for_prompt(
                        r.content, bounds.response_embed_max_bytes
                    )
                ),
            }
            for r in responses
            if r.model_id != judge.model_id
        ]
        coros.append(
            _crossrank_one(
                client, judge.model_id, user_query, others, bounds, on_attempt
            )
        )
        judge_models.append(judge.model_id)
    results = await asyncio.gather(*coros, return_exceptions=True)
    for result in results:
        if isinstance(result, tuple) and isinstance(result[0], _CallbackFailure):
            raise result[0].error
    for result in results:
        if isinstance(result, BaseException):
            raise result
    rankings: list[dict] = []
    failed: list[str] = []
    attempts: list[dict] = []
    for model, result in zip(judge_models, results):
        r, judge_attempts = result
        attempts.extend(judge_attempts)
        if r is None:
            failed.append(model)
        else:
            rankings.append(r)
    success_attempts = [attempt for attempt in attempts if "error" not in attempt]
    return rankings, failed, success_attempts, attempts


async def _chairman(
    client: OpenRouterClient,
    chairman_model: str,
    user_query: str,
    responses: list[ModelResponse],
    rankings: list[dict],
    bounds: StageBounds | None,
) -> ModelResponse:
    """Stage 3: synthesis."""
    prompt_responses = [
        {"model_id": r.model_id, "content": r.content} for r in responses
    ]
    prompt_rankings = rankings
    if bounds is not None:
        prompt_responses = [
            {
                "model_id": r.model_id,
                "content": _truncate_for_prompt(
                    r.content, bounds.response_embed_max_bytes
                ),
            }
            for r in responses
        ]
        prompt_rankings = [
            {
                **ranking,
                "reasoning": _truncate_for_prompt(
                    ranking["reasoning"],
                    bounds.ranking_reasoning_embed_max_bytes,
                ),
            }
            for ranking in rankings
        ]
    user_msg = chairman_prompt(
        user_query=user_query,
        responses=prompt_responses,
        rankings=prompt_rankings,
    )
    return await client.complete(
        model=chairman_model,
        system=CHAIRMAN_SYSTEM,
        user=user_msg,
        **_dispatch_kwargs(
            bounds,
            model=chairman_model,
            max_tokens=bounds.chairman_max_tokens if bounds else 0,
        ),
    )


async def run_council(
    *,
    client: OpenRouterClient,
    profile: Profile,
    user_query: str,
    tag: str,
    sessions_dir: Path | None = None,
    dispatch_bounds: StageBounds | None = None,
    on_attempt: Callable[[dict], None] | None = None,
) -> CouncilSession:
    """End-to-end council run. Aborts on 2+ Stage-1 failures; degrades on 1.

    Every admission gateway must either inject ``dispatch_bounds`` or provide a
    self-bounding client. The council CLI injects ``DEFAULT_STAGE_BOUNDS``;
    the-oracle uses its own guarded, self-bounding client.

    When ``on_attempt`` is supplied, it runs synchronously immediately after each provider
    interaction resolves. Its exceptions propagate unchanged: accounting is a fail-closed
    boundary, so an accounting failure aborts the council rather than losing the attempt.

    Cancellation of the caller cancels the gather and its children; a spontaneous child
    CancelledError propagates rather than being classified as a provider failure.
    """
    started = time.perf_counter()
    session_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    responses, dropped, fanout_attempts, fanout_errors = await _fanout(
        client, profile.models, user_query, dispatch_bounds, on_attempt
    )
    if len(dropped) >= 2:
        raise FanoutAbort(
            f"Council unavailable: two or more models failed in Stage 1 ({dropped}). "
            "Fall back to single-model review.",
            attempts=fanout_attempts + fanout_errors,
        )

    rankings, ranking_failed, crossrank_attempts, all_crossrank_attempts = await _crossrank(
        client, responses, user_query, dispatch_bounds, on_attempt
    )

    try:
        chairman_resp = await _chairman(
            client,
            profile.chairman,
            user_query,
            responses,
            rankings,
            dispatch_bounds,
        )
    except Exception as e:
        # Spec §5: chairman failure aborts with a clear message. The CLI catches
        # RuntimeError and produces a graceful exit; we wrap ClientError here
        # to centralize error normalization at the pipeline boundary.
        chairman_error = _error_attempt_record("chairman", profile.chairman, e)
        _deliver_attempt(on_attempt, chairman_error)
        if not isinstance(e, ClientError):
            raise
        raise ChairmanFailure(
            f"Chairman synthesis failed ({profile.chairman}): {e}. "
            f"Stage-1 produced {len(responses)} responses; Stage-2 produced "
            f"{len(rankings)} rankings. Council session JSON was not written. "
            f"Fall back to single-model review or retry.",
            attempts=(
                fanout_attempts
                + fanout_errors
                + all_crossrank_attempts
                + [chairman_error]
            ),
        ) from e

    chairman_attempt = _attempt_record("chairman", chairman_resp)
    _deliver_attempt(on_attempt, chairman_attempt)
    attempts = (
        fanout_attempts
        + crossrank_attempts
        + [chairman_attempt]
    )
    total_in = sum(a["tokens_in"] for a in attempts)
    total_out = sum(a["tokens_out"] for a in attempts)

    session = CouncilSession(
        id=session_id,
        profile=profile.name,
        tag=tag,
        user_query=user_query,
        responses=[
            {
                "model_id": r.model_id,
                "content": r.content,
                "tokens_in": r.tokens_in,
                "tokens_out": r.tokens_out,
                "latency_ms": r.latency_ms,
            }
            for r in responses
        ],
        rankings=rankings,
        chairman_response=chairman_resp,
        dropped_models=dropped,
        ranking_failed_models=ranking_failed,
        total_tokens_in=total_in,
        total_tokens_out=total_out,
        duration_ms=int((time.perf_counter() - started) * 1000),
        attempts=attempts,
    )

    if sessions_dir is not None:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        out = sessions_dir / f"{session_id}.json"
        out.write_text(json.dumps({
            "id": session.id,
            "profile": session.profile,
            "tag": session.tag,
            "user_query": session.user_query,
            "responses": session.responses,
            "rankings": session.rankings,
            "chairman": asdict(chairman_resp),
            "dropped_models": session.dropped_models,
            "ranking_failed_models": session.ranking_failed_models,
            "total_tokens_in": session.total_tokens_in,
            "total_tokens_out": session.total_tokens_out,
            "duration_ms": session.duration_ms,
            "attempts": session.attempts,
        }, indent=2))

    return session
