#!/usr/bin/env python3
"""Unit tests for the Content Machine retirement scanner."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from check_runtime_retirements import RegistryError, scan_registry


REGISTRY = """\
version = 1

[[retirement]]
id = "old-route"
name = "Old route"
source = "https://example.test/decision"
scan_paths = ["live"]

[[retirement.pattern]]
literal = "run the old route"
reason = "The new route replaced it."

[[retirement.allow]]
path = "live/history.md"
line_contains = "Historical only: run the old route"
reason = "Explicit archaeology."
"""


class RuntimeRetirementScannerTests(unittest.TestCase):
    def _repo(self) -> tuple[tempfile.TemporaryDirectory, Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        registry = root / "runtime-retirements.toml"
        registry.write_text(REGISTRY, encoding="utf-8")
        (root / "live").mkdir()
        return temporary, root, registry

    def test_clean_when_only_declared_history_mentions_retirement(self) -> None:
        temporary, root, registry = self._repo()
        self.addCleanup(temporary.cleanup)
        (root / "live" / "history.md").write_text(
            "Historical only: run the old route\n", encoding="utf-8"
        )

        result = scan_registry(root, registry)

        self.assertTrue(result.clean)
        self.assertEqual(result.files_scanned, 1)

    def test_reports_active_retired_instruction_without_copying_its_line(self) -> None:
        temporary, root, registry = self._repo()
        self.addCleanup(temporary.cleanup)
        (root / "live" / "runtime.md").write_text(
            "Always run the old route with private payload 123.\n", encoding="utf-8"
        )

        result = scan_registry(root, registry)

        self.assertFalse(result.clean)
        self.assertEqual(len(result.findings), 1)
        finding = result.findings[0]
        self.assertEqual(finding.path, "live/runtime.md")
        self.assertEqual(finding.line, 1)
        self.assertEqual(finding.pattern, "run the old route")
        self.assertNotIn("private payload", repr(finding))

    def test_missing_scan_path_is_an_error_not_a_silent_pass(self) -> None:
        temporary, root, registry = self._repo()
        self.addCleanup(temporary.cleanup)
        (root / "live").rmdir()

        with self.assertRaisesRegex(RegistryError, "scan path does not exist"):
            scan_registry(root, registry)


if __name__ == "__main__":
    unittest.main()
