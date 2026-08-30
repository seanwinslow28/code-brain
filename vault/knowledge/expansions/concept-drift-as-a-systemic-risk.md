---
title: "How to make `Concept Drift as a Systemic Risk` better"
type: expansion
parent: "[[concept-drift-as-a-systemic-risk]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-30
updated: 2026-08-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[concept-drift-as-a-systemic-risk]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add “performative drift”: the system helps create the drift it observes

**What to add:** Distinguish exogenous concept drift from **performative prediction**. Sean’s Zillow example already contains the mechanism: predictions alter prices and seller behavior, which changes subsequent training data. Retraining can therefore amplify the loop rather than repair it.

**Anchor:** Juan Perdomo, Tijana Zrnic, Celestine Mendler-Dünner, and Moritz Hardt, [“Performative Prediction” (ICML 2020)](https://proceedings.mlr.press/v119/perdomo20a.html). Their key object is the *performatively stable point*: a model evaluated against the distribution produced by acting on its predictions.

**What it unlocks:** An **agent feedback-loop audit** for Code-Brain:  
`agent output → Sean’s action → changed environment → new evidence → next agent output`.  
This could become a Substack essay—*Your Agent Isn’t Tracking Reality; It’s Manufacturing Its Training Data*—plus an agent spec requiring intervention logging and counterfactual evaluation before automatic policy updates.

## 2. Add “recurring regimes”: adaptation should retrieve, not merely forget

**What to add:** The article assumes drift makes historical knowledge obsolete. That is often wrong. Hiring markets, editorial tastes, model availability, and machine uptime move through recurring contexts. The correct response may be to identify the returning regime and reactivate an old policy.

**Anchor:** Gerhard Widmer and Miroslav Kubat, [“Learning in the Presence of Concept Drift and Hidden Contexts” (1996)](https://www.cs.colostate.edu/~howe/cs640/papers/LearningInThePresenceOfConceptDrift.pdf). Their FLORA family keeps a trusted recent window while storing prior concept descriptions for reuse when contexts recur.

**What it unlocks:** A **regime-indexed memory design** for the agent fleet: persist `{context fingerprint, policy, observed outcome}` rather than continuously overwriting “current truth.” Sean could ship a runbook and executable demo that recognizes states such as `MBP reachable`, `job-market contraction`, or `subscription CLI rate-capped`, then restores the previously successful routing policy. This creates a concrete bridge to `Memory Rot and Lifecycle Management`.

## 3. Add a detector-to-response contract: “monitor performance” is not operational

**What to add:** Specify a sequential detector, its evidence stream, and the action attached to each threshold. Use **ADWIN** as the canonical pattern: maintain an adaptive window, compare its subwindows, and shrink it when the change exceeds a statistically bounded threshold. Sentence pattern:  
`signal → detection confidence → minimum evidence → reversible response → escalation condition`.

**Anchor:** Albert Bifet and Ricard Gavaldà, [“Learning from Time-Changing Data with Adaptive Windowing” (2007)](https://epubs.siam.org/doi/pdf/10.1137/1.9781611972771.42). ADWIN explicitly bounds false positives and false negatives instead of treating every performance wobble as drift.

**What it unlocks:** A **drift-response runbook and fleet health implementation** distinguishing `warning`, `confirmed drift`, and `insufficient labels`. For Sean’s job hunt, it prevents rewriting positioning after three rejections; for scheduled agents, it supports actions such as widen observation, shadow-test a replacement policy, rollback, or require human approval. The current concept identifies a risk but cannot yet produce a decision procedure.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
