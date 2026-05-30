---
title: "How to make `Real-Time Problem Solving` better"
type: expansion
parent: "[[real-time-problem-solving]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-30
updated: 2026-05-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[real-time-problem-solving]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “debugging as performance” anchored on Brian Kernighan & Rob Pike, _The Practice of Programming_, Chapter 5: Debugging.**  
   Current concept says “debugging on-the-fly,” but misses the interview-specific skill: making the invisible search process legible without narrating every keystroke. Add a mode where Sean explicitly cycles: **observe symptom → state invariant → form one hypothesis → run smallest test → update belief**.  
   Sentence pattern: “If this invariant holds, then X should be true; I’m going to test that before changing code.”  
   **Unlocks:** a live-coding interview runbook and demo script where Sean shows agentic-engineering maturity through disciplined diagnosis, not just fast implementation. It also gives his agents a critique rubric for whether an interview answer demonstrated causal debugging or merely “vibe-fixed” the issue.

2. **Add “thinking aloud without bleeding confidence” anchored on Donald Schön, _The Reflective Practitioner_, especially “reflection-in-action.”**  
   The concept treats transparency as explanation, but in interviews the stronger move is controlled reflection: revealing uncertainty while preserving leadership. Schön’s frame gives Sean a better distinction: **not “I don’t know,” but “I’m reframing the problem while acting inside it.”**  
   Sentence pattern: “I’m noticing this solution is optimizing for local simplicity, but the system constraint is probably elsewhere, so I’m going to reframe before coding further.”  
   **Unlocks:** a Substack essay or portfolio one-pager on “reflection-in-action for AI-native PMs,” where Sean can position himself as someone who can work in ambiguity without sounding junior, scattered, or over-explanatory.

3. **Add “pairing protocol” anchored on Llewellyn Falco & Maaret Pyhäjärvi’s strong-style pairing work, especially the maxim: “For an idea to go from your head into the computer, it must go through someone else’s hands.”**  
   Real-time problem solving is not just solo cognition with narration. Vibe-coding interviews increasingly resemble human-agent pair programming: the candidate must direct, critique, accept, reject, and reshape generated code. Add a facet for **driver/navigator control transfer**: when Sean codes, when the agent codes, when he pauses generation, and how he audits the output.  
   Sentence pattern: “I’ll let the agent draft the boring path, but I’m reserving human attention for the boundary condition and the interface contract.”  
   **Unlocks:** an executable interview demo or agent spec for “AI pair-programming under interview pressure,” showing Sean can manage an agent as a collaborator rather than use it as autocomplete. This directly upgrades the concept from generic “think and code live” to a differentiated agentic-engineering signal.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
