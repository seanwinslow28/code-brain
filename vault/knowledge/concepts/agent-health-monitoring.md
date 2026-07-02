---
title: "Agent Health Monitoring"
type: concept
sources:
  - knowledge/connections/the-tension-between-reliability-metrics-and-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This concept describes the traditional paradigm of monitoring as a reactive detection mechanism focused on identifying discrete failure states such as loops, hallucinations, or broken states. It contrasts with proactive resilience by focusing on the immediate symptoms of deviation rather than the systemic capacity to absorb them. The limitation is that it treats health as the absence of errors rather than the presence of adaptive capacity.

## Context

Sean's current monitoring frame is insufficient for demonstrating the operational maturity required in his job hunt, as it misses the nuance of graceful degradation.

## Evidence

> Your current frame treats monitoring as detection: catch loops, hallucinations, broken states.

> The consequence is that his portfolio must evolve from a collection of working scripts to a demonstration of how his agents stretch under failure.

## Examples

- Detecting hallucinations in real-time agent outputs.
- Identifying broken states in automated workflows.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[SRE Error Budget for Agents]]
