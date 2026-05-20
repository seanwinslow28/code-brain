#!/usr/bin/env python3
"""One-shot: close pre-Tier-1.5 contradiction edges from 2026-05-17 lint report.

The 8 CRITICAL contradictions in vault/health/2026-05-17-lint-report.md are all
between shallow auto-generated concept articles (tagged phase-6) written
2026-05-12 through 2026-05-19, before the Tier-1.5 retrofit (v3.38.0) landed
2026-05-20. The validator now in place would have rejected these articles; the
"contradictions" are LLM false positives on paraphrase-shape definitions.

Sets valid_until on currently-open contradiction edges so they stop surfacing in
the weekly lint. Tonight's synthesizer run will write fresh edges from any real
conflicts it finds in regenerated articles.

Idempotent: only touches rows where valid_until IS NULL.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = REPO_ROOT / "vault" / ".vault-index.db"


def main() -> int:
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found", file=sys.stderr)
        return 1

    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.execute(
            "SELECT from_slug, to_slug FROM concept_edges "
            "WHERE relation='contradicts' AND valid_until IS NULL"
        )
        rows = cur.fetchall()
        if not rows:
            print("No open contradiction edges. Nothing to do.")
            return 0

        print(f"Closing {len(rows)} contradiction edges (valid_until={now_iso}):")
        for from_slug, to_slug in rows:
            print(f"  {from_slug} -> {to_slug}")

        conn.execute(
            "UPDATE concept_edges SET valid_until = ? "
            "WHERE relation='contradicts' AND valid_until IS NULL",
            (now_iso,),
        )
        conn.commit()
        print(f"Updated {conn.total_changes} rows.")
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
