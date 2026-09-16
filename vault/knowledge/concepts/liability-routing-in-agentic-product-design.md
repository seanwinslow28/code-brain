---
title: "Liability Routing in Agentic Product Design"
type: concept
sources:
  - 20_projects/research/2026-09-09-productcraft-research-cross-studio-handoff-prior-art.md
tags: [auto-generated, phase-6]
created: 2026-09-16
updated: 2026-09-16
---

## Definition

This concept defines the structural mechanism by which decision authority and failure accountability are assigned to specific agents within a typed handoff protocol. It relies on explicit state transitions—such as `TASK_STATE_REJECTED` or `INPUT_REQUIRED`—to force a refusal or request for clarification rather than allowing silent degradation. The system treats these refusals not as errors but as valid, addressable outcomes that preserve the integrity of the receiving agent's context.

## Context

Sean is building Productcraft and needs to ensure that when one agent hands off work to another, the receiving agent can definitively reject invalid inputs without corrupting its own state. This prevents the 'silent decay' where bad data propagates through a chain of autonomous agents because no one explicitly claimed responsibility for rejecting it.

## Evidence

> The typed protocol therefore encodes 'I will not do this' and 'I need more from you' as first-class outcomes, not as free text.

> Three terminal states (completed/failed/canceled) plus a terminal refusal (REJECTED) and two interrupted-pending-you states (INPUT_REQUIRED, AUTH_REQUIRED).

## Examples

- An agent returns `TASK_STATE_REJECTED` with a structured error code instead of generating hallucinated content.
- A task enters `TASK_STATE_INPUT_REQUIRED`, pausing the pipeline until the upstream provider supplies missing metadata.

## Related Concepts

[[Fault → Error → Failure Taxonomy]] [[Silent Failure Propagation in Agent Fleets]]
