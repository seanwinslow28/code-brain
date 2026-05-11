import json
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from lib.job_scoring import score_posting, JobScoringUnavailable, build_scoring_prompt
from lib.job_types import Posting, ScoringResult


def _p(**overrides) -> Posting:
    base = dict(
        source="x", source_role_id="1", url="https://x.example",
        company="Co", title="Product Manager", location="Remote (US)",
        salary_disclosed=None, posted_at=datetime(2026, 5, 9),
        description="A PM role.",
    )
    base.update(overrides)
    return Posting(**base)


def test_build_scoring_prompt_includes_constraints_and_posting():
    p = _p(title="APM, Foundations")
    prompt = build_scoring_prompt(p)
    assert "$100k" in prompt or "100k" in prompt  # walk-away
    assert "Eastern Time" in prompt
    assert "APM, Foundations" in prompt
    assert "Remote (US)" in prompt


@pytest.mark.asyncio
async def test_score_posting_routes_via_hybrid_router_and_parses():
    router = MagicMock()
    decision = MagicMock(machine="macbook_pro", model="qwen3-14b",
                        base_url="http://192.168.68.50:1234", runtime="lm-studio",
                        is_fallback=False)
    router.route = AsyncMock(return_value=decision)

    fake_response = {
        "fit_score": 4, "role_band": "PM",
        "rationale": "Solid PM fit.", "concerns": ["YOE floor"],
        "fit_dimensions": {"role_band_fit": 4, "geo_fit": 5, "industry_fit": 4, "yoe_fit": 3},
    }

    async def fake_completion(base_url, model, prompt):
        return json.dumps(fake_response)

    result = await score_posting(_p(), router=router, completion_fn=fake_completion)
    assert isinstance(result, ScoringResult)
    assert result.fit_score == 4
    assert result.role_band == "PM"
    assert result.concerns == ["YOE floor"]


@pytest.mark.asyncio
async def test_score_posting_raises_when_router_returns_fallback_decision():
    """fallback_disabled=True path: if router would fall back to claude_api, refuse."""
    router = MagicMock()
    fallback_decision = MagicMock(machine="claude_api", model="claude-sonnet-4-6",
                                 base_url="https://api.anthropic.com", runtime="api",
                                 is_fallback=True, reason="MBP unreachable")
    router.route = AsyncMock(return_value=fallback_decision)

    async def fake_completion(*a, **k):
        raise AssertionError("Must not call completion_fn when fallback would happen")

    with pytest.raises(JobScoringUnavailable):
        await score_posting(_p(), router=router, completion_fn=fake_completion,
                          fallback_disabled=True)


@pytest.mark.asyncio
async def test_score_posting_handles_malformed_json_with_default():
    router = MagicMock()
    decision = MagicMock(machine="macbook_pro", model="qwen3-14b",
                        base_url="http://x", runtime="lm-studio", is_fallback=False)
    router.route = AsyncMock(return_value=decision)

    async def fake_completion(*a, **k):
        return "not json at all"

    result = await score_posting(_p(), router=router, completion_fn=fake_completion)
    assert result.fit_score == 0
    assert "unparseable" in result.rationale.lower()
    assert any("unparseable" in c.lower() for c in result.concerns)
