---
title: "Eval Vocabulary"
type: concept
sources:
  - knowledge/expansions/eval-vocabulary.md
tags: [auto-generated, phase-6]
created: 2026-06-24
updated: 2026-06-24
---

## Definition

An operational framework that shifts evaluation from static rubrics to dynamic, executable systems where datasets, evaluators, and traces form a repeatable loop. This approach treats evals as decision instruments rather than mere scoring tools, requiring explicit lineage from business intent through observable metrics to pass/fail thresholds. The system must account for Goodhart's Law by recognizing that once agents optimize against visible proxies, the eval becomes an incentive structure that can degrade judgment quality over time.

## Context

Sean needs this to transition from describing specs as linters to building miniature eval labs that ship with fixtures and CI-style regression output. This allows him to produce a PM/IC portfolio one-pager that demonstrates how specific evals change decisions, rather than just measuring quality abstractly.

## Evidence

> The missing move is: business intent -> decision question -> observable metric -> eval case -> pass/fail threshold

> An eval becomes dangerous when it stops measuring judgment and starts training agents to satisfy the visible proxy

> Sean’s current concept describes a spec linter; these works turn it into a repeatable system

## Examples

- Bad spec, improved spec, adversarial spec, historical production trace, and CI-style regression output

## Related Concepts

[[Harness Engineering Invariant]] [[Intent Engineering]]
