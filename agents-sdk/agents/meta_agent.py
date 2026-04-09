"""Meta-Agent / Chief of Staff — monitors the active agent fleet.

Checks the 2 active agents (vault-indexer, daily-driver morning) and
infrastructure health, then generates a daily fleet status summary.

IMPORTANT: Only 2 agents are active per AUDIT-2026-04-09-agent-downsizing.md.
Do NOT attempt to monitor, restart, or re-enable disabled agents.

Machine: Mac Mini (phi4-mini-reasoning for summary generation)
Schedule: Daily at 06:30 (before Daily Driver at 08:45)
Safety: max 10 turns, $0.10 budget cap

Usage:
    # Dry run
    python3 agents/meta_agent.py --dry-run

    # Live run
    python3 agents/meta_agent.py
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Add lib to path
SCRIPT_DIR = Path(__file__).parent
SDK_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SDK_ROOT))

from lib.config import load_config


# ─── Constants ────────────────────────────────────────────────────────

ACTIVE_AGENTS = ["vault_indexer", "daily_driver"]
DISABLED_AGENT_COUNT = 6  # process_inbox, daily_driver evening/weekly, pr_digest, sprint_health, meeting_defender
BATON_DIR = Path.home() / ".claude" / "batons"
LOG_DIR_BASE = Path.home() / "Code-Brain" / "claude-code-superuser-pack" / "vault" / "90_system" / "agent-logs"
VAULT_ROOT = Path.home() / "Code-Brain" / "claude-code-superuser-pack" / "vault"
FLEET_STATE_DIR = VAULT_ROOT / "02_Areas" / "Agent-Fleet"

MAC_MINI_OLLAMA = "http://192.168.68.200:11434"
ALIENWARE_OLLAMA = "http://192.168.68.201:11434"
ALIENWARE_COMFYUI = "http://192.168.68.201:8188"

MAX_TURNS = 10
MAX_BUDGET_USD = 0.10


# ─── Health Checks ───────────────────────────────────────────────────

def check_agent_health(agent_name: str, config: dict, dry_run: bool = False) -> dict[str, Any]:
    """Check if an agent ran successfully in the last 24 hours."""
    result = {
        "agent": agent_name,
        "status": "unknown",
        "last_run": None,
        "details": "",
    }

    if dry_run:
        result["status"] = "healthy (dry-run)"
        result["last_run"] = datetime.now().isoformat()
        result["details"] = "Dry run — skipping actual log check"
        return result

    # Check for recent baton files
    baton_pattern = f"{agent_name}*.baton"
    baton_files = sorted(BATON_DIR.glob(baton_pattern), key=lambda p: p.stat().st_mtime, reverse=True)

    if baton_files:
        latest = baton_files[0]
        mtime = datetime.fromtimestamp(latest.stat().st_mtime)
        age_hours = (datetime.now() - mtime).total_seconds() / 3600

        if age_hours < 26:  # Allow 2h buffer for schedule variance
            result["status"] = "healthy"
            result["last_run"] = mtime.isoformat()
            result["details"] = f"Latest baton: {latest.name} ({age_hours:.1f}h ago)"
        else:
            result["status"] = "stale"
            result["last_run"] = mtime.isoformat()
            result["details"] = f"Latest baton: {latest.name} ({age_hours:.1f}h ago — exceeds 24h window)"
    else:
        # Fallback: check log files
        log_files = sorted(LOG_DIR_BASE.glob(f"*{agent_name}*"), key=lambda p: p.stat().st_mtime, reverse=True)
        if log_files:
            latest = log_files[0]
            mtime = datetime.fromtimestamp(latest.stat().st_mtime)
            result["status"] = "log-only"
            result["last_run"] = mtime.isoformat()
            result["details"] = f"No baton found, but log exists: {latest.name}"
        else:
            result["status"] = "no-data"
            result["details"] = "No baton files or logs found"

    return result


def check_daily_note_exists(dry_run: bool = False) -> dict[str, Any]:
    """Check if today's daily note was created (indicates daily-driver ran)."""
    today = datetime.now().strftime("%Y-%m-%d")
    daily_note = VAULT_ROOT / "01_Journals" / "Daily Notes" / f"{today}.md"

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


# ─── Fleet Status Report ─────────────────────────────────────────────

def generate_fleet_report(dry_run: bool = False) -> str:
    """Run all health checks and generate the fleet status report."""
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")

    config = {}
    try:
        config = load_config()
    except Exception:
        pass

    # Check active agents
    vault_indexer = check_agent_health("vault_indexer", config, dry_run)
    daily_driver = check_agent_health("daily_driver", config, dry_run)
    daily_note = check_daily_note_exists(dry_run)

    # Check infrastructure
    mac_mini = check_machine_online(MAC_MINI_OLLAMA, dry_run)
    alienware = check_machine_online(ALIENWARE_OLLAMA, dry_run)
    comfyui = check_comfyui(dry_run)

    # Build report
    report = f"""# Fleet Status — {today}

**Generated:** {today} {now} by Meta-Agent
**Active agents:** 2 of {2 + DISABLED_AGENT_COUNT} | **Disabled:** {DISABLED_AGENT_COUNT}

## Active Agent Health

### vault-indexer (2:00 AM daily, Mac Mini, $0.00/run)
- **Status:** {vault_indexer['status']}
- **Last run:** {vault_indexer['last_run'] or 'N/A'}
- **Details:** {vault_indexer['details']}

### daily-driver morning (8:45 AM daily, Claude API, ~$0.40/run)
- **Status:** {daily_driver['status']}
- **Last run:** {daily_driver['last_run'] or 'N/A'}
- **Details:** {daily_driver['details']}
- **Daily note exists:** {'Yes' if daily_note['exists'] else 'No'} (`{daily_note['path']}`)

## Infrastructure

| Machine | Endpoint | Status |
|---------|----------|--------|
| Mac Mini | {MAC_MINI_OLLAMA} | {'Online' if mac_mini['online'] else 'OFFLINE'} |
| Alienware | {ALIENWARE_OLLAMA} | {'Online' if alienware['online'] else 'OFFLINE'} |
| ComfyUI | {ALIENWARE_COMFYUI} | {'Online' if comfyui['online'] else 'OFFLINE'} |

## Disabled Agents Reminder

{DISABLED_AGENT_COUNT} agents disabled per AUDIT-2026-04-09-agent-downsizing.md:
- process-inbox, daily-driver evening/weekly, pr-digest, sprint-health, meeting-defender
- **Root causes:** CLIConnectionError in SDK transport, MCP servers unavailable in headless mode
- **Do NOT re-enable** without Sean's explicit approval and fixing the underlying SDK bug

## Cost Projection

- vault-indexer: $0.00/month (local Ollama)
- daily-driver morning: ~$12.00/month ($0.40/day x 30)
- meta-agent: ~$3.00/month ($0.10/day x 30)
- **Total active fleet:** ~$15.00/month
"""

    return report


# ─── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Meta-Agent fleet health monitor")
    parser.add_argument("--dry-run", action="store_true", help="Skip real health checks")
    args = parser.parse_args()

    print(f"{'=' * 60}")
    print(f"META-AGENT — Fleet Health Monitor")
    print(f"Active agents: {len(ACTIVE_AGENTS)} | Disabled: {DISABLED_AGENT_COUNT}")
    print(f"Budget cap: ${MAX_BUDGET_USD:.2f} | Max turns: {MAX_TURNS}")
    print(f"Dry run: {args.dry_run}")
    print(f"{'=' * 60}\n")

    report = generate_fleet_report(dry_run=args.dry_run)

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
        if health["status"] not in ("healthy", "healthy (dry-run)", "log-only"):
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
