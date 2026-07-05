---
title: "Silent Failure Propagation in Agent Fleets"
type: concept
sources:
  - knowledge/connections/the-latency-of-trust-in-automated-research-pipelines.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This mechanism describes a state where upstream agents silently under-yield or downstream agents choke on formatting artifacts, resulting in a system that does not crash but merely produces less value than expected. The failure mode is characterized by the absence of explicit error signals, creating an illusion of operational health while actual output quality degrades. This latency forces observers to abandon binary success metrics in favor of yield monitoring, as the system's reliability is defined by its ability to signal degradation rather than just its uptime. Debugging becomes harder because the financial cost of failure is often invisible until later reconciliation, masking the true expense of maintaining pipeline robustness.

## Context

Sean must implement yield monitoring for upstream collectors to detect silent under-delivery before it impacts downstream synthesis. Financial tracking must be decoupled from functional success to accurately measure the cost of debugging and retry loops.

## Evidence

> When upstream agents silently under-yield or downstream agents choke on formatting artifacts, the system does not crash; it merely produces less value than expected.

> Sean cannot rely on binary success/fail metrics to gauge fleet health; he must monitor yield rates and parsing robustness as primary indicators of system reliability.

## Examples

- failed Fusion calls bill OpenRouter but record $0 locally (`record_spend` is post-success only in `__main__.py`) — record usage.cost on failure too.

## Related Concepts

[[Cost-Capped Agentic Workflows]] [[Automation Reliability]]
