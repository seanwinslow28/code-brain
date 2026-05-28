---
title: "How to make `Cost-Capped Agentic Workflows` better"
type: expansion
parent: "[[cost-capped-agentic-workflows]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-28
updated: 2026-05-28
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[cost-capped-agentic-workflows]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “shadow price of cognition” mode**

   **What to add:** A budget model that prices not just API dollars, but *attention, queue slots, latency, and opportunity cost*. Right now the concept treats cost as financial scarcity; it misses the more interesting constraint: which questions deserve scarce reasoning cycles.

   **Anchor:** Herbert A. Simon, “Designing Organizations for an Information-Rich World” in *Computers, Communications, and the Public Interest*.

   **Sentence pattern:** “A `$7` research run is cheap if it prevents a week of false work; it is expensive if it consumes the only high-trust synthesis slot on a low-leverage curiosity.”

   **Unlocks:** A **research allocation runbook** for Code-Brain: classify queued topics by expected decision value, reversibility, uncertainty reduction, and artifact potential. This lets Sean decide when to burn Gemini DR Max, when to route to local LDR, and when to delete the question entirely.

2. **Add “real options portfolio” framing**

   **What to add:** Treat each expensive agent run as buying an option, not buying an answer. The missing facet is portfolio management: small cheap probes preserve optionality; expensive synthesis should be reserved for decisions where exercising the option changes the next build, essay, job pitch, or architecture choice.

   **Anchor:** Carliss Y. Baldwin and Kim B. Clark, *Design Rules, Volume 1: The Power of Modularity*.

   **Sentence pattern:** “The cheapest run is not the one with the lowest price; it is the one that preserves the most valuable future choices per dollar.”

   **Unlocks:** A **portfolio one-pager** for Sean’s agentic-engineering job hunt: “How I Manage Autonomous Research as a Bounded Options Portfolio.” That would turn a private budget hack into a senior-PM/IC signal about ambiguity, sequencing, and capital allocation.

3. **Add “graceful degradation ladder” from reliability engineering**

   **What to add:** A named failure-mode ladder for what the fleet should do as budget headroom collapses: full deep research → scoped synthesis → citation-only scan → local hypothesis generation → queue deferral → explicit refusal. The current concept says caps gate capability, but not how output quality degrades predictably.

   **Anchor:** Richard I. Cook, “How Complex Systems Fail.”

   **Sentence pattern:** “A cost cap is not a stop sign; it is a controlled degradation protocol that keeps the system honest about what kind of answer it is producing.”

   **Unlocks:** An **agent spec / evaluator** for `gemini_dr.py` and the vault critic: every research artifact declares its budget tier, confidence class, citation burden, and allowed downstream use. This would prevent cheap local outputs from being mistaken for DR-grade conclusions, which is the current concept’s biggest operational blind spot.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
