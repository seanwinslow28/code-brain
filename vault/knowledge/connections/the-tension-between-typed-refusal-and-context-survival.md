---
title: "The Tension Between Typed Refusal and Context Survival"
type: connection
connects:
  - Liability Routing in Agentic Product Design
  - Context Compounding
  - Silent Failure Propagation in Agent Fleets
created: 2026-09-16
updated: 2026-09-16
---

## Synthesis

There is a critical tension between the need for agents to explicitly refuse invalid inputs (Liability Routing) and the need to preserve the full decision trace (Context Compounding). If an agent rejects a task, it must also transmit the specific context that made the input invalid; otherwise, the upstream agent cannot correct its behavior. This creates a dependency where 'refusal' is not just a stop signal but a complex data transfer requiring both structural clarity and semantic depth.

## Threads

### [[Liability Routing in Agentic Product Design]]

> The typed protocol therefore encodes 'I will not do this' and 'I need more from you' as first-class outcomes, not as free text.

### [[Context Compounding]]

> Decisions, constraints, discoveries, and partial state have to survive the handoff.

### [[Silent Failure Propagation in Agent Fleets]]

> When they don’t, each agent starts with an incomplete picture and the system gets brittle.

## Implications

- Sean must design Productcraft's handoff contracts to include not just the artifact but the 'rejected context' that led to its creation.
- Agent health monitoring must track not just successful completions but the quality of refusal messages to prevent upstream drift.
