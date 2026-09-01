#!/usr/bin/env python3
"""Rebuild rewrite-band.json — the second dashboard band (#219).

Two bands, and the distinction is the whole point:

  baseline.json      Sean's prose written OUTSIDE the content machine. The
                     yardstick. Rebuilds only on his ruling (build_baseline.py).
  rewrite-band.json  Sean's hand-rewrites THROUGH the machine. The track record.
                     Rebuilds on every ship, automatically. This file.

Keeping them apart is what lets the track record grow without the yardstick ever
being calibrated on the thing it measures — the failure #177 was created to fix.
Nothing here is a gate and nothing downstream reads it; it prints beside the
draft's numbers so Sean can see where a draft sits against what he actually
writes.

Only aggregate statistics are written. No prose lands in a tracked file, the same
discipline baseline.json follows.

    python3 build_rewrite_band.py            # rebuild
    python3 build_rewrite_band.py --check    # still matches the finals on disk?
"""

import argparse
import json
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
STUDIO = REPO / "vault" / "20_projects" / "substack-studio"

# A band needs this many rewrites before it prints as a range. Below it, the
# pieces print as individual labelled points. One piece dressed up as a range is
# how the contaminated 2026-05 baseline read as authoritative on 58 sentences.
N_FLOOR = 3

# The registry: Sean's hand-rewrites, by series. A final enters here when he
# ships it — that is the "rebuilds on every ship" trigger, and it is one line.
# Split by series because the two are different registers, not different quality:
# Raising Agents runs a 43% short-sentence share and no long sentences at all,
# Pencil & Prompt runs 10-20% short and 3-9% long. Pooling them is what made the
# rewrite band look like it spanned eight words of mean and anchored to nothing.
SERIES: dict[str, list[tuple[str, str]]] = {
    "Pencil & Prompt": [
        ("run2 'The Pulitzer Prize Won't Save You'", "author-modes-deleted/final.md"),
        ("run3 'What Are These Guys Even Doing?'", "what-are-these-guys-doing/final.md"),
        ("run4 'I Deleted the Authors'", "rules-off-experiment/arm-b-sean-final.md"),
    ],
    "Raising Agents": [
        ("ep1 'An Agent's Gift'", "raising-agents-ep-1/final.md"),
    ],
}

# run2 and run4 are two hand-rewrites of the SAME story: run4 is the rules-off
# redraft of the run-2 transcript. Both are kept — each is a real rewrite and
# dropping one would quietly shrink the record — but the P&P band is n=3 over two
# distinct stories, and any read of its width should know that.
SHARED_STORY = ["run2 'The Pulitzer Prize Won't Save You'", "run4 'I Deleted the Authors'"]

METRIC_KEYS = ["mean_len", "cv", "short_share", "long_share", "mattr",
               "first_person_rate", "opener_other_pct"]


def piece_metrics(path: Path, analyze) -> dict:
    m = analyze.compute_metrics(str(path))
    sl, ld, pr, op = (m["sentence_length"], m["lexical_diversity"],
                      m["pronouns"], m["openers"])
    return {
        "mean_len": sl["mean"],
        "cv": sl["cv"],
        "short_share": sl["short_share"],
        "long_share": sl["long_share"],
        "mattr": round(ld["mattr"], 4) if ld["mattr"] is not None else None,
        "first_person_rate": pr["first_person_rate"],
        "opener_other_pct": op["other_pct"],
        "sentences": sl["n"],
    }


def aggregate(rows: list[dict]) -> dict:
    out = {}
    for key in METRIC_KEYS:
        vals = [r[key] for r in rows if r.get(key) is not None]
        if not vals:
            continue
        out[key] = {
            "mean": round(statistics.fmean(vals), 4),
            "stdev": round(statistics.pstdev(vals), 4) if len(vals) > 1 else 0.0,
            "min": round(min(vals), 4),
            "max": round(max(vals), 4),
            "n": len(vals),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="verify the committed band still matches the finals on disk")
    ap.add_argument("--out", default=str(Path(__file__).with_name("rewrite-band.json")))
    args = ap.parse_args()

    sys.path.insert(0, str(Path(__file__).parent))
    import analyze  # noqa: E402

    missing = []
    series_out = {}
    for name, entries in SERIES.items():
        rows, pieces = [], []
        for label, rel in entries:
            path = STUDIO / rel
            if not path.is_file():
                missing.append(str(path))
                continue
            met = piece_metrics(path, analyze)
            rows.append(met)
            pieces.append({"label": label, "source": rel, "metrics": met})
        if not pieces:
            continue
        series_out[name] = {
            "n": len(pieces),
            "pieces": pieces,
            # Below the floor there is no band, only points. The dashboard reads
            # `metrics` being null as "print the points instead".
            "metrics": aggregate(rows) if len(rows) >= N_FLOOR else None,
        }

    if missing:
        print("ERROR: registered finals not found:\n  " + "\n  ".join(missing),
              file=sys.stderr)
        return 2

    band = {
        "schema_version": 1,
        "generated_from": "vault/20_projects/substack-studio (aggregate statistics only)",
        "n_floor": N_FLOOR,
        "ticket": "https://github.com/seanwinslow28/code-brain/issues/219",
        "what_this_is": "Sean's hand-rewrites through the content machine. The track "
                        "record, not the yardstick, and not a gate. Recomputed on every "
                        "ship by adding one line to SERIES in build_rewrite_band.py.",
        "shared_story": SHARED_STORY,
        "series": series_out,
    }
    rendered = json.dumps(band, indent=2) + "\n"

    if args.check:
        committed = Path(args.out)
        if not committed.exists():
            print("no committed rewrite band to check against", file=sys.stderr)
            return 1
        same = committed.read_text(encoding="utf-8") == rendered
        print("rewrite band matches the finals" if same
              else "DRIFT: committed rewrite band does not match a fresh build")
        return 0 if same else 1

    Path(args.out).write_text(rendered, encoding="utf-8")
    counts = ", ".join(f"{k} n={v['n']}" for k, v in series_out.items())
    print(f"Wrote rewrite band ({counts}) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
