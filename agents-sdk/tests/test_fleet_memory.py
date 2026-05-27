"""Tests for lib.fleet_memory — shared filesystem-memory layer."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


class TestResolvePathGuard:
    """The path-traversal guard is non-negotiable per CLAUDE.md / synthesis Risk Register."""

    def test_simple_relative_path_resolves_under_mount(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        resolved = _resolve_path(mount, "agent_id/note.md")
        assert resolved == (mount / "agent_id/note.md").resolve()

    def test_dotdot_escape_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "../../etc/passwd")

    def test_absolute_path_outside_mount_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "/etc/passwd")

    def test_symlink_escape_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        outside = tmp_path / "outside"
        outside.mkdir()
        outside_file = outside / "secret.txt"
        outside_file.write_text("nope")
        link = mount / "evil_link"
        link.symlink_to(outside_file)
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "evil_link")

    def test_resolves_to_nonexistent_descendant(self, tmp_path: Path):
        """We must allow paths that don't exist yet (create command), as long
        as they would land under the mount."""
        from lib.fleet_memory import _resolve_path
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        resolved = _resolve_path(mount, "new_agent/new_lesson.md")
        assert str(resolved).startswith(str(mount.resolve()))
        assert not resolved.exists()

    def test_empty_path_raises(self, tmp_path: Path):
        from lib.fleet_memory import _resolve_path, PathEscapeError
        mount = tmp_path / "fleet-memory"
        mount.mkdir()
        with pytest.raises(PathEscapeError):
            _resolve_path(mount, "")
