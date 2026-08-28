---
title: "Reliability as Spendable Resource vs. Absolute Constraint"
type: connection
connects:
  - SRE Error Budget for Agents
  - Cost-Capped Agentic Workflows
  - Agent Health Monitoring
created: 2026-08-28
updated: 2026-08-28
---

## Synthesis

The tension lies in treating reliability as a static quality attribute versus a dynamic control variable that can be traded against cost and latency. When Sean couples financial costs with allowable failure rates, he shifts from monitoring 'did it work?' to 'how much unreliability may we accept before automation stops?'. This mechanism allows autonomous execution to continue while both cost burn and error-budget burn remain within thresholds, but crossing either triggers a shift to degraded or frozen states. The consequence is a portfolio demo of autonomous admission control that substantiates the economic irrationality of 100% reliability.

## Threads

### [[SRE Error Budget for Agents]]

> Their error-budget model treats reliability as a deliberately spendable resource and rejects 100% reliability as economically irrational.

### [[Cost-Capped Agentic Workflows]]

> Continue autonomous execution while cost burn ≤ X and error-budget burn ≤ Y; crossing either threshold changes the permitted action set.

### [[Agent Health Monitoring]]

> The missing question is not merely “Did this run cheaply?” but “How much unreliability may we accept before automation stops?”

## Implications

- Sean can ship a portfolio demo where budget state automatically selects `run`, `degrade`, `defer`, or `freeze`—substantially stronger than a dashboard reporting “$12/month.”
- An executable fleet admission-control spec combining dollars, failed units of work, and degraded outputs becomes the new standard for agent reliability.
