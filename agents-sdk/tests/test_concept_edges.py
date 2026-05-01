"""Tests for lib.concept_edges + vault_indexer init_db Phase D extension."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from agents.vault_indexer import init_db
from lib import concept_edges


# ─── helpers ──────────────────────────────────────────────────────────────


def _open(tmp_path: Path) -> sqlite3.Connection:
    """Open a fresh DB with the Phase D schema applied."""
    return init_db(tmp_path / "test-index.db")


def _populate_chunks(conn: sqlite3.Connection) -> None:
    """Seed the existing chunks table so we can prove migration is non-destructive."""
    conn.execute(
        "INSERT INTO chunks (file_path, chunk_index, chunk_text, embedding, "
        "file_mtime, indexed_at) VALUES (?, ?, ?, ?, ?, ?)",
        ("notes/foo.md", 0, "hello", None, 1714521600.0, "2026-05-01"),
    )
    conn.execute(
        "INSERT INTO chunks (file_path, chunk_index, chunk_text, embedding, "
        "file_mtime, indexed_at) VALUES (?, ?, ?, ?, ?, ?)",
        ("notes/bar.md", 0, "world", None, 1714521700.0, "2026-05-01"),
    )
    conn.commit()


# ─── schema migration ─────────────────────────────────────────────────────


def test_init_db_creates_concept_edges_table(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        row = conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='concept_edges'"
        ).fetchone()
        assert row is not None
    finally:
        conn.close()


def test_init_db_idempotent_preserves_chunks(tmp_path: Path) -> None:
    """Phase D watchpoint: a second init_db on a populated chunks table
    must not corrupt or drop existing chunk rows."""
    db_path = tmp_path / "idem.db"
    conn = init_db(db_path)
    _populate_chunks(conn)
    conn.close()

    # Second invocation — should be a no-op for existing tables.
    conn2 = init_db(db_path)
    try:
        chunks_count = conn2.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        assert chunks_count == 2
        edges_table = conn2.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='concept_edges'"
        ).fetchone()
        assert edges_table is not None
    finally:
        conn2.close()


def test_concept_edges_indexes_present(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        index_names = {
            row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='index' AND tbl_name='concept_edges'"
            ).fetchall()
        }
    finally:
        conn.close()
    expected = {
        "idx_concept_edges_relation",
        "idx_concept_edges_from",
        "idx_concept_edges_current",
    }
    assert expected.issubset(index_names)


# ─── insert_edge happy path + uniqueness ──────────────────────────────────


def test_insert_edge_happy_path(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        ok = concept_edges.insert_edge(
            conn,
            from_slug="alpha",
            to_slug="beta",
            relation="contradicts",
            source_synth_run="2026-05-01T00:00:00",
            confidence=0.85,
            classifier_version="qwen3-14b/2026-05-01",
        )
        assert ok is True
        row = conn.execute(
            "SELECT from_slug, to_slug, relation, confidence, classifier_version "
            "FROM concept_edges"
        ).fetchone()
        assert row == ("alpha", "beta", "contradicts", 0.85, "qwen3-14b/2026-05-01")
    finally:
        conn.close()


def test_insert_edge_unique_returns_false_on_duplicate(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        first = concept_edges.insert_edge(
            conn,
            from_slug="alpha",
            to_slug="beta",
            relation="contradicts",
            source_synth_run="2026-05-01T00:00:00",
        )
        second = concept_edges.insert_edge(
            conn,
            from_slug="alpha",
            to_slug="beta",
            relation="contradicts",
            source_synth_run="2026-05-01T01:00:00",  # different run, same edge
        )
        assert first is True
        assert second is False
        count = conn.execute("SELECT COUNT(*) FROM concept_edges").fetchone()[0]
        assert count == 1
    finally:
        conn.close()


# ─── invalid input handling ───────────────────────────────────────────────


def test_insert_edge_invalid_relation_raises(tmp_path: Path) -> None:
    """Phase D watchpoint: bad relation values are caught BEFORE SQL so
    the synthesizer can log + drop without aborting the run."""
    conn = _open(tmp_path)
    try:
        with pytest.raises(ValueError, match="invalid relation"):
            concept_edges.insert_edge(
                conn,
                from_slug="alpha",
                to_slug="beta",
                relation="nope-not-a-real-relation",
                source_synth_run="2026-05-01T00:00:00",
            )
        # No row was written.
        count = conn.execute("SELECT COUNT(*) FROM concept_edges").fetchone()[0]
        assert count == 0
    finally:
        conn.close()


def test_insert_edge_self_edge_raises(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        with pytest.raises(ValueError, match="self-edges rejected"):
            concept_edges.insert_edge(
                conn,
                from_slug="alpha",
                to_slug="alpha",
                relation="related_to",
                source_synth_run="2026-05-01T00:00:00",
            )
    finally:
        conn.close()


def test_insert_edge_confidence_out_of_range_raises(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        with pytest.raises(ValueError, match="confidence"):
            concept_edges.insert_edge(
                conn,
                from_slug="alpha",
                to_slug="beta",
                relation="supports",
                source_synth_run="2026-05-01T00:00:00",
                confidence=1.5,
            )
    finally:
        conn.close()


# ─── query helpers ────────────────────────────────────────────────────────


def test_find_contradictions_filters_valid_until_null(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        concept_edges.insert_edge(
            conn,
            from_slug="alpha",
            to_slug="beta",
            relation="contradicts",
            source_synth_run="2026-05-01T00:00:00",
        )
        concept_edges.insert_edge(
            conn,
            from_slug="gamma",
            to_slug="delta",
            relation="contradicts",
            source_synth_run="2026-05-01T00:00:00",
            valid_until="2026-05-15",  # superseded — should NOT surface
        )
        # A non-contradiction edge — must not appear.
        concept_edges.insert_edge(
            conn,
            from_slug="alpha",
            to_slug="gamma",
            relation="supports",
            source_synth_run="2026-05-01T00:00:00",
        )
        contradictions = concept_edges.find_contradictions(conn)
        assert contradictions == [("alpha", "beta")]
    finally:
        conn.close()


def test_find_contradictions_fan_out(tmp_path: Path) -> None:
    """One concept contradicting three others → three rows surface."""
    conn = _open(tmp_path)
    try:
        for target in ("beta", "gamma", "delta"):
            concept_edges.insert_edge(
                conn,
                from_slug="alpha",
                to_slug=target,
                relation="contradicts",
                source_synth_run="2026-05-01T00:00:00",
            )
        contradictions = concept_edges.find_contradictions(conn)
        assert len(contradictions) == 3
        assert all(c[0] == "alpha" for c in contradictions)
        assert {c[1] for c in contradictions} == {"beta", "gamma", "delta"}
    finally:
        conn.close()


def test_find_superseded_returns_supersessor_slugs(tmp_path: Path) -> None:
    conn = _open(tmp_path)
    try:
        concept_edges.insert_edge(
            conn,
            from_slug="old-pattern",
            to_slug="new-pattern",
            relation="supersedes",
            source_synth_run="2026-05-01T00:00:00",
        )
        concept_edges.insert_edge(
            conn,
            from_slug="old-pattern",
            to_slug="newer-pattern",
            relation="supersedes",
            source_synth_run="2026-05-01T00:00:00",
        )
        # Unrelated edge — must not appear.
        concept_edges.insert_edge(
            conn,
            from_slug="other",
            to_slug="thing",
            relation="related_to",
            source_synth_run="2026-05-01T00:00:00",
        )
        result = concept_edges.find_superseded(conn, "old-pattern")
        assert result == ["new-pattern", "newer-pattern"]
    finally:
        conn.close()


def test_decay_pass_is_a_noop_in_phase_d(tmp_path: Path) -> None:
    """Stub returns 0; documented as reserved for future tuning."""
    conn = _open(tmp_path)
    try:
        result = concept_edges.decay_pass(
            conn, now_iso="2026-05-01T00:00:00", half_life_days=90
        )
        assert result == 0
    finally:
        conn.close()


def test_get_connection_idempotent(tmp_path: Path) -> None:
    """Calling get_connection twice on the same path doesn't double-init."""
    db_path = tmp_path / "idem.db"
    conn1 = concept_edges.get_connection(db_path)
    concept_edges.insert_edge(
        conn1,
        from_slug="a",
        to_slug="b",
        relation="contradicts",
        source_synth_run="2026-05-01T00:00:00",
    )
    conn1.close()

    conn2 = concept_edges.get_connection(db_path)
    try:
        rows = concept_edges.find_contradictions(conn2)
        assert rows == [("a", "b")]
    finally:
        conn2.close()
