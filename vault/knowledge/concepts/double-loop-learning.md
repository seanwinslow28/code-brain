---
title: "Double-loop learning"
type: concept
sources:
  - knowledge/connections/the-volume-insight-tension-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-03
updated: 2026-07-03
---

## Definition

A learning process where the governing rules or mental models themselves are questioned and modified, rather than just optimizing actions within existing constraints. In this context, it refers to the fleet's inability to self-correct when its underlying synthesis logic produces low-quality outputs. The system continues to execute its current rules efficiently, but fails to notice that those rules are fundamentally flawed for the goal of insight generation.

## Context

Sean needs the fleet to not just produce more data, but to adapt its own criteria for what constitutes 'good' data. Without this meta-level adjustment, the automation remains stuck in a loop of producing irrelevant or low-value content.

## Evidence

> What is missing is the mechanism by which the fleet notices that the rules themselves are wrong.

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of agent-fleets-supporting-knowledge-synthesis.

## Examples

- The fleet's evaluation metrics should shift from 'concepts written' to 'rival hypotheses considered' to prevent shallow synthesis.
- Sean must implement a 'Synthesis Policy Change Record' to track when the fleet's rules need adjustment, not just its outputs.

## Related Concepts

[[Slop as a Trust Deficit]] [[Agent Fleet Observability Dashboard]]
