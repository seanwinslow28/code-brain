---
title: "How to make `Research Workflow Integration` better"
type: expansion
parent: "[[research-workflow-integration]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-14
updated: 2026-08-14
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-workflow-integration]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add a Knowledge-to-Action state machine

- **What to add:** Replace “research is formalized and surfaced” with explicit states: `identified → adapted to context → barriers assessed → action selected → monitored → evaluated → sustained/retired`. Require every research output to name an owner, target behavior, success signal, and expiry condition.
- **Anchor:** Ian Graham et al., [“Lost in Knowledge Translation: Time for a Map?”](https://eshop.werpn.com/wp-content/uploads/2021/12/Journal-of-Continuing-Education-in-the-Health-Professions-2006-Graham-Lost-in-knowledge-translation-Time-for-a-map.pdf), which introduced the Knowledge-to-Action cycle. Its useful contradiction: making knowledge retrievable is not the same as putting it into practice.
- **Unlock:** An executable **research-integration agent spec and runbook**. Sentence pattern: “Because evidence E changes assumption A, modify artifact/system B by date D; observe metric M; revert or retire if condition R occurs.” The current concept can describe ingestion, but cannot determine whether research changed anything.

## 2. Add Pirolli and Card’s foraging–sensemaking loop

- **What to add:** Model integration as two coupled loops: a **foraging loop** that searches, filters, and extracts evidence into a “shoebox,” and a **sensemaking loop** that builds schemas, hypotheses, and an evidence-supported story. Store intermediate objects—not only finished notes: source snippets, competing hypotheses, disconfirming evidence, and the schema each finding modifies.
- **Anchor:** Peter Pirolli and Stuart Card, [“The Sensemaking Process and Leverage Points for Analyst Technology”](https://andymatuschak.org/files/papers/Pirolli%2C%20Card%20-%202005%20-%20The%20sensemaking%20process%20and%20leverage%20points%20for%20analyst%20technology%20as.pdf).
- **Unlock:** A compelling **portfolio demo**: select a decision, inspect its evidence shoebox, watch competing explanations form, then trace the winning hypothesis into an implementation artifact. This is substantially stronger than “call `find_contradictions` and receive vault matches” because it demonstrates machine-assisted reasoning provenance rather than retrieval.

## 3. Add double-loop learning and assumption invalidation

- **What to add:** Classify every research consequence as either **single-loop**—change execution while preserving the objective—or **double-loop**—challenge the objective, policy, metric, or governing assumption itself. Give each important decision an `assumption`, `disconfirming_signal`, and `replacement_rule`.
- **Anchor:** Chris Argyris, [“Double Loop Learning in Organizations”](https://hbr.org/1977/09/double-loop-learning-in-organizations). Argyris’s core challenge is that systems frequently correct errors without questioning the policies that produced them.
- **Unlock:** A **decision-reversal ledger**, ADR extension, or critic-agent mode that says: “This evidence does not suggest improving route X; it invalidates the reason route X exists.” That would let Sean publish a sharp Substack essay—*Your Second Brain Is Probably a Single-Loop Bureaucracy*—and demonstrate a fleet that can revise its governing intent, not merely enrich its existing worldview.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
