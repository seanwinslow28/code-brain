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


@pytest.mark.asyncio
async def test_pipeline_folds_gather_cost_into_spend():
    # Sonar's billed gather cost (carried on bundle.gather_cost_usd) must be added to the run's
    # recorded cost — otherwise the $10/day cap goes blind to ~$0.02/run of real Sonar spend.
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "exports fail silently", 9))
    bundle.gather_cost_usd = 0.0231

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], blind_spots=[], tokens_in=0, tokens_out=0, web_calls=0, cost=0.50)

    res = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False)
    assert res.cost_usd == pytest.approx(0.5231)   # fuse 0.50 + gather 0.0231


@pytest.mark.asyncio
async def test_pipeline_records_gather_cost_on_empty_bundle():
    # Sonar bills even when it yields no usable evidence; the empty-bundle path must still report it.
    empty = EvidenceBundle()
    empty.gather_cost_usd = 0.018

    async def gather_fn(**kw):
        return empty, {"sonar": "ok: 0 records (0 found)"}

    res = await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                              gather_fn=gather_fn, fuse_fn=None)
    assert res.cost_usd == pytest.approx(0.018)


@pytest.mark.asyncio
async def test_empty_bundle_session_carries_verify_and_citation_keys():
    # schema uniformity: the empty-bundle early-return session must carry the same
    # verify_mode / citation_* keys as the full path (substring-only, no metrics).
    async def gather_fn(**kw):
        return EvidenceBundle(), {"sonar": "ok: 0 records (0 found)"}
    res = await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                              gather_fn=gather_fn, fuse_fn=None)
    assert res.session["verify_mode"] == "substring-only"
    assert res.session["citation_precision"] is None
    assert res.session["citation_recall"] is None


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
    res = await run_discovery(topic="x", lens="pm", tier="quick", segment="developer",
                              api_key="k", gather_fn=gather_fn, fuse_fn=None)
    assert res.verified_count == 0
    assert "Low verifiable signal" in res.markdown or "No pain points survived" in res.markdown
    # the empty-bundle hero must honor the passed segment (not falsely tell you to add one)
    assert "Add `--segment" not in res.markdown


def test_normalize_segment_strips_operators_and_collapses_whitespace():
    from council.discovery.pipeline import _normalize_segment
    # --segment is a free-text audience qualifier, NOT a query operator: strip :/parens so it can't
    # alter provider query semantics (the github/reviews/sonar boundary), and collapse whitespace.
    assert _normalize_segment("is:pr (mobile)") == "is pr mobile"
    assert _normalize_segment("site:foo bar") == "site foo bar"
    assert _normalize_segment("  nonprofits  ") == "nonprofits"
    assert _normalize_segment("   ") == ""           # whitespace-only collapses to empty
    assert _normalize_segment("") == ""


@pytest.mark.asyncio
async def test_run_discovery_normalizes_segment_before_gather():
    captured = {}
    async def gather_fn(**kw):
        captured["segment"] = kw["segment"]
        return EvidenceBundle(), {"sonar": "ok: 0 records (0 found)"}
    await run_discovery(topic="crm", lens="pm", tier="quick", api_key="k",
                        segment="is:pr (nonprofits)", gather_fn=gather_fn, fuse_fn=None)
    assert captured["segment"] == "is pr nonprofits"


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
async def test_post_fuse_failure_records_billed_cost(tmp_path):
    # A failure AFTER fuse (verify/backfill/frame/render) must still surface the already-billed FUSE
    # cost as DiscoveryFailed.cost_usd, mirroring the FusionError path — otherwise __main__ records $0
    # and the daily cap goes blind to real spend (observed 2026-06-28 when BACKFILL crashed post-fuse).
    from council.discovery.pipeline import run_discovery, DiscoveryFailed
    import json as _json

    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports fail silently"))

    async def gather_fn(**kw):
        return b, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], blind_spots=["no SSO"], tokens_in=1000, tokens_out=300, cost=0.5)

    async def backfill_fn(**kw):
        raise RuntimeError("post-fuse blowup (e.g. Brave 422)")

    sdir = tmp_path / ".sessions"
    with pytest.raises(DiscoveryFailed) as exc:
        await run_discovery(topic="x", lens="substack", tier="standard", api_key="k",
                            gather_fn=gather_fn, fuse_fn=fuse_fn, backfill_fn=backfill_fn,
                            supplement=True, sessions_dir=sdir)
    assert exc.value.cost_usd == 0.5                  # FUSE was billed; spend survives the post-fuse crash
    written = list(sdir.glob("*.json"))
    assert len(written) == 1
    data = _json.loads(written[0].read_text())
    assert data["failed_stage"] == "post-fuse" and data["cost_usd"] == 0.5
    assert "gather_status" in data


@pytest.mark.asyncio
async def test_post_fuse_failure_still_raises_with_cost_when_session_write_fails(tmp_path):
    from council.discovery.pipeline import run_discovery, DiscoveryFailed
    b = EvidenceBundle(); b.add(EvidenceRecord("reddit", "r", "https://r.com/1", "", "exports fail silently"))

    async def gather_fn(**kw):
        return b, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], blind_spots=["x"], tokens_in=1000, tokens_out=300, cost=0.5)

    async def backfill_fn(**kw):
        raise RuntimeError("boom")

    # sessions_dir points at an existing FILE → diagnostic mkdir/write raises → spend must still survive.
    bad = tmp_path / "not-a-dir"; bad.write_text("x")
    with pytest.raises(DiscoveryFailed) as exc:
        await run_discovery(topic="x", lens="pm", tier="standard", api_key="k",
                            gather_fn=gather_fn, fuse_fn=fuse_fn, backfill_fn=backfill_fn,
                            supplement=True, sessions_dir=bad)
    assert exc.value.cost_usd == 0.5


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


@pytest.mark.asyncio
async def test_pipeline_dedups_near_duplicate_pain_points():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/a", "https://d1.com/a", "2026-06-18", "exports fail silently", 9))
    bundle.add(EvidenceRecord("reddit", "r/b", "https://d2.com/b", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 2 records (2 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Exports fail silently", "exports silently fail on conflict",
                               ["exports fail silently"], ["https://d1.com/a"], intensity=5),
            CandidatePainPoint("Silently failing exports", "on conflict exports fail silently",
                               ["exports fail silently"], ["https://d2.com/b"], intensity=4),
        ], blind_spots=["x"], tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert res.verified_count == 1                              # two near-dups collapsed to one
    assert res.session["merged_count"] == 1
    assert "Merged 1" in res.markdown                           # honest render note


@pytest.mark.asyncio
async def test_pipeline_same_domain_merge_does_not_inflate_corroboration():
    """Two same-domain URLs that merge into one pain point must report only 1 distinct domain,
    proving same-domain corroboration is NOT double-counted after a merge."""
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/a", "https://same.com/a", "2026-06-29", "exports fail silently", 9))
    bundle.add(EvidenceRecord("reddit", "r/b", "https://same.com/b", "2026-06-29", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 2 records (2 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Exports fail silently", "exports silently fail on conflict",
                               ["exports fail silently"], ["https://same.com/a"], intensity=5),
            CandidatePainPoint("Silently failing exports", "on conflict exports fail silently",
                               ["exports fail silently"], ["https://same.com/b"], intensity=4),
        ], blind_spots=["x"], tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    assert res.verified_count == 1                              # two near-dups collapsed to one
    assert res.session["merged_count"] == 1
    # same-domain merge must NOT double-count: only 1 distinct domain should be reported
    assert "1 independent domain(s)" in res.markdown


@pytest.mark.asyncio
async def test_pipeline_ranks_blind_spots_worst_first():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/a", "https://d1.com/a", "2026-06-18", "exports fail silently", 9))

    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}

    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Exports fail silently", "exports silently fail on conflict",
                               ["exports fail silently"], ["https://d1.com/a"], intensity=5),
        ], blind_spots=["nobody covers export conflict recovery",
                        "pricing transparency is unaddressed"],
           tokens_in=900, tokens_out=200, cost=0.3)

    res = await run_discovery(topic="sync apps", lens="pm", tier="standard",
                              api_key="k", gather_fn=gather_fn, fuse_fn=fuse_fn)
    md = res.markdown
    # the orthogonal gap (pricing) is ranked above the one close to the found pain (export recovery)
    assert md.index("pricing transparency is unaddressed") < md.index("nobody covers export conflict recovery")


@pytest.mark.asyncio
async def test_pipeline_records_verify_mode_substring_only_without_scorer(tmp_path):
    from tests.discovery.test_verify_entailment import FakeScorer  # noqa
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "", "exports fail silently", 9))
    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}
    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], blind_spots=[], tokens_in=10, tokens_out=5, cost=0.1)
    sdir = tmp_path / ".sessions"
    res = await run_discovery(topic="x", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                              sessions_dir=sdir, scorer=None)
    import json
    data = json.loads(next(sdir.glob("*.json")).read_text())
    assert data["verify_mode"] == "substring-only"
    assert data["citation_precision"] is None and data["citation_recall"] is None
    assert res.verified_count == 1


@pytest.mark.asyncio
async def test_pipeline_records_nli_mode_and_metrics_with_scorer(tmp_path):
    from tests.discovery.test_verify_entailment import FakeScorer
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "", "exports fail silently", 9))
    async def gather_fn(**kw):
        return bundle, {"sonar": "ok: 1 records (1 found)"}
    async def fuse_fn(**kw):
        return FusionResult(pain_points=[
            CandidatePainPoint("Export loss", "s", ["exports fail silently"], ["https://r.com/1"], intensity=5),
        ], blind_spots=[], tokens_in=10, tokens_out=5, cost=0.1)
    sdir = tmp_path / ".sessions"
    await run_discovery(topic="x", lens="pm", tier="standard", api_key="k",
                        gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                        sessions_dir=sdir, scorer=FakeScorer(prob=0.9))
    import json
    data = json.loads(next(sdir.glob("*.json")).read_text())
    assert data["verify_mode"] == "nli"
    assert data["citation_recall"] == 1.0


from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.velocity import VelocitySignal


class _FakeVProvider:
    def measure_batch(self, terms):
        # rising signal for every term
        return {t: VelocitySignal(term=t, slope=0.8, normalized=0.9, source="pytrends",
                                  window_days=90, points=5) for t in terms}


def _one_point_bundle_and_fuse():
    url = "https://ex.com/a"
    async def gather_fn(**kw):
        b = EvidenceBundle()
        b.add(EvidenceRecord("reddit", "r/pm", url, "2026-06-20", "slow export", engagement=100))
        return b, {"ok": True}
    async def fuse_fn(**kw):
        pt = CandidatePainPoint("Slow export", "it's slow", quotes=["slow export"], urls=[url],
                                intensity=4, recency="2026-06", consensus="4/4 models")
        return FusionResult(pain_points=[pt])
    return gather_fn, fuse_fn


@pytest.mark.asyncio
async def test_velocity_off_by_default_in_session():
    gather_fn, fuse_fn = _one_point_bundle_and_fuse()
    res = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                              velocity_provider=None)
    assert res.session["velocity_mode"] == "off"
    assert res.session["why_now_coverage"] == 0.0


@pytest.mark.asyncio
async def test_velocity_provider_threads_and_reports_coverage():
    gather_fn, fuse_fn = _one_point_bundle_and_fuse()
    res = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=gather_fn, fuse_fn=fuse_fn, supplement=False,
                              velocity_provider=_FakeVProvider())
    assert res.session["velocity_mode"] == "pytrends"
    assert res.session["why_now_coverage"] == 1.0                 # the one card carries a signal


@pytest.mark.asyncio
async def test_empty_bundle_session_carries_velocity_keys():
    async def gather_fn(**kw):
        return EvidenceBundle(), {"ok": True}
    res = await run_discovery(topic="x", lens="pm", tier="quick", api_key="k",
                              gather_fn=gather_fn, fuse_fn=None)
    assert res.session["velocity_mode"] == "off"
    assert res.session["why_now_coverage"] == 0.0


@pytest.mark.asyncio
async def test_invariant_velocity_cannot_perturb_the_gate(monkeypatch):
    # THE MOAT: verified set + citation metrics identical velocity ON (non-zero weight) vs off,
    # and no velocity string leaks into evidence urls/quotes.
    # Velocity now actively re-ranks scores; the gate must remain byte-identical anyway.
    monkeypatch.setattr("council.discovery.scoring.VELOCITY_WEIGHT", 0.3)
    g1, f1 = _one_point_bundle_and_fuse()
    off = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=g1, fuse_fn=f1, supplement=False, velocity_provider=None)
    g2, f2 = _one_point_bundle_and_fuse()
    on = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                             gather_fn=g2, fuse_fn=f2, supplement=False,
                             velocity_provider=_FakeVProvider())
    assert off.session["verified"] == on.session["verified"]
    assert off.session["dropped"] == on.session["dropped"]
    assert off.session["citation_precision"] == on.session["citation_precision"]
    assert off.session["citation_recall"] == on.session["citation_recall"]
    # velocity genuinely did something under the non-zero weight: the on-run's markdown leads
    # with a velocity line in _why_now, while the off-run shows only the recency note.
    assert on.markdown != off.markdown
