import pytest
from council.discovery.gather.reviews import collect_reviews, _review_query, REVIEW_DOMAINS


def test_review_query_is_single_site():
    # Brave collapses an OR'd multi-site: query (most review domains never get searched), so each
    # domain gets its OWN single-site query.
    q = _review_query("acme crm", "g2.com")
    assert "acme crm" in q
    assert "site:g2.com" in q
    assert "worst" in q                          # competitor-weakness bias preserved
    assert "site:trustpilot.com" not in q        # exactly one site: operator per query


@pytest.mark.asyncio
async def test_collect_reviews_fans_out_one_query_per_domain():
    captured = []
    async def search(q):
        captured.append(q)
        dom = next((d for d in REVIEW_DOMAINS if f"site:{d}" in q), "review")
        return [{"title": dom, "url": f"https://{dom}/r/1", "published": "2026-06-01",
                 "_text": f"reviewers say {dom} is broken and painfully slow and they cannot export."}]
    recs = await collect_reviews(topic="acme", search=search, fetch=None)
    assert len(captured) == len(REVIEW_DOMAINS)                       # one query per domain
    assert all(sum(f"site:{d}" in q for d in REVIEW_DOMAINS) == 1 for q in captured)  # single-site each
    assert {r.source_name for r in recs} == set(REVIEW_DOMAINS)       # all domains' results merged


@pytest.mark.asyncio
async def test_collect_reviews_dedups_urls_across_domains():
    async def search(q):
        # different domain queries can surface the same aggregator URL → must dedup to one record
        return [{"title": "dup", "url": "https://shared.com/x", "published": "2026-06-01",
                 "_text": "this product is broken and crashes constantly so we cannot use it."}]
    recs = await collect_reviews(topic="acme", search=search, fetch=None)
    assert len([r for r in recs if r.url == "https://shared.com/x"]) == 1


@pytest.mark.asyncio
async def test_collect_reviews_caps_total_fetches():
    fetched = []
    async def search(q):
        dom = next((d for d in REVIEW_DOMAINS if f"site:{d}" in q), "review")
        return [{"title": "t", "url": f"https://{dom}/r/{i}", "published": "", "_text": "neutral copy"}
                for i in range(5)]                                    # 6 domains × 5 = 30 candidates
    async def fetch(url):
        fetched.append(url)
        return "this tool is the worst and crashes daily, avoid it"
    await collect_reviews(topic="x", search=search, fetch=fetch, max_results=8)
    assert len(fetched) <= 8                                          # fan-out must not explode fetches


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
    captured = []
    async def search(q):
        captured.append(q)
        return []
    await collect_reviews(topic="crm", segment="nonprofits", search=search, fetch=None)
    assert all("crm" in q and "nonprofits" in q for q in captured)   # subject+segment in every query
    assert any("site:g2.com" in q for q in captured)                 # still site-targeted
    assert all(sum(f"site:{d}" in q for d in REVIEW_DOMAINS) == 1 for q in captured)  # single-site each


@pytest.mark.asyncio
async def test_collect_reviews_clamps_long_topic_under_brave_q_ceiling():
    # A long topic/--segment composed with the site:/weakness scaffolding can blow past Brave's
    # ~50-word / ~400-char q-param ceiling and 422. The variable subject must be clamped so the
    # composed query stays under it — without truncating the site: operators away.
    captured = []
    async def search(q):
        captured.append(q)
        return []
    long_topic = " ".join(["creative"] * 40)
    await collect_reviews(topic=long_topic, search=search, fetch=None)
    assert all(len(q.split()) <= 50 for q in captured)               # every fanned-out query under ceiling
    assert all(len(q) <= 400 for q in captured)
    assert any("site:g2.com" in q for q in captured)                 # scaffolding preserved
    assert all("creative" in q for q in captured)                    # subject still present
