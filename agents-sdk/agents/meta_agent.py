"""Meta-Agent / Chief of Staff — monitors the active agent fleet.

Checks the active agents and infrastructure health, then generates a daily
fleet status summary. When operating-model artifacts are wired in (Phase 2,
2026-04-27), the report includes a domain-aware insights section produced
by gemma4:e4b on Mac Mini that ranks fleet activity against Sean's
schedule-recommendations Protect / Automate / Decline lists for all active
domains.

IMPORTANT: Only the 7 currently-active agents in ACTIVE_AGENTS run.
Do NOT attempt to monitor, restart, or re-enable disabled agents.

Machine: Mac Mini (gemma4:e4b for summary generation, local Ollama)
Schedule: Daily at 08:35 (before Daily Driver at 08:45)
Safety: max 10 turns, $0.10 budget cap (LLM call is local → $0.00 actual)

Usage:
    # Dry run (skips LLM call; uses static report only)
    python3 agents/meta_agent.py --dry-run

    # Live run
    python3 agents/meta_agent.py
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable

import httpx

# Add lib to path
SCRIPT_DIR = Path(__file__).parent
SDK_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SDK_ROOT))

from lib.artifact_loader import DOMAINS, load_artifact
from lib.config import Config, load_config


# ─── Constants ────────────────────────────────────────────────────────

ACTIVE_AGENTS = ["vault_indexer", "vault_synthesizer", "deep_researcher", "daily_driver", "knowledge_lint", "flush", "meta_agent"]
DISABLED_AGENT_COUNT = 5  # process_inbox, daily_driver evening/weekly, pr_digest, sprint_health

# Descriptive metadata per active agent — drives the fleet report template.
# Tuple order: (display_name, schedule, machine, cost_label, monthly_cost_usd)
AGENT_METADATA: dict[str, dict[str, str | float]] = {
    "vault_indexer":     {"display": "vault-indexer",         "schedule": "2:00 AM daily",     "machine": "Mac Mini",        "cost_label": "$0.00/run",   "monthly_usd": 0.00},
    "vault_synthesizer": {"display": "vault-synthesizer",     "schedule": "2:30 AM daily",     "machine": "MBP (when awake)","cost_label": "$0.00/run",   "monthly_usd": 0.00},
    "deep_researcher":   {"display": "deep-researcher",       "schedule": "2:45 AM daily",     "machine": "Mac Mini",        "cost_label": "$0.00/run",   "monthly_usd": 0.00},
    "daily_driver":      {"display": "daily-driver morning",  "schedule": "8:45 AM daily",     "machine": "Claude API",      "cost_label": "~$0.40/run",  "monthly_usd": 12.00},
    "knowledge_lint":    {"display": "knowledge-lint",        "schedule": "Sunday 22:00",      "machine": "Mac Mini / MBP",  "cost_label": "$0.00/run",   "monthly_usd": 0.00},
    "flush":             {"display": "session-end-flush",     "schedule": "hook-triggered",    "machine": "Mac Mini / MBP",  "cost_label": "$0.00/run",   "monthly_usd": 0.00},
    "meta_agent":        {"display": "meta-agent",            "schedule": "8:35 AM daily",     "machine": "local",           "cost_label": "$0.00/run",   "monthly_usd": 0.00},
}
BATON_DIR = Path.home() / ".claude" / "batons"
LOG_DIR_BASE = Path.home() / "Code-Brain" / "claude-code-superuser-pack" / "vault" / "90_system" / "agent-logs"
HISTORY_FILE_NAME = "agent-run-history.csv"
HEALTH_WINDOW_HOURS = 26  # default: 24h + 2h buffer for schedule variance

# Per-agent overrides for HEALTH_WINDOW_HOURS. Daily agents take the default;
# weekly knowledge-lint needs 168h + buffer; hook-triggered flush has no
# fixed cadence so we widen the window enough to absorb a quiet weekend.
_STALE_AFTER_HOURS: dict[str, int] = {
    "knowledge_lint": 192,  # Sunday 22:00 weekly + 24h buffer
    "flush":          72,   # hook-triggered, allows quiet stretches
}

# Status values written by lib.logging_setup.record_run, mapped to fleet
# health. recursion-guard rows come from flush.py self-protecting against
# re-entry on rapid SessionEnd hook fires — that's normal idle behavior.
# empty-queue is deep-researcher with no work to do.
_HEALTHY_CSV_STATUSES = {"success", "empty-queue", "recursion-guard"}
_ERROR_CSV_STATUSES = {"error"}
VAULT_ROOT = Path.home() / "Code-Brain" / "claude-code-superuser-pack" / "vault"
FLEET_STATE_DIR = VAULT_ROOT / "02_Areas" / "Agent-Fleet"

MAC_MINI_OLLAMA = "http://192.168.68.200:11434"
ALIENWARE_OLLAMA = "http://192.168.68.201:11434"
ALIENWARE_COMFYUI = "http://192.168.68.201:8188"

# Phase 2 (2026-04-27): meta-agent summary generation routes to gemma4:e4b
# on Mac Mini. Same model flush.py uses via inbox_triage routing — local
# Ollama, $0.00/run, no cloud egress of schedule-recs content.
SUMMARY_MODEL = "gemma4:e4b"
SUMMARY_TIMEOUT_S = 180.0

MAX_TURNS = 10
MAX_BUDGET_USD = 0.10


# ─── Health Checks ───────────────────────────────────────────────────

def _read_run_history(history_file: Path) -> list[dict[str, str]]:
    """Read all rows from agent-run-history.csv.

    Returns an empty list if the file is missing.
    """
    if not history_file.exists():
        return []
    with open(history_file, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _latest_row_for_agent(rows: list[dict[str, str]], agent_name: str) -> dict[str, str] | None:
    """Return the most recent CSV row for `agent_name`.

    The CSV stores agent names with hyphens (deep-researcher, vault-indexer);
    callers may pass either hyphen or underscore form.
    """
    candidates = {agent_name, agent_name.replace("_", "-"), agent_name.replace("-", "_")}
    matching = [r for r in rows if (r.get("agent") or "") in candidates]
    if not matching:
        return None
    # CSV is append-only chronologically, but parse the timestamp
    # explicitly so out-of-order rows (or test fixtures) still pick the
    # latest one.
    def _ts(r: dict[str, str]) -> str:
        return f"{r.get('date', '')} {r.get('time', '')}"
    return max(matching, key=_ts)


def check_agent_health(agent_name: str, config: dict, dry_run: bool = False) -> dict[str, Any]:
    """Check if an agent ran successfully recently per agent-run-history.csv.

    The CSV (written by `lib.logging_setup.record_run`) is the single source
    of truth: one row per agent run with status, cost, duration, turns, and
    notes. We pick the latest row for the agent and check both status and
    age against `HEALTH_WINDOW_HOURS`.

    `meta_agent` itself is special — it doesn't `record_run` on itself, so
    we report it as healthy-running-now to avoid the report flagging the
    very agent that just generated it.
    """
    result: dict[str, Any] = {
        "agent": agent_name,
        "status": "unknown",
        "last_run": None,
        "details": "",
        "cost_usd": None,
        "duration_ms": None,
    }

    if dry_run:
        result["status"] = "healthy (dry-run)"
        result["last_run"] = datetime.now().isoformat()
        result["details"] = "Dry run — skipping actual log check"
        return result

    if agent_name == "meta_agent":
        result["status"] = "healthy"
        result["last_run"] = datetime.now().isoformat()
        result["details"] = "Generating this report now"
        return result

    rows = _read_run_history(LOG_DIR_BASE / HISTORY_FILE_NAME)
    row = _latest_row_for_agent(rows, agent_name)

    if row is None:
        result["status"] = "no-data"
        result["details"] = f"No rows in {HISTORY_FILE_NAME} for {agent_name}"
        return result

    csv_status = (row.get("status") or "").strip()
    mode = (row.get("mode") or "").strip()
    cost_raw = (row.get("cost_usd") or "").strip()
    duration_raw = (row.get("duration_ms") or "").strip()
    notes = (row.get("notes") or "").strip()

    if cost_raw:
        try:
            result["cost_usd"] = float(cost_raw)
        except ValueError:
            pass
    if duration_raw:
        try:
            result["duration_ms"] = int(duration_raw)
        except ValueError:
            pass

    age_hours: float | None
    try:
        ts = datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %H:%M:%S")
        result["last_run"] = ts.isoformat()
        age_hours = (datetime.now() - ts).total_seconds() / 3600
        age_str = f"{age_hours:.1f}h ago"
    except (KeyError, ValueError):
        age_hours = None
        age_str = "age unknown"

    stale_threshold = _STALE_AFTER_HOURS.get(agent_name, HEALTH_WINDOW_HOURS)
    if csv_status in _ERROR_CSV_STATUSES:
        result["status"] = "error"
    elif csv_status in _HEALTHY_CSV_STATUSES:
        if age_hours is not None and age_hours > stale_threshold:
            result["status"] = "stale"
        else:
            result["status"] = "healthy"
    else:
        result["status"] = csv_status or "unknown"

    detail_bits = [f"status={csv_status}", age_str]
    if mode:
        detail_bits.insert(1, f"mode={mode}")
    if cost_raw and cost_raw not in ("0.0000", "0", ""):
        detail_bits.append(f"cost=${cost_raw}")
    if notes:
        snippet = notes.replace("\n", " ").strip()
        if len(snippet) > 80:
            snippet = snippet[:77] + "..."
        detail_bits.append(f"notes='{snippet}'")
    result["details"] = " · ".join(detail_bits)

    return result


def check_daily_note_exists(dry_run: bool = False) -> dict[str, Any]:
    """Check if today's daily note was created (indicates daily-driver ran)."""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_note = VAULT_ROOT / "10_timeline" / "daily" / f"{today}.md"

    if dry_run:
        return {"exists": True, "path": str(daily_note), "dry_run": True}

    return {
        "exists": daily_note.exists(),
        "path": str(daily_note),
    }


def check_machine_online(url: str, dry_run: bool = False) -> dict[str, Any]:
    """Ping an Ollama endpoint to check if a machine is online."""
    if dry_run:
        return {"url": url, "online": True, "dry_run": True}

    try:
        import urllib.request
        req = urllib.request.Request(f"{url}/api/tags", method="GET")
        req.add_header("User-Agent", "meta-agent/1.0")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return {"url": url, "online": resp.status == 200, "status_code": resp.status}
    except Exception as e:
        return {"url": url, "online": False, "error": str(e)}


def check_comfyui(dry_run: bool = False) -> dict[str, Any]:
    """Check if ComfyUI is running on Alienware."""
    if dry_run:
        return {"url": ALIENWARE_COMFYUI, "online": True, "dry_run": True}

    try:
        import urllib.request
        req = urllib.request.Request(f"{ALIENWARE_COMFYUI}/system_stats", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            return {"url": ALIENWARE_COMFYUI, "online": resp.status == 200}
    except Exception as e:
        return {"url": ALIENWARE_COMFYUI, "online": False, "error": str(e)}


# ─── Operating-model artifact wiring (Phase 2, 2026-04-27) ──────────

def build_schedule_recs_context(config: Config | None) -> str:
    """Concatenate schedule-recommendations bodies for all active domains.

    Returns "" when artifacts are globally disabled, the meta_agent has no
    per-agent entry, or schedule-recommendations isn't in its on_demand
    list. Missing or unconfirmed per-domain artifacts map to a placeholder
    line so the LLM still sees structure.
    """
    if config is None:
        return ""
    cfg = config.artifact_config("meta_agent")
    if not cfg:
        return ""
    on_demand = cfg.get("on_demand", [])
    if "schedule-recommendations" not in on_demand:
        return ""

    sections: list[str] = []
    for domain in DOMAINS:
        body = load_artifact(domain, "schedule-recommendations", config.vault_root)
        if body is None:
            sections.append(f"## schedule-recommendations — {domain}\n\n[unavailable]\n")
            continue
        sections.append(f"## schedule-recommendations — {domain}\n\n{body.rstrip()}\n")
    return "\n".join(sections)


def _default_summary_caller(prompt: str) -> str:
    """Local-Ollama call to gemma4:e4b on Mac Mini.

    Returns the raw response string. Network or HTTP errors return "" so
    the summary section falls back to a sentinel rather than crashing the
    whole fleet report.
    """
    try:
        resp = httpx.post(
            f"{MAC_MINI_OLLAMA}/api/generate",
            json={
                "model": SUMMARY_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"num_ctx": 32768},
            },
            timeout=SUMMARY_TIMEOUT_S,
        )
        resp.raise_for_status()
        return resp.json().get("response", "")
    except Exception:
        return ""


_SUMMARY_PROMPT_TEMPLATE = """You are summarizing today's agent-fleet status for Sean's daily ops review.

Use the schedule-recommendations context for the active domains as the
canonical source of his Protect / Automate / Decline lists. Rank what
the active fleet did today against those lists.

Return ONLY a JSON object with these three keys. Each value is a list of
short strings (≤140 chars). Omit obvious filler. No prose outside JSON.

{{
  "aligned":     [...],   // fleet activity that matches a Protect/Automate item
  "misaligned":  [...],   // fleet activity touching a Decline item or not represented
  "suggestions": [...]    // 1–3 concrete next-step ideas grounded in the schedule-recs
}}

--- BEGIN SCHEDULE-RECOMMENDATIONS CONTEXT (active domains) ---

{schedule_recs}

--- END SCHEDULE-RECOMMENDATIONS CONTEXT ---

--- BEGIN FLEET SNAPSHOT (today) ---

{fleet_snapshot}

--- END FLEET SNAPSHOT ---

Respond with ONLY the JSON object, no prose.
"""


def _parse_summary_json(text: str) -> dict[str, list[str]] | None:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        parsed = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    out: dict[str, list[str]] = {}
    for key in ("aligned", "misaligned", "suggestions"):
        val = parsed.get(key, [])
        out[key] = [str(x) for x in val] if isinstance(val, list) else []
    return out


def render_domain_aware_section(parsed: dict[str, list[str]] | None) -> str:
    """Render the LLM result as a markdown section for the fleet report.

    Returns a fallback line if the LLM produced nothing parseable so the
    caller can splice it in unconditionally.
    """
    if parsed is None:
        return (
            "## Domain-Aware Insights\n\n"
            "_Local summary unavailable — gemma4:e4b call returned no parseable JSON. "
            "Static fleet snapshot above remains authoritative._\n"
        )

    def _block(title: str, items: list[str]) -> str:
        if not items:
            return f"### {title}\n\n_(none)_\n"
        body = "\n".join(f"- {it}" for it in items)
        return f"### {title}\n\n{body}\n"

    return (
        "## Domain-Aware Insights\n\n"
        "_Generated by gemma4:e4b on Mac Mini against schedule-recommendations "
        "for creative-studio, life-systems, and job-hunt-2026._\n\n"
        + _block("Aligned with Protect / Automate", parsed.get("aligned", []))
        + "\n"
        + _block("Misaligned or Touching Decline", parsed.get("misaligned", []))
        + "\n"
        + _block("Suggestions", parsed.get("suggestions", []))
    )


def generate_domain_aware_summary(
    *,
    config: Config | None,
    fleet_snapshot: str,
    summary_caller: Callable[[str], str] | None = None,
    dry_run: bool = False,
) -> str:
    """Build and render the LLM-summary section.

    Returns "" when the schedule-recs context is empty (no per-agent entry,
    or globally disabled) so the caller can splice unconditionally.
    """
    schedule_recs = build_schedule_recs_context(config)
    if not schedule_recs:
        return ""

    if dry_run:
        return (
            "## Domain-Aware Insights\n\n"
            "_Dry run — skipped gemma4:e4b call. Schedule-recommendations context "
            f"loaded for {len(DOMAINS)} domains ({len(schedule_recs):,} chars)._\n"
        )

    prompt = _SUMMARY_PROMPT_TEMPLATE.format(
        schedule_recs=schedule_recs,
        fleet_snapshot=fleet_snapshot,
    )
    caller = summary_caller or _default_summary_caller
    response = caller(prompt)
    parsed = _parse_summary_json(response) if response else None
    return render_domain_aware_section(parsed)


# ─── Fleet Status Report ─────────────────────────────────────────────

def generate_fleet_report(
    dry_run: bool = False,
    *,
    config: Config | None = None,
    summary_caller: Callable[[str], str] | None = None,
) -> str:
    """Run all health checks and generate the fleet status report."""
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")

    if config is None:
        try:
            config = load_config()
        except Exception:
            config = None  # health checks still work; LLM section auto-skips

    # Health-check helpers take a dict for legacy reasons; not used today.
    health_cfg: dict = {}

    # Check each active agent
    agent_health: dict[str, dict[str, Any]] = {
        name: check_agent_health(name, health_cfg, dry_run) for name in ACTIVE_AGENTS
    }
    daily_note = check_daily_note_exists(dry_run)

    # Check infrastructure
    mac_mini = check_machine_online(MAC_MINI_OLLAMA, dry_run)
    alienware = check_machine_online(ALIENWARE_OLLAMA, dry_run)
    comfyui = check_comfyui(dry_run)

    # Build per-agent sections
    agent_sections: list[str] = []
    for name in ACTIVE_AGENTS:
        meta = AGENT_METADATA.get(name, {})
        h = agent_health[name]
        display = meta.get("display", name)
        header = f"### {display} ({meta.get('schedule', '—')}, {meta.get('machine', '—')}, {meta.get('cost_label', '—')})"
        lines = [
            header,
            f"- **Status:** {h['status']}",
            f"- **Last run:** {h['last_run'] or 'N/A'}",
            f"- **Details:** {h['details']}",
        ]
        # Extra signal only meaningful for daily_driver
        if name == "daily_driver":
            lines.append(
                f"- **Daily note exists:** {'Yes' if daily_note['exists'] else 'No'} (`{daily_note['path']}`)"
            )
        agent_sections.append("\n".join(lines))

    agents_block = "\n\n".join(agent_sections)

    # Cost projection
    cost_lines: list[str] = []
    total_monthly = 0.0
    for name in ACTIVE_AGENTS:
        meta = AGENT_METADATA.get(name, {})
        monthly = float(meta.get("monthly_usd", 0.0))
        total_monthly += monthly
        label = (
            f"~${monthly:.2f}/month"
            if monthly > 0
            else "$0.00/month (local)"
        )
        cost_lines.append(f"- {meta.get('display', name)}: {label}")
    cost_block = "\n".join(cost_lines)

    active_count = len(ACTIVE_AGENTS)
    total_count = active_count + DISABLED_AGENT_COUNT

    infrastructure_block = (
        "| Machine | Endpoint | Status |\n"
        "|---------|----------|--------|\n"
        f"| Mac Mini | {MAC_MINI_OLLAMA} | {'Online' if mac_mini['online'] else 'OFFLINE'} |\n"
        f"| Alienware | {ALIENWARE_OLLAMA} | {'Online' if alienware['online'] else 'OFFLINE'} |\n"
        f"| ComfyUI | {ALIENWARE_COMFYUI} | {'Online' if comfyui['online'] else 'OFFLINE'} |"
    )

    # Domain-aware insights (Phase 2). Empty string when artifacts are
    # disabled, no per-agent entry, or schedule-recommendations isn't in
    # the on_demand list — report renders unchanged in those cases.
    fleet_snapshot = (
        f"Active agents: {active_count}/{total_count} | Disabled: {DISABLED_AGENT_COUNT}\n\n"
        "Per-agent health:\n\n"
        f"{agents_block}\n\n"
        "Infrastructure:\n\n"
        f"{infrastructure_block}"
    )
    domain_aware_section = generate_domain_aware_summary(
        config=config,
        fleet_snapshot=fleet_snapshot,
        summary_caller=summary_caller,
        dry_run=dry_run,
    )
    domain_aware_block = (
        f"\n{domain_aware_section}\n" if domain_aware_section else ""
    )

    # Build report
    report = f"""# Fleet Status — {today}

**Generated:** {today} {now} by Meta-Agent
**Active agents:** {active_count} of {total_count} | **Disabled:** {DISABLED_AGENT_COUNT}

## Active Agent Health

{agents_block}
{domain_aware_block}
## Infrastructure

{infrastructure_block}

## Disabled Agents Reminder

{DISABLED_AGENT_COUNT} agents disabled per AUDIT-2026-04-09-agent-downsizing.md:
- process-inbox, daily-driver evening/weekly, pr-digest, sprint-health
- **Root causes:** CLIConnectionError in SDK transport, MCP servers unavailable in headless mode
- **Do NOT re-enable** without Sean's explicit approval and fixing the underlying SDK bug

## Cost Projection

{cost_block}
- **Total active fleet:** ~${total_monthly:.2f}/month
"""

    return report


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Meta-Agent fleet health monitor")
    parser.add_argument("--dry-run", action="store_true", help="Skip real health checks")
    args = parser.parse_args()

    try:
        config = load_config()
    except Exception:
        config = None

    print(f"{'=' * 60}")
    print(f"META-AGENT — Fleet Health Monitor")
    print(f"Active agents: {len(ACTIVE_AGENTS)} | Disabled: {DISABLED_AGENT_COUNT}")
    print(f"Budget cap: ${MAX_BUDGET_USD:.2f} | Max turns: {MAX_TURNS}")
    print(f"Summary model: {SUMMARY_MODEL} (Mac Mini, local Ollama)")
    print(f"Dry run: {args.dry_run}")
    print(f"{'=' * 60}\n")

    report = generate_fleet_report(dry_run=args.dry_run, config=config)

    # Write fleet status note
    today = datetime.now().strftime("%Y-%m-%d")
    FLEET_STATE_DIR.mkdir(parents=True, exist_ok=True)

    # Daily status
    daily_path = FLEET_STATE_DIR / f"daily-fleet-status-{today}.md"
    daily_path.write_text(report)
    print(f"Fleet status saved: {daily_path}")

    # Update fleet-state.md (rolling latest)
    state_path = FLEET_STATE_DIR / "fleet-state.md"
    state_path.write_text(report)
    print(f"Fleet state updated: {state_path}")

    # Check for alerts
    alert_needed = False
    for agent_name in ACTIVE_AGENTS:
        health = check_agent_health(agent_name, {}, args.dry_run)
        if health["status"] not in ("healthy", "healthy (dry-run)"):
            alert_needed = True
            print(f"  ALERT: {agent_name} status is {health['status']}")

    if alert_needed:
        BATON_DIR.mkdir(parents=True, exist_ok=True)
        alert_path = BATON_DIR / "fleet_alert.flag"
        alert_path.write_text(f"Fleet alert at {datetime.now().isoformat()}\n")
        print(f"  Alert baton created: {alert_path}")
    else:
        print("  No alerts — all active agents healthy")

    print(f"\n{'─' * 60}")
    print("META-AGENT COMPLETE")

    # Print report summary
    print(report[:500])


if __name__ == "__main__":
    main()
