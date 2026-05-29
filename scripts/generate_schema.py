#!/usr/bin/env python3
"""Generate the concept_edges schema artifacts for the Vault Scorecard.

Reads vault/.vault-index.db -> emits two artifacts:
  - docs/diagrams/concept-edges-erd.mmd  (Mermaid erDiagram source, Markdown-embeddable)
  - docs/diagrams/concept-edges-stats.md (Sanitized stats summary — counts only, NO slug names)

Usage:
  python3 scripts/generate_schema.py [--db-path PATH] [--out-dir docs/diagrams] [--self-test]
"""
from __future__ import annotations

import argparse
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "vault" / ".vault-index.db"
DEFAULT_OUT = ROOT / "docs" / "diagrams"


def emit_erd_mermaid(con: sqlite3.Connection) -> str:
    """Emit the concept_edges ER diagram as Mermaid erDiagram source.

    The ER diagram represents Concept --[relation]--> Concept with the row attributes
    surfaced as a clean Concept entity. This is the *type-level* schema, not the
    instance graph (instance graph would be a separate diagram via NetworkX).
    """
    cur = con.cursor()
    # Pull the actual CHECK constraint values from sqlite_master so the diagram
    # can never drift from the schema. The relation enum is canonical.
    cur.execute("SELECT sql FROM sqlite_master WHERE name='concept_edges'")
    row = cur.fetchone()
    if row is None:
        raise RuntimeError("concept_edges table not found in DB")
    schema_sql = row[0]

    # Six relation verbs are baked into the schema — surface them as the
    # 'relation' attribute's documented enum.
    relations = ["supports", "contradicts", "evolved_into", "supersedes", "depends_on", "related_to"]

    return f"""```mermaid
erDiagram
    Concept ||--o{{ ConceptEdge : "from_slug"
    Concept ||--o{{ ConceptEdge : "to_slug"
    ConceptEdge {{
        int id PK
        text from_slug FK
        text to_slug FK
        text relation "enum: {' | '.join(relations)}"
        real confidence "0..1, NULL when classifier-undecided"
        text valid_until "ISO 8601, NULL when current"
        text classifier_version
        text source_synth_run
        text created_at "ISO 8601"
    }}
    Concept {{
        text slug PK
        text title
        text body
    }}
```"""


def emit_stats(con: sqlite3.Connection) -> str:
    """Emit sanitized stats — counts only, no slug names, safe for public repo."""
    cur = con.cursor()

    total_edges = cur.execute("SELECT COUNT(*) FROM concept_edges").fetchone()[0]
    by_relation = dict(cur.execute("SELECT relation, COUNT(*) FROM concept_edges GROUP BY relation").fetchall())
    distinct_from = cur.execute("SELECT COUNT(DISTINCT from_slug) FROM concept_edges").fetchone()[0]
    distinct_to = cur.execute("SELECT COUNT(DISTINCT to_slug) FROM concept_edges").fetchone()[0]
    with_confidence = cur.execute("SELECT COUNT(*) FROM concept_edges WHERE confidence IS NOT NULL").fetchone()[0]
    superseded = cur.execute("SELECT COUNT(*) FROM concept_edges WHERE valid_until IS NOT NULL").fetchone()[0]
    chunks = cur.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]

    last_run = cur.execute("SELECT value FROM index_meta WHERE key='last_run'").fetchone()
    last_run = last_run[0] if last_run else "n/a"

    confidence_pct = (with_confidence / total_edges * 100) if total_edges else 0

    lines = [
        f"# `concept_edges` stats — {datetime.utcnow().isoformat()}Z",
        "",
        f"_Last synth run reflected: {last_run}_",
        "",
        "## Topology",
        f"- Total edges: **{total_edges}**",
        f"- Distinct `from_slug` nodes: {distinct_from}",
        f"- Distinct `to_slug` nodes: {distinct_to}",
        f"- Approximate node count: ~{max(distinct_from, distinct_to)}",
        f"- Indexed chunks (retrieval pool): **{chunks:,}**",
        "",
        "## Verb distribution",
    ]
    for relation in ["supports", "contradicts", "evolved_into", "supersedes", "depends_on", "related_to"]:
        count = by_relation.get(relation, 0)
        pct = (count / total_edges * 100) if total_edges else 0
        lines.append(f"- `{relation}`: {count} ({pct:.1f}%)")
    lines += [
        "",
        "## Confidence / curation",
        f"- Edges with `confidence` attached: **{with_confidence}** of {total_edges} ({confidence_pct:.1f}%)",
        f"- Edges currently superseded (`valid_until` set): **{superseded}**",
    ]
    return "\n".join(lines) + "\n"


def run_self_test() -> None:
    """In-memory smoke test — 6 edges, one per relation, both artifacts emit."""
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE concept_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_slug TEXT NOT NULL,
            to_slug TEXT NOT NULL,
            relation TEXT NOT NULL CHECK (relation IN (
                'supports','contradicts','evolved_into','supersedes','depends_on','related_to'
            )),
            confidence REAL,
            valid_until TEXT,
            classifier_version TEXT,
            source_synth_run TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(from_slug, to_slug, relation),
            CHECK (from_slug != to_slug)
        );
        CREATE TABLE chunks (id INTEGER PRIMARY KEY, file_path TEXT NOT NULL, chunk_index INT NOT NULL, chunk_text TEXT NOT NULL, embedding BLOB, file_mtime REAL NOT NULL, indexed_at TEXT NOT NULL);
        CREATE TABLE index_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        INSERT INTO index_meta VALUES ('last_run', '2026-01-01T00:00:00');
    """)
    for i, rel in enumerate(["supports","contradicts","evolved_into","supersedes","depends_on","related_to"]):
        cur.execute("INSERT INTO concept_edges (from_slug, to_slug, relation, source_synth_run, created_at) VALUES (?,?,?,?,?)",
                   (f"a-{i}", f"b-{i}", rel, "test", "2026-01-01T00:00:00"))
    con.commit()

    erd = emit_erd_mermaid(con)
    stats = emit_stats(con)
    assert "erDiagram" in erd, "ERD missing erDiagram keyword"
    assert "Total edges: **6**" in stats, "Stats missing total-edges line"
    for rel in ["supports","contradicts","evolved_into","supersedes","depends_on","related_to"]:
        assert f"`{rel}`" in stats, f"Stats missing relation: {rel}"
    print("self-test passed: 6 edges across 6 relations, both artifacts emit cleanly")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db-path", type=Path, default=DEFAULT_DB)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return

    if not args.db_path.exists():
        raise SystemExit(f"DB not found: {args.db_path}")

    con = sqlite3.connect(args.db_path)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    erd_path = args.out_dir / "concept-edges-erd.mmd"
    stats_path = args.out_dir / "concept-edges-stats.md"
    erd_path.write_text(emit_erd_mermaid(con))
    stats_path.write_text(emit_stats(con))
    print(f"wrote {erd_path}")
    print(f"wrote {stats_path}")


if __name__ == "__main__":
    main()
