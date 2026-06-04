---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/connections/control-plane-stability-vs-data-plane-drift.md
tags: [auto-generated, phase-6]
created: 2026-06-04
updated: 2026-06-04
---

## Definition

This framework posits that system reliability is not just about preventing failures in designed workflows, but about detecting when the actual operational workflow diverges from the intended design. Agent ops is not just keeping agents green; it is detecting when the designed workflow and the real workflow diverge. This divergence often occurs because the data plane (the living vault) changes in ways the control plane (the scheduler) did not anticipate. The mechanism here is the gap between the static assumptions of the control logic and the dynamic reality of the data plane.

## Context

Sean's job hunt and creative studio workflows rely on agents to maintain consistency. If the agents drift from the intended workflow without detection, the downstream artifacts (resumes, creative pieces) become misaligned with the user's current intent. Monitoring this gap allows Sean to intervene before the drift becomes systemic.

## Evidence

> agent ops is not just keeping agents green; it is detecting when the designed workflow and the real workflow diverge.

> This framework posits that system reliability is not just about preventing failures in designed workflows, but about detecting when the actual operational workflow diverges from the intended design.

## Examples

- An agent continues to generate daily notes based on a template that the user has stopped using, creating a silent divergence between the agent's output and the user's actual practice.

## Related Concepts

[[Control Plane / Data Plane Split for Agent Fleets]] [[Infrastructure Status and Agent Failure]]
