---
title: "How to make `Eval Vocabulary` better"
type: expansion
parent: "[[eval-vocabulary]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-06-23
updated: 2026-06-23
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[eval-vocabulary]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “measurement lineage” before “eval vocabulary.”**  
   Anchor it on Victor Basili, Gianluigi Caldiera, and H. Dieter Rombach’s **“The Goal Question Metric Approach”** plus **GQM+Strategies**. The missing move is: `business intent -> decision question -> observable metric -> eval case -> pass/fail threshold`. Right now the concept jumps from PRD replacement to scoring tool; GQM adds the reason each score exists.  
   **Unlocks:** an **Eval Charter** artifact for the intent-engineering MCP: every eval must name the decision it changes. This lets Sean produce a PM/IC portfolio one-pager that says, “This eval is not a rubric; it is a decision instrument.” Sources: [GQM](https://en.wikipedia.org/wiki/GQM), [GQM+Strategies paper](https://arxiv.org/abs/1402.0292).

2. **Add “Goodhart-resistant evals” as the contradiction.**  
   Anchor it on Charles Goodhart’s **“Problems of Monetary Management: The UK Experience”** and Marilyn Strathern’s **“Improving Ratings: Audit in the British University System.”** Sentence pattern: “An eval becomes dangerous when it stops measuring judgment and starts training agents to satisfy the visible proxy.” The concept currently treats evals as cleaner PRDs; Goodhart/Strathern says evals become incentive systems the moment agents optimize against them.  
   **Unlocks:** a **red-team runbook** for spec scoring: hidden holdout cases, rotating judges, adversarial specs, proxy-drift checks, and “metric capture” warnings. This also unlocks a sharper Substack essay: **“Evals Are the New PRDs, Which Means They Inherit Every Disease of KPIs.”** Source: [Goodhart’s law / Strathern reference](https://en.wikipedia.org/wiki/Goodhart%27s_law).

3. **Add “eval harness, not eval rubric.”**  
   Anchor it on **OpenAI Evals**, **LangSmith Evaluation**, and **RAGAS** by Shahul Es et al. The missing vocabulary is operational: dataset, evaluator, trace, experiment, regression, online eval, pairwise judge, reference-free metric. Sean’s current concept describes a spec linter; these works turn it into a repeatable system.  
   **Unlocks:** an **executable demo** where `intent_spec` ships with fixtures: bad spec, improved spec, adversarial spec, historical production trace, and CI-style regression output. That gives Sean a stronger artifact than “portable MCP server”: a miniature eval lab for agent specs. Sources: [OpenAI Evals](https://github.com/openai/evals), [LangSmith evaluation concepts](https://docs.langchain.com/langsmith/evaluation), [RAGAS paper](https://arxiv.org/abs/2309.15217).

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
