---
title: "Intent Engineering"
type: concept
sources:
  - knowledge/expansions/intent-engineering.md
tags: [auto-generated, phase-6]
created: 2026-08-28
updated: 2026-08-28
---

## Definition

A mechanism where high-level user intent is compiled into executable tool handles that carry specific, attenuated authorities rather than ambient credentials. This approach replaces broad access with task-scoped, revocable capabilities, ensuring that an agent can act only through authorities explicitly passed into the current task. The system enforces a boundary where naming a resource does not confer authority over it, requiring explicit declassification rules for data to cross security zones.

## Context

Sean is building a portfolio artifact that demonstrates provable security boundaries in agentic systems. By implementing this mechanism, he can show that injected payloads cannot acquire Keychain or filesystem authority, turning abstract security rhetoric into an inspectable, testable system architecture.

## Evidence

> The agent can act only through authorities explicitly passed into this task; naming a resource does not confer authority over it.

> Permission governs actions; information-flow policy governs what influenced those actions and where derived data may travel.

## Examples

- Compile an Intent Charter into short-lived tool handles for an MCP server
- Run adversarial GitHub-issue payloads to test authority boundaries
- Attach labels such as source=github_issue and integrity=untrusted to values

## Related Concepts

[[MCP Server Hardening]] [[Privacy-Aware Data Routing]] [[The Verification-Governance Inversion]]
