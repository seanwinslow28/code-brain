"""F8a.3 hardening — fixes for the independent budget.py review (11 findings).

Each test pins one adjudicated finding so the fail-closed / HARD-cap invariants cannot
regress. Numbered to the review.
"""

import json
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from council import budget
from council.budget import (
    BudgetExceeded,
    LedgerCorrupt,
    ReservationError,
    check_and_reserve,
    mark_dispatched,
    reconcile_stale,
    record_spend,
    settle,
    strict_ledger_state,
)


def _read(path: Path) -> dict:
    return json.loads(path.read_text())


def _daily(spend_dir: Path, on_date: date) -> Path:
    return spend_dir / f"council-spend-{on_date.isoformat()}.json"


_ROOMY = dict(
    per_query_cap=100.0,
    tool_daily_cap=1000.0,
    tool_monthly_cap=1000.0,
    aggregate_daily_cap=1000.0,
    aggregate_monthly_cap=1000.0,
)


def _reserve(on_date, **over):
    kwargs = dict(
        reserved_cost=1.0, tool="oracle-forecast", tag="t", profile="premium",
        run_id="run-1", on_date=on_date, **_ROOMY,
    )
    kwargs.update(over)
    return check_and_reserve(**kwargs)


# Finding 1 — a datetime on_date must not open a timestamp-named daily file that
# bypasses the calendar day's accumulated total.
def test_datetime_on_date_is_normalized_to_calendar_day(tmp_spend_dir):
    record_spend(amount=6.9, profile="p", tag="prior", on_date=date(2026, 7, 14),
                 tool="oracle-forecast")
    with pytest.raises(BudgetExceeded, match="daily"):
        _reserve(datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc),
                 reserved_cost=0.5, tool_daily_cap=7.0)
    # The reservation, when it succeeds, writes to the calendar-day file, not a timestamp one.
    _reserve(datetime(2026, 7, 14, 12, 0, tzinfo=timezone.utc), reserved_cost=0.05,
             tool_daily_cap=7.0)
    assert _daily(tmp_spend_dir, date(2026, 7, 14)).exists()
    assert not list(tmp_spend_dir.glob("council-spend-2026-07-14T*.json"))


# F8b-4 — force is additive and may skip only the per-query comparison.
def test_check_and_reserve_force_skips_per_query_and_keeps_full_debit(tmp_spend_dir):
    reservation = check_and_reserve(
        reserved_cost=2.0,
        tool="oracle-forecast",
        tag="t",
        profile="p",
        run_id="r",
        on_date=date(2026, 7, 14),
        per_query_cap=1.0,
        tool_daily_cap=1000.0,
        tool_monthly_cap=1000.0,
        aggregate_daily_cap=1000.0,
        aggregate_monthly_cap=1000.0,
        force=True,
    )

    assert reservation.amount == 2.0
    with pytest.raises(BudgetExceeded, match="per-query"):
        _reserve(date(2026, 7, 14), reserved_cost=2.0, per_query_cap=1.0)


# Finding 3 — the spend root is resolved ONCE per transaction (lock + files agree).
def test_reserve_pins_spend_root_once(tmp_spend_dir, monkeypatch):
    calls = []
    real = budget._resolve_root

    def counting_root():
        calls.append(1)
        return real()

    monkeypatch.setattr(budget, "_resolve_root", counting_root)
    _reserve(date(2026, 7, 14))
    assert len(calls) == 1  # a mid-transaction env/symlink change cannot split lock vs file


# Finding 4 — a truncated ledger (missing runs) must fail closed, not read as zero.
def test_strict_refuses_ledger_missing_runs(tmp_spend_dir):
    _daily(tmp_spend_dir, date(2026, 7, 14)).write_text(
        json.dumps({"schema_version": 2, "date": "2026-07-14"}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


def test_strict_refuses_ledger_missing_total(tmp_spend_dir):
    _daily(tmp_spend_dir, date(2026, 7, 14)).write_text(
        json.dumps({"schema_version": 2, "date": "2026-07-14",
                    "runs": [{"amount": 1.0, "tool": "x"}]}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


# Finding 5 — a reservation-kind row without an explicit tool must fail closed
# (never silently charged to legacy "council" and omitted from oracle-forecast).
def test_strict_refuses_reservation_row_without_tool(tmp_spend_dir):
    row = {"amount": 39.0, "kind": "reservation", "reservation_id": "r1",
           "run_id": "r", "status": "reserved"}  # no "tool"
    _daily(tmp_spend_dir, date(2026, 7, 14)).write_text(
        json.dumps({"schema_version": 2, "date": "2026-07-14", "total": 39.0,
                    "runs": [row], "actuals": []}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


# Finding 6 — duplicate JSON object keys must be rejected (last-value-wins hides spend).
def test_strict_refuses_duplicate_json_keys(tmp_spend_dir):
    raw = ('{"schema_version": 2, "date": "2026-07-14",'
           ' "runs": [{"amount": 39.0, "tool": "discovery"}], "total": 39.0,'
           ' "runs": [], "total": 0.0}')
    _daily(tmp_spend_dir, date(2026, 7, 14)).write_text(raw)
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))


# Finding 7 — official writers cannot commit forbidden duplicate ids.
def test_duplicate_reservation_id_is_refused(tmp_spend_dir):
    today = date(2026, 7, 14)
    _reserve(today, reservation_id="same", run_id="r1")
    with pytest.raises(ReservationError):
        _reserve(today, reservation_id="same", run_id="r2")


def test_duplicate_attempt_id_is_refused(tmp_spend_dir):
    today = date(2026, 7, 14)
    r1 = _reserve(today, run_id="r1", reservation_id="res1")
    r2 = _reserve(today, run_id="r1", reservation_id="res2")
    mark_dispatched(r1)
    mark_dispatched(r2)
    settle(r1, attempt_id="a1", generation_id="g1", usage_cost=0.1, status="settled")
    with pytest.raises(ReservationError):
        settle(r2, attempt_id="a1", generation_id="g2", usage_cost=0.2, status="settled")


# Finding 8 — reconcile must not clobber a row created after a cutoff (a live dispatch).
def test_reconcile_respects_older_than_cutoff(tmp_spend_dir):
    today = date(2026, 7, 14)
    r = _reserve(today)
    mark_dispatched(r)
    # A cutoff in the past excludes the just-created live row.
    past = datetime(2000, 1, 1, tzinfo=timezone.utc)
    assert reconcile_stale(today, older_than=past) == []
    row = next(x for x in _read(_daily(tmp_spend_dir, today))["runs"]
               if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "dispatched"  # untouched — a live dispatch is not reconciled


# Finding 9 — legacy iterative-rounding totals must not trip the strict parser.
def test_legacy_rounding_drift_does_not_fail_closed(tmp_spend_dir):
    today = date(2026, 7, 14)
    for i in range(5):
        record_spend(amount=0.1234564, profile="p", tag=f"t{i}", on_date=today,
                     tool="discovery")
    # Iterative round(...,6) can drift several micros from the Decimal sum; strict must tolerate.
    state = strict_ledger_state(today)
    assert float(state["day"]["by_tool"]["discovery"]) == pytest.approx(0.617282, abs=1e-6)


# Finding 10 — a reserved_cost microscopically over the cap (float noise) is rejected,
# never admitted by a binary-float comparison.
def test_reserved_cost_epsilon_over_cap_is_rejected(tmp_spend_dir):
    with pytest.raises(BudgetExceeded, match="per-query"):
        _reserve(date(2026, 7, 14), reserved_cost=1.0 + 1e-9, per_query_cap=1.0)


def test_reserved_cost_exactly_at_cap_passes(tmp_spend_dir):
    _reserve(date(2026, 7, 14), reserved_cost=1.0, per_query_cap=1.0)  # equality allowed


# Finding 11 — schema_version: true must not be accepted as version 1.
def test_strict_refuses_bool_schema_version(tmp_spend_dir):
    _daily(tmp_spend_dir, date(2026, 7, 14)).write_text(
        json.dumps({"schema_version": True, "date": "2026-07-14", "total": 0.0, "runs": []}))
    with pytest.raises(LedgerCorrupt):
        strict_ledger_state(date(2026, 7, 14))
