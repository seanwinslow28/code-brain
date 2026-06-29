---
title: "Eval Vocabulary"
type: concept
sources:
  - knowledge/concepts/eval-vocabulary.md
tags: [auto-generated, phase-6]
created: 2026-06-29
updated: 2026-06-29
---

## Definition

This framework redefines evaluation as a dynamic, executable loop where datasets, evaluators, and traces form a repeatable cycle rather than static rubrics. It treats evals as decision instruments that require explicit lineage from business intent through observable metrics to pass/fail thresholds. The system must account for Goodhart's Law by recognizing that once agents optimize against visible proxies, the eval becomes an incentive structure that can degrade judgment quality over time.

## Context

Sean needs this to transition from describing specs as linters to building miniature eval labs that ship with fixtures and CI-style regression output. This allows him to produce a PM/IC portfolio one-pager that demonstrates how specific evals change decisions, rather than just measuring quality abstractly.

## Evidence

> The missing move is: business intent -> decision question -> observable metric -> eval case -> pass/fail threshold

> An eval becomes dangerous when it stops measuring judgment and starts training agents to satisfy the visible proxy

## Examples

- Bad spec, improved spec, adversarial spec, historical production trace, and CI-style regression output

## Related Concepts

[[Harness Engineering Invariant]] [[Intent Engineering]]
