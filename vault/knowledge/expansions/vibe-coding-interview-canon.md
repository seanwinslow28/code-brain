---
title: "How to make `Vibe-Coding Interview Canon` better"
type: expansion
parent: "[[vibe-coding-interview-canon]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[vibe-coding-interview-canon]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Costly Signal Packet” mode**
   - **What to add:** A hiring/interview frame that treats every claim as a signal requiring costly proof, not vocabulary fluency. Pattern: “I claim X; here is the artifact that would have been expensive to fake; here is what it proves.”
   - **Exemplar:** Michael Spence, “Job Market Signaling” (1973), plus Patrick McKenzie, “Don’t Call Yourself A Programmer.”
   - **Unlocks:** A portfolio one-pager or interview leave-behind for Code-Brain: “7-agent local knowledge loop, $0/run, launchd, manifests, failure modes, eval gates.” This prevents the current concept from becoming an interview study guide that sounds competent but unverifiable.

2. **Add “Eval-First Demo Canon”**
   - **What to add:** A rule that every vibe-coding interview prep topic must map to an eval artifact: fixture, rubric, trace, failure taxonomy, before/after score. Pattern: “The agent is good if it passes CASES; it fails when FAILURE MODE; the judge checks SIGNAL.”
   - **Exemplar:** Hamel Husain, “Your AI Product Needs Evals”; OpenAI `evals` repo as the concrete artifact model.
   - **Unlocks:** An executable interview demo, not just prep notes: a tiny agent task with 10 fixtures, a scoring rubric, and a regression report. This lets Sean answer “How do you know it works?” with a shipped harness instead of agentic-engineering rhetoric.

3. **Add “Incident Narrative Interview Mode”**
   - **What to add:** A storytelling pattern for agent failures: normal work, weak signal, compounding condition, intervention, new guardrail. Pattern: “This did not fail because the model was dumb; it failed because the system made the wrong thing easy.”
   - **Exemplar:** Richard Cook, “How Complex Systems Fail”; John Allspaw, “The Infinite Hows.”
   - **Unlocks:** A Substack essay, interview answer bank, and runbook genre Sean currently cannot reach from “vocabulary mastery.” It turns vault conflicts, fabricated citations, launchd path failures, and dual auto-commit systems into senior-level systems judgment instead of anecdotes.

## From Anti-Gravity (Gemini 3)

### 1. Empirical Vibe Distillation (Eval-Driven Engineering)
- **WHAT to add:** The explicit transition from subjective "vibe-coding" to deterministic evaluation. The interview canon currently frames vibe-coding as a performance of fluency (vocabulary, practice). It needs the mechanics of how to instantly scaffold an LLM-as-a-judge eval to prove the vibe-coded output actually works. 
- **WHO/WHAT exemplifies it:** Hamel Husain’s essay *"Creating a LLM-as-a-Judge That Drives Business Value"* (and his broader Eval-Driven Development methodology).
- **WHAT this unlocks:** Transforms Sean's interview artifact from a "look at this app I prompted" demo into an **executable `evals.py` test suite** written live. It proves to engineering managers that he treats LLM output with deep skepticism, unlocking the "Senior IC" trust signal that pure generative fluency lacks.

### 2. The "Squishy" State Boundary (Malleable Systems)
- **WHAT to add:** A framework for explicitly defining the boundary where generative "vibe-coding" ends and deterministic state must take over. AI-PM candidates often fail system-design interviews by treating the entire application as a prompt, rather than isolating the non-deterministic components.
- **WHO/WHAT exemplifies it:** Geoffrey Litt’s essay *"Squishy Interfaces"* (and his work on malleable software at Ink & Switch).
- **WHAT this unlocks:** Unlocks the ability to write a high-fidelity **Agentic-UX Architectural Decision Record (ADR)** during a whiteboard session. Sean can use this to draw explicit boundaries (e.g., "The Phaser sprite generator is squishy; the Pixel Quantizer palette enforcement is deterministic"), proving he understands the product trade-offs of when *not* to use AI.

### 3. Workflow-over-Agent Fallback (Graceful Degradation)
- **WHAT to add:** A vocabulary for "glass-box" traceability and hard fallbacks when the vibe-coding loop hallucinates or times out (like your 900s local LDR limit). The canon focuses on preparation and confidence, but it is missing the systemic handling of inevitable failure states.
- **WHO/WHAT exemplifies it:** Anthropic’s applied AI research paper *"Building Effective Agents"* (specifically their definitions of the rigid "Workflow" vs. autonomous "Agent" trade-off, and when to enforce the former).
- **WHAT this unlocks:** Lets Sean produce a **"Degradation Runbook" or Fallback Spec** artifact. Instead of just talking about successful intent-engineering, he can hand an interviewer a spec detailing how his multi-agent system gracefully degrades into a hard-coded workflow when local model confidence drops. This shifts his positioning from "AI enthusiast" to "hardened production PM."
