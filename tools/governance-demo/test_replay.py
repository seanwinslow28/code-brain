"""Tests for the governance demo. Each fixture must exercise a distinct control leg.

Run:  python -m pytest tools/governance-demo/test_replay.py -v

All tests use --dry-pushover semantics (no network) and a tmp ledger (never touches
the committed outputs/sample_ledger.jsonl).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import replay_budget_breach as rb


def _read_ledger(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def test_allowed_path(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    res = rb.run("allowed", dry_pushover=True, ledger_path=ledger)

    assert res.decision == "allowed"
    assert res.exit_code == rb.EXIT_ALLOWED == 0
    assert res.budget_evaluated is True
    assert res.pushover_fired is False  # an allowed run never pages

    rows = _read_ledger(ledger)
    assert len(rows) == 1
    assert rows[0]["decision"] == "allowed"
    assert rows[0]["exit_code"] == 0


def test_over_budget_path(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    res = rb.run("over_budget", dry_pushover=True, ledger_path=ledger)

    # Circuit trips: distinct exit code, breach decision, human paged (dry), audited.
    assert res.decision == "budget_breach"
    assert res.exit_code == rb.EXIT_BUDGET_BREACH == 7
    assert res.budget_evaluated is True
    assert res.pushover_fired is True
    assert res.pushover_mode == "dry"

    rows = _read_ledger(ledger)
    assert len(rows) == 1
    assert rows[0]["decision"] == "budget_breach"
    assert rows[0]["exit_code"] == 7
    # the breach record proves the projected overshoot was computed before blocking
    assert rows[0]["projected_usd"] > rows[0]["daily_cap_usd"]


def test_missing_auth_path(tmp_path):
    ledger = tmp_path / "ledger.jsonl"
    res = rb.run("missing_auth", dry_pushover=True, ledger_path=ledger)

    # Authority denies at the credential gate BEFORE budget is evaluated.
    assert res.decision == "auth_denied"
    assert res.exit_code == rb.EXIT_AUTH_DENIED == 3
    assert res.budget_evaluated is False  # the key proof: budget never reached
    assert res.pushover_fired is False

    rows = _read_ledger(ledger)
    assert len(rows) == 1
    assert rows[0]["decision"] == "auth_denied"


def test_three_fixtures_exercise_three_distinct_exit_codes(tmp_path):
    """The verification-gate claim: the three fixtures hit three distinct code paths."""
    codes = {
        name: rb.run(name, dry_pushover=True, ledger_path=tmp_path / f"{name}.jsonl").exit_code
        for name in ("allowed", "over_budget", "missing_auth")
    }
    assert codes == {"allowed": 0, "missing_auth": 3, "over_budget": 7}
    assert len(set(codes.values())) == 3  # all distinct


def test_dry_pushover_never_touches_network(tmp_path, monkeypatch):
    """--dry-pushover must not open a connection. Poison urlopen and assert it's unused."""

    def _boom(*_a, **_k):  # pragma: no cover - only runs if the dry guard regresses
        raise AssertionError("dry-pushover must not hit the network")

    monkeypatch.setattr(rb.urllib.request, "urlopen", _boom)
    res = rb.run("over_budget", dry_pushover=True, ledger_path=tmp_path / "l.jsonl")
    assert res.pushover_mode == "dry"


def test_main_returns_exit_code(tmp_path):
    code = rb.main(["--fixture", "over_budget", "--dry-pushover", "--ledger", str(tmp_path / "m.jsonl")])
    assert code == 7


def test_unknown_fixture_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        rb.run("does_not_exist", dry_pushover=True, ledger_path=tmp_path / "x.jsonl")
