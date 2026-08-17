---
title: "How to make `Intent Engineering, Provider Fallback, and Eval Vocabulary Cross-System Resilience` better"
type: expansion
parent: "[[intent-engineering-provider-fallback-and-eval-vocabulary-cross-system-resilience]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-12
updated: 2026-08-12
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[intent-engineering-provider-fallback-and-eval-vocabulary-cross-system-resilience]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add **constraint-based intent** using STPA

- **What:** Replace “agents align with intent” with a control-theoretic model: losses → hazards → safety constraints → unsafe control actions. Test four cases: action omitted, action issued, wrong timing/order, or action continued/stopped incorrectly. Sentence pattern: *“Intent is not the objective an agent repeats; it is the constraint its actions must preserve under changing feedback.”*
- **Anchor:** Nancy Leveson, [*Engineering a Safer World*](https://maritimesafetyinnovationlab.org/wp-content/uploads/2021/04/Engineering_a_Safer_WorldNancyLeveson.pdf), especially the STPA method. Its useful contradiction is that accidents can arise from unsafe interactions even when every component operates as designed.
- **Unlock:** An **Agent Hazard Analysis** for the intent-engineering MCP server: control structure, unsafe actions, stale-feedback scenarios, and enforceable constraints. This would produce a distinctive portfolio artifact—part agent spec, part safety case—that goes beyond the current hiring-oriented claim that the system is “aligned and resilient.”

## 2. Add **behavioral substitutability contracts** for provider fallback

- **What:** Treat each provider as a behavioral subtype, not merely another endpoint. Define preconditions, postconditions, invariants, and history properties that must remain true after routing changes. Sentence pattern: *“Provider B is a valid fallback for Provider A only if no downstream consumer can observe a violation of the task contract.”*
- **Anchor:** Barbara Liskov and Jeannette Wing, [“A Behavioral Notion of Subtyping”](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf). Their substitution rule supplies the missing formal vocabulary for distinguishing genuine fallback from “the request returned something.”
- **Unlock:** An executable **Provider Conformance Suite** for the routing layer: structured-output preservation, citation requirements, tool-call semantics, refusal boundaries, latency ceilings, and degradation declarations. Sean could ship an outage-injection demo showing a route fail over, fail closed, or downgrade explicitly—much stronger evidence than a topology diagram listing Ollama → local heavyweight → cloud.

## 3. Replace the scalar eval with a **capability × behavior matrix**

- **What:** Recast “7/10 baseline plus six failure modes” using three named test types: Minimum Functionality Tests, Invariance tests, and Directional Expectation tests. Apply the same cases before and after provider substitution. Example: formatting noise should not alter an intent classification; increasing blast radius should move the decision toward escalation, never toward autonomy.
- **Anchor:** Marco Tulio Ribeiro, Tongshuang Wu, Carlos Guestrin, and Sameer Singh, [“Beyond Accuracy: Behavioral Testing of NLP Models with CheckList”](https://aclanthology.org/2020.acl-main.442/). CheckList turns vague eval coverage into explicit, diagnostic behaviors.
- **Unlock:** A publishable **Cross-Provider Behavioral Benchmark** and accompanying routing decision record. It would let Sean answer the senior-screen question the concept currently dodges: *Which capabilities survive fallback, which degrade, and which failures force the system to stop rather than silently continue?*

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
