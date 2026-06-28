from council.discovery.backfill import BackfillItem, BackfillResult
from council.discovery.evidence import EvidenceRecord
from council.discovery.frame_substack import PostAngle
from council.discovery.fusion import FusionResult
from council.discovery.render_substack import render_substack_ledger, render_substack_brief


def _angle():
    return PostAngle(
        title="Slow export", audience="solo founders", hook="exports hang for minutes",
        itch="Slow export: exports hang for minutes", transfer="After reading, the reader can fix slow exports.",
        evidence_urls=["https://a.com/1"], quotes=["exports hang for minutes"],
        whitespace="nobody covers recovery UX", score=8.0, corroboration=1,
    )


def test_ledger_includes_all_sections():
    fr = FusionResult(blind_spots=["nobody covers recovery UX"], contradictions=["mobile vs desktop"])
    md = render_substack_ledger(topic="export tools", tier="standard", angles=[_angle()],
                                quote_bank=['"exports hang for minutes" — https://a.com/1'],
                                fusion_result=fr, cost_usd=0.42, dropped_count=2)
    assert "# Substack Idea Ledger — export tools" in md
    assert "Slow export" in md
    assert "https://a.com/1" in md
    assert "Blind-spot" in md and "recovery UX" in md
    assert "Quote Bank" in md
    assert "$0.42" in md and "dropped by verification: 2" in md


def test_brief_scaffolds_value_gate_and_keeps_evidence():
    md = render_substack_brief(topic="export tools", segment="solo founders", angles=[_angle()])
    assert "Substack Handoff Brief — export tools" in md
    assert "substack-value-engine" in md          # names the consumer + chain
    assert "Itch" in md and "Solution" in md and "Transfer" in md
    assert "solo founders" in md                   # target segment surfaced
    assert '"exports hang for minutes"' in md      # verbatim evidence carried into the brief
    assert "https://a.com/1" in md


def test_brief_handles_no_angles():
    md = render_substack_brief(topic="x", segment="", angles=[])
    assert "No verified pain points" in md


def test_supplement_section_renders_in_substack_ledger():
    fr = FusionResult(blind_spots=["nobody covers recovery UX"], contradictions=["mobile vs desktop"])
    sup = BackfillResult(skipped=False, queries_run=1, items=[
        BackfillItem(gap="No before/after recovery data", query="export tools recovery data 2026",
                     findings=[EvidenceRecord("web-supplement", "Study", "https://s.com/1", "",
                                              "Recovery UX cut data loss by 40 percent in the study.")],
                     status="filled"),
    ])
    md = render_substack_ledger(topic="export tools", tier="standard", angles=[_angle()],
                                quote_bank=['"exports hang for minutes" — https://a.com/1'],
                                fusion_result=fr, cost_usd=0.42, dropped_count=2, supplement=sup)
    assert "## Web Supplement (gap-fill)" in md
    assert "LEADS" in md
    assert "Recovery UX cut data loss by 40 percent in the study." in md and "https://s.com/1" in md
    # supplement sits between the Blind-spot map and the Quote Bank, separate from ranked angles
    assert md.index("Blind-spot") < md.index("Web Supplement") < md.index("Quote Bank")


def test_supplement_none_keeps_substack_ledger_byte_identical():
    fr = FusionResult(blind_spots=["nobody covers recovery UX"], contradictions=["mobile vs desktop"])
    kw = dict(topic="export tools", tier="standard", angles=[_angle()],
              quote_bank=['"exports hang for minutes" — https://a.com/1'],
              fusion_result=fr, cost_usd=0.42, dropped_count=2)
    assert render_substack_ledger(**kw, supplement=None) == render_substack_ledger(**kw)
    assert "Web Supplement" not in render_substack_ledger(**kw)
