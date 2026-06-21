import pytest
from datetime import date
from council import budget
from council.discovery.tiers import get_tier
from council.discovery.gather import gather_evidence
from council.discovery.evidence import EvidenceRecord


@pytest.mark.asyncio
async def test_gather_collectors_record_no_spend(tmp_spend_dir):
    """Cost-integrity invariant: Stage-1 collectors are all FREE today, so a full gather run
    records ZERO discovery spend. If a future collector bills (Firecrawl/Apify), this stays
    green ONLY by threading the incurred cost into a typed gather failure + record_spend
    (see the gather/__init__.py invariant note) — never by a silent billable call."""
    async def fake(t):
        return [EvidenceRecord("review", "g2.com", "https://g2.com/1", "", "it crashes daily")]
    bundle, status = await gather_evidence(
        topic="x", tier=get_tier("deep"), api_key="k",
        collectors={"reviews": fake, "github": fake, "qa": fake},
    )
    assert len(bundle.records) >= 1
    assert budget.tool_total_for_day(date.today(), "discovery") == 0.0
