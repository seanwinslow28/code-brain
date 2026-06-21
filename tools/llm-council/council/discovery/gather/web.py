# council/discovery/gather/web.py
"""Collector: neural web search (Exa/Brave) + fetch → complaint-quote extraction."""

import ipaddress
import os
import re
import socket
from urllib.parse import urlparse

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


_FETCH_MAX_REDIRECTS = 3


def _resolve_ips(host: str) -> list[str]:
    """Resolve a hostname to its IP strings (IPv4 + IPv6). Real DNS; injectable in tests.

    Note: a brief blocking getaddrinfo is acceptable for this personal tool. There is a
    residual TOCTOU gap between resolve and connect (DNS rebinding) we accept rather than
    pin the connection IP — fetch targets come from Brave results, not an attacker.
    """
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return []
    return [info[4][0] for info in infos]


def _is_safe_fetch_url(url: str, *, resolve=_resolve_ips) -> bool:
    """True only for http(s) URLs whose host resolves entirely to globally-routable IPs.

    Blocks non-http(s) schemes (file://, gopher://, ftp://, …) and SSRF targets: loopback,
    private, link-local (incl. 169.254.169.254 cloud metadata), and reserved ranges. A host
    that resolves to ANY non-global IP is rejected (no partial trust).
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = parsed.hostname
    if not host:
        return False
    try:                                  # literal IP host → check directly, no DNS
        return ipaddress.ip_address(host).is_global
    except ValueError:
        pass
    ips = resolve(host)
    if not ips:
        return False
    for raw in ips:
        try:
            if not ipaddress.ip_address(raw).is_global:
                return False
        except ValueError:
            return False
    return True


async def _simple_fetch(url: str, timeout: float = 20.0) -> str:
    """Best-effort full-page text for quote density (crude tag-strip).

    SSRF-hardened: validates scheme + resolved IPs of the initial URL AND every redirect hop
    against a public-IP allow-list before connecting. Redirects are followed manually
    (follow_redirects=False) so a public URL can't 302 into a private/metadata address.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as c:
            current = url
            html = ""
            for _ in range(_FETCH_MAX_REDIRECTS + 1):
                if not _is_safe_fetch_url(current):
                    return ""
                r = await c.get(current, headers={"User-Agent": "Mozilla/5.0 (discovery-bot)"})
                if r.is_redirect:
                    loc = r.headers.get("location")
                    if not loc:
                        return ""
                    current = str(httpx.URL(current).join(loc))
                    continue
                r.raise_for_status()
                ctype = r.headers.get("content-type", "")
                # Skip non-HTML bodies (PDF/binary); missing content-type is allowed.
                if ctype and not (ctype.startswith("text/") or ctype.startswith("application/xhtml")):
                    return ""
                html = r.text[:2_000_000]
                break
            else:
                return ""  # exceeded the redirect cap
    except httpx.HTTPError:
        return ""
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


async def collect_web(*, topic: str, segment: str = "", search=..., fetch=..., max_results: int = 8) -> list[EvidenceRecord]:
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
    subject = f"{topic} {segment}".strip() if segment else topic
    query = f"{subject} user complaints problems frustrations 2026"
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
