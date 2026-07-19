"""F8b Task 5 cross-process reconciliation liveness matrix."""

import json
from datetime import date, datetime, timezone

import pytest

from council import budget


TODAY = date(2026, 9, 18)


def _daily(root, on_date=TODAY):
    return root / f"council-spend-{on_date.isoformat()}.json"


def _reservation_row(**overrides):
    row = {
        "amount": 1.0,
        "profile": "test",
        "tag": "liveness",
        "tool": "council",
        "kind": "reservation",
        "reservation_id": "reservation-1",
        "run_id": "run-1",
        "status": "dispatched",
        "created_at": "2026-09-16T00:00:00+00:00",
        "owner_pid": 123,
        "owner_host": "local-host",
        "owner_started_at": "Mon Sep 14 12:00:00 2026",
        "policy_version": None,
        "policy_hash": None,
    }
    row.update(overrides)
    return row


def _write_ledger(root, row, on_date=TODAY):
    _daily(root, on_date).write_text(
        json.dumps(
            {
                "schema_version": 2,
                "date": on_date.isoformat(),
                "total": row["amount"],
                "runs": [row],
                "actuals": [],
            }
        )
    )


def _read_row(root, on_date=TODAY):
    return json.loads(_daily(root, on_date).read_text())["runs"][0]


CUTOFF = datetime(2026, 9, 18, 12, 0, tzinfo=timezone.utc)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("owner_pid", True),
        ("owner_pid", 0),
        ("owner_pid", -1),
        ("owner_pid", "123"),
        ("owner_host", ""),
        ("owner_host", 123),
        ("owner_started_at", ""),
        ("owner_started_at", 123),
    ],
)
def test_strict_parser_refuses_junk_owner_metadata(
    tmp_spend_dir, field, value
):
    _write_ledger(tmp_spend_dir, _reservation_row(**{field: value}))

    with pytest.raises(budget.LedgerCorrupt, match=field):
        budget.strict_ledger_state(TODAY)


def test_reconcile_esrch_owner_is_dead(tmp_spend_dir, monkeypatch):
    _write_ledger(tmp_spend_dir, _reservation_row())
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")

    def _dead(_pid, _signal):
        raise ProcessLookupError

    monkeypatch.setattr(budget.os, "kill", _dead)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == ["reservation-1"]
    assert _read_row(tmp_spend_dir)["status"] == "unknown"


def test_reconcile_eperm_owner_is_assumed_alive_and_alerted(
    tmp_spend_dir, monkeypatch, capsys
):
    _write_ledger(tmp_spend_dir, _reservation_row())
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")

    def _permission_denied(_pid, _signal):
        raise PermissionError

    monkeypatch.setattr(budget.os, "kill", _permission_denied)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == []
    assert _read_row(tmp_spend_dir)["status"] == "dispatched"
    alert = capsys.readouterr().err
    assert "permission" in alert
    assert "skipped" in alert


def test_reconcile_foreign_host_is_skipped_and_alerted(
    tmp_spend_dir, monkeypatch, capsys
):
    _write_ledger(
        tmp_spend_dir,
        _reservation_row(owner_host="remote-host"),
    )
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")
    monkeypatch.setattr(
        budget.os,
        "kill",
        lambda *_args: pytest.fail("foreign-host rows must not probe a remote pid"),
    )

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == []
    assert _read_row(tmp_spend_dir)["status"] == "dispatched"
    assert capsys.readouterr().err.strip() == (
        "[reconcile] foreign-host reservation reservation-1 from remote-host "
        "— cannot verify liveness; skipped"
    )


def test_reconcile_live_owner_over_24h_alerts_without_mutation(
    tmp_spend_dir, monkeypatch, capsys
):
    started_at = "Mon Sep 14 12:00:00 2026"
    _write_ledger(
        tmp_spend_dir,
        _reservation_row(owner_pid=456, owner_started_at=started_at),
    )
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")
    monkeypatch.setattr(budget.os, "kill", lambda _pid, _signal: None)
    monkeypatch.setattr(budget, "_process_start_time", lambda _pid: started_at)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == []
    assert _read_row(tmp_spend_dir)["status"] == "dispatched"
    assert capsys.readouterr().err.strip() == (
        "[reconcile] reservation reservation-1 held by live pid 456 for >24h "
        "— investigate"
    )


def test_reconcile_pid_reuse_is_reconciled(tmp_spend_dir, monkeypatch):
    _write_ledger(tmp_spend_dir, _reservation_row(owner_pid=456))
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")
    monkeypatch.setattr(budget.os, "kill", lambda _pid, _signal: None)
    monkeypatch.setattr(
        budget,
        "_process_start_time",
        lambda _pid: "Tue Sep 15 12:00:00 2026",
    )

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == ["reservation-1"]
    assert _read_row(tmp_spend_dir)["status"] == "unknown"


def test_reconcile_unverifiable_live_owner_degrades_to_ttl_and_alerts(
    tmp_spend_dir, monkeypatch, capsys
):
    _write_ledger(
        tmp_spend_dir,
        _reservation_row(
            owner_pid=456,
            created_at="2026-09-18T11:59:59+00:00",
        ),
    )
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")
    monkeypatch.setattr(budget.os, "kill", lambda _pid, _signal: None)
    monkeypatch.setattr(budget, "_process_start_time", lambda _pid: None)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == []
    assert _read_row(tmp_spend_dir)["status"] == "dispatched"

    data = json.loads(_daily(tmp_spend_dir).read_text())
    data["runs"][0]["created_at"] = "2026-09-16T00:00:00+00:00"
    _daily(tmp_spend_dir).write_text(json.dumps(data))

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == ["reservation-1"]
    assert _read_row(tmp_spend_dir)["status"] == "unknown"
    assert capsys.readouterr().err.splitlines() == [
        "[reconcile] cannot verify owner start time for pid 456 — degraded to TTL",
        "[reconcile] cannot verify owner start time for pid 456 — degraded to TTL",
    ]


def test_reconcile_ps_timeout_degrades_to_ttl_never_pid_reuse(
    tmp_spend_dir, monkeypatch, capsys
):
    _write_ledger(
        tmp_spend_dir,
        _reservation_row(
            owner_pid=456,
            created_at="2026-09-18T11:59:59+00:00",
        ),
    )
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")
    monkeypatch.setattr(budget.os, "kill", lambda _pid, _signal: None)

    def _timeout(command, **kwargs):
        raise budget.subprocess.TimeoutExpired(command, kwargs["timeout"])

    monkeypatch.setattr(budget.subprocess, "run", _timeout)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == []
    assert _read_row(tmp_spend_dir)["status"] == "dispatched"
    assert capsys.readouterr().err.strip() == (
        "[reconcile] cannot verify owner start time for pid 456 — degraded to TTL"
    )


def test_reconcile_legacy_rows_require_24h_ttl_when_cutoff_is_supplied(
    tmp_spend_dir,
):
    old_day = date(2026, 9, 16)
    fresh_day = date(2026, 9, 17)
    old = _reservation_row(
        reservation_id="old-legacy",
        created_at="2026-09-16T00:00:00+00:00",
    )
    fresh = _reservation_row(
        reservation_id="fresh-legacy",
        created_at="2026-09-17T18:00:00+00:00",
    )
    for row in (old, fresh):
        row.pop("owner_pid")
        row.pop("owner_host")
        row.pop("owner_started_at")
    _write_ledger(tmp_spend_dir, old, old_day)
    _write_ledger(tmp_spend_dir, fresh, fresh_day)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == ["old-legacy"]
    assert _read_row(tmp_spend_dir, old_day)["status"] == "unknown"
    assert _read_row(tmp_spend_dir, fresh_day)["status"] == "dispatched"


def test_reconcile_fresh_naive_legacy_created_at_is_interpreted_as_utc(
    tmp_spend_dir,
):
    row = _reservation_row(created_at="2026-09-18T11:59:59")
    row.pop("owner_pid")
    row.pop("owner_host")
    row.pop("owner_started_at")
    _write_ledger(tmp_spend_dir, row)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == []
    assert _read_row(tmp_spend_dir)["status"] == "dispatched"


def test_reconcile_old_naive_legacy_created_at_is_interpreted_as_utc(
    tmp_spend_dir,
):
    row = _reservation_row(created_at="2026-09-16T00:00:00")
    row.pop("owner_pid")
    row.pop("owner_host")
    row.pop("owner_started_at")
    _write_ledger(tmp_spend_dir, row)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == ["reservation-1"]
    assert _read_row(tmp_spend_dir)["status"] == "unknown"


def test_reconcile_legacy_row_without_cutoff_preserves_unconditional_behavior(
    tmp_spend_dir,
):
    row = _reservation_row(created_at="2026-09-18T11:59:59+00:00")
    row.pop("owner_pid")
    row.pop("owner_host")
    row.pop("owner_started_at")
    _write_ledger(tmp_spend_dir, row)

    assert budget.reconcile_stale(TODAY) == ["reservation-1"]
    assert _read_row(tmp_spend_dir)["status"] == "unknown"


def test_reconcile_legacy_unparseable_created_at_is_treated_as_old(
    tmp_spend_dir,
):
    row = _reservation_row(created_at="not-a-timestamp")
    row.pop("owner_pid")
    row.pop("owner_host")
    row.pop("owner_started_at")
    _write_ledger(tmp_spend_dir, row)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == ["reservation-1"]
    assert _read_row(tmp_spend_dir)["status"] == "unknown"


def test_reconcile_alive_owner_without_start_identity_uses_legacy_ttl(
    tmp_spend_dir, monkeypatch
):
    _write_ledger(tmp_spend_dir, _reservation_row(owner_started_at=None))
    monkeypatch.setattr(budget.socket, "gethostname", lambda: "local-host")
    monkeypatch.setattr(budget.os, "kill", lambda _pid, _signal: None)

    assert budget.reconcile_stale(TODAY, older_than=CUTOFF) == ["reservation-1"]
    assert _read_row(tmp_spend_dir)["status"] == "unknown"
