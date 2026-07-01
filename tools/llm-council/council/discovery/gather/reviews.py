# council/discovery/gather/reviews.py
"""Collector: review-site complaint mining with competitor-weakness bias.

Brave site-targeted search across review domains → fetch each result page → extract
complaint quotes biased toward low-star / negative language ("where competitors fail =
your wedge"). Every record is a real review-page URL + a verbatim complaint sentence, so
it is fabrication-gate-compatible. No paid scraper (spec §3) — reuses the free Brave
provider + the SSRF-hardened _simple_fetch from web.py.
"""

import asyncio
import os
from itertools import zip_longest

from council.discovery.evidence import EvidenceRecord
from council.discovery.gather.web import _default_brave_search, _simple_fetch, extract_quotes
from council.discovery.textbudget import BRAVE_Q_MAX_CHARS, BRAVE_Q_MAX_WORDS, clamp_words_chars

REVIEW_DOMAINS = (
    "g2.com", "capterra.com", "trustpilot.com",
    "producthunt.com", "apps.apple.com", "play.google.com",
)
_WEAKNESS = (
    '"1 star"', '"2 star"', "worst", "terrible", "disappointing", "avoid", "cancel",
)


def _review_query(subject: str, domain: str) -> str:
    weak = " OR ".join(_WEAKNESS)
    return f"{subject} review ({weak}) site:{domain}"


async def collect_reviews(*, topic: str, segment: str = "", search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        key = os.environ.get("BRAVE_API_KEY")
        search = _default_brave_search(key) if key else None
    if fetch is ...:
        fetch = _simple_fetch
    if search is None:
        return []
    subject = f"{topic} {segment}".strip() if segment else topic
    # Single-site scaffolding ("review (<weakness OR ...>) site:<domain>") eats ~16 words / ~110 chars
    # of Brave's q-param ceiling; clamp the variable subject so a long topic/--segment can't push any
    # composed query past it and 422.
    subject = clamp_words_chars(subject, max_words=BRAVE_Q_MAX_WORDS - 20, max_chars=BRAVE_Q_MAX_CHARS - 140)

    # Brave collapses an OR'd multi-site: query, so most review domains never get searched. Fan out to
    # one single-site query per domain (concurrently, tolerating a per-domain failure) and merge.
    per_domain = await asyncio.gather(
        *(search(_review_query(subject, d)) for d in REVIEW_DOMAINS),
        return_exceptions=True,
    )
    # Round-robin merge across domains (preserves per-domain relevance rank AND cross-domain diversity),
    # dedup by URL, then cap TOTAL fetches so the fan-out can't explode cost/latency.
    lists = [r if isinstance(r, list) else [] for r in per_domain]
    merged: list[dict] = []
    seen: set[str] = set()
    for rank in zip_longest(*lists):
        for it in rank:
            if it is None:
                continue
            url = it.get("url", "")
            if not url or url in seen:
                continue
            seen.add(url)
            merged.append(it)
    merged = merged[:max_results]

    recs: list[EvidenceRecord] = []
    for it in merged:
        url = it["url"]
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
