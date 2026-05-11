"""Mutation guard - pre-write diff validator for skill_optimizer.

Enforces autoresearch hard constraints + per-iteration mutation policy:
  * No edits to protected line ranges (frontmatter, example outputs)
  * No edits to protected section headings (References, Related Skills, etc.)
  * No whitespace-only diffs (gaming the iteration counter)
  * No headings introduced that match a criterion ID verbatim (anti-gaming)
"""
from __future__ import annotations

import difflib
import re
from typing import Iterable, Sequence


class MutationRejected(Exception):
    """Raised when a proposed mutation violates policy."""


def _stripped_diff(orig: Sequence[str], mod: Sequence[str]) -> list[tuple[str, int, int, str, str]]:
    """Return non-equal opcodes from SequenceMatcher: (op, i1, i2, orig_chunk, mod_chunk)."""
    matcher = difflib.SequenceMatcher(a=orig, b=mod, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            continue
        out.append((op, i1, i2, "".join(orig[i1:i2]), "".join(mod[j1:j2])))
    return out


def _line_in_any_range(line_num: int, ranges: Iterable[tuple[int, int]]) -> bool:
    """1-indexed line number; ranges are inclusive."""
    return any(lo <= line_num <= hi for (lo, hi) in ranges if hi >= lo)


def _section_for_line(lines: Sequence[str], line_num: int) -> str | None:
    """Walk back from line_num (1-indexed) to find the most recent ## or ### heading."""
    heading_re = re.compile(r"^#{2,4}\s+(.*?)\s*$")
    for i in range(min(line_num - 1, len(lines) - 1), -1, -1):
        m = heading_re.match(lines[i])
        if m:
            return m.group(1).strip()
    return None


def validate_mutation(
    original_lines: Sequence[str],
    modified_lines: Sequence[str],
    protected_line_ranges: list[tuple[int, int]],
    protected_section_headings: tuple[str, ...],
    criterion_ids: tuple[str, ...],
) -> tuple[bool, str]:
    """Return (passed, reason). passed=True means the mutation is allowed."""
    if original_lines == modified_lines:
        return False, "diff is empty (no changes)"

    # Whitespace-only check: compare with whitespace stripped.
    orig_stripped = "".join(original_lines).replace(" ", "").replace("\t", "")
    mod_stripped = "".join(modified_lines).replace(" ", "").replace("\t", "")
    if orig_stripped == mod_stripped:
        return False, "whitespace-only diff (rejected as gaming the iteration counter)"

    diff_ops = _stripped_diff(original_lines, modified_lines)
    if not diff_ops:
        return False, "diff is empty after normalization"

    # Check each changed hunk for protected-range violations.
    for op, i1, i2, orig_chunk, mod_chunk in diff_ops:
        for line_num_zero in range(i1, max(i1 + 1, i2)):
            line_num = line_num_zero + 1  # 1-indexed
            if _line_in_any_range(line_num, protected_line_ranges):
                return False, f"diff touches protected line range (line {line_num})"
            section = _section_for_line(original_lines, line_num)
            if section and section in protected_section_headings:
                return False, f"diff touches protected section {section!r}"

    # Anti-gaming: any new heading whose text matches a criterion ID verbatim?
    new_headings = re.findall(r"^#{2,4}\s+(.*?)\s*$", "".join(modified_lines), re.MULTILINE)
    old_headings = set(re.findall(r"^#{2,4}\s+(.*?)\s*$", "".join(original_lines), re.MULTILINE))
    introduced = [h for h in new_headings if h not in old_headings]
    for h in introduced:
        if h.strip() in criterion_ids:
            return False, f"introduced heading {h!r} matches criterion id (anti-gaming guard)"

    return True, "ok"
