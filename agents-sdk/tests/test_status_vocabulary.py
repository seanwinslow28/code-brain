"""The status-token registry — eng-002.d158, the third instance of d21.

``_HEALTHY_CSV_STATUSES`` was an allow-list with an else-branch, so any token
it had never heard of read as an agent failure and paged a human. That has now
mislabelled three different tokens:

* ``"ok"``      — flush's healthy token (eng-001.d21, fixed at Phase 0).
* ``"deferred"``— the vault synthesizer's *designed* off-LAN deferral. BT5
  rebuilt it in 2026-07 precisely so an off-LAN night would defer cleanly
  instead of poll-storming; the agent was taught to defer honestly and the
  monitor was never taught that deferral is honest. Measured 2026-08-26.
* ``"error_max_budget_usd"`` — a real daily-driver failure reported as
  ``unknown`` rather than ``error``.

The shape is always the same: a token nobody registered becomes a lie about an
agent. The registry below closes the class rather than the instance. An
*unregistered* token is now a defect in the monitor and says so, instead of
silently blaming the agent it was watching.

Live census, `agent-run-history.csv` on seans-mac-mini.local, 2026-08-30:
success 1268 · recursion-guard 483 · empty-queue 99 · error 71 · ok 19 ·
deferred 9 · partial 5 · error_max_budget_usd 3 · partial-empty 2.
"""

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


def _row(agent: str, status: str, hours_ago: float = 0.0) -> list[str]:
    ts = datetime.now() - timedelta(hours=hours_ago)
    return [
        ts.strftime("%Y-%m-%d"), ts.strftime("%H:%M:%S"), agent, "", status,
        "0.0000", "12345", "2", "",
    ]


@pytest.fixture
def history_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(meta_agent, "LOG_DIR_BASE", tmp_path)
    return tmp_path


def _health(history_dir: Path, agent: str, status: str) -> dict:
    _write_history(history_dir / meta_agent.HISTORY_FILE_NAME, [_row(agent, status)])
    return meta_agent.check_agent_health(agent, {}, False)


# ── the defect that blocks B3 ───────────────────────────────────────────────

def test_deferred_is_healthy(history_dir: Path):
    """An off-LAN deferral is the design working, not an agent failing.

    This is the one that would have reset B3's seven-night streak: the
    synthesizer deferred on 2026-08-26 and the monitor called it unhealthy.
    """
    assert _health(history_dir, "vault_synthesizer", "deferred")["status"] == "healthy"


def test_deferred_raises_no_alert(history_dir: Path):
    """The end-to-end consequence, not just the label: no page for a clean defer."""
    _write_history(
        history_dir / meta_agent.HISTORY_FILE_NAME,
        [_row(a, "deferred" if a == "vault_synthesizer" else "success")
         for a in meta_agent.ACTIVE_AGENTS],
    )
    alerts = meta_agent.collect_fleet_alerts({}, False)
    assert [a for a in alerts if a[0] == "vault_synthesizer"] == []


def test_deferred_still_ages_into_stale(history_dir: Path):
    """Routed *through* the healthy branch, not around it — a token that can
    never go stale was never really recognised."""
    _write_history(
        history_dir / meta_agent.HISTORY_FILE_NAME,
        [_row("vault_synthesizer", "deferred",
              hours_ago=meta_agent._STALE_AFTER_HOURS.get(
                  "vault_synthesizer", meta_agent.HEALTH_WINDOW_HOURS) + 5)],
    )
    assert meta_agent.check_agent_health("vault_synthesizer", {}, False)["status"] == "stale"


# ── a real error, correctly named ───────────────────────────────────────────

def test_budget_stop_is_an_error_not_unknown(history_dir: Path):
    """`error_max_budget_usd` alerted only by falling through the else-branch.
    It is a genuine failure and must be labelled one; the daily note may be
    missing when it fires."""
    assert _health(history_dir, "daily_driver", "error_max_budget_usd")["status"] == "error"


# ── degraded: still pages, but says what it is ──────────────────────────────

@pytest.mark.parametrize("agent,status", [
    ("job_feed", "partial"),            # fetch=3674 scored=0 — the scoring leg died
    ("vault_synthesizer", "partial-empty"),  # concepts=0 connections=0 — produced nothing
])
def test_partial_runs_are_degraded_and_alert(history_dir: Path, agent: str, status: str):
    """A run that fetched thousands and scored none is not healthy. It keeps
    paging — but as `degraded`, so the report distinguishes 'worked badly'
    from 'did not run' and from 'the monitor has no idea'."""
    assert _health(history_dir, agent, status)["status"] == "degraded"
    _write_history(history_dir / meta_agent.HISTORY_FILE_NAME, [_row(agent, status)])
    assert any(a[0] == agent for a in meta_agent.collect_fleet_alerts({}, False))


# ── the structural fix: unknown tokens accuse the monitor, not the agent ────

def test_unregistered_token_is_a_monitoring_defect(history_dir: Path):
    """The generator of all three bugs above.

    An unregistered token must not read as an agent failure — that is what
    made 'ok' and 'deferred' into lies about healthy agents. It surfaces
    loudly, but as the monitor's own defect.
    """
    result = _health(history_dir, "flush", "some-new-token-nobody-registered")
    assert result["status"] == "unclassified-status"
    assert "some-new-token-nobody-registered" in result["details"]
    assert "monitor" in result["details"].lower()


def test_unregistered_token_still_surfaces(history_dir: Path):
    """Loud, never silent — an unclassified token must still reach a human,
    or the fix would trade a false positive for a false negative."""
    _write_history(
        history_dir / meta_agent.HISTORY_FILE_NAME,
        [_row(a, "brand-new-token" if a == "flush" else "success")
         for a in meta_agent.ACTIVE_AGENTS],
    )
    assert any(a[0] == "flush" for a in meta_agent.collect_fleet_alerts({}, False))


def test_every_live_token_is_registered():
    """The census from production on 2026-08-30. If an agent gains a status
    token, this test is where it gets classified — deliberately, once."""
    for token in ("success", "ok", "empty-queue", "recursion-guard",
                  "deferred", "error", "error_max_budget_usd",
                  "partial", "partial-empty"):
        assert token in meta_agent.STATUS_VOCABULARY, f"unregistered live token: {token}"


def test_registry_classifications_are_closed():
    """Every registered token maps to one of the three known classes; a typo
    in the registry cannot invent a fourth."""
    assert set(meta_agent.STATUS_VOCABULARY.values()) <= {"healthy", "error", "degraded"}
