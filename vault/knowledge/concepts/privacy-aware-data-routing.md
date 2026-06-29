---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - knowledge/connections/the-tension-between-privacy-isolation-and-agentic-accessibility.md
tags: [auto-generated, phase-6]
created: 2026-06-29
updated: 2026-06-29
---

## Definition

This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole interface for agentic systems. The invariant here is that privacy follows derivation rather than location; any generated concept must store its provenance chain so that if any ancestor node contains private information, the descendant cannot be promoted to the public graph without explicit review. This creates a dependency where the integrity of the public knowledge graph relies entirely on the correctness of the scrubbing process, as agents lack the semantic capability to distinguish between safe abstraction and leaked identity.

## Context

Sean's Substack series derives its unique value from personal, sensitive narratives that must be excluded from his public, agent-accessible knowledge graph. This routing mechanism allows him to maintain a 'sanitized proxy layer' for his AI agents while keeping the raw emotional and factual truth in private storage, preventing accidental exposure of family names or compensation terms.

## Evidence

> The privacy gate returns zero hits across all tracked files when checking for named individuals, compensation terms, or family names.

> Privacy follows derivation, not location: every generated concept stores why_provenance and where_provenance; if any ancestor is private, the descendant cannot be promoted without review.

## Examples

- A scrubbing process that filters out 'Do-Not-Promote' framing elements like prior-employer names before data enters the public graph.
- The requirement that Sean maintain two parallel states: private originals for narrative depth and public copies for agentic accessibility.

## Related Concepts

[[Vault as Agent Infrastructure]] [[Do-Not-Promote Framing]]
