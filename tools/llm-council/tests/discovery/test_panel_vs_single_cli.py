# tests/discovery/test_panel_vs_single_cli.py
import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from council.budget import BudgetExceeded
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import FusionResult, CandidatePainPoint
from experiments.panel_vs_single import _write_artifacts, main


def _result():
    b = EvidenceBundle()
    b.add(EvidenceRecord(source_type="web", source_name="X", url="https://e.com/a", date="", quote="q"))
    fa = FusionResult(pain_points=[CandidatePainPoint(title="Alpha", summary="s", quotes=["qa"], urls=["https://e.com/a"])],
                      blind_spots=["bs"], contradictions=[], cost=0.12)
    fb = FusionResult(pain_points=[CandidatePainPoint(title="Beta", summary="s", quotes=["qb"], urls=["https://e.com/b"])],
                      cost=0.05)
    return {"bundle": b, "gather_status": {"web": "ok"}, "arm_a": fa, "arm_b": fb, "cost": 0.17}


def test_write_artifacts_emits_all_files_and_blind_key(tmp_path):
    paths = _write_artifacts(tmp_path, _result(), topic="t")
    for name in ("bundle.json", "arm-A.json", "arm-B.json", "blind-rating.md", "key.json"):
        assert (tmp_path / name).exists(), name
    # bundle round-trips
    bundle_d = json.loads((tmp_path / "bundle.json").read_text())
    assert EvidenceBundle.from_dict(bundle_d).has_url("https://e.com/a")
    # key maps both sets to distinct arms; blind md never names the arms
    key = json.loads((tmp_path / "key.json").read_text())
    assert set(key.values()) == {"A", "B"}
    md = (tmp_path / "blind-rating.md").read_text()
    assert "Alpha" in md and "Beta" in md
    assert "arm-A" not in md.lower() and "panel" not in md.lower()
    # arm json carries the real (unblinded) identity for the writeup
    arm_a = json.loads((tmp_path / "arm-A.json").read_text())
    assert arm_a["pain_points"][0]["title"] == "Alpha"
    assert arm_a["cost"] == 0.12


# ---------------------------------------------------------------------------
# CLI guardrail tests (hermetic — no real network, no real spend)
# ---------------------------------------------------------------------------

def test_cli_preflight_rejection_exits_2(monkeypatch):
    """When preflight_tool raises BudgetExceeded the CLI must exit with code 2."""
    monkeypatch.setattr(
        "experiments.panel_vs_single.preflight_tool",
        lambda **kw: (_ for _ in ()).throw(BudgetExceeded("nope")),
    )
    res = CliRunner().invoke(main, ["--yes"])
    assert res.exit_code == 2, res.output


def test_cli_decline_exits_1():
    """With --skip-budget-check and the user answering 'n', exit code must be 1."""
    res = CliRunner().invoke(main, ["--skip-budget-check"], input="n\n")
    assert res.exit_code == 1, res.output


def test_cli_happy_path_writes_artifacts(tmp_path, monkeypatch):
    """With --yes --skip-budget-check the CLI writes blind-rating.md and key.json."""
    b = EvidenceBundle()
    b.add(EvidenceRecord(source_type="web", source_name="X",
                         url="https://e.com/a", date="", quote="q"))
    fr_a = FusionResult(
        pain_points=[CandidatePainPoint(title="Alpha pain", summary="s",
                                        quotes=["q"], urls=["https://e.com/x"])],
        cost=0.05,
    )
    fr_b = FusionResult(
        pain_points=[CandidatePainPoint(title="Beta pain", summary="s",
                                        quotes=["q"], urls=["https://e.com/x"])],
        cost=0.05,
    )

    async def fake_core(*, topic, tier_name, single_model, api_key, on_date, **kw):
        return {"bundle": b, "gather_status": {"web": "ok: 1 records"},
                "arm_a": fr_a, "arm_b": fr_b, "cost": 0.10}

    monkeypatch.setattr("experiments.panel_vs_single.run_panel_vs_single", fake_core)

    out_dir = tmp_path / "run-out"
    res = CliRunner().invoke(main, [
        "--yes", "--skip-budget-check", "--out", str(out_dir),
    ])
    assert res.exit_code == 0, res.output
    assert (out_dir / "blind-rating.md").exists()
    key = json.loads((out_dir / "key.json").read_text())
    assert set(key.keys()) == {"Set 1", "Set 2"}
    assert set(key.values()) == {"A", "B"}
