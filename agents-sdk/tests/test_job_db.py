import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

from lib.job_db import (
    JobDB,
    DEDUPE_NEW, DEDUPE_SCORED, DEDUPE_CARRYOVER,
)
from lib.job_types import Posting, ScoringResult


@pytest.fixture
def db(tmp_path) -> JobDB:
    return JobDB(tmp_path / "test.db")


def _p(**overrides) -> Posting:
    base = dict(
        source="remoteok", source_role_id="1", url="https://x.example",
        company="Co", title="PM", location="Remote (US)",
        salary_disclosed=None, posted_at=datetime(2026, 5, 9),
        description="x",
    )
    base.update(overrides)
    return Posting(**base)


def test_init_creates_schema(db: JobDB):
    with sqlite3.connect(db.path) as conn:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(job_postings)")]
    assert "source" in cols
    assert "source_role_id" in cols
    assert "fit_score" in cols
    assert "status" in cols


def test_dedupe_new(db: JobDB):
    state = db.dedupe_state(_p(source="x", source_role_id="1"))
    assert state == DEDUPE_NEW


def test_persist_then_dedupe_carryover(db: JobDB):
    p = _p(source="x", source_role_id="2")
    db.persist_rules_passed(p, scored=None)  # rules_passed=1, fit_score=NULL
    assert db.dedupe_state(p) == DEDUPE_CARRYOVER


def test_persist_then_dedupe_scored(db: JobDB):
    p = _p(source="x", source_role_id="3")
    db.persist_rules_passed(p, scored=None)
    score = ScoringResult(
        fit_score=4, role_band="PM", rationale="ok",
        concerns=[], fit_dimensions={"role_band_fit": 4},
    )
    db.update_score(p, score)
    assert db.dedupe_state(p) == DEDUPE_SCORED


def test_unique_constraint_no_duplicate_inserts(db: JobDB):
    p = _p(source="x", source_role_id="4")
    db.persist_rules_passed(p, scored=None)
    db.persist_rules_passed(p, scored=None)  # second call must not insert
    with sqlite3.connect(db.path) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM job_postings WHERE source='x' AND source_role_id='4'"
        ).fetchone()[0]
    assert count == 1


def test_persist_rejected_stores_reason(db: JobDB):
    p = _p(source="x", source_role_id="5")
    db.persist_rejected(p, reason="not a PM role")
    with sqlite3.connect(db.path) as conn:
        row = conn.execute(
            "SELECT rules_passed, rules_rejection_reason FROM job_postings WHERE source='x' AND source_role_id='5'"
        ).fetchone()
    assert row == (0, "not a PM role")


def test_description_excerpt_truncated_to_500(db: JobDB):
    long_desc = "x" * 2000
    p = _p(source="x", source_role_id="6", description=long_desc)
    db.persist_rules_passed(p, scored=None)
    with sqlite3.connect(db.path) as conn:
        excerpt = conn.execute(
            "SELECT description_excerpt FROM job_postings WHERE source='x' AND source_role_id='6'"
        ).fetchone()[0]
    assert len(excerpt) == 500


def test_unscored_query(db: JobDB):
    db.persist_rules_passed(_p(source="x", source_role_id="7"), scored=None)
    db.persist_rules_passed(_p(source="x", source_role_id="8"), scored=None)
    score = ScoringResult(fit_score=4, role_band="PM", rationale="ok")
    db.update_score(_p(source="x", source_role_id="8"), score)
    unscored = db.unscored_postings()
    ids = {p.source_role_id for p in unscored}
    assert ids == {"7"}


def test_status_mutation(db: JobDB):
    p = _p(source="x", source_role_id="9")
    db.persist_rules_passed(p, scored=None)
    row_id = db.row_id(p)
    db.update_status(row_id, "applied")
    with sqlite3.connect(db.path) as conn:
        status = conn.execute(
            "SELECT status FROM job_postings WHERE id=?", (row_id,)
        ).fetchone()[0]
    assert status == "applied"
