"""F8b Task 5 enforcement-flip regressions."""

import ast
import json
import os
import socket
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from council import budget, policy


_LEGACY_BUDGET_APIS = {"preflight", "preflight_tool", "record_spend"}


def _legacy_budget_api_references(source):
    references = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom):
            for imported in node.names:
                if imported.name in _LEGACY_BUDGET_APIS:
                    references.append((node.lineno, imported.name))
            continue
        if isinstance(node, ast.Import):
            for imported in node.names:
                name = imported.name.rsplit(".", 1)[-1]
                if name in _LEGACY_BUDGET_APIS:
                    references.append((node.lineno, name))
            continue
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        else:
            name = None
        if name in _LEGACY_BUDGET_APIS:
            references.append((node.lineno, name))
    return references


def test_policy_enforcement_is_shipped_on():
    assert budget.POLICY_ENFORCEMENT_ENABLED is True


def test_record_spend_refuses_unknown_tool_under_activation(tmp_spend_dir):
    policy.activate_policy(root=tmp_spend_dir)

    with pytest.raises(budget.ReservationError, match="not in active policy"):
        budget.record_spend(
            amount=0.10,
            profile="legacy",
            tag="plain-debit",
            on_date=date(2026, 7, 18),
            tool="unknown-tool",
        )


def test_record_spend_refuses_registered_tool_under_activation(tmp_spend_dir):
    policy.activate_policy(root=tmp_spend_dir)

    with pytest.raises(budget.ReservationError, match="use check_and_reserve"):
        budget.record_spend(
            amount=0.10,
            profile="legacy",
            tag="plain-debit",
            on_date=date(2026, 7, 18),
            tool="council",
        )


def test_check_and_reserve_writes_os_owner_identity(tmp_spend_dir):
    today = date(2026, 7, 18)

    reservation = budget.check_and_reserve(
        reserved_cost=0.10,
        tool="unregistered-before-activation",
        tag="owner",
        profile="test",
        run_id="owner-run",
        on_date=today,
        per_query_cap=1.0,
        tool_daily_cap=1.0,
        tool_monthly_cap=1.0,
        aggregate_daily_cap=1.0,
        aggregate_monthly_cap=1.0,
    )

    data = json.loads(
        (tmp_spend_dir / f"council-spend-{today.isoformat()}.json").read_text()
    )
    row = next(
        row
        for row in data["runs"]
        if row.get("reservation_id") == reservation.reservation_id
    )
    assert row["owner_pid"] == os.getpid()
    assert row["owner_host"] == socket.gethostname()
    assert row["owner_started_at"] == budget._process_start_time(os.getpid())


def test_process_start_time_uses_os_ps_identity_query(monkeypatch):
    captured = {}

    def _run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0, stdout=" Mon Jul 18 12:00:00 2026 \n")

    monkeypatch.setattr(budget.subprocess, "run", _run)

    assert budget._process_start_time(4321) == "Mon Jul 18 12:00:00 2026"
    assert captured == {
        "command": ["ps", "-p", "4321", "-o", "lstart="],
        "kwargs": {
            "capture_output": True,
            "text": True,
            "check": False,
            "timeout": 5,
        },
    }


def test_reservation_records_null_start_identity_when_os_query_fails(
    tmp_spend_dir, monkeypatch
):
    monkeypatch.setattr(budget, "_process_start_time", lambda _pid: None)
    today = date(2026, 7, 18)

    budget.check_and_reserve(
        reserved_cost=0.10,
        tool="pre-activation",
        tag="owner-query-failed",
        profile="test",
        run_id="null-owner-start",
        on_date=today,
        per_query_cap=1.0,
        tool_daily_cap=1.0,
        tool_monthly_cap=1.0,
        aggregate_daily_cap=1.0,
        aggregate_monthly_cap=1.0,
    )

    data = json.loads(
        (tmp_spend_dir / f"council-spend-{today.isoformat()}.json").read_text()
    )
    assert data["runs"][0]["owner_started_at"] is None


def test_record_spend_without_activation_keeps_exact_legacy_bytes(tmp_spend_dir):
    today = date(2026, 7, 18)
    budget.record_spend(
        amount=0.25,
        profile="legacy",
        tag="pre-activation",
        on_date=today,
        tool="unregistered-legacy-tool",
    )

    expected = {
        "date": today.isoformat(),
        "total": 0.25,
        "runs": [
            {
                "amount": 0.25,
                "profile": "legacy",
                "tag": "pre-activation",
                "tool": "unregistered-legacy-tool",
            }
        ],
    }
    path = tmp_spend_dir / f"council-spend-{today.isoformat()}.json"
    assert path.read_text() == json.dumps(expected, indent=2)


def test_active_policy_counts_pre_activation_null_policy_reservation(
    tmp_spend_dir,
):
    today = date(2026, 7, 18)
    path = tmp_spend_dir / f"council-spend-{today.isoformat()}.json"
    legacy_row = {
        "amount": 149.0,
        "profile": "premium",
        "tag": "pre-activation",
        "tool": "oracle-forecast",
        "kind": "reservation",
        "reservation_id": "legacy-null-policy",
        "run_id": "legacy-run",
        "status": "unknown",
        "created_at": "2026-07-17T00:00:00+00:00",
        "policy_version": None,
        "policy_hash": None,
    }
    path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "date": today.isoformat(),
                "total": 149.0,
                "runs": [legacy_row],
                "actuals": [],
            }
        )
    )
    active = policy.activate_policy(root=tmp_spend_dir)

    budget.check_and_reserve(
        reserved_cost=1.0,
        tool="oracle-forecast",
        tag="post-activation",
        profile="premium",
        run_id="new-run",
        on_date=today,
        per_query_cap=6.50,
        tool_daily_cap=150.00,
        tool_monthly_cap=650.00,
        aggregate_daily_cap=245.00,
        aggregate_monthly_cap=1000.00,
    )

    data = json.loads(path.read_text())
    assert data["total"] == 150.0
    assert data["runs"][0]["policy_version"] is None
    assert data["runs"][0]["policy_hash"] is None
    assert data["runs"][1]["policy_version"] == active["policy_version"]
    assert data["runs"][1]["policy_hash"] == active["policy_hash"]


def test_legacy_preflight_docstrings_are_explicitly_deprecated():
    notice = "DEPRECATED: not a production admission path (F8b Task 5); importable for tests only."
    assert notice in budget.preflight.__doc__
    assert notice in budget.preflight_tool.__doc__


def test_production_sources_have_no_legacy_preflight_calls():
    project_root = Path(__file__).resolve().parents[1]
    production = [
        path
        for tree in (project_root / "council", project_root / "experiments")
        for path in tree.rglob("*.py")
        if "tests" not in path.parts
    ]
    call_sites = []
    for path in production:
        for lineno, name in _legacy_budget_api_references(path.read_text()):
            if name in {"preflight", "preflight_tool"}:
                call_sites.append((path.relative_to(project_root), lineno, name))

    assert call_sites == []


def test_production_sources_have_no_record_spend_calls():
    project_root = Path(__file__).resolve().parents[1]
    call_sites = []
    for tree_root in (project_root / "council", project_root / "experiments"):
        for path in tree_root.rglob("*.py"):
            if "tests" in path.parts:
                continue
            for lineno, name in _legacy_budget_api_references(path.read_text()):
                if name == "record_spend":
                    call_sites.append((path.relative_to(project_root), lineno))

    assert call_sites == []


def test_legacy_budget_api_guard_catches_aliased_import():
    source = "from council.budget import preflight as admit\n\nadmit(estimated=1)\n"

    assert _legacy_budget_api_references(source) == [(1, "preflight")]


def test_production_sources_have_no_budget_bypass_terms():
    project_root = Path(__file__).resolve().parents[1]
    hits = []
    for tree in (project_root / "council", project_root / "experiments"):
        for path in tree.rglob("*.py"):
            if "tests" in path.parts:
                continue
            source = path.read_text()
            for term in ("skip-budget-check", "skip_budget_check"):
                if term in source:
                    hits.append((path.relative_to(project_root), term))

    assert hits == []


def test_gateway_and_kernel_sources_never_use_local_date_today():
    project_root = Path(__file__).resolve().parents[1]
    paths = (
        project_root / "council" / "budget.py",
        project_root / "council" / "cli.py",
        project_root / "council" / "discovery" / "__main__.py",
        project_root / "experiments" / "panel_vs_single.py",
    )

    assert all("date.today()" not in path.read_text() for path in paths)


def test_budget_documents_local_filesystem_only_flock_contract():
    assert "LOCAL filesystem" in budget.__doc__
    assert "flock on NFS is unsupported" in budget.__doc__
