import pytest
from council.discovery.evidence import EvidenceRecord
from council.discovery.tiers import get_tier
from council.discovery.gather import gather_evidence


@pytest.mark.asyncio
async def test_gather_returns_bundle_and_status():
    async def s(topic): return [EvidenceRecord("sonar", "S", "https://a/1", "", "pain a")]
    async def w(topic): return [EvidenceRecord("web", "W", "https://a/1", "", "pain a"),   # dup
                                EvidenceRecord("web", "W", "https://b/2", "", "pain b")]
    async def l(topic): raise RuntimeError("last30 down")
    bundle, status = await gather_evidence(
        topic="x", tier=get_tier("quick"), api_key="k",
        collectors={"sonar": s, "web": w, "last30": l},
    )
    assert len(bundle.records) == 2                 # dup dropped, last30 failure tolerated
    assert bundle.has_url("https://b/2")
    assert status["sonar"].startswith("ok:")
    assert "1 records" in status["web"]             # 2 found, 1 net-new after dedup
    assert status["last30"].startswith("error: RuntimeError")
