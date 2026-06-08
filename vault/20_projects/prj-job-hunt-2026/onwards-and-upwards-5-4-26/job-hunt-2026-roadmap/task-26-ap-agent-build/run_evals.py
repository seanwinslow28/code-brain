"""
run_evals.py — runner for the AP invoice-approval eval suite.

Usage:
  python run_evals.py            # run against the stub agent (Session A tree) -> expect 10/10
  python run_evals.py --naive    # run against a naive approve-all agent -> expect failures

The --naive run is the BITE TEST: a suite that also passes on a broken agent
has no teeth. The naive agent auto-approves everything, so every non-happy
case must fail.
"""
import os
import sys
import yaml

from stub_agent import decide


def naive_decide(_inv):
    """A broken baseline: approve everything. Used only to prove the suite has bite."""
    return {"level": "L1", "action": "auto_approve", "flags": []}


def check(case, out):
    errs = []
    if out["level"] != case["expected_level"]:
        errs.append(f"level {out['level']} != expected {case['expected_level']}")
    auto = out["action"] == "auto_approve"
    if auto != case.get("expect_auto_approve", False):
        errs.append(f"auto_approve={auto} but expected {case.get('expect_auto_approve', False)}")
    for f in (case.get("expect_flags") or []):
        if not any(f in af for af in out["flags"]):
            errs.append(f"missing expected flag '{f}' (got {out['flags']})")
    return errs


def main():
    naive = "--naive" in sys.argv
    agent = naive_decide if naive else decide
    label = "NAIVE approve-all agent" if naive else "stub agent (Session A tree)"

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "eval-suite.yaml")) as fh:
        suite = yaml.safe_load(fh)
    cases = suite["cases"]

    print(f"Running {len(cases)} cases against: {label}\n")
    npass = 0
    for c in cases:
        out = agent(c["input"])
        errs = check(c, out)
        ok = not errs
        npass += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {c['id']:30s} -> {out['level']:3s} {out['action']}")
        for e in errs:
            print(f"         - {e}")

    print(f"\n{npass}/{len(cases)} passed")
    sys.exit(0 if npass == len(cases) else 1)


if __name__ == "__main__":
    main()
