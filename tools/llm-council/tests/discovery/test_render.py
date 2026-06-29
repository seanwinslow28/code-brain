from council.discovery.backfill import BackfillItem, BackfillResult
from council.discovery.bet import ProposedBet
from council.discovery.evidence import EvidenceRecord
from council.discovery.frame import IdeaCard
from council.discovery.fusion import FusionResult
from council.discovery.render import render_ledger
from council.discovery.scoring import ScoreBreakdown


def _score():
    return ScoreBreakdown(composite=68.0, value=0.83, confidence=0.82, importance=0.8,
                          reach=0.71, recency=0.84, source_corroboration=0.55,
                          consensus_ratio=1.0, intensity=4, engagement_sum=340,
                          distinct_sources=5, distinct_domains=2, evidence_date="2026-06")


def _cards():
    return [IdeaCard("Slow export", "PMs", "Slow export: it hangs", '"exports hang for minutes"',
                     ["https://a.com/1"], ['"slow"'], _score(),
                     "Fresh signal — evidence dated 2026-06",
                     ProposedBet("workflow-friction", "users won't switch", "time-on-task test"))]


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
    assert "score 68/100" in md
    assert '"exports hang for minutes"' in md          # leads with verbatim quote
    assert "**Size:**" in md and "importance 4/5" in md and "recency 0.84" in md
    assert "**Confidence:**" in md and "0.82" in md
    assert "**Why now:**" in md
    assert "Proposed bet" in md and "workflow-friction" in md and "Your call" in md
    assert "https://a.com/1" in md
    assert "## ⭐ Whitespace Map — what this run MISSED" in md and "no SSO talk" in md
    assert "## Blind-spot / Whitespace Map" not in md          # old buried heading removed
    assert md.index("⭐ Whitespace Map") < md.index("## Ranked Opportunities")  # hero leads
    assert "Quote Bank" in md and "Contradiction" in md
    assert "$0.91" in md and "dropped by verification: 2" in md


def test_supplement_none_is_byte_identical_to_omitted():
    # default-off / --no-supplement path must reproduce the exact pre-Stage-5 ledger
    explicit_none = _render(supplement=None)
    omitted = render_ledger(topic="pm tools", lens="pm", tier="standard", cards=_cards(),
                            quote_bank=['"slow" — https://a.com/1'], fusion_result=_fr(),
                            cost_usd=0.91, dropped_count=2)
    assert explicit_none == omitted
    assert "## Web Supplement" not in explicit_none   # the section (the hero references it by name)


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


def test_render_includes_receipt_line_and_legend_once():
    md = _render()
    # _score() has distinct_domains=2, recency=0.84, evidence_date="2026-06"
    assert "🧾 corroborated · 2 independent domains" in md
    assert "fresh · evidence 2026-06" in md
    assert md.count("Receipts** show evidence") == 1          # legend once, not per-card
    assert "**Size:**" in md and "**Confidence:**" in md      # detail lines kept (augment, not replace)
    assert md.index("score 68/100") < md.index("🧾") < md.index("**Who:**")  # receipt under heading


def test_render_single_source_card_reads_single_source():
    score = ScoreBreakdown(composite=40.0, value=0.5, confidence=0.6, importance=0.6,
                           reach=0.4, recency=0.4, source_corroboration=0.3, consensus_ratio=0.5,
                           intensity=3, engagement_sum=50, distinct_sources=1, distinct_domains=1,
                           evidence_date="2026-05-20")
    card = IdeaCard("Niche bug", "devs", "Niche bug: x", '"x"', ["https://b.com/1"], ['"x"'],
                    score, "Older signal", ProposedBet("s", "a", "t"))
    md = render_ledger(topic="t", lens="pm", tier="standard", cards=[card], quote_bank=[],
                       fusion_result=_fr(), cost_usd=0.1, dropped_count=0)
    assert "🧾 single-source · 1 domain" in md
    assert "well-corroborated" not in md                       # not over-stated


def test_render_empty_cards_no_receipts_no_legend():
    md = render_ledger(topic="t", lens="pm", tier="standard", cards=[], quote_bank=[],
                       fusion_result=_fr(), cost_usd=0.1, dropped_count=3)
    assert "🧾" not in md
    assert "Receipts** show evidence" not in md
    assert "No pain points survived verification" in md
