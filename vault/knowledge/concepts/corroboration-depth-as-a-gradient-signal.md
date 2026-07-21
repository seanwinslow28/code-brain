---
title: "Corroboration Depth as a Gradient Signal"
type: concept
sources:
  - knowledge/concepts/corroboration-depth-as-a-gradient-signal.md
tags: [auto-generated, phase-6]
created: 2026-07-21
updated: 2026-07-21
---

## Definition

This mechanism defines how the reliability of an automated judgment scales with the number and diversity of independent verification methods applied. A single signal, no matter how sophisticated, provides low confidence because it lacks orthogonal validation. As more distinct matchers (lexical, semantic, LLM-based) converge on the same result, the probability of a shared systematic error decreases. The depth of corroboration acts as a gradient that determines whether an automated output is safe to persist or requires human intervention.

## Context

Sean's research shows that no single matcher meets the 80% bar alone. He must design his system to require multiple converging signals before accepting a pain-point match, effectively using corroboration depth as the gatekeeper for automation trust.

## Evidence

> Shared source URL is a strong hint even when Jaccard score is low

> Evaluated the two-stage architecture proposed after pass 1: cheap candidate generation followed by rigorous judgment

## Examples

- Scoring precision/recall against the 80% campaign bar for each individual matcher
- Running within-run sanity probes to detect internal consistency issues

## Related Concepts

[[SRE Error Budget for Agents]] [[Verification-Governance Inversion]]
