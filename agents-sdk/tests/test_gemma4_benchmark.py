"""Tests for lib.gemma4_benchmark — multi-model benchmark harness."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from lib.gemma4_benchmark import (
    BenchmarkResult,
    SampleResult,
    compute_jaccard,
    latency_percentiles,
    run_benchmark,
    summarize_results,
    veto_gate_decision,
)


def test_latency_p50_p95_math() -> None:
    samples = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    p = latency_percentiles(samples)
    assert p["p50"] == pytest.approx(55.0, abs=0.5) or p["p50"] == pytest.approx(
        50.0, abs=5.0
    )
    assert p["p95"] >= 90
    assert p["min"] == 10
    assert p["max"] == 100


def test_jaccard_entity_extraction() -> None:
    a = ["urgent", "meeting", "friday"]
    b = ["urgent", "meeting", "monday"]
    # 2 shared / 4 union = 0.5
    assert compute_jaccard(a, b) == pytest.approx(0.5)
    # Identical
    assert compute_jaccard(a, a) == 1.0
    # Disjoint
    assert compute_jaccard(a, ["x", "y"]) == 0.0
    # Empty both
    assert compute_jaccard([], []) == 1.0


def test_veto_gate_holds_incumbent_on_regression() -> None:
    # 5% exactly = veto (keep incumbent per plan)
    assert veto_gate_decision(incumbent=0.80, challenger=0.76, threshold=0.05) == "keep"
    # 3% regression = also keep (within threshold)
    assert veto_gate_decision(incumbent=0.80, challenger=0.78, threshold=0.05) == "keep"
    # Challenger wins by 10% = swap
    assert veto_gate_decision(incumbent=0.80, challenger=0.88, threshold=0.05) == "swap"
    # Identical = keep (no reason to swap)
    assert veto_gate_decision(incumbent=0.80, challenger=0.80, threshold=0.05) == "keep"


def test_summarize_results_schema() -> None:
    results = [
        BenchmarkResult(
            model="phi4-mini-reasoning",
            machine="mac_mini",
            task="inbox_triage",
            samples=[
                SampleResult(
                    sample_id=i,
                    latency_ms=50 + i,
                    tokens_out=100,
                    extracted=["urgent"],
                    expected=["urgent"],
                )
                for i in range(5)
            ],
        ),
        BenchmarkResult(
            model="gemma4:27b",
            machine="mac_mini",
            task="inbox_triage",
            samples=[
                SampleResult(
                    sample_id=i,
                    latency_ms=40 + i,
                    tokens_out=100,
                    extracted=["urgent"],
                    expected=["urgent"],
                )
                for i in range(5)
            ],
        ),
    ]
    summary = summarize_results(results)
    assert "inbox_triage" in summary
    assert "phi4-mini-reasoning" in summary["inbox_triage"]
    assert "gemma4:27b" in summary["inbox_triage"]
    entry = summary["inbox_triage"]["gemma4:27b"]
    assert {"p50_ms", "p95_ms", "quality", "samples"} <= entry.keys()


def test_results_json_writable(tmp_path: Path) -> None:
    results = [
        BenchmarkResult(
            model="phi4-mini-reasoning",
            machine="mac_mini",
            task="inbox_triage",
            samples=[
                SampleResult(
                    sample_id=0,
                    latency_ms=50,
                    tokens_out=10,
                    extracted=["a"],
                    expected=["a"],
                )
            ],
        )
    ]
    summary = summarize_results(results)
    out_path = tmp_path / "gemma4-benchmark.json"
    out_path.write_text(json.dumps(summary, indent=2))
    loaded = json.loads(out_path.read_text())
    assert "inbox_triage" in loaded


def test_run_benchmark_calls_router() -> None:
    mock_router = AsyncMock()
    mock_router.route.return_value.model = "phi4-mini-reasoning"
    mock_router.route.return_value.machine = "mac_mini"
    mock_router.route.return_value.base_url = "http://fake"
    mock_router.route.return_value.runtime = "ollama"

    golden = [
        {"id": 0, "prompt": "test", "expected": ["a"]},
        {"id": 1, "prompt": "test2", "expected": ["b"]},
    ]

    async def fake_call(decision, prompt, timeout_s):
        return {"text": "contains a", "tokens_out": 5, "latency_ms": 42.0}

    async def go():
        return await run_benchmark(
            router=mock_router,
            task="inbox_triage",
            golden_set=golden,
            extractor=lambda text: ["a"] if "a" in text else [],
            call_model=fake_call,
        )

    result = asyncio.run(go())

    assert result.model == "phi4-mini-reasoning"
    assert result.task == "inbox_triage"
    assert len(result.samples) == 2
    assert result.samples[0].latency_ms == 42.0
