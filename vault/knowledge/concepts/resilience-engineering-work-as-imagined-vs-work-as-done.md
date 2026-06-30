---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/connections/resilience-vs-reliability-in-agent-health.md
tags: [auto-generated, phase-6]
created: 2026-06-30
updated: 2026-06-30
---

## Definition

This concept defines the structural gap between the deterministic, linear workflows agents are programmed to execute and the chaotic, non-linear reality of their actual runtime environments. It posits that agent health cannot be measured by binary success/failure states because these states ignore the 'stretch' capacity required to handle partial failures gracefully. The mechanism relies on observing how an agent degrades under pressure rather than just its ability to maintain uptime in ideal conditions.

## Context

Sean's current portfolio projects likely emphasize successful automation runs, which fails to demonstrate operational maturity. By shifting focus to graceful degradation, he can signal to hiring managers that his systems are robust enough for complex, real-world enterprise environments where perfect reliability is impossible.

## Evidence

> The useful question becomes not “did the agent fail?” but “did the workflow degrade gracefully, preserve intent, and create a recovery path?”

> Your current frame treats monitoring as detection: catch loops, hallucinations, broken states.

## Examples

- Designing portfolio projects to explicitly show fallback behaviors rather than just successful runs.
- Demonstrating that hiring managers value the 'stretch' capability of agents more than uptime statistics.

## Related Concepts

[[SRE Error Budget for Agents]] [[Agent Health Monitoring]]
