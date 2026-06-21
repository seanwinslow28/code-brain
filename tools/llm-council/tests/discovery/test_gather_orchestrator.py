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


@pytest.mark.asyncio
async def test_default_collectors_respect_tier_flags(monkeypatch):
    seen = []

    def stub(name):
        async def fn(*a, **k):
            seen.append(name)
            return []
        return fn

    import council.discovery.gather as gmod
    monkeypatch.setattr(gmod, "collect_last30", stub("last30"))
    monkeypatch.setattr(gmod, "collect_sonar", stub("sonar"))
    monkeypatch.setattr(gmod, "collect_web", stub("web"))
    monkeypatch.setattr(gmod, "collect_reviews", stub("reviews"))
    monkeypatch.setattr(gmod, "collect_github", stub("github"))
    monkeypatch.setattr(gmod, "collect_qa", stub("qa"))

    await gmod.gather_evidence(topic="x", tier=get_tier("quick"), api_key="k")
    assert "reviews" not in seen and "github" not in seen and "qa" not in seen

    seen.clear()
    await gmod.gather_evidence(topic="x", tier=get_tier("standard"), api_key="k")
    assert "reviews" in seen and "github" in seen and "qa" not in seen

    seen.clear()
    await gmod.gather_evidence(topic="x", tier=get_tier("deep"), api_key="k")
    assert {"reviews", "github", "qa"} <= set(seen)
