# council/discovery/gather/github.py
"""Collector: GitHub Issues — explicit, upvoted unmet needs (strongest pm-lens signal).

Free GitHub Search API (https://docs.github.com/rest/search/search#search-issues-and-pull-requests).
Works unauthenticated (low rate limit); reads an optional GITHUB_TOKEN from the env for a higher
limit. Each issue is a real html_url + a verbatim title quote → fabrication-gate-compatible.
"""

import os

import httpx

from council.discovery.evidence import EvidenceRecord
from council.discovery.textbudget import GITHUB_Q_MAX_CHARS, clamp_words_chars

GITHUB_SEARCH_URL = "https://api.github.com/search/issues"


def _repo_from_html_url(html_url: str) -> str:
    # https://github.com/owner/repo/issues/123 → "owner/repo"
    parts = html_url.split("/")
    if "github.com" in html_url and len(parts) >= 5:
        return f"{parts[3]}/{parts[4]}"
    return "github"


def _default_github_search(token: str | None):
    async def search(query: str) -> list[dict]:
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.get(GITHUB_SEARCH_URL, headers=headers,
                            params={"q": query, "sort": "reactions", "order": "desc", "per_page": 12})
            r.raise_for_status()
            return r.json().get("items", [])
    return search


async def collect_github(*, topic: str, segment: str = "", search=..., max_results: int = 8) -> list[EvidenceRecord]:
    if search is ...:
        search = _default_github_search(os.environ.get("GITHUB_TOKEN"))
    if search is None:
        return []
    subject = f"{topic} {segment}".strip() if segment else topic
    # GitHub search q caps at ~256 chars; clamp the subject so the ` in:title,body is:issue` operators
    # still fit and a long topic/--segment can't 422 the search.
    subject = clamp_words_chars(subject, max_words=40, max_chars=GITHUB_Q_MAX_CHARS - 40)
    items = await search(f"{subject} in:title,body is:issue")
    recs: list[EvidenceRecord] = []
    for it in items[:max_results]:
        url = it.get("html_url", "")
        title = it.get("title", "")
        if not (url and title):
            continue
        reactions = (it.get("reactions") or {}).get("total_count", 0) or 0
        recs.append(EvidenceRecord(
            source_type="github", source_name=_repo_from_html_url(url), url=url,
            date=(it.get("created_at") or "")[:10], quote=title, engagement=int(reactions),
        ))
    return recs
