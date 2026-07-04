---
title: "Double-loop learning"
type: concept
sources:
  - knowledge/concepts/double-loop-learning.md
tags: [auto-generated, phase-6]
created: 2026-07-04
updated: 2026-07-04
---

## Definition

This mechanism describes a systemic failure mode where an automated system optimizes for local efficiency metrics while ignoring the degradation of its underlying governance rules. In agent fleets, this manifests as continued high-volume output despite declining insight quality, because the evaluation loop only measures quantity rather than the validity of the synthesis logic itself. The system remains trapped in a single-loop optimization cycle, treating symptoms like 'low concept count' as the problem to solve, rather than recognizing that the criteria for what constitutes a valid concept are fundamentally misaligned with the goal of deep understanding.

## Context

Sean is currently observing a trajectory where his fleet's output volume increases significantly (from 3 to 150 concepts) while the underlying quality and utility of those outputs remain questionable. Without intervening in the governing rules, he risks accumulating 'slop' that erodes trust in the system without providing any actual cognitive leverage or job-hunt advantage.

## Evidence

> What is missing is the mechanism by which the fleet notices that the rules themselves are wrong.

> The system continues to execute its current rules efficiently, but fails to notice that those rules are fundamentally flawed for the goal of insight generation.

## Examples

- Shifting evaluation metrics from 'concepts written' to 'rival hypotheses considered' to force deeper synthesis.
- Implementing a 'Synthesis Policy Change Record' to explicitly track adjustments to the fleet's governing logic rather than just its output volume.

## Related Concepts

[[Slop as a Trust Deficit]] [[Agent Fleet Observability Dashboard]]
