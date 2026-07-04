---
title: "Privacy-Aware Data Routing"
type: concept
sources:
  - knowledge/concepts/privacy-aware-data-routing.md
tags: [auto-generated, phase-6]
created: 2026-07-04
updated: 2026-07-04
---

## Definition

This mechanism establishes a strict architectural bifurcation where high-risk personal data is isolated in gitignored private directories, while a sanitized proxy serves as the sole input for agentic processing. The system enforces a boundary that prevents raw narratives from entering the agent's context window, thereby mitigating privacy leakage during automated synthesis. This separation creates a dependency on continuous automated verification scripts to ensure the public copy remains clean, as manual review is not scalable for this volume of data.

## Context

Sean must implement these verification scripts because the reliance on a sanitized proxy means agents lack access to full nuance, potentially limiting assistance depth in sensitive areas. The tension lies in balancing the need for agentic utility against the risk of exposing private entities through automated leakage.

## Evidence

> This mechanism describes a deliberate architectural split where sensitive, high-risk personal data is isolated in gitignored private directories while a sanitized, public-facing copy serves as the sole input for agentic processing.

> Sean must implement automated verification scripts to continuously check that no private entities have leaked into the public copy, as manual review is not scalable.

## Examples

- gitignored private directories
- sanitized, public-facing copy

## Related Concepts

[[Vault as Agent Infrastructure]] [[Do-Not-Promote Framing]]
