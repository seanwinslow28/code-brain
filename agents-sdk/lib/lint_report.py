"""Parse knowledge-lint reports for daily_driver morning-brief surfacing.

Phase 6 D.3.d: pull the latest `vault/health/YYYY-MM-DD-lint-report.md`,
return a one-line summary with CRITICAL + HIGH counts, and a deep link.
No report or all-PASS → 'PASS ✓'.

Phase D (v3.20.0, 2026-05-01): adds `latest_synth_manifest` +
`synth_health_summary` for the same morning-brief slot. The two functions
are siblings — `vault_health_summary` reports lint findings, the new
`synth_health_summary` reports the most recent vault_synthesizer run's
counts (concepts, connections, edges, rejected). Daily-driver wires both.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_SEVERITY_HEADER_RE_TMPL = r"^##\s+{sev}\s+\((\d+)\)"


def latest_lint_report(vault_root: Path) -> Path | None:
    """Return newest `vault/health/*-lint-report.md` or None."""
    health_dir = vault_root / "health"
    if not health_dir.exists():
        return None
    reports = sorted(health_dir.glob("*-lint-report.md"))
    return reports[-1] if reports else None


def _count(text: str, sev: str) -> int:
    m = re.search(_SEVERITY_HEADER_RE_TMPL.format(sev=sev), text, flags=re.MULTILINE)
    return int(m.group(1)) if m else 0


def vault_health_summary(vault_root: Path) -> str:
    report = latest_lint_report(vault_root)
    if not report:
        return "VAULT HEALTH: PASS ✓ (no lint reports yet)"
    try:
        text = report.read_text(encoding="utf-8")
    except OSError:
        return f"VAULT HEALTH: could not read {report.name}"
    critical = _count(text, "CRITICAL")
    high = _count(text, "HIGH")
    if critical == 0 and high == 0:
        return f"VAULT HEALTH: PASS ✓ (latest: {report.name})"
    return (
        f"VAULT HEALTH: {critical} CRITICAL, {high} HIGH issues. "
        f"See {report.as_posix()} for the full report."
    )


def latest_synth_manifest(vault_root: Path) -> Path | None:
    """Return newest `vault/health/synth-manifest-*.json` or None.

    Sorts by name; the manifest filenames embed an ISO date so name-sort
    matches chronological order without inspecting file mtimes (which
    can drift on git checkout).
    """
    health_dir = vault_root / "health"
    if not health_dir.exists():
        return None
    manifests = sorted(health_dir.glob("synth-manifest-*.json"))
    return manifests[-1] if manifests else None


def synth_health_summary(vault_root: Path) -> str:
    """One-line summary of the latest synth-manifest, or '' when missing.

    Returns '' when:
      - no manifest exists (caller suppresses the line)
      - manifest is malformed JSON
      - manifest is unreadable

    Tolerates broken manifests so the daily-driver morning brief never
    crashes on a bad file. Format intentionally short — the caller
    appends it to the existing VAULT HEALTH line.
    """
    manifest = latest_synth_manifest(vault_root)
    if not manifest:
        return ""
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    if not isinstance(data, dict):
        return ""
    return (
        f"last synth: {data.get('concepts_written', 0)} concepts, "
        f"{data.get('connections_written', 0)} connections, "
        f"{data.get('edges_written', 0)} edges, "
        f"{data.get('rejected_count', 0)} rejected "
        f"(see {manifest.as_posix()})"
    )
