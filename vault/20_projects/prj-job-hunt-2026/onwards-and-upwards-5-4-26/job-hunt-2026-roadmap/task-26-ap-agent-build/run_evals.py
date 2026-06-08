"""
run_evals.py — runner for the AP invoice-approval eval suite.

Usage:
  python run_evals.py            # run against the stub agent (Session A tree)
  python run_evals.py --naive    # run against a naive approve-all agent (bite test)

Two ideas make this a serious suite, not a checkbox:

1. BITE TEST (--naive): a suite that also passes on a broken agent measures
   nothing. The naive agent approves everything, so every case that should NOT
   auto-approve must fail.

2. KNOWN STUB LIMITATIONS (xfail): some cases test PRECISION — that a legit
   invoice is NOT over-escalated. The keyword-based stub is too crude to pass
   those, so they are marked `stub_limitation: true` and reported as XFAIL
   (expected to fail on the stub, would pass on a real classifier). An XFAIL is
   not a suite failure — it is documentation of where the stub ends and the
   production agent must begin.
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
    npass = nfail = nxfail = nxpass = 0
    for c in cases:
        out = agent(c["input"])
        errs = check(c, out)
        # stub_limitation cases are expected to fail on the stub, not on naive.
        is_xfail = c.get("stub_limitation", False) and not naive

        if is_xfail:
            if errs:
                status, nxfail = "XFAIL", nxfail + 1
            else:
                status, nxpass = "XPASS", nxpass + 1
        elif errs:
            status, nfail = "FAIL", nfail + 1
        else:
            status, npass = "PASS", npass + 1

        print(f"[{status:5s}] {c['id']:30s} -> {out['level']:3s} {out['action']}")
        if status == "FAIL":
            for e in errs:
                print(f"          - {e}")
        elif status == "XFAIL":
            print("          - expected: keyword stub over-flags a benign token; a real classifier passes this")
        elif status == "XPASS":
            print("          - note: stub unexpectedly passed a case marked as a known limitation")

    parts = [f"{npass} passed"]
    if nxfail:
        parts.append(f"{nxfail} xfail (known stub limitation)")
    if nxpass:
        parts.append(f"{nxpass} xpass")
    if nfail:
        parts.append(f"{nfail} FAILED")
    print("\n" + ", ".join(parts))

    # A real FAIL fails the run; XFAIL/XPASS do not.
    sys.exit(0 if nfail == 0 else 1)


if __name__ == "__main__":
    main()
