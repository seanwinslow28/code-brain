#!/usr/bin/env python3
"""Run the $0 instruments over every spread-run draft and emit measurements.json.

Analyzer dashboard (writing-critique) + origin/claims check (content-machine gate),
plus raw shape stats. Nothing here judges; it reports.
"""
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ANALYZE = ROOT / ".claude/skills/writing-critique/references/analyze.py"
ORIGIN = ROOT / ".claude/skills/content-machine/gates/origin_check.py"
BASELINE = ROOT / ".claude/skills/writing-critique/references/baseline.json"
BAND = ROOT / ".claude/skills/writing-critique/references/rewrite-band.json"
TRANSCRIPT = ROOT / "creative-studio/content-machine/transcripts/2026-08-27-deleted-the-author-modes.md"


def jrun(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 1) or not p.stdout.strip():
        return {"_error": (p.stderr or p.stdout or f"rc={p.returncode}")[:300]}
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"_error": "non-json output", "_raw": p.stdout[:300]}


def main() -> None:
    out = {}
    for f in sorted(HERE.glob("drafts/*.md")):
        arm = f.stem
        text = f.read_text().strip()
        if not text:
            out[arm] = {"status": "empty"}
            continue
        rec = {"status": "ok", "words": len(text.split()), "path": str(f.relative_to(ROOT))}
        rec["analyzer"] = jrun([sys.executable, str(ANALYZE), str(f), "--json",
                                "--baseline", str(BASELINE), "--rewrite-band", str(BAND)])
        rec["origin"] = jrun([sys.executable, str(ORIGIN), str(f), str(TRANSCRIPT),
                              "--lane", "expressive", "--json"])
        out[arm] = rec
        print(f"{arm:<26} {rec['words']:>5}w", flush=True)
    (HERE / "measurements.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"\nwrote measurements.json ({len(out)} arms)")


if __name__ == "__main__":
    main()
