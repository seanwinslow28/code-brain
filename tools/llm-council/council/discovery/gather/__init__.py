# council/discovery/gather/__init__.py
"""Stage 1 orchestrator: run tier-enabled collectors concurrently → (deduped bundle, per-collector status).

COST-INTEGRITY INVARIANT: every collector below is FREE (no billable provider call). The CLI's
generic pre-fuse `except` therefore records $0 correctly. If you add a paid collector (e.g. Firecrawl
/ Apify), you MUST thread its incurred cost into a typed gather failure and record_spend it in that
`except` — mirror FusionError.cost → DiscoveryFailed.cost_usd — or a gather-stage failure will
silently record $0 (cost-integrity leak). See test_gather_cost_integrity.py.
"""

import asyncio
import sys

from council.discovery.evidence import EvidenceBundle
from council.discovery.gather.github import collect_github
from council.discovery.gather.last30 import collect_last30
from council.discovery.gather.qa import collect_qa
from council.discovery.gather.reviews import collect_reviews
from council.discovery.gather.sonar import collect_sonar
from council.discovery.gather.web import collect_web, _simple_fetch
from council.discovery.tiers import TierConfig


async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str,
                          collectors: dict | None = None) -> tuple[EvidenceBundle, dict]:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model, fetch=_simple_fetch)),
            "web": (lambda t: collect_web(topic=t)) if tier.web else None,
            "reviews": (lambda t: collect_reviews(topic=t)) if tier.reviews else None,
            "github": (lambda t: collect_github(topic=t)) if tier.github else None,
            "qa": (lambda t: collect_qa(topic=t)) if tier.qa else None,
        }
    active = {name: fn for name, fn in collectors.items() if fn is not None}
    results = await asyncio.gather(*(fn(topic) for fn in active.values()), return_exceptions=True)
    bundle = EvidenceBundle()
    status: dict[str, str] = {}
    for name, r in zip(active.keys(), results):
        if isinstance(r, Exception):
            status[name] = f"error: {type(r).__name__}: {r!r}"
            print(f"[gather] collector {name!r} failed: {type(r).__name__}: {r}", file=sys.stderr)
        else:
            added = sum(1 for rec in r if bundle.add(rec))
            status[name] = f"ok: {added} records ({len(r)} found)"
    return bundle, status
