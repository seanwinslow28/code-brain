# council/discovery/gather/web.py
"""Collector: neural web search (Exa/Brave) + fetch → complaint-quote extraction."""

import os
import re

import httpx

from council.discovery.evidence import EvidenceRecord

_SENT = re.compile(r"[^.!?]{20,240}[.!?]")
_COMPLAINT = re.compile(
    r"\b(complain|frustrat|annoy|hate|broken|fails?|can't|cannot|wish|missing|lacks?|"
    r"slow|confusing|workaround|painful|bug|crash)\b", re.I,
)


def extract_quotes(text: str, limit: int = 2) -> list[str]:
    hits = [s.strip() for s in _SENT.findall(text) if _COMPLAINT.search(s)]
    return hits[:limit]


def _default_exa_search(api_key: str):
    async def search(query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(
                "https://api.exa.ai/search",
                headers={"x-api-key": api_key, "Content-Type": "application/json"},
                json={"query": query, "numResults": 8, "type": "neural",
                      "contents": {"text": True}},
            )
            r.raise_for_status()
            out = []
            for it in r.json().get("results", []):
                out.append({"title": it.get("title", ""), "url": it.get("url", ""),
                            "published": (it.get("publishedDate") or "")[:10],
                            "_text": (it.get("text") or "")})
            return out
    return search


def _default_brave_search(api_key: str):
    async def search(query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"X-Subscription-Token": api_key, "Accept": "application/json"},
                params={"q": query, "count": 8},
            )
            r.raise_for_status()
            out = []
            for it in r.json().get("web", {}).get("results", []):
                out.append({"title": it.get("title", ""), "url": it.get("url", ""),
                            "published": (it.get("page_age") or it.get("age") or "")[:10],
                            "_text": it.get("description", "")})
            return out
    return search


async def _simple_fetch(url: str, timeout: float = 20.0) -> str:
    """Best-effort full-page text for quote density. Crude tag-strip; Phase 3 may swap a real parser."""
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as c:
            r = await c.get(url, headers={"User-Agent": "Mozilla/5.0 (discovery-bot)"})
            r.raise_for_status()
            html = r.text
    except httpx.HTTPError:
        return ""
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


async def collect_web(*, topic: str, search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        if os.environ.get("EXA_API_KEY"):
            search = _default_exa_search(os.environ["EXA_API_KEY"])
            if fetch is ...:
                fetch = None  # Exa returns full _text already
        elif os.environ.get("BRAVE_API_KEY"):
            search = _default_brave_search(os.environ["BRAVE_API_KEY"])
            if fetch is ...:
                fetch = _simple_fetch  # Brave returns a snippet only
        else:
            search = None
    if fetch is ...:
        fetch = None
    if search is None:
        return []
    query = f"{topic} user complaints problems frustrations 2026"
    results = await search(query)
    recs: list[EvidenceRecord] = []
    for it in results[:max_results]:
        url = it.get("url", "")
        if not url:
            continue
        text = it.get("_text") or ""
        if not extract_quotes(text) and fetch is not None:
            text = await fetch(url)
        for q in extract_quotes(text):
            recs.append(EvidenceRecord(
                source_type="web", source_name=it.get("title", "") or "web",
                url=url, date=it.get("published", ""), quote=q, engagement=0,
            ))
    return recs
