---
title: "Complexity Override vs. Single-Shape Constraints"
type: connection
connects:
  - System Constraints
  - Research Workflow Integration
  - Context Management as a Bottleneck
created: 2026-06-30
updated: 2026-06-30
---

## Synthesis

The tension exists between the efficiency of 'single-shape topics only' rules and the necessity of probing in complex domains where decomposition fails. Single-shape constraints work for complicated problems but break down when applied to complex questions that require experimental iteration rather than linear routing. The consequence is that Sean’s current system may force premature synthesis on messy topics, leading to low-quality outputs that appear valid but are structurally unsound. Recognizing this tension allows him to introduce a complexity-domain override that suspends standard constraints when the problem space is inherently non-decomposable.

## Threads

### [[System Constraints]]

> Cynefin contradicts it: some research questions are not complicated-but-decomposable; they are complex, meaning the right move is probing multiple small experiments before synthesis.

### [[Research Workflow Integration]]

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-methodology-integration]].

### [[Context Management as a Bottleneck]]

> Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[harness-engineering-invariant]].

## Implications

- Sean needs a decision tree that identifies 'complex' domains early to bypass single-shape routing rules.
- Research protocols must allow for non-linear probing phases before entering the synthesis stage for complex topics.
- The system should flag topics that resist decomposition as candidates for the complexity override rather than forcing them into standard queues.
