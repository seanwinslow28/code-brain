# Phase 6 A.6 — Swap Decision Report

**Date:** 2026-04-17
**Outcome:** **NO SWAP**
**Status vs. plan Gate Check #2 (≥1 model swap approved and deployed):** **PARTIAL** (per plan §5 fallback: "If Gemma 4 loses all: commit benchmark doc + mark this bullet PARTIAL")

---

## Summary

Phase 6 A.1 pulled Gemma 4 26B MoE to Mac Mini Ollama (18 GB) and Gemma 4 31B dense MLX 4-bit to MacBook Pro LM Studio (28.85 GB). A.5 benchmarks were run against the inbox_triage golden set (5 samples). Results:

| Task | Incumbent | Challenger | Quality Δ | Latency Δ | Verdict |
|---|---|---|---|---|---|
| inbox_triage | phi4-mini-reasoning @ mac_mini (q=0.667, p50=21.2s) | gemma4-31b @ mbp (q=0.567, p50=32.3s) | −15 pp | +53% | **KEEP incumbent** (veto gate fires) |
| inbox_triage | phi4-mini-reasoning @ mac_mini | gemma4:26b @ mac_mini | q=0.000 (every sample ≥120s timeout) | n/a | **KEEP incumbent** (veto) |
| financial_analysis | qwen3-14b @ mbp | gemma4-31b @ mbp | _deferred_ — incumbent run blocked by LM Studio RAM guardrail while gemma4-31b held 28 GB | — | DEFERRED |
| code_review | qwen2.5-coder-32b-instruct @ mbp | gemma4-31b @ mbp | _not run_ — per plan §7.1, challenger tests are optional after inbox_triage veto fires | — | DEFERRED |

## Rule application (plan §A.6 + §7.1)

The plan's veto gate: "if Gemma 4 quality ≥5% worse than incumbent on a task, keep the incumbent — quality over speed." Inbox_triage challenger was **15 percentage points** below incumbent — a decisive veto. Per §7.1, if Gemma 4 does not win inbox_triage by ≥5%, the optional autoresearch function-calling test is skipped and further challenger runs are low-priority.

## Substitution note

The super-plan specified `gemma4:27b` as the Mac Mini challenger. That tag does not exist in the public Ollama registry as of 2026-04-17. The closest match — `gemma4:26b` (26B MoE with 3.8B active params, the spiritual successor to Gemma 3 27B) — was used instead. It would not have met the latency bar in any case: a 26B MoE with MoE dispatch overhead exceeds 120s/sample on Mac Mini M4 Pro 24 GB, even quantized.

## Why the LM Studio RAM guardrail blocked financial_analysis

LM Studio refuses JIT model loads that would push memory past a safe threshold. While `gemma4-31b` (≈29 GB resident) was held loaded for the inbox_triage challenger run, the subsequent `qwen3-14b` JIT-load request (≈8 GB) triggered the guardrail on the 48 GB MBP. Fix for the next attempt: unload the challenger between tasks, or drive load/unload from the benchmark runner itself.

## A.7 config.toml action

**None.** `[routing.task_map]` is unchanged — all incumbents retained:
- `inbox_triage` → `phi4-mini-reasoning @ mac_mini`
- `financial_analysis` → `qwen3-14b @ macbook_pro`
- `code_review` → `qwen2.5-coder-32b-instruct @ macbook_pro`
- `vault_synthesis` → `qwen3-14b @ macbook_pro` (new Phase 6 entry, unchanged by A.6)

## Consequences for Phase 6 gate check

- Criterion 1 (Gemma 4 benchmarks on 3 tasks): **PARTIAL** — inbox_triage head-to-head complete; the other two are runnable once RAM is managed.
- Criterion 2 (≥1 swap deployed): **PARTIAL** — no swap triggered; veto gate behaved correctly.
- Criteria 3–5 (D-track): unaffected by A.6; proceed independently.
- Criterion 6 (autoresearch ≥10%): blocked on Phase 1 completion (pre-existing).

## Future re-runs

If Sean wants a full head-to-head later:

```bash
# Unload gemma4-31b first, then:
lms unload gemma4-31b
cd agents-sdk && PYTHONPATH=. .venv/bin/python3 scripts/run_gemma4_benchmark.py --samples 20
```

The benchmark runner's CHALLENGERS matrix already points at `gemma4-31b` on MBP for all three tasks; sequential load/unload between incumbent and challenger is the only infra change needed.
