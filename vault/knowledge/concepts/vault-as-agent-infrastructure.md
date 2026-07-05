---
title: "Vault as Agent Infrastructure"
type: concept
sources:
  - knowledge/connections/archival-offloading-as-context-optimization.md
tags: [auto-generated, phase-6]
created: 2026-05-31
updated: 2026-05-31
---

## Definition

Vault as Agent Infrastructure is the pattern where the knowledge base serves as the literal control plane for autonomous work, requiring explicit design of context preparation to survive handoffs between agents. This mechanism treats the vault not as a passive archive but as an active system where decisions, constraints, discoveries, and partial state must survive the transition from one agent to another. When this survival fails, each agent starts with an incomplete picture, making the system brittle and prone to errors. The consequence is that the vault's structure directly dictates the reliability and coherence of the entire agentic workflow.

## Context

Sean's vault is currently failing to protect the integrity of active work because historical data is not properly isolated. This failure mode leads to the token waste and roadmap bloat that degrade his agent's performance. The implication is that the vault must be treated as a critical infrastructure component where context preparation is an explicit design problem, not an afterthought.

## Evidence

> Decisions, constraints, discoveries, and partial state have to survive the handoff. When they don’t, each agent starts with an incomplete picture and the system gets brittle.

> This file holds the ship history — dated amendments and the bodies of fully-closed tasks.

## Examples

- The vault holding the ship history with dated amendments and the bodies of fully-closed tasks.

## Related Concepts

[[Token Waste]] [[Unified Roadmap]]
