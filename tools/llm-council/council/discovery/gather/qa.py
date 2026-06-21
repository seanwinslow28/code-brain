# council/discovery/gather/qa.py
"""Collector: Stack Exchange Q&A pain mining (deep tier).

Free Stack Exchange API (https://api.stackexchange.com/docs/advanced-search) — no key needed
(300 req/day unauthenticated). Each question is a real link + a verbatim (HTML-unescaped) title
quote → fabrication-gate-compatible. Defaults to the stackoverflow site; multi-site is deferred.
"""

import html
from datetime import datetime, timezone

import httpx

from council.discovery.evidence import EvidenceRecord

STACKEXCHANGE_URL = "https://api.stackexchange.com/2.3/search/advanced"


def _epoch_to_date(epoch) -> str:
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        return ""


def _default_se_search(site: str = "stackoverflow"):
    async def search(query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(STACKEXCHANGE_URL, params={
                "order": "desc", "sort": "relevance", "q": query, "site": site, "pagesize": 15,
            })
            r.raise_for_status()
            return r.json().get("items", [])
    return search


async def collect_qa(*, topic: str, search=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        search = _default_se_search()
    if search is None:
        return []
    items = await search(topic)
    recs: list[EvidenceRecord] = []
    for it in items[:max_results]:
        url = it.get("link", "")
        title = html.unescape(it.get("title", ""))
        if not (url and title):
            continue
        recs.append(EvidenceRecord(
            source_type="qa", source_name="stackoverflow", url=url,
            date=_epoch_to_date(it.get("creation_date")), quote=title,
            engagement=int(it.get("score", 0) or 0),
        ))
    return recs
