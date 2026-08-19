---
title: "Capability-Aware Scheduling"
type: concept
sources:
  - knowledge/expansions/capability-aware-scheduling.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

A resource allocation mechanism that decouples the matching phase from the claiming phase, allowing heterogeneous nodes to publish hard requirements and soft rankings rather than accepting one-way dispatch. This approach treats a match as a tentative proposal that must be revalidated against current availability and policy constraints before execution begins. By separating intent publication from resource acquisition, the system tolerates stale advertisements and enables dynamic negotiation between job needs and machine capabilities.

## Context

Sean's agent fleet operates across diverse hardware (Alienware, MacBook) with conflicting operational modes (interactive vs. batch). Without this separation, urgent jobs can starve creative workloads by seizing scarce resources without regard for fairness or node state, leading to silent failures in non-critical pipelines.

## Evidence

> Their crucial move is separating matching from claiming, which tolerates stale advertisements and lets resource owners express whom they will serve—not merely what they can run.

> The current concept cannot express machine-side intent or detect a node whose advertised capability became stale before dispatch.

## Examples

- Alienware accepts interruptible GPU work only during its manual-awake window
- MacBook rejects batch claims during interactive use

## Related Concepts

[[Dominant Resource Fairness]] [[HTCondor ClassAds]]
