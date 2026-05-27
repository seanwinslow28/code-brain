---
title: "Automation Reliability"
type: concept
sources:
  - 20_projects/research/2026-05-26-topic-20-mbp-ollama-runtime-comparison.md
tags: [auto-generated, phase-6]
created: 2026-05-27
updated: 2026-05-27
---

## Definition

Automation Reliability is the measure of an agent's ability to produce structurally valid outputs consistently across varying environmental conditions. It is undermined by 'silent failures' where a model generates text that looks correct but violates strict schema constraints, often due to hidden inference flags like 'thinking' modes. Reliability requires not just monitoring for crashes, but actively benchmarking schema adherence and needle recall across different runtime-model combinations to detect degradation before it impacts downstream tasks.

## Context

Sean's vault synthesizer and job-feed scoring agents are critical to his daily workflow. If these agents fail silently due to schema mismatches, his knowledge base becomes corrupted or his job applications are mis-scored. This concept highlights the need for rigorous, per-model runtime testing to ensure his automation pipeline remains trustworthy.

## Evidence

> gains range from +25 pp to -25 pp depending on the model.

> Cross-runtime data refutes any "switch wholesale" framing; the right move is per-model runtime selection.

> qwen3.5:27b | 70 %, 13.9 tok/s, 0/5 needle | 90 %, 8.8 tok/s, 5/5 | 90 %, 6.9 tok/s, 5/5 | +20 pp ✅

## Examples

- qwen3.5:27b shows a +20 pp gain in schema accuracy when moved to Ollama, recovering needle recall from 0/5 to 5/5.
- qwen3-coder:30b shows a -5 pp loss in schema accuracy when moved to Ollama, which is within noise but indicates a potential risk for code-heavy tasks.

## Related Concepts

[[Runtime-Model Coupling]] [[Infrastructure Status]]
