---
title: "MCP Server Hardening"
type: concept
sources:
  - knowledge/expansions/connections/mcp-security-framework.md
tags: [auto-generated, phase-6]
created: 2026-08-13
updated: 2026-08-13
---

## Definition

Hardening an MCP server involves moving beyond input sanitization to enforce strict provenance tracking and capability-based access control. This requires treating tool output as data rather than executable instruction, ensuring that any privileged actions are derived solely from the authenticated user's intent and not influenced by untrusted external content. The mechanism relies on separating trusted control flow from untrusted data flow at every layer of the agent's execution stack.

## Context

Sean is building a portfolio demo for 'intent-engineering-mcp' that requires proving his system can withstand prompt injection attacks without relying on fragile regex filters.

## Evidence

> CaMeL separates trusted control flow from untrusted data flow and applies capability policies at exfiltration points, providing a reference implementation for defeating prompt injections by design.

> The MCP authorization specification explicitly identifies confused-deputy failure modes, requiring audience-bound tokens and per-client consent while prohibiting token passthrough.

## Examples

- Implementing an executable prompt-injection red-team demo where malicious issue text enters through one tool but is blocked by provenance checks before steering another.
- Creating a publishable authorization decision table that validates whether a client can invoke a specific tool on a resource for a declared intent.

## Related Concepts

[[MCP Server Hardening]] [[Velocity vs. Judgment in MCP Strengthening]] [[Control Plane / Data Plane Split for Agent Fleets]]
