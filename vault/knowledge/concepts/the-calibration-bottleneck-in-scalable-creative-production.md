---
title: "The Calibration Bottleneck in Scalable Creative Production"
type: concept
sources:
  - knowledge/concepts/the-calibration-bottleneck-in-scalable-creative-production.md
tags: [auto-generated, phase-6]
created: 2026-09-22
updated: 2026-09-22
---

## Definition

This pattern emerges when a high-performance, low-cost decision model is deployed at scale but lacks the robustness to handle distribution shifts or unanswerable queries. The bottleneck is not computational throughput but epistemic stability: the model performs well on known distributions ('strong zero-shot on semantic classification') but fails silently or incorrectly when faced with ambiguity ('calibration does not survive out-of-distribution'). This creates a production risk where speed and cost advantages are negated by the need for heavy human-in-the-loop verification on edge cases.

## Context

Sean is building automated fleets (vault synthesizer). If he integrates Jev, he must account for the fact that 'single broad questions underperform decomposed ones'. This limits the scalability of any creative or judgment pipeline that relies on Jev for initial triage or classification without rigorous decomposition steps.

## Evidence

> calibration does not survive out-of-distribution or unanswerable questions

> single broad questions underperform decomposed ones

> roughly tied with a frontier LLM at 1/100–1/300 of the cost and 2–3× the speed

## Examples

- The five reproducible GitHub evals showing 'strong zero-shot on semantic classification (83–96%)'
- The requirement to use 'decomposed ones' instead of broad questions to maintain accuracy

## Related Concepts

[[Supervision Fatigue as the Hard Cap on Fleet Scaling]] [[Silent Failure Propagation in Agent Fleets]]
