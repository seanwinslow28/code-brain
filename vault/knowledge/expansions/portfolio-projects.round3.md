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

1. **Add “Portfolio as Proof-of-Work Argument,” anchored on Austin Kleon’s _Show Your Work!_**

   Current concept defines portfolio projects as examples. That is too passive. Add a mode where each project is treated as a public proof chain: problem, constraint, artifact, decision record, failure, revision, observable output.

   **Sentence pattern:** “This project proves I can `CAPABILITY` under `CONSTRAINT`, because I shipped `ARTIFACT`, made `TRADEOFF`, and learned `NON-OBVIOUS LESSON`.”

   **Unlocks:** a portfolio one-pager and interview talk track where Code-Brain, 16BitFit, intent-engineering, and llm-council stop sounding like “cool personal projects” and become evidence packets for hiring decisions. This especially helps AI-PM interviews where the risk is sounding like an enthusiast instead of an operator.

2. **Add “Taste as Selection Pressure,” anchored on Ira Glass’s _The Gap_ monologue**

   Sean’s portfolio concept is missing the aesthetic judgment layer: why these projects, why this quality bar, why this weird combination of agent ops, pixel art, PM artifacts, and writing voice? Ira Glass’s “taste gap” frame gives him a way to explain unfinished-but-serious work without apologizing for incompleteness.

   **Sentence pattern:** “The important part is not that this is finished; it is that my taste is already rejecting `WEAK_VERSION`, so I built `SYSTEM/LOOP` to close the gap.”

   **Unlocks:** a Substack essay or portfolio intro that makes the fleet itself legible as a taste-closing machine. Without this, Sean’s projects risk reading as breadth-first tinkering. With it, the work reads as a coherent apprenticeship in judgment: agents, critique loops, evals, and creative pipelines as mechanisms for improving taste at scale.

3. **Add “Artifact Portfolio vs Credential Portfolio,” anchored on Paul Graham’s essay _The Bus Ticket Theory of Genius_**

   The concept currently assumes portfolio projects demonstrate skill and values. Missing contradiction: conventional portfolios optimize for legibility to employers; Sean’s strongest signal may be obsessive, slightly unreasonable artifact density. Graham’s “bus ticket” frame gives language for why the weirdness is the point, not a liability.

   **Sentence pattern:** “This is not here because it maps cleanly to a job description; it is here because it reveals the obsession that keeps generating useful artifacts.”

   **Unlocks:** a decision framework for what to include or cut. Code-Brain belongs because it shows obsession plus compounding infrastructure. A generic PM case study may not. This would let Sean produce a sharper portfolio taxonomy: “credential artifacts” for recruiter trust, “proof artifacts” for hiring-manager confidence, and “obsession artifacts” for differentiated signal.

## From Anti-Gravity (Gemini 3)

**1. Glass-Box Trace Artifacts**
*   **WHAT to add:** Shift the atomic unit of the portfolio from "completed software" to "annotated reasoning traces." For an agentic IC, the final product matters less than the *steering*. You must show the agent's multi-step decision tree, specifically highlighting tool-use rejections, PreToolUse hook denials, and the fleet's self-correction.
*   **WHO/WHAT exemplifies it:** **Simon Willison's "TIL" (Today I Learned) repository** and his methodology of publishing raw `llm` CLI interaction logs. Willison treats the messy, iterative interaction log—including dead ends—as the primary technical artifact, rather than just the polished output.
*   **WHAT this unlocks:** **The Interactive Audit Log**. Instead of a static PM case study, you ship a reproducible `llm-council` debate transcript or an annotated `vault_critic` execution trace. This proves you can instrument and orchestrate high-variance AI logic, where a generic PM would just show a screenshot of a final product.

**2. The Agentic Incident Post-Mortem**
*   **WHAT to add:** Frame your autonomous fleet's failures (like the Qwen3-14B LDR citation collapse referenced in your vault) as high-signal portfolio assets. A traditional portfolio highlights successes; a senior IC portfolio highlights the architectural response to non-deterministic failure.
*   **WHO/WHAT exemplifies it:** **Dan Luu’s "Post-mortems" essay collection**, specifically his analyses distinguishing systemic failures from root causes in distributed systems. Treat your macOS launchd agent fleet exactly like a production distributed system that suffered an outage.
*   **WHAT this unlocks:** **The Agent Incident Runbook / Autopsy Essay**. You write a public autopsy of exactly *why* the local model hallucinated `learn.microsoft.com` URLs, and map it directly to the architectural fix you implemented (the hard routing rule to Gemini DR). This instantly establishes engineering credibility, proving you mitigate LLM unreliability through hard system architecture rather than fragile prompt-tweaking.

**3. The Literate Intent Specification**
*   **WHAT to add:** Elevate the *constraints themselves* to be the portfolio deliverable. Don't just show the output of 16BitFit Battle Mode; show the explicit Action Schemas, Stop Rules, and Forbidden Actions that constrained the AI to build it correctly within your Hexagonal/Ports & Adapters architecture. 
*   **WHO/WHAT exemplifies it:** **Anthropic’s public release of the "Claude 3.5 System Prompts" (July 2024)** combined with **David Harel’s paper "Statecharts: A visual formalism for complex systems."** Anthropic’s release demonstrated that for autonomous AI, the constraint document *is* the intellectual property. 
*   **WHAT this unlocks:** **The Executable Spec One-Pager**. You publish an artifact displaying your Intent Charter, the I-5 mapping, and the exact `<default_to_action>` trace that executed it. This unlocks the "Spec-Driven Development" PM genre, proving to employers you know how to encode organizational intent into autonomous guardrails, completely escaping the generic "I built an app with Claude" failure mode.
