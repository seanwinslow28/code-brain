"""End-to-end pipeline test with mocked HTTP + mocked router. No live network."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest
import respx

from agents.job_feed import run_pipeline
from lib.job_types import Posting, ScoringResult

FIXTURES = Path(__file__).parent / "fixtures" / "job_feed"


@pytest.mark.asyncio
async def test_pipeline_writes_rollup_and_persists(tmp_path, monkeypatch):
    # Arrange: tiny watchlist + temp DB + temp roll-up dir
    watchlist = tmp_path / "watchlist.yaml"
    watchlist.write_text("ai_native:\n  - anthropic\n")
    db_path = tmp_path / ".job-feed.db"
    roll_up_dir = tmp_path / "job-feed"
    manifest_dir = tmp_path / "health"

    remoteok_body = (FIXTURES / "remoteok.json").read_text()
    gh_body = (FIXTURES / "greenhouse.json").read_text()

    # Mock router to always return MBP healthy + non-fallback
    router = MagicMock()
    router.route = AsyncMock(return_value=MagicMock(
        machine="macbook_pro", model="qwen3-14b",
        base_url="http://mbp:1234", runtime="lm-studio", is_fallback=False, reason="ok",
    ))

    # Mock the LLM completion to return a clean PM score
    async def fake_completion(base_url, model, prompt):
        return json.dumps({
            "fit_score": 4, "role_band": "PM",
            "rationale": "AI-native, remote-US PM role.",
            "concerns": [], "fit_dimensions": {"role_band_fit": 4, "geo_fit": 5, "industry_fit": 5, "yoe_fit": 4},
        })

    monkeypatch.setattr("lib.job_sources.get_credential", lambda n: None)

    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://remoteok.com/api").mock(return_value=httpx.Response(200, content=remoteok_body))
        mock.get("https://hn.algolia.com/api/v1/search").mock(return_value=httpx.Response(200, json={"hits": []}))
        mock.get("https://weworkremotely.com/categories/remote-product-jobs.rss").mock(return_value=httpx.Response(200, text=""))
        mock.get("https://boards-api.greenhouse.io/v1/boards/anthropic/jobs").mock(return_value=httpx.Response(200, content=gh_body))
        mock.get("https://api.lever.co/v0/postings/anthropic").mock(return_value=httpx.Response(404))
        mock.get("https://api.ashbyhq.com/posting-api/job-board/anthropic").mock(return_value=httpx.Response(404))
        # MBP probe: respond OK so the agent proceeds to scoring
        mock.head("http://mbp:1234/v1/models").mock(return_value=httpx.Response(200))
        mock.get("http://mbp:1234/v1/models").mock(return_value=httpx.Response(200, json={"data": []}))

        report = await run_pipeline(
            today_iso="2026-05-09",
            db_path=db_path,
            watchlist_path=watchlist,
            roll_up_dir=roll_up_dir,
            manifest_dir=manifest_dir,
            mbp_probe_url="http://mbp:1234/v1/models",
            mbp_probe_timeout_sec=2,
            http_timeout_sec=10,
            fetch_skip_if_within_hours=4,
            fallback_disabled=True,
            router=router,
            completion_fn=fake_completion,
        )

    # Assert: roll-up file exists, contains scored postings
    roll_up = roll_up_dir / "2026-05-09.md"
    assert roll_up.exists()
    body = roll_up.read_text()
    assert "complete: true" in body
    assert "Acme" in body or "Anthropic" in body
    assert report["mbp_reachable"] is True

    # Assert: SQLite persists rules-passed and rules-rejected
    with sqlite3.connect(db_path) as conn:
        total = conn.execute("SELECT COUNT(*) FROM job_postings").fetchone()[0]
        rejected = conn.execute("SELECT COUNT(*) FROM job_postings WHERE rules_passed=0").fetchone()[0]
    assert total >= 2  # at least the 2 RemoteOK rows and 1 Greenhouse row
    assert rejected >= 1  # the Director-of-Product row from remoteok.json


@pytest.mark.asyncio
async def test_pipeline_idempotent_when_complete_true(tmp_path):
    """If today's roll-up already has complete: true, pipeline exits ~50ms."""
    roll_up_dir = tmp_path / "job-feed"
    roll_up_dir.mkdir()
    (roll_up_dir / "2026-05-09.md").write_text(
        "---\ntype: job-feed-daily\ncomplete: true\ntotal_surfaced: 12\n---\n"
    )
    router = MagicMock()
    router.route = AsyncMock(side_effect=AssertionError("Must not call router when complete"))

    report = await run_pipeline(
        today_iso="2026-05-09",
        db_path=tmp_path / ".job-feed.db",
        watchlist_path=tmp_path / "wl.yaml",
        roll_up_dir=roll_up_dir,
        manifest_dir=tmp_path / "health",
        mbp_probe_url="http://x",
        mbp_probe_timeout_sec=2,
        http_timeout_sec=10,
        fetch_skip_if_within_hours=4,
        fallback_disabled=True,
        router=router,
        completion_fn=None,
    )
    assert report["short_circuited"] is True


@pytest.mark.asyncio
async def test_pipeline_mbp_unreachable_writes_partial(tmp_path, monkeypatch):
    """MBP down => rules-pass postings persisted with fit_score=NULL, complete=false."""
    watchlist = tmp_path / "watchlist.yaml"
    watchlist.write_text("ai_native:\n  - anthropic\n")
    monkeypatch.setattr("lib.job_sources.get_credential", lambda n: None)

    remoteok_body = (FIXTURES / "remoteok.json").read_text()
    gh_body = (FIXTURES / "greenhouse.json").read_text()

    with respx.mock(assert_all_called=False) as mock:
        mock.get("https://remoteok.com/api").mock(return_value=httpx.Response(200, content=remoteok_body))
        mock.get("https://hn.algolia.com/api/v1/search").mock(return_value=httpx.Response(200, json={"hits": []}))
        mock.get("https://weworkremotely.com/categories/remote-product-jobs.rss").mock(return_value=httpx.Response(200, text=""))
        mock.get("https://boards-api.greenhouse.io/v1/boards/anthropic/jobs").mock(return_value=httpx.Response(200, content=gh_body))
        mock.get("https://api.lever.co/v0/postings/anthropic").mock(return_value=httpx.Response(404))
        mock.get("https://api.ashbyhq.com/posting-api/job-board/anthropic").mock(return_value=httpx.Response(404))
        # MBP probe FAILS
        mock.head("http://mbp:1234/v1/models").mock(side_effect=httpx.ConnectError("MBP asleep"))

        report = await run_pipeline(
            today_iso="2026-05-09",
            db_path=tmp_path / ".job-feed.db",
            watchlist_path=watchlist,
            roll_up_dir=tmp_path / "job-feed",
            manifest_dir=tmp_path / "health",
            mbp_probe_url="http://mbp:1234/v1/models",
            mbp_probe_timeout_sec=2,
            http_timeout_sec=10,
            fetch_skip_if_within_hours=4,
            fallback_disabled=True,
            router=None,
            completion_fn=None,
        )

    roll_up = (tmp_path / "job-feed" / "2026-05-09.md").read_text()
    assert "complete: false" in roll_up
    assert report["mbp_reachable"] is False
