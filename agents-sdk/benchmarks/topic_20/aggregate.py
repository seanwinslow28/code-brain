"""Aggregate raw JSONL benchmark results into per-(model, tier) scorecards.

Reads every *.jsonl in benchmarks/topic_20/results/, groups by (model, tier),
and writes a single markdown table per tier to stdout. Designed to be
imported into the Topic 20 synthesis report.

Distinguishes Ollama records (have eval_count/eval_duration → ollama_tps) from
LM Studio records (have wall_tps, no eval_duration).
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev


RESULTS_DIR = Path(__file__).parent / "results"


def _infer_tier(filename: str) -> str:
    if "tierA" in filename or "lmstudio" in filename:
        return "A"
    if "tierB" in filename:
        return "B"
    if "tierC" in filename:
        return "C"
    return "?"


def _runtime(filename: str) -> str:
    return "LM Studio MLX" if "lmstudio" in filename else "Ollama"


def load_records() -> list[tuple[str, str, list[dict]]]:
    """Returns list of (filename, tier, records)."""
    out = []
    for jl in sorted(RESULTS_DIR.glob("*.jsonl")):
        recs = []
        for line in jl.open():
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        out.append((jl.name, _infer_tier(jl.name), recs))
    return out


def summarize_file(filename: str, tier: str, recs: list[dict]) -> dict:
    runtime = _runtime(filename)
    model = recs[0].get("model", "?") if recs else "?"

    tcs = [r for r in recs if r.get("kind") == "tool_call"]
    tps = [r for r in recs if r.get("kind") == "throughput"]
    nls = [r for r in recs if r.get("kind") == "needle" and not r.get("skipped_reason")]
    pis = [r for r in recs if r.get("kind") == "pi_gotcha"]

    valid = sum(1 for r in tcs if r.get("valid"))
    schema_ok = sum(1 for r in tcs if r.get("schema_match"))

    if runtime == "Ollama":
        tps_vals = [r.get("ollama_tps") for r in tps if r.get("ollama_tps")]
    else:
        tps_vals = [r.get("wall_tps") for r in tps if r.get("wall_tps")]
    tps_vals = [t for t in tps_vals if t]

    needle_pass = sum(1 for r in nls if r.get("recalled"))
    pi_affected = sum(1 for r in pis if r.get("affected"))

    return {
        "file": filename,
        "model": model,
        "tier": tier,
        "runtime": runtime,
        "tool_call_valid": (valid, len(tcs)),
        "tool_call_schema": (schema_ok, len(tcs)),
        "tps_mean": mean(tps_vals) if tps_vals else 0,
        "tps_stdev": stdev(tps_vals) if len(tps_vals) > 1 else 0,
        "needle": (needle_pass, len(nls)),
        "pi_affected": (pi_affected, len(pis)),
    }


def print_markdown() -> None:
    summaries = [summarize_file(fn, tier, recs) for fn, tier, recs in load_records()]
    by_tier: dict[str, list[dict]] = defaultdict(list)
    for s in summaries:
        by_tier[s["tier"]].append(s)

    for tier in ("A", "B", "C"):
        rows = by_tier.get(tier, [])
        if not rows:
            continue
        rows.sort(key=lambda s: (-s["tool_call_schema"][0], -s["tps_mean"]))
        print(f"\n## Tier {tier} scorecard ({rows[0]['runtime']})\n")
        print("| Model | Valid JSON | Schema match | Tok/s mean ± σ | 32K Needle | Pi gotchas |")
        print("|---|---|---|---|---|---|")
        for s in rows:
            v, vt = s["tool_call_valid"]
            sm, smt = s["tool_call_schema"]
            tps = f"{s['tps_mean']:.1f}"
            if s["tps_stdev"]:
                tps += f" ± {s['tps_stdev']:.1f}"
            nd, ndt = s["needle"]
            pi, pit = s["pi_affected"]
            needle_str = f"{nd}/{ndt}" if ndt else "—"
            print(
                f"| `{s['model']}` | {v}/{vt} | "
                f"**{sm}/{smt}** ({sm*100//smt if smt else 0}%) | "
                f"{tps} | {needle_str} | {pi}/{pit} |"
            )


if __name__ == "__main__":
    print_markdown()
