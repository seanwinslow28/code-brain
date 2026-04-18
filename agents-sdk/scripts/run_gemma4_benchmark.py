#!/usr/bin/env python3
"""Phase 6 A.5 — run the 60-sample benchmark across all 3 tasks × all models.

Per task, runs each configured challenger + the incumbent listed in
config.toml [routing.task_map] and emits one JSON summary.

Usage:
    python3 scripts/run_gemma4_benchmark.py                       # all tasks
    python3 scripts/run_gemma4_benchmark.py --task inbox_triage   # single task
    python3 scripts/run_gemma4_benchmark.py --samples 5           # smoke run

Output:
    benchmarks/results/gemma4-benchmark-<YYYY-MM-DD>.json

This script is cheap to re-run — it does NOT modify config.toml. A.6
swap-decision tooling (compare_and_swap.py) is a separate step.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.config import load_config  # noqa: E402
from lib.gemma4_benchmark import (  # noqa: E402
    BenchmarkResult,
    run_benchmark,
    summarize_results,
    write_results_json,
)
from lib.hybrid_router import HybridRouter, RoutingDecision  # noqa: E402

TASKS = ["inbox_triage", "financial_analysis", "code_review"]

# Challenger matrix per task — incumbent is read from config.toml at runtime.
# Note: gemma4:26b on Mac Mini was tested in an earlier pass and timed out
# on every sample (Mac Mini M4 Pro 24GB cannot fit the 26B MoE with usable
# latency — cold-prompt infer ~100s, long-prompt inferences exceed 120s).
# Per the plan §7.1 veto gate, that's a >5% regression → keep incumbent.
# Only the MBP-resident gemma4-31b is still a live challenger here.
CHALLENGERS: dict[str, list[tuple[str, str]]] = {
    "inbox_triage": [
        ("gemma4-31b", "macbook_pro"),
    ],
    "financial_analysis": [
        ("gemma4-31b", "macbook_pro"),
    ],
    "code_review": [
        ("gemma4-31b", "macbook_pro"),
    ],
}


def _lowercase_tokens(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z0-9-]*", text.lower())


def _extract_entities_generic(text: str, expected: list[str]) -> list[str]:
    """Golden-set-agnostic extractor: keep any expected-list token that
    appears as a whole word in the model's response (case-insensitive).

    This is what the plan calls "Jaccard on extracted entities" — if the
    model's text mentions the expected token, credit it.
    """
    lowered = text.lower()
    tokens = set()
    for exp in expected:
        pattern = rf"\b{re.escape(exp.lower())}\b"
        if re.search(pattern, lowered):
            tokens.add(exp.lower())
    return sorted(tokens)


def _golden_path(repo_root: Path, task: str) -> Path:
    return repo_root / "benchmarks" / "golden_sets" / f"{task}.json"


def _load_golden(repo_root: Path, task: str, limit: int | None) -> list[dict]:
    raw = json.loads(_golden_path(repo_root, task).read_text(encoding="utf-8"))
    samples = raw.get("samples", [])
    if limit is not None:
        samples = samples[:limit]
    return samples


async def _run_one(
    router: HybridRouter,
    task: str,
    samples: list[dict],
    override: tuple[str, str] | None,
) -> BenchmarkResult:
    """Run one (task, model, machine) combo.

    If `override` is set, temporarily patch `router.task_map[task]` so
    run_benchmark resolves to the challenger rather than the incumbent.
    """
    original = router.task_map.get(task, {}).copy()
    if override:
        model, machine = override
        router.task_map[task] = {"model": model, "machine": machine}
    try:
        samples_with_expected = samples  # pass through; extractor uses rec.expected
        result = await run_benchmark(
            router=router,
            task=task,
            golden_set=samples_with_expected,
            extractor=lambda text: _extract_entities_generic(
                text, expected=[]  # filled per-sample below
            ),
        )
        # Re-compute extracted per sample with the sample's expected list.
        # (run_benchmark already ran the model calls — we just rescore.)
        for idx, s in enumerate(result.samples):
            rec = samples[idx] if idx < len(samples) else {}
            s.extracted = _extract_entities_generic(
                # we don't have the raw text at rescore — the extractor was
                # called inside run_benchmark; but since we passed an empty
                # expected list, `extracted` is already []. Re-run with the
                # sample's expected list by doing a second pass: we'll call
                # the model again — but to avoid double-latency, we keep the
                # first-pass latency and just fall back to expected presence
                # check against the per_sample text stored on result.
                # In the simple case here, the model response text is not
                # retained by run_benchmark, so second-pass scoring isn't
                # available. Use the same heuristic: extracted=expected on
                # the assumption the extractor was run correctly first pass.
                "", expected=list(rec.get("expected", []))
            )
        return result
    finally:
        if override:
            router.task_map[task] = original


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", default=None, choices=TASKS + [None])
    parser.add_argument("--samples", type=int, default=None, help="Cap samples per task for smoke runs")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    cfg = load_config()
    repo_root = Path(__file__).parent.parent  # agents-sdk/

    # Load raw config.toml for router
    import tomllib
    with open(repo_root / "config.toml", "rb") as f:
        raw_cfg = tomllib.load(f)
    router = HybridRouter.from_config(raw_cfg)

    tasks = [args.task] if args.task else TASKS
    all_results: list[BenchmarkResult] = []

    for task in tasks:
        samples = _load_golden(repo_root, task, args.samples)
        print(f"\n=== {task} — {len(samples)} samples ===")

        # Incumbent (as configured in config.toml)
        inc = router.task_map.get(task, {})
        print(f"  incumbent: {inc.get('model')} @ {inc.get('machine')}")
        try:
            inc_result = await run_benchmark_with_text(router, task, samples, override=None)
            all_results.append(inc_result)
            print(f"    quality={inc_result.mean_quality:.3f} "
                  f"p50={_pct(inc_result, 50):.0f}ms p95={_pct(inc_result, 95):.0f}ms")
        except Exception as exc:
            print(f"  INCUMBENT FAILED: {exc}")

        # Challengers
        for challenger in CHALLENGERS.get(task, []):
            print(f"  challenger: {challenger[0]} @ {challenger[1]}")
            try:
                ch_result = await run_benchmark_with_text(
                    router, task, samples, override=challenger
                )
                all_results.append(ch_result)
                print(f"    quality={ch_result.mean_quality:.3f} "
                      f"p50={_pct(ch_result, 50):.0f}ms p95={_pct(ch_result, 95):.0f}ms")
            except Exception as exc:
                print(f"  CHALLENGER FAILED: {exc}")

    summary = summarize_results(all_results)
    today = date.today().isoformat()
    out_dir = repo_root / "benchmarks" / "results"
    out_path = Path(args.out) if args.out else write_results_json(summary, out_dir, today)
    print(f"\nWrote {out_path}")
    return 0


def _pct(result: BenchmarkResult, pct: int) -> float:
    ls = sorted(result.latencies)
    if not ls:
        return 0.0
    idx = max(0, min(len(ls) - 1, int(round(pct / 100 * (len(ls) - 1)))))
    return ls[idx]


async def run_benchmark_with_text(
    router: HybridRouter,
    task: str,
    samples: list[dict],
    override: tuple[str, str] | None,
) -> BenchmarkResult:
    """Wrapper that captures model text into each SampleResult.extracted."""
    import time
    import httpx
    from lib.gemma4_benchmark import BenchmarkResult, SampleResult

    original = router.task_map.get(task, {}).copy()
    if override:
        model, machine = override
        router.task_map[task] = {"model": model, "machine": machine}
    try:
        decision = await router.route(task)
        results: list[SampleResult] = []
        for rec in samples:
            prompt = rec.get("prompt", "")
            expected = list(rec.get("expected", []))
            t0 = time.monotonic()
            try:
                async with httpx.AsyncClient(timeout=300.0) as client:
                    if decision.runtime == "ollama":
                        resp = await client.post(
                            f"{decision.base_url}/api/generate",
                            json={"model": decision.model, "prompt": prompt, "stream": False},
                        )
                        resp.raise_for_status()
                        data = resp.json()
                        text = data.get("response", "")
                        tokens_out = int(data.get("eval_count", 0))
                    else:
                        resp = await client.post(
                            f"{decision.base_url}/v1/chat/completions",
                            json={
                                "model": decision.model,
                                "messages": [{"role": "user", "content": prompt}],
                                "stream": False,
                            },
                        )
                        resp.raise_for_status()
                        j = resp.json()
                        text = j["choices"][0]["message"]["content"]
                        tokens_out = int(j.get("usage", {}).get("completion_tokens", 0))
                latency_ms = (time.monotonic() - t0) * 1000
                extracted = _extract_entities_generic(text, expected)
            except Exception as exc:
                print(f"    sample {rec.get('id')} error: {exc}")
                extracted = []
                latency_ms = -1.0
                tokens_out = 0
            results.append(
                SampleResult(
                    sample_id=int(rec.get("id", len(results))),
                    latency_ms=latency_ms,
                    tokens_out=tokens_out,
                    extracted=extracted,
                    expected=expected,
                )
            )
        return BenchmarkResult(
            model=decision.model,
            machine=decision.machine,
            task=task,
            samples=results,
        )
    finally:
        if override:
            router.task_map[task] = original


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
