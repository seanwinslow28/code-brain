import asyncio
from datetime import date

import pytest

from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import FusionResult, FusionError, CandidatePainPoint
from experiments.panel_vs_single_core import run_panel_vs_single


def _bundle():
    b = EvidenceBundle()
    b.add(EvidenceRecord(source_type="web", source_name="X", url="https://e.com/a", date="", quote="q"))
    return b


def test_both_arms_fuse_same_bundle_with_different_panels():
    bundle = _bundle()
    seen = []

    async def fake_gather(*, topic, tier, api_key, segment=""):
        return bundle, {"web": "ok: 1 records (1 found)"}

    async def fake_fuse(*, api_key, bundle, tier, topic):
        seen.append((id(bundle), tuple(tier.panel)))
        return FusionResult(pain_points=[CandidatePainPoint(title="t", summary="s", quotes=[], urls=[])], cost=0.1)

    records = []
    res = asyncio.run(run_panel_vs_single(
        topic="t", tier_name="standard", single_model="anthropic/claude-opus-4.7",
        api_key="k", on_date=date(2026, 6, 30),
        gather_fn=fake_gather, fuse_fn=fake_fuse,
        record_fn=lambda **kw: records.append(kw),
    ))
    # same bundle object both times; arm A panel has 4 models, arm B exactly 1
    assert seen[0][0] == seen[1][0]
    assert len(seen[0][1]) == 4
    assert seen[1][1] == ("anthropic/claude-opus-4.7",)
    # spend recorded once per arm, tagged discovery
    assert len(records) == 2
    assert all(r["tool"] == "discovery" and r["tag"] == "discovery-experiment" for r in records)
    assert res["arm_a"].cost == 0.1 and res["arm_b"].cost == 0.1
    assert res["cost"] == pytest.approx(0.2)


def test_arm_b_failure_still_records_arm_a_and_arm_b_cost():
    bundle = _bundle()
    calls = {"n": 0}

    async def fake_gather(*, topic, tier, api_key, segment=""):
        return bundle, {}

    async def fake_fuse(*, api_key, bundle, tier, topic):
        calls["n"] += 1
        if calls["n"] == 1:
            return FusionResult(cost=0.1)
        raise FusionError("arm B blew up", cost=0.05)

    records = []
    with pytest.raises(FusionError):
        asyncio.run(run_panel_vs_single(
            topic="t", tier_name="standard", single_model="anthropic/claude-opus-4.7",
            api_key="k", on_date=date(2026, 6, 30),
            gather_fn=fake_gather, fuse_fn=fake_fuse,
            record_fn=lambda **kw: records.append(kw),
        ))
    # both the successful arm-A cost and the failed arm-B cost are recorded
    assert [r["amount"] for r in records] == [0.1, 0.05]
