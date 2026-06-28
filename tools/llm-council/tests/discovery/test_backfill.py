# tests/discovery/test_backfill.py
"""Stage 5 — BACKFILL (web-supplement gap-fill). Credential-free: inject search=/fetch=."""

import pytest

from council.discovery.backfill import (
    BackfillItem,
    BackfillResult,
    _supplement_query,
    run_backfill,
)
from council.discovery.evidence import EvidenceBundle, EvidenceRecord
from council.discovery.fusion import CandidatePainPoint, FusionResult
from council.discovery.pipeline import WEB_QUERY_PRICE, run_discovery
from council.discovery.tiers import get_tier
from council.discovery.verify import quote_supported_at_url

_CMP_TEXT = ("A detailed comparison of coding assistants shows Copilot leads on speed. "
             "Independent benchmarks ranked several coding assistants by accuracy.")


# --- query derivation -------------------------------------------------------

def test_supplement_query_strips_meta_prefix_and_targets_solution():
    q = _supplement_query("No evidence that references or fine-tuning solve it",
                          topic="ai writing", segment="creators").lower()
    assert "ai writing" in q
    assert "references" in q and "fine-tuning" in q
    assert "2026" in q
    assert not q.startswith("no evidence")             # meta-prefix stripped
    assert "user complaints" not in q                  # solution-side, NOT the complaint query


def test_supplement_query_handles_bare_no_and_little():
    assert not _supplement_query("Little data on latency", "x", "").lower().startswith("little")
    assert not _supplement_query("No tool head-to-head", "x", "").lower().startswith("no ")


# --- the shared verification gate (forward-compat E1 chokepoint) -------------

def test_quote_supported_at_url_gate():
    assert quote_supported_at_url(cited_quote="exports fail silently",
                                  fetched_text="teams say exports fail silently weekly") is True
    # uncited / fabricated claim absent from the page → dropped
    assert quote_supported_at_url(cited_quote="totally invented claim",
                                  fetched_text="teams say exports fail silently weekly") is False
    # embedding attack: a long fabricated quote that merely embeds a real short one must NOT pass
    assert quote_supported_at_url(cited_quote="exports fail silently because the vendor sells your data",
                                  fetched_text="exports fail silently") is False


# --- run_backfill -----------------------------------------------------------

@pytest.mark.asyncio
async def test_run_backfill_emits_url_anchored_verbatim_findings():
    async def search(q):
        return [{"title": "Cmp", "url": "https://blog.com/cmp", "published": "2026-05-01", "_text": _CMP_TEXT}]
    res = await run_backfill(blind_spots=["No head-to-head comparison of coding assistants"],
                             bundle=EvidenceBundle(), topic="coding assistants", segment="",
                             tier=get_tier("standard"), search=search, fetch=None)
    assert res.skipped is False
    assert len(res.items) == 1
    item = res.items[0]
    assert item.status == "filled"
    assert item.findings
    for f in item.findings:
        assert f.url == "https://blog.com/cmp"
        assert f.source_type == "web-supplement"
        assert f.quote in _CMP_TEXT                    # verbatim, present at the URL


@pytest.mark.asyncio
async def test_unfillable_gap_renders_still_open():
    async def search(q):
        return [{"title": "X", "url": "https://x.com/1", "published": "",
                 "_text": "An unrelated cooking recipe about onions, garlic and slow roasting."}]
    res = await run_backfill(blind_spots=["No quantitative latency data"], bundle=EvidenceBundle(),
                             topic="animation tooling", segment="", tier=get_tier("quick"),
                             search=search, fetch=None)
    assert res.items[0].status == "still open"
    assert res.items[0].findings == []
    assert res.queries_run == 1


@pytest.mark.asyncio
async def test_no_web_key_skips_without_crash():
    # autouse fixture deletes EXA/BRAVE keys; no injected search → graceful skip
    res = await run_backfill(blind_spots=["No tool head-to-head"], bundle=EvidenceBundle(),
                             topic="x", segment="", tier=get_tier("standard"))
    assert res.skipped is True
    assert "no web-search key" in res.skip_reason.lower()
    assert res.queries_run == 0
    assert res.items == []


@pytest.mark.asyncio
async def test_tier_scaling_caps_blind_spots():
    blinds = [f"No evidence on aspect {i}" for i in range(8)]
    async def search(q):
        return []
    quick = await run_backfill(blind_spots=blinds, bundle=EvidenceBundle(), topic="t", segment="",
                               tier=get_tier("quick"), search=search, fetch=None)
    deep = await run_backfill(blind_spots=blinds, bundle=EvidenceBundle(), topic="t", segment="",
                              tier=get_tier("deep"), search=search, fetch=None)
    assert len(quick.items) == 2 and quick.queries_run == 2
    assert len(deep.items) == 6 and deep.queries_run == 6
    assert len(deep.items) > len(quick.items)


@pytest.mark.asyncio
async def test_empty_blind_spots_runs_no_queries():
    async def search(q):
        return []
    res = await run_backfill(blind_spots=[], bundle=EvidenceBundle(), topic="t", segment="",
                             tier=get_tier("standard"), search=search, fetch=None)
    assert res.skipped is False
    assert res.items == []
    assert res.queries_run == 0


@pytest.mark.asyncio
async def test_dedup_against_existing_bundle_url():
    bundle = EvidenceBundle()
    bundle.add(EvidenceRecord("web", "src", "https://blog.com/cmp", "", "pre-existing quote"))
    async def search(q):
        return [{"title": "Cmp", "url": "https://blog.com/cmp", "published": "", "_text": _CMP_TEXT}]
    res = await run_backfill(blind_spots=["No comparison of coding assistants"], bundle=bundle,
                             topic="coding assistants", segment="", tier=get_tier("standard"),
                             search=search, fetch=None)
    # URL already in the main bundle → not re-surfaced
    assert res.items[0].findings == []
    assert res.items[0].status == "still open"


# --- pipeline integration (cost fold + section, both lenses) -----------------

def _bundle_with_pain():
    b = EvidenceBundle()
    b.add(EvidenceRecord("reddit", "r/pm", "https://r.com/1", "2026-06-18", "exports fail silently", 9))
    return b


async def _gather_fn(**kw):
    return _bundle_with_pain(), {"sonar": "ok: 1 records (1 found)"}


async def _fuse_fn(**kw):
    return FusionResult(
        pain_points=[CandidatePainPoint("Export loss", "s", ["exports fail silently"],
                                        ["https://r.com/1"], intensity=5)],
        blind_spots=["No tool head-to-head"], tokens_in=1000, tokens_out=300, web_calls=4)


def _stub_backfill(queries_run=2):
    async def backfill_fn(**kw):
        return BackfillResult(
            skipped=False, skip_reason="", queries_run=queries_run,
            items=[BackfillItem(gap="No tool head-to-head", query="x head-to-head 2026",
                                findings=[EvidenceRecord("web-supplement", "Cmp", "https://cmp.com/1",
                                                         "2026-05-01", "tool A beats tool B on speed")],
                                status="filled")])
    return backfill_fn


@pytest.mark.asyncio
async def test_supplement_section_and_cost_fold_pm():
    base = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                               gather_fn=_gather_fn, fuse_fn=_fuse_fn, supplement=False)
    sup = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=_gather_fn, fuse_fn=_fuse_fn,
                              backfill_fn=_stub_backfill(2), supplement=True)
    assert "Web Supplement" not in base.markdown
    assert "Web Supplement (gap-fill)" in sup.markdown
    assert "tool A beats tool B" in sup.markdown
    assert "https://cmp.com/1" in sup.markdown
    assert round(sup.cost_usd - base.cost_usd, 4) == round(2 * WEB_QUERY_PRICE, 4)


@pytest.mark.asyncio
async def test_supplement_section_renders_for_substack_lens():
    sup = await run_discovery(topic="sync apps", lens="substack", tier="standard", api_key="k",
                              gather_fn=_gather_fn, fuse_fn=_fuse_fn,
                              backfill_fn=_stub_backfill(1), supplement=True)
    assert "Substack Idea Ledger" in sup.markdown
    assert "Web Supplement (gap-fill)" in sup.markdown
    assert "tool A beats tool B" in sup.markdown


@pytest.mark.asyncio
async def test_no_supplement_produces_no_section():
    res = await run_discovery(topic="pm tools", lens="pm", tier="standard", api_key="k",
                              gather_fn=_gather_fn, fuse_fn=_fuse_fn, supplement=False)
    assert "Web Supplement" not in res.markdown
