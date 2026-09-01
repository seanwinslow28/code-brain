---
title: "Golden Dataset as Taste Artifact"
type: concept
sources:
  - knowledge/concepts/golden-dataset-as-taste-artifact.md
tags: [auto-generated, phase-6]
created: 2026-09-01
updated: 2026-09-01
---

## Definition

The construction of a 'golden dataset' functions not merely as a technical baseline for regression testing, but as an externalized manifestation of the creator's aesthetic and functional preferences. When a system requires weeks to compile real human interactions into a reference set before any model selection occurs, the resulting artifact becomes a rigid constraint on future creative direction. This process forces the agent to codify implicit taste into explicit, non-negotiable data points that dictate what constitutes 'correct' behavior.

## Context

Sean is building a personal knowledge vault and agent fleet where 'taste' is often subjective and hard to automate. By treating the evaluation dataset as a primary artifact rather than a secondary test suite, he can lock in his specific editorial standards early, preventing the drift toward generic or low-quality outputs that often plague automated synthesis.

## Evidence

> building the evaluation layer must precede writing any application code or selecting models

> spent weeks 1 and 2 purely on building the evaluation database (compiling 200 real human agent chats to represent the 'golden data set') and establishing metrics before ever testing a model

## Examples

- Databricks team compiling 200 real human agent chats to create a golden dataset for a retail banking chatbot
- Anthropic's separation of test suites into Capability Evals (low pass rate) and Regression Evals (high pass rate)

## Related Concepts

[[Taste as Evaluation Function vs. Activity Proof]] [[Supervision as the New AI Edge]]
