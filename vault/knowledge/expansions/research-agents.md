---
title: "How to make `Research Agents` better"
type: expansion
parent: "[[research-agents]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-28
updated: 2026-05-28
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[research-agents]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “research triage as a queueing discipline,” anchored on Donald Knuth’s _The Art of Computer Programming, Vol. 1_, section 2.2.1, and John D. C. Little’s 1961 paper “A Proof for the Queuing Formula: L = λW.”**

   The concept currently says research agents “manage queues,” but it lacks a theory of backlog pressure. Add a facet that treats research as a constrained service system: arrival rate, service time, timeout budget, retry cost, citation-quality degradation, and abandonment thresholds.

   Sentence pattern: “A research agent is not a smart searcher; it is a queue governor deciding which questions deserve scarce attention before staleness, cost, or citation risk makes them no longer worth answering.”

   This unlocks a **research-operations runbook**: routing rules for LDR vs Gemini DR vs manual review, SLA classes for research prompts, and a dashboard artifact showing queue age, model lane, failure mode, and escalation rule. Right now the concept cannot produce operational policy beyond “send big things to Gemini.”

2. **Add “negative capability / epistemic restraint mode,” anchored on John Keats’s 1817 letter to George and Thomas Keats and Tetlock & Gardner’s _Superforecasting_.**

   Sean’s current concept assumes the research agent’s job is distribution and execution. Missing: the agent sometimes should preserve uncertainty rather than collapse it into a summary. Research agents need a “do not synthesize yet” state when evidence is thin, contradictory, or overfit to one retrieval path.

   Sentence pattern: “A good research agent can hold a question open without laundering uncertainty into prose.”

   This unlocks a **contradiction ledger** or **forecast-grade research note**: claims tagged as known / plausible / disputed / unknown, with confidence deltas after each source pass. It would let Sean ship a Substack essay or portfolio case study on “research agents that know when not to answer,” which is much sharper than another agent-routing description.

3. **Add “bibliographic control and provenance-first research,” anchored on Thomas S. Kuhn’s _The Structure of Scientific Revolutions_ plus Vannevar Bush’s 1945 essay “As We May Think.”**

   The concept names research systems but not the knowledge-graph problem underneath them: how a research agent decides whether a finding is a new claim, a duplicate, a paradigm conflict, or a bridge between concepts. Bush gives the associative-trail frame; Kuhn gives the paradigm-conflict frame.

   Sentence pattern: “Research agents should not merely fetch answers; they should maintain the trail by which an answer became thinkable.”

   This unlocks an **agent spec for provenance-aware synthesis**: every research output must emit source lineage, concept-edge proposals, contradiction candidates, and “trailheads” for future investigation. Sean could turn this into a portfolio one-pager for Code-Brain: not “I built nightly research agents,” but “I built a research memory system that detects when new evidence changes the structure of the vault.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
