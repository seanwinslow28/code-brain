import json
from datetime import datetime
from pathlib import Path

import pytest
import respx
import httpx

from lib.job_sources import RemoteOKAdapter, HNWhoIsHiringAdapter, Web3CareerAdapter, WeWorkRemotelyAdapter, GreenhouseAdapter, LeverAdapter, AshbyAdapter, fetch_ats, fetch_all
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


@pytest.mark.asyncio
async def test_web3career_adapter_uses_token(monkeypatch):
    monkeypatch.setattr("lib.job_sources.get_credential", lambda name: "fake-token")
    body = (FIXTURES / "web3career.json").read_text()
    captured = {}

    def _capture(request):
        captured["url"] = str(request.url)
        return httpx.Response(200, content=body)

    with respx.mock(base_url="https://web3.career") as mock:
        mock.get("/api/v1").mock(side_effect=_capture)
        async with httpx.AsyncClient() as client:
            adapter = Web3CareerAdapter(client=client)
            postings = await adapter.fetch(since=None)

    assert "token=fake-token" in captured["url"]
    assert len(postings) == 1
    assert postings[0].company == "Messari"
    assert postings[0].source == "web3career"


@pytest.mark.asyncio
async def test_web3career_adapter_skips_when_token_missing(monkeypatch, caplog):
    monkeypatch.setattr("lib.job_sources.get_credential", lambda name: None)
    async with httpx.AsyncClient() as client:
        adapter = Web3CareerAdapter(client=client)
        postings = await adapter.fetch(since=None)
    assert postings == []


@pytest.mark.asyncio
async def test_wwr_adapter_parses_rss():
    body = (FIXTURES / "wwr.rss").read_text()
    with respx.mock(base_url="https://weworkremotely.com") as mock:
        mock.get("/categories/remote-product-jobs.rss").mock(
            return_value=httpx.Response(200, content=body)
        )
        async with httpx.AsyncClient() as client:
            adapter = WeWorkRemotelyAdapter(client=client)
            postings = await adapter.fetch(since=None)

    assert len(postings) == 1
    p = postings[0]
    assert p.source == "wwr"
    assert p.company == "Acme"
    assert p.title == "Product Manager"
    assert p.url == "https://weworkremotely.com/remote-jobs/acme-pm-5001"
    assert p.source_role_id == "https://weworkremotely.com/remote-jobs/acme-pm-5001"


@pytest.mark.asyncio
async def test_greenhouse_adapter_parses():
    body = (FIXTURES / "greenhouse.json").read_text()
    with respx.mock(base_url="https://boards-api.greenhouse.io") as mock:
        mock.get("/v1/boards/anthropic/jobs").mock(
            return_value=httpx.Response(200, content=body)
        )
        async with httpx.AsyncClient() as client:
            adapter = GreenhouseAdapter("anthropic", client=client)
            postings = await adapter.fetch(since=None)
    assert len(postings) == 1
    p = postings[0]
    assert p.source == "greenhouse:anthropic"
    assert p.company == "Anthropic"
    assert p.salary_disclosed == "$180k-$220k"


@pytest.mark.asyncio
async def test_lever_adapter_parses():
    body = (FIXTURES / "lever.json").read_text()
    with respx.mock(base_url="https://api.lever.co") as mock:
        mock.get("/v0/postings/figma").mock(
            return_value=httpx.Response(200, content=body)
        )
        async with httpx.AsyncClient() as client:
            adapter = LeverAdapter("figma", client=client)
            postings = await adapter.fetch(since=None)
    assert postings[0].source == "lever:figma"
    assert postings[0].company == "Figma"
    assert postings[0].salary_disclosed == "$140000-$180000"


@pytest.mark.asyncio
async def test_ashby_adapter_parses():
    body = (FIXTURES / "ashby.json").read_text()
    with respx.mock(base_url="https://api.ashbyhq.com") as mock:
        mock.get("/posting-api/job-board/hopper").mock(
            return_value=httpx.Response(200, content=body)
        )
        async with httpx.AsyncClient() as client:
            adapter = AshbyAdapter("hopper", client=client)
            postings = await adapter.fetch(since=None)
    assert postings[0].source == "ashby:hopper"


@pytest.mark.asyncio
async def test_fetch_ats_walks_greenhouse_then_lever_then_ashby():
    """Greenhouse 404 -> Lever 200 wins; Ashby is never called."""
    body = (FIXTURES / "lever.json").read_text()
    with respx.mock() as mock:
        mock.get("https://boards-api.greenhouse.io/v1/boards/figma/jobs").mock(
            return_value=httpx.Response(404)
        )
        mock.get("https://api.lever.co/v0/postings/figma").mock(
            return_value=httpx.Response(200, content=body)
        )
        async with httpx.AsyncClient() as client:
            postings, source_used = await fetch_ats("figma", client=client)
    assert source_used == "lever"
    assert len(postings) == 1


@pytest.mark.asyncio
async def test_fetch_ats_returns_empty_when_all_404():
    with respx.mock() as mock:
        mock.get("https://boards-api.greenhouse.io/v1/boards/nope/jobs").mock(
            return_value=httpx.Response(404)
        )
        mock.get("https://api.lever.co/v0/postings/nope").mock(
            return_value=httpx.Response(404)
        )
        mock.get("https://api.ashbyhq.com/posting-api/job-board/nope").mock(
            return_value=httpx.Response(404)
        )
        async with httpx.AsyncClient() as client:
            postings, source_used = await fetch_ats("nope", client=client)
    assert postings == []
    assert source_used is None


@pytest.mark.asyncio
async def test_fetch_all_aggregates_feeds_and_ats(monkeypatch):
    monkeypatch.setattr("lib.job_sources.get_credential", lambda n: None)  # no web3 token
    remoteok_body = (FIXTURES / "remoteok.json").read_text()
    gh_body = (FIXTURES / "greenhouse.json").read_text()

    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://remoteok.com/api").mock(return_value=httpx.Response(200, content=remoteok_body))
        mock.get("https://hn.algolia.com/api/v1/search").mock(return_value=httpx.Response(200, json={"hits": []}))
        mock.get("https://weworkremotely.com/categories/remote-product-jobs.rss").mock(return_value=httpx.Response(200, text=""))
        mock.get("https://boards-api.greenhouse.io/v1/boards/anthropic/jobs").mock(return_value=httpx.Response(200, content=gh_body))
        mock.get("https://api.lever.co/v0/postings/anthropic").mock(return_value=httpx.Response(404))
        mock.get("https://api.ashbyhq.com/posting-api/job-board/anthropic").mock(return_value=httpx.Response(404))

        postings, failed = await fetch_all(
            watchlist_slugs=["anthropic"],
            http_timeout_sec=10,
        )

    assert any(p.source == "remoteok" for p in postings)
    assert any(p.source.startswith("greenhouse:") for p in postings)
    assert failed == []  # no failed pollers
