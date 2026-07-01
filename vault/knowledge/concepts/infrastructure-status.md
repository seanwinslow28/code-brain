---
title: "Infrastructure Status"
type: concept
sources:
  - knowledge/connections/observability-vs-operational-reality-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

This invariant describes the physical and network dependencies that underpin agent functionality, where hardware offline states directly negate software-level health reports. When physical machines go offline, agents that depend on them become non-functional regardless of their internal process status, creating a disconnect between the orchestration layer's perception of health and the execution layer's physical reality. This dependency means that infrastructure stability is a prerequisite for any claimed agent capability, yet it is often ignored in favor of software-centric monitoring.

## Context

Sean's workflow requires sync across three machines (Creative Studio/Life Systems). When Alienware and ComfyUI are offline, the entire sync requirement fails, but this is not reflected in the agent health dashboard, leading to a broken daily drive experience.

## Evidence

> Alienware and ComfyUI are OFFLINE, severely impacting the 3-machine sync requirement (Creative Studio/Life Systems).

> When physical machines go offline, agents that depend on them become non-functional regardless of their internal process status.

## Examples

- 3-machine sync requirement failing due to offline hardware
- Agents depending on offline machines becoming non-functional

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Infrastructure Dependency and Creative Pipeline Failure]] [[Vault as Agent Infrastructure]]
