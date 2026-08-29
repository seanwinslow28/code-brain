---
title: "How to make `GoodGoodhart Failure Typing` better"
type: expansion
parent: "[[goodgoodhart-failure-typing]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-20
updated: 2026-08-20
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[goodgoodhart-failure-typing]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

### 1. Replace the single failure bucket with the four Goodhart mechanisms

**Add:** A diagnostic matrix distinguishing **regressional, extremal, causal, and adversarial Goodhart**. The current concept labels every proxy failure “corruption,” obscuring different remedies.

**Anchor:** David Manheim and Scott Garrabrant, [“Categorizing Variants of Goodhart’s Law”](https://arxiv.org/abs/1803.04585).

Map Sean’s cases explicitly:

- Novelty score selects noisy false positives → regressional.
- Fleet generates concepts unlike the evaluator’s training distribution → extremal.
- Adding links changes what “connectedness” signifies → causal.
- Agents learn critic-pleasing rhetoric → adversarial.

**Unlock:** An **agent-fleet metric-failure runbook**: observed symptom → Goodhart type → confirming test → intervention. This could also become an intent-engineering MCP command such as `diagnose_proxy_failure`, turning the concept into executable governance rather than another warning essay.

### 2. Add “quantilizer mode” as the missing alternative to maximization

**Add:** **Quantilization**—sample from an acceptable top band instead of repeatedly choosing the highest-scoring output. Policy pattern: “Generate 20 candidates; discard everything below the usefulness threshold; sample among the survivors without exposing their exact ranking to the generator.”

**Anchor:** Jessica Taylor, [*Quantilizers: A Safer Alternative to Maximizers for Limited Optimization*](https://aaai.org/papers/aaaiw-ws0198-16-12613/). Taylor’s central move is limiting optimization pressure when the utility function necessarily omits things humans value.

**Unlock:** An **executable Goodhart demo** using Sean’s own vault: compare “highest novelty score wins” against top-decile sampling, then blind-review depth, surprise, and shipability. It also yields a concrete fleet control: critics may veto weak work, but their scalar scores do not determine the winner. The current article diagnoses optimization pressure without offering a different selection algorithm.

### 3. Treat metrics as world-making interventions, not damaged mirrors

**Add:** **Reactivity through commensuration and self-fulfilling prophecy.** This contradicts the article’s implicit model that metrics first represent quality and are later corrupted. Sometimes measurement creates the category it claims merely to observe: once “connection count” is visible, agents redefine a good concept as a highly linked concept, and Sean may eventually adopt that definition too.

**Anchor:** Wendy Nelson Espeland and Michael Sauder, [“Rankings and Reactivity: How Public Measures Recreate Social Worlds”](https://www.journals.uchicago.edu/doi/10.1086/517897). Their law-school study identifies commensuration and self-fulfilling prophecy as distinct mechanisms by which rankings reorganize behavior and institutional meaning.

**Unlock:** A sharper **Substack essay or portfolio case study**: *Your Agent Dashboard Is Training You*. Pair it with a **metric-reactivity ledger** recording what behavior, vocabulary, and taste changed after each metric became visible. That reaches the human side of fleet governance—how Sean’s evaluative machinery modifies Sean—not just how agents game scores.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
