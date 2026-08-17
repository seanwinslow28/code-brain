---
title: "Metric Distortion vs. Semantic Decay"
type: connection
connects:
  - Goodhart Failure Typing
  - The Illusion of Health in Autonomous Systems
  - Hardware Fragility Masks Semantic Decay in Agent Fleets
created: 2026-08-13
updated: 2026-08-13
---

## Synthesis

The tension lies between operational metrics that signal 'health' (uptime, completion rate) and semantic metrics that signal 'value' (novelty, connection density). When Sean optimizes for the former without auditing the latter, he creates a system that is robustly useless. The consequence is that hardware fragility masks this decay because the system appears to function correctly even as its cognitive output stagnates.

## Threads

### [[Goodhart Failure Typing]]

> David Manheim and Scott Garrabrant’s paper Categorizing Variants of Goodhart’s Law separates regressional, extremal, causal, and adversarial proxy failures.

### [[The Illusion of Health in Autonomous Systems]]

> declare fleet healthy from exit status despite zero novel concept edges.

### [[Hardware Fragility Masks Semantic Decay in Agent Fleets]]

> If hardware loss causes semantic decay, then disabling route X while holding inputs constant should move semantic measure Y by Z.

## Implications

- Sean must implement 'chaos engineering' experiments to falsify the link between hardware stability and semantic novelty.
- Exit codes are insufficient health indicators; semantic integrity checks must be added to the control loop.
