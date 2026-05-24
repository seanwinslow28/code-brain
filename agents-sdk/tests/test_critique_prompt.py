from pathlib import Path

from lib.critique_prompt import (
    build_critique_prompt,
    extract_wikilinks_summary,
    load_standing_context,
)


ARTICLE = """\
---
title: "Writing Voice Modes"
type: concept
sources:
  - .claude/skills/writing-voice-modes/SKILL.md
created: 2026-05-13
---

## Definition

Sean's writing-voice-modes skill calibrates 5 authorial voices for long-form writing:
1. Domestic Observer (David Sedaris)
2. Gonzo Technical (Hunter S. Thompson)
3. Beat Flow (Jack Kerouac)
4. Minimalist Absurdist (Kurt Vonnegut)
5. Sean Mode

## Related Concepts

[[creative-writing]] [[blog-cadence]] [[tone-calibration]]
"""


def test_build_critique_prompt_includes_slug_and_body():
    prompt = build_critique_prompt(
        slug="writing-voice-modes",
        article_body=ARTICLE,
        source_path=".claude/skills/writing-voice-modes/SKILL.md",
        recent_titles=["agentic-engineering", "vault-architecture"],
    )
    assert "writing-voice-modes" in prompt
    assert "Domestic Observer (David Sedaris)" in prompt
    assert ".claude/skills/writing-voice-modes/SKILL.md" in prompt


def test_build_critique_prompt_extracts_wikilink_summary():
    prompt = build_critique_prompt(
        slug="writing-voice-modes",
        article_body=ARTICLE,
        source_path="any.md",
        recent_titles=[],
    )
    # The wikilink summary lists the three [[targets]] from the article body.
    assert "creative-writing" in prompt
    assert "blog-cadence" in prompt
    assert "tone-calibration" in prompt


def test_build_critique_prompt_caps_recent_titles_at_default_limit():
    long_titles = [f"concept-{i}" for i in range(100)]
    prompt = build_critique_prompt(
        slug="x", article_body="body", source_path="p", recent_titles=long_titles,
    )
    # Default cap is 30 — verify concept-99 NOT present but concept-0 IS.
    assert "concept-0" in prompt
    assert "concept-99" not in prompt


def test_extract_wikilinks_summary_dedupes_and_orders():
    body = "Some [[alpha]] text [[beta]] more [[alpha]] [[gamma]]"
    assert extract_wikilinks_summary(body) == "alpha, beta, gamma"


def test_extract_wikilinks_summary_handles_aliased():
    body = "Reference [[real-slug|Display Name]] in body"
    assert extract_wikilinks_summary(body) == "real-slug"


def test_extract_wikilinks_summary_empty_when_no_links():
    assert extract_wikilinks_summary("no links here") == "(no wikilinks)"


# ---------------------------------------------------------------------------
# Standing-context preamble — "About Sean" enrichment (2026-05-24, Round 2)
# ---------------------------------------------------------------------------


def test_load_standing_context_returns_empty_when_file_missing(tmp_path):
    """Missing-file degrades to empty string; the prompt template's
    {standing_context} slot then renders as a blank line. No exception, no
    half-rendered prompt — the agent must stay quiet when enrichment is off."""
    assert load_standing_context(tmp_path / "does-not-exist.md") == ""


def test_load_standing_context_reads_file_contents(tmp_path):
    p = tmp_path / "ctx.md"
    p.write_text("# About Sean\n\nbuilt thing X.\n", encoding="utf-8")
    out = load_standing_context(p)
    assert "About Sean" in out
    assert out == out.strip()  # trimmed for clean injection


def test_build_critique_prompt_includes_standing_context_by_default(tmp_path):
    """Default behavior: the preamble is prepended right after the
    'Sean's complaint' line, before ARTICLE UNDER REVIEW. This is the
    Round-2-and-beyond behavior — nightly + manual runs both get it."""
    ctx = tmp_path / "ctx.md"
    ctx.write_text("STANDING_CONTEXT_MARKER", encoding="utf-8")
    out = build_critique_prompt(
        slug="x", article_body="body", source_path="x.md",
        recent_titles=[],
        standing_context_path=ctx,
    )
    assert "STANDING_CONTEXT_MARKER" in out
    # Position check: preamble lands BEFORE the article body, not after.
    assert out.index("STANDING_CONTEXT_MARKER") < out.index("ARTICLE UNDER REVIEW")


def test_build_critique_prompt_skips_standing_context_when_disabled(tmp_path):
    """`include_standing_context=False` powers ablation runs (Round 1 vs Round 2
    on the same target). The CLIs see the original outside-perspective-only
    prompt with no enrichment — must match pre-2026-05-24 behavior."""
    ctx = tmp_path / "ctx.md"
    ctx.write_text("STANDING_CONTEXT_MARKER", encoding="utf-8")
    out = build_critique_prompt(
        slug="x", article_body="body", source_path="x.md",
        recent_titles=[],
        standing_context_path=ctx,
        include_standing_context=False,
    )
    assert "STANDING_CONTEXT_MARKER" not in out
