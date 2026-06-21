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
        return bundle, {"sonar": "ok: 1 records (1 found)"}

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


def test_estimate_cost_prefers_usage_cost():
    from council.discovery.pipeline import _estimate_cost
    from council.discovery.fusion import FusionResult
    from council.discovery.tiers import get_tier
    fr = FusionResult(tokens_in=1000, tokens_out=300, web_calls=4, cost=0.88)
    assert _estimate_cost(fr, get_tier("standard")) == 0.88
    fr0 = FusionResult(tokens_in=1000, tokens_out=300, web_calls=4, cost=0.0)
    assert _estimate_cost(fr0, get_tier("standard")) > 0      # falls back to token estimate


@pytest.mark.asyncio
async def test_empty_bundle_renders_low_signal():
    async def gather_fn(**kw):
        return EvidenceBundle(), {"sonar": "ok: 0 records (0 found)"}
    res = await run_discovery(topic="x", lens="pm", tier="quick",
                              api_key="k", gather_fn=gather_fn, fuse_fn=None)
    assert res.verified_count == 0
    assert "Low verifiable signal" in res.markdown or "No pain points survived" in res.markdown


@pytest.mark.asyncio
async def test_fuse_failure_persists_session_and_raises_discoveryfailed(tmp_path):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.fusion import FusionError
    from council.discovery.pipeline import run_discovery, DiscoveryFailed
    import json as _json

    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))

    async def gather_fn(**kw):
        return b, {"sonar": "ok: 1 records (1 found)", "web": "error: RuntimeError: boom"}

    async def fuse_fn(**kw):
        raise FusionError("unparseable after retry", cost=0.42)

    sdir = tmp_path / ".sessions"
    with pytest.raises(DiscoveryFailed) as exc:
        await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                            gather_fn=gather_fn, fuse_fn=fuse_fn, sessions_dir=sdir)
    assert exc.value.cost_usd == 0.42
    assert exc.value.session["gather_status"]["sonar"].startswith("ok:")
    written = list(sdir.glob("*.json"))
    assert len(written) == 1
    data = _json.loads(written[0].read_text())
    assert data["failed_stage"] == "fuse" and data["cost_usd"] == 0.42
    assert "gather_status" in data


@pytest.mark.asyncio
async def test_fuse_failure_still_raises_with_cost_when_session_write_fails(tmp_path):
    from council.discovery.evidence import EvidenceBundle, EvidenceRecord
    from council.discovery.fusion import FusionError
    from council.discovery.pipeline import run_discovery, DiscoveryFailed
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "q"))
    async def gather_fn(**kw):
        return b, {"sonar": "ok: 1 records (1 found)"}
    async def fuse_fn(**kw):
        raise FusionError("boom", cost=0.42)
    # sessions_dir points at an existing FILE → mkdir raises → spend must still survive.
    bad = tmp_path / "not-a-dir"
    bad.write_text("x")
    with pytest.raises(DiscoveryFailed) as exc:
        await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                            gather_fn=gather_fn, fuse_fn=fuse_fn, sessions_dir=bad)
    assert exc.value.cost_usd == 0.42


@pytest.mark.asyncio
async def test_substack_lens_produces_angles_ledger_and_brief():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/x", "https://r.com/1", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "notes vanish on conflict", ["exports fail silently"],
                               ["https://r.com/1"], intensity=5, segment="power users"),
        ], blind_spots=["nobody covers recovery UX"], tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="substack", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert "Substack Idea Ledger" in res.markdown
    assert "Export loss" in res.markdown
    assert res.verified_count == 1
    assert res.brief_markdown                                   # the brief is produced
    assert "Itch" in res.brief_markdown
    assert "exports fail silently" in res.brief_markdown        # verbatim evidence carried into the brief


@pytest.mark.asyncio
async def test_run_discovery_passes_segment_to_gather():
    seen = {}
    async def gather_fn(**kw):
        seen.update(kw)
        return EvidenceBundle(), {"sonar": "ok: 0 records (0 found)"}
    await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                        segment="developers", gather_fn=gather_fn)
    assert seen["segment"] == "developers"


@pytest.mark.asyncio
async def test_pm_lens_produces_no_brief():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/x", "https://r.com/1", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert "Idea Ledger — sync apps" in res.markdown
    assert res.brief_markdown == ""
