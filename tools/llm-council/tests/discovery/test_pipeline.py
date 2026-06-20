# tests/discovery/test_pipeline.py
import pytest
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.pipeline import run_discovery


@pytest.mark.asyncio
async def test_pipeline_end_to_end_drops_unverified():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
            CandidatePainPoint("Fabricated", "s", ["never said this"], ["https://fake.com/x"], intensity=4),
        ], blind_spots=["no SSO"], tokens_in=1000, tokens_out=300, web_calls=4)

    res = await run_discovery(topic="pm tools", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert res.verified_count == 1
    assert res.dropped_count == 1
    assert "Export loss" in res.markdown
    assert "Fabricated" not in res.markdown
    assert res.cost_usd > 0


@pytest.mark.asyncio
async def test_empty_bundle_renders_low_signal():
    async def gather_fn(**kw):
        return EvidenceBundle()
    res = await run_discovery(topic="x", lens="pm", tier="quick",
                              api_key="k", gather_fn=gather_fn, fuse_fn=None)
    assert res.verified_count == 0
    assert "Low verifiable signal" in res.markdown or "No pain points survived" in res.markdown
