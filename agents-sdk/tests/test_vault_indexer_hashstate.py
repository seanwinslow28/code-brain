"""Tests for vault_indexer hash-state tracking + daily exclusion (D.2.a)."""

from __future__ import annotations

from pathlib import Path

from agents.vault_indexer import (
    compute_file_hash,
    detect_changed_files,
    discover_vault_files,
    read_indexer_state,
    write_indexer_state,
)


def _touch(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_compute_file_hash_stable(tmp_path: Path) -> None:
    f = tmp_path / "x.md"
    _touch(f, "hello")
    h1 = compute_file_hash(f)
    h2 = compute_file_hash(f)
    assert h1 == h2
    assert len(h1) == 64  # sha256 hex


def test_compute_file_hash_differs_on_content_change(tmp_path: Path) -> None:
    f = tmp_path / "x.md"
    _touch(f, "hello")
    h1 = compute_file_hash(f)
    _touch(f, "goodbye")
    h2 = compute_file_hash(f)
    assert h1 != h2


def test_read_indexer_state_missing_returns_empty(tmp_path: Path) -> None:
    state = read_indexer_state(tmp_path / "missing.json")
    assert state == {}


def test_write_read_indexer_state_roundtrip(tmp_path: Path) -> None:
    state_path = tmp_path / ".indexer-state.json"
    state = {"a.md": {"hash": "abc", "indexed_at": "2026-04-17T10:00:00"}}
    write_indexer_state(state_path, state)
    back = read_indexer_state(state_path)
    assert back == state


def test_discover_excludes_daily(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    _touch(vault / "kept.md", "kept")
    _touch(vault / "daily" / "2026-04-17.md", "daily log")
    _touch(vault / "daily" / "2026-04-16.md", "old daily")
    _touch(vault / "knowledge" / "concepts" / "c.md", "concept")
    _touch(vault / ".obsidian" / "cfg.json", "{}")

    found = {p.relative_to(vault).as_posix() for p in discover_vault_files(vault)}
    assert "kept.md" in found
    assert "knowledge/concepts/c.md" in found
    assert all("daily" not in p for p in found), f"daily leaked in: {found}"
    assert all(".obsidian" not in p for p in found)


def test_detect_changed_files_sees_new_and_modified(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    a = vault / "a.md"
    b = vault / "b.md"
    _touch(a, "one")
    _touch(b, "two")

    # First run: both are new
    state = {}
    changed, new_state = detect_changed_files(vault, state)
    changed_rel = sorted(p.relative_to(vault).as_posix() for p in changed)
    assert changed_rel == ["a.md", "b.md"]
    assert "a.md" in new_state and "b.md" in new_state

    # Second run with same state: no changes
    changed2, state2 = detect_changed_files(vault, new_state)
    assert changed2 == []
    assert state2 == new_state

    # Modify b.md and add c.md
    _touch(b, "two-modified")
    c = vault / "c.md"
    _touch(c, "three")
    changed3, state3 = detect_changed_files(vault, new_state)
    changed3_rel = sorted(p.relative_to(vault).as_posix() for p in changed3)
    assert changed3_rel == ["b.md", "c.md"]
    # a.md hash unchanged but still tracked
    assert state3["a.md"]["hash"] == new_state["a.md"]["hash"]


def test_detect_changed_files_removes_deleted(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    a = vault / "a.md"
    _touch(a, "one")
    _, state = detect_changed_files(vault, {})
    assert "a.md" in state

    a.unlink()
    changed, state2 = detect_changed_files(vault, state)
    assert "a.md" not in state2
    assert changed == []
