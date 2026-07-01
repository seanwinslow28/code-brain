---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - knowledge/concepts/privacy-aware-data-routing.md
tags: [auto-generated, phase-6]
created: 2026-07-01
updated: 2026-07-01
---

## Definition

This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole input for agentic processing. The system relies on a 'privacy gate' that actively filters out named individuals, compensation terms, and family names to prevent leakage into the agent-accessible knowledge graph. This creates a dependency risk where the integrity of the public proxy must be continuously verified against the private original, as any drift or scrubbing failure could inadvertently propagate sensitive information to external agents.

## Context

Sean faces a structural tension where the very data that gives his Substack series its unique value (personal, sensitive narratives) is also the data that must be excluded from his public, agent-accessible knowledge graph. This routing mechanism allows him to maintain two parallel states—private originals and public copies—while relying on strict gitignore rules rather than semantic understanding by the agents themselves.

## Evidence

> This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole input for agentic processing.

> The privacy gate (Do-Not-Promote term / prior-employer name / named individuals / compensation terms / family names) returns zero hits across all tracked files.

## Examples

- Sean consolidates 'Raising Claude' Substack work into a tracked public folder inside code-brain so it backs up to GitHub.
- The privacy gate returns zero hits across all tracked files for terms like 'Do-Not-Promote' or prior-employer names.

## Related Concepts

[[Vault as Agent Infrastructure]] [[Do-Not-Promote Framing]]
