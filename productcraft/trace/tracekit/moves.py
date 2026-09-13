"""The `## Moves` section every artifact closes with (#272 decision 4).

Torres's change-set pattern with a fixed five-word vocabulary. Moves are
claims until a replay confirms them; rung 0 only checks that each line names
an upstream item that exists and that a split's children are new.

Grammar, one line per move (an em dash or a hyphen after the op):

    - kept — <upstream item> from <source>
    - added — <new item> from <source>
    - split — <upstream item> → <child>, <child> from <source>
    - merged — <upstream item> + <upstream item> → <item> from <source>
    - dropped — <upstream item> from <source>; <why>

The Strategist's origin draft writes one line instead:

    origin draft, no upstream — leaned on: <thing>; <thing>
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional

__all__ = ["OPS", "Move", "MovesSection", "parse_moves", "extract_ids"]

OPS = ("kept", "added", "split", "merged", "dropped")

_HEADING = re.compile(r"^##\s+Moves\s*$", re.M)
_NEXT_HEADING = re.compile(r"^(##\s|meter:)", re.M)
_LINE = re.compile(r"^-\s+([A-Za-z]+)\s+(?:—|–|-)\s+(.*)$")
_ORIGIN = re.compile(r"^origin draft,\s*no upstream(?:\s*(?:—|–|-)\s*leaned on:\s*(.*))?$", re.I)
_ID = re.compile(r"\b([A-Z]{1,4})-?(\d+)([a-z])?\b")
_RANGE = re.compile(r"\b([A-Z]{1,4})-?(\d+)\s*[–\-]\s*(?:\1-?)?(\d+)\b")


@dataclass
class Move:
    op: str
    item: str                       # the upstream item acted on (kept/split/dropped), or the new item (added)
    source: str                     # what the line says it came from
    children: list[str] = field(default_factory=list)   # split: the new items
    items: list[str] = field(default_factory=list)      # merged: the upstream items combined
    result: Optional[str] = None    # merged: the surviving item
    why: Optional[str] = None       # dropped: the reason after the semicolon
    lineno: int = 0


@dataclass
class MovesSection:
    origin: bool = False
    leaned_on: list[str] = field(default_factory=list)
    lines: list[Move] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def counts(self) -> dict[str, int]:
        return {op: sum(1 for m in self.lines if m.op == op) for op in OPS}


def parse_moves(text: str) -> Optional[MovesSection]:
    """Parse the artifact's `## Moves` section; None when the artifact has none."""
    m = _HEADING.search(text)
    if not m:
        return None
    start = m.end()
    nxt = _NEXT_HEADING.search(text, start)
    section = text[start : nxt.start() if nxt else len(text)]
    base_line = text[:start].count("\n") + 1
    out = MovesSection()
    for offset, raw in enumerate(section.split("\n")):
        line = raw.strip()
        lineno = base_line + offset
        if not line or line.startswith("<!--"):
            continue
        o = _ORIGIN.match(line)
        if o:
            out.origin = True
            if o.group(1):
                out.leaned_on = [s.strip() for s in re.split(r";\s*", o.group(1)) if s.strip()]
            continue
        lm = _LINE.match(line)
        if not lm:
            out.errors.append(f"line {lineno}: not a move line: {line!r}")
            continue
        op, rest = lm.group(1).lower(), lm.group(2).strip()
        if op not in OPS:
            out.errors.append(f"line {lineno}: unknown move `{op}` ({' | '.join(OPS)})")
            continue
        split_at = re.search(r"\s+from\s+", rest)
        if not split_at:
            out.errors.append(f"line {lineno}: `{op}` names no source (… from <source>)")
            continue
        item_text, source = rest[: split_at.start()].strip(), rest[split_at.end() :].strip()
        mv = Move(op=op, item=item_text, source=source, lineno=lineno)
        if op == "split":
            if "→" not in item_text:
                out.errors.append(f"line {lineno}: a split names its children: <item> → <child>, <child>")
                continue
            parent, kids = item_text.split("→", 1)
            mv.item = parent.strip()
            mv.children = [k.strip() for k in kids.split(",") if k.strip()]
        elif op == "merged":
            if "→" not in item_text:
                out.errors.append(f"line {lineno}: a merge names its result: <item> + <item> → <item>")
                continue
            parts, result = item_text.split("→", 1)
            mv.items = [p.strip() for p in parts.split("+") if p.strip()]
            mv.result = result.strip()
            mv.item = " + ".join(mv.items)
        elif op == "dropped":
            if ";" in source:
                src, why = source.split(";", 1)
                mv.source, mv.why = src.strip(), why.strip()
        out.lines.append(mv)
    return out


def extract_ids(text: str) -> list[str]:
    """Item ids like O2, OC-1a, KR-2 — ranges E1–E5 and B1-B3 expanded.

    Prose with no id ("Action 4") yields []; callers fall back to a phrase
    search over the upstream text.
    """
    text = text.strip().strip('"“”')
    out: list[str] = []
    covered: list[tuple[int, int]] = []
    for r in _RANGE.finditer(text):
        prefix, lo, hi = r.group(1), int(r.group(2)), int(r.group(3))
        if hi >= lo and hi - lo < 100:
            sep = "-" if "-" in text[r.start() : r.start() + len(prefix) + 1] else ""
            out.extend(f"{prefix}{sep}{n}" for n in range(lo, hi + 1))
            covered.append((r.start(), r.end()))
    for m in _ID.finditer(text):
        if any(a <= m.start() < b for a, b in covered):
            continue
        out.append(m.group(0))
    return out
