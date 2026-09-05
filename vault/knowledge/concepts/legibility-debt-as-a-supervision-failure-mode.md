---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/connections/the-cost-of-ignored-debt-in-automated-workflows.md
tags: [auto-generated, phase-6]
created: 2026-09-05
updated: 2026-09-05
---

## Definition

This concept defines the accumulation of unstructured or poorly documented information that makes it difficult for humans to supervise automated systems. When agents generate outputs without clear provenance or context, the supervisor (Sean) must spend more time reconstructing the logic behind each output. This debt grows as the system scales, eventually exceeding the supervisor's capacity to verify, leading to blind trust in automated processes.

## Context

Sean is the primary supervisor of his agent fleet. As the vault grows, the 'legibility' of its contents decreases because the automated synthesis creates complex, non-obvious connections. This makes it harder for Sean to audit the vault's health, leading to a supervision failure where he cannot distinguish between high-quality and low-quality outputs.

## Evidence

> This connection reveals the tension between the efficiency of automated linting and the necessity of manual curation in maintaining a high-fidelity knowledge vault.

> Sean must prioritize manual curation of the vault's core structure over automated expansion to prevent further degradation.

## Examples

- The manifest lists '62c/29x' for one run and '125c/34x' for another, showing inconsistent output quality that is hard to track without manual review.
- The 'rejected_count' varies significantly (e.g., 7 vs 106), indicating that the system's ability to self-correct is unstable and dependent on external factors.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Silent Decay in Strategic Pipelines]]
