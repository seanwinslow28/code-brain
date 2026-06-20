# council/discovery/gather/__init__.py
"""Stage 1 orchestrator: run tier-enabled collectors concurrently → deduped EvidenceBundle."""

import asyncio

from council.discovery.evidence import EvidenceBundle
from council.discovery.gather.last30 import collect_last30
from council.discovery.gather.sonar import collect_sonar
from council.discovery.gather.web import collect_web
from council.discovery.tiers import TierConfig


async def gather_evidence(*, topic: str, tier: TierConfig, api_key: str, collectors: dict | None = None) -> EvidenceBundle:
    if collectors is None:
        collectors = {
            "last30": (lambda t: collect_last30(t)) if tier.social else None,
            "sonar": (lambda t: collect_sonar(api_key=api_key, topic=t, model=tier.sonar_model)),
            "web": (lambda t: collect_web(topic=t)) if tier.web else None,
        }
    coros = [fn(topic) for fn in collectors.values() if fn is not None]
    results = await asyncio.gather(*coros, return_exceptions=True)
    bundle = EvidenceBundle()
    for r in results:
        if isinstance(r, Exception):
            continue
        for rec in r:
            bundle.add(rec)
    return bundle
