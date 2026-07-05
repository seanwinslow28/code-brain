---
title: "Control Plane / Data Plane Split for Agent Fleets"
type: concept
sources:
  - knowledge/concepts/control-plane-data-plane-split-for-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This architectural pattern separates deterministic orchestration logic from probabilistic agent execution, creating a structural gap where the control plane's simplified model of reality diverges from the complex, noisy outputs generated in the data plane. This divergence produces 'legibility debt,' a state where the operator loses visibility into the true system state because the control signals no longer accurately reflect the underlying agent behaviors. The tension escalates when high-throughput sampling prioritizes volume over signal quality, leading to silent failures that erode trust before they are detected by standard success/failure metrics.

## Context

Sean must implement 'unsafe control action' modes that explicitly flag when representations diverge from reality, preventing the accumulation of unobserved errors in his personal knowledge vault. The current fleet's drive for high-throughput sampling creates a systemic trust deficit, requiring a shift toward observability dashboards that highlight distortion metrics rather than just completion rates.

## Evidence

> accidents are produced by inadequate control in a sociotechnical system, not just broken components

> Sean needs to implement 'unsafe control action' modes that explicitly flag when representations diverge from reality

## Examples

- The fleet's drive for high-throughput sampling leads to a systemic trust deficit as the volume of outputs increases.
- Observability dashboards should highlight distortion metrics, not just success/failure rates.

## Related Concepts

[[Slop as a Trust Deficit]] [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]
