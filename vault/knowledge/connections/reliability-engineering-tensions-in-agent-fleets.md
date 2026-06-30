---
title: "Reliability Engineering Tensions in Agent Fleets"
type: connection
connects:
  - SRE Error Budget for Agents
  - Normal Accident Critique
  - Control Plane / Data Plane Split for Agent Fleets
created: 2026-06-30
updated: 2026-06-30
---

## Synthesis

The tension between error budgeting and normal accidents reveals a fundamental contradiction in autonomous system design: while error budgets provide a contractual framework for managing acceptable failure rates, they assume that failures are independent events. However, in tightly coupled agent fleets, monitoring itself can create new coupling paths and false confidence, making some failures inevitable regardless of the budget. This means Sean must balance explicit reliability contracts with architectural patterns that allow for graceful degradation, rather than relying solely on monitoring to prevent all errors.

## Threads

### [[SRE Error Budget for Agents]]

> Agent X may silently fail N times per month before feature velocity stops and reliability work becomes mandatory.

### [[Normal Accident Critique]]

> If agent fleets are complex and tightly coupled, some failures are not bugs to eliminate but system properties to design around.

### [[Control Plane / Data Plane Split for Agent Fleets]]

> Treat job-hunt automation as a control-plane problem: desired state is 'credible role pipeline stays warm'; agents are controllers; notes, resumes, applications, and outreach are reconciled resources.

## Implications

- Sean should design his agent fleet with explicit error budgets that trigger graceful degradation rather than attempting to eliminate all failures.
- Monitoring dashboards must be interpreted with caution, as they can create false confidence in tightly coupled systems where some failures are inevitable.
