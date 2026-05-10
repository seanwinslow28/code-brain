"""Tests for mutation_guard module."""
import pytest
from lib.skill_optimizer.mutation_guard import (
    validate_mutation,
    MutationRejected,
)

PROTECTED_LINE_RANGES = [(1, 4), (23, 69)]
PROTECTED_SECTION_HEADINGS = ("References", "Related Skills", "Copy/Paste Ready")
CRITERION_IDS = (
    "substack_format_intro",
    "anti_pattern_overreference",
    "stylometric_distance",
    "signature_move_present",
    "sounds_like_sean",
    "no_anti_pattern_violation",
)


class TestValidateMutation:
    def test_accepts_valid_single_section_edit(self):
        original = "## Section A\nold body line one\nold body line two\n## Section B\nbody\n"
        modified = "## Section A\nnew body line one with substantive change here\nnew body line two as well now\n## Section B\nbody\n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[(1, 0)],  # no protected lines for this test
            protected_section_headings=(),
            criterion_ids=(),
        )
        assert ok, reason

    def test_rejects_change_to_protected_lines(self):
        original = ["line 1\n", "line 2\n", "line 3\n", "line 4\n", "line 5\n"]
        modified = ["line 1 EDITED\n", "line 2\n", "line 3\n", "line 4\n", "line 5\n"]
        ok, reason = validate_mutation(
            original_lines=original,
            modified_lines=modified,
            protected_line_ranges=[(1, 4)],
            protected_section_headings=(),
            criterion_ids=(),
        )
        assert not ok
        assert "protected line range" in reason.lower()

    def test_rejects_change_under_protected_section(self):
        original = "## Section A\nbody\n## References\noriginal refs\n"
        modified = "## Section A\nbody\n## References\nedited refs body now\n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[],
            protected_section_headings=("References",),
            criterion_ids=(),
        )
        assert not ok
        assert "protected section" in reason.lower()

    def test_rejects_whitespace_only_diff(self):
        original = "## Section A\nline one\n"
        modified = "## Section A\nline one  \n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[],
            protected_section_headings=(),
            criterion_ids=(),
        )
        assert not ok
        assert "whitespace" in reason.lower()

    def test_rejects_heading_matching_criterion_id(self):
        original = "## Old Heading\nbody line one\n"
        modified = "## sounds_like_sean\nbody line one\n"
        ok, reason = validate_mutation(
            original_lines=original.splitlines(keepends=True),
            modified_lines=modified.splitlines(keepends=True),
            protected_line_ranges=[],
            protected_section_headings=(),
            criterion_ids=("sounds_like_sean",),
        )
        assert not ok
        assert "criterion id" in reason.lower()
