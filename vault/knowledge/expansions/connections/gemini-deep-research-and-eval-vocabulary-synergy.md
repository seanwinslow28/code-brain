---
title: "How to make `Gemini Deep Research and Eval Vocabulary Synergy` better"
type: expansion
parent: "[[gemini-deep-research-and-eval-vocabulary-synergy]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-07-03
updated: 2026-07-03
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[gemini-deep-research-and-eval-vocabulary-synergy]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “research triage vocabulary” anchored on Carol Weiss’s _Evaluation Research: Methods for Assessing Program Effectiveness_**

   Current concept says Gemini DR “enriches” eval vocabulary, but it does not distinguish research outputs by decision use. Add Weiss’s modes: research for **instrumental use**, **conceptual use**, and **enlightenment**.

   Pattern to add: “This research output is not valuable because it is deep; it is valuable because it changes one of three things: a decision, a frame, or the background assumptions.”

   This unlocks a **research intake rubric** for the fleet: every Gemini DR artifact must declare whether it supports a go/no-go decision, expands vocabulary, or changes the operating model. Without this, Sean’s agents keep summarizing research as “insights” instead of routing it into decisions.

2. **Add “evals as contract tests” anchored on Hamel Husain’s _Your AI Product Needs Evals_**

   The concept links Gemini Deep Research to Eval Vocabulary, but misses the operational move: eval vocabulary should not just name quality dimensions; it should become executable regression pressure. Hamel’s practical eval framing is useful because it treats evals as product infrastructure, not academic measurement.

   Pattern to add: “If a research note creates a new quality word, it must also create one failing example, one passing example, and one scorer instruction.”

   This unlocks an **eval-pack artifact**: for each new concept, Sean can ship a tiny benchmark with fixtures, expected judgments, and failure modes. That is stronger portfolio signal than “I researched agent evaluation,” because it shows he can turn vocabulary into machinery.

3. **Add “citation laundering failure mode” anchored on Harry Frankfurt’s _On Bullshit_ plus Metaculus-style track records from Philip Tetlock’s _Superforecasting_**

   Gemini DR creates a special risk: research outputs can feel authoritative because they contain citations, but citation density is not epistemic quality. The current concept treats “deep, real-time insights” as additive. The missing contradiction is that research tools can launder weak claims into polished confidence.

   Pattern to add: “A cited claim is not trusted until it survives source inspection, prediction exposure, or downstream falsification.”

   This unlocks a **research trust ledger**: each Gemini DR output gets claims classified as verified, plausible, unsupported, or decision-critical. Pair that with a lightweight forecast: “If this claim is true, what would we expect to observe in 30 days?” This would let Sean produce a Substack essay or agent spec on **anti-bullshit research loops**, where the fleet is judged by calibration rather than volume.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
