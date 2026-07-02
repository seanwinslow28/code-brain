---
title: "Cost-Capped Agentic Workflows"
type: concept
sources:
  - knowledge/connections/the-latency-of-trust-in-automated-research-pipelines.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This pattern defines a financial leakage vector where the cost accounting logic is decoupled from the functional success state of an agent run. Specifically, when external API calls fail or return empty results, the billing provider charges for the request, but the local ledger only records spend upon successful completion. This creates a hidden tax on debugging and retry loops, as the system accumulates financial debt without corresponding data assets, distorting the true cost-per-insight metric.

## Context

Sean's job-hunt and research agents frequently hit rate limits or return empty results during retries. If the local ledger does not capture these failed API calls, he cannot accurately calculate the true cost of his automated workflows, leading to underestimation of operational expenses.

## Evidence

> failed Fusion calls bill OpenRouter but record $0 locally (`record_spend` is post-success only in `__main__.py`) — record usage.cost on failure too.

> Financial tracking must be decoupled from functional success to accurately measure the cost of debugging and retry loops.

## Examples

- OpenRouter billing for failed Fusion calls while local ledger records $0
- Local ledger recording spend only after successful completion in `__main__.py`

## Related Concepts

[[Silent Failure Propagation in Agent Fleets]] [[Automation Reliability]]
