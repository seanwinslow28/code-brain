import json
from datetime import datetime
from pathlib import Path

import pytest
import respx
import httpx

from lib.job_sources import RemoteOKAdapter, HNWhoIsHiringAdapter
from lib.job_types import Posting

FIXTURES = Path(__file__).parent / "fixtures" / "job_feed"


@pytest.mark.asyncio
async def test_remoteok_adapter_parses_postings():
    body = (FIXTURES / "remoteok.json").read_text()
    with respx.mock(base_url="https://remoteok.com") as mock:
        mock.get("/api").mock(return_value=httpx.Response(200, content=body))
        async with httpx.AsyncClient() as client:
            adapter = RemoteOKAdapter(client=client)
            postings = await adapter.fetch(since=None)

    assert len(postings) == 2
    pm = postings[0]
    assert isinstance(pm, Posting)
    assert pm.source == "remoteok"
    assert pm.source_role_id == "remoteok-1001"
    assert pm.company == "Acme"
    assert pm.title == "Product Manager"
    assert pm.url == "https://remoteok.com/remote-jobs/1001"
    assert pm.location == "Worldwide"
    assert pm.salary_disclosed == "$110000-$140000"
    assert pm.posted_at == datetime.fromisoformat("2026-05-09T08:00:00+00:00")
    assert "We're hiring a PM" in pm.description  # HTML stripped via markdownify


@pytest.mark.asyncio
async def test_remoteok_adapter_skips_metadata_row():
    body = '[{"legal": "RemoteOK API"}]'
    with respx.mock(base_url="https://remoteok.com") as mock:
        mock.get("/api").mock(return_value=httpx.Response(200, content=body))
        async with httpx.AsyncClient() as client:
            adapter = RemoteOKAdapter(client=client)
            postings = await adapter.fetch(since=None)
    assert postings == []


@pytest.mark.asyncio
async def test_remoteok_adapter_handles_empty_salary():
    body = json.dumps([
        {"legal": "RemoteOK"},
        {
            "id": "rok-3", "url": "https://x.example/3", "company": "C",
            "position": "PM", "location": None, "salary_min": None, "salary_max": None,
            "date": "2026-05-09T08:00:00+00:00", "description": "x",
        },
    ])
    with respx.mock(base_url="https://remoteok.com") as mock:
        mock.get("/api").mock(return_value=httpx.Response(200, content=body))
        async with httpx.AsyncClient() as client:
            adapter = RemoteOKAdapter(client=client)
            postings = await adapter.fetch(since=None)
    assert postings[0].salary_disclosed is None


@pytest.mark.asyncio
async def test_hn_adapter_parses_pipe_delimited_postings():
    thread = (FIXTURES / "hn_thread.json").read_text()
    comments = (FIXTURES / "hn_comments.json").read_text()
    with respx.mock(base_url="https://hn.algolia.com") as mock:
        mock.get("/api/v1/search").mock(return_value=httpx.Response(200, content=thread))
        mock.get("/api/v1/search_by_date").mock(return_value=httpx.Response(200, content=comments))
        async with httpx.AsyncClient() as client:
            adapter = HNWhoIsHiringAdapter(client=client)
            postings = await adapter.fetch(since=None)

    # The pipe-delimited Anthropic ad is parsed; the non-pipe comment is dropped.
    assert len(postings) == 1
    p = postings[0]
    assert p.source == "hn"
    assert p.source_role_id == "40000002"
    assert p.company == "Anthropic"
    assert "Product Manager" in p.title
    assert p.url == "https://anthropic.com/careers/pm"
    assert "REMOTE (US)" in (p.location or "")


@pytest.mark.asyncio
async def test_hn_adapter_returns_empty_when_no_thread():
    with respx.mock(base_url="https://hn.algolia.com") as mock:
        mock.get("/api/v1/search").mock(return_value=httpx.Response(200, json={"hits": []}))
        async with httpx.AsyncClient() as client:
            adapter = HNWhoIsHiringAdapter(client=client)
            postings = await adapter.fetch(since=None)
    assert postings == []
