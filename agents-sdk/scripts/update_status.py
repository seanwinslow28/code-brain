#!/usr/bin/env python3
"""Mutate job_postings.status from the CLI.

Usage:
    python3 scripts/update_status.py <db_id> <new|reviewed|applied|passed>
    python3 scripts/update_status.py 47 applied
    python3 scripts/update_status.py 47 applied --db /custom/path.db
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.job_db import JobDB


def main() -> int:
    parser = argparse.ArgumentParser(description="Update job posting status.")
    parser.add_argument("db_id", type=int, help="Numeric id from the daily roll-up")
    parser.add_argument("status", choices=["new", "reviewed", "applied", "passed"])
    parser.add_argument("--db", help="Override DB path (default: from config.toml)")
    args = parser.parse_args()

    if args.db:
        db_path = Path(args.db)
    else:
        config = load_config()
        db_path = config.repo_root / config.agents["job_feed"]["paths"]["db"]

    if not db_path.exists():
        print(f"DB not found: {db_path}", file=sys.stderr)
        return 1

    # Pre-check: does the row exist? (Resolves Task 10 review note re: silent no-op.)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("SELECT 1 FROM job_postings WHERE id=?", (args.db_id,)).fetchone()
    if row is None:
        print(f"No row found for db_id={args.db_id}", file=sys.stderr)
        return 1

    db = JobDB(db_path)
    try:
        db.update_status(args.db_id, args.status)
    except ValueError as e:
        print(f"Invalid status: {e}", file=sys.stderr)
        return 2

    print(f"OK — id={args.db_id} status={args.status}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
