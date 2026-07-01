# tests/discovery/test_gather_sonar.py
import pytest
from council.discovery.gather.sonar import collect_sonar


@pytest.mark.asyncio
async def test_collect_sonar_uses_citations(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Teams report onboarding is slow. Pricing is opaque."}}],
        "citations": ["https://news.com/a", "https://blog.com/b"],
        "usage": {"prompt_tokens": 100, "completion_tokens": 60},
    })
    recs, _ = await collect_sonar(api_key="k", topic="pm tools", model="perplexity/sonar-reasoning-pro")
    assert len(recs) >= 1
    assert all(r.url.startswith("http") for r in recs)
    assert all(r.source_type == "sonar" for r in recs)


@pytest.mark.asyncio
async def test_no_citations_yields_nothing(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Some claim."}}], "citations": [], "usage": {},
    })
    recs, _ = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar")
    assert recs == []


@pytest.mark.asyncio
async def test_collect_sonar_reads_message_annotations(httpx_mock):
    # Live OpenRouter Sonar shape (2026-06): citations live in choices[0].message.annotations
    # as url_citation entries, NOT a top-level `citations` key.
    httpx_mock.add_response(json={
        "choices": [{"message": {
            "content": "Reliability has dropped sharply. Context windows burn out far too fast.",
            "annotations": [
                {"type": "url_citation", "url_citation": {"url": "https://a.com/x", "title": "A"}},
                {"type": "url_citation", "url_citation": {"url": "https://b.com/y", "title": "B"}},
            ],
        }}],
        "usage": {"prompt_tokens": 100, "completion_tokens": 60},
    })
    recs, _ = await collect_sonar(api_key="k", topic="claude code", model="perplexity/sonar")
    assert len(recs) == 2
    assert {r.url for r in recs} == {"https://a.com/x", "https://b.com/y"}
    assert all(r.source_type == "sonar" for r in recs)
    assert all(r.quote for r in recs)


@pytest.mark.asyncio
async def test_collect_sonar_anchors_verbatim_quote_via_fetch(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Synthesized paraphrase sentence about onboarding."}}],
        "citations": ["https://news.com/a"], "usage": {},
    })
    async def fetch(url):
        return "Real reviewers complain the onboarding flow is broken and confusing."
    recs, _ = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar", fetch=fetch)
    assert len(recs) == 1
    assert "onboarding flow is broken" in recs[0].quote   # verbatim from the page, not the paraphrase


@pytest.mark.asyncio
async def test_collect_sonar_falls_back_to_synthesized_when_fetch_empty(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Teams report onboarding is slow and painful."}}],
        "citations": ["https://news.com/a"], "usage": {},
    })
    async def fetch(url):
        return ""    # page yielded no complaint sentence
    recs, _ = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar", fetch=fetch)
    assert recs[0].quote == "Teams report onboarding is slow and painful."


@pytest.mark.asyncio
async def test_collect_sonar_returns_billed_cost(httpx_mock):
    # Sonar is a PAID Perplexity call; OpenRouter returns usage.cost. collect_sonar must surface
    # that billed cost (records, cost) so the orchestrator can thread it into the spend ledger —
    # the "every collector is FREE" gather invariant never applied to Sonar.
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Onboarding is slow. Pricing is opaque."}}],
        "citations": ["https://news.com/a", "https://blog.com/b"],
        "usage": {"prompt_tokens": 100, "completion_tokens": 60, "cost": 0.0231},
    })
    result = await collect_sonar(api_key="k", topic="pm tools", model="perplexity/sonar")
    assert isinstance(result, tuple)
    recs, cost = result
    assert cost == pytest.approx(0.0231)
    assert all(r.source_type == "sonar" for r in recs)


@pytest.mark.asyncio
async def test_collect_sonar_cost_zero_when_usage_missing(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "A claim about it here."}}],
        "citations": ["https://a.com/1"], "usage": {},
    })
    recs, cost = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar")
    assert cost == 0.0
    assert len(recs) == 1


@pytest.mark.asyncio
async def test_collect_sonar_no_citations_returns_zero_cost(httpx_mock):
    # Sonar can bill even when it returns no usable citations; surface that billed cost, not just [].
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Vague."}}], "citations": [],
        "usage": {"cost": 0.018},
    })
    recs, cost = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar")
    assert recs == []
    assert cost == pytest.approx(0.018)


@pytest.mark.asyncio
async def test_collect_sonar_includes_segment_in_prompt(httpx_mock):
    import json as _json
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "a claim about it here."}}],
        "citations": ["https://a.com/1"], "usage": {},
    })
    await collect_sonar(api_key="k", topic="note apps", model="perplexity/sonar",
                        segment="developers", fetch=None)
    body = _json.loads(httpx_mock.get_requests()[0].content)
    assert "developers" in body["messages"][0]["content"]
