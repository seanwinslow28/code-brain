---
title: "How to make `Open-Source Contributions to Agentic Research` better"
type: expansion
parent: "[[open-source-contributions-to-agentic-research]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-15
updated: 2026-06-15
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[open-source-contributions-to-agentic-research]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “adversarial retrieval evaluation,” anchored on Lin et al., _TruthfulQA_ and OpenAI’s _WebGPT_ paper.**  
   The concept currently treats open-source + LDR as a resilience story: if local systems run, research continues. Missing is the failure mode where the system confidently retrieves, ranks, and cites the wrong thing. Add a section: **“Research agents need adversarial evals, not just queues.”**  
   Sentence pattern: “For every queued research task, define the false-but-plausible answer the agent is likely to produce, then test whether retrieval resists it.”  
   This unlocks an **eval artifact**: a `deep-researcher-adversarial-suite.md` or pytest fixture set with known traps, citation-quality checks, and “fabricated source” regression cases. Right now the concept cannot produce a defensible claim that LDR is reliable; it only says the pipeline exists.

2. **Add “epistemic status labels,” anchored on Gwern Branwen’s essay practice and Julia Galef’s _The Scout Mindset_.**  
   The article collapses queue, model, source, and conclusion into one flat synthesis. It needs a visible distinction between **found**, **inferred**, **suspected**, **actionable**, and **not-yet-trusted**. Gwern’s longform habit of explicit epistemic status and Galef’s scout/soldier framing give Sean a language for research agents that do not merely summarize but disclose confidence.  
   Sentence pattern: “This conclusion is usable for X, but not yet usable for Y, because the evidence is only source-type Z.”  
   This unlocks a **research brief genre**: not “here is what LDR found,” but “here is what the fleet is willing to bet on.” Sean could ship a Substack essay or portfolio case study on **local-agent epistemology**, which is much stronger than another architecture summary.

3. **Add “human provenance and maintenance contract,” anchored on Nadia Eghbal’s _Working in Public_ and Karl Fogel’s _Producing Open Source Software_.**  
   “Open-source contributions” is currently treated as model availability: Qwen, Ollama, SearXNG, free model endpoints. That misses the actual open-source problem: maintainers, governance, bus factor, issue velocity, release discipline, and whether a dependency is socially alive. Eghbal and Fogel would force the concept to evaluate open source as an institution, not just a parts bin.  
   Sentence pattern: “Before routing critical agent work through an open component, score not just capability but maintainer health: release cadence, issue response, governance clarity, and exit path.”  
   This unlocks a **dependency due-diligence runbook** for agent fleets: a checklist Sean could apply before adopting Qwen variants, LDR forks, SearXNG instances, or MCP libraries. The current concept can recommend tools; this addition lets him make adoption decisions like an engineering IC.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
