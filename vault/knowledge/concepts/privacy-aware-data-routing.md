---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - knowledge/connections/the-tension-between-privacy-isolation-and-agentic-accessibility.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole interface for agentic systems. The routing logic enforces a strict boundary: any concept derived from private ancestors cannot be promoted to the public graph without explicit review, ensuring that privacy follows derivation rather than location. This creates a proxy layer that allows agents to operate on structured knowledge without ever accessing the raw, sensitive source material, effectively decoupling agentic utility from data exposure.

## Context

Sean's Substack series relies on personal narratives that are valuable precisely because they are sensitive; however, his agent infrastructure requires broad access to function. This tension forces him to maintain two parallel states of truth, creating a dependency risk where the public copy may lack the nuance necessary for deep agentic assistance if the scrubbing process is imperfect.

## Evidence

> The privacy gate (Do-Not-Promote term / prior-employer name / named individuals / compensation terms / family names) returns zero hits across all tracked files.

> Privacy follows derivation, not location: every generated concept stores `why_provenance` and `where_provenance`; if any ancestor is private, the descendant cannot be promoted without review.

## Examples

- The scrubbing process that removes prior-employer names and family names from the public copy of the Substack work.
- The gitignore rules that prevent private directories from syncing to GitHub or being indexed by the MCP server.

## Related Concepts

[[Vault as Agent Infrastructure]] [[Do-Not-Promote Framing]]
