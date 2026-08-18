---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/expansions/connections/agent-health-and-operational-resilience.md
tags: [auto-generated, phase-6]
created: 2026-08-18
updated: 2026-08-18
---

## Definition

A design philosophy that prioritizes graceful extensibility over hardening, asking what the system does after its assumptions fail rather than how to stop failure. It requires defining essential versus nonessential capability tiers and establishing load-shedding orders when capacity saturates. This approach prevents the disguise of deferred work as successful work by explicitly managing degraded modes.

## Context

Sean's current infrastructure often fails silently or produces incorrect outputs when dependencies disappear. Implementing this concept forces explicit definitions of what can be shed (e.g., visual QA) versus what must be preserved (e.g., provenance), reducing the cognitive load of debugging silent failures.

## Evidence

> Hardening asks how to stop failure; graceful extensibility asks what the system does after its assumptions fail.

> When Tier C disappears, preserve manifest truth and bounded backlog growth; shed visual QA before provenance, and never disguise deferred work as successful work.

## Examples

- A degraded-mode specification for Code-Brain: essential/nonessential capability tiers, load-shedding order, backlog ceilings, recovery semantics, and dependency-loss drills.

## Related Concepts

[[Agent Health]] [[Silent Failure Propagation in Agent Fleets]]
