---
title: "Harness Engineering Invariant"
type: concept
sources:
  - knowledge/concepts/harness-engineering-invariant.md
tags: [auto-generated, phase-6]
created: 2026-06-20
updated: 2026-06-20
---

## Definition

A structural constraint where the complexity of an agent's utility is inversely proportional to the simplicity of its maintenance surface. This invariant dictates that adding tools or capabilities expands the 'harness'—the browser, approvals, logs, and data feeds—creating new points of failure that require continuous inspection. The mechanism operates as a trade-off between immediate capability and long-term reliability, where owning the harness allows for deeper control but increases the cognitive load of maintenance.

## Context

Sean is building a personal knowledge vault and agent fleet; understanding this invariant helps him resist feature creep in his own tools. By recognizing that 'the parts that need care are the same' regardless of scale, he can prioritize robust verification loops over adding new capabilities to his synthesizer or daily-driver agents.

## Evidence

> Whether the harness is small or large, the parts that need care are the same, and they are more specific than 'keep it healthy' suggests.

> So when you set up your own agents, you are not only choosing a model. You are choosing how much of the harness you want to own versus rent.

## Examples

- The Vercel sales agent story illustrates that reducing tools can improve outcomes by simplifying the maintenance surface.
- Boat maintenance teaches that 'mostly' means failures stay small because there is enough care and margin in the system.

## Related Concepts

[[Agent Rationalization]] [[System Constraints]]
