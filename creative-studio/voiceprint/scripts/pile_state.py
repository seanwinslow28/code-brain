#!/usr/bin/env python3
"""
pile_state.py — read a reader's VoicePrint workspace and report where they are.

Pure standard library. The single source of truth for "what's collected, what's
missing, what's next." Used by build_dashboard.py and runnable on its own for a
quick status line. Never writes; read-only.

Usage:
  python3 pile_state.py --root voiceprint/            # human-readable status
  python3 pile_state.py --root voiceprint/ --json     # machine-readable
"""

import argparse
import json
import sys
from pathlib import Path

STAGES = ["interview", "gauntlet", "mine", "synthesize", "refine"]
STAGE_LABELS = {
    "interview": "Reference-universe interview",
    "gauntlet": "Cheese gauntlet",
    "mine": "Mine pre-AI writing",
    "synthesize": "Generate the voice skill",
    "refine": "Refine loop",
}


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return None


def read_refine_log(work_dir: Path):
    log = work_dir / "refine-log.jsonl"
    rounds = []
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rounds.append(json.loads(line))
            except Exception:
                continue
    return rounds


def summarize(root: Path) -> dict:
    work = root / "_work"
    state = load_json(work / "pile-state.json") or {}
    stages = state.get("stages", {})
    rounds = read_refine_log(work)

    stage_status = {}
    for s in STAGES:
        stage_status[s] = (stages.get(s) or {}).get("status", "not_started")

    # convergence: pct_changed across rounds (lower = the voice is converging)
    trend = [r.get("pct_changed") for r in rounds if r.get("pct_changed") is not None]
    converging = None
    if len(trend) >= 2:
        converging = trend[-1] < trend[0]

    bundle_exists = (root / "my-voice" / "SKILL.md").exists()

    return {
        "root": str(root),
        "reader_label": state.get("reader_label", "anon"),
        "stages": stage_status,
        "refine_rounds": len(rounds),
        "pct_changed_trend": trend,
        "converging": converging,
        "cold_start": (stages.get("mine") or {}).get("cold_start", False),
        "bundle_exists": bundle_exists,
        "next_best_action": state.get("next_best_action"),
    }


def human(summary: dict) -> str:
    lines = [f"VoicePrint — {summary['reader_label']}  ({summary['root']})", ""]
    for s in STAGES:
        st = summary["stages"][s]
        mark = {"complete": "[x]", "incomplete": "[~]", "not_started": "[ ]"}.get(st, "[ ]")
        lines.append(f"  {mark} {STAGE_LABELS[s]} — {st}")
    lines.append("")
    if summary["refine_rounds"]:
        trend = summary["pct_changed_trend"]
        conv = "converging" if summary["converging"] else "not converging yet"
        lines.append(f"  Refine rounds: {summary['refine_rounds']}  |  edit-diff %: {trend}  ({conv})")
    if summary["cold_start"]:
        lines.append("  Note: cold-start — skill is outline-grade until real samples are added.")
    if summary["next_best_action"]:
        lines.append("")
        lines.append(f"  Next: {summary['next_best_action']}")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="Report VoicePrint workspace state.")
    p.add_argument("--root", default="voiceprint", help="path to the voiceprint/ root")
    p.add_argument("--json", action="store_true", help="emit JSON")
    args = p.parse_args(argv)

    root = Path(args.root)
    if not (root / "_work").exists():
        print(f"No VoicePrint workspace at {root}/_work — run /voiceprint-start first.", file=sys.stderr)
        return 1

    summary = summarize(root)
    print(json.dumps(summary, indent=2) if args.json else human(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
