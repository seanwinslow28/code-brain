"""Three-stage council orchestrator: fan-out → cross-rank → chairman."""

import asyncio
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path

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


async def _fanout(client: OpenRouterClient, models: tuple[str, ...], user_query: str) -> tuple[list[ModelResponse], list[str]]:
    """Stage 1: parallel fan-out. Returns (surviving_responses, dropped_model_ids)."""
    user_msg = fanout_prompt(user_query=user_query)
    coros = [
        client.complete(model=m, system=FANOUT_SYSTEM, user=user_msg)
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
) -> tuple[dict | None, list[ModelResponse]]:
    """Run one judge's cross-rank.

    Returns (parsed ranking dict or None, list of the response attempts made). Both the
    first and the parse-retry attempts are returned so their usage is measured even when
    parsing fails (a returned-but-unparsed response was still billed).
    """
    user_msg = crossrank_prompt(user_query=user_query, others=others)
    attempts: list[ModelResponse] = []
    try:
        first = await client.complete(model=judge_model, system=CROSSRANK_SYSTEM, user=user_msg)
        attempts.append(first)
        parsed = _parse_ranking(first.content)
        if parsed is not None:
            return {"judge_model": judge_model, **parsed}, attempts
        retry = await client.complete(
            model=judge_model,
            system=CROSSRANK_SYSTEM + "\n\nReturn ONLY a JSON object. No prose, no markdown fence.",
            user=user_msg,
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
            {"model_id": r.model_id, "content": r.content}
            for r in responses
            if r.model_id != judge.model_id
        ]
        coros.append(_crossrank_one(client, judge.model_id, user_query, others))
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
) -> ModelResponse:
    """Stage 3: synthesis."""
    user_msg = chairman_prompt(
        user_query=user_query,
        responses=[{"model_id": r.model_id, "content": r.content} for r in responses],
        rankings=rankings,
    )
    return await client.complete(
        model=chairman_model,
        system=CHAIRMAN_SYSTEM,
        user=user_msg,
    )


async def run_council(
    *,
    client: OpenRouterClient,
    profile: Profile,
    user_query: str,
    tag: str,
    sessions_dir: Path | None = None,
) -> CouncilSession:
    """End-to-end council run. Aborts on 2+ Stage-1 failures; degrades on 1."""
    started = time.perf_counter()
    session_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    responses, dropped = await _fanout(client, profile.models, user_query)
    if len(dropped) >= 2:
        raise RuntimeError(
            f"Council unavailable: two or more models failed in Stage 1 ({dropped}). "
            "Fall back to single-model review."
        )

    rankings, ranking_failed, crossrank_attempts = await _crossrank(client, responses, user_query)

    try:
        chairman_resp = await _chairman(
            client,
            profile.chairman,
            user_query,
            responses,
            rankings,
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
