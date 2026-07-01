---
title: "Normal Accident Critique"
type: concept
sources:
  - knowledge/concepts/normal-accident-critique.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

This concept identifies a failure mode in tightly coupled agent fleets where individual components remain healthy, yet systemic collapse occurs due to timing, authority, or feedback-loop pressures. Unlike standard health monitoring which checks for broken parts, this framework diagnoses coupling incidents where one agent's success condition creates an unsafe context for another. It shifts the diagnostic lens from component reliability to interaction topology, revealing that failures can emerge from the architecture of dependencies rather than the quality of execution.

## Context

Sean is building a personal knowledge vault with multiple autonomous agents (synthesizer, daily note generators). As he scales this fleet, he risks creating 'normal accidents' where the system appears green but is structurally fragile. Understanding this allows him to design runbooks that diagnose why reliability degraded even when no single agent crashed.

## Evidence

> This failure is not an agent-health incident; it is a coupling incident where A’s success condition creates B’s unsafe context.

> Failures in tightly coupled systems are not always caused by a sick component; they can emerge from individually healthy components interacting under timing, authority, or feedback-loop pressure.

## Examples

- A synthesizer agent successfully writes a concept, but the timing of that write creates a stale-context dependency for a daily-note generator that reads it before the index updates.
- An agent fleet appears healthy because all processes return exit code 0, yet the system fails to produce useful output because the agents' success conditions are mutually exclusive under load.

## Related Concepts

[[Resilience Engineering: Work-as-Imagined vs Work-as-Done]] [[Silent Failure Propagation in Agent Fleets]]
