# tests/discovery/test_gather_web.py
import pytest
from council.discovery.gather import web as webmod
from council.discovery.gather.web import (
    collect_web,
    extract_quotes,
    _default_brave_search,
    _simple_fetch,
    _is_safe_fetch_url,
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
    httpx_mock.add_response(url="http://93.184.216.34/p",
                            text="<html><body><p>Exports fail silently every time.</p><script>x()</script></body></html>")
    text = await _simple_fetch("http://93.184.216.34/p")
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


def test_is_safe_fetch_url_blocks_non_http_schemes():
    assert _is_safe_fetch_url("file:///etc/passwd") is False
    assert _is_safe_fetch_url("gopher://169.254.169.254/") is False
    assert _is_safe_fetch_url("ftp://example.com/x") is False


def test_is_safe_fetch_url_blocks_private_and_metadata_ips():
    assert _is_safe_fetch_url("http://169.254.169.254/latest/meta-data/") is False  # cloud metadata
    assert _is_safe_fetch_url("http://127.0.0.1/") is False
    assert _is_safe_fetch_url("http://10.0.0.5/") is False
    assert _is_safe_fetch_url("http://192.168.1.10/") is False


def test_is_safe_fetch_url_resolves_hostname_via_injected_resolver():
    assert _is_safe_fetch_url("https://g2.com/x", resolve=lambda h: ["93.184.216.34"]) is True
    # any resolved private IP rejects the whole host (DNS-rebinding-conservative)
    assert _is_safe_fetch_url("https://evil.test/x", resolve=lambda h: ["10.1.2.3"]) is False
    # unresolvable host is rejected
    assert _is_safe_fetch_url("https://nope.test/x", resolve=lambda h: []) is False


@pytest.mark.asyncio
async def test_simple_fetch_blocks_redirect_to_metadata(httpx_mock):
    # public literal-IP first hop 302s toward the cloud-metadata IP → must be blocked, returns ""
    httpx_mock.add_response(url="http://93.184.216.34/start", status_code=302,
                            headers={"location": "http://169.254.169.254/latest"})
    text = await _simple_fetch("http://93.184.216.34/start")
    assert text == ""
    assert len(httpx_mock.get_requests()) == 1   # metadata hop never fetched


@pytest.mark.asyncio
async def test_collect_web_includes_segment_in_query():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_web(topic="note apps", segment="designers", search=search, fetch=None)
    assert "designers" in captured["q"] and "note apps" in captured["q"]


@pytest.mark.asyncio
async def test_collect_web_no_segment_unchanged():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_web(topic="note apps", search=search, fetch=None)
    assert captured["q"] == "note apps user complaints problems frustrations 2026"
