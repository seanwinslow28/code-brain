# tests/discovery/test_fusion.py
import json
import httpx
import pytest
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.tiers import get_tier
from council.discovery import fusion


def _bundle():
    b = EvidenceBundle()
    b.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "sync drops notes", 40))
    return b


@pytest.mark.asyncio
async def test_fuse_parses_judge_json(httpx_mock):
    judge_payload = {
        "pain_points": [{
            "title": "Sync data loss",
            "summary": "Notes silently dropped on conflict.",
            "quotes": ["sync drops notes"],
            "urls": ["https://r.com/1"],
            "consensus": "4/4 models",
            "intensity": 5, "recency": "2026-06", "segment": "power users",
        }],
        "blind_spots": ["no model addressed enterprise SSO"],
        "contradictions": ["grok: mobile-only; gemini: desktop too"],
    }
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": json.dumps(judge_payload)}}],
        "usage": {"prompt_tokens": 1200, "completion_tokens": 400},
    })
    res = await fusion.fuse(api_key="k", bundle=_bundle(), tier=get_tier("quick"), topic="obsidian sync")
    assert len(res.pain_points) == 1
    assert res.pain_points[0].title == "Sync data loss"
    assert res.pain_points[0].urls == ["https://r.com/1"]
    assert res.blind_spots == ["no model addressed enterprise SSO"]
    assert res.tokens_in == 1200 and res.tokens_out == 400


@pytest.mark.asyncio
async def test_fuse_retries_then_raises_on_unparseable(httpx_mock):
    httpx_mock.add_response(json={"choices": [{"message": {"content": "not json"}}], "usage": {}})
    httpx_mock.add_response(json={"choices": [{"message": {"content": "still not json"}}], "usage": {}})
    with pytest.raises(fusion.FusionError):
        await fusion.fuse(api_key="k", bundle=_bundle(), tier=get_tier("quick"), topic="x")
