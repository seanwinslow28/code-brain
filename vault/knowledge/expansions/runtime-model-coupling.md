---
title: "How to make `Runtime-Model Coupling` better"
type: expansion
parent: "[[runtime-model-coupling]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-27
updated: 2026-05-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[runtime-model-coupling]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Sampling Contract” as a first-class facet.**  
   Anchor it on Holtzman et al., **“The Curious Case of Neural Text Degeneration”** and OpenAI’s **Structured Outputs / constrained decoding** work.

   Current concept says runtime config changes capability, but it under-specifies the sampling layer: temperature, top-p, repetition penalties, grammar constraints, JSON mode, tool-call decoding, seed behavior, and stop sequences. Add a section that treats every agent task as having a **sampling contract**:

   `model weights + runtime + prompt + sampler + decoder constraint + schema validator = actual capability`

   This unlocks a **fleet runbook / eval harness artifact**: a matrix where each scheduled agent has an approved sampling contract, not just an approved model. Sean could ship a “schema-critical local model certification” demo that proves why `qwen3.6:35b-a3b on Ollama think:false` is not interchangeable with the same model under another runtime.

2. **Add “Capability Is an Interaction Effect,” not a model property.**  
   Anchor it on Gary Klein, **Sources of Power**, especially the Recognition-Primed Decision model, plus Woods & Hollnagel, **Joint Cognitive Systems: Foundations of Cognitive Systems Engineering**.

   The missing contradiction: this concept still treats the runtime as a technical gate on model capability. Cognitive systems engineering would say the real unit of analysis is the **joint system**: Sean + launchd + runtime + schema validator + retry policy + artifact consumer + downstream agent. A model “failing JSON” is not merely a model/runtime defect; it is a coordination failure in the larger control loop.

   Add a paragraph with this sentence pattern:

   `The question is not “Can model X do task Y?” but “Under which joint-system conditions does model X remain a trustworthy component in workflow Z?”`

   This unlocks a stronger **agent-ops decision record** genre. Instead of “Ollama beat LM Studio for this model,” Sean can write ADRs that justify routing, fallback, HITL escalation, and disablement thresholds as system-design choices.

3. **Add “Portability Tax” as the economic frame.**  
   Anchor it on Martin Fowler’s essay **“Semantic Diffusion”** and Hyrum Wright’s **“Hyrum’s Law”**.

   Sean has the technical observation, but not the maintenance-cost implication: once a fleet quietly depends on runtime quirks like `think:false`, prompt formatting, hidden tokenizer behavior, or JSON repair tolerance, the system has accumulated a **portability tax**. Any runtime swap becomes a migration, not an implementation detail.

   Add a section called **Portability Tax**:

   `Every runtime-specific success condition becomes an undocumented API. If enough downstream agents depend on it, the runtime is no longer replaceable without regression testing.`

   This unlocks a **portfolio one-pager / Substack essay** with a sharper outside-view hook: “Local models are not portable until their runtime contracts are tested.” That is more legible to AI-PM and agentic-engineering hiring readers than “I benchmarked Ollama vs LM Studio,” because it reframes the work as product-risk management for autonomous systems.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
