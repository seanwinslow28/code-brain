# council/discovery/gather/reviews.py
"""Collector: review-site complaint mining with competitor-weakness bias.

Brave site-targeted search across review domains → fetch each result page → extract
complaint quotes biased toward low-star / negative language ("where competitors fail =
your wedge"). Every record is a real review-page URL + a verbatim complaint sentence, so
it is fabrication-gate-compatible. No paid scraper (spec §3) — reuses the free Brave
provider + the SSRF-hardened _simple_fetch from web.py.
"""

import os

from council.discovery.evidence import EvidenceRecord
from council.discovery.gather.web import _default_brave_search, _simple_fetch, extract_quotes

REVIEW_DOMAINS = (
    "g2.com", "capterra.com", "trustpilot.com",
    "producthunt.com", "apps.apple.com", "play.google.com",
)
_WEAKNESS = (
    '"1 star"', '"2 star"', "worst", "terrible", "disappointing", "avoid", "cancel",
)


def _review_query(topic: str) -> str:
    sites = " OR ".join(f"site:{d}" for d in REVIEW_DOMAINS)
    weak = " OR ".join(_WEAKNESS)
    return f"{topic} review ({weak}) ({sites})"


async def collect_reviews(*, topic: str, search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        key = os.environ.get("BRAVE_API_KEY")
        search = _default_brave_search(key) if key else None
    if fetch is ...:
        fetch = _simple_fetch
    if search is None:
        return []
    results = await search(_review_query(topic))
    recs: list[EvidenceRecord] = []
    for it in results[:max_results]:
        url = it.get("url", "")
        if not url:
            continue
        text = it.get("_text") or ""
        quotes = extract_quotes(text)
        if not quotes and fetch is not None:
            quotes = extract_quotes(await fetch(url))
        domain = next((d for d in REVIEW_DOMAINS if d in url), "review")
        for q in quotes:
            recs.append(EvidenceRecord(
                source_type="review", source_name=domain, url=url,
                date=it.get("published", ""), quote=q, engagement=0,
            ))
    return recs
