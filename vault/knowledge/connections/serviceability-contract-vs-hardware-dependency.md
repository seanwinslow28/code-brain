---
title: "Serviceability Contract vs. Hardware Dependency"
type: connection
connects:
  - Operational Uptime vs. Cognitive Utility Tension
  - Capability-Aware Scheduling
  - Infrastructure
created: 2026-08-17
updated: 2026-08-17
---

## Synthesis

The tension between defining infrastructure by service outcomes versus hardware dependencies creates a fragility in system design. When Sean relies on specific machines, any change in hardware availability breaks the workflow. By shifting to a serviceability contract, he decouples functional requirements from physical assets, allowing for more resilient and adaptable agent operations.

## Threads

### [[Operational Uptime vs. Cognitive Utility Tension]]

> a reachable machine is not necessarily delivering useful work, while an offline optional node may not impair the system at all

### [[Capability-Aware Scheduling]]

> Model each machine as a pool of schedulable capabilities rather than a named endpoint

### [[Infrastructure]]

> Replace the binary ONLINE/OFFLINE model with black-box service checks, white-box diagnostics, and the four golden signals: latency, traffic, errors, and saturation

## Implications

- Sean must define clear SLIs/SLOs for each agent task to enable capability-aware scheduling.
- Hardware changes become less disruptive if tasks are defined by capabilities rather than specific machines.
