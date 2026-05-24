---
title: "How to make `Agentic Engineering` better"
type: expansion
parent: "[[agentic-engineering]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[agentic-engineering]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “joint activity coordination” as the missing operating theory**

   Anchor it on Gary Klein, Paul Feltovich, Jeffrey Bradshaw, and David Woods, **“Common Ground and Coordination in Joint Activity”**.

   Current concept says “agents own decomposition; human owns judgment,” but it does not explain how human and agent stay mutually calibrated while work unfolds. Add a facet for **common ground maintenance**: what the agent must surface, what the human must confirm, when assumptions expire, and how coordination breakdowns are repaired.

   Sentence pattern to add: “Agentic engineering is not delegation to tools; it is the design of joint activity, where the main artifact is the shared state that lets human and agent predict each other’s next move.”

   This unlocks a **fleet coordination runbook** or **agent spec template** Sean cannot currently produce: one with explicit handoff contracts, assumption registers, stale-context alarms, and repair protocols. It also gives him interview language beyond “I built agents” toward “I design coordination systems.”

2. **Add “adaptive automation failure modes” as the contradiction**

   Anchor it on Lisanne Bainbridge, **“Ironies of Automation”**.

   Sean’s concept currently risks sounding like a confident acceleration thesis: agents decompose, humans supervise. Bainbridge gives the uncomfortable counterpoint: the more capable automation becomes, the more humans are pushed into rare, high-stakes oversight moments where their skill, context, and attention may have degraded.

   Add a named critique: **the oversight paradox**. Human judgment is not automatically preserved by keeping a person “in the loop”; it has to be trained, rehearsed, and instrumented.

   Sentence pattern to add: “The failure mode of agentic engineering is not that agents do too little; it is that they do enough to make the human’s remaining intervention harder, rarer, and more brittle.”

   This unlocks a **Substack essay** with teeth: “The Irony of Agentic Engineering.” It also unlocks a practical **pre-mortem checklist** for Code-Brain agents: what skills atrophy, what decisions become invisible, what alerting creates false confidence, and where Sean should deliberately keep manual reps.

3. **Add “cognitive apprenticeship for agents” as the portfolio bridge**

   Anchor it on Allan Collins, John Seely Brown, and Susan Newman, **“Cognitive Apprenticeship: Teaching the Crafts of Reading, Writing, and Mathematics.”**

   The concept says agents own decomposition, but it does not yet explain how agents get better at Sean’s taste, judgment, and craft. Cognitive apprenticeship gives him a stronger frame: modeling, coaching, scaffolding, articulation, reflection, exploration. That maps cleanly onto his skills, hooks, critic loops, and voice modes.

   Add a mode called **agent apprenticeship**: agents should not merely execute tasks; they should be trained through exposed reasoning traces, critique rituals, fading scaffolds, and comparison against expert examples.

   Sentence pattern to add: “Agentic engineering treats the agent fleet less like software automation and more like apprentices: first shown the craft, then coached through it, then trusted only where the scaffolding has proven removable.”

   This unlocks a **portfolio one-pager** that connects PM and IC credibility: “How I train agents like junior collaborators.” It also gives Sean a concrete artifact to ship: an **apprenticeship ladder for agents**, showing novice/intermediate/senior behaviors, eval gates, critique prompts, and promotion criteria.

## From Anti-Gravity (Gemini 3)

### 1. Flow Engineering (Contradicting "Agents own decomposition")
*   **WHAT to add:** Flow Engineering. Your concept assumes agents *should* own decomposition. Flow Engineering explicitly contradicts this, arguing that LLMs are currently poor at autonomous zero-shot decomposition but excel at executing rigidly defined, iterative, human-designed state machines with explicit test-and-repair loops.
*   **WHO/WHAT exemplifies it:** *AlphaCodium: From Prompt Engineering to Flow Engineering* by Tal Ridnik et al. (2024).
*   **WHAT this unlocks:** A **Deterministic Flow Spec**. Instead of writing standard PM PRDs that hand off ambiguous goals to an agent, you can ship executable state-machine blueprints (e.g., LangGraph nodes). For an AI-PM portfolio, this shifts your output from "I prompt agents well" to "I engineer reliable, production-ready AI pipelines that prevent hallucination."

### 2. LLM Cascading (Formalizing your `HybridRouter`)
*   **WHAT to add:** Formal LLM Cascading. You have an intuitive multi-tier router (Mac Mini `gemma4:e4b` → MBP `qwen3` → API) and cost caps. You are missing the formal algorithmic framework for scoring query complexity upstream and dynamically routing it based on a mathematically optimal cost/latency tradeoff, rather than relying on failure-based fallback chains.
*   **WHO/WHAT exemplifies it:** *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance* by Lingjiao Chen et al. (2023).
*   **WHAT this unlocks:** An **Enterprise Routing Architecture RFC / Standalone SDK Module**. You can extract your `hybrid_router.py` and rewrite it using formal cascade methodologies. Shipping this as a rigorously documented IC artifact proves to hiring managers you can operationalize local vs. cloud unit economics at an enterprise scale.

### 3. Bootstrapped Reasoning (Automating "Human owns judgment")
*   **WHAT to add:** Rationalization Capture. You treat "human owns judgment" as a terminal boundary. It shouldn't be. Every time you override a subagent, deny a hook (Exit Code 2), or reject a `vault_synthesizer` pass, you generate a preference signal. The missing facet is closing the loop to shift the judgment boundary over time.
*   **WHO/WHAT exemplifies it:** *STaR: Bootstrapping Reasoning With Reasoning* by Eric Zelikman et al. (2022).
*   **WHAT this unlocks:** A **CLI-History LoRA Data Flywheel**. You already train LoRAs for 16BitFit sprites. This framework lets you ship a Python script that parses your Claude CLI traces (`history.jsonl` + hook exit codes), transforms them into a DPO (Direct Preference Optimization) dataset, and fine-tunes your local `qwen3-14b` orchestrator. This yields an executable demo: a local model continuously trained on your own IC/PM judgment exhaust.
