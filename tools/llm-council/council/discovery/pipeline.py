# council/discovery/pipeline.py
"""4-stage orchestrator: gather → fuse → verify → frame → render."""

import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from council.discovery.fusion import FusionResult, fuse as _fuse
from council.discovery.frame import frame_pm
from council.discovery.gather import gather_evidence
from council.discovery.render import render_ledger
from council.discovery.tiers import get_tier
from council.discovery.verify import verify_pain_points

# Per-1k-token blended prices (USD) and per-web-query price for cost estimation.
DISCOVERY_PRICE_IN_PER_1K = 0.003
DISCOVERY_PRICE_OUT_PER_1K = 0.015
WEB_QUERY_PRICE = 0.012


@dataclass
class DiscoveryResult:
    markdown: str
    cost_usd: float
    verified_count: int
    dropped_count: int
    session: dict


def _estimate_cost(fr: FusionResult, tier) -> float:
    tok = (fr.tokens_in / 1000.0) * DISCOVERY_PRICE_IN_PER_1K + (fr.tokens_out / 1000.0) * DISCOVERY_PRICE_OUT_PER_1K
    web = len(tier.panel) * tier.max_tool_calls * WEB_QUERY_PRICE
    return round(tok + web, 4)


async def run_discovery(*, topic: str, lens: str, tier: str, api_key: str,
                        gather_fn=None, fuse_fn=None, sessions_dir: Path | None = None) -> DiscoveryResult:
    tcfg = get_tier(tier)
    session_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    gather = gather_fn or gather_evidence
    bundle = await gather(topic=topic, tier=tcfg, api_key=api_key)

    if not bundle.records:
        md = render_ledger(topic=topic, lens=lens, tier=tier, cards=[], quote_bank=[],
                           fusion_result=FusionResult(), cost_usd=0.0, dropped_count=0)
        return DiscoveryResult(markdown=md, cost_usd=0.0, verified_count=0, dropped_count=0,
                               session={"id": session_id, "topic": topic, "empty": True})

    fuse = fuse_fn or _fuse
    fr = await fuse(api_key=api_key, bundle=bundle, tier=tcfg, topic=topic)

    verified = verify_pain_points(fr.pain_points, bundle)
    dropped = sum(1 for v in verified if not v.verified)
    cards, quote_bank = frame_pm(verified, fr)
    cost = _estimate_cost(fr, tcfg)

    md = render_ledger(topic=topic, lens=lens, tier=tier, cards=cards, quote_bank=quote_bank,
                       fusion_result=fr, cost_usd=cost, dropped_count=dropped)

    session = {
        "id": session_id, "topic": topic, "lens": lens, "tier": tier,
        "evidence_count": len(bundle.records), "verified": len(cards),
        "dropped": dropped, "cost_usd": cost,
        "blind_spots": fr.blind_spots, "contradictions": fr.contradictions,
    }
    if sessions_dir is not None:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / f"{session_id}.json").write_text(json.dumps(session, indent=2))

    return DiscoveryResult(markdown=md, cost_usd=cost, verified_count=len(cards),
                           dropped_count=dropped, session=session)
