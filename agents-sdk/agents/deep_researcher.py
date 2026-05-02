#!/usr/bin/env python3
"""Deep Researcher Agent — local autonomous deep research via LDR + SearXNG + LM Studio.

Picks one question from the research queue (or `--query` for one-shot), runs
LearningCircuit Local Deep Research locally (Qwen3-14B MLX 4-bit on LM Studio,
SearXNG via Docker), writes the full report into the vault, injects a digest
line into today's daily note, and marks the queue item done with a backlink.

This is a pure-Python wrapper — LDR is the synthesis engine, not Claude.
The Claude Agent SDK is *not* used here; `agent_config.skills` is decorative.

Usage:
    python3 agents/deep_researcher.py --mode queue
    python3 agents/deep_researcher.py --mode queue --dry-run
    python3 agents/deep_researcher.py --mode oneshot --query "Your question here"
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config
from lib.keychain import get_credential
from lib.logging_setup import record_run, setup_logger
from lib.vault_io import daily_note_path, inject_at_anchor

AGENT_NAME = "deep-researcher"
ANCHOR_FALLBACK_HEADING = "## Deep Research"


def _slugify(text: str, max_len: int = 60) -> str:
    """Filesystem-safe slug for note filenames."""
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:max_len].rstrip("-") or "untitled"


def _next_unchecked(queue_path: Path) -> str | None:
    """Return the first `- [ ] ...` line text from the queue file, or None."""
    if not queue_path.exists():
        return None
    for line in queue_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\s*-\s*\[\s\]\s+(.+?)\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _mark_done(queue_path: Path, question: str, link_target: Path, vault_root: Path) -> bool:
    """Mark `- [ ] question` as done with timestamp + backlink to the topical note.

    Returns True if a line was rewritten.
    """
    if not queue_path.exists():
        return False
    text = queue_path.read_text(encoding="utf-8")
    rel = link_target.relative_to(vault_root)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    note_link = f"[[{rel.with_suffix('').as_posix()}]]"
    needle = re.compile(
        r"^(\s*-\s*\[)\s(\]\s+" + re.escape(question) + r")\s*$",
        re.MULTILINE,
    )
    new_text, n = needle.subn(rf"\1x\2 — done {timestamp} → {note_link}", text, count=1)
    if n == 0:
        return False
    queue_path.write_text(new_text, encoding="utf-8")
    return True


def _build_topical_note(question: str, summary: str, run_meta: dict) -> str:
    """Compose the front-matter + body for the topical research note."""
    today = date.today().isoformat()
    fm_question = question.replace('"', "'")
    body = summary if isinstance(summary, str) and summary.strip() else "_(no summary returned)_"
    return (
        f"---\n"
        f"type: research-report\n"
        f"date: {today}\n"
        f"question: \"{fm_question}\"\n"
        f"source: deep-researcher-agent\n"
        f"ldr_research_id: {run_meta.get('research_id', '')}\n"
        f"wall_seconds: {run_meta.get('wall_seconds', '')}\n"
        f"tags: [research, deep-research, autogen]\n"
        f"---\n\n"
        f"# {question}\n\n"
        f"> Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} by `deep-researcher` "
        f"(LDR {run_meta.get('ldr_version', '?')} · model qwen3-14b · "
        f"iterations={run_meta.get('iterations', '?')}).\n\n"
        f"{body}\n"
    )


def _build_digest_line(question: str, topical_path: Path, vault_root: Path, run_meta: dict) -> str:
    """One-line digest for today's daily note."""
    rel = topical_path.relative_to(vault_root).with_suffix("").as_posix()
    timestamp = datetime.now().strftime("%H:%M")
    wall = run_meta.get("wall_seconds")
    wall_s = f" ({wall}s)" if wall else ""
    return f"- {timestamp} — [[{rel}|{question}]]{wall_s}"


def _inject_or_append_digest(
    daily_path: Path, anchor: str, digest_line: str
) -> str:
    """Inject digest at <!-- anchor -->, or append a fallback section if missing.

    Returns one of: "injected", "appended-section", "skipped-no-note".
    """
    if not daily_path.exists():
        return "skipped-no-note"
    if inject_at_anchor(daily_path, anchor, digest_line):
        return "injected"
    # Anchor missing — append a fresh section so the digest still lands.
    with open(daily_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n{ANCHOR_FALLBACK_HEADING}\n<!-- {anchor} -->\n{digest_line}\n")
    return "appended-section"


def _run_ldr(
    base_url: str,
    query: str,
    search_engines: list[str],
    iterations: int,
    questions_per_iteration: int,
    timeout: int,
    logger,
) -> tuple[dict, dict]:
    """Drive LDR's REST API via httpx — replicates LDRClient.quick_research.

    LDR runs in its own venv (~/Code-Brain/local-deep-research-stack/.venv)
    on Python 3.11; this agent runs in agents-sdk/.venv on Python 3.13. We
    can't cross-import — instead we hit LDR's HTTP endpoints directly. This
    is the same endpoint set the Phase 4 smoke test validated.
    """
    import httpx

    user = get_credential("ldr_username")
    pw = get_credential("ldr_password")
    if not user or not pw:
        raise RuntimeError(
            "LDR credentials missing from Keychain. "
            "Set with: python3 agents-sdk/lib/keychain.py set ldr_username <user>"
        )

    with httpx.Client(base_url=base_url, timeout=30.0, follow_redirects=False) as client:
        # 1. GET login page → CSRF token + initial session cookie
        r = client.get("/auth/login")
        r.raise_for_status()
        m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
        if not m:
            raise RuntimeError("CSRF token not found on /auth/login")
        csrf = m.group(1)

        # 2. POST login (form-encoded, like the HTML form)
        r = client.post(
            "/auth/login",
            data={"csrf_token": csrf, "username": user, "password": pw},
        )
        if r.status_code != 302:
            raise RuntimeError(f"LDR login failed: http={r.status_code} body={r.text[:200]}")
        logger.info(f"LDR login ok at {base_url}")

        # 3. Grab a fresh CSRF token for protected JSON POSTs
        r = client.get("/")
        m = re.search(r'name="csrf_token"\s+value="([^"]+)"', r.text)
        csrf2 = m.group(1) if m else csrf

        # 4. Submit research — same payload shape as LDRClient.quick_research
        t0 = time.time()
        r = client.post(
            "/research/api/start",
            json={
                "query": query,
                "search_engines": search_engines,
                "iterations": iterations,
                "questions_per_iteration": questions_per_iteration,
            },
            headers={"X-CSRFToken": csrf2, "Content-Type": "application/json"},
        )
        if r.status_code != 200:
            raise RuntimeError(f"start research failed: http={r.status_code} body={r.text[:300]}")
        start_resp = r.json()
        research_id = start_resp.get("research_id") or start_resp.get("id")
        if not research_id:
            raise RuntimeError(f"no research_id in start response: {start_resp}")
        logger.info(f"research_id={research_id}")

        # 5. Poll until terminal state
        deadline = t0 + timeout
        last_progress = None
        status = "?"
        while time.time() < deadline:
            r = client.get(f"/research/api/status/{research_id}")
            if r.status_code == 200:
                s = r.json()
                status = s.get("status", "?")
                progress = s.get("progress")
                if progress != last_progress:
                    logger.info(f"  t={int(time.time()-t0):>3}s status={status} progress={progress}%")
                    last_progress = progress
                if status in ("completed", "failed", "suspended", "error"):
                    break
            time.sleep(4)
        else:
            raise RuntimeError(f"LDR research timed out after {timeout}s (research_id={research_id})")

        if status != "completed":
            raise RuntimeError(f"LDR research ended in non-success state: {status} (research_id={research_id})")

        # 6. Fetch final report
        r = client.get(f"/api/report/{research_id}", timeout=60.0)
        if r.status_code != 200:
            raise RuntimeError(f"report fetch failed: http={r.status_code}")
        result = r.json() if "json" in r.headers.get("Content-Type", "") else {"content": r.text}

        wall = int(time.time() - t0)
        run_meta = {
            "wall_seconds": wall,
            "research_id": research_id,
            "ldr_version": "via-rest",  # version not exposed via API; agent doesn't import LDR
            "iterations": iterations,
        }
        return result, run_meta


def run(mode: str, dry_run: bool = False, oneshot_query: str | None = None) -> int:
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level, mode=mode)

    raw_cfg = config.agents.get("deep_researcher", {})
    if not raw_cfg.get("enabled", False):
        logger.warning("deep_researcher disabled in config.toml — exiting")
        return 0

    queue_path = config.repo_root / raw_cfg["queue_path"]
    output_dir = config.repo_root / raw_cfg["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    anchor = raw_cfg.get("output_anchor", "research-digest")
    base_url = raw_cfg.get("ldr_base_url", "http://localhost:5050")

    # Pick the question to research.
    if mode == "oneshot":
        if not oneshot_query:
            logger.error("--mode oneshot requires --query")
            return 2
        question = oneshot_query.strip()
    else:  # queue
        question = _next_unchecked(queue_path)
        if not question:
            logger.info(f"Queue empty at {queue_path} — nothing to do")
            record_run(
                config.log_dir, AGENT_NAME, mode,
                status="empty-queue", cost_usd=0.0, duration_ms=0, turns=0,
                notes="no unchecked items",
            )
            return 0

    logger.info(f"Selected question: {question}")

    if dry_run:
        slug = _slugify(question)
        topical_path = output_dir / f"{date.today().isoformat()}-{slug}.md"
        daily_path = daily_note_path(config.vault_root)
        print("=== DRY RUN — Deep Researcher ===")
        print(f"Mode:           {mode}")
        print(f"Question:       {question}")
        print(f"LDR base URL:   {base_url}")
        print(f"Search engines: {raw_cfg.get('ldr_search_engines', ['searxng'])}")
        print(f"Iterations:     {raw_cfg.get('ldr_iterations', 2)}")
        print(f"Q/iteration:    {raw_cfg.get('ldr_questions_per_iteration', 2)}")
        print(f"Timeout:        {raw_cfg.get('ldr_timeout_seconds', 900)}s")
        print(f"Topical note:   {topical_path}")
        print(f"Daily note:     {daily_path}  (anchor=<!-- {anchor} -->)")
        print(f"Queue:          {queue_path}")
        print("=== END DRY RUN ===")
        return 0

    # Live run.
    t_start = time.time()
    try:
        result, run_meta = _run_ldr(
            base_url=base_url,
            query=question,
            search_engines=raw_cfg.get("ldr_search_engines", ["searxng"]),
            iterations=raw_cfg.get("ldr_iterations", 2),
            questions_per_iteration=raw_cfg.get("ldr_questions_per_iteration", 2),
            timeout=raw_cfg.get("ldr_timeout_seconds", 900),
            logger=logger,
        )
    except Exception as e:
        duration_ms = int((time.time() - t_start) * 1000)
        logger.exception(f"LDR call failed: {e}")
        record_run(
            config.log_dir, AGENT_NAME, mode,
            status="error", cost_usd=0.0,
            duration_ms=duration_ms, turns=0,
            notes=f"LDR failure: {str(e)[:200]}",
        )
        return 3

    summary = result.get("summary") or result.get("content") or ""
    if not summary and isinstance(result, dict):
        # LDRClient.quick_research returns a results dict; report body lives
        # under "summary" or top-level "content"; fall back to the whole dict.
        summary = str(result)

    slug = _slugify(question)
    topical_path = output_dir / f"{date.today().isoformat()}-{slug}.md"
    topical_path.write_text(_build_topical_note(question, summary, run_meta), encoding="utf-8")
    logger.info(f"Wrote topical note: {topical_path}")

    # Inject digest into today's daily note (with append fallback).
    daily_path = daily_note_path(config.vault_root)
    digest = _build_digest_line(question, topical_path, config.vault_root, run_meta)
    inject_status = _inject_or_append_digest(daily_path, anchor, digest)
    logger.info(f"Daily note digest: {inject_status} ({daily_path.name})")

    # Mark queue done (only in queue mode).
    if mode == "queue":
        ok = _mark_done(queue_path, question, topical_path, config.vault_root)
        if not ok:
            logger.warning(
                f"Could not mark queue item done — line not found in {queue_path}. "
                f"Question may have been edited. Topical note still saved."
            )

    duration_ms = int((time.time() - t_start) * 1000)
    record_run(
        config.log_dir, AGENT_NAME, mode,
        status="success", cost_usd=0.0,
        duration_ms=duration_ms,
        turns=run_meta.get("iterations"),
        notes=f"id={run_meta.get('research_id', '')[:8]} wall={run_meta.get('wall_seconds')}s digest={inject_status}",
    )
    print(f"OK — wrote {topical_path.name} ({len(summary.split())} words, {run_meta.get('wall_seconds')}s); daily digest: {inject_status}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Deep Researcher Agent")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["queue", "oneshot"],
        help="queue: pick first unchecked from research-queue.md. oneshot: use --query.",
    )
    parser.add_argument("--query", help="Question to research (oneshot mode only).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without calling LDR.",
    )
    args = parser.parse_args()
    return run(args.mode, dry_run=args.dry_run, oneshot_query=args.query)


if __name__ == "__main__":
    sys.exit(main())
