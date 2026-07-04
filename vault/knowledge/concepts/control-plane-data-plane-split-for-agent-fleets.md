---
title: "Control Plane / Data Plane Split for Agent Fleets"
type: concept
sources:
  - knowledge/connections/representation-distortion-and-trust-erosion-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-04
updated: 2026-07-04
---

## Definition

This concept defines the architectural separation between the simplified, deterministic control logic (control plane) and the complex, probabilistic agent behaviors (data plane). The tension arises when the control plane's assumptions about agent behavior diverge from the actual outputs produced in the data plane. This split creates a 'legibility debt' where the operator cannot easily see the true state of the system, leading to trust erosion when silent failures or 'slop' occur.

## Context

Sean needs to implement 'unsafe control action' modes that explicitly flag when representations diverge from reality. The vault synthesizer must prioritize signal quality over volume to prevent trust erosion from 'slop'.

## Evidence

> accidents are produced by inadequate control in a sociotechnical system, not just broken components

> Sean needs to implement 'unsafe control action' modes that explicitly flag when representations diverge from reality

## Examples

- The fleet's drive for high-throughput sampling leads to a systemic trust deficit as the volume of outputs increases.
- Observability dashboards should highlight distortion metrics, not just success/failure rates.

## Related Concepts

[[Slop as a Trust Deficit]] [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]
