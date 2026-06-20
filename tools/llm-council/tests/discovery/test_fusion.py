# tests/discovery/test_fusion.py
import json
import httpx
import pytest
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.tiers import get_tier
from council.discovery import fusion
from council.discovery.fusion import _strip_sse_padding, _first_json_object, _parse


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


@pytest.mark.asyncio
async def test_fuse_surfaces_4xx_body_without_retry(httpx_mock):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    from council.discovery import fusion
    httpx_mock.add_response(status_code=400, json={"error": {"message": "max_tool_calls too high"}})
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    with pytest.raises(fusion.FusionError) as exc:
        await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert "max_tool_calls too high" in str(exc.value)
    assert "400" in str(exc.value)
    assert len(httpx_mock.get_requests()) == 1          # no retry on HTTP error


@pytest.mark.asyncio
async def test_fuse_captures_usage_cost(httpx_mock):
    import json
    payload = {"pain_points": [{"title": "T", "summary": "s", "quotes": ["q"], "urls": ["https://r.com/1"]}]}
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": json.dumps(payload)}}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 50, "cost": 0.4231},
    })
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    from council.discovery import fusion
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    res = await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert res.cost == 0.4231


def test_strip_sse_padding_removes_comment_lines():
    raw = ": OPENROUTER PROCESSING\n\n: OPENROUTER PROCESSING\n\n{\"a\": 1}"
    assert _strip_sse_padding(raw) == '{"a": 1}'


def test_first_json_object_extracts_balanced_object_from_prose():
    text = 'Sure, here you go:\n{"pain_points": [{"title": "x"}]}\nLet me know!'
    obj = _first_json_object(text)
    assert obj == {"pain_points": [{"title": "x"}]}


def test_first_json_object_handles_braces_inside_strings():
    text = '{"q": "a } b { c", "pain_points": []}'
    assert _first_json_object(text) == {"q": "a } b { c", "pain_points": []}


def test_parse_tolerates_prose_wrapped_json():
    content = 'Here are the results:\n{"pain_points": [{"title": "T"}], "blind_spots": []}\nDone.'
    assert _parse(content) == {"pain_points": [{"title": "T"}], "blind_spots": []}


@pytest.mark.asyncio
async def test_fuse_decodes_sse_padded_response(httpx_mock):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.tiers import get_tier
    judge = {"pain_points": [{"title": "T", "summary": "s", "quotes": ["q"], "urls": ["https://r.com/1"]}]}
    envelope = {"choices": [{"message": {"content": json.dumps(judge)}}], "usage": {"cost": 0.3}}
    padded = ": OPENROUTER PROCESSING\n\n: OPENROUTER PROCESSING\n\n" + json.dumps(envelope)
    httpx_mock.add_response(text=padded)   # text/plain → resp.json() would fail; _decode_payload recovers
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    res = await fusion.fuse(api_key="k", bundle=b, tier=get_tier("quick"), topic="x")
    assert res.pain_points[0].title == "T"
    assert res.cost == 0.3


def test_decode_payload_raises_on_undecodable_body():
    class _R:
        text = "not json at all <html>"
    with pytest.raises(fusion.FusionError):
        fusion._decode_payload(_R())
