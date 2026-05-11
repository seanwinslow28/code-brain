"""LLM scoring for the job-feed agent.

Routes the `job_scoring` task through HybridRouter. With fallback_disabled=True,
refuses to score if the router would fall back to claude_api (cost integrity).
Postings that fail scoring persist with fit_score=NULL for retry next run.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Awaitable, Callable

import httpx

from lib.hybrid_router import HybridRouter
from lib.job_types import Posting, ScoringResult

logger = logging.getLogger(__name__)


class JobScoringUnavailable(Exception):
    """Raised when scoring can't run (MBP unreachable + fallback_disabled)."""


SYSTEM_PROMPT = """You are a JSON-only assistant scoring how well a job posting fits Sean Winslow's profile.

Sean's hard constraints (Tier-A):
- Walk-away base salary: $100k (treat $90k+ as borderline)
- Office: ≤3 days RTO; prefers 0-2 (remote ideal)
- Geography: US-remote OR Boston-metro (Boston, Cambridge, Somerville, Waltham, Newton, Brookline)
- Time zone: must accommodate Eastern Time

Sean's eligible role bands:
- APM, PM I/II, PM, Senior APM = primary fit
- Senior PM = STRETCH (only if YOE floor ≤ 3 yrs)
- Principal PM = STRETCH (some companies use as IC track)
- Director, VP, Head of Product, Group PM, Sr Director, CPO = EXCLUDE (band already filtered, flag if seen)

Sean's background: 2 years titled PM experience at The Block (crypto/Web3 publisher),
prior 8 years editorial/design at Bloomberg. Side AI portfolio: Phaser game dev, Remotion
video, Claude Code mastery. Strong fit signals: AI-native, crypto, creative tools, dev tools.

Output STRICT JSON ONLY, no preamble, no markdown:
{
  "fit_score": 0-5 integer,
  "role_band": "PM" | "APM" | "Sr_PM_stretch" | "Principal_stretch" | "Other",
  "rationale": "one-sentence why this lands or doesn't",
  "concerns": ["array of disqualifiers worth flagging"],
  "fit_dimensions": {
    "role_band_fit": 0-5,
    "geo_fit": 0-5,
    "industry_fit": 0-5,
    "yoe_fit": 0-5
  }
}

Example 1 — clean APM fit:
Input: Anthropic, Associate Product Manager, Claude Code, Remote (US), $140k-$170k
Output: {"fit_score":5,"role_band":"APM","rationale":"AI-native, remote-US, APM band lands cleanly with side AI portfolio.","concerns":[],"fit_dimensions":{"role_band_fit":5,"geo_fit":5,"industry_fit":5,"yoe_fit":5}}

Example 2 — Senior PM stretch with domain depth:
Input: Hopper, Senior PM, AI & Commerce, Remote (US), $180k-$220k, 3+ years
Output: {"fit_score":4,"role_band":"Sr_PM_stretch","rationale":"Stretch on title but YOE floor is 3yr; AI-PM + Boston-HQ are strong industry/geo signals.","concerns":["YOE floor"],"fit_dimensions":{"role_band_fit":3,"geo_fit":5,"industry_fit":5,"yoe_fit":3}}

Example 3 — on-paper match that fails geo:
Input: Sierra, PM, Conversational AI, London only, £100k-£140k
Output: {"fit_score":1,"role_band":"PM","rationale":"London-only excludes Sean's US-or-Boston requirement.","concerns":["geo: London only"],"fit_dimensions":{"role_band_fit":5,"geo_fit":0,"industry_fit":5,"yoe_fit":4}}
"""


def build_scoring_prompt(posting: Posting) -> str:
    return (
        SYSTEM_PROMPT
        + "\n\nPosting to score:\n"
        + f"Company: {posting.company}\n"
        + f"Title: {posting.title}\n"
        + f"Location: {posting.location or 'unspecified'}\n"
        + f"Salary: {posting.salary_disclosed or 'undisclosed'}\n"
        + f"URL: {posting.url}\n"
        + f"Description (truncated):\n{posting.description[:1500]}\n"
        + "\nReply with one JSON object. No other text.\n"
    )


CompletionFn = Callable[[str, str, str], Awaitable[str]]


async def _default_completion(base_url: str, model: str, prompt: str) -> str:
    """Default LLM completion via Ollama or LM Studio (both expose OpenAI-compat).

    Tries Ollama /api/generate first (Ollama default), falls back to /v1/chat/completions.
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Try Ollama /api/generate
        r = await client.post(
            f"{base_url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False, "format": "json"},
        )
        if r.status_code == 200:
            return r.json().get("response", "")
        # Fall through to OpenAI-compat
        r = await client.post(
            f"{base_url}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            },
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]


def _parse_score_json(raw: str) -> ScoringResult | None:
    """Best-effort JSON extraction from the model's output."""
    raw = raw.strip()
    # Strip ```json fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```\s*$", "", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    try:
        return ScoringResult(
            fit_score=int(data["fit_score"]),
            role_band=str(data["role_band"]),
            rationale=str(data["rationale"]),
            concerns=list(data.get("concerns", [])),
            fit_dimensions=dict(data.get("fit_dimensions", {})),
        )
    except (KeyError, TypeError, ValueError):
        return None


async def score_posting(
    posting: Posting,
    *,
    router: HybridRouter,
    completion_fn: CompletionFn | None = None,
    fallback_disabled: bool = True,
) -> ScoringResult:
    """Score a single posting via the HybridRouter.

    Raises JobScoringUnavailable if fallback_disabled and the router can't reach
    the preferred local machine.
    """
    decision = await router.route("job_scoring")
    if decision.is_fallback and fallback_disabled:
        raise JobScoringUnavailable(
            f"job_scoring routed to fallback ({decision.machine}); fallback_disabled=True. "
            f"Reason: {decision.reason}"
        )

    fn = completion_fn or _default_completion
    try:
        raw = await fn(decision.base_url, decision.model, build_scoring_prompt(posting))
    except Exception as exc:
        logger.warning("Scoring HTTP call failed for %s: %s", posting.source_role_id, exc)
        raise JobScoringUnavailable(str(exc)) from exc

    result = _parse_score_json(raw)
    if result is None:
        logger.warning("Unparseable scoring output for %s: %r", posting.source_role_id, raw[:200])
        return ScoringResult(
            fit_score=0,
            role_band="Other",
            rationale="LLM output unparseable; defaulted to low score for manual audit.",
            concerns=["LLM output unparseable — flag for audit"],
            fit_dimensions={},
        )
    return result
