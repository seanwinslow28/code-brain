---
title: "How to make `Infrastructure Status` better"
type: expansion
parent: "[[infrastructure-status]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-27
updated: 2026-05-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[infrastructure-status]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “USE Method status cards” anchored on Brendan Gregg’s _The USE Method_**

   Add a diagnostic layer that reports every runtime/machine as **Utilization, Saturation, Errors** rather than “fast/accurate/best.” Sentence pattern:

   > “MBP-Ollama qwen3.6:35b-a3b is Tier A only when GPU utilization is below X, memory pressure below Y, queue depth below Z, and error rate below N.”

   Exemplified by: Brendan Gregg, [_The USE Method_](https://www.brendangregg.com/usemethod.html).

   This unlocks an **agent fleet runbook** instead of a concept note: “If vault_synthesizer misses schema, check saturation before swapping models.” Right now the concept names winners; USE would let Sean explain *why a winner stops being a winner under load*.

2. **Add “error-budget routing” anchored on Google SRE’s _Service Level Objectives_ chapter**

   The concept treats accuracy-critical vs. speed-critical as qualitative. Add explicit **SLO classes** for local inference:

   - `Tier A`: schema validity >= 95%, recall >= 5/5, timeout <= 900s
   - `Tier B`: draft latency <= N seconds, schema validity allowed to degrade
   - `Fallback`: cloud only after local error budget burns

   Exemplified by: Betsy Beyer, Chris Jones, Jennifer Petoff, Niall Richard Murphy, eds., [_Site Reliability Engineering_, Chapter 4: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/).

   This unlocks a **portfolio-grade “Local Agent SRE” one-pager**: Sean can show that his fleet is governed by reliability contracts, not vibes. It also creates a concrete decision artifact: “When does MBP-Ollama displace LM Studio, and when does it merely join the pool?”

3. **Add “capacity frontier / roofline thinking” anchored on Williams, Waterman & Patterson’s _Roofline_ paper**

   The concept says runtime choice is non-uniform across model family, but it does not name the deeper pattern: every model/runtime/machine pair sits on a **capacity frontier** bounded by memory bandwidth, compute throughput, context length, quantization, batching, and decode policy.

   Add a small “frontier table” per candidate:

   > “This model is memory-bound on MBP-Ollama, decode-bound on LM Studio, and VRAM-bound on Alienware; do not compare tok/s without identifying the bottleneck.”

   Exemplified by: Samuel Williams, Andrew Waterman, David Patterson, [_Roofline: An Insightful Visual Performance Model for Multicore Architectures_](https://people.eecs.berkeley.edu/~kubitron/courses/cs252-S12/handouts/papers/Roofline.pdf).

   This unlocks an **executable benchmark dashboard** or Substack essay: “Why my local AI stack does not have a best model.” The current concept can say “qwen3.6 wins”; roofline mode lets Sean produce a more senior artifact: a falsifiable routing model that predicts when the winner changes.

## From Anti-Gravity (Gemini 3)

### 1. Semantic Circuit Breaking (System Architecture)
- **WHAT:** Your "Infrastructure Status" assumes that if a runtime is up, it can handle the workload. You are missing **Semantic Circuit Breaking**—the practice of failing fast not just on network timeouts, but on *schema degradation*. If Ollama on the MBP falls back to a smaller model, you shouldn't send it the exact same prompt; you must degrade the *intent complexity*.
- **WHO/WHAT:** Michael T. Nygard’s *Release It!* (specifically the Circuit Breaker and Bulkhead patterns), applied to LLM reasoning envelopes rather than just database queries.
- **WHAT IT UNLOCKS:** **Artifact: `agents-sdk/lib/semantic_breaker.py`**. Instead of a binary "fallback to Claude API" when your Mac Mini times out, you write an executable wrapper that detects when a local model's output schema degrades below 85% match. The circuit trips, automatically stripping complex JSON-schema requirements from the prompt and asking the fallback model for plain markdown instead. This unlocks a Substack essay on "Graceful Degradation in Agentic Systems," mapping perfectly to your intent-engineering framework.

### 2. Promise Theory for Runtime Orchestration (Framework)
- **WHAT:** Your infrastructure relies on imperative state-checks ("is the MBP awake? Is port 1234 open?"). You are missing **Promise Theory**, which flips the architecture from centralized imperative checks to decentralized nodes publishing autonomous SLAs. An infrastructure component doesn't have a binary "status"; it publishes a "promise" (e.g., "I promise 5/5 needle recall at 30 tok/s"). 
- **WHO/WHAT:** Mark Burgess’s *Promise Theory: Principles and Applications*.
- **WHAT IT UNLOCKS:** **Artifact: A rewritten `hybrid_router.py` using a Promise interface**. Instead of your Python script pinging LM Studio or Ollama to see if they are alive, the MBP and Mac Mini instances write expiring SLA JSONs to a local SQLite table (`vault/.vault-index.db`). The router simply reads the best current promise. This unlocks a highly technical IC PRD on "Promise-Oriented Agent Design," solving the exact race conditions you hit with your `daily-driver` and `meta-agent` cron jobs.

### 3. Feedback Control Loops for Context Throttling (Algorithmic Technique)
- **WHAT:** You are measuring capability bounds via static benchmarking (e.g., "qwen3.6:35b-a3b does 30 tok/s"). You are missing **Dynamic Feedback Control**. When your Mac Mini runs 3 cron jobs at once, thermal throttling destroys that 30 tok/s baseline, pushing your 900s local LDR tasks into hard timeouts. You need a controller that adjusts workload sizes based on the real-time derivative of token latency.
- **WHO/WHAT:** Philipp K. Janert’s *Feedback Control for Computer Systems* (specifically applying PID—Proportional-Integral-Derivative—controllers to software queues).
- **WHAT IT UNLOCKS:** **Artifact: A PID-controller injected into `agents-sdk/agents/vault_synthesizer.py`**. When the derivative of your `tok/s` goes negative (indicating thermal throttling on the M4 Pro), the PID loop automatically reduces the HDBSCAN cluster-and-sample chunk size *before* the 900s timeout is reached. This unlocks an executable demo repository and an accompanying PM one-pager demonstrating how to build self-healing, thermally-aware AI pipelines—a massive signal for a senior AI-PM portfolio.
