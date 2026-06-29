import pytest
from council.discovery.gather.reviews import collect_reviews, _review_query, REVIEW_DOMAINS


def test_review_query_targets_sites_and_weakness():
    q = _review_query("acme crm")
    assert "acme crm" in q
    assert "site:g2.com" in q and "site:trustpilot.com" in q
    assert "worst" in q  # competitor-weakness bias term


@pytest.mark.asyncio
async def test_collect_reviews_builds_records_with_domain_name():
    async def search(query):
        return [{"title": "Acme on G2", "url": "https://www.g2.com/products/acme/reviews",
                 "published": "2026-06-12",
                 "_text": "Reviewers complain Acme crashes during export and support is slow."}]
    recs = await collect_reviews(topic="acme", search=search, fetch=None)
    assert len(recs) >= 1
    r = recs[0]
    assert r.source_type == "review"
    assert r.source_name == "g2.com"
    assert r.url == "https://www.g2.com/products/acme/reviews"
    assert "crashes during export" in r.quote


@pytest.mark.asyncio
async def test_collect_reviews_fetch_fallback_when_snippet_thin():
    async def search(query):
        return [{"title": "T", "url": "https://www.capterra.com/p/x", "published": "2026-06-01",
                 "_text": "neutral marketing copy"}]
    async def fetch(url):
        return "One reviewer wrote that the tool is painfully slow and they will cancel."
    recs = await collect_reviews(topic="x", search=search, fetch=fetch)
    assert any("painfully slow" in r.quote for r in recs)


@pytest.mark.asyncio
async def test_collect_reviews_no_key_returns_empty(monkeypatch):
    monkeypatch.delenv("BRAVE_API_KEY", raising=False)
    recs = await collect_reviews(topic="x")
    assert recs == []


@pytest.mark.asyncio
async def test_collect_reviews_includes_segment_in_query():
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    await collect_reviews(topic="crm", segment="nonprofits", search=search, fetch=None)
    assert "crm" in captured["q"] and "nonprofits" in captured["q"]
    assert "site:g2.com" in captured["q"]   # still site-targeted


@pytest.mark.asyncio
async def test_collect_reviews_clamps_long_topic_under_brave_q_ceiling():
    # A long topic/--segment composed with the site:/weakness scaffolding can blow past Brave's
    # ~50-word / ~400-char q-param ceiling and 422. The variable subject must be clamped so the
    # composed query stays under it — without truncating the site: operators away.
    captured = {}
    async def search(q):
        captured["q"] = q
        return []
    long_topic = " ".join(["creative"] * 40)
    await collect_reviews(topic=long_topic, search=search, fetch=None)
    assert len(captured["q"].split()) <= 50
    assert len(captured["q"]) <= 400
    assert "site:g2.com" in captured["q"]    # scaffolding preserved
    assert "creative" in captured["q"]       # subject still present
