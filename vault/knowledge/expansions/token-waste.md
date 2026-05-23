---
title: "How to make `Token Waste` better"
type: expansion
parent: "[[token-waste]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-23
updated: 2026-05-23
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[token-waste]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “token ledger mode” anchored on Anthropic’s `Prompt Caching` docs.**  
   - **What to add:** A concrete accounting pattern: `static prefix -> cacheable`, `retrieved context -> scoped`, `task state -> fresh`, `output -> uncached`. Sentence pattern: “This workflow wastes tokens when durable context is resent as fresh context instead of being promoted into a cached prefix or retrieved shard.”
   - **Exemplar:** Anthropic, [“Prompt caching”](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching), especially `cache_creation_input_tokens` and `cache_read_input_tokens`.
   - **Unlocks:** A new artifact Sean cannot currently produce: an **agent fleet token bill of materials**. Instead of saying “agents burn too many tokens,” he can decide: cache, retrieve, compress, delete, or split. This turns the concept from complaint into infrastructure design.

2. **Add “attention waste” anchored on Nelson F. Liu et al., `Lost in the Middle`.**  
   - **What to add:** The missing facet that tokens can be wasted even when they are relevant. Long-context loading fails when useful evidence is buried where the model underuses it. Sentence pattern: “Token waste is not only excess context; it is paid-for context that lands outside the model’s effective attention path.”
   - **Exemplar:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang, [“Lost in the Middle: How Language Models Use Long Contexts”](https://arxiv.org/abs/2307.03172).
   - **Unlocks:** A **context-packing critique** for Sean’s vault agents: which docs deserve top/bottom placement, which should be chunked, which should be queried, and which should never enter the prompt. This lets him produce retrieval evals and context-layout rules, not just cost summaries.

3. **Add “Jevons mode” anchored on William Stanley Jevons’s `The Coal Question`.**  
   - **What to add:** A contradicting framework: efficiency gains may increase total usage. Cheaper tokens can lead Sean to run more agents, bigger searches, and more speculative workflows. Sentence pattern: “The goal is not lower token spend; the goal is higher creative yield per token under explicit reinvestment rules.”
   - **Exemplar:** William Stanley Jevons, [*The Coal Question*](https://energyhistory.yale.edu/w-stanley-jevons-the-coal-question-1865/), the classic source of Jevons’ paradox.
   - **Unlocks:** A **token reinvestment policy**: saved tokens get routed into higher-value genres such as creative-studio exploration, job-hunt market maps, or Superuser Pack regression tests. This prevents the article from sounding like generic austerity and reframes optimization as capacity creation.

## From Anti-Gravity (Gemini 3)

**1. Semantic Prompt Compression**
- **WHAT to add:** Add "Compression/Density Tactics" to reframe token waste. Your current concept treats token waste as a pipeline problem (how data is loaded); it completely misses the information density of the tokens themselves.
- **WHO exemplifies it:** Microsoft Research (Huiqiang Jiang et al.) in the paper *"LLMLingua: Compressing Prompts for Accelerated Inference of Large Language Models"*.
- **WHAT this unlocks:** Unlocks the **Micro-Agent Orchestration script** genre. Instead of passing verbose instructions and raw text between agents, this lets you build pipelines that pass mathematically compressed state representations. It moves you past the generic failure mode of building "fat god-prompts" that bloat your budget to run simple cross-domain tasks.

**2. Tiered Memory Architecture**
- **WHAT to add:** Add "Context Paging" to address temporal token waste. The concept mentions "non-cached system prompts," but ignores how token costs compound exponentially simply because conversational history is blindly appended over time.
- **WHO exemplifies it:** Charles Packer et al. in the paper *"MemGPT: Towards LLMs as Operating Systems"*.
- **WHAT this unlocks:** Unlocks the **Persistent Daily-Drive Agent** genre. This allows you to build agents that actively summarize, prune, and page out their own memory to vector stores or flat files. It solves the generic failure mode where your continuous agents "hit a context wall, become too expensive to run, and are forced to restart."

**3. Prefix-Caching Structural Economics**
- **WHAT to add:** Add "Static Prefix Design." Your concept frames caching as a passive cost-saver, missing that it dictates strict architectural rules: token waste is often an *ordering* problem where dynamic variables injected too early break the cache block. 
- **WHO exemplifies it:** Anthropic's official API Documentation on *"Prompt Caching"*, specifically the architectural mandate for immutable block ordering.
- **WHAT this unlocks:** Unlocks the **Mega-Context Tooling** genre. By strictly isolating dynamic inputs to the absolute end of your prompts, you can inject the entirety of your Superuser Pack or Confluence specs into every single agent turn for fractions of a cent. This permanently eliminates the generic failure mode of "budget-driven trade-offs restricting AI exploration."
