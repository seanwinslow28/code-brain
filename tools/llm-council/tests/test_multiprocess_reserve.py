"""Real multiprocess proofs for the shared spend-ledger flock and liveness."""

import ast
import inspect
import json
import multiprocessing
import os
import signal
import textwrap
import time
from datetime import date, datetime, timedelta, timezone
from queue import Empty

from council import budget


RACE_DAY = date(2026, 7, 18)


def _reserve_kwargs(*, run_id, on_date=RACE_DAY, cap=1.0):
    return {
        "reserved_cost": 1.0,
        "tool": "multiprocess-proof",
        "tag": "flock",
        "profile": "test",
        "run_id": run_id,
        "on_date": on_date,
        "per_query_cap": cap,
        "tool_daily_cap": cap,
        "tool_monthly_cap": cap,
        "aggregate_daily_cap": cap,
        "aggregate_monthly_cap": cap,
    }


def _race_reserve_worker(spend_dir, start, results, worker_number):
    os.environ["COUNCIL_SPEND_DIR"] = spend_dir
    start.wait()
    try:
        reservation = budget.check_and_reserve(
            **_reserve_kwargs(run_id=f"race-{worker_number}")
        )
    except budget.BudgetExceeded:
        results.put(("refused", worker_number))
    except BaseException as exc:
        results.put(("error", repr(exc)))
        raise
    else:
        results.put(("admitted", reservation.reservation_id))


def _hold_month_lock_worker(spend_dir, ready):
    os.environ["COUNCIL_SPEND_DIR"] = spend_dir
    with budget.month_lock(RACE_DAY):
        ready.set()
        while True:
            time.sleep(1)


def _single_reserve_worker(spend_dir, results, run_id):
    os.environ["COUNCIL_SPEND_DIR"] = spend_dir
    try:
        reservation = budget.check_and_reserve(
            **_reserve_kwargs(run_id=run_id, cap=10.0)
        )
    except BaseException as exc:
        results.put(("error", repr(exc)))
        raise
    else:
        results.put(("admitted", reservation.reservation_id))


def _reserve_and_dispatch_worker(spend_dir, results, run_id):
    os.environ["COUNCIL_SPEND_DIR"] = spend_dir
    try:
        reservation = budget.check_and_reserve(
            **_reserve_kwargs(run_id=run_id, cap=10.0)
        )
        budget.mark_dispatched(reservation)
    except BaseException as exc:
        results.put(("error", repr(exc)))
        raise
    else:
        results.put(("dispatched", reservation.reservation_id))


def _join_or_fail(processes, timeout=10):
    deadline = time.monotonic() + timeout
    for process in processes:
        process.join(max(0.0, deadline - time.monotonic()))
    stuck = [process for process in processes if process.is_alive()]
    for process in stuck:
        process.kill()
        process.join(2)
    assert not stuck, f"worker processes wedged: {[process.pid for process in stuck]}"


def _collect(results, count):
    collected = []
    for _ in range(count):
        try:
            collected.append(results.get(timeout=2))
        except Empty:
            collected.append(("missing", None))
    return collected


def test_four_processes_race_for_exactly_one_admission(tmp_spend_dir):
    ctx = multiprocessing.get_context("spawn")
    start = ctx.Event()
    results = ctx.Queue()
    processes = [
        ctx.Process(
            target=_race_reserve_worker,
            args=(str(tmp_spend_dir), start, results, worker_number),
        )
        for worker_number in range(4)
    ]
    for process in processes:
        process.start()
    start.set()
    _join_or_fail(processes)

    outcomes = _collect(results, 4)
    assert [process.exitcode for process in processes] == [0, 0, 0, 0]
    assert [kind for kind, _ in outcomes].count("admitted") == 1
    assert [kind for kind, _ in outcomes].count("refused") == 3
    assert [kind for kind, _ in outcomes].count("error") == 0

    state = budget.strict_ledger_state(RACE_DAY)
    assert state["day"]["aggregate"] == 1
    assert state["month"]["aggregate"] == 1
    assert state["day"]["by_tool"]["multiprocess-proof"] == 1


def test_sigkill_releases_flock_and_next_process_reserves(tmp_spend_dir):
    ctx = multiprocessing.get_context("spawn")
    ready = ctx.Event()
    holder = ctx.Process(
        target=_hold_month_lock_worker,
        args=(str(tmp_spend_dir), ready),
    )
    holder.start()
    try:
        assert ready.wait(5), "lock holder never acquired the month flock"

        holder.kill()
        holder.join(5)
        assert holder.exitcode == -signal.SIGKILL

        results = ctx.Queue()
        successor = ctx.Process(
            target=_single_reserve_worker,
            args=(str(tmp_spend_dir), results, "after-killed-lock-owner"),
        )
        successor.start()
        _join_or_fail([successor], timeout=5)

        assert successor.exitcode == 0
        assert _collect(results, 1)[0][0] == "admitted"
    finally:
        if holder.is_alive():
            holder.kill()
        holder.join(5)


def test_sigkill_regression_always_reaps_holder_from_finally():
    source = textwrap.dedent(
        inspect.getsource(test_sigkill_releases_flock_and_next_process_reserves)
    )
    tree = ast.parse(source)
    holder_cleanup_calls = {
        node.func.attr
        for try_node in ast.walk(tree)
        if isinstance(try_node, ast.Try)
        for statement in try_node.finalbody
        for node in ast.walk(statement)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "holder"
    }

    assert {"kill", "join"} <= holder_cleanup_calls


def test_exited_live_and_pid_reuse_owners_follow_liveness_matrix(
    tmp_spend_dir, monkeypatch
):
    ctx = multiprocessing.get_context("spawn")
    results = ctx.Queue()
    exited_owner = ctx.Process(
        target=_reserve_and_dispatch_worker,
        args=(str(tmp_spend_dir), results, "exited-owner"),
    )
    exited_owner.start()
    _join_or_fail([exited_owner])
    exited_kind, exited_id = _collect(results, 1)[0]
    assert exited_owner.exitcode == 0
    assert exited_kind == "dispatched"

    # Some restricted CI sandboxes forbid ps(1). Keep this integration focused on real
    # process liveness/PIDs while supplying one stable OS-query result to both writer and
    # reconciler; _process_start_time's subprocess contract is covered separately.
    monkeypatch.setattr(
        budget,
        "_process_start_time",
        lambda pid: f"os-reported-start-{pid}",
    )
    live = budget.check_and_reserve(
        **_reserve_kwargs(run_id="live-parent", cap=10.0)
    )
    budget.mark_dispatched(live)
    reused = budget.check_and_reserve(
        **_reserve_kwargs(run_id="simulated-pid-reuse", cap=10.0)
    )
    budget.mark_dispatched(reused)

    path = tmp_spend_dir / f"council-spend-{RACE_DAY.isoformat()}.json"
    data = json.loads(path.read_text())
    reused_row = next(
        row for row in data["runs"] if row.get("reservation_id") == reused.reservation_id
    )
    assert reused_row["owner_pid"] == os.getpid()
    assert reused_row["owner_started_at"] == f"os-reported-start-{os.getpid()}"
    reused_row["owner_started_at"] = "doctored process start time"
    path.write_text(json.dumps(data))

    reconciled = budget.reconcile_stale(
        RACE_DAY,
        older_than=datetime.now(timezone.utc) + timedelta(seconds=1),
    )

    assert reconciled == [exited_id, reused.reservation_id]
    rows = {
        row["reservation_id"]: row
        for row in json.loads(path.read_text())["runs"]
        if row.get("kind") == "reservation"
    }
    assert rows[exited_id]["status"] == "unknown"
    assert rows[live.reservation_id]["status"] == "dispatched"
    assert rows[reused.reservation_id]["status"] == "unknown"


def test_previous_month_orphan_is_reconciled_in_next_month_sweep(tmp_spend_dir):
    august_day = date(2026, 8, 20)
    path = tmp_spend_dir / f"council-spend-{august_day.isoformat()}.json"
    row = {
        "amount": 1.0,
        "profile": "test",
        "tag": "previous-month",
        "tool": "council",
        "kind": "reservation",
        "reservation_id": "august-orphan",
        "run_id": "august-run",
        "status": "dispatched",
        "created_at": "2026-08-20T00:00:00+00:00",
        "policy_version": None,
        "policy_hash": None,
    }
    path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "date": august_day.isoformat(),
                "total": 1.0,
                "runs": [row],
                "actuals": [],
            }
        )
    )

    reconciled = budget.reconcile_stale(
        date(2026, 9, 2),
        older_than=datetime(2026, 9, 2, tzinfo=timezone.utc),
    )

    assert reconciled == ["august-orphan"]
    assert json.loads(path.read_text())["runs"][0]["status"] == "unknown"
