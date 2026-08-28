---
title: Golden Loop — hiring-manager mock one-pager
type: mock (forward-test artifact, D6/D7)
status: draft for Sean's edit
created: 2026-08-17
purpose: shown to 2-3 recent AI-PM hiring managers with one question — "would you forward this to a peer?" — as the demand-side falsifier registered in decision-log D7
---

# Golden Loop

**The discipline layer for AI product quality.** Your team already has an eval lab — traces in Langfuse or Braintrust, a dataset, a judge, a compare view. Golden Loop is the layer that makes the lab honest: the sealed holdout, the one-change round, and the written record of why anything shipped.

---

## The problem

Every AI team now measures quality. Almost none can answer three questions their own process creates:

1. **"Did we just overfit to our own test set?"** Offline scores climb, production doesn't. The only defense — a held-out split your iteration loop never sees — exists in no major eval tool as an enforced concept. Teams that do it, do it by hand and by honor system.
2. **"Which change actually helped?"** Prompt tweaks ship bundled with model swaps and parameter changes. When the score moves, nobody knows what moved it.
3. **"Why did we ship this?"** Six weeks later, the eval numbers exist but the reasoning is gone. There is no record of what the alternatives were, what the holdout said, or who made the call.

The tools that own your traces (Braintrust, Langfuse, Freeplay, LangSmith) all ship dataset-building and comparison views. None of them ships the discipline. It lives in convention — which means under deadline pressure, it doesn't live at all.

## How it works

Golden Loop sits on top of the trace tooling you already run. One loop, five gates:

1. **Capture** — a flagged production failure imports from your trace tool (Langfuse-native at launch) and becomes a case in a versioned golden dataset, provenance attached.
2. **Seal** — the dataset splits on creation. The improvement set is your workbench; the holdout is sealed, and the product physically will not score a work-in-progress change against it.
3. **Challenge** — every round is champion vs. challenger, and a challenger is *one* change. The product holds you to it — a second edit in the same round is a new round.
4. **Title fight** — a challenger that wins on the improvement set earns exactly one run against the holdout. Beat the champion there or it doesn't ship. Ties go to the champion.
5. **Record** — promote or reject, the round writes its own decision record: the change, both scores, the verdict, and your one-line reason. The log is the audit trail your next PM, your compliance review, and your own memory will thank you for.

A PM operates every gate from the UI. Engineers wire the trace source once; after that, quality iteration belongs to the person accountable for quality.

## Why now

Champion/challenger with approval gates is how mature ML ops shipped models for a decade. LLM tooling skipped it — the field spent three years building labs and never installed the lab safety rules. Meanwhile the vendors that might have are being absorbed into platform agendas (OpenAI acquired two of the top five eval tools in the last year). The seat for a vendor-neutral, PM-first discipline layer is open.

## Proof it works the way it claims

Golden Loop runs its own medicine. The tool's own quality — starting with the relevance judgments of a real production job-feed agent — is governed by its own golden dataset, its own sealed holdout, and its own public decision log. Every claim in the walkthrough is a real round you can read.

**See it:** 2-minute walkthrough — you'll ship a change without the discipline, watch it burn, then run one honest round and feel the holdout catch what the green checkmarks missed. *(link)*

---
---

## ⚙️ How to run the forward test (not part of the mock — Sean's script)

- **Who:** 2–3 hiring managers who have hired an AI PM in the last ~6 months. Warm intros beat cold.
- **The ask, verbatim:** *"Two minutes: if a candidate showed you this as a portfolio artifact, would you forward it to a peer — and would that forward say 'evidence of PM skill' or 'neat side project'? Be blunt."*
- **What counts (per decision-log D7):** majority "wouldn't forward" or "neat side project" → the wedge is a feature gap without buyer pull; positioning reopens before the PRD locks. Any "what does it cost / can my team try it" counts as strong pull — note it verbatim.
- **Capture:** their exact words, in the decision log's D7 review. No paraphrase.
