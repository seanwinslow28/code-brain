---
title: "Automation Reliability"
type: concept
sources:
  - knowledge/expansions/automation-reliability.md
tags: [auto-generated, phase-6]
created: 2026-05-28
updated: 2026-05-28
---

## Definition

Automation reliability is the capacity of an agent fleet to maintain operational continuity despite component failures or silent logic errors. It requires shifting from simple benchmark accuracy to control-loop reliability, where safety cases define constraints on unsafe control actions rather than just measuring output variance. This mechanism treats reliability as a policy problem governed by error budgets, allowing the system to make go/no-go decisions based on SLOs rather than binary pass/fail metrics. The invariant is that silent failures in one agent's output propagate as stale context to dependent agents, creating a dependency chain that is invisible until the final user-facing artifact is generated.

## Context

Sean manages a personal knowledge vault where agents depend on each other's outputs. If the synthesizer fails silently, the morning brief inherits stale context, and the user notices the staleness before the brief flags the failure. This concept matters because it transforms how Sean evaluates his job-hunt infrastructure, moving from 'does it work?' to 'when should it stop working to prevent damage?'

## Evidence

> safety failures come from inadequate control, feedback, constraints, and process models, not only component breakage.

> Current concept treats reliability as a measurement problem; SRE turns it into a go/no-go policy: if schema-valid concept generation drops below X over Y runs, freeze model swaps, route to manual review, or spend budget on eval hardening before new agent features.

## Examples

- An agent safety case / incident review template for Sean’s fleet: controller, controlled process, feedback channel, unsafe control action, missing constraint.
- An executable eval harness for vault synthesizer/job-feed agents that finds silent failures without needing a golden answer for every article.

## Related Concepts

[[Automation Pipeline]] [[Agent Health]] [[Vault Synthesizer Eval Suite]]
