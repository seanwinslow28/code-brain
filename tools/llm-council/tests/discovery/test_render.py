from council.discovery.frame import IdeaCard
from council.discovery.fusion import FusionResult
from council.discovery.render import render_ledger


def test_render_includes_all_sections():
    cards = [IdeaCard("Slow export", "PMs", "Slow export: s", "wa", "opp",
                      ["https://a.com/1"], ['"slow"'], 8.0, 1)]
    fr = FusionResult(blind_spots=["no SSO talk"], contradictions=["mobile vs desktop"])
    md = render_ledger(topic="pm tools", lens="pm", tier="standard", cards=cards,
                       quote_bank=['"slow" — https://a.com/1'], fusion_result=fr,
                       cost_usd=0.91, dropped_count=2)
    assert "# Idea Ledger — pm tools" in md
    assert "Slow export" in md
    assert "https://a.com/1" in md
    assert "Blind-spot" in md and "no SSO talk" in md
    assert "Quote Bank" in md and "Contradiction" in md
    assert "$0.91" in md and "dropped by verification: 2" in md
