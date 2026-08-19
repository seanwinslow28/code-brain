---
title: "Resilience Engineering: Work-as-Imagined vs Work-as-Done"
type: concept
sources:
  - knowledge/concepts/resilience-engineering-work-as-imagined-vs-work-as-done.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This concept defines a design philosophy that prioritizes graceful extensibility over hardening, fundamentally shifting the focus from preventing failure to managing system behavior after assumptions break. It requires explicitly defining essential versus nonessential capability tiers and establishing strict load-shedding orders when capacity saturates. This approach prevents the dangerous disguise of deferred work as successful work by forcing explicit management of degraded modes rather than relying on implicit stability.

## Context

Sean's current infrastructure often fails silently or produces incorrect outputs when dependencies disappear, creating a gap between perceived health and actual utility. Implementing this concept forces explicit definitions of what can be shed (e.g., visual QA) versus what must be preserved (e.g., provenance), reducing the cognitive load of debugging silent failures.

## Evidence

> Hardening asks how to stop failure; graceful extensibility asks what the system does after its assumptions fail.

> When Tier C disappears, preserve manifest truth and bounded backlog growth; shed visual QA before provenance, and never disguise deferred work as successful work.

## Examples

- A degraded-mode specification for Code-Brain that defines essential/nonessential capability tiers, load-shedding order, backlog ceilings, recovery semantics, and dependency-loss drills.

## Related Concepts

[[Agent Health]] [[Silent Failure Propagation in Agent Fleets]]
