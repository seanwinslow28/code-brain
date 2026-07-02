---
title: "Complexity Override"
type: concept
sources:
  - knowledge/concepts/complexity-override.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

A decision mechanism that suspends standard single-shape routing constraints when a problem space is identified as inherently non-decomposable. This override prevents the system from forcing premature synthesis on messy topics, which would otherwise result in structurally unsound outputs that appear valid but lack depth. It acts as a circuit breaker for linear routing rules, allowing for experimental probing phases before any final synthesis occurs.

## Context

Sean's current infrastructure relies heavily on deterministic protocol instrumentation and single-shape constraints to manage workflow efficiency. However, this rigidity creates a structural fragility when applied to complex creative or research questions that require iterative exploration rather than linear decomposition. Recognizing this tension allows Sean to introduce a complexity-domain override that suspends standard constraints when the problem space is inherently non-decomposable.

## Evidence

> The tension exists between the efficiency of 'single-shape topics only' rules and the necessity of probing in complex domains where decomposition fails.

> Cynefin contradicts it: some research questions are not complicated-but-decomposable; they are complex, meaning the right move is probing multiple small experiments before synthesis.

## Examples

- Suspending single-shape routing rules for topics that resist decomposition
- Introducing non-linear probing phases before entering the synthesis stage

## Related Concepts

[[System Constraints]] [[Research Workflow Integration]]
