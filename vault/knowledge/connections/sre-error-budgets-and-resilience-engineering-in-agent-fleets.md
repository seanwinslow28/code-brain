---
title: "SRE Error Budgets and Resilience Engineering in Agent Fleets"
type: connection
connects:
  - SRE Error Budget for Agents
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Graceful Extensibility in Adaptive Systems
created: 2026-06-29
updated: 2026-06-29
---

## Synthesis

The tension between SRE error budgets and resilience engineering lies in the balance between strict reliability targets and adaptive capacity. While error budgets enforce a freeze on feature work to maintain stability, resilience engineering requires exposing saturation and recruiting extra capacity when the environment changes. This creates a dynamic where Sean must constantly negotiate between maintaining service level objectives and adapting to new demands in his job hunt.

## Threads

### [[SRE Error Budget for Agents]]

> For job-hunt automation, reliability means `X critical workflow succeeds by Y time with Z freshness`; when the error budget burns, freeze feature work and spend cycles on recovery.

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> Failure is not only component breakage; it is unsafe control action: agent acts too early, too late, not at all, or with stale context.

### [[Graceful Extensibility in Adaptive Systems]]

> The fleet should not merely prevent known failures; it should expose saturation early and recruit extra capacity when the job hunt changes shape.

## Implications

- Sean must design a hybrid system that balances strict SLOs with adaptive scaling mechanisms to handle unpredictable job-hunt dynamics.
- The error budget policy must include provisions for graceful degradation rather than just hard freezes to maintain resilience.
