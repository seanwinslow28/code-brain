---
title: "Agent Fleet Observability Dashboard"
type: concept
sources:
  - knowledge/connections/velocity-vs-legibility-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-09
updated: 2026-07-09
---

## Definition

An observability dashboard that prioritizes successful completions over missing data or silence creates a blind spot for systemic failures. Effective design requires treating silence as a critical error signal, ensuring that gaps in output are as visible as successes. This approach prevents the normalization of silent failures and forces attention to areas where the system is not performing.

## Context

Sean's current dashboard likely highlights volume metrics, which obscures the declining quality of connections. By shifting focus to missing data and silence, Sean can identify where the agent fleet is failing to produce meaningful insights rather than just processing inputs.

## Evidence

> Automated dashboards should be designed to highlight missing data or silence as critical errors, not just successful completions.

> Sean must treat manual tickets as the single source of truth for system health, rather than a reflection of agent activity.

## Examples

- Treating manual tickets as the primary health indicator reveals gaps that automated metrics miss.
- Highlighting silence in output streams forces investigation into why certain concepts are not being generated or connected.

## Related Concepts

[[Legibility Debt as a Supervision Failure Mode]] [[The Illusion of Health in Autonomous Systems]]
