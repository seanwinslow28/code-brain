---
title: "Probe Design vs. Routing Compliance in Agentic Workflows"
type: connection
connects:
  - Complexity Override
  - Agent Fleet Observability Dashboard
  - SRE Error Budget for Agents
created: 2026-07-03
updated: 2026-07-03
---

## Synthesis

The tension lies between the efficiency of linear routing and the necessity of probe design in complex domains. Linear routing assumes a known structure, while probe design acknowledges that the structure must be discovered through safe-to-fail experiments. This creates a dependency where agents must balance execution speed with the slower, iterative process of learning what kind of problem they are solving. The consequence is a shift from optimizing for throughput to optimizing for signal clarity in uncertain environments.

## Threads

### [[Complexity Override]]

> Complexity Override does not relax discipline; it changes the unit of discipline from routing compliance to probe design: safe-to-fail experiment, observable signal, amplification/dampening rule.

### [[Agent Fleet Observability Dashboard]]

> Operational visibility is required to distinguish between a failed probe and a successful one, ensuring that the system can amplify good signals and dampen bad ones without losing track of overall health.

### [[SRE Error Budget for Agents]]

> The error budget must account for the cost of probes that fail to yield signal, treating them as necessary exploration costs rather than pure failures in execution.

## Implications

- Sean must redefine success metrics for his agents to include signal quality and learning velocity, not just task completion rates.
- The fleet's architecture needs to support parallel probe execution with independent kill switches to prevent cascading failures in complex domains.
