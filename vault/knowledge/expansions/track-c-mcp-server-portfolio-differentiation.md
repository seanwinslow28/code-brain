---
title: "How to make `Track C MCP Server / Portfolio Differentiation` better"
type: expansion
parent: "[[track-c-mcp-server-portfolio-differentiation]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[track-c-mcp-server-portfolio-differentiation]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “Capability Naming as Positioning” anchored on April Dunford’s _Obviously Awesome_**

   The concept currently says MCP names should tell strangers what the server connects to. That is useful, but too shallow. Add a positioning test: name the server by the **competitive alternative it replaces** and the **unique capability it creates**.

   **Pattern:** “For people using `[existing workflow]`, this is not a `[generic MCP server]`; it is a `[specific capability]` that lets them `[new action].`”

   **Exemplar:** April Dunford, _Obviously Awesome: How to Nail Product Positioning so Customers Get It, Buy It, Love It_.

   **Unlocks for Sean:** A portfolio one-pager that stops presenting “vault MCP” as plumbing and frames it as a product wedge: “personal knowledge vault as an interviewable agent memory substrate,” “MCP server for critique retrieval,” “portfolio-grade agent context API.” This would help him decide whether the artifact is for hiring managers, agent engineers, PM leaders, or open-source users. Right now the concept only reaches README clarity; Dunford gets it to market category design.

2. **Add “Interface Contract Over Tool Demo” anchored on Martin Fowler’s _Consumer-Driven Contracts_ writing**

   The missing facet is that an MCP server is not differentiated by what it exposes; it is differentiated by the **contract it guarantees under agent use**. Naming and allowlists are table stakes. The stronger portfolio signal is: “Here is the contract agents can rely on, here are the unsafe queries it refuses, here are the invariants tested.”

   **Exemplar:** Martin Fowler, “Consumer-Driven Contracts: A Service Evolution Pattern.”

   **Add this mode:** Define MCP endpoints as contracts with examples:
   - `search_concepts` guarantees cited vault paths, not synthetic summaries.
   - `get_concept_graph` guarantees relation types from the six-edge ontology.
   - `critique_concept` must return missing references, contradicting frameworks, and ship-able artifact suggestions.

   **Unlocks for Sean:** An executable demo and test suite, not just a portfolio narrative. This lets him ship “vault MCP contract tests” as proof of agentic-engineering maturity: behavior specs, failure cases, permissions, and regression checks. The current concept says “clarity and focus”; this would show operational reliability.

3. **Add “Memex-to-Augmenting-Intellect Lineage” anchored on Vannevar Bush + Douglas Engelbart**

   The concept is missing historical lineage. “Personal knowledge vault exposed through MCP” sounds like another Obsidian integration unless it is placed inside the older tradition of tools that augment cognition.

   **Exemplars:** Vannevar Bush, “As We May Think” and Douglas Engelbart, “Augmenting Human Intellect: A Conceptual Framework.”

   **Add this contrast:** Bush gives the associative trail; Engelbart gives the bootstrapping system. Sean’s differentiator is not “vault access by MCP.” It is **agent-readable augmentation infrastructure**: trails, citations, contradictions, scheduled critique, and tool-mediated self-improvement.

   **Unlocks for Sean:** A Substack essay or interview answer with intellectual weight: “My vault MCP is a small Engelbart system, not an Obsidian plugin.” This gives him a stronger voice for AI-PM and agentic-IC interviews, where the current concept risks sounding like integration glue.

## From Anti-Gravity (Gemini 3)

### 1. Intent-Exposing Interfaces
- **WHAT to add:** A UX pattern that moves agent orchestration out of headless terminal execution and into visible, scrubbable state machines. Portfolio differentiation for an AI-PM isn't just naming a backend MCP clearly; it is making the agent's internal intent visually negotiable for the user. 
- **WHO/WHAT exemplifies it:** Amelia Wattenberger's essay *"Why Chatbots Are Not the Future"* (specifically her arguments on exposing LLM state and spatial affordances, which heavily influenced Adept and Copilot Workspace).
- **WHAT this would unlock:** An **executable UX prototype** (built via your Remotion or Phaser pipeline). Instead of just pitching a headless CLI in an interview, you ship a visual demo where an agent pauses to negotiate an Action Schema and Stop Rules with the user *before* mutating the vault. This bridges your backend Intent Engineering work into a PM-grade product demo, proving you can design human-in-the-loop (HITL) agent interactions.

### 2. Declarative Capability Signatures
- **WHAT to add:** Your current concept compares your server to `mcp-obsidian`—which merely exposes raw markdown files. True differentiation comes from exposing the *computational signatures* of your autonomous layer. Your MCP shouldn't just serve files; it should serve the declarative capabilities of your fleet (e.g., triggering your Vault Critic or Deep Researcher).
- **WHO/WHAT exemplifies it:** Stanford NLP's paper *"DSPy: Compiling Declarative Language Model Calls into State-of-the-Art Pipelines"* (Omar Khattab et al., 2023), specifically the shift from imperative prompting to declarative capability signatures.
- **WHAT this would unlock:** An **Architecture Decision Record (ADR) and an executable code snippet** showing how your MCP server translates the static Intent Rules from your `CLAUDE.md` into programmatic, DSPy-style declarative tools. This artifact proves to engineering and PM hiring panels that you understand multi-agent orchestration beyond naive string-passing and wrapper APIs.

### 3. Epistemic State Tracking
- **WHAT to add:** A structural approach to data provenance. Your Code-Brain vault contains a mix of human-authored notes and agent-generated synthetic edges (`.vault-index.db`). A differentiated personal MCP must explicitly broadcast the provenance, generation method, and confidence decay of its data so the consuming model knows how to weight it. 
- **WHO/WHAT exemplifies it:** Maggie Appleton's design essay *"Epistemic Disclosure"* combined with Gwern Branwen's strict *"Epistemic Status / Certainty"* metadata architecture on his canonical digital garden (`gwern.net`).
- **WHAT this would unlock:** A **Substack practice essay and a concrete SQLite schema update** detailing "Solving RAG Hallucination via Epistemic Metadata." It shifts your writing from descriptive ("I built a cool tool to connect Obsidian") to prescriptive thought leadership ("How enterprise agent fleets must structurally weigh human vs. synthetic ground truth").
