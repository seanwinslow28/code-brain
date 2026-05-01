"""Typed reasoning edges helper — Phase D (v3.20.0, 2026-05-01).

Wraps the `concept_edges` SQLite table created by vault_indexer.init_db().
Pure stdlib so any caller can use it without dragging the synthesizer's
dependency tree.

Producer side: vault_synthesizer parses the LLM's typed `relations` per
connection article and calls insert_edge() inside the existing FileLock
window on vault/knowledge/.lock.

Consumer side: knowledge_lint Tier 2 calls find_contradictions() as a
zero-LLM-cost fast path, then deduplicates the LLM contradictions pass
against the SQL hits.

Origin: OB1's `schemas/typed-reasoning-edges/schema.sql` provides the
six-relation taxonomy. Sean's vault uses kebab-case slugs as identifiers
(stable enough for a personal vault; UUIDs would be overkill).
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

ALLOWED_RELATIONS: tuple[str, ...] = (
    "supports",
    "contradicts",
    "evolved_into",
    "supersedes",
    "depends_on",
    "related_to",
)


def get_connection(db_path: Path) -> sqlite3.Connection:
    """Open a connection and apply init_db() so the schema exists.

    Idempotent — `CREATE TABLE IF NOT EXISTS` makes a second call a no-op.
    Imported lazily to avoid a circular import (vault_indexer → concept_edges).
    """
    # Lazy import: vault_indexer.init_db owns the canonical schema for both
    # `chunks` and `concept_edges`. Importing here prevents a circular at
    # module load time when vault_indexer also wants to call concept_edges
    # helpers in the future.
    from agents.vault_indexer import init_db
    return init_db(db_path)


def _now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def insert_edge(
    conn: sqlite3.Connection,
    *,
    from_slug: str,
    to_slug: str,
    relation: str,
    source_synth_run: str,
    confidence: float | None = None,
    classifier_version: str | None = None,
    valid_until: str | None = None,
    created_at: str | None = None,
) -> bool:
    """INSERT OR IGNORE one edge row.

    Returns True on a real insert, False on UNIQUE-violation no-op.

    Raises ValueError when:
      - `relation` is not in ALLOWED_RELATIONS (caught before SQL so the
        caller can log without a stack trace from sqlite3.IntegrityError)
      - `from_slug == to_slug` (CHECK constraint would reject anyway)
      - `confidence` is outside [0, 1]
    The synthesizer wraps these so a bad relation drops the edge but never
    aborts the synthesis run.
    """
    if relation not in ALLOWED_RELATIONS:
        raise ValueError(
            f"invalid relation {relation!r}; allowed: {ALLOWED_RELATIONS}"
        )
    if from_slug == to_slug:
        raise ValueError(f"from_slug == to_slug ({from_slug!r}); self-edges rejected")
    if confidence is not None and not (0.0 <= confidence <= 1.0):
        raise ValueError(f"confidence {confidence!r} outside [0, 1]")

    created = created_at or _now_iso()
    try:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO concept_edges (
                from_slug, to_slug, relation, confidence,
                valid_until, classifier_version,
                source_synth_run, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                from_slug,
                to_slug,
                relation,
                confidence,
                valid_until,
                classifier_version,
                source_synth_run,
                created,
            ),
        )
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.IntegrityError as exc:
        # CHECK constraint backstop — should be unreachable given the guards
        # above, but if the schema gains a new constraint we surface the
        # offending value cleanly.
        raise ValueError(f"integrity error inserting edge: {exc}") from exc


def find_contradictions(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """All currently-valid contradictions as (from_slug, to_slug) pairs.

    Filters on `valid_until IS NULL` so superseded edges drop out. Returns
    [] when the table is empty (or, depending on init order, missing — the
    caller should `get_connection` first to guarantee the table exists).
    """
    cur = conn.execute(
        "SELECT from_slug, to_slug FROM concept_edges "
        "WHERE relation = 'contradicts' AND valid_until IS NULL "
        "ORDER BY from_slug, to_slug"
    )
    return [(row[0], row[1]) for row in cur.fetchall()]


def find_superseded(conn: sqlite3.Connection, slug: str) -> list[str]:
    """Slugs that supersede `slug` via relation='supersedes'.

    Reads the edges where this slug is the `from_slug` (i.e. "this concept
    has been superseded by these other ones"). Currently-valid only.
    """
    cur = conn.execute(
        "SELECT to_slug FROM concept_edges "
        "WHERE relation = 'supersedes' AND from_slug = ? "
        "AND valid_until IS NULL "
        "ORDER BY to_slug",
        (slug,),
    )
    return [row[0] for row in cur.fetchall()]


def decay_pass(
    conn: sqlite3.Connection,
    *,
    now_iso: str,
    half_life_days: int = 90,
) -> int:
    """Stamp `valid_until` on edges older than half_life_days when a newer
    `supersedes` edge exists for the same from_slug.

    Stubbed for Phase D — the full decay rule needs production telemetry
    before we tune half_life_days. Exposed here so future callers (a
    future synth-tail job, perhaps) can wire it without another rev.
    Returns 0 today.
    """
    # Intentionally a no-op until we have data to tune the decay rule.
    # Not raising NotImplementedError because callers may wire it
    # speculatively; returning 0 keeps that path quiet.
    _ = (conn, now_iso, half_life_days)
    return 0
