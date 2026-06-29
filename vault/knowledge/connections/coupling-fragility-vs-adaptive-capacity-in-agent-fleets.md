---
title: "Coupling Fragility vs Adaptive Capacity in Agent Fleets"
type: connection
connects:
  - Normal Accident Critique
  - Resilience Engineering: Work-as-Imagined vs Work-as-Done
  - Agent Fleet Observability Dashboard
created: 2026-06-29
updated: 2026-06-29
---

## Synthesis

The tension lies between designing agents for reliable execution of known tasks and ensuring the fleet can adapt when those tasks become impossible. Sean's current focus on 'green checkmarks' masks the risk of normal accidents where healthy components interact fatally. By integrating resilience engineering metrics, he can shift from monitoring uptime to measuring adaptive capacity, which is critical for maintaining trust in a personal knowledge system.

## Threads

### [[Normal Accident Critique]]

> This failure is not an agent-health incident; it is a coupling incident where A’s success condition creates B’s unsafe context.

### [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]

> The dashboard should not only report whether the nightly loop ran; it should show what adaptive capacity remains when the loop is partially degraded.

### [[Agent Fleet Observability Dashboard]]

> Current concept points toward uptime. This would let Sean ship a stronger portfolio artifact: “How I designed a personal agent fleet for graceful degradation, not just green checkmarks.”

## Implications

- Sean should redesign his monitoring dashboards to include metrics on fallback quality and manual takeover cost, not just success rates.
- He needs to create incident review templates that distinguish between component failures and coupling failures in his agent fleet.
