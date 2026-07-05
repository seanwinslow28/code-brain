---
title: "Double-loop learning"
type: concept
sources:
  - knowledge/connections/the-volume-insight-tension-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-05
updated: 2026-07-05
---

## Definition

This mechanism refers to the process by which a system identifies that its governing rules or mental models are flawed and adjusts them accordingly, rather than merely optimizing within existing constraints. In the context of agent fleets, it requires the system to notice when the rules themselves are wrong, not just when the outputs are noisy. This is critical for maintaining long-term utility as the complexity of the knowledge base grows.

## Context

Sean needs a mechanism by which the fleet notices that the rules themselves are wrong. Without this, the fleet continues to produce high-volume, low-value outputs, reinforcing the trust deficit rather than resolving it.

## Evidence

> What is missing is the mechanism by which the fleet notices that the rules themselves are wrong.

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of agent-fleets-supporting-knowledge-synthesis.

## Examples

- Sean must implement a 'Synthesis Policy Change Record' to track when the fleet's rules need adjustment, not just its outputs.
- The fleet's evaluation metrics should shift from 'concepts written' to 'rival hypotheses considered' to prevent shallow synthesis.

## Related Concepts

[[Slop as a Trust Deficit]] [[Agent Fleet Observability Dashboard]]
