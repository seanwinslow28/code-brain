"""Phase 0 P0 fixes from the eng-001 fleet audit (eng-002 B3 + the note assertion).

Three defects, one file:

* **eng-001.d21 — crying wolf.** ``flush.py`` records ``status="ok"`` on every
  healthy run, but ``_HEALTHY_CSV_STATUSES`` never held ``"ok"``, so every
  healthy flush fell through to the else-branch and tripped the alert baton.
* **eng-001.d40 — no delivery path.** The meta-agent detected failures and only
  ``print()``-ed them. Detection existed; awareness did not (MTTA was three
  nights, closed by an external audit).
* **daily-driver note assertion.** The SDK can report ``success`` on a morning
  run that never wrote the daily note. A green row for an absent artifact is
  the same defect class: the record says fine, the vault says nothing.
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


# ── eng-001.d21 — the crying-wolf status-vocabulary mismatch ─────────────────

def test_flush_ok_reads_healthy(history_dir: Path):
    """flush's own healthy token must not fire the alert loop."""
    _write_history(history_dir / meta_agent.HISTORY_FILE_NAME, [_row("flush", "ok")])
    assert meta_agent.check_agent_health("flush", {}, False)["status"] == "healthy"


def test_ok_still_ages_into_stale(history_dir: Path):
    """'ok' must route through the healthy branch, not around it — a stale 'ok'
    is stale, which is only reachable if the token was recognised."""
    _write_history(
        history_dir / meta_agent.HISTORY_FILE_NAME,
        [_row("flush", "ok", hours_ago=meta_agent._STALE_AFTER_HOURS["flush"] + 5)],
    )
    assert meta_agent.check_agent_health("flush", {}, False)["status"] == "stale"


@pytest.mark.parametrize(
    "status,expected",
    [("error", "error"), ("success", "healthy"), ("empty-queue", "healthy"),
     ("recursion-guard", "healthy"), ("banana", "banana")],
)
def test_existing_status_vocabulary_unchanged(history_dir: Path, status: str, expected: str):
    """The d21 fix widens the healthy set by exactly one token."""
    _write_history(history_dir / meta_agent.HISTORY_FILE_NAME, [_row("flush", status)])
    assert meta_agent.check_agent_health("flush", {}, False)["status"] == expected


# ── eng-001.d40 — the alert needs a path to a human ─────────────────────────

def test_collect_fleet_alerts_names_the_unhealthy(history_dir: Path):
    _write_history(
        history_dir / meta_agent.HISTORY_FILE_NAME,
        [_row("flush", "ok"), _row("vault_synthesizer", "error"), _row("job_feed", "success")],
    )
    named = {a[0]: a[1] for a in meta_agent.collect_fleet_alerts({}, dry_run=False)}
    # Agents with no history row at all are legitimately unhealthy (no data is
    # not health), so assert only on the three this fixture actually wrote.
    assert named["vault_synthesizer"] == "error"
    assert "flush" not in named
    assert "job_feed" not in named


def test_alert_delivers_one_aggregated_push(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    sent: list[dict] = []
    monkeypatch.setattr(meta_agent, "_send_fleet_push", lambda **kw: sent.append(kw) or True)
    monkeypatch.setattr(meta_agent, "ALERT_DELIVERY_LOG", tmp_path / "delivery.jsonl")

    ok = meta_agent.deliver_fleet_alert(
        [("vault_synthesizer", "error", "status=error"), ("flush", "stale", "status=ok")],
        dry_run=False,
    )

    assert ok is True
    assert len(sent) == 1, "one baton, one page — never one push per agent"
    assert "vault_synthesizer" in sent[0]["message"] and "flush" in sent[0]["message"]


def test_healthy_fleet_sends_nothing(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    sent: list[dict] = []
    monkeypatch.setattr(meta_agent, "_send_fleet_push", lambda **kw: sent.append(kw) or True)
    monkeypatch.setattr(meta_agent, "ALERT_DELIVERY_LOG", tmp_path / "delivery.jsonl")

    assert meta_agent.deliver_fleet_alert([], dry_run=False) is True
    assert sent == []


def test_dry_run_never_pushes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    sent: list[dict] = []
    monkeypatch.setattr(meta_agent, "_send_fleet_push", lambda **kw: sent.append(kw) or True)
    monkeypatch.setattr(meta_agent, "ALERT_DELIVERY_LOG", tmp_path / "delivery.jsonl")

    meta_agent.deliver_fleet_alert([("flush", "error", "status=error")], dry_run=True)
    assert sent == []


def test_send_failure_never_raises_into_the_run(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """The system whose job is surfacing failure must not fail loudly at the
    point of surfacing it — but it must record that it failed."""
    def _boom(**_kw):
        raise RuntimeError("pushover down")

    monkeypatch.setattr(meta_agent, "_send_fleet_push", _boom)
    monkeypatch.setattr(meta_agent, "ALERT_DELIVERY_LOG", tmp_path / "delivery.jsonl")

    assert meta_agent.deliver_fleet_alert([("flush", "error", "x")], dry_run=False) is False
    assert '"delivered": false' in (tmp_path / "delivery.jsonl").read_text()


def test_every_run_writes_one_delivery_record(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """B3 needs seven consecutive nights of evidence that the path works. A
    healthy night sends nothing, so the record — not the push — is the trial."""
    log = tmp_path / "delivery.jsonl"
    monkeypatch.setattr(meta_agent, "_send_fleet_push", lambda **kw: True)
    monkeypatch.setattr(meta_agent, "ALERT_DELIVERY_LOG", log)

    meta_agent.deliver_fleet_alert([], dry_run=False)
    meta_agent.deliver_fleet_alert([("flush", "error", "x")], dry_run=False)

    lines = [l for l in log.read_text().splitlines() if l.strip()]
    assert len(lines) == 2
    assert '"alerts": 0' in lines[0] and '"alerts": 1' in lines[1]


# ── the daily-driver note assertion ─────────────────────────────────────────

def test_morning_success_without_a_note_is_not_a_success(tmp_path: Path):
    from agents import daily_driver

    assert daily_driver.assert_daily_note(
        "success", mode="morning", vault_root=tmp_path
    ) == ("error_no_note", "daily note absent after a reported success")


def test_morning_success_with_a_note_stays_a_success(tmp_path: Path, monkeypatch):
    from agents import daily_driver
    from lib import vault_io

    note = vault_io.daily_note_path(tmp_path)
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("# today\n")

    assert daily_driver.assert_daily_note(
        "success", mode="morning", vault_root=tmp_path
    ) == ("success", "")


def test_assertion_does_not_mask_an_existing_error(tmp_path: Path):
    """A run that already failed keeps its own status — the assertion adds a
    failure mode, it never renames one."""
    from agents import daily_driver

    assert daily_driver.assert_daily_note(
        "error_auth", mode="morning", vault_root=tmp_path
    ) == ("error_auth", "")


def test_assertion_only_applies_to_the_mode_that_writes_the_note(tmp_path: Path):
    from agents import daily_driver

    assert daily_driver.assert_daily_note(
        "success", mode="evening", vault_root=tmp_path
    ) == ("success", "")
