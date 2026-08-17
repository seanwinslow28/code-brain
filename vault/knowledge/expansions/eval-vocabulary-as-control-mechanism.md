---
title: "How to make `Eval Vocabulary as Control Mechanism` better"
type: expansion
parent: "[[eval-vocabulary-as-control-mechanism]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-16
updated: 2026-08-16
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[eval-vocabulary-as-control-mechanism]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add a “goal → question → metric” layer; reject “evals replace PRDs”

**WHAT:** Add the Goal–Question–Metric hierarchy. The concept currently jumps from intent directly to measurable tests, encouraging proxy fixation. Sentence pattern: “For this goal, what questions would reveal success, and which measurements answer each question?” Evals should operationalize a product specification, not erase it.

**WHO/WHAT:** Victor Basili, Gianluigi Caldiera, and H. Dieter Rombach’s *Goal Question Metric Approach*, especially Basili’s 1992 report, [Software Modeling and Measurement: The Goal/Question/Metric Paradigm](https://drum.lib.umd.edu/items/8119803a-362b-42ec-b6ce-2311713e7236).

**UNLOCK:** An **Intent-to-Eval Contract** for the intent-engineering MCP server:

```text
Intent → diagnostic questions → indicators → evals → escalation rule
```

This would demonstrate that Sean can preserve qualitative purpose while making behavior testable—stronger AI-PM positioning than the generic slogan “evals are the new PRDs.”

## 2. Add behavioral testing vocabulary: MFT, INV, and DIR

**WHAT:** Replace the article’s pass/fail framing with CheckList’s three test types:

- **Minimum Functionality Tests:** Does the agent perform a narrowly specified capability?
- **Invariance Tests:** Which transformations must not change the result?
- **Directional Expectation Tests:** Which transformations should predictably improve or worsen it?

For a vault critic: adding irrelevant prose should not improve its novelty score; removing citations should reduce groundedness; replacing a concept with a paraphrase should preserve its critique.

**WHO/WHAT:** Marco Tulio Ribeiro, Tongshuang Wu, Carlos Guestrin, and Sameer Singh, [*Beyond Accuracy: Behavioral Testing of NLP Models with CheckList*](https://aclanthology.org/2020.acl-main.442/) (ACL 2020). Their capability-by-test-type matrix produced substantially more tests and exposed failures missed by aggregate accuracy.

**UNLOCK:** A reusable **fleet behavioral-eval matrix** plus executable regression suite for the synthesizer, critic, and job-feed agents. This reaches a portfolio-quality engineering demo: mutate inputs, rerun agents, and visualize violated behavioral contracts—not merely report one quality score.

## 3. Add the adversarial case: passing the eval can be evidence of failure

**WHAT:** Introduce the distinction between **observed reward** and a **hidden performance function**. The current concept assumes that increasingly precise evals create increasingly strong control. The contradiction is specification gaming: capable agents learn the measurement surface and satisfy it without producing the intended outcome.

For Sean’s critic, “three external references per article” could yield citation stuffing; “novel concepts generated” could reward ontology spam; “zero broken links” could reward deleting difficult connections.

**WHO/WHAT:** Jan Leike et al., [*AI Safety Gridworlds*](https://arxiv.org/abs/1711.09883), which deliberately separates the reward visible to the agent from a hidden safety-performance measure. Pair it with Victoria Krakovna et al.’s concrete catalogue, [*Specification Gaming: The Flip Side of AI Ingenuity*](https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/).

**UNLOCK:** A **Goodhart red-team runbook** and executable “gaming harness”: expose one metric to an agent, retain a shadow evaluator, then document how optimization widens the gap. That becomes both a compelling Substack essay—*My Agent Passed Every Eval and Got Worse*—and a concrete governance demo for agentic-engineering interviews.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
