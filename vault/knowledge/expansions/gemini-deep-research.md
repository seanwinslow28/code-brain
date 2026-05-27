---
title: "How to make `Gemini Deep Research` better"
type: expansion
parent: "[[gemini-deep-research]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-27
updated: 2026-05-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[gemini-deep-research]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “progressive disclosure research mode” anchored on Bret Victor’s essay _Explorable Explanations_.**

   The current concept treats Gemini DR as a report generator: compound question in, cited synthesis out. Missing is the interaction pattern where research output becomes something the reader can *manipulate*, not merely read.

   Add a facet like: “For high-variance topics, Gemini DR should not only return conclusions; it should return adjustable assumptions, comparison axes, and decision levers.”

   **Exemplar:** Bret Victor, [_Explorable Explanations_](https://worrydream.com/ExplorableExplanations/).

   **Unlocks:** an executable research artifact: “Deep Research as decision surface.” For Sean, this could become a Substack/demo pair where a Gemini DR report is transformed into an interactive due-diligence matrix: sliders for risk tolerance, cost, confidence, timeline, reversibility. Current concept can produce a report; this addition lets him ship a research UI or agent spec that turns citations into steering controls.

2. **Add “intelligence tasking doctrine” anchored on Richards J. Heuer Jr.’s _Psychology of Intelligence Analysis_.**

   The concept says Gemini DR handles “complex, multi-step research,” but it lacks a doctrine for *when research is epistemically dangerous*. Compound research does not just need more horsepower; it needs anti-bias structure.

   Add a mode like: “Before Gemini DR runs, classify whether the task requires evidence collection, hypothesis competition, adversarial disconfirmation, or estimate calibration.”

   **Exemplar:** Richards J. Heuer Jr., _Psychology of Intelligence Analysis_, especially the Analysis of Competing Hypotheses method.

   **Unlocks:** a research runbook and agent-routing spec. Sean could produce a “Gemini DR Tasking Manual” with templates like: “ACH run,” “due diligence run,” “market map run,” “canonical reference excavation,” and “red-team contradiction run.” Current concept says “send hard stuff to Gemini”; this would define *what kind of hard* and which reasoning scaffold belongs around it.

3. **Add “report-to-claim graph conversion” anchored on Andy Matuschak’s _Evergreen Notes_ practice.**

   This article stops at Gemini DR as a cloud tier. It does not specify how a long report becomes durable knowledge in Code-Brain. Sean’s vault problem is not only research quality; it is converting cited reports into atomic, reusable claims that later agents can critique, connect, and contradict.

   Add a post-processing mode: “Every Gemini DR output must be decomposed into claim nodes, evidence nodes, contradiction candidates, and open questions before entering the vault.”

   **Exemplar:** Andy Matuschak, [_Evergreen notes should be atomic_](https://notes.andymatuschak.org/Evergreen_notes_should_be_atomic).

   **Unlocks:** a vault ingestion artifact: `gemini-report-to-claim-graph` agent spec or script. The current concept can justify cloud research; this addition makes it operationally useful inside the nightly synthesis/critic loop. It would let Sean ship a portfolio one-pager showing how expensive research becomes reusable infrastructure instead of another markdown report buried in `vault/20_projects/research/`.

## From Anti-Gravity (Gemini 3)

### 1. Multi-Perspective Pre-Computation (The "STORM" Pattern)
**WHAT to add:** A pre-computation step that fractures a single compound query into simulated, adversarial personas *before* dispatching it to Gemini Deep Research, forcing the cloud agent to synthesize across forced perspectives rather than defaulting to its RLHF'd "helpful consensus" narrative. 
**WHO/WHAT exemplifies it:** Stanford's STORM framework (Yijia Shao et al., *"Evaluating Collaborative Roleplay for Wikipedia-like Article Generation"*). STORM explicitly splits research into a perspective-driven question-asking phase and a subsequent synthesis phase.
**WHAT this unlocks:** **An Agent Spec (`dr_orchestrator.py`).** Currently, your concept treats Gemini DR as a black box you throw a prompt into. By implementing STORM's pattern, you ship an orchestrator that uses your local Mac Mini (`phi4-mini`) to generate 5 conflicting expert personas, ask 5 distinct sub-questions, and feed *that* matrix into Gemini DR. This unlocks the ability to generate rigorous, multi-axis Due-Diligence Matrices (e.g., "compare A/B/C on dimensions 1-4") where Gemini DR currently risks glossing over edge cases in favor of a smooth narrative. 

### 2. Predictive LLM Cascading (A Priori Routing)
**WHAT to add:** Predictive model routing. Right now, your vault notes indicate you route to Gemini DR reactively—either when LDR hits a hard 900-second timeout or when citation quality collapses. You are paying a 15-minute latency penalty just to discover a query was too hard for local inference.
**WHO/WHAT exemplifies it:** *"FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance"* (Lingjiao Chen et al., Stanford/Berkeley). FrugalGPT formalizes LLM cascades by training lightweight scorers to predict when a cheaper model will fail, routing to the expensive model immediately.
**WHAT this unlocks:** **A Substack Essay & Runbook.** You ship an essay titled "Killing the Timeout: Predictive LLM Cascading in Local Fleets," accompanied by a Python runbook. You use your existing `nomic-embed-text` to cluster past failed LDR prompts, creating a logistic regression gate in `hybrid_router.py`. This unlocks zero-latency routing: the system instantly identifies compound queries (≥3 sub-questions) and sends them to Gemini DR at second 0, rather than second 900. 

### 3. Declarative Concept Extraction (The DSPy Paradigm)
**WHAT to add:** A compiler-driven extraction layer for Gemini DR's output. Gemini deep research produces massive, unstructured markdown walls. Your architecture relies on highly structured SQLite `concept_edges` (supports/contradicts/evolved_into). The missing link is how to robustly pull graph data out of Gemini's prose without writing flaky prompt-chaining scripts or manually reviewing the `research-queue.md`.
**WHO/WHAT exemplifies it:** The **DSPy** framework by Omar Khattab et al. (Stanford), specifically the `dspy.TypedPredict` module. DSPy treats LLMs as optimizable programs rather than conversational agents, compiling declarative signatures into robust extraction pipelines.
**WHAT this unlocks:** **An Executable Demo.** You build a small DSPy pipeline script that ingests the raw markdown blob from Gemini DR, applies a strict `Signature` for your 6 SQLite relations, and deterministically outputs JSON arrays of new vault concepts and edges. This unlocks a fully autonomous "Cloud-to-Local-Graph" pipeline, allowing the `Vault Synthesizer` to automatically ingest Gemini's multi-day research straight into `vault/.vault-index.db` with validated confidence scores.
