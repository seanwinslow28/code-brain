---
title: "Intent Engineering"
type: concept
sources:
  - knowledge/concepts/intent-engineering.md
tags: [auto-generated, phase-6]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

Intent engineering is an architectural discipline that compiles high-level security policies into executable constraints, thereby governing agent behavior through structural enforcement rather than relying on natural language instructions which are inherently vulnerable to context drift. This approach functions by strictly separating the control plane, where trusted planners operate, from the data plane, where untrusted tool output resides, ensuring that even if an attacker manipulates the data, the control flow remains bound to the original intent specification. By treating prompt injection as an architectural information-flow problem rather than a mere prompting issue, it creates a provable security boundary where specific capabilities are delegated only when explicitly authorized by the intent charter.

## Context

Sean is building a personal knowledge vault that interacts with external APIs and MCP servers, exposing him to the risk of 'confused deputies' where an agent might inadvertently use credentials for the wrong resource due to prompt injection. This concept provides the structural solution to maintain authority over his own infrastructure by ensuring that GitHub issue text may influence classification but never selects a credential-reading or outbound-network action.

## Evidence

> Intent engineering is the architectural practice of compiling high-level security policies into executable constraints that govern agent behavior, rather than relying on natural language instructions which are vulnerable to context drift.

> The seven-part intent specification compiles into capabilities and flow constraints: 'GitHub issue text may influence classification but may never select a credential-reading or outbound-network action.'

## Examples

- Treating prompt injection as an 'architectural information-flow problem' rather than a prompting issue.
- Using 'capability-based enforcement' to report provable security on agent tasks.

## Related Concepts

[[Control Plane / Data Plane Split for Agent Fleets]] [[Liability Routing in Agentic Product Design]]
