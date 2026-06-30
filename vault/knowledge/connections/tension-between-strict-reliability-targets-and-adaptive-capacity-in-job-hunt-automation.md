---
title: "Tension Between Strict Reliability Targets and Adaptive Capacity in Job Hunt Automation"
type: connection
connects:
  - SRE Error Budget for Agents
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Graceful Extensibility in Adaptive Systems
created: 2026-06-30
updated: 2026-06-30
---

## Synthesis

The core tension lies between the SRE requirement for strict reliability targets, which enforces a freeze on feature work to maintain stability, and the resilience engineering need for adaptive capacity to handle unpredictable job-hunt dynamics. While error budgets demand a halt to new development when failures occur, the volatile nature of the job market requires continuous adaptation and scaling. This creates a conflict where Sean must balance the need for reliable, error-free automation with the necessity of rapidly adjusting his strategy and tools in response to changing market conditions.

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
- Monitoring must focus on context freshness and timing errors, not just binary success/failure, to detect early signs of saturation.
