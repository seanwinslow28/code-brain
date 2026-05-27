---
title: "Infrastructure Status"
type: concept
sources:
  - 20_projects/research/2026-05-26-topic-20-mbp-ollama-runtime-comparison.md
tags: [auto-generated, phase-6]
created: 2026-05-27
updated: 2026-05-27
---

## Definition

Infrastructure Status refers to the real-time operational health and capability boundaries of the local compute stack, specifically the trade-offs between decode speed, memory bandwidth, and inference accuracy. It is not a static metric but a dynamic state where hardware tiers (MBP vs. Alienware) and runtime choices (MLX vs. Ollama) create distinct performance envelopes. A status update must account for the fact that a model's 'best' runtime is non-uniform across the model family, requiring per-model configuration rather than a global switch.

## Context

Sean's job hunt and agent development depend on a reliable local AI stack. Understanding the specific status of his MBP's Ollama vs. LM Studio capabilities allows him to route high-stakes tasks (like interview prep or code generation) to the correct runtime, preventing delays caused by re-running failed jobs.

## Evidence

> Best Tier A upgrade candidate identified: qwen3.6:35b-a3b on MBP-Ollama at 85 % schema match, 5/5 needle recall, 30 tok/s — beats the current qwen3-14b LM Studio production baseline on every dimension.

> Adoption recommendation: add Ollama as a co-resident runtime on the MBP (Ollama + LM Studio both bound, different ports).

> Migrate the agents that benefit (vault_synthesizer, knowledge_lint Tier 2, job_feed scoring) to call MBP-Ollama with qwen3.6:35b-a3b for accuracy-critical work; keep LM Studio available for cases where its 2-3× decode-speed advantage matters more.

## Examples

- The MBP-Ollama runtime with qwen3.6:35b-a3b is identified as the best Tier A upgrade candidate, outperforming the current production baseline on schema, recall, and speed.
- LM Studio is retained for its 2-3× decode-speed advantage in scenarios where speed is prioritized over schema accuracy.

## Related Concepts

[[Runtime-Model Coupling]] [[Automation Reliability]]
