---
title: "Cost-Capped Workflows and Agent Health Monitoring"
type: connection
connects:
  - SRE Error Budget for Agents
  - The Efficiency-Quality Inversion in Automated Synthesis
  - Cost-Capped Agentic Workflows
created: 2026-08-28
updated: 2026-08-28
---

## Synthesis

The tension between cost-capping and health monitoring reveals a fundamental conflict between financial constraints and operational reliability. Hard cost caps terminate work abruptly, potentially leaving artifacts in an incomplete state that requires human intervention to resolve, thereby increasing the effective cost of failure. By integrating error budgets and anytime computation, the system can gracefully degrade output quality rather than failing entirely, aligning financial limits with acceptable utility thresholds.

## Threads

### [[SRE Error Budget for Agents]]

> Define a user-visible SLO—such as “95% of scheduled runs produce a usable artifact by its deadline”—then treat the remaining failure allowance as an error budget.

### [[The Efficiency-Quality Inversion in Automated Synthesis]]

> Track cost per accepted artifact, cost per novel connection retained after 30 days, and human correction minutes per usable output.

### [[Cost-Capped Agentic Workflows]]

> Replace hard cost caps that terminate work with staged agents that always retain a valid best-so-far result.

## Implications

- Sean should implement graceful degradation strategies for his agent runs to prevent partial artifacts from accumulating in his vault.
- Monitoring 'cost per accepted artifact' provides a more accurate measure of system efficiency than total run duration or concept count.
