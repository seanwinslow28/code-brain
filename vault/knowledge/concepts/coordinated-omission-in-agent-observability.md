---
title: "Coordinated Omission in Agent Observability"
type: concept
sources:
  - knowledge/expansions/connections/agent-health-and-cost-efficiency.md
tags: [auto-generated, phase-6]
created: 2026-08-17
updated: 2026-08-17
---

## Definition

This phenomenon occurs when a stalled system stops generating the very observations that would reveal the stall, causing health metrics to appear improved during actual failure. It arises because health denominators come from expected work rather than observed logs, meaning sleeping machines or missing batons produce no duration samples. This creates an illusion of competence where averages improve precisely when the system is failing to execute its scheduled tasks.

## Context

Sean's dashboard metrics may falsely indicate high agent health if they only measure successful runs, masking the silent decay of the automation infrastructure.

## Evidence

> Coordinated omission occurs when a stalled system stops generating the very observations that would reveal the stall.

> Health denominators come from expected work, not observed logs.

## Examples

- A sleeping machine producing no duration or cost sample, making averages improve during failure.
- An expected-run ledger that records scheduled, started, completed, deferred, absent, and stale states to capture the full picture of agent health.

## Related Concepts

[[Agent Health Monitoring]] [[The Illusion of Competence in Automated Systems]]
