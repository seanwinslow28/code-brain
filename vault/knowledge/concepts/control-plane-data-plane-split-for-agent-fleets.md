---
title: "Control Plane / Data Plane Split for Agent Fleets"
type: concept
sources:
  - knowledge/connections/representation-distortion-and-trust-erosion-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-03
updated: 2026-07-03
---

## Definition

This architectural invariant separates the decision-making logic (control plane) from the execution and state management (data plane), creating a dependency where the control plane's view of reality is mediated by potentially flawed data sources. When agents operate in this split architecture, failures often manifest as discrepancies between the intended state defined by the controller and the actual state maintained by the workers. This separation allows for scalability but introduces a critical vulnerability: if the control plane cannot accurately perceive the data plane's condition, it issues commands that are either redundant or destructive. The mechanism thrives on the assumption that observability is sufficient for control, which is often false in complex adaptive systems.

## Context

Sean's infrastructure uses this split to manage his vault and job hunt processes. When the control plane (his dashboards or manifests) fails to reflect the data plane (actual agent outputs and file states), he makes decisions based on stale or incorrect information, leading to systemic failures in his career progression and creative output quality.

## Evidence

> accidents are produced by inadequate control in a sociotechnical system, not just broken components

> The tension lies between the operator's need for a simplified control surface and the system's complex, often failing, reality.

## Examples

- inadequate control in a sociotechnical system
- simplified control surface

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Slop as a Trust Deficit]]
