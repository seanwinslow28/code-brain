---
title: "Agent Health Monitoring"
type: concept
sources:
  - knowledge/connections/operational-uptime-vs-strategic-stagnation.md
tags: [auto-generated, phase-6]
created: 2026-08-12
updated: 2026-08-12
---

## Definition

This concept defines the practice of evaluating agent viability based on binary operational states (up/down) rather than semantic output quality or strategic alignment. It establishes a dependency where the cost-effectiveness and reliability of agentic workflows are contingent upon the continuous availability of specific agents, yet this monitoring often fails to detect when an agent is 'alive' but producing no value. The mechanism creates a false sense of security by prioritizing process continuity over outcome integrity.

## Context

Sean's current monitoring approach tracks whether agents are running and completing tasks, but it does not adequately distinguish between healthy agents that generate insight and those that are merely executing empty loops.

## Evidence

> The operational health of agents directly impacts the cost-effectiveness of agentic workflows if an agent is unhealthy, it may incur unnecessary costs or disrupt other automation tasks.

> Agents report success based on process execution while knowledge integrity depends on successful semantic integration.

## Examples

- A synthesizer agent continues to run and consume tokens without writing any new concepts, yet its health status remains 'Green' because the process did not crash.

## Related Concepts

[[Agent Health]] [[SRE Error Budget for Agents]]
