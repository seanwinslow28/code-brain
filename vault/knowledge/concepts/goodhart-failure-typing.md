---
title: "Goodhart Failure Typing"
type: concept
sources:
  - knowledge/concepts/goodhart-failure-typing.md
tags: [auto-generated, phase-6]
created: 2026-08-19
updated: 2026-08-19
---

## Definition

This framework categorizes proxy failures into regressional, extremal, causal, and adversarial variants to diagnose when a metric ceases to correlate with the intended goal. In agentic systems, this manifests when optimizing for operational health (the proxy) actively degrades semantic value (the target), creating a regime where the system becomes robustly useless. The mechanism involves identifying which type of Goodhart failure is active to determine whether to adjust the metric, change the optimization strategy, or accept the trade-off.

## Context

Sean needs to apply David Manheim and Scott Garrabrant’s paper Categorizing Variants of Goodhart’s Law to separate regressional from extremal failures in his agent fleet. By typing the failure correctly, he can determine if improving hardware stability will actually improve semantic output or if he is facing an adversarial proxy failure where health metrics actively suppress insight generation.

## Evidence

> David Manheim and Scott Garrabrant’s paper Categorizing Variants of Goodhart’s Law separates regressional, extremal, causal, and adversarial proxy failures.

> The core tension lies in the decoupling of operational health metrics from semantic value, where systems report 'healthy' status based on process execution while knowledge integrity depends on successful insight generation.

## Examples

- Separating regressional, extremal, causal, and adversarial proxy failures.
- Implementing chaos engineering experiments to falsify the link between hardware stability and semantic novelty.

## Related Concepts

[[The Illusion of Health in Autonomous Systems]] [[Hardware Fragility Masks Semantic Decay in Agent Fleets]]
