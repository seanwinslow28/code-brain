import pytest
from datetime import date
from council import budget
from council.discovery.tiers import get_tier
from council.discovery.gather import gather_evidence
from council.discovery.evidence import EvidenceRecord


@pytest.mark.asyncio
async def test_gather_collectors_record_no_spend(tmp_spend_dir):
    """Cost-integrity invariant: gather() itself NEVER calls record_spend — a billing collector
    (Sonar today) surfaces its cost via the (records, cost) tuple, which the orchestrator puts on
    bundle.gather_cost_usd and the PIPELINE folds into recorded spend. So a gather() call in
    isolation (these free list-returning fakes) records ZERO discovery spend. A future paid
    collector must return the (records, cost) tuple too — never make a silent billable call.
    See gather/__init__.py and test_gather_orchestrator.py for the cost-threading path."""
    async def fake(t):
        return [EvidenceRecord("review", "g2.com", "https://g2.com/1", "", "it crashes daily")]
    bundle, status = await gather_evidence(
        topic="x", tier=get_tier("deep"), api_key="k",
        collectors={"reviews": fake, "github": fake, "qa": fake},
    )
    assert len(bundle.records) >= 1
    assert budget.tool_total_for_day(date.today(), "discovery") == 0.0
