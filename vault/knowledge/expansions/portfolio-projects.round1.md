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

1. **Add “Case-Study Spine” anchored on Julie Zhuo’s _The Making of a Manager_**

Add a portfolio-project pattern that turns each project into a managerial/product judgment story, not a showcase item.

Sentence pattern: **“The ambiguous situation was X; the constraint that mattered was Y; I chose Z; the tradeoff was A over B; the evidence afterward was C.”**

Exemplar: Julie Zhuo, _The Making of a Manager_, especially her repeated focus on decisions, feedback loops, and what changed because of the work.

This unlocks **interview-ready product judgment artifacts**: STAR stories, PM case narratives, “tell me about a project” answers, and project one-pagers. Right now the concept says “curated selection of past work,” which leaves Sean sounding like he is listing artifacts. This addition makes each project prove decision quality.

2. **Add “Brag Document Mode” anchored on Julia Evans’ _Get your work recognized: write a brag document_**

Add a facet for portfolio projects as accumulated evidence of impact, written in concrete units: shipped, improved, automated, reduced, clarified, taught, influenced.

Sentence pattern: **“Before this, X was costly/unclear/manual; I built Y; the measurable or observable change was Z; the reusable lesson is A.”**

Exemplar: Julia Evans, “Get your work recognized: write a brag document.”

This unlocks **evidence inventories and promotion/interview packets**: a living brag document, resume bullets, LinkedIn project descriptions, recruiter screens, and answer banks. The current concept cannot distinguish “interesting project” from “proof of employable signal.” Brag-document mode forces each portfolio item to carry outcome, scope, and credibility.

3. **Add “Build-in-Public Artifact Ladder” anchored on Maggie Appleton’s _The Expanding Dark Forest and Generative AI_**

Add a framework for portfolio projects as public trust artifacts, not just private examples. Sean should define which layer each project has reached: private note, internal demo, narrated walkthrough, public essay, repo, live tool, reusable template, repeatable method.

Sentence pattern: **“This project is not finished until it has a public artifact that lets a stranger verify one claim: CLAIM. The artifact form is FORM because the trust problem is TRUST PROBLEM.”**

Exemplar: Maggie Appleton, “The Expanding Dark Forest and Generative AI,” specifically the pressure it places on authentic, attributable human signal in a web flooded by generated text.

This unlocks **public credibility work**: portfolio pages, GitHub READMEs, Loom walkthroughs, architecture notes, demo scripts, and “how I think” essays. The current concept treats portfolio projects as things to explain when asked. This addition makes them things that already explain Sean before the interview starts.

## From Anti-Gravity (Gemini 3)

**1. Executable Process Artifacts (Prompt/Trace Logging)**
*   **WHAT:** Shift the portfolio unit from the "finished application" to the "executable iteration log." This means treating the prompt traces, dead ends, and context-window management as the actual portfolio piece, proving *how* the agent was steered rather than just showing the end result.
*   **WHO/WHAT:** Anchored on Simon Willison's essay "Prompt-Driven Development" and his specific `simonw/til` (Today I Learned) repository pattern, which explicitly publishes the full LLM chat transcripts alongside the resulting code commits.
*   **UNLOCKS:** This unlocks the Forensic Interview Artifact genre where Sean currently sounds like a generic traditional product manager claiming credit for black-box AI output. By handing the interviewer the exact prompt trace, Sean proves hands-on steering capability for vibe-coding interviews.

**2. The "Failed-State Narrative" (Agentic ADRs)**
*   **WHAT:** A formal structure for cataloging the exact boundaries of what *didn't* work in his past agent builds. It treats the discarded branches, hallucination regressions, and architectural dead ends as the primary signal of senior-level competence and intent engineering.
*   **WHO/WHAT:** Anchored on Michael Nygard's canonical article "Documenting Architecture Decisions" (the formalization of the ADR), specifically adapting the "Alternatives Considered" section to explain why specific agentic frameworks or prompting strategies were explicitly abandoned.
*   **UNLOCKS:** This unlocks the Resilience Proof genre where Sean currently sounds like a junior developer giving a happy-path demo. It allows him to proactively lead the vibe-coding interview by dissecting his own architectural dead-ends before the interviewer has to probe for them.

**3. Evals as the Primary Portfolio Deliverable**
*   **WHAT:** Flipping the portfolio focus so the *evaluation framework*—the unit tests, the semantic boundary checks, the LLM-as-a-judge criteria, and the CI/CD pipeline—is presented as the core project, rather than the consumer-facing app the agent built.
*   **WHO/WHAT:** Anchored on Hamel Husain's specific essay "Your AI Product Needs Evals," adopting his exact methodology for building and documenting task-specific assertion pipelines that constrain unpredictable models.
*   **UNLOCKS:** This unlocks the System Definition Document genre where Sean currently sounds like a prompt-jockey showing off a lucky zero-shot output. Focusing on evals proves he knows how to reliably productionize, bound, and measure an agent fleet, establishing immediate engineering-leadership credibility.
