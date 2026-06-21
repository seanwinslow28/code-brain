# council/discovery/gather/__init__.py
"""Stage 1 orchestrator: run tier-enabled collectors concurrently → (deduped bundle, per-collector status)."""

import asyncio
import sys

from council.discovery.evidence import EvidenceBundle
from council.discovery.gather.last30 import collect_last30
from council.discovery.gather.sonar import collect_sonar
from council.discovery.gather.web import collect_web
from council.discovery.tiers import TierConfig


async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str,
                          collectors: dict | None = None) -> tuple[EvidenceBundle, dict]:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model)),
            "web": (lambda t: collect_web(topic=t)) if tier.web else None,
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
