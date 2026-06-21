# tests/discovery/test_gather_web.py
import pytest
from council.discovery.gather import web as webmod
from council.discovery.gather.web import (
    collect_web,
    extract_quotes,
    _default_brave_search,
    _simple_fetch,
)


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


@pytest.mark.asyncio
async def test_brave_search_normalizes(httpx_mock):
    httpx_mock.add_response(
        url="https://api.search.brave.com/res/v1/web/search?q=acme+user+complaints+problems+frustrations+2026&count=8",
        json={"web": {"results": [
            {"title": "Acme is broken", "url": "https://b.com/1",
             "description": "Users complain Acme crashes on export.", "page_age": "2026-06-10T00:00:00"},
        ]}},
    )
    search = _default_brave_search("k")
    out = await search("acme user complaints problems frustrations 2026")
    assert out[0]["url"] == "https://b.com/1"
    assert out[0]["published"] == "2026-06-10"
    assert "crashes on export" in out[0]["_text"]


@pytest.mark.asyncio
async def test_simple_fetch_strips_html(httpx_mock):
    httpx_mock.add_response(url="https://x.com/p",
                            text="<html><body><p>Exports fail silently every time.</p><script>x()</script></body></html>")
    text = await _simple_fetch("https://x.com/p")
    assert "Exports fail silently" in text
    assert "x()" not in text


@pytest.mark.asyncio
async def test_collect_web_fetch_fallback_when_snippet_has_no_quote():
    # snippet has no complaint word → fetch fallback supplies the quote
    async def search(q):
        return [{"title": "T", "url": "https://b.com/2", "published": "2026-06-15", "_text": "neutral blurb"}]
    async def fetch(u):
        return "Teams say the dashboard is painfully slow to load."
    recs = await collect_web(topic="dashboards", search=search, fetch=fetch)
    assert len(recs) == 1
    assert "painfully slow" in recs[0].quote


@pytest.mark.asyncio
async def test_collect_web_selects_brave_when_only_brave_key(monkeypatch, httpx_mock):
    monkeypatch.delenv("EXA_API_KEY", raising=False)
    monkeypatch.setenv("BRAVE_API_KEY", "bk")
    httpx_mock.add_response(  # brave search
        json={"web": {"results": [
            {"title": "T", "url": "https://b.com/3", "description": "Users hate the broken sync.", "page_age": "2026-06-01"}]}})
    recs = await collect_web(topic="sync")
    assert any(r.url == "https://b.com/3" for r in recs)
