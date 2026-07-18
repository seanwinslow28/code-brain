"""F8b Task 2 cap-policy registry, activation, and opt-in enforcement."""

import contextlib
import copy
import json
from datetime import date
from pathlib import Path

import pytest

from council import budget, policy


SHIPPED_POLICY = {
    "policy_version": 1,
    "tools": {
        "council": {
            "per_query_caps": [0.40, 1.00],
            "daily_cap": 7.00,
            "monthly_cap": 40.00,
            "reservation_basis": "estimate",
            "force_per_query_allowed": True,
        },
        "discovery": {
            "per_query_caps": [0.50, 1.50, 4.00, 10.00],
            "daily_cap": 10.00,
            "monthly_cap": 50.00,
            "reservation_basis": "estimate",
            "force_per_query_allowed": True,
        },
        "oracle-forecast": {
            "per_query_caps": [6.50],
            "daily_cap": 150.00,
            "monthly_cap": 650.00,
            "reservation_basis": "worst_case",
            "force_per_query_allowed": False,
        },
        "oracle-retrieve": {
            "per_query_caps": [1.00],
            "daily_cap": 65.00,
            "monthly_cap": 275.00,
            "reservation_basis": "worst_case",
            "force_per_query_allowed": False,
        },
        "baserate": {
            "per_query_caps": [1.00],
            "daily_cap": 30.00,
            "monthly_cap": 75.00,
            "reservation_basis": "worst_case",
            "force_per_query_allowed": False,
        },
    },
    "aggregate": {"daily_cap": 245.00, "monthly_cap": 1000.00},
    "sum_exceeds_aggregate": True,
}


def _write_policy(path: Path, content=None) -> Path:
    path.write_text(json.dumps(content if content is not None else SHIPPED_POLICY))
    return path


def _activated_reserve_kwargs(on_date: date, **overrides) -> dict:
    kwargs = {
        "reserved_cost": 0.10,
        "tool": "oracle-forecast",
        "tag": "policy-test",
        "profile": "premium",
        "run_id": "run-policy",
        "on_date": on_date,
        "per_query_cap": 6.50,
        "tool_daily_cap": 150.00,
        "tool_monthly_cap": 650.00,
        "aggregate_daily_cap": 245.00,
        "aggregate_monthly_cap": 1000.00,
    }
    kwargs.update(overrides)
    return kwargs


def _daily_file(root: Path, on_date: date) -> Path:
    return root / f"council-spend-{on_date.isoformat()}.json"


def _reservation_rows(root: Path, on_date: date) -> list[dict]:
    data = json.loads(_daily_file(root, on_date).read_text())
    return [row for row in data["runs"] if row.get("kind") == "reservation"]


# --- Strict registry loading ------------------------------------------------


def test_shipped_policy_loads_and_equals_approved_census():
    loaded = policy.load_policy()

    assert loaded == SHIPPED_POLICY
    assert loaded["tools"]["council"]["per_query_caps"] == [0.40, 1.00]
    assert loaded["tools"]["discovery"]["per_query_caps"] == [0.50, 1.50, 4.00, 10.00]
    assert loaded["tools"]["oracle-forecast"] == SHIPPED_POLICY["tools"]["oracle-forecast"]
    assert loaded["tools"]["oracle-retrieve"] == SHIPPED_POLICY["tools"]["oracle-retrieve"]
    assert loaded["tools"]["baserate"] == SHIPPED_POLICY["tools"]["baserate"]
    assert loaded["aggregate"] == {"daily_cap": 245.00, "monthly_cap": 1000.00}
    assert loaded["sum_exceeds_aggregate"] is True


def test_load_policy_refuses_missing_file(tmp_path):
    with pytest.raises(policy.PolicyError, match="missing"):
        policy.load_policy(tmp_path / "absent.json")


def test_load_policy_refuses_malformed_json(tmp_path):
    path = tmp_path / "policy.json"
    path.write_text("{not json")
    with pytest.raises(policy.PolicyError, match="malformed JSON"):
        policy.load_policy(path)


def test_load_policy_refuses_duplicate_json_keys(tmp_path):
    path = tmp_path / "policy.json"
    path.write_text(
        '{"policy_version":1,"policy_version":2,"tools":{},'
        '"aggregate":{},"sum_exceeds_aggregate":false}'
    )
    with pytest.raises(policy.PolicyError, match="duplicate JSON key"):
        policy.load_policy(path)


def test_load_policy_refuses_non_object_top_level(tmp_path):
    with pytest.raises(policy.PolicyError, match="top level"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", []))


@pytest.mark.parametrize("mutation", ["missing", "extra"])
def test_load_policy_refuses_wrong_top_level_keys(tmp_path, mutation):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    if mutation == "missing":
        candidate.pop("aggregate")
    else:
        candidate["unexpected"] = True
    with pytest.raises(policy.PolicyError, match="top-level keys"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize("value", [True, 0, -1, 1.5, "1"])
def test_load_policy_refuses_non_positive_integer_policy_version(tmp_path, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["policy_version"] = value
    with pytest.raises(policy.PolicyError, match="policy_version"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize("value", [{}, [], "tools"])
def test_load_policy_refuses_tools_that_are_not_a_nonempty_object(tmp_path, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"] = value
    with pytest.raises(policy.PolicyError, match="tools"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize("mutation", ["missing", "extra"])
def test_load_policy_refuses_wrong_tool_entry_keys(tmp_path, mutation):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    tool = candidate["tools"]["council"]
    if mutation == "missing":
        tool.pop("daily_cap")
    else:
        tool["unexpected"] = 1
    with pytest.raises(policy.PolicyError, match="tool.*keys"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize("value", [None, [], "1.0"])
def test_load_policy_refuses_per_query_caps_that_are_not_a_nonempty_list(tmp_path, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"]["per_query_caps"] = value
    with pytest.raises(policy.PolicyError, match="per_query_caps"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize(
    "value",
    [[0.40, 0.40], [0.40, True], [0.40, 0], [0.40, -1], [0.40, float("inf")]],
)
def test_load_policy_refuses_non_unique_or_non_positive_finite_per_query_caps(tmp_path, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"]["per_query_caps"] = value
    with pytest.raises(policy.PolicyError, match="per_query_caps"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


def test_load_policy_refuses_unsorted_per_query_caps(tmp_path):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"]["per_query_caps"] = [1.00, 0.40]
    with pytest.raises(policy.PolicyError, match="sorted ascending"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize(
    ("field", "value"),
    [("daily_cap", True), ("daily_cap", 0), ("monthly_cap", -1), ("monthly_cap", float("nan"))],
)
def test_load_policy_refuses_non_positive_finite_tool_caps(tmp_path, field, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"][field] = value
    with pytest.raises(policy.PolicyError, match=field):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


def test_load_policy_refuses_tool_daily_cap_above_monthly_cap(tmp_path):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"]["daily_cap"] = 41.00
    with pytest.raises(policy.PolicyError, match="daily_cap.*monthly_cap"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


def test_load_policy_refuses_unknown_reservation_basis(tmp_path):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"]["reservation_basis"] = "hope"
    with pytest.raises(policy.PolicyError, match="reservation_basis"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize("value", [0, 1, None, "false"])
def test_load_policy_refuses_non_boolean_force_permission(tmp_path, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"]["force_per_query_allowed"] = value
    with pytest.raises(policy.PolicyError, match="force_per_query_allowed"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize(
    "value",
    [[], {"daily_cap": 245.0}, {"daily_cap": 245.0, "monthly_cap": 1000.0, "extra": 1}],
)
def test_load_policy_refuses_malformed_aggregate(tmp_path, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["aggregate"] = value
    with pytest.raises(policy.PolicyError, match="aggregate"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize(
    ("field", "value"),
    [("daily_cap", False), ("daily_cap", 0), ("monthly_cap", float("inf"))],
)
def test_load_policy_refuses_non_positive_finite_aggregate_caps(tmp_path, field, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["aggregate"][field] = value
    with pytest.raises(policy.PolicyError, match=f"aggregate.{field}"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


def test_load_policy_refuses_aggregate_daily_cap_above_monthly_cap(tmp_path):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["aggregate"] = {"daily_cap": 1001.0, "monthly_cap": 1000.0}
    with pytest.raises(policy.PolicyError, match="aggregate.daily_cap.*monthly_cap"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize("value", [0, 1, None, "true"])
def test_load_policy_refuses_non_boolean_sum_relation_flag(tmp_path, value):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["sum_exceeds_aggregate"] = value
    with pytest.raises(policy.PolicyError, match="sum_exceeds_aggregate"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


def test_load_policy_refuses_true_sum_flag_when_neither_sum_exceeds(tmp_path):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["aggregate"] = {"daily_cap": 300.0, "monthly_cap": 1200.0}
    with pytest.raises(
        policy.PolicyError,
        match=r"daily sum 262.*daily aggregate 300.*monthly sum 1090.*monthly aggregate 1200",
    ):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


def test_load_policy_refuses_false_sum_flag_when_either_sum_exceeds(tmp_path):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["sum_exceeds_aggregate"] = False
    with pytest.raises(
        policy.PolicyError,
        match=r"daily sum 262.*daily aggregate 245.*monthly sum 1090.*monthly aggregate 1000",
    ):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


# --- Canonical hash + checkout-relative packaging --------------------------


def test_policy_hash_is_stable_across_source_key_order(tmp_path):
    first = _write_policy(tmp_path / "first.json")
    reordered = {
        "sum_exceeds_aggregate": True,
        "aggregate": {"monthly_cap": 1000.00, "daily_cap": 245.00},
        "tools": dict(reversed(list(SHIPPED_POLICY["tools"].items()))),
        "policy_version": 1,
    }
    second = _write_policy(tmp_path / "second.json", reordered)

    assert policy.policy_hash(policy.load_policy(first)) == policy.policy_hash(policy.load_policy(second))


def test_policy_hash_changes_when_a_value_changes(tmp_path):
    changed = copy.deepcopy(SHIPPED_POLICY)
    changed["policy_version"] = 2
    changed["tools"]["oracle-forecast"]["monthly_cap"] = 651.00

    original_hash = policy.policy_hash(policy.load_policy(_write_policy(tmp_path / "v1.json")))
    changed_hash = policy.policy_hash(policy.load_policy(_write_policy(tmp_path / "v2.json", changed)))

    assert changed_hash != original_hash


def test_default_policy_path_is_relative_to_installed_council_package(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert policy.load_policy() == SHIPPED_POLICY
    assert Path(policy.__file__).with_name("cap_policy.json").is_file()


# --- Shared activation ------------------------------------------------------


def test_activate_policy_writes_atomic_round_trippable_snapshot(tmp_spend_dir):
    record = policy.activate_policy(root=tmp_spend_dir)
    active_path = tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME

    assert active_path.is_file()
    assert policy.load_active_policy(tmp_spend_dir) == record
    assert record["policy"] == SHIPPED_POLICY
    assert record["policy_version"] == 1
    assert record["policy_hash"] == policy.policy_hash(record["policy"])
    assert record["activated_at_utc"].endswith("+00:00")
    assert list(tmp_spend_dir.glob(f"{policy.ACTIVE_POLICY_FILENAME}.*.tmp")) == []


def test_load_active_policy_returns_none_when_activation_is_absent(tmp_spend_dir):
    assert policy.load_active_policy(tmp_spend_dir) is None


def test_load_active_policy_refuses_malformed_json(tmp_spend_dir):
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_text("{not json")
    with pytest.raises(budget.LedgerCorrupt, match="activation.*malformed JSON"):
        policy.load_active_policy(tmp_spend_dir)


def test_load_active_policy_refuses_duplicate_json_keys(tmp_spend_dir):
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_text(
        '{"policy_version":1,"policy_version":1,"policy_hash":"x",'
        '"activated_at_utc":"x","policy":{}}'
    )
    with pytest.raises(budget.LedgerCorrupt, match="duplicate JSON key"):
        policy.load_active_policy(tmp_spend_dir)


def test_load_active_policy_refuses_hash_mismatch(tmp_spend_dir):
    record = policy.activate_policy(root=tmp_spend_dir)
    record["policy"]["aggregate"]["daily_cap"] = 244.00
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_text(json.dumps(record))
    with pytest.raises(budget.LedgerCorrupt, match="hash mismatch"):
        policy.load_active_policy(tmp_spend_dir)


def test_load_active_policy_refuses_missing_required_key(tmp_spend_dir):
    record = policy.activate_policy(root=tmp_spend_dir)
    record.pop("activated_at_utc")
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_text(json.dumps(record))
    with pytest.raises(budget.LedgerCorrupt, match="activation keys"):
        policy.load_active_policy(tmp_spend_dir)


def test_load_active_policy_refuses_invalid_embedded_policy_even_with_matching_hash(tmp_spend_dir):
    record = policy.activate_policy(root=tmp_spend_dir)
    record["policy"]["tools"]["council"]["per_query_caps"] = [1.0, 0.4]
    record["policy_hash"] = policy.policy_hash(record["policy"])
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_text(json.dumps(record))
    with pytest.raises(budget.LedgerCorrupt, match="embedded policy"):
        policy.load_active_policy(tmp_spend_dir)


def test_activate_policy_takes_current_utc_month_lock_once(tmp_spend_dir, tmp_path, monkeypatch):
    today = date(2026, 7, 18)
    acquired = []

    @contextlib.contextmanager
    def spy_month_lock(on_date, *, root=None):
        acquired.append((on_date, root))
        yield

    monkeypatch.setattr(budget, "utc_accounting_date", lambda: today)
    monkeypatch.setattr(budget, "month_lock", spy_month_lock)

    policy.activate_policy(policy_path=_write_policy(tmp_path / "policy.json"), root=tmp_spend_dir)

    assert acquired == [(today, tmp_spend_dir)]


def test_policy_cli_activate_prints_version_and_hash(tmp_spend_dir, capsys):
    expected_hash = policy.policy_hash(policy.load_policy())

    assert policy.main(["activate"]) == 0

    output = capsys.readouterr()
    assert "version 1" in output.out
    assert expected_hash in output.out
    assert output.err == ""


def test_policy_cli_activate_exits_nonzero_with_error_on_refusal(tmp_path, capsys):
    malformed = tmp_path / "malformed.json"
    malformed.write_text("{not json")

    assert policy.main(["activate", "--policy", str(malformed)]) != 0

    assert "malformed JSON" in capsys.readouterr().err


# --- Enforcement against the shared activation -----------------------------


def test_active_policy_is_cross_checkout_authority_and_stamps_legacy_callers(
    tmp_spend_dir, tmp_path, monkeypatch
):
    v1_path = _write_policy(tmp_path / "checkout-v1.json")
    v2 = copy.deepcopy(SHIPPED_POLICY)
    v2["policy_version"] = 2
    v2["tools"]["oracle-forecast"]["monthly_cap"] = 651.00
    v2_path = _write_policy(tmp_path / "checkout-v2.json", v2)
    active = policy.activate_policy(v1_path, root=tmp_spend_dir)
    v2_hash = policy.policy_hash(policy.load_policy(v2_path))
    today = budget.utc_accounting_date()
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)

    budget.check_and_reserve(
        **_activated_reserve_kwargs(
            today,
            run_id="v1-explicit",
            policy_version=active["policy_version"],
            policy_hash=active["policy_hash"],
        )
    )
    with pytest.raises(budget.ReservationError, match="active policy"):
        budget.check_and_reserve(
            **_activated_reserve_kwargs(
                today,
                run_id="v2-stale-checkout",
                tool_monthly_cap=651.00,
                policy_version=2,
                policy_hash=v2_hash,
            )
        )
    budget.check_and_reserve(**_activated_reserve_kwargs(today, run_id="legacy-unstamped"))

    rows = _reservation_rows(tmp_spend_dir, today)
    assert [(row["run_id"], row["policy_version"], row["policy_hash"]) for row in rows] == [
        ("v1-explicit", 1, active["policy_hash"]),
        ("legacy-unstamped", 1, active["policy_hash"]),
    ]


def test_enforcement_refuses_only_one_policy_identity_field(tmp_spend_dir, monkeypatch):
    active = policy.activate_policy(root=tmp_spend_dir)
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)

    with pytest.raises(budget.ReservationError, match="both policy_version and policy_hash"):
        budget.check_and_reserve(
            **_activated_reserve_kwargs(
                budget.utc_accounting_date(), policy_version=active["policy_version"]
            )
        )


def test_enforcement_refuses_per_query_cap_outside_activated_enumeration(
    tmp_spend_dir, monkeypatch
):
    policy.activate_policy(root=tmp_spend_dir)
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)

    with pytest.raises(budget.ReservationError, match="per_query_cap drift"):
        budget.check_and_reserve(
            **_activated_reserve_kwargs(budget.utc_accounting_date(), per_query_cap=6.51)
        )


def test_enforcement_refuses_tool_daily_cap_drift_by_one_cent(tmp_spend_dir, monkeypatch):
    policy.activate_policy(root=tmp_spend_dir)
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)

    with pytest.raises(budget.ReservationError, match="tool_daily_cap drift"):
        budget.check_and_reserve(
            **_activated_reserve_kwargs(budget.utc_accounting_date(), tool_daily_cap=150.01)
        )


def test_enforcement_refuses_unknown_tool(tmp_spend_dir, monkeypatch):
    policy.activate_policy(root=tmp_spend_dir)
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)

    with pytest.raises(budget.ReservationError, match="tool.*not in active policy"):
        budget.check_and_reserve(
            **_activated_reserve_kwargs(budget.utc_accounting_date(), tool="unknown-tool")
        )


def test_enforcement_on_without_activation_preserves_legacy_null_policy(
    tmp_spend_dir, monkeypatch
):
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)
    today = budget.utc_accounting_date()

    budget.check_and_reserve(
        **_activated_reserve_kwargs(
            today,
            tool="not-registered",
            per_query_cap=99.0,
            tool_daily_cap=99.0,
            tool_monthly_cap=99.0,
            aggregate_daily_cap=99.0,
            aggregate_monthly_cap=99.0,
        )
    )

    row = _reservation_rows(tmp_spend_dir, today)[0]
    assert row["policy_version"] is None
    assert row["policy_hash"] is None


def test_shipped_enforcement_off_never_consults_policy_and_does_not_stamp(
    tmp_spend_dir, monkeypatch
):
    """OFF is proven by absence of consultation, not just by a successful admission
    (review finding 4): any read of the activation file while the flag is False trips
    the bomb, so a regression that partially un-gates the policy path fails loudly."""
    assert budget.POLICY_ENFORCEMENT_ENABLED is False
    policy.activate_policy(root=tmp_spend_dir)

    def _bomb(root):
        raise AssertionError("policy.load_active_policy consulted while enforcement is OFF")

    monkeypatch.setattr(policy, "load_active_policy", _bomb)
    today = budget.utc_accounting_date()

    budget.check_and_reserve(
        **_activated_reserve_kwargs(
            today,
            tool="not-registered",
            per_query_cap=99.0,
            tool_daily_cap=99.0,
            tool_monthly_cap=99.0,
            aggregate_daily_cap=99.0,
            aggregate_monthly_cap=99.0,
        )
    )

    row = _reservation_rows(tmp_spend_dir, today)[0]
    assert row["policy_version"] is None
    assert row["policy_hash"] is None


# --- Review-round regressions (Task 2 round 2) ------------------------------


def test_activation_with_boolean_outer_version_is_ledger_corrupt(tmp_spend_dir):
    record = policy.activate_policy(root=tmp_spend_dir)
    record["policy_version"] = True  # True == 1 must NOT launder through equality
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_text(json.dumps(record))
    with pytest.raises(budget.LedgerCorrupt, match="policy_version must be an integer"):
        policy.load_active_policy(tmp_spend_dir)


def test_activation_with_non_string_hash_is_ledger_corrupt(tmp_spend_dir):
    record = policy.activate_policy(root=tmp_spend_dir)
    record["policy_hash"] = 1
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_text(json.dumps(record))
    with pytest.raises(budget.LedgerCorrupt, match="policy_hash must be a string"):
        policy.load_active_policy(tmp_spend_dir)


def test_enforcement_refuses_boolean_caller_policy_version(tmp_spend_dir, monkeypatch):
    active = policy.activate_policy(root=tmp_spend_dir)
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)

    with pytest.raises(budget.ReservationError, match="policy_version must be an integer"):
        budget.check_and_reserve(
            **_activated_reserve_kwargs(
                budget.utc_accounting_date(),
                policy_version=True,
                policy_hash=active["policy_hash"],
            )
        )


def test_enforcement_refuses_non_string_caller_policy_hash(tmp_spend_dir, monkeypatch):
    active = policy.activate_policy(root=tmp_spend_dir)
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)

    with pytest.raises(budget.ReservationError, match="policy_hash must be a string"):
        budget.check_and_reserve(
            **_activated_reserve_kwargs(
                budget.utc_accounting_date(),
                policy_version=active["policy_version"],
                policy_hash=12345,
            )
        )


def test_load_policy_refuses_unhashable_reservation_basis_as_policy_error(tmp_path):
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["tools"]["council"]["reservation_basis"] = []  # was a raw TypeError
    with pytest.raises(policy.PolicyError, match="reservation_basis"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


def test_load_policy_refuses_invalid_utf8_as_policy_error(tmp_path):
    path = tmp_path / "policy.json"
    path.write_bytes(b"\xff\xfe{}")
    with pytest.raises(policy.PolicyError, match="not valid UTF-8"):
        policy.load_policy(path)


def test_load_active_policy_refuses_invalid_utf8_as_ledger_corrupt(tmp_spend_dir):
    (tmp_spend_dir / policy.ACTIVE_POLICY_FILENAME).write_bytes(b"\xff\xfe{}")
    with pytest.raises(budget.LedgerCorrupt, match="not valid UTF-8"):
        policy.load_active_policy(tmp_spend_dir)


def test_load_policy_refuses_integer_money_so_hashes_stay_canonical(tmp_path):
    """245 vs 245.00 parse to == policies but hash differently (review finding 3);
    the loader closes the class by requiring money to be authored as a JSON decimal."""
    candidate = copy.deepcopy(SHIPPED_POLICY)
    candidate["aggregate"]["daily_cap"] = 245  # int, not 245.0
    with pytest.raises(policy.PolicyError, match="JSON decimal"):
        policy.load_policy(_write_policy(tmp_path / "policy.json", candidate))


@pytest.mark.parametrize(
    "mutate",
    [
        lambda p: p.__setitem__("policy_version", 2),
        lambda p: p["tools"]["oracle-forecast"].__setitem__("monthly_cap", 651.00),
        lambda p: p["tools"]["council"].__setitem__("force_per_query_allowed", False),
    ],
)
def test_policy_hash_is_sensitive_to_each_field_independently(tmp_path, mutate):
    base_hash = policy.policy_hash(policy.load_policy(_write_policy(tmp_path / "base.json")))
    changed = copy.deepcopy(SHIPPED_POLICY)
    mutate(changed)
    changed_hash = policy.policy_hash(
        policy.load_policy(_write_policy(tmp_path / "changed.json", changed))
    )
    assert changed_hash != base_hash
