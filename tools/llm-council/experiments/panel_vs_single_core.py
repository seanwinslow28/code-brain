"""Experiment core: gather one bundle, fuse it through the full panel vs a single model."""

from dataclasses import replace

from council.budget import record_spend as _record_spend
from council.discovery.fusion import FusionError, fuse as _fuse
from council.discovery.gather import gather_evidence
from council.discovery.tiers import get_tier


async def run_panel_vs_single(*, topic, tier_name, single_model, api_key, on_date,
                              gather_fn=None, fuse_fn=None, record_fn=None) -> dict:
    tcfg = get_tier(tier_name)
    single_cfg = replace(tcfg, panel=(single_model,))
    gather = gather_fn or gather_evidence
    fuse = fuse_fn or _fuse
    record = record_fn or _record_spend

    def _bill(fr_cost: float) -> None:
        record(amount=round(fr_cost or 0.0, 6), profile=tier_name,
               tag="discovery-experiment", on_date=on_date, tool="discovery")

    bundle, gather_status = await gather(topic=topic, tier=tcfg, api_key=api_key)

    try:
        fr_a = await fuse(api_key=api_key, bundle=bundle, tier=tcfg, topic=topic)
    except FusionError as e:
        _bill(getattr(e, "cost", 0.0) or 0.0)   # record arm-A partial spend before surfacing
        raise
    _bill(fr_a.cost)

    try:
        fr_b = await fuse(api_key=api_key, bundle=bundle, tier=single_cfg, topic=topic)
    except FusionError as e:
        _bill(getattr(e, "cost", 0.0) or 0.0)   # record the failed arm's real spend before surfacing
        raise
    _bill(fr_b.cost)

    return {"bundle": bundle, "gather_status": gather_status,
            "arm_a": fr_a, "arm_b": fr_b, "cost": round((fr_a.cost or 0.0) + (fr_b.cost or 0.0), 6)}
