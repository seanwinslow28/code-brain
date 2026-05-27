---
title: "Runtime-Model Coupling"
type: concept
sources:
  - 20_projects/research/2026-05-26-topic-20-mbp-ollama-runtime-comparison.md
tags: [auto-generated, phase-6]
created: 2026-05-27
updated: 2026-05-27
---

## Definition

Runtime-Model Coupling is the phenomenon where the functional capability of a model is not an intrinsic property of the weights alone, but is strictly gated by the inference engine's configuration. When a runtime lacks a specific control flag (such as disabling chain-of-thought), the model's output distribution shifts in ways that degrade structural constraints like JSON schema adherence. This creates a dependency where the 'correct' model for a task is contingent on the specific runtime environment, rather than the model's architecture or parameter count.

## Context

This matters to Sean because his agent fleet relies on deterministic schema outputs for tasks like vault synthesis and job-feed scoring. If he switches runtimes without auditing model-specific behavior, he risks silent failures where the model 'works' but violates the strict JSON structures required by his MCP servers.

## Evidence

> the hypothesis ("Ollama think:false will recover capability lost to LM Studio's missing thinking-disable") is partially confirmed and partially refuted — gains range from +25 pp to -25 pp depending on the model.

> qwen3.6:27b | 50 %, 14.4 tok/s, 0/5 needle | 25 %, 8.8 tok/s, 5/5 | 20 %, 7.8 tok/s, 5/5 | -25 pp ❌

> qwen3.6:35b-a3b | 60 %, 80.2 tok/s, 0/5 needle | 85 %, 30.0 tok/s, 5/5 | not tested | +25 pp ✅

## Examples

- qwen3.6:27b loses 25 percentage points of schema accuracy when moved from LM Studio to Ollama, despite both runtimes having similar token speeds.
- qwen3.6:35b-a3b gains 25 percentage points of schema accuracy when moved from LM Studio to Ollama, recovering needle recall from 0/5 to 5/5.

## Related Concepts

[[Automation Reliability]] [[Infrastructure Status]]
