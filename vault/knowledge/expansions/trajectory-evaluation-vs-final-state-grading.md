---
title: "How to make `Trajectory Evaluation vs. Final-State Grading` better"
type: expansion
parent: "[[trajectory-evaluation-vs-final-state-grading]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-31
updated: 2026-08-31
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[trajectory-evaluation-vs-final-state-grading]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Add three-valued runtime verification

**What to add:** Replace the article’s vague “continuous monitoring” with executable temporal contracts over finite traces: `satisfied`, `violated`, or `inconclusive`. Long-running agents often cannot honestly be graded pass/fail mid-run. Example properties:

- `approval must precede destructive_action`
- `deny implies no later equivalent_action`
- `tool_call must eventually receive result_or_timeout`
- `budget_exceeded implies terminate_before_next_call`

**Anchor:** Martin Leucker and Christian Schallhart, [“A Brief Account of Runtime Verification”](https://www.isp.uni-luebeck.de/research/publications/brief-account-runtime-verification), plus Andreas Bauer, Martin Leucker, and Christian Schallhart’s finite-trace semantics work. They show how formal specifications become monitors and why partial traces require more than Boolean judgment.

**What this unlocks:** An executable **trajectory-contract specification** for `intent-engineering`, plus a portfolio demo that replays fleet traces against generated state machines. The current concept can argue that paths matter; this addition lets Sean compile “how” into enforceable tests.

### 2. Add adversarial trajectory generation, not merely trajectory observation

**What to add:** Introduce **counterfactual trace testing**: deliberately mutate tool responses, permissions, environmental state, and timing to discover trajectories the production fleet has not yet produced. Sentence pattern: “A trace evaluator detects known bad behavior; an adversarial emulator manufactures the conditions under which unknown bad behavior becomes likely.”

**Anchor:** Yangjun Ruan et al., [“Identifying the Risks of LM Agents with an LM-Emulated Sandbox”](https://proceedings.iclr.cc/paper_files/paper/2024/hash/7274ed909a312d4d869cc328ad1c5f04-Abstract-Conference.html). Their **ToolEmu** framework emulates tools and uses adversarially chosen sandbox states to expose long-tail agent failures before real deployment.

**What this unlocks:** A reusable **fleet chaos-testing harness** and incident runbook: inject stale context, partial tool success, permission drift, duplicate responses, host loss, or misleading success codes, then score the resulting trajectory. The current article remains retrospective; this turns evaluation into prospective red-teaming.

### 3. Add selective prediction for the trajectory judge itself

**What to add:** Treat the agentic judge as another fallible model requiring a **reject option**. Track judge risk against coverage instead of pretending every trajectory can be classified confidently. Require abstention or human review when judges disagree, evidence is incomplete, or the trace lies outside the calibration set.

**Anchor:** Yonatan Geifman and Ran El-Yaniv, [“Selective Classification for Deep Neural Networks”](https://arxiv.org/abs/1705.08500), and their follow-up [“SelectiveNet: A Deep Neural Network with an Integrated Reject Option”](https://proceedings.mlr.press/v97/geifman19a.html). The core construct is the **risk–coverage trade-off**: lowering tolerated error necessarily reduces how many cases the model may decide automatically.

**What this unlocks:** A **human-escalation policy and calibration dashboard** for the Vault Critic or governance demo: “At ≤5% measured judge error, automate 72% of traces; route the remainder to Sean.” The current concept scrutinizes the worker’s epistemic trustworthiness while leaving the evaluator’s trustworthiness unexamined.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
