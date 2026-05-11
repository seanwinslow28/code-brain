"""Feed + ATS adapters for the job-feed agent.

Each adapter implements:
    name: str                                          # 'remoteok', 'hn', 'greenhouse:<slug>', ...
    async def fetch(self, since) -> list[Posting]     # since=None ⇒ everything available

All adapters take an injected httpx.AsyncClient so the orchestrator can apply
a shared per-host semaphore (1 req/sec/host) and rate-limit politely.

# web3.career requires a free API token. One-time setup:
#   python3 agents-sdk/lib/keychain.py set web3career_token <token>
# Followed by:
#   security find-generic-password -s com.sean.agents.web3career_token  # verify
# If the token is missing, the adapter logs a warning and returns [] (does not raise).
"""

from __future__ import annotations

import asyncio
import logging
import re
from datetime import datetime, timezone
from typing import Any

import feedparser
import httpx
from markdownify import markdownify

from lib.job_types import Posting
from lib.keychain import get_credential

USER_AGENT = "SeanWinslow-JobFeed/1.0 (personal job-hunt agent)"
_logger = logging.getLogger(__name__)


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


# Pipe-delimited "Company | Title | Location | Type" — the de-facto HN format
_HN_HEAD_RE = re.compile(r"^([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+?)(?:\s*\|\s*(.+))?\s*$")
_URL_RE = re.compile(r'https?://[^\s<>"\']+')


class HNWhoIsHiringAdapter:
    name = "hn"
    search_url = "https://hn.algolia.com/api/v1/search"
    by_date_url = "https://hn.algolia.com/api/v1/search_by_date"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def fetch(self, since: datetime | None) -> list[Posting]:
        # 1. Find current month's "Who is hiring" thread
        r = await self.client.get(
            self.search_url,
            params={"tags": "story", "query": "Ask HN Who is hiring"},
            headers={"User-Agent": USER_AGENT},
        )
        r.raise_for_status()
        hits = r.json().get("hits", [])
        if not hits:
            return []
        # Most recent thread first
        thread = sorted(hits, key=lambda h: h.get("created_at", ""), reverse=True)[0]
        thread_id = thread["objectID"]

        # 2. Pull top-level comments under that thread
        r = await self.client.get(
            self.by_date_url,
            params={"tags": f"comment,story_{thread_id}", "hitsPerPage": 1000},
            headers={"User-Agent": USER_AGENT},
        )
        r.raise_for_status()
        comments = r.json().get("hits", [])

        postings: list[Posting] = []
        for c in comments:
            text = c.get("comment_text") or ""
            md = _html_to_md(text)
            # Look at the first non-blank line
            first_line = next((ln.strip() for ln in md.splitlines() if ln.strip()), "")
            m = _HN_HEAD_RE.match(first_line)
            if not m:
                continue  # Not a pipe-delimited job ad — drop (heuristic 70-80% precision)
            company, title, location, _kind = m.group(1, 2, 3, 4)
            url_match = _URL_RE.search(md)
            if not url_match:
                continue
            posted = _parse_iso(c.get("created_at"))
            if since and posted and posted < since:
                continue
            postings.append(Posting(
                source=self.name,
                source_role_id=str(c["objectID"]),
                url=url_match.group(0),
                company=company.strip(),
                title=title.strip(),
                location=location.strip(),
                salary_disclosed=None,
                posted_at=posted,
                description=md,
            ))
        return postings


class Web3CareerAdapter:
    name = "web3career"
    base_url = "https://web3.career/api/v1"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def fetch(self, since: datetime | None) -> list[Posting]:
        token = get_credential("web3career_token")
        if not token:
            _logger.warning("web3career_token missing from Keychain — skipping web3.career fetch")
            return []

        r = await self.client.get(
            self.base_url,
            params={"token": token},
            headers={"User-Agent": USER_AGENT},
        )
        r.raise_for_status()
        rows = r.json().get("jobs", [])

        postings: list[Posting] = []
        for row in rows:
            posted = _parse_iso(row.get("created_at"))
            if since and posted and posted < since:
                continue
            postings.append(Posting(
                source=self.name,
                source_role_id=str(row.get("id") or row.get("slug")),
                url=row.get("url", ""),
                company=row.get("company", ""),
                title=row.get("title", ""),
                location=row.get("location"),
                salary_disclosed=row.get("salary"),
                posted_at=posted,
                description=_html_to_md(row.get("description", "")),
            ))
        return postings


class WeWorkRemotelyAdapter:
    name = "wwr"
    rss_url = "https://weworkremotely.com/categories/remote-product-jobs.rss"

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def fetch(self, since: datetime | None) -> list[Posting]:
        r = await self.client.get(self.rss_url, headers={"User-Agent": USER_AGENT})
        r.raise_for_status()
        feed = feedparser.parse(r.text)

        postings: list[Posting] = []
        for entry in feed.entries:
            # WWR titles are formatted "Company: Title" — split on first colon
            raw_title = entry.get("title", "")
            if ":" in raw_title:
                company, _, title = raw_title.partition(":")
                company = company.strip()
                title = title.strip()
            else:
                company, title = "", raw_title.strip()

            link = entry.get("link", "")
            posted_struct = entry.get("published_parsed")
            posted = datetime(*posted_struct[:6]) if posted_struct else None
            if since and posted and posted < since:
                continue

            postings.append(Posting(
                source=self.name,
                source_role_id=link or entry.get("id", ""),
                url=link,
                company=company,
                title=title,
                location=None,
                salary_disclosed=None,
                posted_at=posted,
                description=_html_to_md(entry.get("description", "")),
            ))
        return postings


class GreenhouseAdapter:
    base = "https://boards-api.greenhouse.io/v1/boards"

    def __init__(self, slug: str, client: httpx.AsyncClient) -> None:
        self.slug = slug
        self.client = client
        self.name = f"greenhouse:{slug}"

    async def fetch(self, since: datetime | None) -> list[Posting]:
        r = await self.client.get(
            f"{self.base}/{self.slug}/jobs",
            params={"content": "true"},
            headers={"User-Agent": USER_AGENT},
        )
        r.raise_for_status()  # 404 raises httpx.HTTPStatusError; fetch_ats walks on that
        rows = r.json().get("jobs", [])
        postings: list[Posting] = []
        for row in rows:
            salary = next(
                (m["value"] for m in row.get("metadata") or [] if m.get("name") == "Salary"),
                None,
            )
            posted = _parse_iso(row.get("updated_at"))
            if since and posted and posted < since:
                continue
            postings.append(Posting(
                source=self.name,
                source_role_id=str(row["id"]),
                url=row.get("absolute_url", ""),
                company=row.get("company_name") or self.slug.title(),
                title=row.get("title", ""),
                location=(row.get("location") or {}).get("name"),
                salary_disclosed=salary,
                posted_at=posted,
                description=_html_to_md(row.get("content", "")),
            ))
        return postings


class LeverAdapter:
    base = "https://api.lever.co/v0/postings"

    def __init__(self, slug: str, client: httpx.AsyncClient) -> None:
        self.slug = slug
        self.client = client
        self.name = f"lever:{slug}"

    async def fetch(self, since: datetime | None) -> list[Posting]:
        r = await self.client.get(
            f"{self.base}/{self.slug}",
            params={"mode": "json"},
            headers={"User-Agent": USER_AGENT},
        )
        r.raise_for_status()
        rows = r.json()
        postings: list[Posting] = []
        for row in rows:
            sr = row.get("salaryRange") or {}
            salary = _format_salary(sr.get("min"), sr.get("max"))
            ts = row.get("createdAt")
            posted = datetime.fromtimestamp(ts / 1000, tz=timezone.utc) if ts else None
            if since and posted and posted < since:
                continue
            cats = row.get("categories") or {}
            postings.append(Posting(
                source=self.name,
                source_role_id=str(row.get("id")),
                url=row.get("hostedUrl", ""),
                company=self.slug.title(),
                title=row.get("text", ""),
                location=cats.get("location"),
                salary_disclosed=salary,
                posted_at=posted,
                description=_html_to_md(row.get("descriptionPlain", "")),
            ))
        return postings


class AshbyAdapter:
    base = "https://api.ashbyhq.com/posting-api/job-board"

    def __init__(self, slug: str, client: httpx.AsyncClient) -> None:
        self.slug = slug
        self.client = client
        self.name = f"ashby:{slug}"

    async def fetch(self, since: datetime | None) -> list[Posting]:
        r = await self.client.get(
            f"{self.base}/{self.slug}",
            params={"includeCompensation": "true"},
            headers={"User-Agent": USER_AGENT},
        )
        r.raise_for_status()
        rows = r.json().get("jobs", [])
        postings: list[Posting] = []
        for row in rows:
            posted = _parse_iso(row.get("publishedDate"))
            if since and posted and posted < since:
                continue
            postings.append(Posting(
                source=self.name,
                source_role_id=str(row.get("id")),
                url=row.get("applyUrl", ""),
                company=self.slug.title(),
                title=row.get("title", ""),
                location=row.get("locationName"),
                salary_disclosed=(row.get("compensation") or {}).get("compensationTierSummary"),
                posted_at=posted,
                description=_html_to_md(row.get("descriptionHtml", "")),
            ))
        return postings


async def fetch_ats(
    slug: str, client: httpx.AsyncClient
) -> tuple[list[Posting], str | None]:
    """Try Greenhouse -> Lever -> Ashby; first non-404 wins. Returns ([], None) if all 404."""
    for cls, label in [
        (GreenhouseAdapter, "greenhouse"),
        (LeverAdapter, "lever"),
        (AshbyAdapter, "ashby"),
    ]:
        adapter = cls(slug, client=client)
        try:
            postings = await adapter.fetch(since=None)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                continue
            raise
        return postings, label
    return [], None


async def fetch_all(
    watchlist_slugs: list[str],
    http_timeout_sec: int = 10,
) -> tuple[list[Posting], list[str]]:
    """Run all 4 feed adapters + ATS pollers for each watchlist slug in parallel.

    Returns: (combined_postings, failed_poller_labels)
    """
    failed: list[str] = []
    transport = httpx.AsyncHTTPTransport(retries=2)
    timeout = httpx.Timeout(http_timeout_sec)

    async with httpx.AsyncClient(transport=transport, timeout=timeout, follow_redirects=True) as client:
        feed_adapters = [
            RemoteOKAdapter(client=client),
            HNWhoIsHiringAdapter(client=client),
            Web3CareerAdapter(client=client),
            WeWorkRemotelyAdapter(client=client),
        ]

        async def _safe_feed(adapter):
            try:
                return await adapter.fetch(since=None)
            except Exception as exc:
                _logger.warning("Feed adapter %s failed: %s", adapter.name, exc)
                failed.append(adapter.name)
                return []

        async def _safe_ats(slug):
            try:
                postings, label = await fetch_ats(slug, client=client)
                if label is None:
                    failed.append(f"ats:{slug} (all 404)")
                return postings
            except Exception as exc:
                _logger.warning("ATS poll %s failed: %s", slug, exc)
                failed.append(f"ats:{slug} ({type(exc).__name__})")
                return []

        feed_results = await asyncio.gather(*[_safe_feed(a) for a in feed_adapters])
        ats_results = await asyncio.gather(*[_safe_ats(s) for s in watchlist_slugs])

    combined: list[Posting] = []
    for batch in feed_results + ats_results:
        combined.extend(batch)
    return combined, failed
