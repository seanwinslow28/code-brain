---
title: "Agent Health Monitoring"
type: concept
sources:
  - knowledge/connections/the-tension-between-reliability-metrics-and-adaptive-capacity-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-04
updated: 2026-07-04
---

## Definition

This concept describes the mechanism of distinguishing between technical detection of system states and the semantic evaluation of agent utility. It defines monitoring not merely as catching broken states or loops, but as assessing whether the agent's output preserves the original intent despite environmental noise. The underlying pattern is that traditional health checks are insufficient because they do not account for the 'work-as-done' reality where agents must navigate partial failures. Effective monitoring requires measuring the fidelity of intent preservation rather than just the presence of errors.

## Context

Sean's current frame treats monitoring as detection, which is insufficient for demonstrating the resilience required in complex agent fleets. He must evolve his monitoring strategy to capture the quality of degradation and recovery, which is more valuable for his portfolio and job hunt.

## Evidence

> Your current frame treats monitoring as detection: catch loops, hallucinations, broken states.

> The core tension exists between the traditional engineering obsession with reliability (uptime, success rates) and the operational reality of resilience (graceful degradation under surprise).

## Examples

- The fleet memory index tracks concepts written and connections made, but does not explicitly measure the semantic integrity of those outputs during high-load runs.
- Hiring managers value the 'stretch' capability of agents more than uptime statistics because it signals a deeper understanding of complex system dynamics.

## Related Concepts

[[SRE Error Budget for Agents]] [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]
