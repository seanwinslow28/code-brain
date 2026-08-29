---
title: "Reliability Contract vs. Agentic Intent"
type: connection
connects:
  - SRE Error Budget for Agents
  - MAPE-K Closed-Loop Controller
  - Agent Health Monitoring
created: 2026-08-15
updated: 2026-08-15
---

## Synthesis

The tension lies between the rigid, user-centric reliability contracts of SRE and the flexible, intent-driven nature of agentic workflows. While SRE demands explicit error budgets and SLIs to prevent feature creep during instability, agentic systems prioritize adaptive behavior and intent execution. This creates a conflict where the need for operational stability (stopping feature work) directly contradicts the agent's primary directive to fulfill user intent continuously, requiring a formalized policy layer to mediate between reliability constraints and creative/professional goals.

## Threads

### [[SRE Error Budget for Agents]]

> after two misses in seven days, feature work stops and reliability work begins.

### [[MAPE-K Closed-Loop Controller]]

> policy selected Z; the executor acted; the knowledge store recorded the result.

### [[Agent Health Monitoring]]

> health must be defined from what users care about—not whatever telemetry happens to be available

## Implications

- Sean must define explicit SLIs for his daily note and job feed before adding new automation features.
- The fleet needs a formal policy layer to decide when to stop feature development and focus on reliability.
- Agent health metrics must be tied to user outcomes, not just system uptime.
