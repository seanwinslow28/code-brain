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
    recs = await collect_sonar(api_key="k", topic="pm tools", model="perplexity/sonar-reasoning-pro")
    assert len(recs) >= 1
    assert all(r.url.startswith("http") for r in recs)
    assert all(r.source_type == "sonar" for r in recs)


@pytest.mark.asyncio
async def test_no_citations_yields_nothing(httpx_mock):
    httpx_mock.add_response(json={
        "choices": [{"message": {"content": "Some claim."}}], "citations": [], "usage": {},
    })
    recs = await collect_sonar(api_key="k", topic="x", model="perplexity/sonar")
    assert recs == []
