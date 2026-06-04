"""Tests for lib.portfolio_dateline — the fleet→portfolio dateline bridge.

Hermetic: each test builds a temp repo_root with a fake agent-run-history.csv
and synth manifest, so no real vault or git state is touched.
"""

from __future__ import annotations

import json
import subprocess
import urllib.error
from datetime import date, datetime, timedelta
from pathlib import Path

from lib import portfolio_dateline
from lib.portfolio_dateline import (
    _count_commits,
    commit_and_push,
    render_about_pulse,
    render_dateline,
    render_next_piece,
    render_shipped_stats,
    run_publish,
)


def _git_init(root: Path) -> None:
    """Init a hermetic git repo with a local identity (no global config needed)."""
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "t@t"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "t"], check=True)


def _commit(root: Path, subject: str) -> None:
    n = len(list(root.glob("f*.txt")))
    (root / f"f{n}.txt").write_text(subject, encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", subject], check=True)


class _FakeResp:
    """Minimal urlopen() context-manager stand-in."""

    def __init__(self, status: int, payload: dict) -> None:
        self.status = status
        self._payload = json.dumps(payload).encode("utf-8")

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, *_a):
        return False


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


# --- commit count -----------------------------------------------------------


def test_count_commits_excludes_vault_auto_commits(tmp_path):
    repo = tmp_path / "repo"
    _git_init(repo)
    _commit(repo, "feat: real work one")
    _commit(repo, "vault: auto-commit 2026-06-04 10:33:58")
    _commit(repo, "fix: real work two")
    _commit(repo, "vault: auto-commit 2026-06-04 11:33:58")
    # Only the two non-vault subjects count.
    assert _count_commits(repo) == 2


def test_count_commits_zero_outside_git_repo(tmp_path):
    # Non-fatal: a non-repo path yields 0, never an exception.
    assert _count_commits(tmp_path) == 0


def test_about_pulse_includes_commit_count(tmp_path):
    _write_fleet(tmp_path, critic_status="ok", synth_status="ok")
    _git_init(tmp_path)
    _commit(tmp_path, "feat: shipped a thing")
    items = render_about_pulse(tmp_path)["items"]
    assert items[0] == {"type": "commits", "count": 1, "label": "1 commit"}


# --- next-piece -------------------------------------------------------------


def test_next_piece_from_spec():
    out = render_next_piece({"title": "Vault Scorecard", "date_target": "2026-06-10"})
    assert out["title"] == "Vault Scorecard"
    assert out["date_target"] == "2026-06-10"
    assert "updated_at" in out


def test_next_piece_skips_when_block_or_field_missing():
    assert render_next_piece(None) is None
    assert render_next_piece({}) is None
    assert render_next_piece({"title": "x"}) is None  # no date_target
    assert render_next_piece({"date_target": "2026-06-10"}) is None  # no title


# --- shipped-stats (live npm + GitHub) --------------------------------------


def test_shipped_stats_live_fetch(monkeypatch):
    def fake_urlopen(req, timeout=10):
        url = req.full_url
        if "npmjs" in url:
            return _FakeResp(200, {"downloads": 47})
        return _FakeResp(200, {"stargazers_count": 8})

    monkeypatch.setattr(portfolio_dateline.urllib.request, "urlopen", fake_urlopen)
    out = render_shipped_stats(
        "intent-engineering-mcp", {"npm_package": "x", "github_repo": "a/b"}
    )
    assert out["slug"] == "intent-engineering-mcp"
    assert out["items"][0] == {"label": "weekly downloads", "value": "47", "unit": "npm"}
    assert out["items"][1] == {"label": "stars", "value": "8", "unit": "GitHub"}
    # The non-measurable "verified installs" row is intentionally dropped.
    assert not any(i["label"] == "verified installs" for i in out["items"])


def test_shipped_stats_skips_on_fetch_failure(monkeypatch):
    def boom(req, timeout=10):
        raise urllib.error.HTTPError(req.full_url, 404, "not found", {}, None)

    monkeypatch.setattr(portfolio_dateline.urllib.request, "urlopen", boom)
    # Honesty: a 404 must skip (None), never fabricate or zero.
    assert render_shipped_stats("s", {"npm_package": "x", "github_repo": "a/b"}) is None


def test_shipped_stats_skips_on_missing_identifiers():
    assert render_shipped_stats("s", {}) is None
    assert render_shipped_stats("s", {"npm_package": "x"}) is None
    assert render_shipped_stats("s", None) is None


# --- validation gate + commit message ---------------------------------------


def _publishable_cfg(tmp_path):
    worktree = tmp_path / "wt"
    (worktree / "public" / "api").mkdir(parents=True)

    class _Cfg:
        repo_root = tmp_path
        vault_root = tmp_path / "vault"
        portfolio = {
            "enabled": True,
            "worktree_path": str(worktree),
            "api_subpath": "public/api",
            "commit": True,
            "auto_push": False,
        }

    return _Cfg()


def test_run_publish_aborts_when_validation_fails(tmp_path, monkeypatch):
    _write_fleet(tmp_path, critic_status="ok", synth_status="ok")
    cfg = _publishable_cfg(tmp_path)

    monkeypatch.setattr(portfolio_dateline, "_validate_portfolio", lambda wt, **k: (False, "boom"))
    called = {"commit": False}

    def fake_commit(*a, **k):
        called["commit"] = True
        return "committed"

    monkeypatch.setattr(portfolio_dateline, "commit_and_push", fake_commit)

    assert run_publish(cfg) == "validation-failed (not pushed)"
    assert called["commit"] is False  # the gate must block the push


def test_run_publish_commits_when_validation_passes(tmp_path, monkeypatch):
    _write_fleet(tmp_path, critic_status="ok", synth_status="ok")
    cfg = _publishable_cfg(tmp_path)

    monkeypatch.setattr(portfolio_dateline, "_validate_portfolio", lambda wt, **k: (True, ""))
    monkeypatch.setattr(
        portfolio_dateline, "commit_and_push", lambda *a, **k: "committed + pushed to main"
    )

    assert run_publish(cfg) == "committed + pushed to main"


def test_commit_message_is_fleet_refresh(tmp_path):
    repo = tmp_path / "repo"
    _git_init(repo)
    (repo / "x.json").write_text("1", encoding="utf-8")
    status = commit_and_push(repo, ["x.json"], do_push=False, today=date(2026, 6, 4))
    assert status == "committed (push disabled — auto_push=false)"
    out = subprocess.run(
        ["git", "-C", str(repo), "log", "-1", "--pretty=%s"],
        capture_output=True, text=True, check=True,
    )
    assert out.stdout.strip() == "chore(daily): fleet refresh 2026-06-04"
