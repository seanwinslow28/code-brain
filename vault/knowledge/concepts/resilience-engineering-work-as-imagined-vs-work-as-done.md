---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/expansions/connections/agentic-engineering-and-daily-driver-agent-optimization.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

This concept defines the gap between an agent's designed operational state and its actual failure modes in a sociotechnical loop. It requires modeling the system not as a sequence of successful steps, but as a controller interacting with environmental constraints where unsafe actions occur when provided, not provided, or at the wrong time. The mechanism shifts focus from preventing all errors to identifying which failures are dangerous versus merely annoying, ensuring that graceful degradation preserves user decision quality even when normal coordination breaks.

## Context

Sean is building a daily-driver agent that must handle overnight context injection and daily note creation. Without this lens, he risks optimizing for 'health' metrics while ignoring the specific hazard of false operational certainty caused by stale context. This insight allows him to define explicit stop rules and escalation boundaries rather than just monitoring uptime.

## Evidence

> Model the daily-driver as a controller in a sociotechnical loop: Sean, vault, launchd, local models, calendar backfill, cost caps, daily-note state.

> Injecting stale overnight context is worse than injecting none because it creates false operational certainty.

## Examples

- Defining fallback states such as full automation, partial digest, stale-but-labeled digest, empty daily note, manual recovery prompt, and fleet quarantine.
- When capability fails, the system must preserve user decision quality by degrading to a fallback state with visible confidence labels.

## Related Concepts

[[Agent Health Monitoring]] [[Intent Engineering]]
