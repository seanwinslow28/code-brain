---
title: "How to make `Deep Research System Constraints` better"
type: expansion
parent: "[[deep-research-system-constraints]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-13
updated: 2026-06-13
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[deep-research-system-constraints]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Cynefin routing,” not just simple/compound routing.**  
   Anchor it on Dave Snowden & Mary Boone, **“A Leader’s Framework for Decision Making”** (*Harvard Business Review*, 2007).  
   Current concept routes by prompt size and timeout risk: simple → LDR, compound → Gemini DR. That misses the more useful distinction: **clear / complicated / complex / chaotic**.  
   Sentence pattern to add: “Route research by epistemic domain: clear questions need retrieval; complicated questions need expert decomposition; complex questions need probes and competing interpretations; chaotic questions need containment first.”  
   This unlocks a **research intake classifier / agent spec** where Sean can decide whether a question should become a queue item, Gemini DR run, LLM Council critique, experiment, or manual decision memo.

2. **Add “sensemaking loop” as the missing middle between research input and report output.**  
   Anchor it on Peter Pirolli & Stuart Card, **“The Sensemaking Process and Leverage Points for Analyst Technology”** (PARC, 2005).  
   The concept currently treats deep research as a batch pipeline: question in, report out. Pirolli/Card gives Sean the canonical loop his agents are missing: **forage → collect evidence → build schema → reframe → search again → present**.  
   Sentence pattern to add: “A research agent should not merely answer the queued question; it should maintain a working frame, detect when evidence changes the frame, and emit the frame shift as a first-class artifact.”  
   This unlocks a **research trace format** or **vault report template** that captures why the agent changed direction, not just what it found. That would make the critic generative instead of descriptive because it can attack the frame, not only the summary.

3. **Add “premortem / reference-class gate” before escalating to Gemini DR.**  
   Anchor it on Gary Klein, **“Performing a Project Premortem”** (*Harvard Business Review*, 2007), paired with Daniel Kahneman & Amos Tversky’s **“Intuitive Prediction: Biases and Corrective Procedures”** (1979) for the outside-view logic.  
   Right now escalation is operational: LDR times out, citations collapse, so Gemini DR gets the compound work. Missing is a judgment gate: “What kind of failure has this class of research produced before?”  
   Sentence pattern to add: “Before running expensive research, write a 5-line premortem: likely failure mode, nearest prior bad output, citation-risk class, decision at stake, cheapest disconfirming probe.”  
   This unlocks a **Deep Research Runbook** and **cost/quality decision record**. Sean could show employers a concrete agentic-engineering artifact: not “I use Gemini for hard research,” but “I built escalation governance that predicts when local research will hallucinate, stall, or produce unusable synthesis.”

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
