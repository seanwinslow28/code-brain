---
title: "How to make `Automation Reliability` better"
type: expansion
parent: "[[automation-reliability]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-05-27
updated: 2026-05-27
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via Anti-Gravity CLI) of [[automation-reliability]]. The synthesizer describes what the concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

1. **Add “control-loop reliability,” not just benchmark reliability.**  
   Anchor it on Nancy Leveson’s STAMP/STPA in *Engineering a Safer World* and MIT PSASS’s STAMP/STPA materials: safety failures come from inadequate control, feedback, constraints, and process models, not only component breakage. Current concept says “schema adherence degraded”; STPA would ask: *which controller had a wrong model of runtime state, and which constraint failed to prevent bad output?*  
   Unlock: an **agent safety case / incident review template** for Sean’s fleet: controller, controlled process, feedback channel, unsafe control action, missing constraint. This turns “silent failure” into a publishable agent-ops framework instead of another monitoring note. Sources: [MIT PSASS](https://psas.scripts.mit.edu/home/books-and-handbooks/), [STAMP overview](https://www.stamp-workshop.eu/about-stamp/).

2. **Add “metamorphic evals” for outputs without stable oracles.**  
   Anchor it on T.Y. Chen, S.C. Cheung, and S.M. Yiu’s “Metamorphic Testing: A New Approach for Generating Next Test Cases” and David MacIver/Zac Hatfield-Dodds’ Hypothesis paper. Sentence pattern: *If input transformation T preserves requirement R, output relation O must still hold.* Example: reorder source snippets, rename neutral entities, vary runtime temperature, or add irrelevant context; the concept extraction should preserve required JSON shape, key claims, and citation provenance.  
   Unlock: an **executable eval harness** for vault synthesizer/job-feed agents that finds silent failures without needing a golden answer for every article. Current concept can compare runtimes; metamorphic testing lets Sean generate adversarial reliability cases cheaply. Sources: [Chen/Cheung/Yiu lineage](https://arxiv.org/abs/2002.12543), [Hypothesis JOSS paper](https://joss.theoj.org/papers/10.21105/joss.01891).

3. **Add “reliability budget mode” for deciding when automation may keep shipping.**  
   Anchor it on Google’s *Site Reliability Engineering*, especially SLOs/error budgets. Current concept treats reliability as a measurement problem; SRE turns it into a **go/no-go policy**: if schema-valid concept generation drops below X over Y runs, freeze model swaps, route to manual review, or spend budget on eval hardening before new agent features.  
   Unlock: a **fleet reliability runbook + portfolio one-pager**: “I manage personal agents with SLOs, error budgets, and release gates.” That maps directly to AI-PM/senior-PM interviews because it converts Sean’s homegrown fleet into a product-operating system with decision rules. Source: [Google SRE chapter on SLOs](https://sre.google/sre-book/service-level-objectives/).

## From Anti-Gravity (Gemini 3)

_Anti-Gravity rate-capped or failed; no critique this run._
