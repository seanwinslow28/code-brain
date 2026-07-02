---
title: "Double-loop learning"
type: concept
sources:
  - knowledge/connections/the-tension-between-volume-and-insight-in-agent-fleets.md
tags: [auto-generated, phase-6]
created: 2026-07-02
updated: 2026-07-02
---

## Definition

A mechanism where a system not only improves its outputs within existing rules but also detects and modifies the governing rules themselves when they are found to be incorrect or suboptimal. It requires an external critique or internal monitoring loop that identifies structural failures in the logic rather than just surface-level errors in execution. Without this capability, the system remains trapped in single-loop optimization, refining actions that do not address the root cause of poor outcomes.

## Context

Sean needs double-loop learning to prevent his fleet from optimizing for vanity metrics like 'concepts written' while ignoring the underlying quality of synthesis, which currently requires his manual oversight.

## Evidence

> The article currently describes agents improving outputs inside the same governing rules.

> What is missing is the mechanism by which the fleet notices that the rules themselves are wrong.

## Examples

- Shifting evaluation metrics from 'concepts written' to 'rival hypotheses considered' to prevent shallow synthesis.
- Implementing a policy change record to track when the fleet's rules need adjustment.

## Related Concepts

[[The Tension Between Volume and Insight in Agent Fleets]] [[Agent Fleet Observability Dashboard]]
