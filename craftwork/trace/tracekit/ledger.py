"""Ledger entry ids — hand out the next one, and say where the gaps are.

The first engagement reserved `dNN` blocks ahead of writing them (`d10`–`d14`
for a stage whose seat then wrote three entries), which left holes in the
numbering. The holes are harmless — an id is permanent and bare, never
renumbered (#268) — but a coordinator eyeballing the folder for "the next
free number" is how two passes end up claiming one id. This hands it out.

An id is claimed by either of two things, and both are counted: a file on
disk (`dNN-<slug>.md` at the engagement root), and a pass record that names
`<eng-id>.dNN` among its outputs. A reserved-but-unwritten id is claimed,
so it is never handed out twice; it is also reported, because at Close an
id with no file is either a gap to leave alone or an entry someone forgot
to write.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .engagement import Engagement, load_engagement

__all__ = ["EntryIds", "entry_ids", "next_entry_id"]

_ENTRY_FILE = re.compile(r"^d(\d+)-([^.]+)\.md$")
_ENTRY_ID = re.compile(r"^(.+)\.d(\d+)$")


@dataclass
class EntryIds:
    eng_id: str
    on_disk: dict[int, str] = field(default_factory=dict)      # NN → filename
    reserved: dict[int, str] = field(default_factory=dict)     # NN → the pass that recorded it
    width: int = 2

    @property
    def claimed(self) -> set[int]:
        return set(self.on_disk) | set(self.reserved)

    @property
    def next_n(self) -> int:
        return (max(self.claimed) + 1) if self.claimed else 1

    @property
    def next_id(self) -> str:
        return f"{self.eng_id}.d{self.next_n:0{self.width}d}"

    @property
    def gaps(self) -> list[int]:
        """Numbers below the high-water mark that nothing claims — left alone, never reused."""
        return [n for n in range(1, (max(self.claimed) if self.claimed else 0)) if n not in self.claimed]

    @property
    def unwritten(self) -> list[int]:
        """Reserved by a pass record but with no file on disk — a gap, or a forgotten entry."""
        return sorted(n for n in self.reserved if n not in self.on_disk)

    def report(self) -> str:
        lines = [self.next_id]
        lines.append(f"  {len(self.on_disk)} entr{'y' if len(self.on_disk) == 1 else 'ies'} on disk"
                     + (f", high-water d{max(self.claimed):0{self.width}d}" if self.claimed else ""))
        if self.unwritten:
            lines.append("  reserved by a pass but not written: "
                         + ", ".join(f"d{n:0{self.width}d} ({self.reserved[n]})" for n in self.unwritten))
        if self.gaps:
            lines.append("  gaps, left alone — ids are permanent and never reused: "
                         + ", ".join(f"d{n:0{self.width}d}" for n in self.gaps))
        return "\n".join(lines) + "\n"


def entry_ids(eng: Engagement | Path | str) -> EntryIds:
    """Every `dNN` an engagement has claimed, from its files and its pass records."""
    if not isinstance(eng, Engagement):
        eng = load_engagement(eng)
    ids = EntryIds(eng_id=str(eng.brief.get("id") or eng.id))
    for f in sorted(eng.root.glob("d*.md")):
        m = _ENTRY_FILE.match(f.name)
        if m:
            ids.width = max(ids.width, len(m.group(1)))
            ids.on_disk[int(m.group(1))] = f.name
    for r in eng.records:
        for o in r.outputs:
            m = _ENTRY_ID.match(o.id or "")
            if m:
                ids.width = max(ids.width, len(m.group(2)))
                ids.reserved.setdefault(int(m.group(2)), r.pass_id)
    return ids


def next_entry_id(eng: Engagement | Path | str) -> str:
    """The next free entry id, e.g. `pc-eng-001.d17`. Claimed means on disk *or* in a record."""
    return entry_ids(eng).next_id
