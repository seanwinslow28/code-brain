---
title: "Vault Maintenance"
type: concept
sources:
  - knowledge/connections/cost-vs-automation-depth-tension.md
tags: [auto-generated, phase-6]
created: 2026-06-04
updated: 2026-06-04
---

## Definition

This pattern describes a producer/consumer pattern where one agent's write creates a dependency that another agent's read enforces. When a synthesizer fails silently overnight, the morning brief inherits stale context, and the user notices the staleness before the brief flags the failure. The dependency is invisible in each agent's source. This requires Sean to build a $0/run local summarizer that curates daily_driver's fleet-memory namespace to ensure context integrity without incurring additional costs.

## Context

Sean's vault maintenance relies on local, low-cost summarizers to curate fleet memory. This approach ensures context integrity without triggering cost caps, but it requires careful management of dependencies between agents.

## Evidence

> Build a $0/run local summarizer ... that curates daily_driver's fleet-memory namespace

> Complex integrations like MCP bridges are risky and should be avoided unless their value clearly outweighs the cost.

## Examples

- Building a $0/run local summarizer for fleet-memory curation
- Avoiding MCP bridges due to their high cost and risk

## Related Concepts

[[Cost-Capped Agentic Workflows]] [[Agent Health Monitoring]]
