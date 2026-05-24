---
title: "How to make `Portfolio Projects` better"
type: expansion
parent: "[[portfolio-projects]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[portfolio-projects]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Portfolio as Proof-of-Work Ledger,” anchored on Austin Kleon’s _Show Your Work!_**

   Current concept says “curated selection of past work,” which is too static. Add a mode where each project is treated as a public trail of decisions, constraints, failures, pivots, and shipped artifacts.

   **Sentence pattern:** “This project proves I can move from `messy constraint` to `working artifact` by making `specific technical/product decision` under `specific pressure`.”

   **Exemplar:** Austin Kleon, _Show Your Work!_ especially the “think process, not product” frame.

   **Unlocks:** A portfolio one-pager or interview runbook where Code-Brain, 16BitFit, intent-engineering, and llm-council are not listed as achievements but decomposed into evidence chains. This helps Sean avoid the generic “I built cool agent stuff” failure mode and instead show how he thinks, cuts scope, debugs, and ships.


2. **Add “Case Study Spine,” anchored on Richard Rumelt’s _Good Strategy Bad Strategy_**

   The article lacks a structure for turning a portfolio project into a strategic story. Add Rumelt’s kernel: diagnosis, guiding policy, coherent actions. Every portfolio project should answer:

   - Diagnosis: what was actually broken or uncertain?
   - Guiding policy: what principle narrowed the solution space?
   - Coherent actions: what did Sean build, automate, measure, or discard?

   **Exemplar:** Richard Rumelt, _Good Strategy Bad Strategy_, specifically the “kernel of good strategy.”

   **Unlocks:** Senior-PM and AI-PM interview narratives. This lets Sean explain Code-Brain as a strategic response to “personal knowledge systems become passive archives,” not merely “I have agents and an Obsidian vault.” It also supports PRD-style artifacts, roadmap memos, and portfolio case studies that sound executive-legible without flattening the engineering depth.


3. **Add “Demo-First Portfolio,” anchored on Bret Victor’s “Inventing on Principle” talk**

   The current concept treats portfolio projects as things to explain. For agentic-engineering IC work, Sean needs a stronger facet: portfolio projects as live demonstrations of a principle.

   Add a “demo-first” requirement: each portfolio project should contain one inspectable moment where the viewer can see the system’s principle in action.

   **Exemplar:** Bret Victor, “Inventing on Principle” talk, 2012.

   **Sentence pattern:** “The principle is `X`; the demo makes it visible when `Y changes and Z responds immediately`.”

   **Unlocks:** Executable demos and narrated walkthroughs. For Code-Brain, this could be a live “concept enters vault → indexer updates graph → critic proposes missing references → Sean accepts/rejects” loop. For intent-engineering, it could be “change declarative intent → agent behavior changes without rewriting imperative prompts.” This moves Sean beyond portfolio-as-description into portfolio-as-working argument.

## From Anti-Gravity (Gemini 3)

### 1. The "Executable Portfolio" Pattern
- **WHAT:** Transition from passive "curated selections" to active, "queryable capabilities." A portfolio for agentic engineering shouldn't be read; it should be run. 
- **WHO/WHAT:** Simon Willison's *Today I Learned (TIL)* repository architecture and *Datasette* ecosystem. Willison eschews traditional project pages in favor of continuous, automated, executable data artifacts and CLIs that programmatically prove his capabilities.
- **WHAT THIS UNLOCKS:** A "Portfolio MCP Server" artifact. Instead of sending a Notion link to an AI-PM hiring manager, you ship a ready-to-install MCP server that their local Claude instance can query to independently evaluate your `Code-Brain` architecture, retrieve your local LLM benchmarks, or interact with your `intent-engineering` specifications.

### 2. The Search Tree Graveyard
- **WHAT:** The explicit documentation of negative results, failed abstractions, and token-exhaustion dead ends as a core portfolio asset. Vibe-coding interviews test how you recover when the vibe is wrong; your portfolio must show your friction points.
- **WHO/WHAT:** Gwern Branwen's *Gwern.net*, specifically his essays documenting deeply researched failed experiments (e.g., his early GPT-2/3 blind alleys and generation failures). Gwern proves elite expertise by extensively mapping the failure space of generative models, not just their happy paths.
- **WHAT THIS UNLOCKS:** A "Local Model Post-Mortem Runbook" or a Substack essay in your *gonzo* voice. Documenting exactly *why* a Qwen3-14B routing strategy collapsed, or how your Kokoro TTS pipeline hallucinated audio garbage, proves deep IC pragmatism. It yields an artifact that separates you from traditional PMs who only understand AI as an API wrapper.

### 3. Declarative Framing via Promise Theory
- **WHAT:** A unifying architectural lens for presenting agentic work. Instead of listing imperative features ("I built 7 scheduled agents on launchd"), frame the portfolio as a study in moving from imperative commands to declarative states—the theoretical foundation of your "intent-engineering" project.
- **WHO/WHAT:** Mark Burgess's *Promise Theory: Principles and Applications*. Burgess defines complex systems not as top-down control structures, but as autonomous nodes making voluntary, declarative promises to one another.
- **WHAT THIS UNLOCKS:** An "Agent Fleet Architecture One-Pager." You rewrite the `Code-Brain` portfolio entry using Promise Theory: your Vault Indexer doesn't "run a script"; it *promises* updated vectors. The Critic *promises* high-variance teardowns. This unlocks a systems-architect narrative for senior AI-PM roles, elevating your local macOS automation scripts into a rigorous, documented distributed systems framework.
