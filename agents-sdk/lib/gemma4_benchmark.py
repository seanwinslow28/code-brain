"""Multi-model benchmark harness for Phase 6 A.3–A.7.

Given a task (e.g., "inbox_triage"), a golden set of prompt+expected records,
and an extractor that turns a model response into a list of entities, this
runs N samples against a model via the HybridRouter, records per-sample
latency/tokens_out/extracted/expected, and emits p50/p95 + Jaccard quality.

Writes `agents-sdk/benchmarks/results/gemma4-benchmark-<YYYY-MM-DD>.json`.

Veto gate: if challenger quality is ≥5% worse than incumbent on a task,
keep the incumbent (see §7.1 of the super-plan).
"""

from __future__ import annotations

import json
import statistics
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable

import httpx

from lib.hybrid_router import HybridRouter, RoutingDecision


@dataclass
class SampleResult:
    sample_id: int
    latency_ms: float
    tokens_out: int
    extracted: list[str]
    expected: list[str]

    @property
    def jaccard(self) -> float:
        return compute_jaccard(self.extracted, self.expected)


@dataclass
class BenchmarkResult:
    model: str
    machine: str
    task: str
    samples: list[SampleResult] = field(default_factory=list)

    @property
    def latencies(self) -> list[float]:
        return [s.latency_ms for s in self.samples]

    @property
    def mean_quality(self) -> float:
        if not self.samples:
            return 0.0
        return statistics.mean(s.jaccard for s in self.samples)


# ─── pure helpers ─────────────────────────────────────────────────────

def compute_jaccard(a: list[str], b: list[str]) -> float:
    """Jaccard similarity over two bags of strings. Empty-both = 1.0."""
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    union = sa | sb
    if not union:
        return 0.0
    return len(sa & sb) / len(union)


def latency_percentiles(samples: list[float]) -> dict[str, float]:
    if not samples:
        return {"p50": 0.0, "p95": 0.0, "min": 0.0, "max": 0.0, "mean": 0.0}
    s = sorted(samples)
    n = len(s)

    def _pct(p: float) -> float:
        # Nearest-rank for small n; matches common benchmark conventions.
        k = max(0, min(n - 1, int(round(p * (n - 1)))))
        return s[k]

    return {
        "p50": _pct(0.50),
        "p95": _pct(0.95),
        "min": s[0],
        "max": s[-1],
        "mean": statistics.mean(s),
    }


def veto_gate_decision(
    *, incumbent: float, challenger: float, threshold: float = 0.05
) -> str:
    """Return 'swap' or 'keep' per Phase 6 veto rule.

    Plan §A.6: "if Gemma 4 quality ≥5% worse than incumbent, keep incumbent."
    Strict improvement → swap. Tie or any regression → keep (covers the ≥5%
    veto case AND any smaller regression — we won't swap for noise either).

    `threshold` is retained so the spec stays readable even though the
    current rule (strict-better-wins) doesn't branch on it.
    """
    del threshold
    return "swap" if challenger > incumbent else "keep"


def summarize_results(results: list[BenchmarkResult]) -> dict[str, Any]:
    """Collapse BenchmarkResults into the output JSON schema."""
    out: dict[str, dict[str, dict[str, Any]]] = {}
    for r in results:
        task_bucket = out.setdefault(r.task, {})
        pcts = latency_percentiles(r.latencies)
        task_bucket[r.model] = {
            "machine": r.machine,
            "samples": len(r.samples),
            "quality": round(r.mean_quality, 4),
            "p50_ms": round(pcts["p50"], 2),
            "p95_ms": round(pcts["p95"], 2),
            "mean_ms": round(pcts["mean"], 2),
            "min_ms": round(pcts["min"], 2),
            "max_ms": round(pcts["max"], 2),
            "per_sample": [asdict(s) for s in r.samples],
        }
    return out


# ─── runtime ────────────────────────────────────────────────────────────

async def _call_model(
    decision: RoutingDecision,
    prompt: str,
    timeout_s: float,
) -> dict[str, Any]:
    """Call a model via Ollama (/api/generate) or OpenAI-compat (/v1/chat/completions).

    Returns {"text": str, "tokens_out": int, "latency_ms": float}.
    """
    start = time.monotonic()
    async with httpx.AsyncClient(timeout=timeout_s) as client:
        if decision.runtime == "ollama":
            resp = await client.post(
                f"{decision.base_url}/api/generate",
                json={"model": decision.model, "prompt": prompt, "stream": False},
            )
            resp.raise_for_status()
            data = resp.json()
            text = data.get("response", "")
            tokens_out = int(data.get("eval_count", 0))
        elif decision.runtime in ("mlx-lm", "lm-studio"):
            resp = await client.post(
                f"{decision.base_url}/v1/chat/completions",
                json={
                    "model": decision.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            tokens_out = int(data.get("usage", {}).get("completion_tokens", 0))
        else:
            raise ValueError(f"Unsupported runtime: {decision.runtime}")
    latency_ms = (time.monotonic() - start) * 1000.0
    return {"text": text, "tokens_out": tokens_out, "latency_ms": latency_ms}


async def run_benchmark(
    *,
    router: HybridRouter,
    task: str,
    golden_set: list[dict[str, Any]],
    extractor: Callable[[str], list[str]],
    per_sample_timeout_s: float = 60.0,
    call_model: Callable[[RoutingDecision, str, float], Awaitable[dict]] | None = None,
) -> BenchmarkResult:
    """Run all samples against the task's currently-routed model.

    `extractor(text) -> list[str]` turns a model's raw output into the set
    of entities compared to the golden expected[] via Jaccard.
    """
    decision = await router.route(task)
    caller = call_model or _call_model

    samples: list[SampleResult] = []
    for rec in golden_set:
        prompt = rec.get("prompt", "")
        expected = list(rec.get("expected", []))
        try:
            resp = await caller(decision, prompt, per_sample_timeout_s)
        except Exception as exc:
            samples.append(
                SampleResult(
                    sample_id=int(rec.get("id", len(samples))),
                    latency_ms=-1.0,
                    tokens_out=0,
                    extracted=[],
                    expected=expected,
                )
            )
            continue
        extracted = extractor(resp["text"])
        samples.append(
            SampleResult(
                sample_id=int(rec.get("id", len(samples))),
                latency_ms=float(resp.get("latency_ms", 0.0)),
                tokens_out=int(resp.get("tokens_out", 0)),
                extracted=extracted,
                expected=expected,
            )
        )

    return BenchmarkResult(
        model=decision.model,
        machine=decision.machine,
        task=task,
        samples=samples,
    )


def write_results_json(summary: dict[str, Any], out_dir: Path, date_str: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"gemma4-benchmark-{date_str}.json"
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return path
