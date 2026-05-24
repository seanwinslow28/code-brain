---
title: "How to make `Eval Vocabulary and Vibe-Coding Interview Canon Synergy` better"
type: expansion
parent: "[[eval-vocabulary-and-vibe-coding-interview-canon-synergy]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-24
updated: 2026-05-24
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[eval-vocabulary-and-vibe-coding-interview-canon-synergy]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “construct-validity mode” anchored on Messick**
   - **What to add:** A missing eval-interview facet: *validity before metrics*. The concept currently treats eval vocabulary as terms to master, but not as an argument about whether a metric measures the thing Sean claims it measures. Add a section called **Construct Validity for AI Evals** with the sentence pattern: “This metric is only useful if the target construct is actually ___; otherwise it optimizes ___ instead.”
   - **Exemplar:** Samuel Messick, **“Validity of Psychological Assessment: Validation of Inferences from Persons’ Responses and Performances as Scientific Inquiry into Score Meaning”**.
   - **Unlocks:** Lets Sean produce a stronger **AI-PM interview artifact**: an eval-design teardown where he can say, “accuracy is the wrong eval because the product claim is trust, not correctness.” Current concept gets him fluent; this makes him judgmental in the good sense.

2. **Add “Goodhart failure mode” anchored on Strathern/Campbell**
   - **What to add:** A contradicting framework: eval vocabulary should not just help Sean choose metrics; it should help him explain how metrics corrupt systems once agents optimize against them. Add **Metric Capture / Goodhart Mode** with the sentence pattern: “Once ___ becomes the target, the agent can satisfy it by ___ while degrading ___.”
   - **Exemplar:** Marilyn Strathern, **“‘Improving Ratings’: Audit in the British University System”**; pair with Donald Campbell, **“Assessing the Impact of Planned Social Change.”**
   - **Unlocks:** Lets Sean ship a **Substack essay or portfolio one-pager** on agent fleet governance: “Why my nightly critic should not optimize for number of new concepts.” This connects eval vocabulary to his real Code-Brain system instead of leaving it as interview prep trivia.

3. **Add “interview answer as eval card” anchored on Mitchell et al.**
   - **What to add:** A practical artifact pattern: every eval concept should produce a reusable interview answer in the shape of an **Eval Card**: task, user harm, metric, baseline, slice, failure mode, mitigation, decision threshold. This turns vocabulary into performance scaffolding.
   - **Exemplar:** Margaret Mitchell et al., **“Model Cards for Model Reporting.”**
   - **Unlocks:** Lets Sean produce an executable **vibe-coding interview canon artifact**: a bank of 10 eval cards for common AI-product scenarios, e.g. “support bot hallucination,” “job-feed ranking,” “agent tool-call safety,” “sprite QA classifier.” Current concept says “know precision/recall”; this would make Sean sound like someone who has operated evals in anger.

## From Anti-Gravity (Gemini 3)

### 1. LLM-as-a-Judge and Pairwise Elo Scoring
- **WHAT:** The current concept relies on traditional ML classifier metrics (Precision, Recall, F1). You must replace these with LLM-as-a-Judge rubric engineering and pairwise Elo rating systems, which are the actual standards for evaluating generative "vibe" tasks.
- **WHO/WHAT:** Hamel Husain's essay "Evaluating LLMs is a Minefield" and the LMSYS Chatbot Arena paper ("Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" by Zheng et al.).
- **WHAT THIS UNLOCKS:** An **executable demo** leveraging your existing `llm-council`. Instead of just synthesizing critique, you can build a script that uses your `llm-council` to run pairwise Bradley-Terry Elo scoring on the outputs of your `vault-synthesizer` vs. a baseline model. This proves to hiring managers you can architect modern, non-deterministic evaluation pipelines, not just recite classification metrics.

### 2. Assertion-Based LLM Testing (Span-level Evaluation)
- **WHAT:** The leap from "vibe coding" to production requires deterministic assertion-based testing for non-deterministic outputs (e.g., semantic similarity thresholds, structural JSON validation, forbidden substring checks, context-grounding checks).
- **WHO/WHAT:** The `promptfoo` evaluation framework documentation and methodology (specifically their concepts of deterministic assertions on generative pipelines) and Harrison Chase's talks on trace-based evaluation in LangSmith.
- **WHAT THIS UNLOCKS:** A **runbook and agent spec** for upgrading your `evals/vault-synthesizer/` 10-case suite. You can ship a concrete implementation that automatically fails the build if the synthesizer hallucinates a citation or breaks the `EDC canonicalization` JSON schema, converting a vague "interview canon" into a deployable AI-PM artifact.

### 3. The "Vibe-to-Eval" Maturity Model (Contradicting Framework)
- **WHAT:** A contradicting framework. "Vibe coding" (fast, intuition-driven, prompt-and-pray) and "eval engineering" (slow, empirical, dataset-driven) are fundamentally at odds. You don't "synergize" them; you transition between them via production logging and bootstrap evaluation. 
- **WHO/WHAT:** Swyx (Shawn Wang) on the Latent Space podcast/Substack ("The Rise of the AI Engineer") and Shreya Shankar's research paper "Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences."
- **WHAT THIS UNLOCKS:** A **Substack essay** (in your "sean default" voice). You can articulate the exact inflection point in an AI product's lifecycle where a solo developer must stop "vibe coding" and lock down a CI-gated eval harness. This gives you a high-signal portfolio one-pager for AI-PM roles, demonstrating you understand the trade-off between engineering velocity and product reliability.
