---
title: "Control Plane / Data Plane Split for Agent Fleets"
type: concept
sources:
  - knowledge/connections/control-plane-stability-vs-data-plane-drift.md
tags: [auto-generated, phase-6]
created: 2026-06-04
updated: 2026-06-04
---

## Definition

This architectural invariant separates the agent system into two distinct layers: the control plane, which manages scheduling, authorization, and halting logic, and the data plane, where agents actually read/write vault artifacts, run research, generate summaries, or mutate files. The stability of the control plane is often assumed to be static, yet it must interface with a data plane that experiences inherent volatility due to user changes or agent mutations. When the control plane assumes a static environment but the data plane experiences drift, the system fails not because of control logic errors, but because of unmanaged divergence between intended and actual workflows. This split requires explicit design of context preparation to survive the volatility of the living vault.

## Context

Sean's vault operates as a living system where agent outputs mutate the very artifacts they depend on. By explicitly defining the boundary between the scheduling logic and the artifact mutation logic, Sean can isolate failures in agent behavior from failures in orchestration. This distinction is critical for debugging why an agent might be 'green' (running) but producing stale or incorrect outputs due to data plane drift.

## Evidence

> distinguish the control plane that schedules, routes, authorizes, observes, and halts agents from the data plane where agents actually read/write vault artifacts, run research, generate summaries, or mutate files.

> This architectural invariant separates the agent system into two distinct layers: the control plane, which manages scheduling, authorization, and halting logic, and the data plane, where agents actually read/write vault artifacts, run research, generate summaries, or mutate files.

## Examples

- The control plane halts an agent because it detects a deviation in the data plane's output format, even though the agent's internal logic was correct.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Vault as Agent Infrastructure]]
