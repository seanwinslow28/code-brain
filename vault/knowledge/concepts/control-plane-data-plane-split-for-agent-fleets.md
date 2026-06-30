---
title: "Control Plane / Data Plane Split for Agent Fleets"
type: concept
sources:
  - knowledge/concepts/control-plane-data-plane-split-for-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-06-30
updated: 2026-06-30
---

## Definition

This mechanism defines operational efficiency not as an intrinsic property of automation, but as a function of the handoffs between visible user workflows and backstage agent work. It requires distinguishing between the control logic that directs agents (the control plane) and the actual data processing or content generation they perform (the data plane). When these layers are tightly coupled, failures in one domain cascade into the other; when separated, bottlenecks can be isolated to the throughput-limiting layer without destabilizing the entire system.

## Context

Sean's vault synthesizer and fleet memory index represent the control plane, while job application tracking is the data plane. Understanding this split allows him to diagnose whether a slowdown in his job hunt is due to poor decision-making (control) or execution capacity (data), preventing misdiagnosis of operational issues.

## Evidence

> Operational efficiency is not a property of the automation; it is a property of the handoffs between visible user workflow, backstage agent work, and support systems.

> Identify constraint, map upstream/downstream queues, decide whether to automate, staff, delete, or buffer.

## Examples

- Creating a before/after blueprint of an AdOps intake flow with each agent/hook/API placed behind the line of visibility
- Using Eliyahu M. Goldratt’s Theory of Constraints to determine if automation should target bottleneck protection rather than general efficiency

## Related Concepts

[[System Constraints]] [[Value Chain / Activity System Mapping]] [[Resilience Engineering: Work-as-Imagined vs Work-as-Done]]
