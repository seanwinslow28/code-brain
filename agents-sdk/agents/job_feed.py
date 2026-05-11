#!/usr/bin/env python3
"""Job Feed Agent — daily PM/APM role discovery.

Polls 4 free feeds + ~40-company ATS watchlist, rules-filters, scores survivors
with Qwen3-14B on MBP (fallback_disabled=true => $0/run), persists to
vault/.job-feed.db, writes a Markdown roll-up to vault/20_projects/prj-job-hunt-2026/job-feed/<today>.md.

Runs 7x/morning via launchd from 8:00-11:00 AM ET to handle MBP-asleep catch-up.
Idempotency: today's roll-up `complete: true` => exit silent in ~50ms.

Usage:
    python3 agents/job_feed.py
    python3 agents/job_feed.py --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
from datetime import date, datetime, timezone, timedelta
from pathlib import Path
from typing import Callable, Awaitable

import httpx

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.hybrid_router import HybridRouter
from lib.job_db import JobDB, DEDUPE_NEW, DEDUPE_SCORED
from lib.job_renderer import read_roll_up_frontmatter, render_roll_up
from lib.job_rules import apply_rules
from lib.job_scoring import JobScoringUnavailable, score_posting
from lib.job_sources import fetch_all, load_watchlist_slugs
from lib.logging_setup import record_run, setup_logger

AGENT_NAME = "job-feed"
DISABLE_FLAG = Path(__file__).parent.parent / ".disable-job-feed"

CompletionFn = Callable[[str, str, str], Awaitable[str]]


def _today_et_iso() -> str:
    """Today's date in Eastern Time as YYYY-MM-DD."""
    # ET is UTC-4 (EDT, May 11). Use a fixed offset for the date boundary check.
    # Production: switch to zoneinfo("America/New_York") for DST correctness.
    return (datetime.now(timezone.utc) - timedelta(hours=4)).date().isoformat()


async def _probe_mbp(url: str, timeout_sec: int) -> bool:
    """HTTP HEAD probe to the MBP LLM endpoint. Returns True if reachable."""
    try:
        async with httpx.AsyncClient(timeout=timeout_sec) as client:
            r = await client.head(url)
            return r.status_code < 500
    except Exception:
        return False


async def run_pipeline(
    *,
    today_iso: str,
    db_path: Path,
    watchlist_path: Path,
    roll_up_dir: Path,
    manifest_dir: Path,
    mbp_probe_url: str,
    mbp_probe_timeout_sec: int,
    http_timeout_sec: int,
    fetch_skip_if_within_hours: int,
    fallback_disabled: bool,
    router: HybridRouter | None,
    completion_fn: CompletionFn | None,
) -> dict:
    """Single end-to-end pipeline run. Returns a run-report dict for the manifest."""
    t0 = time.monotonic()
    report = {
        "fired_at": datetime.now().isoformat(),
        "fetch_total": 0,
        "rules_passed": 0,
        "rules_rejected": 0,
        "llm_scored": 0,
        "llm_failed": 0,
        "mbp_reachable": False,
        "duration_sec": 0,
        "failed_pollers": [],
        "short_circuited": False,
    }

    roll_up_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    roll_up_path = roll_up_dir / f"{today_iso}.md"

    # 1. Idempotency: complete=true => exit silent
    existing_fm = read_roll_up_frontmatter(roll_up_path)
    if existing_fm and existing_fm.get("complete") is True:
        report["short_circuited"] = True
        report["duration_sec"] = time.monotonic() - t0
        return report

    db = JobDB(db_path)

    # 2. Probe MBP
    mbp_up = await _probe_mbp(mbp_probe_url, mbp_probe_timeout_sec)
    report["mbp_reachable"] = mbp_up

    # 3. Fetch — skipped if existing roll-up was recently written
    need_fetch = True
    if existing_fm:
        # Spec: skip refetch if last fetch < fetch_skip_if_within_hours ago.
        # Use roll-up file mtime as the proxy.
        age_hr = (time.time() - roll_up_path.stat().st_mtime) / 3600.0
        if age_hr < fetch_skip_if_within_hours:
            need_fetch = False

    if need_fetch:
        slugs = load_watchlist_slugs(watchlist_path)
        postings, failed = await fetch_all(
            watchlist_slugs=slugs,
            http_timeout_sec=http_timeout_sec,
        )
        report["fetch_total"] = len(postings)
        report["failed_pollers"] = failed

        # 4. Dedupe + rules-filter + persist
        for p in postings:
            state = db.dedupe_state(p)
            if state == DEDUPE_SCORED:
                continue
            if state == DEDUPE_NEW:
                passed, reason = apply_rules(p)
                if not passed:
                    db.persist_rejected(p, reason or "unspecified")
                    report["rules_rejected"] += 1
                else:
                    db.persist_rules_passed(p, scored=None)
                    report["rules_passed"] += 1
            # DEDUPE_CARRYOVER: already persisted with rules_passed=1; just re-queue for scoring

    # 5. LLM scoring (only if MBP reachable)
    if mbp_up and router is not None:
        for p in db.unscored_postings():
            try:
                result = await score_posting(
                    p, router=router, completion_fn=completion_fn,
                    fallback_disabled=fallback_disabled,
                )
                db.update_score(p, result)
                report["llm_scored"] += 1
            except JobScoringUnavailable:
                report["llm_failed"] += 1
                # Leave fit_score=NULL; next run picks it up via carryover

    # 6. Render roll-up
    # scored_today filters by date(scored_at) — use today's actual date since
    # scored_at is always datetime.now(). In production today_iso == today's real date;
    # in tests today_iso may be a synthetic label while scoring happens on the real clock.
    real_today = date.today().isoformat()
    scored = db.scored_today(real_today)
    unscored = db.unscored_postings() if (mbp_up is False or report["llm_failed"] > 0) else []
    complete = (mbp_up and report["llm_failed"] == 0 and not unscored)
    roll_up_path.write_text(
        render_roll_up(today_iso, scored=scored, unscored=unscored, complete=complete),
        encoding="utf-8",
    )

    # 7. Write run manifest (append today's run to the daily manifest)
    manifest_path = manifest_dir / f"job-feed-manifest-{today_iso}.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
    else:
        manifest = {"date": today_iso, "runs": []}
    report["duration_sec"] = round(time.monotonic() - t0, 2)
    manifest["runs"].append(report)
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Job Feed Agent")
    parser.add_argument("--dry-run", action="store_true",
                       help="Fetch + rules + persist to temp DB. Skips MBP probe + scoring + roll-up.")
    args = parser.parse_args()

    # One-off skip
    if DISABLE_FLAG.exists():
        print(f"Skipping — {DISABLE_FLAG.name} present", file=sys.stderr)
        return 0

    config = load_config()
    jf_cfg = config.agents.get("job_feed", {})
    if not jf_cfg.get("enabled", False):
        print("job_feed disabled in config.toml — exiting", file=sys.stderr)
        return 0

    logger = setup_logger(AGENT_NAME, config.log_dir, jf_cfg.get("log_level", "INFO"))
    paths = jf_cfg.get("paths", {})

    today_iso = _today_et_iso()

    if args.dry_run:
        print("=== DRY RUN — Job Feed Agent ===")
        print(f"Today (ET):       {today_iso}")
        print(f"DB path:          {config.repo_root / paths['db']}")
        print(f"Watchlist:        {config.repo_root / paths['watchlist']}")
        print(f"Roll-up dir:      {config.repo_root / paths['roll_up_dir']}")
        print(f"Manifest dir:     {config.repo_root / paths['manifest_dir']}")
        print(f"MBP probe URL:    {jf_cfg['mbp_probe_url']}")
        print(f"fallback_disabled: {jf_cfg.get('fallback_disabled', True)}")
        print("=== END DRY RUN ===")
        return 0

    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib
    raw_cfg_path = Path(__file__).parent.parent / "config.toml"
    with open(raw_cfg_path, "rb") as f:
        raw = tomllib.load(f)
    router = HybridRouter.from_config(raw)

    t0 = time.time()
    try:
        report = asyncio.run(run_pipeline(
            today_iso=today_iso,
            db_path=config.repo_root / paths["db"],
            watchlist_path=config.repo_root / paths["watchlist"],
            roll_up_dir=config.repo_root / paths["roll_up_dir"],
            manifest_dir=config.repo_root / paths["manifest_dir"],
            mbp_probe_url=jf_cfg["mbp_probe_url"],
            mbp_probe_timeout_sec=jf_cfg["mbp_probe_timeout_sec"],
            http_timeout_sec=jf_cfg["http_timeout_sec"],
            fetch_skip_if_within_hours=jf_cfg["fetch_skip_if_within_hours"],
            fallback_disabled=jf_cfg.get("fallback_disabled", True),
            router=router,
            completion_fn=None,
        ))
        status = "success" if report.get("short_circuited") or report.get("llm_failed", 0) == 0 else "partial"
        logger.info(
            "Done — fetch=%d rules_passed=%d rules_rejected=%d scored=%d mbp_up=%s",
            report["fetch_total"], report["rules_passed"], report["rules_rejected"],
            report["llm_scored"], report["mbp_reachable"],
        )
        record_run(
            config.log_dir, AGENT_NAME, mode=None, status=status,
            cost_usd=0.0, duration_ms=int((time.time() - t0) * 1000), turns=None,
            notes=f"fetch={report['fetch_total']} scored={report['llm_scored']} mbp={report['mbp_reachable']}",
        )
        return 0
    except Exception as exc:
        logger.exception("Pipeline failed: %s", exc)
        record_run(
            config.log_dir, AGENT_NAME, mode=None, status="error",
            cost_usd=0.0, duration_ms=int((time.time() - t0) * 1000), turns=None,
            notes=f"error: {str(exc)[:200]}",
        )
        return 3


if __name__ == "__main__":
    sys.exit(main())
