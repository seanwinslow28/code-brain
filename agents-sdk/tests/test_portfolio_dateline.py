"""Tests for lib.portfolio_dateline — the fleet→portfolio dateline bridge.

Hermetic: each test builds a temp repo_root with a fake agent-run-history.csv
and synth manifest, so no real vault or git state is touched.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path

from lib.portfolio_dateline import render_about_pulse, render_dateline, run_publish


def _write_fleet(repo_root: Path, *, critic_status: str, synth_status: str) -> None:
    """Seed a last-24h CSV (all runs structurally succeed) + a synth manifest.

    Rows are stamped one hour ago so they always fall inside the 24h window
    regardless of when the test runs.
    """
    logs = repo_root / "vault" / "90_system" / "agent-logs"
    logs.mkdir(parents=True, exist_ok=True)
    ts = datetime.now() - timedelta(hours=1)
    d, t = ts.strftime("%Y-%m-%d"), ts.strftime("%H:%M:%S")
    rows = [
        "date,time,agent,mode,status,cost_usd,duration_ms,turns,notes",
        f'{d},{t},vault-indexer,,success,0,11000,,"chunks=139, embeddings=139, errors=0"',
        f"{d},{t},vault-synthesizer,,success,0,2727,,concepts=2 connections=1 rejected=4 edges=2",
        f"{d},{t},vault-critic,,success,0,600,,status={critic_status} articles=0 ag_fail=5",
    ]
    (logs / "agent-run-history.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")

    health = repo_root / "vault" / "health"
    health.mkdir(parents=True, exist_ok=True)
    (health / "synth-manifest-2026-06-02.json").write_text(
        json.dumps({"concepts_written": 2, "connections_written": 1, "status": synth_status}),
        encoding="utf-8",
    )


def test_dateline_pulls_real_numbers(tmp_path):
    _write_fleet(tmp_path, critic_status="partial", synth_status="partial")
    body = render_dateline(tmp_path)["body"]
    assert "indexer wrote 139 chunks at" in body
    assert "synth landed 2 concepts + 1 connection" in body


def test_dateline_partial_night_never_claims_green(tmp_path):
    # The honesty thesis: a partial critic/synth must not render "fleet green".
    _write_fleet(tmp_path, critic_status="partial", synth_status="partial")
    body = render_dateline(tmp_path)["body"]
    assert "critic flagged partial" in body
    assert "morning fleet logged in" in body
    assert "fleet up." in body
    assert "green" not in body


def test_dateline_clean_night_is_green(tmp_path):
    _write_fleet(tmp_path, critic_status="ok", synth_status="ok")
    body = render_dateline(tmp_path)["body"]
    assert "morning fleet ran clean" in body
    assert "fleet green." in body


def test_about_pulse_counts_fleet_runs_and_daily_note(tmp_path):
    _write_fleet(tmp_path, critic_status="partial", synth_status="partial")

    labels = [i["label"] for i in render_about_pulse(tmp_path)["items"]]
    assert any("3 fleet runs" in s for s in labels)
    assert not any("daily note" in s for s in labels)  # none written yet

    daily = tmp_path / "vault" / "10_timeline" / "daily"
    daily.mkdir(parents=True, exist_ok=True)
    (daily / f"{date.today().isoformat()}.md").write_text("# note", encoding="utf-8")
    labels2 = [i["label"] for i in render_about_pulse(tmp_path)["items"]]
    assert any("1 daily note" in s for s in labels2)


def test_run_publish_noops_without_worktree(tmp_path):
    class _Cfg:
        repo_root = tmp_path
        vault_root = tmp_path / "vault"
        portfolio = {
            "enabled": True,
            "worktree_path": str(tmp_path / "does-not-exist"),
            "api_subpath": "public/api",
        }

    # Self-activating guard: must not raise or write when the worktree is absent.
    assert run_publish(_Cfg()) == "no-worktree"
