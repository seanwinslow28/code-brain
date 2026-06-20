# tests/discovery/test_gather_web.py
import pytest
from council.discovery.gather.web import collect_web, extract_quotes


def test_extract_quotes_prefers_complaint_sentences():
    text = "The dashboard is fine. Users complain that exports fail silently every week. Nice colors."
    quotes = extract_quotes(text)
    assert any("exports fail" in q for q in quotes)


@pytest.mark.asyncio
async def test_collect_web_builds_records():
    async def search(q):
        return [{"title": "T", "url": "https://blog.com/x", "published": "2026-06-15"}]
    async def fetch(u):
        return "Teams say the export silently fails and support never replies."
    recs = await collect_web(topic="exports", search=search, fetch=fetch)
    assert len(recs) == 1
    assert recs[0].url == "https://blog.com/x"
    assert recs[0].date == "2026-06-15"
    assert recs[0].source_type == "web"


@pytest.mark.asyncio
async def test_no_search_provider_returns_empty():
    recs = await collect_web(topic="x", search=None, fetch=None)
    assert recs == []
