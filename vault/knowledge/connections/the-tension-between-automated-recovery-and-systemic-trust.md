---
title: "The Tension Between Automated Recovery and Systemic Trust"
type: connection
connects:
  - SRE Error Budget for Agents
  - Saga / Compensation Patterns for Agent Workflows
  - The Illusion of Competence in Automated Systems
created: 2026-06-30
updated: 2026-06-30
---

## Synthesis

There is a fundamental tension between the desire for high availability through provider fallback and the risk of amplifying systemic failure or cost when those fallbacks are unbounded. When agents automatically route to secondary providers without semantic constraints or error budgets, they may continue to produce low-quality or expensive outputs during degraded states, creating an 'illusion of competence' that erodes user trust over time. This tension requires Sean to define explicit failure semantics and compensation patterns that prioritize correctness and cost control over mere uptime.

## Threads

### [[SRE Error Budget for Agents]]

> Fallback increases reliability only when it does not hide systemic failure, amplify cost, or degrade user trust.

### [[Saga / Compensation Patterns for Agent Workflows]]

> Reliability there requires compensation, idempotency keys, checkpoints, and resumable state, not just alternate providers.

### [[The Illusion of Competence in Automated Systems]]

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[the-illusion-of-competence-in-automated-systems]].

## Implications

- Sean must implement a decision table for autonomous agent routing that includes quality and cost thresholds, not just availability checks.
- Agent workflows need explicit compensation actions to handle partial failures, preventing silent corruption in the knowledge vault.
