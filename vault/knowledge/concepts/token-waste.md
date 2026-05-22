---
title: "Token Waste"
type: concept
sources:
  - 40_knowledge/references/ref-66000-tokens-of-plugins-before-you-type.md
tags: [auto-generated, phase-6]
created: 2026-05-22
updated: 2026-05-22
---

## Definition

A systemic inefficiency in AI workflows where excessive tokens are consumed by non-essential elements such as plugin context, system prompts, and reference documents that are not cached. This creates a hidden cost multiplier where users pay disproportionately more for the same output due to avoidable overhead. The issue stems from a lack of awareness around how contextual loading influences token usage, leading to unnecessary consumption and limiting the scale or depth of AI tasks that could be performed within budget.

## Context

Token waste directly impacts Sean's ability to optimize his AI workflows, especially in areas like job hunting and knowledge synthesis. By reducing unnecessary token consumption, Sean can stretch his Claude credits further to explore more complex prompts or scale his research agents without hitting usage limits.

## Evidence

> The problem is that most people don’t know what they’re doing. They’re burning 5x, 10x, sometimes 20x what they should on the exact same work, and they think that’s just what AI costs.

> If your system prompt, tool definitions, and reference documents aren’t cached, you’re paying ten dollars for every dollar of stable context, and this should be the first thing you set up.

## Examples

- A production AI pipeline that ingests multiple long-form conversations per user, runs analysis across dozens of dimensions, and generates fully personalized output.
- Claude usage limits dominating every AI community on the internet.

## Related Concepts

[[Claude Skills]] [[Cost-Capped Agentic Workflows]]
