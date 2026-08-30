---
title: "How to make `Citation Quality` better"
type: expansion
parent: "[[citation-quality]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-08-30
updated: 2026-08-30
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[citation-quality]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

## 1. Add an “entailment × completeness” citation contract

- **What to add:** Replace the binary good/bad notion of citation quality with two claim-level tests: **citation entailment** (“Does this source actually support the attached claim?”) and **citation completeness** (“Does every externally verifiable claim have support?”). A real URL can pass validity while failing both.
- **Exemplar:** Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen, [“Enabling Large Language Models to Generate Text with Citations” (ALCE)](https://aclanthology.org/2023.emnlp-main.398.pdf). ALCE supplies an executable benchmark and evaluation code, not merely principles.
- **What it unlocks:** Ship a **citation-quality eval suite** for the fleet: atomize each generated note into claims, score entailment and completeness separately, and block publication below thresholds. This turns the concept from an incident description into a measurable agent specification and gives Sean a strong portfolio demo: “Here is the regression test that catches plausible-looking citations.”

## 2. Add pipeline-localized failure diagnosis

- **What to add:** Citation failure is not one failure mode. Separate **retrieval relevance**, **context coverage**, **generation faithfulness**, and **answer relevance**. The current article prematurely attributes collapse to Qwen3-14B and compound prompts; sometimes the generator never received adequate evidence.
- **Exemplar:** Shahul Es, Jithin James, Luis Espinosa-Anke, and Steven Schockaert, [“RAGAS: Automated Evaluation of Retrieval Augmented Generation”](https://aclanthology.org/2024.eacl-demo.16.pdf). Its key move is evaluating retrieval and generation independently without requiring a human-authored reference answer.
- **What it unlocks:** Ship a **citation-collapse runbook** and failure manifest with fields such as `retrieval_miss`, `context_noise`, `unsupported_generation`, and `citation_misattribution`. That would let Sean decide whether to rewrite the query, change retrieval/reranking, reduce scope, upgrade the model, or escalate to Gemini DR—rather than treating every bad citation as a model-capability problem.

## 3. Add warrant auditing: a citation can be correct while the conclusion is wrong

- **What to add:** Introduce a **Toulmin claim–data–warrant–qualifier–rebuttal pass**. Citations establish data; they do not validate the unstated rule connecting that data to a conclusion. Require agents to expose that rule and identify conditions under which it fails.
- **Exemplar:** Stephen Toulmin, [*The Uses of Argument*](https://johnnywalters.weebly.com/uploads/1/3/3/5/13358288/toulmin-the-uses-of-argument_1.pdf). Toulmin’s framework distinguishes evidence from the warrant authorizing an inference and from the qualifier limiting its force.
- **What it unlocks:** Ship an **argument-audit agent** or evidence ledger whose rows are `claim → evidence → warrant → qualifier → rebuttal`. This reaches decision memos, research syntheses, and critical Substack essays that the current concept cannot: outputs that are not merely source-backed, but whose reasoning is inspectable. It also catches the more dangerous failure mode—perfect citations attached to an invalid inference.

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
