"""Parse knowledge-lint reports for daily_driver morning-brief surfacing.

Phase 6 D.3.d: pull the latest `vault/health/YYYY-MM-DD-lint-report.md`,
return a one-line summary with CRITICAL + HIGH counts, and a deep link.
No report or all-PASS → 'PASS ✓'.
"""

from __future__ import annotations

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
