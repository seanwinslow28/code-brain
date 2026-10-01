"""labels.md — Sean's judgment, kept apart from the run's facts (#272 decision 6).

One file per engagement, one markdown table, rows keyed by pass id. The
viewer's *Copy label rows* exports rows in exactly this column order, so a
pasted block is a valid file body. `verdict` is pass or fail, nothing between —
except `defer` (ratified 2026-09-25, DESIGN.md §15): a recorded "come back to
this", which is not a verdict. A deferred row still waits, never reveals a blind
pair, and is never counted as labeled.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

__all__ = ["COLUMNS", "DECIDED", "Label", "LabelsError", "parse_labels", "format_rows", "decided"]

COLUMNS = ("pass", "verdict", "first_failing_stage", "critique", "failure_code")
DECIDED = ("pass", "fail")   # the two verdicts; "defer" is a recorded non-verdict


def decided(verdict: Optional[str]) -> bool:
    """True only for a pass or a fail. A defer or an empty cell is a row that still waits."""
    return verdict in DECIDED


class LabelsError(ValueError):
    """The labels table is malformed."""


@dataclass(frozen=True)
class Label:
    pass_id: str
    verdict: Optional[str]              # "pass" | "fail" | "defer" (come back to it) | None (row present, no verdict yet)
    first_failing_stage: Optional[int]  # set on a fail; may be upstream of the pass read
    critique: str
    failure_code: str


_ESCAPED_PIPE = "\x00PIPE\x00"


def _split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells = line.replace("\\|", _ESCAPED_PIPE).split("|")
    return [c.replace(_ESCAPED_PIPE, "|").strip() for c in cells]


def parse_labels(text: str, stages: Optional[list[int]] = None) -> dict[str, Label]:
    """Return {pass_id: Label} for the first table whose header is COLUMNS.

    A file with no table (labels not started) yields {}. A table with the
    wrong header, an unknown verdict, a fail without its first failing stage,
    or a duplicated pass id raises LabelsError naming the row.
    """
    allowed = sorted(stages) if stages else list(range(0, 8))   # Productcraft's 0–7 when no studio is named
    lines = text.split("\n")
    out: dict[str, Label] = {}
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            header = tuple(c.lower() for c in _split_row(lines[i]))
            if header != COLUMNS:
                raise LabelsError(
                    f"labels table header must be | {' | '.join(COLUMNS)} |, got | {' | '.join(header)} |"
                )
            i += 1
            if i < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i]):
                i += 1
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = _split_row(lines[i])
                if len(cells) != len(COLUMNS):
                    raise LabelsError(f"row {lines[i].strip()!r} has {len(cells)} cells, expected {len(COLUMNS)}")
                pid, verdict, ffs, critique, code = cells
                if not pid:
                    raise LabelsError(f"row {lines[i].strip()!r} has no pass id")
                if pid in out:
                    raise LabelsError(f"pass {pid} appears twice in the labels file")
                v: Optional[str] = verdict.lower() or None
                if v not in (None, "pass", "fail", "defer"):
                    raise LabelsError(f"{pid}: verdict must be pass or fail (or defer, to come back to it), nothing between; got {verdict!r}")
                stage: Optional[int] = None
                if ffs:
                    if not re.fullmatch(r"-?\d+", ffs) or int(ffs) not in allowed:
                        raise LabelsError(
                            f"{pid}: first_failing_stage must be a stage number {allowed[0]}–{allowed[-1]}, got {ffs!r}"
                        )
                    stage = int(ffs)
                if v == "fail" and stage is None:
                    raise LabelsError(f"{pid}: a fail must name its first failing stage")
                out[pid] = Label(pid, v, stage, critique, code)
                i += 1
            return out
        i += 1
    return out


def format_rows(labels: list[Label]) -> str:
    """Render rows (no header) in the file's column order, pipes escaped."""
    def cell(s: object) -> str:
        return str("" if s is None else s).replace("|", "\\|").replace("\n", " ")
    return "\n".join(
        f"| {cell(l.pass_id)} | {cell(l.verdict)} | {cell(l.first_failing_stage)} | {cell(l.critique)} | {cell(l.failure_code)} |"
        for l in labels
    )
