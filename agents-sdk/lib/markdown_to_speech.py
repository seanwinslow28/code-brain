"""Verbatim markdown → speech-ready segments for the doc_to_audio pipeline.

Hard guarantee: sentence content is preserved byte-for-byte. Only structural
markdown (frontmatter, code fences, wikilinks, links, emphasis, tables) is
normalized. No paraphrasing, no rewriting.

Output is a list of `Segment` (speakable text) and `SectionBreak` (heading
markers, triggering a 200ms silence in the synthesizer). Tables are exploded
into one Segment per row with cells comma-joined.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Union


# ─── data shapes ──────────────────────────────────────────────────────────

@dataclass
class Segment:
    """A speakable run of text."""
    text: str


@dataclass
class SectionBreak:
    """A heading break — render as a brief silence + the heading title."""
    level: int  # 1, 2, or 3
    title: str


Element = Union[Segment, SectionBreak]


# ─── regexes ──────────────────────────────────────────────────────────────

_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*\n", re.DOTALL)
_CODE_FENCE_RE = re.compile(r"```[^\n]*\n.*?\n```", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
_WIKILINK_RE = re.compile(r"\[\[([^\]\n|#]+)(?:#[^\]\n|]+)?(?:\|([^\]\n]+))?\]\]")
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK_RE = re.compile(r"\[([^\]\n]+)\]\([^)\n]+\)")
_BOLDITALIC_RE = re.compile(r"\*{1,3}([^*\n]+)\*{1,3}")
_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")
_TABLE_LINE_RE = re.compile(r"^\|.*\|\s*$")
_TABLE_SEP_RE = re.compile(r"^\|[\s:|-]+\|\s*$")
_BLOCKQUOTE_RE = re.compile(r"^>\s?", re.MULTILINE)
_LIST_MARKER_RE = re.compile(r"^(\s*)[-*+]\s+", re.MULTILINE)
_NUMBERED_LIST_RE = re.compile(r"^(\s*)\d+\.\s+", re.MULTILINE)
_HORIZONTAL_RULE_RE = re.compile(r"^[-*_]{3,}\s*$", re.MULTILINE)
_MULTI_BLANK_RE = re.compile(r"\n{3,}")


# ─── pure helpers (each composes for end-to-end preprocess) ───────────────


def strip_frontmatter(text: str) -> str:
    """Drop a leading `---\\n...\\n---\\n` YAML block if present."""
    return _FRONTMATTER_RE.sub("", text, count=1)


def strip_code_fences(text: str) -> str:
    """Replace fenced code blocks with 'Code block omitted.' and strip inline backticks."""
    text = _CODE_FENCE_RE.sub("Code block omitted.", text)
    text = _INLINE_CODE_RE.sub(r"\1", text)
    return text


def flatten_wikilinks(text: str) -> str:
    """`[[target|display]]` → `display`; `[[target]]` → `target`; anchors dropped."""
    def repl(m: re.Match[str]) -> str:
        target = m.group(1).strip()
        display = (m.group(2) or "").strip()
        return display if display else target
    return _WIKILINK_RE.sub(repl, text)


def flatten_links(text: str) -> str:
    """Drop images entirely; reduce `[text](url)` to `text`."""
    text = _IMAGE_RE.sub("", text)
    text = _LINK_RE.sub(r"\1", text)
    return text


def flatten_emphasis(text: str) -> str:
    """`**bold**` / `*italic*` / `***both***` → bare visible text."""
    return _BOLDITALIC_RE.sub(r"\1", text)


def table_to_segments(table_text: str) -> list[str]:
    """One Segment per row, cells joined with ', '. Separator rows dropped.

    Input is the raw markdown table block; returns a list of strings ready to
    feed into Segment(...). Trailing period added per row so the TTS engine
    inserts a natural pause between rows.
    """
    out: list[str] = []
    for line in table_text.splitlines():
        line = line.strip()
        if not line or not _TABLE_LINE_RE.match(line):
            continue
        if _TABLE_SEP_RE.match(line):
            continue
        # Drop outer pipes, split on |, strip each cell
        cells = [c.strip() for c in line.strip("|").split("|")]
        cells = [c for c in cells if c]
        if not cells:
            continue
        out.append(", ".join(cells) + ".")
    return out


# ─── orchestrator ─────────────────────────────────────────────────────────


def preprocess(text: str) -> list[Element]:
    """Convert markdown text into ordered Segment / SectionBreak elements.

    Pipeline:
        1. strip_frontmatter
        2. strip_code_fences
        3. flatten_wikilinks, flatten_links, flatten_emphasis
        4. line-by-line walk:
            - heading line → SectionBreak
            - table block → table_to_segments (one Segment per row)
            - paragraph line → accumulate into a Segment, flushed on blank line
    """
    text = strip_frontmatter(text)
    text = strip_code_fences(text)
    text = flatten_wikilinks(text)
    text = flatten_links(text)
    text = flatten_emphasis(text)
    text = _BLOCKQUOTE_RE.sub("", text)
    text = _LIST_MARKER_RE.sub(r"\1", text)
    text = _NUMBERED_LIST_RE.sub(r"\1", text)
    text = _HORIZONTAL_RULE_RE.sub("", text)
    text = _MULTI_BLANK_RE.sub("\n\n", text)

    elements: list[Element] = []
    lines = text.splitlines()
    i = 0
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            joined = " ".join(p.strip() for p in paragraph if p.strip())
            if joined:
                elements.append(Segment(text=joined))
            paragraph.clear()

    while i < len(lines):
        line = lines[i]
        # Heading
        m = _HEADING_RE.match(line)
        if m:
            flush_paragraph()
            level = len(m.group(1))
            title = m.group(2).strip()
            elements.append(SectionBreak(level=level, title=title))
            i += 1
            continue
        # Table block
        if _TABLE_LINE_RE.match(line.strip()):
            flush_paragraph()
            table_lines: list[str] = []
            while i < len(lines) and _TABLE_LINE_RE.match(lines[i].strip()):
                table_lines.append(lines[i])
                i += 1
            for row_text in table_to_segments("\n".join(table_lines)):
                elements.append(Segment(text=row_text))
            continue
        # Blank line → flush
        if not line.strip():
            flush_paragraph()
            i += 1
            continue
        # Plain paragraph line
        paragraph.append(line)
        i += 1

    flush_paragraph()
    return elements
