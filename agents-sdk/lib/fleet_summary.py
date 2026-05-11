"""Build the Fleet Overnight Digest for the daily note.

Reads the last 24h of vault/90_system/agent-logs/agent-run-history.csv plus
the latest synth manifest and lint report to produce a markdown block that
Daily Driver injects into each morning's daily note at the
<!-- fleet-overnight --> anchor.

Output is intentionally short and link-rich — the daily note is open on
the desktop all day; the digest is meant to be glanced at, not read.

Empty / missing inputs degrade gracefully: a missing CSV returns a "no
runs in last 24h" block; a missing manifest or lint report just omits
that line. The function never raises on malformed rows.
"""

from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path

from .lint_report import latest_lint_report, latest_synth_manifest

AGENT_ORDER = [
    "vault-indexer",
    "vault-synthesizer",
    "deep-researcher",
    "meta-agent",
    "daily-driver",
    "knowledge-lint",
    "flush",
]

AGENT_DISPLAY = {
    "vault-indexer": "Vault Indexer",
    "vault-synthesizer": "Vault Synthesizer",
    "deep-researcher": "Deep Researcher",
    "meta-agent": "Meta-Agent",
    "daily-driver": "Daily Driver",
    "knowledge-lint": "Knowledge Lint",
    "flush": "Session Flush",
}

STATUS_BADGE = {
    "success": "✓",
    "empty-queue": "○ empty queue",
    "recursion-guard": "○ no-op",
    "error": "✗",
}


def _read_recent_runs(repo_root: Path, hours: int = 24, now: datetime | None = None) -> dict[str, dict]:
    """Return {agent_name: latest_run_row_within_window}.

    `now` is injectable for testing. Bad rows are silently skipped.
    """
    csv_path = repo_root / "vault" / "90_system" / "agent-logs" / "agent-run-history.csv"
    if not csv_path.exists():
        return {}
    anchor = now or datetime.now()
    cutoff = anchor - timedelta(hours=hours)
    latest: dict[str, dict] = {}
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ts = datetime.fromisoformat(f"{row['date']}T{row['time']}")
                except (ValueError, KeyError, TypeError):
                    continue
                if ts < cutoff:
                    continue
                agent = (row.get("agent") or "").strip()
                if not agent:
                    continue
                row_with_ts = dict(row)
                row_with_ts["_ts"] = ts
                if agent not in latest or ts > latest[agent]["_ts"]:
                    latest[agent] = row_with_ts
    except OSError:
        return {}
    return latest


def _format_line(agent_key: str, run: dict | None) -> str:
    name = AGENT_DISPLAY.get(agent_key, agent_key)
    if run is None:
        return f"- **{name}** — no run in last 24h"
    status = (run.get("status") or "?").strip()
    badge = STATUS_BADGE.get(status, status)
    time = (run.get("time") or "").strip()
    notes = (run.get("notes") or "").strip()
    notes = notes.strip('"').replace("\n", " ")
    if len(notes) > 110:
        notes = notes[:107] + "..."
    notes_part = f" — {notes}" if notes else ""
    return f"- **{name}** {badge} ({time}){notes_part}"


def build_fleet_overnight_digest(
    repo_root: Path,
    vault_root: Path,
    now: datetime | None = None,
) -> str:
    """Build the Fleet Overnight Digest markdown body.

    Returns the markdown block (no surrounding `##` header — the template
    owns the header). Caller injects this at the <!-- fleet-overnight -->
    anchor in the daily note.
    """
    runs = _read_recent_runs(repo_root, hours=24, now=now)
    today_iso = (now or datetime.now()).date().isoformat()

    lines: list[str] = [
        f"_Last 24h. Live snapshot: [[daily-fleet-status-{today_iso}|today's fleet status]]._",
        "",
    ]

    fleet_status_today = vault_root / "02_Areas" / "Agent-Fleet" / f"daily-fleet-status-{today_iso}.md"

    for agent_key in AGENT_ORDER:
        if agent_key == "meta-agent":
            # meta-agent reads the CSV but does not write to it (it reports
            # itself as healthy-running-now); use today's fleet-status
            # snapshot existence as the success proxy.
            if fleet_status_today.exists():
                lines.append(f"- **Meta-Agent** ✓ — wrote [[daily-fleet-status-{today_iso}]]")
            else:
                lines.append("- **Meta-Agent** — no fleet-status snapshot for today yet")
            continue
        lines.append(_format_line(agent_key, runs.get(agent_key)))

    extras: list[str] = []
    manifest = latest_synth_manifest(vault_root)
    if manifest:
        extras.append(f"- **Synth manifest:** [[{manifest.stem}]]")
    report = latest_lint_report(vault_root)
    if report:
        extras.append(f"- **Latest lint report:** [[{report.stem}]]")

    if extras:
        lines.extend(["", "**Deep links:**", *extras])

    return "\n".join(lines)
