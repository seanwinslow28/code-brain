"""taxonomy.md — rung 1's tracked vocabulary, read so `failure_code` cannot be free text.

One file per studio (#272 decision 7's ladder; the process-waste codes ratified on
#296 clause 8, landed on #298; the seat failure modes opened from the first
engagement's labels on #299). Studio-agnostic: the parser knows the table's shape, never which
codes a studio has. The default path is the kit's own folder, so the content
machine's copy (#291) passes its own file rather than inheriting this one.

A code row may be marked quote-required, which makes the code a claim the reader
can check: the label's critique has to quote the text it indicts.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

__all__ = ["Code", "Taxonomy", "DEFAULT_TAXONOMY_PATH", "parse_taxonomy", "load_taxonomy", "critique_quotes"]

DEFAULT_TAXONOMY_PATH = Path(__file__).resolve().parent.parent / "taxonomy.md"

_HEADER = ("code", "family", "a label with this code says", "quote")
_CODE = re.compile(r"`([a-z][a-z0-9-]*)`")
# a quotation the reader can go and find: "…", '…', “…”, or `…` of three chars or more
_QUOTED = re.compile(r"\"[^\"]{3,}\"|'[^']{3,}'|“[^”]{3,}”|`[^`]{3,}`")


@dataclass(frozen=True)
class Code:
    code: str
    family: str
    means: str
    quote_required: bool


@dataclass(frozen=True)
class Taxonomy:
    codes: dict[str, Code]
    path: Optional[Path] = None

    @property
    def open(self) -> bool:
        """True once any code exists — rung 1 has begun."""
        return bool(self.codes)

    def __contains__(self, code: str) -> bool:
        return code in self.codes


def _cells(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def parse_taxonomy(text: str, path: Optional[Path] = None) -> Taxonomy:
    """Read every table whose header is the code table's, in file order.

    A file with no such table is a taxonomy with no codes — honest, not an error:
    rung 1 has not opened. The process-waste family and the seat failure modes
    live in separate tables under separate headings (#299), and both count. A row
    whose first cell holds no `code` span is skipped, so prose tables elsewhere in
    the file are ignored; a later table that repeats a code overrides the earlier row.
    """
    codes: dict[str, Code] = {}
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            header = tuple(c.lower() for c in _cells(lines[i]))
            if header == _HEADER:
                i += 1
                if i < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i]):
                    i += 1
                while i < len(lines) and lines[i].lstrip().startswith("|"):
                    cells = _cells(lines[i])
                    m = _CODE.search(cells[0]) if cells else None
                    if m and len(cells) == len(_HEADER):
                        quote = "required" in cells[3].lower()
                        codes[m.group(1)] = Code(m.group(1), cells[1], cells[2], quote)
                    i += 1
                continue
        i += 1
    return Taxonomy(codes, path)


def load_taxonomy(path: Optional[Path] = None) -> Taxonomy:
    """Load a studio's taxonomy; a missing file is an unopened rung 1, never a crash."""
    p = Path(path) if path is not None else DEFAULT_TAXONOMY_PATH
    if not p.is_file():
        return Taxonomy({}, p)
    return parse_taxonomy(p.read_text(encoding="utf-8"), p)


def critique_quotes(critique: str) -> bool:
    """True when the critique contains a findable quotation of the text it indicts."""
    return bool(_QUOTED.search(critique or ""))
