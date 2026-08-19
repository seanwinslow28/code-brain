---
title: "Legibility Debt as a Supervision Failure Mode"
type: concept
sources:
  - knowledge/concepts/legibility-debt-as-a-supervision-failure-mode.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

Legibility debt is the accumulation of opacity in an automated system's internal state, creating a widening gap between reported metrics and actual operational reality. This debt manifests as a systemic trust deficit because the human supervisor can no longer verify output correctness without expending more cognitive effort than the automation originally saved. The underlying mechanism is a failure of observability where the causal 'why' of a decision is lost within the sheer volume of the 'what', forcing the operator to treat all outputs as potentially suspect.

## Context

Sean's vault relies on his ability to trust the synthesizer's output without constant manual verification. When legibility debt grows, he must revert to manual auditing, which negates the efficiency gains of automation and creates a hidden, compounding cost in cognitive load that eventually breaks the feedback loop necessary for system improvement.

## Evidence

> This connection reveals a fundamental tension where the drive for automated throughput directly conflicts with the preservation of taste memory, leading to a systemic trust deficit.

> As Sean increases throughput, the preservation of taste memory is directly conflicted by the automation's output volume.

## Examples

- The rejected_count in run-2026-08-15 was 36, indicating a significant portion of output required manual rejection due to lack of legibility.
- The duration_seconds for run-2026-08-15 was 2733.9, showing that high throughput does not correlate with faster curation.

## Related Concepts

[[The Taste-Throughput Trade-off in Agentic Synthesis]] [[Supervision Fatigue as the Hard Cap on Fleet Scaling]]
