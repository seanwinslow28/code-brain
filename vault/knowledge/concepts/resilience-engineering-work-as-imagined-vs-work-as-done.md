---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/expansions/agent-ops-fdp-backup-track.md
tags: [auto-generated, phase-6]
created: 2026-06-03
updated: 2026-06-03
---

## Definition

This framework posits that system reliability is not just about preventing failures in designed workflows, but about detecting when the actual operational workflow diverges from the intended design. It shifts the focus from merely tracking uptime to analyzing the hidden couplings, brittle handoffs, and drift that occur when agents operate in complex, real-world environments. By treating agent failures as organizational phenomena rather than just software bugs, operators can identify near-misses and adapt the system to the reality of how it is actually used.

## Context

Sean's agents operate in a dynamic personal knowledge vault, where context and file states change frequently. Understanding this divergence helps him anticipate failures that standard monitoring might miss, such as agents failing because of unexpected file structures or timing issues rather than code errors.

## Evidence

> agent ops is not just keeping agents green; it is detecting when the designed workflow and the real workflow diverge.

> Add a section on drift, hidden coupling, brittle handoffs, and how operators learn from near-misses.

## Examples

- Analyzing why agents fail in ways that resemble organizational breakdowns rather than typical software crashes.

## Related Concepts

[[Automation Reliability]] [[Infrastructure Status and Agent Failure]]
