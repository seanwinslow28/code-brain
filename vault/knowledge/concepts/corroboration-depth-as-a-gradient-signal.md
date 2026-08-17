---
title: "Corroboration Depth as a Gradient Signal"
type: concept
sources:
  - knowledge/concepts/corroboration-depth-as-a-gradient-signal.md
tags: [auto-generated, phase-6]
created: 2026-08-17
updated: 2026-08-17
---

## Definition

This mechanism defines a continuous reliability metric where automated decision confidence scales with the density of independent evidence sources converging on a single conclusion, rather than relying on binary thresholds. The underlying invariant is that convergence among distinct matchers reduces shared-error probability only if those matchers do not share common failure pathways or upstream assumptions. Systems must modulate their trust levels based on this gradient, treating corroboration count as a signal of epistemic safety rather than mere volume. This approach prevents the illusion of competence by forcing a dependency audit that distinguishes genuine independent verification from correlated errors arising from shared ontologies or model-derived assumptions.

## Context

Sean relies on this mechanism to determine when to trust automated synthesis outputs without manual review as his agent fleet grows. Distinguishing between genuine independent verification and correlated errors becomes critical for maintaining the integrity of his knowledge vault and job-hunt pipelines. Without this gradient, high-confidence but badly calibrated outputs can silently corrupt the system.

## Evidence

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[corroboration-depth-as-a-gradient-signal]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

> Replace “distinct matchers imply independent evidence” with a dependency audit. Lexical, embedding, and LLM judges can share the same source text, candidate generator, ontology, or model-derived assumptions.

## Examples

- Count *independent failure pathways*, not matcher types.
- The shippable artifact is a dependency matrix—`matcher × upstream assumption × observed joint-error rate`

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[SRE Error Budget for Agents]]
