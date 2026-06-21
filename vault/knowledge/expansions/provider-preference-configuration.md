---
title: "How to make `Provider Preference Configuration` better"
type: expansion
parent: "[[provider-preference-configuration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-20
updated: 2026-06-20
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[provider-preference-configuration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “quality-gated LLM cascades,” not just provider preferences.**  
   Anchor it on Lingjiao Chen, Matei Zaharia, and James Zou’s paper [“FrugalGPT”](https://arxiv.org/abs/2305.05176), plus the newer routing/cascading framing in Dekoninck, Baader, and Vechev’s [“A Unified Approach to Routing and Cascading for LLMs”](https://arxiv.org/abs/2410.10347).  
   Sentence pattern to add: “Provider preference is a static policy knob; cascades are a learned decision system where cheap models attempt first, quality estimators decide escalation, and fallback is conditional on observed adequacy.”  
   This unlocks an **agent-routing RFC** for Code-Brain: task class → cheap/local first attempt → evaluator signal → escalation threshold → paid model cap. The current concept can say “sort by price”; this would let Sean specify when Qwen3-14B, gemma4:e4b, GPT-5.5, or Gemini DR should earn the next dollar.

2. **Add “resilience patterns for provider failure: circuit breakers, bulkheads, and load shedding.”**  
   Anchor it on Michael Nygard’s *Release It!* and Google SRE’s chapter [“Handling Overload”](https://sre.google/sre-book/handling-overload/).  
   Sentence pattern to add: “Fallbacks are not free reliability; without circuit breakers and backpressure, they can turn one provider outage into fleet-wide cost explosion, latency pileup, or degraded-output spam.”  
   This unlocks a **provider-failure runbook** for the autonomous fleet: when OpenRouter/provider X fails, trip breaker for N minutes, degrade to local summaries, skip noncritical agents, preserve daily-driver only, and write a manifest event. The current concept treats `allow_fallbacks` as uptime insurance; this adds the missing operational question: “What should not run when the good route is unavailable?”

3. **Add “route selection by eval contract,” not provider metadata.**  
   Anchor it on OpenAI’s [simple-evals / SimpleQA](https://github.com/openai/simple-evals) and Jason Wei et al.’s paper [“Measuring short-form factuality in large language models”](https://arxiv.org/abs/2411.04368).  
   Sentence pattern to add: “A provider policy is only meaningful when paired with task-specific evals: factual QA routes optimize abstention and correctness, critique routes optimize novelty and contradiction, code routes optimize patch validity, and research routes optimize citation grounding.”  
   This unlocks a **portfolio-grade executable demo**: `route_eval.py` runs Sean’s real task classes through local, subscription, and paid routes; outputs cost, latency, hallucination rate, abstention rate, and artifact usefulness. The current concept cannot distinguish “cheap and fast” from “cheap but silently wrong”; this makes provider preference defensible as agentic-engineering judgment rather than configuration trivia.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
