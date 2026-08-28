---
title: "Capability-Aware Scheduling"
type: concept
sources:
  - knowledge/concepts/capability-aware-scheduling.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

This mechanism decouples the matching phase from the claiming phase, allowing heterogeneous nodes to publish hard requirements and soft rankings rather than accepting one-way dispatch. By treating a match as a tentative proposal that must be revalidated against current availability and policy constraints before execution begins, the system tolerates stale advertisements and enables dynamic negotiation between job needs and machine capabilities. This separation prevents urgent jobs from starving creative workloads by seizing scarce resources without regard for fairness or node state.

## Context

Sean's agent fleet operates across diverse hardware (Alienware, MacBook) with conflicting operational modes (interactive vs. batch). Without this separation, silent failures occur in non-critical pipelines when nodes reject claims due to stale capability advertisements or active user interference.

## Evidence

> Their crucial move is separating matching from claiming, which tolerates stale advertisements and lets resource owners express whom they will serve—not merely what they can run.

> The current concept cannot express machine-side intent or detect a node whose advertised capability became stale before dispatch.

## Examples

- Alienware accepts interruptible GPU work only during its manual-awake window
- MacBook rejects batch claims during interactive use

## Related Concepts

[[Dominant Resource Fairness]] [[HTCondor ClassAds]]
