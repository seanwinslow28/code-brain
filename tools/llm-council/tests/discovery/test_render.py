from council.discovery.backfill import BackfillItem, BackfillResult
from council.discovery.evidence import EvidenceRecord
from council.discovery.frame import IdeaCard
from council.discovery.fusion import FusionResult
from council.discovery.render import render_ledger


def _cards():
    return [IdeaCard("Slow export", "PMs", "Slow export: s", "wa", "opp",
                     ["https://a.com/1"], ['"slow"'], 8.0, 1)]


def _fr():
    return FusionResult(blind_spots=["no SSO talk"], contradictions=["mobile vs desktop"])


def _render(supplement=None):
    return render_ledger(topic="pm tools", lens="pm", tier="standard", cards=_cards(),
                         quote_bank=['"slow" — https://a.com/1'], fusion_result=_fr(),
                         cost_usd=0.91, dropped_count=2, supplement=supplement)


def test_render_includes_all_sections():
    md = _render()
    assert "# Idea Ledger — pm tools" in md
    assert "Slow export" in md
    assert "https://a.com/1" in md
    assert "Blind-spot" in md and "no SSO talk" in md
    assert "Quote Bank" in md and "Contradiction" in md
    assert "$0.91" in md and "dropped by verification: 2" in md


def test_supplement_none_is_byte_identical_to_omitted():
    # default-off / --no-supplement path must reproduce the exact pre-Stage-5 ledger
    explicit_none = _render(supplement=None)
    omitted = render_ledger(topic="pm tools", lens="pm", tier="standard", cards=_cards(),
                            quote_bank=['"slow" — https://a.com/1'], fusion_result=_fr(),
                            cost_usd=0.91, dropped_count=2)
    assert explicit_none == omitted
    assert "Web Supplement" not in explicit_none


def test_supplement_skipped_renders_honest_note():
    md = _render(supplement=BackfillResult(skipped=True,
                                           skip_reason="no web-search key configured (set EXA_API_KEY or BRAVE_API_KEY)"))
    assert "## Web Supplement (gap-fill)" in md
    assert "supplement skipped" in md.lower() and "no web-search key" in md.lower()


def test_supplement_findings_render_with_leads_label_and_still_open():
    sup = BackfillResult(skipped=False, queries_run=2, items=[
        BackfillItem(gap="No tool head-to-head", query="pm tools head-to-head 2026",
                     findings=[EvidenceRecord("web-supplement", "Cmp", "https://cmp.com/1", "",
                                              "Tool A beats Tool B on export speed.")], status="filled"),
        BackfillItem(gap="No latency data", query="pm tools latency 2026", findings=[], status="still open"),
    ])
    md = _render(supplement=sup)
    assert "## Web Supplement (gap-fill)" in md
    assert "LEADS" in md                              # honesty label (not consensus-verified)
    assert "Tool A beats Tool B on export speed." in md and "https://cmp.com/1" in md
    assert "still open" in md
    # supplement stays separate from the ranked list (above Contradiction Map)
    assert md.index("Web Supplement") < md.index("Contradiction Map")
