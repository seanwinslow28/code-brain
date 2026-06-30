# council/discovery/gather/__init__.py
"""Stage 1 orchestrator: run tier-enabled collectors concurrently → (deduped bundle, per-collector status).

COST-INTEGRITY CONTRACT: a collector returns EITHER `list[EvidenceRecord]` (FREE) OR a
`(records, billed_cost_usd)` tuple (PAID). Sonar is the one paid collector today — OpenRouter
reports its spend in `usage.cost`. The orchestrator accumulates every collector's billed cost onto
`bundle.gather_cost_usd`, which the pipeline folds into the run's recorded spend so the daily cap
isn't blind to it. If you add another paid collector (Firecrawl / Apify), return the `(records, cost)`
tuple — do NOT make a silent billable call that returns a bare list. See test_gather_cost_integrity.py
and test_gather_orchestrator.py.
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


async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str, segment: str = "",
                          collectors: dict | None = None) -> tuple[EvidenceBundle, dict]:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t, segment=segment)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model, segment=segment, fetch=_simple_fetch)),
            "web": (lambda t: collect_web(topic=t, segment=segment)) if tier.web else None,
            "reviews": (lambda t: collect_reviews(topic=t, segment=segment)) if tier.reviews else None,
            "github": (lambda t: collect_github(topic=t, segment=segment)) if tier.github else None,
            "qa": (lambda t: collect_qa(topic=t, segment=segment)) if tier.qa else None,
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
            records, cost = (r if isinstance(r, tuple) else (r, 0.0))   # PAID collector → (records, cost)
            bundle.gather_cost_usd = round(bundle.gather_cost_usd + cost, 6)
            added = sum(1 for rec in records if bundle.add(rec))
            status[name] = f"ok: {added} records ({len(records)} found)"
    return bundle, status
