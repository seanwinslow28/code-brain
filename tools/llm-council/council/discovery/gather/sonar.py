# council/discovery/gather/sonar.py
"""Collector: Perplexity Sonar fresh-article harvest. Citation URLs are the evidence anchors."""

import re
import httpx

from council.discovery.evidence import EvidenceRecord

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_SENT = re.compile(r"[^.!?]{20,}[.!?]")


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
    citations = payload.get("citations") or []
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
