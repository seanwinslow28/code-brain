---
title: "Double-loop learning"
type: concept
sources:
  - knowledge/concepts/double-loop-learning.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This mechanism refers to the process by which a system identifies that its governing rules or mental models are themselves flawed, rather than just correcting errors within those rules. In the context of agent fleets, it requires the system to notice when the volume of output no longer correlates with insight quality, prompting a revision of the synthesis policy itself. Without this capability, the fleet continues to optimize for metrics that degrade overall value.

## Context

Sean's current setup lacks the mechanism by which the fleet notices that the rules themselves are wrong, forcing him to manually adjust the governing logic. This gap between automated execution and strategic adjustment is a key bottleneck in scaling his personal knowledge infrastructure.

## Evidence

> What is missing is the mechanism by which the fleet notices that the rules themselves are wrong.

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of agent-fleets-supporting-knowledge-synthesis.

## Examples

- The fleet's evaluation metrics should shift from 'concepts written' to 'rival hypotheses considered' to prevent shallow synthesis.
- Sean must implement a 'Synthesis Policy Change Record' to track when the fleet's rules need adjustment, not just its outputs.

## Related Concepts

[[The Illusion of Competence in Automated Systems]] [[Supervision as the New AI Edge]]
