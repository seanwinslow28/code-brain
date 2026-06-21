# council/discovery/gather/sonar.py
"""Collector: Perplexity Sonar fresh-article harvest. Citation URLs are the evidence anchors."""

import re
import httpx

from council.discovery.evidence import EvidenceRecord

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_SENT = re.compile(r"[^.!?]{20,}[.!?]")


def _extract_citations(payload: dict) -> list[str]:
    """Pull citation URLs from the live OpenRouter Sonar response.

    Current shape (2026-06): citations are in choices[0].message.annotations as
    `{"type":"url_citation","url_citation":{"url":...}}` entries. Older/alt shape
    used a top-level `citations` list of URL strings — kept as a fallback. Never
    fabricates: returns only URLs actually present in the response.
    """
    msg = (payload.get("choices") or [{}])[0].get("message", {}) or {}
    urls: list[str] = []
    for ann in msg.get("annotations") or []:
        if ann.get("type") == "url_citation":
            url = (ann.get("url_citation") or {}).get("url")
            if url:
                urls.append(url)
    if not urls:
        urls = [u for u in (payload.get("citations") or []) if u]
    # de-dup, preserve order
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


async def collect_sonar(*, api_key: str, topic: str, model: str, timeout: float = 120.0) -> list[EvidenceRecord]:
    body = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": f"What are the most recent, specific user complaints and unmet needs about {topic}? "
                       f"Quote real users where possible. Cite sources.",
        }],
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(OPENROUTER_URL, headers=headers, json=body)
            resp.raise_for_status()
            payload = resp.json()
    except (httpx.HTTPError,):
        return []
    citations = _extract_citations(payload)
    if not citations:
        return []
    content = (payload.get("choices") or [{}])[0].get("message", {}).get("content", "")
    sentences = [s.strip() for s in _SENT.findall(content)][: len(citations)] or [content[:200]]
    recs = []
    for i, url in enumerate(citations):
        quote = sentences[i] if i < len(sentences) else sentences[-1]
        recs.append(EvidenceRecord(
            source_type="sonar", source_name="Perplexity Sonar", url=url,
            date="", quote=quote, engagement=0,
        ))
    return recs
