---
title: "The Joint System Dependency in Agent Reliability"
type: connection
connects:
  - Runtime-Model Coupling
  - Infrastructure Status
  - Agent Ops / FDP Backup Track
created: 2026-05-28
updated: 2026-05-28
---

## Synthesis

The tension lies between treating AI models as isolated computational units versus recognizing them as components within a larger joint cognitive system. When Sean's agents fail, it is often misdiagnosed as a model defect rather than a coordination failure in the control loop involving launchd, schema validators, and retry policies. This misdiagnosis leads to unnecessary model swaps instead of fixing the underlying system design, such as routing or escalation thresholds. The consequence is that reliability becomes a function of the entire ecosystem's alignment rather than the model's inherent quality.

## Threads

### [[Runtime-Model Coupling]]

> A model “failing JSON” is not merely a model/runtime defect; it is a coordination failure in the larger control loop.

### [[Infrastructure Status]]

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[infrastructure-status]].

### [[Agent Ops / FDP Backup Track]]

> Sean can write ADRs that justify routing, fallback, HITL escalation, and disablement thresholds as system-design choices.

## Implications

- Sean should shift his evaluation metrics from model accuracy to joint-system reliability under specific runtime conditions.
- Agent failure logs must capture the full runtime context, not just the model output, to diagnose coordination failures.
