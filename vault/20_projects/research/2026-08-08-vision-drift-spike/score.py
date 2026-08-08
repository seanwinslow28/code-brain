#!/usr/bin/env python3
"""Score a judge's results against the manifest ground truth + pre-registered bars.

Input file format: {"model": ..., "results": [{"id": ..., "majority": "consistent"|"drifted", ...}]}
(for single-vote judges, "majority" is just the verdict).
"""
import json
import pathlib
import sys

SPIKE = pathlib.Path(__file__).parent
manifest = json.loads((SPIKE / "manifest.json").read_text())
truth = {c["id"]: c for c in manifest["cases"]}

MATERIALS = {  # haircut materials -> (with_note_id, without_note_id)
    "kid": ("X26", "X27"),
    "grandma": ("X28", "X29"),
    "mascot-register": ("X30", "X31"),
}
CONTROL = "X32"


def score(path: str) -> None:
    data = json.loads((SPIKE / path).read_text())
    verdicts = {r["id"]: r["majority"] for r in data["results"]}
    rows = []

    a_ids = [c["id"] for c in manifest["cases"] if c["set"] == "A"]
    b_ids = [c["id"] for c in manifest["cases"] if c["set"] == "B"]

    fa = [i for i in a_ids if verdicts.get(i) != "consistent"]
    hits = [i for i in b_ids if verdicts.get(i) == "drifted"]
    misses = [i for i in b_ids if verdicts.get(i) != "drifted"]

    recall = len(hits) / len(b_ids)
    fa_rate = len(fa) / len(a_ids)

    with_ok = sum(1 for m, (w, _) in MATERIALS.items() if verdicts.get(w) == "consistent")
    without_ok = sum(1 for m, (_, wo) in MATERIALS.items() if verdicts.get(wo) == "drifted")
    control_ok = verdicts.get(CONTROL) == "drifted"

    bar1 = recall >= 0.75
    bar2 = fa_rate <= 0.20
    bar3 = with_ok >= 2 and without_ok >= 2 and control_ok

    print(f"== {data.get('model', path)} ==")
    print(f"Set B drift recall:      {recall:.2f} ({len(hits)}/{len(b_ids)})  bar>=0.75 {'PASS' if bar1 else 'FAIL'}")
    print(f"  misses: {misses} -> {[truth[i]['truth_label'] for i in misses]}")
    print(f"Set A false-alarm rate:  {fa_rate:.2f} ({len(fa)}/{len(a_ids)})  bar<=0.20 {'PASS' if bar2 else 'FAIL'}")
    print(f"  false alarms: {fa}")
    print(f"Haircut: with-note accepted {with_ok}/3, without-note flagged {without_ok}/3, control flagged: {control_ok}")
    print(f"  bar3 {'PASS' if bar3 else 'FAIL'}")
    print(f"ALL BARS: {'GO-grade' if (bar1 and bar2 and bar3) else 'not met'}")
    print()
    per_case = {i: {"verdict": verdicts.get(i), "truth": truth[i]["truth"],
                    "label": truth[i]["truth_label"],
                    "correct": verdicts.get(i) == truth[i]["truth"]}
                for i in verdicts}
    (SPIKE / path).with_suffix(".scored.json").write_text(json.dumps(
        {"model": data.get("model"), "recall": recall, "false_alarm": fa_rate,
         "haircut": {"with_ok": with_ok, "without_ok": without_ok, "control_ok": control_ok},
         "bars": {"recall": bar1, "false_alarm": bar2, "haircut": bar3},
         "per_case": per_case}, indent=2))


if __name__ == "__main__":
    for p in sys.argv[1:]:
        score(p)
