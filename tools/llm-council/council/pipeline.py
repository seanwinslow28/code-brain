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


def _parse_ranking(content: str) -> dict | None:
    """Parse and shape-validate the cross-rank JSON. Returns the dict or None on failure.

    The CROSSRANK_SYSTEM contract is a list of unique single-letter labels plus a string
    reasoning. Enforcing that shape here matters beyond tidiness: chairman_prompt executes
    ' > '.join(ranking) and embeds reasoning verbatim, so an unvalidated ranking value
    (e.g. one long string) would expand a bounded judge response into an unbounded
    chairman input. Junk keys are stripped for the same reason.
    """
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
) -> tuple[list[ModelResponse], list[str]]:
    """Stage 1: parallel fan-out. Returns (surviving_responses, dropped_model_ids)."""
    user_msg = fanout_prompt(user_query=user_query)
    coros = [
        client.complete(
            model=m,
            system=FANOUT_SYSTEM,
            user=user_msg,
            **_dispatch_kwargs(
                bounds,
                model=m,
                max_tokens=bounds.fanout_max_tokens if bounds else 0,
            ),
        )
        for m in models
    ]
    results = await asyncio.gather(*coros, return_exceptions=True)
    survivors: list[ModelResponse] = []
    dropped: list[str] = []
    for model, r in zip(models, results):
        if isinstance(r, Exception):
            dropped.append(model)
        else:
            survivors.append(r)
    return survivors, dropped


async def _crossrank_one(
    client: OpenRouterClient,
    judge_model: str,
    user_query: str,
    others: list[dict],
    bounds: StageBounds | None,
) -> tuple[dict | None, list[ModelResponse]]:
    """Run one judge's cross-rank.

    Returns (parsed ranking dict or None, list of the response attempts made). Both the
    first and the parse-retry attempts are returned so their usage is measured even when
    parsing fails (a returned-but-unparsed response was still billed).
    """
    user_msg = crossrank_prompt(user_query=user_query, others=others)
    attempts: list[ModelResponse] = []
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
        attempts.append(first)
        parsed = _parse_ranking(first.content)
        if parsed is not None:
            return {"judge_model": judge_model, **parsed}, attempts
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
        attempts.append(retry)
        parsed = _parse_ranking(retry.content)
        if parsed is not None:
            return {"judge_model": judge_model, **parsed}, attempts
    except ClientError:
        return None, attempts
    return None, attempts


async def _crossrank(
    client: OpenRouterClient,
    responses: list[ModelResponse],
    user_query: str,
    bounds: StageBounds | None,
) -> tuple[list[dict], list[str], list[ModelResponse]]:
    """Stage 2: each surviving model judges the OTHER N-1 responses.

    Returns (parsed_rankings, ranking_failed_model_ids, all_response_attempts). The third
    element carries every cross-rank response attempt (first + parse-retry) for usage
    accounting.
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
        coros.append(_crossrank_one(client, judge.model_id, user_query, others, bounds))
        judge_models.append(judge.model_id)
    results = await asyncio.gather(*coros)
    rankings: list[dict] = []
    failed: list[str] = []
    attempts: list[ModelResponse] = []
    for model, (r, judge_attempts) in zip(judge_models, results):
        attempts.extend(judge_attempts)
        if r is None:
            failed.append(model)
        else:
            rankings.append(r)
    return rankings, failed, attempts


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
) -> CouncilSession:
    """End-to-end council run. Aborts on 2+ Stage-1 failures; degrades on 1.

    Every admission gateway must either inject ``dispatch_bounds`` or provide a
    self-bounding client. The council CLI injects ``DEFAULT_STAGE_BOUNDS``;
    the-oracle uses its own guarded, self-bounding client.
    """
    started = time.perf_counter()
    session_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    responses, dropped = await _fanout(
        client, profile.models, user_query, dispatch_bounds
    )
    if len(dropped) >= 2:
        raise RuntimeError(
            f"Council unavailable: two or more models failed in Stage 1 ({dropped}). "
            "Fall back to single-model review."
        )

    rankings, ranking_failed, crossrank_attempts = await _crossrank(
        client, responses, user_query, dispatch_bounds
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
    except ClientError as e:
        # Spec §5: chairman failure aborts with a clear message. The CLI catches
        # RuntimeError and produces a graceful exit; we wrap ClientError here
        # to centralize error normalization at the pipeline boundary.
        raise RuntimeError(
            f"Chairman synthesis failed ({profile.chairman}): {e}. "
            f"Stage-1 produced {len(responses)} responses; Stage-2 produced "
            f"{len(rankings)} rankings. Council session JSON was not written. "
            f"Fall back to single-model review or retry."
        ) from e

    attempts = (
        [_attempt_record("fanout", r) for r in responses]
        + [_attempt_record("crossrank", r) for r in crossrank_attempts]
        + [_attempt_record("chairman", chairman_resp)]
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
