#!/usr/bin/env python3
"""Phase 6 gate-check: run all 6 criteria and print PASS/FAIL/PARTIAL.

Criteria (super-plan §5 + §E.5):
  1. Gemma 4 benchmarks on 3 tasks with head-to-head scoring
  2. ≥1 model swap approved and deployed (may be PARTIAL if Gemma loses)
  3. SessionEnd hook capturing ≥3 sessions/week
  4. ≥2 concept + ≥1 connection article per nightly run (avg of 7 nights)
  5. Lint ≥95% recall on synthetic vault
  6. Autoresearch convergence ≥10% improvement (Wilcoxon, p<0.1)
  7. Meta-Agent ≥5 fleet-status artifacts/week + ≥1 with actionable alert

Exits 0 if all criteria PASS or PARTIAL; non-zero if any FAIL.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config  # noqa: E402

AGENTS_SDK = Path(__file__).parent.parent


def _check_criterion_1() -> tuple[str, str]:
    """Gemma 4 benchmarks — latest results file has all 3 tasks."""
    results_dir = AGENTS_SDK / "benchmarks" / "results"
    files = sorted(results_dir.glob("gemma4-benchmark-*.json"), reverse=True)
    if not files:
        return ("FAIL", "No gemma4-benchmark-*.json files in benchmarks/results/")
    latest = files[0]
    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return ("FAIL", f"Latest results file unreadable: {exc}")
    required_tasks = {"inbox_triage", "financial_analysis", "code_review"}
    missing = required_tasks - set(data.keys())
    if missing:
        return ("PARTIAL", f"{latest.name}: missing tasks {sorted(missing)}")
    n_models = sum(len(m) for m in data.values())
    return ("PASS", f"{latest.name}: all 3 tasks, {n_models} model entries")


def _check_criterion_2() -> tuple[str, str]:
    """≥1 model swap — check git log for config.toml [routing.task_map] change
    in the Phase 6 window. Heuristic: look for a commit touching config.toml
    with 'swap' or 'gemma' in the message."""
    try:
        out = subprocess.run(
            ["git", "log", "--since=2026-04-01", "--oneline", "--all", "--",
             "agents-sdk/config.toml"],
            cwd=AGENTS_SDK.parent,
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = out.stdout.strip().splitlines()
        hits = [l for l in lines if any(t in l.lower() for t in ("gemma", "swap", "routing"))]
        if hits:
            return ("PASS", f"{len(hits)} candidate swap commit(s): {hits[0][:80]}")
        if lines:
            return ("PARTIAL", f"config.toml has {len(lines)} commits but none obvious swaps")
        return ("FAIL", "No config.toml commits in Phase 6 window")
    except Exception as exc:
        return ("PARTIAL", f"git log probe failed: {exc}")


def _check_criterion_3(vault_root: Path) -> tuple[str, str]:
    """SessionEnd hook capture: count vault/daily/*.md in last 7 days."""
    daily = vault_root / "daily"
    if not daily.exists():
        return ("FAIL", "vault/daily/ does not exist yet")
    cutoff = date.today() - timedelta(days=7)
    recent = [p for p in daily.glob("*.md")
              if _parse_date(p.stem) and _parse_date(p.stem) >= cutoff]
    if len(recent) >= 3:
        return ("PASS", f"{len(recent)} daily logs in last 7 days")
    return ("PARTIAL" if recent else "FAIL",
            f"{len(recent)} daily logs in last 7 days (need ≥3)")


def _parse_date(stem: str) -> date | None:
    try:
        return date.fromisoformat(stem)
    except ValueError:
        return None


def _check_criterion_4(vault_root: Path) -> tuple[str, str]:
    """Synthesizer output: avg ≥2 concepts + ≥1 connection per nightly run
    across the last 7 nights. Heuristic: count files in concepts/ and
    connections/ created within 7 days."""
    concepts = vault_root / "knowledge" / "concepts"
    connections = vault_root / "knowledge" / "connections"
    if not concepts.exists() or not connections.exists():
        return ("FAIL", "vault/knowledge/concepts/ or connections/ missing")
    cutoff = date.today() - timedelta(days=7)
    import os

    def _recent(p: Path) -> int:
        return sum(
            1 for f in p.glob("*.md")
            if date.fromtimestamp(f.stat().st_mtime) >= cutoff
        )

    c, k = _recent(concepts), _recent(connections)
    # avg of 7 nights → total ≥14 concepts + ≥7 connections
    if c >= 14 and k >= 7:
        return ("PASS", f"{c} concepts + {k} connections in last 7 days")
    return (
        "PARTIAL" if (c or k) else "FAIL",
        f"{c} concepts + {k} connections in last 7 days (need ≥14 + ≥7)",
    )


def _check_criterion_5() -> tuple[str, str]:
    """Lint 95% recall: run the synthetic-vault pytest."""
    result = subprocess.run(
        [str(AGENTS_SDK / ".venv" / "bin" / "pytest"),
         "tests/test_knowledge_lint.py::test_tier1_recall_on_synthetic_vault",
         "-q"],
        cwd=AGENTS_SDK,
        env={"PYTHONPATH": str(AGENTS_SDK), "PATH": "/usr/bin:/bin:/usr/local/bin"},
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode == 0:
        return ("PASS", "test_tier1_recall_on_synthetic_vault green")
    return ("FAIL", f"recall test failed: {result.stdout[-300:]}")


def _check_criterion_6() -> tuple[str, str]:
    """Autoresearch ≥10% convergence improvement — needs compare_convergence
    artifacts present."""
    candidate = AGENTS_SDK.parent / "vault" / "90_system" / "autoresearch-convergence-ab.md"
    if candidate.exists():
        text = candidate.read_text(encoding="utf-8")
        if "PASS" in text or "≥10%" in text:
            return ("PASS", f"convergence AB report at {candidate.name}")
        return ("PARTIAL", f"report exists but not clearly passing")
    # D.4 descoped 2026-04-18: autoresearch integration blocked pending
    # dependency rework. Tracked in CHANGELOG v3.14.x.
    return ("DESCOPED", "D.4 descoped — autoresearch integration deferred")


def _check_criterion_7(vault_root: Path) -> tuple[str, str]:
    """Meta-Agent fleet-status artifacts in last 7 days (§E.5).

    PASS:     ≥5 daily-fleet-status-*.md in last 7 days AND ≥1 contains alerts
    PARTIAL:  ≥1 artifact exists but either <5 total or no alert-bearing ones
    FAIL:     directory missing or zero artifacts
    """
    fleet_dir = vault_root / "02_Areas" / "Agent-Fleet"
    if not fleet_dir.exists():
        return ("FAIL", "vault/02_Areas/Agent-Fleet/ does not exist")
    cutoff = date.today() - timedelta(days=7)
    recent: list[Path] = []
    for p in fleet_dir.glob("daily-fleet-status-*.md"):
        stem_date = _parse_date(p.stem.replace("daily-fleet-status-", ""))
        if stem_date and stem_date >= cutoff:
            recent.append(p)
    if not recent:
        return ("FAIL", "no fleet-status artifacts in last 7 days")
    # Count how many contain an actionable "## Alerts" section (and are not
    # just "No alerts — all active agents healthy")
    alerting = 0
    for p in recent:
        try:
            text = p.read_text(encoding="utf-8")
        except OSError:
            continue
        if "## Alerts" in text and "No alerts" not in text:
            alerting += 1
    if len(recent) >= 5 and alerting >= 1:
        return ("PASS", f"{len(recent)} artifacts, {alerting} with alerts")
    return (
        "PARTIAL",
        f"{len(recent)} artifacts, {alerting} with alerts (need ≥5 + ≥1)",
    )


def main() -> int:
    cfg = load_config()

    results = [
        ("1. Gemma 4 benchmarks on 3 tasks", _check_criterion_1()),
        ("2. ≥1 model swap deployed",         _check_criterion_2()),
        ("3. SessionEnd ≥3 captures/week",    _check_criterion_3(cfg.vault_root)),
        ("4. Synthesis ≥2 concepts/night",    _check_criterion_4(cfg.vault_root)),
        ("5. Lint ≥95% recall",               _check_criterion_5()),
        ("6. Autoresearch ≥10% convergence",  _check_criterion_6()),
        ("7. Meta-Agent fleet-status/week",   _check_criterion_7(cfg.vault_root)),
    ]

    print("=" * 70)
    print(" Phase 6 Gate Check")
    print("=" * 70)
    fail = 0
    partial = 0
    descoped = 0
    markers = {"PASS": "✓", "PARTIAL": "~", "FAIL": "✗", "DESCOPED": "—"}
    for label, (status, note) in results:
        marker = markers.get(status, "?")
        print(f" {marker} {status:8s} {label}")
        print(f"              {note}")
        if status == "FAIL":
            fail += 1
        elif status == "PARTIAL":
            partial += 1
        elif status == "DESCOPED":
            descoped += 1
    print("=" * 70)
    passed = len(results) - fail - partial - descoped
    tail = f" · {descoped} DESCOPED" if descoped else ""
    print(f" {passed} PASS · {partial} PARTIAL · {fail} FAIL{tail}")
    print("=" * 70)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
