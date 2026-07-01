---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - knowledge/connections/the-latency-of-trust-in-automated-research-pipelines.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

This pattern involves decoupling financial accounting from functional success metrics to prevent the masking of debugging costs. When failed API calls are not billed locally, the system under-reports the true cost of reliability issues, creating a blind spot in resource allocation for retry loops and error handling. Accurate cost tracking requires recording usage even when the primary function fails, ensuring that the financial burden of instability is visible.

## Context

Sean needs to accurately measure the cost of debugging and retry loops to justify infrastructure improvements. If failed calls do not bill locally, the apparent efficiency of the system is illusory, hiding the true expense of maintaining reliability in automated workflows.

## Evidence

> failed Fusion calls bill OpenRouter but record $0 locally (`record_spend` is post-success only in `__main__.py`) — record usage.cost on failure too.

> Financial tracking must be decoupled from functional success to accurately measure the cost of debugging and retry loops.

## Examples

- OpenRouter billing for failed Fusion calls while local logs show zero spend
- Local recording of `usage.cost` only after successful execution, ignoring failure states

## Related Concepts

[[Silent Failure Propagation in Agent Fleets]] [[Automation Reliability]]
