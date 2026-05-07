"""Tests for meta_agent.check_agent_health — CSV-driven health check."""

from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from agents import meta_agent


HEADER = ["date", "time", "agent", "mode", "status", "cost_usd", "duration_ms", "turns", "notes"]


def _write_history(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        for row in rows:
            w.writerow(row)


@pytest.fixture
def history_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point meta_agent at a tmp log dir for the duration of the test."""
    monkeypatch.setattr(meta_agent, "LOG_DIR_BASE", tmp_path)
    return tmp_path


def _now_row(agent: str, status: str, **extra) -> list[str]:
    now = datetime.now()
    return [
        now.strftime("%Y-%m-%d"),
        now.strftime("%H:%M:%S"),
        agent,
        extra.get("mode", ""),
        status,
        extra.get("cost_usd", "0.0000"),
        extra.get("duration_ms", "12345"),
        extra.get("turns", "2"),
        extra.get("notes", ""),
    ]


def _stale_row(agent: str, status: str, hours_ago: float) -> list[str]:
    ts = datetime.now() - timedelta(hours=hours_ago)
    return [
        ts.strftime("%Y-%m-%d"),
        ts.strftime("%H:%M:%S"),
        agent,
        "",
        status,
        "0.0000",
        "12345",
        "2",
        "",
    ]


class TestCheckAgentHealth:
    def test_dry_run_short_circuits(self, history_dir: Path):
        out = meta_agent.check_agent_health("deep_researcher", {}, dry_run=True)
        assert out["status"] == "healthy (dry-run)"

    def test_meta_agent_self_reports_healthy(self, history_dir: Path):
        # No CSV row exists for meta_agent — it doesn't record_run on itself.
        out = meta_agent.check_agent_health("meta_agent", {})
        assert out["status"] == "healthy"
        assert "Generating this report now" in out["details"]

    def test_no_csv_file_means_no_data(self, history_dir: Path):
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "no-data"

    def test_no_matching_row_means_no_data(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("vault-indexer", "success")],
        )
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "no-data"

    def test_recent_success_is_healthy(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("deep-researcher", "success", notes="id=abc wall=640s")],
        )
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "healthy"
        assert "status=success" in out["details"]
        assert "id=abc wall=640s" in out["details"]

    def test_hyphen_underscore_name_normalization(self, history_dir: Path):
        # CSV uses hyphens; ACTIVE_AGENTS uses underscores. Both must match.
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("vault-indexer", "success")],
        )
        out = meta_agent.check_agent_health("vault_indexer", {})
        assert out["status"] == "healthy"

    def test_recent_error_surfaces_as_error(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("deep-researcher", "error", notes="LDR timeout 900s")],
        )
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "error"
        assert "LDR timeout" in out["details"]

    def test_empty_queue_is_healthy(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("deep-researcher", "empty-queue", notes="no unchecked items")],
        )
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "healthy"

    def test_recursion_guard_is_healthy(self, history_dir: Path):
        # flush.py writes recursion-guard rows on rapid SessionEnd hooks; normal idle.
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("flush", "recursion-guard", notes="0 msgs")],
        )
        out = meta_agent.check_agent_health("flush", {})
        assert out["status"] == "healthy"

    def test_stale_success_flagged(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_stale_row("deep-researcher", "success", hours_ago=48)],
        )
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "stale"

    def test_weekly_agent_uses_wider_threshold(self, history_dir: Path):
        # knowledge-lint runs weekly (Sunday 22:00). 48h-old row must NOT
        # be flagged stale — weekly threshold is 192h.
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_stale_row("knowledge-lint", "success", hours_ago=48)],
        )
        out = meta_agent.check_agent_health("knowledge_lint", {})
        assert out["status"] == "healthy"

    def test_weekly_agent_still_goes_stale_past_threshold(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_stale_row("knowledge-lint", "success", hours_ago=240)],
        )
        out = meta_agent.check_agent_health("knowledge_lint", {})
        assert out["status"] == "stale"

    def test_picks_latest_row_among_many(self, history_dir: Path):
        rows = [
            _stale_row("deep-researcher", "error", hours_ago=72),
            _stale_row("deep-researcher", "success", hours_ago=48),
            _now_row("deep-researcher", "success", notes="fresh"),
        ]
        _write_history(history_dir / meta_agent.HISTORY_FILE_NAME, rows)
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "healthy"
        assert "fresh" in out["details"]

    def test_surfaces_cost_and_duration(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("daily-driver", "success", cost_usd="0.5161", duration_ms="86752", mode="morning")],
        )
        out = meta_agent.check_agent_health("daily_driver", {})
        assert out["cost_usd"] == pytest.approx(0.5161)
        assert out["duration_ms"] == 86752
        assert "mode=morning" in out["details"]
        assert "cost=$0.5161" in out["details"]

    def test_unknown_status_passes_through(self, history_dir: Path):
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("deep-researcher", "weird-status")],
        )
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert out["status"] == "weird-status"

    def test_long_notes_get_truncated(self, history_dir: Path):
        long_note = "x" * 200
        _write_history(
            history_dir / meta_agent.HISTORY_FILE_NAME,
            [_now_row("deep-researcher", "success", notes=long_note)],
        )
        out = meta_agent.check_agent_health("deep_researcher", {})
        assert "..." in out["details"]
        # snippet capped at 80 chars
        assert "x" * 100 not in out["details"]
