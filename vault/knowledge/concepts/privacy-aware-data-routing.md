---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - knowledge/connections/the-privacy-accessibility-paradox-in-agentic-workflows.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole input for agentic processing. The system enforces a strict boundary that prevents raw personal narratives from entering the agent's context window, thereby mitigating privacy leakage risks during automated synthesis. This separation requires continuous verification to ensure the proxy remains clean, creating a dependency on automated scripts rather than manual review.

## Context

Sean must implement automated verification scripts to continuously check that no private entities have leaked into the public copy, as manual review is not scalable. The reliance on a 'sanitized proxy' means that any agent operating on the public data lacks access to the full nuance of the original stories, potentially limiting the depth of agentic assistance in sensitive areas.

## Evidence

> This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole input for agentic processing.

> Sean must implement automated verification scripts to continuously check that no private entities have leaked into the public copy, as manual review is not scalable.

## Examples

- gitignored private directories
- sanitized, public-facing copy

## Related Concepts

[[Vault as Agent Infrastructure]] [[Do-Not-Promote Framing]]
