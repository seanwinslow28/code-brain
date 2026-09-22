"""Registry numbers — the runtime × seat table the runtime registry reads (#272 decision 9, built on #286).

The registry (`productcraft/templates/runtime-registry.md`) carries one row per
runtime route and, under § Numbers, what each runtime has actually done on real
work. Those numbers are never typed by hand: this module derives them from the
pass records and the labels file of one or more engagements, in the shapes the
design ratified — labeled passes as **counts** ("3 of 4", no percentage anywhere,
the design forbids one below ten and nothing here ever prints one), the rung-0
clean count, median runtime-reported tokens and wall-clock over measured passes,
meter availability, trials and promotions.

A promotion is a dated, owner-approved substitution (#272 decision 9) and lives
in the trial record's `## Notes` as a line beginning `promoted:`; the count here
reads that line and nothing else. A trial whose blind label passes while its
baseline's fails is *promotable*, which is a fact about the labels and is
counted separately.
"""
from __future__ import annotations

import re
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

from .checker import run_checks
from .engagement import METER_SOURCES, Engagement, Record, load_engagement, normalize_meter

__all__ = ["Cell", "numbers", "numbers_for", "render_markdown", "SEAT_FAMILIES", "family_of"]

# the seat families #287 ranks runtimes by (research note 2026-09-21-open-models-per-seat-role.md);
# the numbers stay per seat, and the family is a column so either roll-up reads off the same table
SEAT_FAMILIES = {
    "product-strategist": "framing",
    "product-leadership": "framing",
    "discovery-lead": "discovery synthesis",
    "insights-analytics": "evidence grading",
    "business-economics": "quantitative",
    "growth-distribution": "growth",
    "delivery-execution": "delivery breakdown",
    "red-team-gate": "gate",
    "coordinator": "coordination",
}


def family_of(seat: str) -> str:
    return SEAT_FAMILIES.get(seat, "other")


@dataclass
class Cell:
    """One runtime × seat cell, or a runtime's roll-up when `seat` is empty."""
    runtime: str
    seat: str = ""
    passes: int = 0
    labeled: int = 0
    passed: int = 0                    # labeled rows whose verdict is pass
    clean: int = 0                     # passes no rung-0 finding names
    measured: int = 0                  # passes whose meter carries a real count
    tokens: list[int] = field(default_factory=list)
    wall_clock: list[int] = field(default_factory=list)
    trials: int = 0
    promotable: int = 0
    promoted: int = 0
    engagements: set[str] = field(default_factory=set)

    @property
    def family(self) -> str:
        return family_of(self.seat) if self.seat else ""

    @property
    def median_tokens(self) -> Optional[int]:
        return int(statistics.median(self.tokens)) if self.tokens else None

    @property
    def median_wall_clock_s(self) -> Optional[int]:
        return int(statistics.median(self.wall_clock)) if self.wall_clock else None

    def add(self, other: "Cell") -> None:
        self.passes += other.passes
        self.labeled += other.labeled
        self.passed += other.passed
        self.clean += other.clean
        self.measured += other.measured
        self.tokens += other.tokens
        self.wall_clock += other.wall_clock
        self.trials += other.trials
        self.promotable += other.promotable
        self.promoted += other.promoted
        self.engagements |= other.engagements

    def as_dict(self) -> dict:
        return {
            "runtime": self.runtime, "seat": self.seat, "family": self.family,
            "passes": self.passes, "labeled": self.labeled, "passed": self.passed,
            "rung0_clean": self.clean, "measured": self.measured,
            "median_tokens": self.median_tokens, "median_wall_clock_s": self.median_wall_clock_s,
            "trials": self.trials, "promotable": self.promotable, "promoted": self.promoted,
            "engagements": sorted(self.engagements),
        }


_PROMOTED = re.compile(r"^\s*promoted:\s*\S", re.MULTILINE)


def _named_in_findings(eng: Engagement) -> set[str]:
    """Pass ids that any rung-0 finding names — the complement is the clean count."""
    named: set[str] = set()
    ids = [r.pass_id for r in eng.records]
    for check in run_checks(eng):
        for finding in check.findings:
            for pid in ids:
                if re.search(rf"\b{re.escape(pid)}\b", finding):
                    named.add(pid)
    return named


def _cell_for(eng: Engagement, r: Record, named: set[str]) -> Cell:
    c = Cell(runtime=r.runtime or "—", seat=r.seat or "—", passes=1)
    c.engagements.add(str(eng.brief.get("id") or eng.root.name))
    label = eng.labels.get(r.pass_id)
    if label is not None and label.verdict in ("pass", "fail"):
        c.labeled = 1
        c.passed = 1 if label.verdict == "pass" else 0
    if r.pass_id not in named:
        c.clean = 1
    fields, bad = normalize_meter(r.meter)
    # a count from a source the registry does not name is not a measurement — rung 0 already flags the record
    registered = r.meter_source in METER_SOURCES and r.meter_source != "UNMEASURED"
    if registered and not bad and "total" in fields:
        c.measured = 1
        c.tokens.append(int(fields["total"]))
    if r.wall_clock_s is not None and registered:
        c.wall_clock.append(int(r.wall_clock_s))
    if r.kind == "trial":
        c.trials = 1
        base = eng.labels.get(r.shadow_of or "")
        if label is not None and label.verdict == "pass" and base is not None and base.verdict == "fail":
            c.promotable = 1
        if _PROMOTED.search(r.notes or ""):
            c.promoted = 1
    return c


def numbers_for(engagements: Iterable[Engagement]) -> tuple[list[Cell], list[Cell]]:
    """Per-runtime roll-ups and per runtime × seat cells, both sorted, across the engagements given."""
    by_pair: dict[tuple[str, str], Cell] = {}
    for eng in engagements:
        named = _named_in_findings(eng)
        for r in eng.records:
            c = _cell_for(eng, r, named)
            key = (c.runtime, c.seat)
            if key not in by_pair:
                by_pair[key] = Cell(runtime=c.runtime, seat=c.seat)
            by_pair[key].add(c)
    per_pair = [by_pair[k] for k in sorted(by_pair)]
    by_runtime: dict[str, Cell] = defaultdict(lambda: Cell(runtime=""))
    for c in per_pair:
        if not by_runtime[c.runtime].runtime:
            by_runtime[c.runtime].runtime = c.runtime
        by_runtime[c.runtime].add(c)
    per_runtime = [by_runtime[k] for k in sorted(by_runtime)]
    return per_runtime, per_pair


def numbers(paths: Iterable[Path]) -> tuple[list[Cell], list[Cell]]:
    return numbers_for(load_engagement(Path(p)) for p in paths)


def _n_of(n: int, of: int) -> str:
    return f"{n} of {of}" if of else "—"


def _num(v: Optional[int]) -> str:
    return f"{v:,}" if v is not None else "—"


def render_markdown(per_runtime: list[Cell], per_pair: list[Cell], engagement_ids: Optional[list[str]] = None) -> str:
    """The two tables the registry's § Numbers section holds, counts only."""
    ids = engagement_ids or sorted({e for c in per_runtime for e in c.engagements})
    out = [f"Engagements read: {', '.join(ids) if ids else 'none'}. Counts, never percentages; medians over measured passes only.", ""]
    out.append("| Runtime | Passes | Labeled pass | Rung-0 clean | Measured | Median tokens | Median wall-clock (s) | Trials | Promotable | Promoted |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for c in per_runtime:
        out.append(
            f"| `{c.runtime}` | {c.passes} | {_n_of(c.passed, c.labeled)} | {_n_of(c.clean, c.passes)} | "
            f"{_n_of(c.measured, c.passes)} | {_num(c.median_tokens)} | {_num(c.median_wall_clock_s)} | "
            f"{c.trials} | {c.promotable} | {c.promoted} |"
        )
    out.append("")
    out.append("| Runtime | Seat | Family | Passes | Labeled pass | Rung-0 clean | Measured | Median tokens | Median wall-clock (s) | Trials | Promoted |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    for c in per_pair:
        out.append(
            f"| `{c.runtime}` | {c.seat} | {c.family} | {c.passes} | {_n_of(c.passed, c.labeled)} | "
            f"{_n_of(c.clean, c.passes)} | {_n_of(c.measured, c.passes)} | {_num(c.median_tokens)} | "
            f"{_num(c.median_wall_clock_s)} | {c.trials} | {c.promoted} |"
        )
    return "\n".join(out) + "\n"
