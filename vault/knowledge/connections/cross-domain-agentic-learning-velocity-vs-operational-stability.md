---
title: "Cross-Domain: Agentic Learning Velocity vs. Operational Stability"
type: connection
connects:
  - Probe Design vs. Routing Compliance in Agentic Workflows
  - Agent Fleet Observability Dashboard
  - SRE Error Budget for Agents
created: 2026-07-04
updated: 2026-07-04
---

## Synthesis

The tension lies between the need for agents to explore uncertain domains (learning velocity) and the requirement for the system to remain stable and observable (operational stability). Probe design drives learning velocity by allowing safe-to-fail experiments, but this increases the load on the observability dashboard. The consequence is that Sean must balance the breadth of exploration against the depth of signal clarity, ensuring that the error budget covers both execution errors and exploration costs.

## Threads

### [[Probe Design vs. Routing Compliance in Agentic Workflows]]

> The tension lies between the efficiency of linear routing and the necessity of probe design in complex domains.

### [[Agent Fleet Observability Dashboard]]

> Operational visibility is required to distinguish between a failed probe and a successful one, ensuring that the system can amplify good signals and dampen bad ones without losing track of overall health.

### [[SRE Error Budget for Agents]]

> The error budget must account for the cost of probes that fail to yield signal, treating them as necessary exploration costs rather than pure failures in execution.

## Implications

- Sean must redefine success metrics for his agents to include signal quality and learning velocity, not just task completion rates.
- The fleet's architecture needs to support parallel probe execution with independent kill switches to prevent cascading failures in complex domains.
