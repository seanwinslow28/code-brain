"""Feed + ATS adapters for the job-feed agent.

Each adapter implements:
    name: str                                          # 'remoteok', 'hn', 'greenhouse:<slug>', ...
    async def fetch(self, since) -> list[Posting]     # since=None ⇒ everything available

All adapters take an injected httpx.AsyncClient so the orchestrator can apply
a shared per-host semaphore (1 req/sec/host) and rate-limit politely.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx
from markdownify import markdownify

from lib.job_types import Posting

USER_AGENT = "SeanWinslow-JobFeed/1.0 (personal job-hunt agent)"


def _html_to_md(html: str | None) -> str:
    if not html:
        return ""
    return markdownify(html).strip()


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def _format_salary(lo: int | None, hi: int | None) -> str | None:
    if lo is None and hi is None:
        return None
    if lo is not None and hi is not None:
        return f"${lo}-${hi}"
    return f"${lo or hi}"


class RemoteOKAdapter:
    name = "remoteok"
    url = "https://remoteok.com/api"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def fetch(self, since: datetime | None) -> list[Posting]:
        resp = await self.client.get(self.url, headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        rows: list[dict[str, Any]] = resp.json()

        postings: list[Posting] = []
        for row in rows:
            # Skip the metadata row (no "id" key)
            if "id" not in row:
                continue
            posted = _parse_iso(row.get("date"))
            if since and posted and posted < since:
                continue
            postings.append(Posting(
                source=self.name,
                source_role_id=str(row["id"]),
                url=row.get("url", ""),
                company=row.get("company", ""),
                title=row.get("position", ""),
                location=row.get("location"),
                salary_disclosed=_format_salary(row.get("salary_min"), row.get("salary_max")),
                posted_at=posted,
                description=_html_to_md(row.get("description", "")),
            ))
        return postings
