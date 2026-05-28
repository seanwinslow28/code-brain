---
title: "Agent Fleet Observability Dashboard"
type: concept
sources:
  - knowledge/expansions/infrastructure-status.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

A diagnostic layer that maps runtime performance to Brendan Gregg’s USE Method, reporting Utilization, Saturation, and Errors rather than qualitative speed or accuracy. This mechanism shifts the evaluation from static 'winner' selection to dynamic thresholding, where a model's viability is contingent on specific resource constraints like GPU utilization or memory pressure. By anchoring status in these physical limits, the system creates a runbook for failure modes, allowing the operator to distinguish between a model that is simply slow and one that is failing under load.

## Context

Sean currently relies on qualitative assessments of his local inference fleet. Without this observability layer, he cannot predict when a 'Tier A' model will degrade into a 'Tier B' or 'Fallback' state, leaving him vulnerable to silent failures during critical job-hunt tasks.

## Evidence

> Add a diagnostic layer that reports every runtime/machine as Utilization, Saturation, Errors rather than “fast/accurate/best.”

> This unlocks an agent fleet runbook instead of a concept note: “If vault_synthesizer misses schema, check saturation before swapping models.”

> Right now the concept names winners; USE would let Sean explain why a winner stops being a winner under load.

## Examples

- MBP-Ollama qwen3.6:35b-a3b is Tier A only when GPU utilization is below X, memory pressure below Y, queue depth below Z, and error rate below N.

## Related Concepts

[[Infrastructure Status]] [[Runtime-Model Coupling]]
