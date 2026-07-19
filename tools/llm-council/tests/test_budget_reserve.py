"""F8a.3 — the-oracle's locked reserve on the shared ledger.

Canonical month-lock identity, a locked ``record_spend`` for every writer, a strict
fail-closed enforcement parser, ``check_and_reserve`` + crash-safe lifecycle, and the
versioned reserved(debit)/actual(non-debit) schema. These primitives are the-oracle's
adoption surface; siblings keep their unlocked preflight/settlement lifecycle until F8b.
"""

import json
import os
import threading
from datetime import date
from pathlib import Path

import pytest

from council import budget
from council.budget import (
    BudgetExceeded,
    LedgerCorrupt,
    ReservationError,
    check_and_reserve,
    mark_dispatched,
    month_lock_path,
    reconcile_stale,
    record_spend,
    settle,
    strict_ledger_state,
)


def _read(path: Path) -> dict:
    return json.loads(path.read_text())


def _daily(spend_dir: Path, on_date: date) -> Path:
    return spend_dir / f"council-spend-{on_date.isoformat()}.json"


# Default cap kwargs that never fire; individual tests override the one under test.
_ROOMY = dict(
    per_query_cap=100.0,
    tool_daily_cap=1000.0,
    tool_monthly_cap=1000.0,
    aggregate_daily_cap=1000.0,
    aggregate_monthly_cap=1000.0,
)


def _reserve(on_date, **over):
    kwargs = dict(
        reserved_cost=1.0,
        tool="oracle-forecast",
        tag="pdufa-x",
        profile="premium",
        run_id="run-1",
        on_date=on_date,
        **_ROOMY,
    )
    kwargs.update(over)
    return check_and_reserve(**kwargs)


# --- Canonical lock identity -------------------------------------------------

def test_month_lock_path_is_month_scoped(tmp_spend_dir):
    p1 = month_lock_path(date(2026, 7, 1))
    p31 = month_lock_path(date(2026, 7, 31))
    p_aug = month_lock_path(date(2026, 8, 1))
    assert p1 == p31  # every day in the month shares one lock
    assert p1 != p_aug
    assert p1.name == ".council-spend-2026-07.lock"


def test_month_lock_path_collapses_symlinked_spend_dir(tmp_path, monkeypatch):
    real = tmp_path / "real" / "health"
    real.mkdir(parents=True)
    link = tmp_path / "linked"
    link.symlink_to(tmp_path / "real")
    # Same directory, two spellings (symlink vs realpath) → one canonical lock file.
    monkeypatch.setenv("COUNCIL_SPEND_DIR", str(link / "health"))
    via_link = month_lock_path(date(2026, 7, 14))
    monkeypatch.setenv("COUNCIL_SPEND_DIR", str(real))
    via_real = month_lock_path(date(2026, 7, 14))
    assert via_link == via_real
    assert via_link == via_link.resolve()


# --- Locked record_spend for every writer (finding 1) ------------------------

def test_record_spend_still_appends_and_totals(tmp_spend_dir):
    today = date(2026, 7, 14)
    record_spend(amount=0.50, profile="variance", tag="t1", on_date=today)
    record_spend(amount=0.30, profile="premium", tag="t2", on_date=today, tool="discovery")
    data = _read(_daily(tmp_spend_dir, today))
    assert data["total"] == pytest.approx(0.80, abs=1e-6)
    assert [r["amount"] for r in data["runs"]] == [0.50, 0.30]


def test_oracle_reservation_survives_concurrent_legacy_settlement(tmp_spend_dir):
    """The load-bearing regression: a sibling's stale read-modify-write must not
    clobber a durably-appended oracle reservation. With record_spend locked, the
    sibling blocks on the month lock instead of overwriting."""
    today = date(2026, 7, 14)
    sibling_reading = threading.Event()
    reservation_committed = threading.Event()

    real_atomic = budget._atomic_write_json

    def paused_atomic(path, data):
        # Only the legacy sibling writer carries a discovery run; pause it mid-write
        # (holding the month lock) until the oracle reservation has committed.
        if any(r.get("tool") == "discovery" for r in data.get("runs", [])):
            sibling_reading.set()
            reservation_committed.wait(timeout=5)
        return real_atomic(path, data)

    budget._atomic_write_json = paused_atomic
    try:
        def sibling():
            record_spend(amount=0.10, profile="disc", tag="d", on_date=today, tool="discovery")

        t = threading.Thread(target=sibling)
        t.start()
        assert sibling_reading.wait(timeout=5), "sibling never entered its locked write"
        # The oracle now reserves. If record_spend were unlocked the sibling's stale
        # snapshot would erase this row; the lock forces it to serialize instead.
        reserved = None
        reserve_error = []

        def oracle():
            nonlocal reserved
            try:
                reserved = _reserve(today, reserved_cost=2.0, run_id="run-oracle")
            except BaseException as exc:  # pragma: no cover - surfaced via assert
                reserve_error.append(exc)

        ot = threading.Thread(target=oracle)
        ot.start()
        # The oracle reserve must block on the sibling's held lock, so it cannot finish yet.
        ot.join(timeout=0.5)
        assert ot.is_alive(), "oracle reserve did not block on the month lock"
        reservation_committed.set()
        ot.join(timeout=5)
        t.join(timeout=5)
        assert not reserve_error, reserve_error
    finally:
        budget._atomic_write_json = real_atomic

    runs = _read(_daily(tmp_spend_dir, today))["runs"]
    tools = [r.get("tool") for r in runs]
    assert "discovery" in tools, "sibling settlement lost"
    assert "oracle-forecast" in tools, "oracle reservation clobbered by stale sibling write"


# --- Strict fail-closed enforcement parser (finding 2) -----------------------

def test_strict_state_sums_day_and_month_by_tool(tmp_spend_dir):
    record_spend(amount=1.0, profile="p", tag="t", on_date=date(2026, 7, 10), tool="oracle-forecast")
    record_spend(amount=2.0, profile="p", tag="t", on_date=date(2026, 7, 14), tool="oracle-forecast")
    record_spend(amount=0.5, profile="p", tag="t", on_date=date(2026, 7, 14), tool="discovery")
    state = strict_ledger_state(date(2026, 7, 14))
    assert state["month"]["by_tool"]["oracle-forecast"] == pytest.approx(3.0)
    assert state["day"]["by_tool"]["oracle-forecast"] == pytest.approx(2.0)
    assert state["day"]["aggregate"] == pytest.approx(2.5)
    assert state["month"]["aggregate"] == pytest.approx(3.5)


def test_strict_state_refuses_malformed_json(tmp_spend_dir):
    _daily(tmp_spend_dir, date(2026, 7, 14)).write_text("{not json")
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


def test_strict_state_refuses_negative_money(tmp_spend_dir):
    f = _daily(tmp_spend_dir, date(2026, 7, 14))
    f.write_text(json.dumps({"date": "2026-07-14", "total": -1.0,
                             "runs": [{"amount": -1.0, "tool": "discovery"}]}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


def test_strict_state_refuses_non_finite_money(tmp_spend_dir):
    f = _daily(tmp_spend_dir, date(2026, 7, 14))
    f.write_text('{"date": "2026-07-14", "total": 1.0, "runs": [{"amount": 1e999, "tool": "x"}]}')
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


def test_strict_state_refuses_inconsistent_total(tmp_spend_dir):
    f = _daily(tmp_spend_dir, date(2026, 7, 14))
    f.write_text(json.dumps({"date": "2026-07-14", "total": 9.0,
                             "runs": [{"amount": 1.0, "tool": "discovery"}]}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


def test_strict_state_tolerates_micro_rounding_in_total(tmp_spend_dir):
    # A one-micro float artifact in a legacy total must NOT fail closed.
    f = _daily(tmp_spend_dir, date(2026, 7, 14))
    f.write_text(json.dumps({"date": "2026-07-14", "total": 2.000001,
                             "runs": [{"amount": 1.0, "tool": "a"}, {"amount": 1.0, "tool": "b"}]}))
    state = strict_ledger_state(date(2026, 7, 14))
    assert state["day"]["aggregate"] == pytest.approx(2.0)


def test_strict_state_refuses_bad_schema_version(tmp_spend_dir):
    f = _daily(tmp_spend_dir, date(2026, 7, 14))
    f.write_text(json.dumps({"schema_version": 99, "date": "2026-07-14", "total": 0.0, "runs": []}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


def test_strict_state_refuses_duplicate_reservation_id(tmp_spend_dir):
    row = {"amount": 1.0, "tool": "oracle-forecast", "kind": "reservation",
           "reservation_id": "dup", "run_id": "r", "status": "reserved"}
    f = _daily(tmp_spend_dir, date(2026, 7, 14))
    f.write_text(json.dumps({"schema_version": 2, "date": "2026-07-14", "total": 2.0,
                             "runs": [row, dict(row)], "actuals": []}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


def test_strict_state_refuses_illegal_status(tmp_spend_dir):
    row = {"amount": 1.0, "tool": "oracle-forecast", "kind": "reservation",
           "reservation_id": "r1", "run_id": "r", "status": "bogus"}
    f = _daily(tmp_spend_dir, date(2026, 7, 14))
    f.write_text(json.dumps({"schema_version": 2, "date": "2026-07-14", "total": 1.0,
                             "runs": [row], "actuals": []}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


# --- check_and_reserve: per-tool + aggregate + durable reservation -----------

def test_reserve_writes_durable_reserved_row(tmp_spend_dir):
    today = date(2026, 7, 14)
    r = _reserve(today, reserved_cost=1.5)
    data = _read(_daily(tmp_spend_dir, today))
    assert data["schema_version"] == 2
    assert data["total"] == pytest.approx(1.5, abs=1e-6)
    row = next(x for x in data["runs"] if x.get("kind") == "reservation")
    assert row["amount"] == pytest.approx(1.5)
    assert row["tool"] == "oracle-forecast"
    assert row["status"] == "reserved"
    assert row["run_id"] == "run-1"
    assert row["reservation_id"] == r.reservation_id
    assert row["policy_version"] is None and row["policy_hash"] is None
    assert data["actuals"] == []


def test_reserve_refuses_over_per_query_cap(tmp_spend_dir):
    with pytest.raises(BudgetExceeded, match="per-query"):
        _reserve(date(2026, 7, 14), reserved_cost=5.0, per_query_cap=1.0)


def test_force_skips_only_per_query_cap(tmp_spend_dir):
    reservation = _reserve(
        date(2026, 7, 14), reserved_cost=5.0, per_query_cap=1.0, force=True
    )

    assert reservation.amount == 5.0


@pytest.mark.parametrize(
    ("prior", "cap_name", "cap_value", "message"),
    [
        (6.5, "tool_daily_cap", 7.0, "daily"),
        (39.5, "tool_monthly_cap", 40.0, "monthly"),
        (6.5, "aggregate_daily_cap", 7.0, "aggregate daily"),
        (39.5, "aggregate_monthly_cap", 40.0, "aggregate monthly"),
    ],
)
def test_force_never_skips_daily_monthly_or_aggregate_caps(
    tmp_spend_dir, prior, cap_name, cap_value, message
):
    today = date(2026, 7, 14)
    prior_date = today if "daily" in cap_name else date(2026, 7, 1)
    record_spend(
        amount=prior,
        profile="p",
        tag="prior",
        on_date=prior_date,
        tool="oracle-forecast",
    )

    with pytest.raises(BudgetExceeded, match=message):
        _reserve(
            today,
            reserved_cost=1.0,
            per_query_cap=0.5,
            force=True,
            **{cap_name: cap_value},
        )


def test_reserve_refuses_over_tool_monthly_cap(tmp_spend_dir):
    record_spend(amount=39.5, profile="p", tag="prior", on_date=date(2026, 7, 1),
                 tool="oracle-forecast")
    with pytest.raises(BudgetExceeded, match="monthly"):
        _reserve(date(2026, 7, 14), reserved_cost=1.0, tool_monthly_cap=40.0)


def test_reserve_refuses_over_tool_daily_cap(tmp_spend_dir):
    record_spend(amount=6.5, profile="p", tag="prior", on_date=date(2026, 7, 14),
                 tool="oracle-forecast")
    with pytest.raises(BudgetExceeded, match="daily"):
        _reserve(date(2026, 7, 14), reserved_cost=1.0, tool_daily_cap=7.0)


def test_reserve_refuses_when_aggregate_would_breach(tmp_spend_dir):
    # Another tool has consumed the shared ceiling; the-oracle must refuse even though
    # its own per-tool room is ample (the aggregate is CHECKED under the lock).
    record_spend(amount=6.9, profile="p", tag="sib", on_date=date(2026, 7, 14),
                 tool="discovery")
    with pytest.raises(BudgetExceeded, match="aggregate"):
        _reserve(date(2026, 7, 14), reserved_cost=0.5, aggregate_daily_cap=7.0)


def test_reserve_fails_closed_on_corrupt_ledger(tmp_spend_dir):
    _daily(tmp_spend_dir, date(2026, 7, 14)).write_text("{corrupt")
    with pytest.raises(LedgerCorrupt):
        _reserve(date(2026, 7, 14))


def test_reserve_fsyncs_file_and_parent_dir(tmp_spend_dir, monkeypatch):
    calls = []
    real = os.fsync
    monkeypatch.setattr(os, "fsync", lambda fd: (calls.append(fd), real(fd))[1])
    _reserve(date(2026, 7, 14))
    assert len(calls) >= 2  # data file + parent directory


# --- Crash-safe lifecycle ----------------------------------------------------

def test_mark_dispatched_transitions_and_keeps_debit(tmp_spend_dir):
    today = date(2026, 7, 14)
    r = _reserve(today, reserved_cost=1.5)
    mark_dispatched(r)
    data = _read(_daily(tmp_spend_dir, today))
    row = next(x for x in data["runs"] if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "dispatched"
    assert data["total"] == pytest.approx(1.5)  # debit unchanged across the transition


def test_settle_records_non_debit_actual(tmp_spend_dir):
    today = date(2026, 7, 14)
    r = _reserve(today, reserved_cost=1.5)
    mark_dispatched(r)
    settle(r, attempt_id="a1", generation_id="g1", usage_cost=0.42, status="settled")
    data = _read(_daily(tmp_spend_dir, today))
    row = next(x for x in data["runs"] if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "settled"
    assert data["total"] == pytest.approx(1.5)  # actual NEVER debits total
    act = next(a for a in data["actuals"] if a["reservation_id"] == r.reservation_id)
    assert act["usage_cost"] == pytest.approx(0.42)
    assert act["attempt_id"] == "a1" and act["generation_id"] == "g1"


def test_settle_unknown_allows_null_actual_and_retains_debit(tmp_spend_dir):
    today = date(2026, 7, 14)
    r = _reserve(today, reserved_cost=1.5)
    mark_dispatched(r)
    settle(r, attempt_id="a1", generation_id=None, usage_cost=None, status="unknown")
    data = _read(_daily(tmp_spend_dir, today))
    row = next(x for x in data["runs"] if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "unknown"
    assert data["total"] == pytest.approx(1.5)  # unknown retains the reservation debit
    act = next(a for a in data["actuals"] if a["reservation_id"] == r.reservation_id)
    assert act["usage_cost"] is None


def test_settle_rejects_illegal_transition(tmp_spend_dir):
    today = date(2026, 7, 14)
    r = _reserve(today)
    # Cannot settle a reservation that was never dispatched.
    with pytest.raises(ReservationError):
        settle(r, attempt_id="a1", generation_id="g1", usage_cost=0.1, status="settled")


def test_reconcile_stale_retains_debit_as_unknown(tmp_spend_dir, monkeypatch):
    # Explicit legacy/degraded-owner path: Task 5 gives positively identified live owners
    # precedence over reconciliation, while an unavailable OS start query preserves the
    # older_than=None behavior this regression has always specified.
    monkeypatch.setattr(budget, "_process_start_time", lambda _pid: None)
    today = date(2026, 7, 14)
    r1 = _reserve(today, reserved_cost=1.0, run_id="r1")
    r2 = _reserve(today, reserved_cost=2.0, run_id="r2")
    mark_dispatched(r2)  # crash after dispatch, before settle
    reconciled = reconcile_stale(today)
    assert set(reconciled) == {r1.reservation_id, r2.reservation_id}
    data = _read(_daily(tmp_spend_dir, today))
    statuses = {x["reservation_id"]: x["status"] for x in data["runs"] if x.get("kind") == "reservation"}
    assert statuses[r1.reservation_id] == "unknown"
    assert statuses[r2.reservation_id] == "unknown"
    assert data["total"] == pytest.approx(3.0)  # both debits retained


def test_reconcile_leaves_settled_rows_untouched(tmp_spend_dir):
    today = date(2026, 7, 14)
    r = _reserve(today, reserved_cost=1.0)
    mark_dispatched(r)
    settle(r, attempt_id="a1", generation_id="g1", usage_cost=0.2, status="settled")
    assert reconcile_stale(today) == []
    row = next(x for x in _read(_daily(tmp_spend_dir, today))["runs"]
               if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "settled"


# --- Mixed old/new reader compatibility --------------------------------------

def test_legacy_sum_runs_ignores_reservation_extra_fields(tmp_spend_dir):
    today = date(2026, 7, 14)
    _reserve(today, reserved_cost=1.5, tool="oracle-forecast")
    record_spend(amount=0.3, profile="d", tag="d", on_date=today, tool="discovery")
    # Legacy tolerant readers still tally per tool from runs[].amount.
    assert budget.tool_total_for_day(today, "oracle-forecast") == pytest.approx(1.5)
    assert budget.tool_total_for_day(today, "discovery") == pytest.approx(0.3)
    assert budget._read_total_for_day(today) == pytest.approx(1.8)


def test_shared_run_id_two_reservations(tmp_spend_dir):
    today = date(2026, 7, 14)
    _reserve(today, reserved_cost=1.0, run_id="shared", tag="council")
    _reserve(today, reserved_cost=0.4, run_id="shared", tag="fallback")
    rows = [x for x in _read(_daily(tmp_spend_dir, today))["runs"] if x.get("kind") == "reservation"]
    assert {x["run_id"] for x in rows} == {"shared"}
    assert len(rows) == 2  # council + fallback graphs retained, no refund
