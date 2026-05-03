#!/usr/bin/env python3
"""Gemini Deep Research helper — Phase 1 (v3.25.0).

Calls Gemini Deep Research or Deep Research Max via the Google Interactions API
with background polling, writes a topical report to the vault, updates the spend
ledger, and refuses when caps are hit.

Used by both the gemini-deep-research skill (Phase 2) and the gemini_researcher
agent (Phase 3).

Usage:
    # Dry run (no API call, prints intent):
    python3 scripts/gemini_dr.py --query "Your question" --tier dr --dry-run

    # Live run (DR, prompts if DR Max):
    python3 scripts/gemini_dr.py --query "Your question" --tier dr

    # DR Max — requires --no-confirm (confirmation is the skill's job):
    python3 scripts/gemini_dr.py --query "Your question" --tier max --no-confirm

Note: Status values from the Interactions API are:
    "in_progress", "requires_action", "completed", "failed", "cancelled", "incomplete"
    The plan spec referenced "running" — this helper uses the actual SDK values.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import tomllib
from datetime import date, datetime
from pathlib import Path

# Add agents-sdk/ to Python path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from google import genai  # noqa: E402  (after sys.path insert)

from lib.config import load_config
from lib.filelock import FileLock
from lib.keychain import get_credential
from lib.logging_setup import record_run, setup_logger
from lib.vault_io import daily_note_path, inject_at_anchor

AGENT_NAME = "gemini-dr"
ANCHOR_FALLBACK_HEADING = "## Gemini Research"

# Terminal statuses from the Interactions API (v1.74.0).
# Anything NOT in _TERMINAL_STATUSES is treated as still-running, including
# unknown future status values (e.g. "queued", "requires_action", "running").
_TERMINAL_STATUSES = {"completed", "failed", "cancelled", "incomplete"}


# ─── Config loading ─────────────────────────────────────────────────────────


def _load_gemini_cfg() -> dict:
    """Load [gemini] and [gemini.budget] sections from config.toml.

    Returns a flat dict merging both sections (budget keys nested under 'budget').
    The main Config dataclass does not expose these — we re-parse TOML directly.
    """
    config_path = Path(__file__).parent.parent / "config.toml"
    with open(config_path, "rb") as f:
        raw = tomllib.load(f)
    return raw.get("gemini", {})


# ─── Cost / budget helpers ───────────────────────────────────────────────────


def predicted_cost(tier: str, cfg: dict) -> float:
    """Return predicted cost for a tier using midpoint × multiplier.

    Per plan: DR midpoint=$2.00, Max midpoint=$5.00, multiplier=1.4.
    Defaults are embedded here as fallback if config is missing keys.
    """
    budget = cfg.get("budget", {})
    multiplier = budget.get("prediction_multiplier", 1.4)
    if tier == "max":
        midpoint = budget.get("max_predicted_usd", 5.00)
    else:
        midpoint = budget.get("dr_predicted_usd", 2.00)
    return round(midpoint * multiplier, 4)


def read_ledger(ledger_path: Path) -> list[dict]:
    """Read the spend ledger JSON. Returns empty list if missing or invalid."""
    if not ledger_path.exists():
        return []
    try:
        data = json.loads(ledger_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, OSError):
        return []


def ledger_totals(entries: list[dict], today_iso: str) -> tuple[float, float]:
    """Return (month_to_date, today_so_far) cost totals from ledger entries.

    Sums cost_actual_usd if available, else cost_predicted_usd, else cost_usd.
    The third fallback (cost_usd) supports legacy entries written by older code
    that stored only a single cost field.
    Entries without a 'created' field are counted toward mtd only.
    """
    month_prefix = today_iso[:7]  # "YYYY-MM"
    mtd = 0.0
    today_total = 0.0
    for entry in entries:
        # Prefer actual > predicted > legacy single-field.
        # Use explicit is-not-None checks so that 0.0 (free/cancelled run) is
        # treated as $0, not silently fallen through to the next field.
        if entry.get("cost_actual_usd") is not None:
            cost = entry["cost_actual_usd"]
        elif entry.get("cost_predicted_usd") is not None:
            cost = entry["cost_predicted_usd"]
        elif entry.get("cost_usd") is not None:
            cost = entry["cost_usd"]
        else:
            cost = 0.0
        created = entry.get("created", "")
        if created.startswith(month_prefix):
            mtd += cost
            if created.startswith(today_iso):
                today_total += cost
    return round(mtd, 4), round(today_total, 4)


def check_caps(
    tier: str,
    cfg: dict,
    ledger_path: Path,
    today_iso: str,
) -> tuple[bool, str, float, float, float]:
    """Check all cost caps before making an API call.

    Order per plan: per-task → daily → monthly.

    Returns:
        (ok, message, predicted, mtd, today_total)
        ok=True if all caps pass; False if any cap is hit.
        message is empty on success, descriptive on failure.
    """
    budget = cfg.get("budget", {})
    max_per_task = budget.get("max_per_task_usd", 7.00)
    monthly_cap = budget.get("monthly_cap_usd", 20.00)
    daily_cap = budget.get("daily_cap_usd", 10.00)

    pred = predicted_cost(tier, cfg)
    entries = read_ledger(ledger_path)
    mtd, today_total = ledger_totals(entries, today_iso)

    # Check per-task cap first
    if pred > max_per_task:
        return (
            False,
            f"per-task cap: predicted ${pred:.2f} > max_per_task_usd ${max_per_task:.2f}",
            pred,
            mtd,
            today_total,
        )

    # Check daily cap
    if (today_total + pred) > daily_cap:
        return (
            False,
            f"daily cap: today ${today_total:.2f} + predicted ${pred:.2f} = "
            f"${today_total + pred:.2f} > daily_cap_usd ${daily_cap:.2f}",
            pred,
            mtd,
            today_total,
        )

    # Check monthly cap
    if (mtd + pred) > monthly_cap:
        return (
            False,
            f"monthly cap: mtd ${mtd:.2f} + predicted ${pred:.2f} = "
            f"${mtd + pred:.2f} > monthly_cap_usd ${monthly_cap:.2f}",
            pred,
            mtd,
            today_total,
        )

    return True, "", pred, mtd, today_total


def warn_if_approaching_cap(
    mtd: float,
    cfg: dict,
    logger,
) -> None:
    """Emit a WARN to stderr (via logger) if mtd > 70% of monthly cap."""
    budget = cfg.get("budget", {})
    monthly_cap = budget.get("monthly_cap_usd", 20.00)
    threshold = monthly_cap * 0.7
    if mtd > threshold:
        logger.warning(
            f"Gemini spend alert: month-to-date ${mtd:.2f} exceeds 70% of "
            f"monthly cap (${monthly_cap:.2f}). Threshold: ${threshold:.2f}."
        )


def append_ledger(
    ledger_path: Path,
    entry: dict,
) -> None:
    """Atomically append one entry to the spend ledger.

    Uses FileLock → read → mutate → write .tmp → os.replace for atomicity.
    """
    lock_path = ledger_path.parent / ".gemini-ledger.lock"
    ledger_path.parent.mkdir(parents=True, exist_ok=True)

    with FileLock(lock_path, exclusive=True, timeout=10.0):
        entries = read_ledger(ledger_path)
        entries.append(entry)
        tmp_path = ledger_path.with_suffix(".tmp")
        try:
            tmp_path.write_text(
                json.dumps(entries, indent=2, default=str),
                encoding="utf-8",
            )
            os.replace(tmp_path, ledger_path)
        except Exception:
            tmp_path.unlink(missing_ok=True)
            raise


# ─── Slug + note helpers ─────────────────────────────────────────────────────


def slugify(text: str, max_len: int = 60) -> str:
    """Filesystem-safe slug for note filenames.

    Mirrors deep_researcher._slugify but is module-level for importability.
    """
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:max_len].rstrip("-") or "untitled"


def build_topical_note(
    query: str,
    tier: str,
    report_text: str,
    interaction_id: str,
    agent_id: str,
    wall_seconds: int,
    cost_predicted_usd: float,
    cost_actual_usd: float | None,
) -> str:
    """Compose frontmatter + body for the Gemini DR topical note."""
    today = date.today().isoformat()
    fm_query = query.replace('"', "'")
    source = "gemini-deep-research-max" if tier == "max" else "gemini-deep-research"
    cost_usd = cost_actual_usd if cost_actual_usd is not None else cost_predicted_usd
    body = report_text.strip() if report_text and report_text.strip() else "_(no report returned)_"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return (
        f"---\n"
        f"type: research-report\n"
        f"date: {today}\n"
        f"question: \"{fm_query}\"\n"
        f"source: {source}\n"
        f"cost_usd: {cost_usd:.4f}\n"
        f"wall_seconds: {wall_seconds}\n"
        f"interaction_id: {interaction_id}\n"
        f"agent_id: {agent_id}\n"
        f"created: {today}\n"
        f"tags: [research, gemini-deep-research, autogen]\n"
        f"---\n\n"
        f"# {query}\n\n"
        f"> Generated {now} by `gemini-dr` "
        f"(agent={agent_id} · tier={tier} · wall={wall_seconds}s).\n\n"
        f"{body}\n"
    )


def build_digest_line(
    query: str,
    topical_path: Path,
    vault_root: Path,
    tier: str,
    wall_seconds: int,
    cost_usd: float,
) -> str:
    """One-line digest for today's daily note."""
    rel = topical_path.relative_to(vault_root).with_suffix("").as_posix()
    timestamp = datetime.now().strftime("%H:%M")
    tier_tag = "DR Max" if tier == "max" else "DR"
    return f"- {timestamp} — [[{rel}|{query}]] ({tier_tag} · {wall_seconds}s · ${cost_usd:.2f})"


def inject_or_append_digest(
    daily_path: Path,
    anchor: str,
    digest_line: str,
) -> str:
    """Inject digest at anchor, or append a fallback section.

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


# ─── Polling ─────────────────────────────────────────────────────────────────


def poll_interaction(
    client: genai.Client,
    interaction_id: str,
    poll_interval: int,
    max_poll_seconds: int,
    logger,
) -> tuple[str, str | None, dict | None]:
    """Poll until terminal status or timeout.

    Returns:
        (status, report_text, usage_dict)
        report_text is None on non-completed statuses.
        usage_dict is None when not available.

    Raises:
        RuntimeError: On timeout.

    Note: Actual SDK status values are "in_progress", "requires_action",
    "completed", "failed", "cancelled", "incomplete" — not "running".
    """
    deadline = time.time() + max_poll_seconds
    last_status = None

    while time.time() < deadline:
        interaction = client.interactions.get(interaction_id)
        status = interaction.status

        if status != last_status:
            logger.info(f"  interaction={interaction_id[:8]} status={status}")
            last_status = status

        if status in _TERMINAL_STATUSES:
            usage = None
            if hasattr(interaction, "usage") and interaction.usage is not None:
                usage = interaction.usage

            if status == "completed":
                # Extract text from the last output
                outputs = getattr(interaction, "outputs", None) or []
                report_text = None
                if outputs:
                    last = outputs[-1]
                    report_text = getattr(last, "text", None)
                return status, report_text, usage
            else:
                error = getattr(interaction, "error", None)
                err_msg = str(error) if error else f"status={status}"
                raise RuntimeError(f"Interaction ended in non-success state: {err_msg}")

        time.sleep(poll_interval)

    raise RuntimeError(
        f"Gemini DR polling timed out after {max_poll_seconds}s "
        f"(interaction_id={interaction_id})"
    )


# ─── Main run logic ───────────────────────────────────────────────────────────


def run(
    query: str,
    tier: str,
    dry_run: bool = False,
    no_confirm: bool = False,
    output_dir: str | None = None,
    ledger_path_override: Path | None = None,
    max_poll_seconds: int | None = None,
) -> int:
    """Core logic — importable by agents/gemini_researcher.py (Phase 3).

    Returns exit code (0 = success, 1 = cap refusal, 2 = usage error, 3 = API error).
    """
    config = load_config()
    logger = setup_logger(AGENT_NAME, config.log_dir, config.log_level, mode=tier)

    gemini_cfg = _load_gemini_cfg()

    # Determine output dir
    out_dir_str = output_dir or gemini_cfg.get("output_dir", "vault/20_projects/research")
    out_dir = config.repo_root / out_dir_str
    anchor = gemini_cfg.get("output_anchor", "research-digest")

    # Determine ledger path
    today_iso = date.today().isoformat()
    month_str = today_iso[:7]  # YYYY-MM
    ledger_dir = config.repo_root / gemini_cfg.get("ledger_dir", "vault/health")
    if ledger_path_override is not None:
        ledger_path = ledger_path_override
    else:
        ledger_path = ledger_dir / f"gemini-spend-{month_str}.json"

    # Resolve poll config
    poll_interval = gemini_cfg.get("poll_interval_seconds", 10)
    max_poll = max_poll_seconds if max_poll_seconds is not None else gemini_cfg.get(
        "max_poll_seconds", 3900
    )

    # Determine agent ID from tier
    if tier == "max":
        agent_id = gemini_cfg.get("agent_id_max", "deep-research-max-preview-04-2026")
    else:
        agent_id = gemini_cfg.get("agent_id_dr", "deep-research-preview-04-2026")

    # Compute slug + output path
    slug = slugify(query)
    topical_path = out_dir / f"{today_iso}-{slug}.md"
    daily_path = daily_note_path(config.vault_root)

    # Handle DR Max confirmation requirement BEFORE any cap checks
    # Per plan constraint 3: helper refuses, does NOT use input()
    if tier == "max" and not no_confirm:
        print(
            "ERROR: DR Max requires --no-confirm flag or interactive confirmation "
            "via the gemini-deep-research skill. Pass --no-confirm to proceed.",
            file=sys.stderr,
        )
        return 2

    # Cost cap checks (happen BEFORE any API call — hard constraint)
    ok, cap_msg, pred_cost, mtd, today_total = check_caps(
        tier, gemini_cfg, ledger_path, today_iso
    )

    # Warn if approaching cap — include this run's predicted cost so the alert
    # fires when *this run* would push spend toward the cap, not just prior runs.
    warn_if_approaching_cap(mtd + pred_cost, gemini_cfg, logger)

    if not ok:
        print(f"ERROR: Refused — {cap_msg}", file=sys.stderr)
        logger.error(f"Cap refusal: {cap_msg}")
        record_run(
            config.log_dir, AGENT_NAME, tier,
            status="cap-refused", cost_usd=0.0,
            duration_ms=0, turns=0,
            notes=f"cap: {cap_msg}",
        )
        return 1

    if dry_run:
        print("=== DRY RUN — Gemini Deep Research ===")
        print(f"Query:          {query}")
        print(f"Tier:           {tier}")
        print(f"Agent ID:       {agent_id}")
        print(f"Predicted cost: ${pred_cost:.2f}")
        print(f"MTD spent:      ${mtd:.2f}")
        print(f"Today spent:    ${today_total:.2f}")
        print(f"Output path:    {topical_path}")
        print(f"Ledger:         {ledger_path}")
        print(f"Daily note:     {daily_path}  (anchor=<!-- {anchor} -->)")
        print(f"Max poll:       {max_poll}s  (interval {poll_interval}s)")
        print("=== END DRY RUN ===")
        return 0

    # Load API key from Keychain
    api_key = get_credential("gemini_api_key")
    if not api_key:
        print(
            "ERROR: gemini_api_key not found in Keychain. "
            "Set with: python3 agents-sdk/lib/keychain.py set gemini_api_key <key>",
            file=sys.stderr,
        )
        return 2

    # Live run
    t_start = time.time()
    try:
        client = genai.Client(api_key=api_key)

        logger.info(f"Calling Gemini DR: agent={agent_id} query={query[:80]!r}")
        interaction = client.interactions.create(
            input=query,
            agent=agent_id,
            background=True,
            store=True,
            agent_config={"type": "deep-research", "thinking_summaries": "auto"},
        )
        interaction_id = interaction.id
        logger.info(f"Interaction created: id={interaction_id}")

        status, report_text, usage = poll_interaction(
            client,
            interaction_id,
            poll_interval=poll_interval,
            max_poll_seconds=max_poll,
            logger=logger,
        )

    except Exception as e:
        duration_ms = int((time.time() - t_start) * 1000)
        logger.exception(f"Gemini DR call failed: {e}")
        record_run(
            config.log_dir, AGENT_NAME, tier,
            status="error", cost_usd=0.0,
            duration_ms=duration_ms, turns=0,
            notes=f"API failure: {str(e)[:200]}",
        )
        return 3

    wall_seconds = int(time.time() - t_start)

    # Determine cost: usage doesn't include cost_usd, so we always use predicted
    cost_actual_usd = None  # Interactions API doesn't return a dollar amount
    cost_for_record = pred_cost

    # Write topical note
    out_dir.mkdir(parents=True, exist_ok=True)
    note_content = build_topical_note(
        query=query,
        tier=tier,
        report_text=report_text or "",
        interaction_id=interaction_id,
        agent_id=agent_id,
        wall_seconds=wall_seconds,
        cost_predicted_usd=pred_cost,
        cost_actual_usd=cost_actual_usd,
    )
    topical_path.write_text(note_content, encoding="utf-8")
    logger.info(f"Wrote topical note: {topical_path}")

    # Inject digest into today's daily note
    digest = build_digest_line(
        query=query,
        topical_path=topical_path,
        vault_root=config.vault_root,
        tier=tier,
        wall_seconds=wall_seconds,
        cost_usd=cost_for_record,
    )
    inject_status = inject_or_append_digest(daily_path, anchor, digest)
    logger.info(f"Daily note digest: {inject_status} ({daily_path.name})")

    # Append to ledger (atomic)
    ledger_entry = {
        "interaction_id": interaction_id,
        "agent_id": agent_id,
        "tier": tier,
        "cost_predicted_usd": pred_cost,
        "cost_actual_usd": cost_actual_usd,
        "cost_usd": cost_for_record,
        "wall_seconds": wall_seconds,
        "query": query,
        "created": datetime.utcnow().isoformat() + "Z",
        "output_path": str(topical_path),
    }
    append_ledger(ledger_path, ledger_entry)
    logger.info(f"Appended to ledger: {ledger_path}")

    duration_ms = int((time.time() - t_start) * 1000)
    record_run(
        config.log_dir, AGENT_NAME, tier,
        status="success", cost_usd=cost_for_record,
        duration_ms=duration_ms, turns=0,
        notes=(
            f"id={interaction_id[:8]} wall={wall_seconds}s "
            f"cost=${cost_for_record:.2f} digest={inject_status}"
        ),
    )
    print(
        f"OK — wrote {topical_path.name} ({wall_seconds}s · ${cost_for_record:.2f}); "
        f"daily digest: {inject_status}"
    )
    return 0


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gemini Deep Research helper — calls DR / DR Max, writes vault note, updates ledger."
    )
    parser.add_argument(
        "--query",
        required=True,
        help="Research question to send to Gemini Deep Research.",
    )
    parser.add_argument(
        "--tier",
        choices=["dr", "max"],
        default="dr",
        help="Model tier: 'dr' (Deep Research, ~$2) or 'max' (DR Max, ~$5). Default: dr.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print intended call without making any API request or vault writes.",
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        dest="no_confirm",
        help=(
            "Required for DR Max tier. The skill handles user confirmation — "
            "pass this flag when confirmation has been obtained interactively."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Override output directory for research notes (relative to repo root).",
    )
    parser.add_argument(
        "--ledger",
        default=None,
        dest="ledger",
        help="Override ledger file path (absolute).",
    )
    parser.add_argument(
        "--max-poll-seconds",
        type=int,
        default=None,
        dest="max_poll_seconds",
        help="Hard wall time for polling in seconds. Default: 3900 (65 min).",
    )

    args = parser.parse_args()

    ledger_override = Path(args.ledger) if args.ledger else None

    return run(
        query=args.query,
        tier=args.tier,
        dry_run=args.dry_run,
        no_confirm=args.no_confirm,
        output_dir=args.output_dir,
        ledger_path_override=ledger_override,
        max_poll_seconds=args.max_poll_seconds,
    )


if __name__ == "__main__":
    sys.exit(main())
