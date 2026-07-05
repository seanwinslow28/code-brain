---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - 20_projects/substack-studio/MIGRATION-REPORT.md
tags: [auto-generated, phase-6]
created: 2026-06-23
updated: 2026-06-23
---

## Definition

This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the operational interface for agents and version control. The system enforces a hard invariant that no named individuals, compensation terms, or proprietary identifiers can leak into the tracked knowledge graph, effectively decoupling the 'work-as-done' (private reality) from the 'work-as-promoted' (public artifact). This creates a dual-state vault where the public layer acts as a controlled abstraction, allowing agentic tools to function on structured data without accessing the raw, sensitive source material that triggered the initial privacy constraints.

## Context

Sean is managing a Substack series ('Raising Claude') that involves sensitive personal narratives and prior employment details. By routing this through a scrubbed public copy, he enables GitHub backup and cross-machine sync (the primary utility) while strictly adhering to his 'Do-Not-Promote' rule and Rule #10, preventing accidental exposure of private life-systems data in his public code-brain infrastructure.

## Evidence

> The privacy gate (Do-Not-Promote term / prior-employer name / named individuals / compensation terms / family names) returns zero hits across all tracked files.

> All edits applied to the public copy only; the un-scrubbed originals remain in the gitignored source.

## Examples

- The `_private/` directory is explicitly gitignored and empty of content, serving as a null sink for any accidental inclusion attempts.
- Originals were verified to have no git modifications, ensuring the 'copy-not-move' strategy preserved the private state while the public copy was transformed.

## Related Concepts

[[Vault as Agent Infrastructure]] [[Do-Not-Promote Framing]]
