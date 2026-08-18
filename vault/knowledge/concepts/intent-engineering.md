---
title: "Intent Engineering"
type: concept
sources:
  - knowledge/concepts/intent-engineering.md
tags: [auto-generated, phase-6]
created: 2026-08-18
updated: 2026-08-18
---

## Definition

Intent engineering is the architectural practice of compiling high-level security policies into executable constraints that govern agent behavior, rather than relying on natural language instructions which are vulnerable to context drift. It functions by separating the 'control plane' (trusted planner) from the 'data plane' (untrusted tool output), ensuring that even if an attacker manipulates the data, the control flow remains bound to the original intent. This creates a provable security boundary where specific capabilities are delegated only when explicitly authorized by the intent specification.

## Context

Sean is building a personal knowledge vault that interacts with external APIs and MCP servers. He faces the risk of 'confused deputies' where an agent might inadvertently use credentials for the wrong resource due to prompt injection. This concept provides the structural solution to maintain authority over his own infrastructure.

## Evidence

> The seven-part intent specification compiles into capabilities and flow constraints: 'GitHub issue text may influence classification but may never select a credential-reading or outbound-network action.'

> Required pattern: one audience-bound token per resource; never relay an inbound bearer token downstream; record consent per client.

## Examples

- Treating prompt injection as an 'architectural information-flow problem' rather than a prompting issue.
- Using 'capability-based enforcement' to report provable security on agent tasks.

## Related Concepts

[[Control Plane / Data Plane Split for Agent Fleets]] [[Liability Routing in Agentic Product Design]]
