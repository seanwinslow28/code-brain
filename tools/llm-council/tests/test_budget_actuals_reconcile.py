"""F8a.4 — per-attempt actuals + idempotent generation-id reconciliation.

The council/retrieval graphs run up to 13/N attempts under ONE reservation. To keep
per-generation granularity (so a failed-but-billed attempt is never laundered into zero
cost), the-oracle records each attempt's ``usage.cost``+``generation_id`` as its own
non-debit ``actuals`` row via ``record_actual`` (no state transition), then performs the
single terminal transition via ``close``. ``settle`` (the atomic single-attempt
record+transition) is left intact for single-call seams.

``reconcile_generations`` is a pure, idempotent reconciliation of the ledger's recorded
actuals against authoritative provider generation records: it fills a null ledger cost
from provider truth, surfaces a provider generation absent from the ledger (failed-but-
billed), and leaves an unresolved attempt ``unknown`` (never zero).
"""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from council.budget import (
    LedgerCorrupt,
    ReservationError,
    check_and_reserve,
    close,
    mark_dispatched,
    reconcile_generations,
    record_actual,
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
        reserved_cost=12.0,
        tool="oracle-forecast",
        tag="pdufa-x",
        profile="premium",
        run_id="run-1",
        on_date=on_date,
        **_ROOMY,
    )
    kwargs.update(over)
    return check_and_reserve(**kwargs)


def _dispatched(on_date, **over):
    r = _reserve(on_date, **over)
    mark_dispatched(r)
    return r


TODAY = date(2026, 7, 14)


# --- record_actual: per-attempt non-debit rows, no transition ----------------

def test_record_actual_appends_non_debit_row_without_transition(tmp_spend_dir):
    r = _dispatched(TODAY, reserved_cost=12.0)
    record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.42, status="settled")
    data = _read(_daily(tmp_spend_dir, TODAY))
    row = next(x for x in data["runs"] if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "dispatched"  # NO terminal transition
    assert data["total"] == pytest.approx(12.0)  # actual NEVER debits total
    act = next(a for a in data["actuals"] if a["attempt_id"] == "a1")
    assert act["usage_cost"] == pytest.approx(0.42)
    assert act["generation_id"] == "g1"
    assert act["run_id"] == r.run_id


def test_record_actual_records_multiple_attempts_under_one_reservation(tmp_spend_dir):
    r = _dispatched(TODAY, reserved_cost=12.0)
    record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.10, status="settled")
    record_actual(r, attempt_id="a2", generation_id="g2", usage_cost=0.20, status="settled")
    record_actual(r, attempt_id="a3", generation_id=None, usage_cost=None, status="unknown")
    data = _read(_daily(tmp_spend_dir, TODAY))
    ours = [a for a in data["actuals"] if a["reservation_id"] == r.reservation_id]
    assert {a["attempt_id"] for a in ours} == {"a1", "a2", "a3"}
    # reserved (12) >= sum of the known per-attempt actuals (0.30) — the cross-check.
    known = sum(a["usage_cost"] for a in ours if a["usage_cost"] is not None)
    assert known == pytest.approx(0.30)
    assert data["total"] == pytest.approx(12.0)


def test_record_actual_rejects_duplicate_attempt_id(tmp_spend_dir):
    r = _dispatched(TODAY)
    record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.1, status="settled")
    with pytest.raises(ReservationError):
        record_actual(r, attempt_id="a1", generation_id="g9", usage_cost=0.2, status="settled")


def test_record_actual_requires_dispatched_reservation(tmp_spend_dir):
    r = _reserve(TODAY)  # reserved, not yet dispatched
    with pytest.raises(ReservationError):
        record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.1, status="settled")


def test_record_actual_refused_after_terminal(tmp_spend_dir):
    r = _dispatched(TODAY)
    record_actual(r, attempt_id="a0", generation_id="g0", usage_cost=0.1, status="settled")
    close(r, status="settled")  # a legit terminal (one fully-accounted actual)
    with pytest.raises(ReservationError):
        record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.1, status="settled")


def test_record_actual_rejects_unknown_status(tmp_spend_dir):
    r = _dispatched(TODAY)
    with pytest.raises(ReservationError):
        record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.1, status="bogus")


# --- close: terminal transition without an actual ----------------------------

def test_close_transitions_without_appending_actual(tmp_spend_dir):
    r = _dispatched(TODAY, reserved_cost=12.0)
    record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.10, status="settled")
    close(r, status="settled")
    data = _read(_daily(tmp_spend_dir, TODAY))
    row = next(x for x in data["runs"] if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "settled"
    assert data["total"] == pytest.approx(12.0)  # debit retained
    # close adds NO actual of its own — only the one record_actual row survives.
    ours = [a for a in data["actuals"] if a["reservation_id"] == r.reservation_id]
    assert len(ours) == 1 and ours[0]["attempt_id"] == "a1"


def test_close_unknown_retains_debit(tmp_spend_dir):
    r = _dispatched(TODAY, reserved_cost=12.0)
    close(r, status="unknown")  # zero attempts survived — a fully failed graph
    data = _read(_daily(tmp_spend_dir, TODAY))
    row = next(x for x in data["runs"] if x.get("reservation_id") == r.reservation_id)
    assert row["status"] == "unknown"
    assert data["total"] == pytest.approx(12.0)  # unknown retains the reservation debit
    assert [a for a in data["actuals"] if a["reservation_id"] == r.reservation_id] == []


def test_close_rejects_illegal_transition(tmp_spend_dir):
    r = _reserve(TODAY)  # never dispatched
    with pytest.raises(ReservationError):
        close(r, status="settled")


def test_close_rejects_bad_status(tmp_spend_dir):
    r = _dispatched(TODAY)
    with pytest.raises(ReservationError):
        close(r, status="reserved")


# --- reconcile_generations: pure, idempotent, provider-authoritative ---------

def _ledger_actual(attempt_id, generation_id, usage_cost, status="settled"):
    return {
        "reservation_id": "res-1",
        "run_id": "run-1",
        "attempt_id": attempt_id,
        "generation_id": generation_id,
        "usage_cost": usage_cost,
        "status": status,
    }


def test_reconcile_fills_null_ledger_cost_from_provider_truth():
    actuals = [_ledger_actual("a1", "g1", None, status="unknown")]
    result = reconcile_generations(actuals, {"g1": 0.37})
    assert result.reconciled_total == Decimal("0.37")
    resolved = {r["generation_id"]: r["reconciled_cost"] for r in result.resolved}
    assert resolved == {"g1": Decimal("0.37")}
    assert result.unresolved == [] and result.unaccounted == []


def test_reconcile_surfaces_failed_but_billed_generation_absent_from_ledger():
    # The ledger recorded only g1; the provider billed g1 AND g2 (a failed-but-billed
    # attempt the session never captured). g2 must be surfaced, never laundered to zero.
    actuals = [_ledger_actual("a1", "g1", 0.20)]
    result = reconcile_generations(actuals, {"g1": 0.20, "g2": 0.05})
    assert [u["generation_id"] for u in result.unaccounted] == ["g2"]
    assert result.reconciled_total == Decimal("0.25")  # includes the billed-but-unledgered g2


def test_reconcile_leaves_unresolved_attempt_unknown_never_zero():
    # Ledger has a null-cost attempt whose generation_id the provider has NO record of.
    # It stays unresolved/unknown — NOT zeroed, NOT trusted as billed.
    actuals = [_ledger_actual("a1", "g1", None, status="unknown")]
    result = reconcile_generations(actuals, {})
    assert [u["attempt_id"] for u in result.unresolved] == ["a1"]
    assert result.reconciled_total == Decimal("0")
    assert result.resolved == []


def test_reconcile_confirms_matching_cost():
    actuals = [_ledger_actual("a1", "g1", 0.20)]
    result = reconcile_generations(actuals, {"g1": 0.20})
    assert [c["generation_id"] for c in result.confirmed] == ["g1"]
    assert result.corrected == []
    assert result.reconciled_total == Decimal("0.20")


def test_reconcile_corrects_disagreeing_cost_provider_authoritative():
    actuals = [_ledger_actual("a1", "g1", 0.20)]
    result = reconcile_generations(actuals, {"g1": 0.29})
    corrected = {c["generation_id"]: c["reconciled_cost"] for c in result.corrected}
    assert corrected == {"g1": Decimal("0.29")}  # provider wins
    assert result.reconciled_total == Decimal("0.29")


def test_reconcile_is_idempotent_on_resolved_ledger():
    # First pass resolves g1's null cost; feeding the resolved ledger back with the same
    # provider truth confirms it and yields the identical total.
    first = reconcile_generations(
        [_ledger_actual("a1", "g1", None, status="unknown")], {"g1": 0.37}
    )
    # Feed the returned Decimal back UNCHANGED (no float() laundering) — the helper must
    # accept its own output for the idempotency claim to hold honestly.
    resolved_ledger = [_ledger_actual("a1", "g1", first.reconciled_total, status="settled")]
    second = reconcile_generations(resolved_ledger, {"g1": 0.37})
    assert second.reconciled_total == first.reconciled_total == Decimal("0.37")
    assert [c["generation_id"] for c in second.confirmed] == ["g1"]
    assert second.resolved == [] and second.unresolved == [] and second.unaccounted == []


def test_reconcile_counts_each_provider_generation_once():
    # Provider truth is billed once per generation_id. Even if the ledger somehow holds two
    # rows for the same generation, the honest total must count that billing exactly once —
    # a doubled cost total is dangerously-wrong (silent, trusted, propagating into caps).
    actuals = [_ledger_actual("a1", "g1", 0.20), _ledger_actual("a2", "g1", 0.20)]
    result = reconcile_generations(actuals, {"g1": 0.20})
    assert result.reconciled_total == Decimal("0.20")


def test_reconcile_null_generation_id_actual_stays_unresolved():
    # A terminal/uncaptured actual with no generation_id can't be matched → unresolved.
    actuals = [_ledger_actual("a1", None, None, status="unknown")]
    result = reconcile_generations(actuals, {"g1": 0.10})
    assert [u["attempt_id"] for u in result.unresolved] == ["a1"]
    # g1 is billed by the provider but has no ledger row → unaccounted.
    assert [u["generation_id"] for u in result.unaccounted] == ["g1"]
    assert result.reconciled_total == Decimal("0.10")


# --- Review-hardening (independent Codex pass, F8a.4) -------------------------

def test_record_actual_rejects_settled_with_null_cost(tmp_spend_dir):
    # settled <-> a KNOWN cost. A null-cost "settled" actual would falsely assert the
    # attempt was fully accounted (finding 2).
    r = _dispatched(TODAY)
    with pytest.raises(ReservationError):
        record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=None, status="settled")


def test_record_actual_rejects_unknown_with_nonnull_cost(tmp_spend_dir):
    # unknown <-> NO usable cost. A known cost labelled unknown is contradictory (finding 2).
    r = _dispatched(TODAY)
    with pytest.raises(ReservationError):
        record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.10, status="unknown")


def test_record_actual_rejects_blank_or_nonstring_attempt_id(tmp_spend_dir):
    r = _dispatched(TODAY)
    for bad in ("", None, [], 5):
        with pytest.raises(ReservationError):
            record_actual(r, attempt_id=bad, generation_id="g1", usage_cost=0.1, status="settled")


def test_record_actual_rejects_nonstring_generation_id(tmp_spend_dir):
    r = _dispatched(TODAY)
    for bad in ("", [], 5):  # None IS allowed (uncaptured attempt); "" and non-str are not
        with pytest.raises(ReservationError):
            record_actual(r, attempt_id="a1", generation_id=bad, usage_cost=0.1, status="settled")


def test_close_settled_requires_at_least_one_accounted_actual(tmp_spend_dir):
    # A zero-actual graph must not be laundered into a clean "settled" — only unknown (finding 1).
    r = _dispatched(TODAY)
    with pytest.raises(ReservationError):
        close(r, status="settled")
    close(r, status="unknown")  # unknown is the honest terminal for zero evidence


def test_close_settled_refused_when_an_actual_is_unknown(tmp_spend_dir):
    # If ANY attempt cost is unknown, the graph is not fully accounted → cannot close settled.
    r = _dispatched(TODAY)
    record_actual(r, attempt_id="a1", generation_id="g1", usage_cost=0.10, status="settled")
    record_actual(r, attempt_id="a2", generation_id=None, usage_cost=None, status="unknown")
    with pytest.raises(ReservationError):
        close(r, status="settled")
    close(r, status="unknown")  # honest terminal while an attempt cost is unknown


def test_reconcile_fails_closed_on_corrupt_ledger_money():
    # A corrupt (negative / non-finite) ledger cost must fail closed even when there is no
    # provider truth to compare against — never silently pass as unresolved zero (finding 5).
    for bad in (-7.0, float("inf"), float("nan")):
        with pytest.raises(LedgerCorrupt):
            reconcile_generations([_ledger_actual("a1", "g1", bad)], {})


def test_reconcile_fails_closed_on_nonstring_generation_id():
    # A list generation_id would crash provider.get(); fail closed instead (finding 4).
    with pytest.raises(LedgerCorrupt):
        reconcile_generations([_ledger_actual("a1", [], 0.1)], {"g1": 0.1})


def test_reconcile_provider_none_with_ledger_row_yields_single_unresolved():
    # Provider knows g1 but reports no cost; the ledger already has a g1 row. Exactly one
    # unresolved entry (the real attempt), no phantom provider-only duplicate (finding 6).
    result = reconcile_generations([_ledger_actual("a1", "g1", None, status="unknown")], {"g1": None})
    assert result.unresolved == [{"attempt_id": "a1", "generation_id": "g1"}]
    assert result.reconciled_total == Decimal("0")


def test_reconcile_sub_micro_difference_is_corrected():
    # Any exact disagreement with provider truth is corrected (provider authoritative),
    # even below a micro — no silent micro-tolerance confirming a mismatch (finding 7).
    result = reconcile_generations([_ledger_actual("a1", "g1", 0.10000040)], {"g1": 0.10000049})
    assert [c["generation_id"] for c in result.corrected] == ["g1"]
    assert result.confirmed == []
    assert result.reconciled_total == Decimal("0.10000049")
