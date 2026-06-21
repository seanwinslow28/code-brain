# council/discovery/pipeline.py
"""4-stage orchestrator: gather → fuse → verify → frame → render."""

import json
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from council.discovery.fusion import FusionResult, FusionError, fuse as _fuse
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
    brief_markdown: str = ""


class DiscoveryFailed(Exception):
    def __init__(self, message: str, *, cost_usd: float = 0.0, session: dict | None = None):
        super().__init__(message)
        self.cost_usd = cost_usd
        self.session = session or {}


def _estimate_cost(fr: FusionResult, tier) -> float:
    if getattr(fr, "cost", 0.0):
        return round(fr.cost, 4)                  # authoritative OpenRouter usage.cost
    tok = (fr.tokens_in / 1000.0) * DISCOVERY_PRICE_IN_PER_1K + (fr.tokens_out / 1000.0) * DISCOVERY_PRICE_OUT_PER_1K
    web = len(tier.panel) * tier.max_tool_calls * WEB_QUERY_PRICE
    return round(tok + web, 4)


async def run_discovery(*, topic: str, lens: str, tier: str, api_key: str, segment: str = "",
                        gather_fn=None, fuse_fn=None, sessions_dir: Path | None = None) -> DiscoveryResult:
    tcfg = get_tier(tier)
    session_id = f"{time.strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

    gather = gather_fn or gather_evidence
    bundle, gather_status = await gather(topic=topic, tier=tcfg, api_key=api_key)

    if not bundle.records:
        md = render_ledger(topic=topic, lens=lens, tier=tier, cards=[], quote_bank=[],
                           fusion_result=FusionResult(), cost_usd=0.0, dropped_count=0)
        return DiscoveryResult(markdown=md, cost_usd=0.0, verified_count=0, dropped_count=0,
                               session={"id": session_id, "topic": topic, "empty": True,
                                        "gather_status": gather_status})

    fuse = fuse_fn or _fuse
    try:
        fr = await fuse(api_key=api_key, bundle=bundle, tier=tcfg, topic=topic)
    except FusionError as e:
        cost = round(getattr(e, "cost", 0.0) or 0.0, 4)
        fail_session = {
            "id": session_id, "topic": topic, "lens": lens, "tier": tier,
            "evidence_count": len(bundle.records), "gather_status": gather_status,
            "failed_stage": "fuse", "error": str(e), "cost_usd": cost,
        }
        if sessions_dir is not None:
            try:
                sessions_dir.mkdir(parents=True, exist_ok=True)
                (sessions_dir / f"{session_id}.json").write_text(json.dumps(fail_session, indent=2))
            except Exception as write_err:  # never let a failed diagnostic write eat the spend record
                print(f"[discovery] failed to persist failure session {session_id}: {write_err}", file=sys.stderr)
        raise DiscoveryFailed(str(e), cost_usd=cost, session=fail_session) from e

    verified = verify_pain_points(fr.pain_points, bundle)
    dropped = sum(1 for v in verified if not v.verified)
    cost = _estimate_cost(fr, tcfg)

    brief_md = ""
    if lens == "substack":
        from council.discovery.frame_substack import frame_substack
        from council.discovery.render_substack import render_substack_ledger, render_substack_brief
        angles, quote_bank = frame_substack(verified, fr, segment=segment)
        md = render_substack_ledger(topic=topic, tier=tier, angles=angles, quote_bank=quote_bank,
                                    fusion_result=fr, cost_usd=cost, dropped_count=dropped)
        brief_md = render_substack_brief(topic=topic, segment=segment, angles=angles)
        verified_count = len(angles)
    else:
        cards, quote_bank = frame_pm(verified, fr)
        md = render_ledger(topic=topic, lens=lens, tier=tier, cards=cards, quote_bank=quote_bank,
                           fusion_result=fr, cost_usd=cost, dropped_count=dropped)
        verified_count = len(cards)

    session = {
        "id": session_id, "topic": topic, "lens": lens, "tier": tier,
        "evidence_count": len(bundle.records), "verified": verified_count,
        "dropped": dropped, "cost_usd": cost,
        "gather_status": gather_status,
        "blind_spots": fr.blind_spots, "contradictions": fr.contradictions,
    }
    if sessions_dir is not None:
        sessions_dir.mkdir(parents=True, exist_ok=True)
        (sessions_dir / f"{session_id}.json").write_text(json.dumps(session, indent=2))

    return DiscoveryResult(markdown=md, cost_usd=cost, verified_count=verified_count,
                           dropped_count=dropped, session=session, brief_markdown=brief_md)
