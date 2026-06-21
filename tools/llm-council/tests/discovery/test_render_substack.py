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
