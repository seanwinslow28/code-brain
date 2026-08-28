---
title: "Probe Design vs. Routing Compliance in Agentic Workflows"
type: concept
sources:
  - knowledge/connections/declarative-intent-vs-situated-action-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

This mechanism describes the conflict between designing probes that accurately measure system state versus routing agents to enforce compliance with predefined paths. When agents prioritize routing compliance, they suppress the very signals (deviations) needed for accurate probing, leading to a blind spot where the system appears healthy while degrading in reality. The tension arises because compliance is easily measurable and automatable, whereas accurate probing requires tolerating noise and interpreting non-standard outcomes.

## Context

Sean's fleet memory index shows high 'rejected_count' metrics, indicating that agents are actively filtering out or failing to process deviations from the norm. This suggests a routing bias where only 'clean' executions are recorded, masking the true complexity of Sean's interactions with his knowledge vault.

## Evidence

> Treat those deviations as evidence about the real workflow—not noncompliance to eliminate

> Add a trace schema: Declared routine → encountered situation → improvisation → residue worth preserving

## Examples

- Deviations being treated as evidence about the real workflow rather than noncompliance to eliminate
- The implementation of a trace schema that captures the full sequence from declared routine to final residue

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Operational Uptime vs. Cognitive Utility Tension]]
