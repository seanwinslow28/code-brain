"""Tests for verbatim markdown → speech-ready text conversion."""
from __future__ import annotations

import pytest

from lib.markdown_to_speech import (
    SectionBreak,
    Segment,
    preprocess,
    strip_frontmatter,
    strip_code_fences,
    flatten_wikilinks,
    flatten_links,
    flatten_emphasis,
    table_to_segments,
)


# ─── frontmatter ──────────────────────────────────────────────────────────

def test_strip_frontmatter_removes_yaml_block():
    text = "---\ntitle: Foo\ntype: note\n---\n\n# Body\n\nHello."
    assert strip_frontmatter(text) == "# Body\n\nHello."


def test_strip_frontmatter_no_frontmatter_unchanged():
    text = "# Body\n\nHello."
    assert strip_frontmatter(text) == text


def test_strip_frontmatter_handles_trailing_dashes_in_body():
    text = "---\ntitle: Foo\n---\n\nBody with --- mid-sentence."
    assert strip_frontmatter(text) == "Body with --- mid-sentence."


# ─── code fences ──────────────────────────────────────────────────────────

def test_strip_code_fences_replaces_with_omitted_marker():
    text = "Before.\n\n```python\nprint('x')\n```\n\nAfter."
    assert strip_code_fences(text) == "Before.\n\nCode block omitted.\n\nAfter."


def test_strip_code_fences_unlabeled_fence():
    text = "A.\n\n```\nfoo\n```\n\nB."
    assert strip_code_fences(text) == "A.\n\nCode block omitted.\n\nB."


def test_strip_code_fences_inline_backticks_preserved_text():
    text = "Run `pytest` to verify."
    assert strip_code_fences(text) == "Run pytest to verify."


# ─── wikilinks ────────────────────────────────────────────────────────────

def test_flatten_wikilinks_pipe_form_uses_display():
    assert flatten_wikilinks("See [[concepts/error-handling|error handling]] for details.") == \
        "See error handling for details."


def test_flatten_wikilinks_bare_form_uses_target():
    assert flatten_wikilinks("See [[Nate]] yesterday.") == "See Nate yesterday."


def test_flatten_wikilinks_anchor_dropped():
    assert flatten_wikilinks("See [[doc#section|details]] now.") == "See details now."


# ─── markdown links ───────────────────────────────────────────────────────

def test_flatten_links_keeps_visible_text():
    assert flatten_links("Read the [Anthropic guide](https://example.com).") == \
        "Read the Anthropic guide."


def test_flatten_links_drops_images():
    assert flatten_links("Before ![alt](img.png) after.") == "Before  after."


# ─── emphasis ─────────────────────────────────────────────────────────────

def test_flatten_emphasis_strips_markers():
    assert flatten_emphasis("**bold** and *italic* and ***both***.") == \
        "bold and italic and both."


def test_flatten_emphasis_preserves_apostrophes():
    assert flatten_emphasis("It's Sean's vault.") == "It's Sean's vault."


# ─── tables ───────────────────────────────────────────────────────────────

def test_table_to_segments_speaks_rows_with_pauses():
    table = (
        "| Col A | Col B |\n"
        "|---|---|\n"
        "| foo | bar |\n"
        "| baz | qux |\n"
    )
    segs = table_to_segments(table)
    # Header row + 2 body rows = 3 segments, each cell comma-separated
    assert len(segs) == 3
    assert segs[0] == "Col A, Col B."
    assert segs[1] == "foo, bar."
    assert segs[2] == "baz, qux."


# ─── end-to-end preprocess ────────────────────────────────────────────────

def test_preprocess_canonical_test_doc_shape():
    """The canonical retrofit doc shape: frontmatter, H1, paragraph, table, code fence."""
    source = (
        "---\n"
        "type: retrofit-plan\n"
        "created: 2026-05-13\n"
        "---\n\n"
        "# Vault Synthesizer v2 — Retrofit Tiers\n\n"
        "On 2026-05-13 morning, after a clean nightly synth run.\n\n"
        "## Why this exists\n\n"
        "Specific evidence from [[concepts/cluster-collapse|cluster collapse]].\n\n"
        "| Defect | Pattern |\n"
        "|---|---|\n"
        "| Cluster bias | TopClustRAG |\n\n"
        "```python\n"
        "format_connection_article()\n"
        "```\n\n"
        "End of body.\n"
    )
    segments = preprocess(source)
    # Filter to just speakable text + section breaks
    section_titles = [s.title for s in segments if isinstance(s, SectionBreak)]
    speech_text = " ".join(s.text for s in segments if isinstance(s, Segment))

    assert "Vault Synthesizer v2 — Retrofit Tiers" in section_titles
    assert "Why this exists" in section_titles
    # Verbatim sentence preservation
    assert "On 2026-05-13 morning, after a clean nightly synth run." in speech_text
    # Wikilink flattened, display text preserved verbatim
    assert "Specific evidence from cluster collapse." in speech_text
    # Code fence replaced
    assert "Code block omitted." in speech_text
    # Table rows present
    assert "Defect, Pattern." in speech_text
    assert "Cluster bias, TopClustRAG." in speech_text
    # No frontmatter leakage
    assert "retrofit-plan" not in speech_text
    assert "created: 2026-05-13" not in speech_text


def test_preprocess_preserves_sentence_verbatim_no_paraphrase():
    """The hard guarantee: a sentence enters, the same sentence leaves."""
    source = "On 2026-05-13, the synthesizer wrote 203 concepts and 111 connections."
    segments = preprocess(source)
    speech = " ".join(s.text for s in segments if isinstance(s, Segment))
    assert speech.strip() == source.strip()
