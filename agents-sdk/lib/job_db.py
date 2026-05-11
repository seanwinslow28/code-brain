"""SQLite layer for the job-feed agent.

Single standalone DB at vault/.job-feed.db. All write paths take an exclusive
FileLock on `<db_path>.lock` to serialize writes if multiple launchd fires
ever overlap (shouldn't happen with 30-min spacing, but cheap insurance).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from lib.filelock import FileLock
from lib.job_types import Posting, ScoringResult

DEDUPE_NEW = "new"
DEDUPE_SCORED = "scored"
DEDUPE_CARRYOVER = "carryover"

SCHEMA = """
CREATE TABLE IF NOT EXISTS job_postings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL,
    source_role_id TEXT NOT NULL,
    url TEXT NOT NULL,
    company TEXT NOT NULL,
    title TEXT NOT NULL,
    location TEXT,
    salary_disclosed TEXT,
    posted_at TEXT,
    first_seen_at TEXT NOT NULL,
    description_excerpt TEXT,
    rules_passed INTEGER NOT NULL,
    rules_rejection_reason TEXT,
    fit_score INTEGER,
    role_band TEXT,
    rationale TEXT,
    concerns TEXT,
    fit_dimensions TEXT,
    scored_at TEXT,
    status TEXT DEFAULT 'new',
    UNIQUE(source, source_role_id)
);
CREATE INDEX IF NOT EXISTS idx_first_seen ON job_postings(first_seen_at);
CREATE INDEX IF NOT EXISTS idx_fit_score ON job_postings(fit_score DESC) WHERE fit_score IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_status ON job_postings(status);
CREATE INDEX IF NOT EXISTS idx_unscored ON job_postings(rules_passed, fit_score)
  WHERE rules_passed = 1 AND fit_score IS NULL;
"""


class JobDB:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock_path = self.path.with_suffix(self.path.suffix + ".lock")
        with self._writer() as conn:
            conn.executescript(SCHEMA)

    def _writer(self):
        """Context manager yielding a write-locked connection."""
        class _Ctx:
            def __init__(inner_self):
                inner_self.lock = FileLock(self.lock_path, exclusive=True)
                inner_self.conn = None

            def __enter__(inner_self):
                inner_self.lock.__enter__()
                inner_self.conn = sqlite3.connect(self.path)
                return inner_self.conn

            def __exit__(inner_self, exc_type, exc, tb):
                try:
                    if exc_type is None:
                        inner_self.conn.commit()
                    inner_self.conn.close()
                finally:
                    inner_self.lock.__exit__(exc_type, exc, tb)
        return _Ctx()

    def dedupe_state(self, posting: Posting) -> str:
        with sqlite3.connect(self.path) as conn:
            row = conn.execute(
                "SELECT rules_passed, fit_score FROM job_postings "
                "WHERE source=? AND source_role_id=?",
                (posting.source, posting.source_role_id),
            ).fetchone()
        if row is None:
            return DEDUPE_NEW
        rules_passed, fit_score = row
        if fit_score is not None:
            return DEDUPE_SCORED
        if rules_passed == 1:
            return DEDUPE_CARRYOVER
        # rules_passed=0 with fit_score=NULL → already rejected, treat as scored (don't re-process)
        return DEDUPE_SCORED

    def persist_rejected(self, posting: Posting, reason: str) -> None:
        now = datetime.now().isoformat()
        with self._writer() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO job_postings "
                "(source, source_role_id, url, company, title, location, salary_disclosed, "
                " posted_at, first_seen_at, description_excerpt, rules_passed, rules_rejection_reason) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,0,?)",
                (
                    posting.source, posting.source_role_id, posting.url,
                    posting.company, posting.title, posting.location,
                    posting.salary_disclosed,
                    posting.posted_at.isoformat() if posting.posted_at else None,
                    now,
                    (posting.description or "")[:500],
                    reason,
                ),
            )

    def persist_rules_passed(self, posting: Posting, scored: ScoringResult | None) -> None:
        now = datetime.now().isoformat()
        with self._writer() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO job_postings "
                "(source, source_role_id, url, company, title, location, salary_disclosed, "
                " posted_at, first_seen_at, description_excerpt, rules_passed) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,1)",
                (
                    posting.source, posting.source_role_id, posting.url,
                    posting.company, posting.title, posting.location,
                    posting.salary_disclosed,
                    posting.posted_at.isoformat() if posting.posted_at else None,
                    now,
                    (posting.description or "")[:500],
                ),
            )
            # Inline the score update inside the same lock window to avoid
            # re-entrant FileLock deadlock (fcntl.flock is per-fd, not per-process).
            if scored is not None:
                conn.execute(
                    "UPDATE job_postings SET fit_score=?, role_band=?, rationale=?, "
                    "concerns=?, fit_dimensions=?, scored_at=? "
                    "WHERE source=? AND source_role_id=?",
                    (
                        scored.fit_score, scored.role_band, scored.rationale,
                        json.dumps(scored.concerns), json.dumps(scored.fit_dimensions),
                        datetime.now().isoformat(),
                        posting.source, posting.source_role_id,
                    ),
                )

    def update_score(self, posting: Posting, scored: ScoringResult) -> None:
        with self._writer() as conn:
            conn.execute(
                "UPDATE job_postings SET fit_score=?, role_band=?, rationale=?, "
                "concerns=?, fit_dimensions=?, scored_at=? "
                "WHERE source=? AND source_role_id=?",
                (
                    scored.fit_score, scored.role_band, scored.rationale,
                    json.dumps(scored.concerns), json.dumps(scored.fit_dimensions),
                    datetime.now().isoformat(),
                    posting.source, posting.source_role_id,
                ),
            )

    def unscored_postings(self) -> list[Posting]:
        """All postings with rules_passed=1 AND fit_score IS NULL (the scoring queue)."""
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                "SELECT source, source_role_id, url, company, title, location, "
                "salary_disclosed, posted_at, description_excerpt "
                "FROM job_postings WHERE rules_passed=1 AND fit_score IS NULL"
            ).fetchall()
        return [
            Posting(
                source=r[0], source_role_id=r[1], url=r[2], company=r[3], title=r[4],
                location=r[5], salary_disclosed=r[6],
                posted_at=datetime.fromisoformat(r[7]) if r[7] else None,
                description=r[8] or "",
            )
            for r in rows
        ]

    def scored_today(self, today_iso: str) -> list[tuple[int, Posting, ScoringResult]]:
        """All postings scored on `today_iso` (YYYY-MM-DD), ordered by fit_score desc."""
        with sqlite3.connect(self.path) as conn:
            rows = conn.execute(
                "SELECT id, source, source_role_id, url, company, title, location, "
                "salary_disclosed, posted_at, description_excerpt, "
                "fit_score, role_band, rationale, concerns, fit_dimensions "
                "FROM job_postings "
                "WHERE rules_passed=1 AND fit_score IS NOT NULL "
                "AND date(scored_at)=? "
                "ORDER BY fit_score DESC, scored_at DESC",
                (today_iso,),
            ).fetchall()
        out = []
        for r in rows:
            p = Posting(
                source=r[1], source_role_id=r[2], url=r[3], company=r[4], title=r[5],
                location=r[6], salary_disclosed=r[7],
                posted_at=datetime.fromisoformat(r[8]) if r[8] else None,
                description=r[9] or "",
            )
            s = ScoringResult(
                fit_score=r[10], role_band=r[11] or "", rationale=r[12] or "",
                concerns=json.loads(r[13]) if r[13] else [],
                fit_dimensions=json.loads(r[14]) if r[14] else {},
            )
            out.append((r[0], p, s))
        return out

    def row_id(self, posting: Posting) -> int:
        with sqlite3.connect(self.path) as conn:
            row = conn.execute(
                "SELECT id FROM job_postings WHERE source=? AND source_role_id=?",
                (posting.source, posting.source_role_id),
            ).fetchone()
        if row is None:
            raise KeyError(f"No row for {posting.source}/{posting.source_role_id}")
        return row[0]

    def update_status(self, row_id: int, new_status: str) -> None:
        if new_status not in ("new", "reviewed", "applied", "passed"):
            raise ValueError(f"Invalid status: {new_status}")
        with self._writer() as conn:
            conn.execute("UPDATE job_postings SET status=? WHERE id=?", (new_status, row_id))
