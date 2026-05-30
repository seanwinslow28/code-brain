"""Tests for mock_interview_loop.py — the Task 19 (A6) mock-interview grader.

Covers the PURE parsing + aggregation layer (no network, no audio, no council).
The transcription + live-council legs are integration-only and exercised by
Sean on his Mac (mic + OpenRouter key + faster-whisper). Here we pin:
  1. extract_json_objects — tolerant balanced-brace JSON extraction
  2. parse_panelist_scorecards — pulls only the 4 panelist cards, not chairman prose
  3. aggregate_scorecards — median-per-dimension + overall mean + Gate-C bar
  4. extract_chairman_synthesis — preserves the qualitative read
"""

from __future__ import annotations

import sys
from pathlib import Path

# scripts/ isn't on the default path; insert it (mirrors test_auto_stub_people.py).
SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import mock_interview_loop as mil  # type: ignore[import-not-found]  # noqa: E402


def _card(**overrides) -> str:
    """A panelist scorecard JSON string with all 8 dims = 8 unless overridden."""
    scores = {dim: {"score": overrides.get(dim, 8), "justification": "x"} for dim in mil.DIMENSIONS}
    revs = overrides.get("revs", ["cut the V3 tangent", "drop two 'kind of' hedges"])
    import json
    return json.dumps({"scores": scores, "overall_score": 8.0, "three_specific_revisions": revs})


def _council_markdown(panelist_cards: list[str], chairman: str = "The panel converged on 7-8.") -> str:
    """Reconstruct the shape cli.py._render_markdown produces."""
    parts = ["# Council Session — interview-grader-test\n", "## Original prompt\n```\n…\n```\n",
             "## Council responses\n"]
    for i, card in enumerate(panelist_cards):
        parts.append(f"### model-{i}\n")
        parts.append(card)
        parts.append("")
    parts.append("## Cross-rankings\n")
    parts.append("### Judge: model-0\n- **Order:** A > B\n- **Reasoning:** {not a scorecard}\n")
    parts.append("## Chairman synthesis\n")
    parts.append("_Chairman model: `anthropic/claude-opus-4.7`_\n")
    parts.append(chairman)
    return "\n".join(parts)


# ── extract_json_objects ─────────────────────────────────────────────────────
def test_extract_plain_object():
    objs = mil.extract_json_objects('prefix {"a": 1} suffix')
    assert objs == [{"a": 1}]


def test_extract_ignores_braces_in_strings():
    objs = mil.extract_json_objects('{"note": "has a } brace and { inside"}')
    assert objs == [{"note": "has a } brace and { inside"}]


def test_extract_multiple_objects():
    objs = mil.extract_json_objects('{"a": 1} junk {"b": {"c": 2}}')
    assert objs == [{"a": 1}, {"b": {"c": 2}}]


def test_extract_tolerates_json_fence():
    objs = mil.extract_json_objects('```json\n{"a": 1}\n```')
    assert objs == [{"a": 1}]


# ── parse_panelist_scorecards ────────────────────────────────────────────────
def test_parse_picks_up_four_cards_not_chairman():
    md = _council_markdown([_card(), _card(), _card(), _card()])
    cards = mil.parse_panelist_scorecards(md)
    assert len(cards) == 4
    assert all("scores" in c for c in cards)


def test_parse_excludes_crossrank_and_chairman_braces():
    # The cross-rank reasoning contains a literal {...} that is NOT a scorecard;
    # the chairman prose could too. Neither should be counted.
    md = _council_markdown([_card(), _card()])
    cards = mil.parse_panelist_scorecards(md)
    assert len(cards) == 2  # only the two real panelist cards


# ── aggregate_scorecards ─────────────────────────────────────────────────────
def test_aggregate_median_and_overall():
    # Three cards, timing scores 6/8/10 -> median 8; everything else 8 -> overall 8.0
    cards = [
        {"scores": {d: {"score": 8} for d in mil.DIMENSIONS}},
        {"scores": {**{d: {"score": 8} for d in mil.DIMENSIONS}, "timing": {"score": 6}}},
        {"scores": {**{d: {"score": 8} for d in mil.DIMENSIONS}, "timing": {"score": 10}}},
    ]
    agg = mil.aggregate_scorecards(cards)
    assert agg["panelists"] == 3
    assert agg["dimensions"]["timing"]["median"] == 8.0
    assert agg["dimensions"]["timing"]["spread"] == 4.0
    assert agg["overall_score"] == 8.0
    assert agg["passes_gate_c"] is True


def test_aggregate_below_gate_c():
    cards = [{"scores": {d: {"score": 5} for d in mil.DIMENSIONS}}]
    agg = mil.aggregate_scorecards(cards)
    assert agg["overall_score"] == 5.0
    assert agg["passes_gate_c"] is False


def test_aggregate_handles_bare_int_scores():
    # Some models may emit {"timing": 7} instead of {"timing": {"score": 7}}.
    cards = [{"scores": {d: 7 for d in mil.DIMENSIONS}}]
    agg = mil.aggregate_scorecards(cards)
    assert agg["overall_score"] == 7.0


def test_aggregate_merges_and_dedupes_revisions():
    cards = [
        {"scores": {d: {"score": 8} for d in mil.DIMENSIONS}, "three_specific_revisions": ["fix A", "fix B"]},
        {"scores": {d: {"score": 8} for d in mil.DIMENSIONS}, "three_specific_revisions": ["fix B", "fix C"]},
    ]
    agg = mil.aggregate_scorecards(cards)
    assert agg["merged_revisions"] == ["fix A", "fix B", "fix C"]


def test_aggregate_empty_is_safe():
    agg = mil.aggregate_scorecards([])
    assert agg["overall_score"] is None
    assert "_error" in agg


# ── extract_chairman_synthesis ───────────────────────────────────────────────
def test_chairman_synthesis_preserved():
    md = _council_markdown([_card()], chairman="Strong on specificity, weak on filler.")
    syn = mil.extract_chairman_synthesis(md)
    assert "Strong on specificity" in syn


# ── full parse->aggregate path on a realistic council markdown ───────────────
def test_end_to_end_parse_then_aggregate():
    md = _council_markdown([_card(timing=6), _card(timing=8), _card(timing=10), _card(timing=8)])
    agg = mil.aggregate_scorecards(mil.parse_panelist_scorecards(md))
    assert agg["panelists"] == 4
    assert agg["overall_score"] == 8.0
