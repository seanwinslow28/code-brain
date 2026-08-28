"""F8b Task 4: discovery writers use the locked reserve lifecycle."""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from council import budget, policy, reservations
from council.discovery import __main__ as discovery_cli
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionError, FusionResult
from council.discovery.pipeline import DiscoveryFailed, DiscoveryResult
from experiments import panel_vs_single as experiment_cli


def _ledger(spend_dir: Path) -> dict:
    files = sorted(spend_dir.glob("council-spend-????-??-??.json"))
    assert len(files) == 1
    return json.loads(files[0].read_text())


def _reservation_rows(spend_dir: Path) -> list[dict]:
    return [r for r in _ledger(spend_dir)["runs"] if r.get("kind") == "reservation"]


def _discovery_result(cost) -> DiscoveryResult:
    return DiscoveryResult(
        markdown="# Idea Ledger\nok",
        cost_usd=cost,
        verified_count=1,
        dropped_count=0,
        session={"id": "s"},
    )


def _experiment_result() -> dict:
    bundle = EvidenceBundle()
    bundle.add(
        EvidenceRecord(
            source_type="web",
            source_name="X",
            url="https://example.com/evidence",
            date="",
            quote="q",
        )
    )
    point = CandidatePainPoint(
        title="Pain", summary="s", quotes=["q"], urls=["https://example.com/evidence"]
    )
    arm_a = FusionResult(pain_points=[point], cost=0.12)
    arm_b = FusionResult(pain_points=[point], cost=0.05)
    return {
        "bundle": bundle,
        "gather_status": {"web": "ok"},
        "arm_a": arm_a,
        "arm_b": arm_b,
        "cost": 0.17,
    }


def test_discovery_cli_reserves_dispatches_records_estimate_and_closes_unknown(
    tmp_path, tmp_spend_dir, fake_api_key, monkeypatch
):
    async def fake_run(**kwargs):
        row = _reservation_rows(tmp_spend_dir)[0]
        assert row["status"] == "dispatched"
        assert kwargs["api_key"] == fake_api_key
        return _discovery_result(0.42)

    monkeypatch.setattr(discovery_cli, "run_discovery", fake_run)
    out = tmp_path / "ledger.md"

    result = CliRunner().invoke(
        discovery_cli.main,
        ["roadmap tools", "--tier", "quick", "--output", str(out)],
    )

    assert result.exit_code == 0, result.output
    ledger = _ledger(tmp_spend_dir)
    row = _reservation_rows(tmp_spend_dir)[0]
    assert row["amount"] == 3.232560
    assert row["status"] == "unknown"
    assert row["profile"] == "quick"
    assert row["tag"] == "discovery-pm"
    assert ledger["total"] == 3.232560
    assert len(ledger["actuals"]) == 1
    actual = ledger["actuals"][0]
    assert actual["reservation_id"] == row["reservation_id"]
    assert actual["usage_cost"] == 0.42
    assert actual["status"] == "settled"
    assert actual["provenance"] == "estimated"
    assert "estimated" in result.output.lower()
    assert "0.42" in result.output
    assert out.read_text().startswith("# Idea Ledger")


def test_discovery_cli_failure_retains_estimated_actual_and_unknown_debit(
    tmp_path, tmp_spend_dir, fake_api_key, monkeypatch
):
    async def fail(**kwargs):
        assert _reservation_rows(tmp_spend_dir)[0]["status"] == "dispatched"
        raise DiscoveryFailed(
            "fuse blew up",
            cost_usd=0.42,
            session={
                "failed_stage": "fuse",
                "gather_status": {"sonar": "ok: 3 records (3 found)"},
            },
        )

    monkeypatch.setattr(discovery_cli, "run_discovery", fail)

    result = CliRunner().invoke(
        discovery_cli.main,
        ["obsidian", "--tier", "quick", "--output", str(tmp_path / "out.md")],
    )

    assert result.exit_code == 3
    ledger = _ledger(tmp_spend_dir)
    row = _reservation_rows(tmp_spend_dir)[0]
    assert row["status"] == "unknown"
    assert ledger["actuals"][0]["usage_cost"] == 0.42
    assert ledger["actuals"][0]["provenance"] == "estimated"
    assert "Gather status" in result.output
    assert "estimated" in result.output.lower()


@pytest.mark.parametrize("unusable_cost", [None, float("inf"), True])
def test_discovery_cli_unusable_success_cost_records_unknown_actual(
    unusable_cost, tmp_path, tmp_spend_dir, fake_api_key, monkeypatch
):
    async def fake_run(**kwargs):
        return _discovery_result(unusable_cost)

    monkeypatch.setattr(discovery_cli, "run_discovery", fake_run)

    result = CliRunner().invoke(
        discovery_cli.main,
        ["x", "--tier", "quick", "--output", str(tmp_path / "out.md")],
    )

    assert result.exit_code == 0, result.output
    ledger = _ledger(tmp_spend_dir)
    row = _reservation_rows(tmp_spend_dir)[0]
    assert row["status"] == "unknown"
    assert ledger["actuals"][0]["usage_cost"] is None
    assert ledger["actuals"][0]["status"] == "unknown"
    assert ledger["actuals"][0]["provenance"] == "unknown"


def test_discovery_cli_budget_rejection_exits_before_dispatch(
    tmp_path, tmp_spend_dir, fake_api_key, monkeypatch
):
    ran = False

    async def forbidden_run(**kwargs):
        nonlocal ran
        ran = True

    def reject(**kwargs):
        raise budget.BudgetExceeded("nope")

    monkeypatch.setattr(discovery_cli.budget, "check_and_reserve", reject)
    monkeypatch.setattr(discovery_cli, "run_discovery", forbidden_run)

    result = CliRunner().invoke(
        discovery_cli.main,
        ["x", "--tier", "quick", "--output", str(tmp_path / "out.md")],
    )

    assert result.exit_code == 2
    assert "Budget rejected" in result.output
    assert ran is False
    assert not list(tmp_spend_dir.glob("council-spend-????-??-??.json"))


def test_discovery_force_only_bypasses_amount_not_activated_cap_enumeration(
    tmp_path, tmp_spend_dir, fake_api_key, monkeypatch
):
    policy.activate_policy(root=tmp_spend_dir)
    monkeypatch.setattr(budget, "POLICY_ENFORCEMENT_ENABLED", True)
    monkeypatch.setattr(reservations, "discovery_worst_case_reservation", lambda tier: 3.26)

    async def fake_run(**kwargs):
        return _discovery_result(0.10)

    monkeypatch.setattr(discovery_cli, "run_discovery", fake_run)
    admitted = CliRunner().invoke(
        discovery_cli.main,
        [
            "x",
            "--tier",
            "quick",
            "--force",
            "--output",
            str(tmp_path / "admitted.md"),
        ],
    )
    assert admitted.exit_code == 0, admitted.output
    assert len(_reservation_rows(tmp_spend_dir)) == 1

    monkeypatch.setitem(discovery_cli.TIER_PER_QUERY_CAP, "quick", 3.26)
    refused = CliRunner().invoke(
        discovery_cli.main,
        [
            "x",
            "--tier",
            "quick",
            "--force",
            "--output",
            str(tmp_path / "refused.md"),
        ],
    )
    assert refused.exit_code != 0
    assert isinstance(refused.exception, budget.ReservationError)
    assert "per_query_cap drift" in str(refused.exception)
    assert len(_reservation_rows(tmp_spend_dir)) == 1


def test_discovery_tier_caps_are_registry_members_and_cover_reservations():
    enumerated = set(policy.load_policy()["tools"]["discovery"]["per_query_caps"])

    assert set(discovery_cli.TIER_PER_QUERY_CAP.values()) <= enumerated
    for tier_name, cap in discovery_cli.TIER_PER_QUERY_CAP.items():
        assert cap >= reservations.discovery_worst_case_reservation(
            discovery_cli.get_tier(tier_name)
        )


def test_experiment_cli_records_each_estimated_arm_and_closes_unknown(
    tmp_path, tmp_spend_dir, fake_api_key, monkeypatch
):
    async def fake_core(**kwargs):
        assert _reservation_rows(tmp_spend_dir)[0]["status"] == "dispatched"
        kwargs["record_fn"](amount=0.12, ignored="core metadata")
        kwargs["record_fn"](amount=0.05, profile="ignored")
        return _experiment_result()

    monkeypatch.setattr(experiment_cli, "run_panel_vs_single", fake_core)
    out = tmp_path / "experiment"

    result = CliRunner().invoke(
        experiment_cli.main,
        ["--yes", "--tier", "standard", "--out", str(out)],
    )

    assert result.exit_code == 0, result.output
    ledger = _ledger(tmp_spend_dir)
    row = _reservation_rows(tmp_spend_dir)[0]
    assert row["amount"] == 8.555680
    assert row["status"] == "unknown"
    assert row["tag"] == "discovery-experiment"
    assert [a["usage_cost"] for a in ledger["actuals"]] == [0.12, 0.05]
    assert all(a["reservation_id"] == row["reservation_id"] for a in ledger["actuals"])
    assert all(a["provenance"] == "estimated" for a in ledger["actuals"])
    assert (out / "blind-rating.md").exists()


def test_experiment_fusion_failure_records_partial_bill_then_closes_unknown(
    tmp_path, tmp_spend_dir, fake_api_key, monkeypatch
):
    async def fail_core(**kwargs):
        kwargs["record_fn"](amount=0.07, tool="discovery")
        raise FusionError("arm A blew up", cost=0.07)

    monkeypatch.setattr(experiment_cli, "run_panel_vs_single", fail_core)

    result = CliRunner().invoke(
        experiment_cli.main,
        ["--yes", "--tier", "standard", "--out", str(tmp_path / "experiment")],
    )

    assert result.exit_code != 0
    assert isinstance(result.exception, FusionError)
    ledger = _ledger(tmp_spend_dir)
    row = _reservation_rows(tmp_spend_dir)[0]
    assert row["status"] == "unknown"
    assert ledger["total"] == 8.555680
    assert ledger["actuals"][0]["usage_cost"] == 0.07
    assert ledger["actuals"][0]["provenance"] == "estimated"


@pytest.mark.parametrize("removed_option", ["--force", "--skip-budget-check"])
def test_experiment_cli_rejects_removed_budget_options(removed_option, monkeypatch):
    async def forbidden_core(**kwargs):
        raise AssertionError("removed options must be rejected before dispatch")

    monkeypatch.setattr(experiment_cli, "run_panel_vs_single", forbidden_core)
    result = CliRunner().invoke(experiment_cli.main, [removed_option, "--yes"])

    assert result.exit_code == 2
    assert "No such option" in result.output


def test_budget_spend_dir_is_a_public_reporting_accessor(tmp_spend_dir):
    assert budget.spend_dir() == tmp_spend_dir
