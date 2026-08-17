---
title: Phase B Falsification Verdict — the five-tool teardown
type: research-verdict
status: final (verdict delivered 2026-08-17)
created: 2026-08-17
method: 5 parallel primary-source teardowns (official docs, GitHub, pricing, changelogs only; every claim cited in the per-tool files) + a $0 second-ring named-candidate sweep; per the program rule, a negative claim is only asserted against a named candidate list, never from absence of search results
evidence: teardowns-2026-08-17/ (braintrust.md, langfuse.md, promptfoo.md, statsig.md, freeplay.md — per-claim citations)
decision-log: ../product/decision-log.md (D1 falsifier; verdict entry pending sweep)
---

# Phase B Falsification Verdict

**The question this document answers** (D1's falsifier, stated before the research ran): *does a PM-grade decision layer on top of existing trace tooling survive contact with what Braintrust, Langfuse, promptfoo, Statsig, and Freeplay already do?*

## The one-paragraph answer

**The original hypothesis is dead in its broad form, and a narrower, better one survives.** "No tool lets a non-coding PM build datasets from production failures" is false — three of the five (Braintrust, Langfuse, Freeplay) ship no-code trace→dataset curation today, and Freeplay markets the whole lab directly to PMs, golden-set vocabulary included. What no tool ships — verified absent across all five, per-claim citations in the evidence files — is the **discipline**: (A) a first-class holdout split the iteration loop provably cannot optimize against, (B) one-change-per-round champion/challenger structure with a promotion gate, and (C) written promote/reject decision records for offline changes. Golden Loop's wedge survives **re-scoped from "the PM's eval lab" to "the scientific method, productized": the governance layer that makes an existing lab honest.**

## Feature-by-feature scoreboard

| Capability | Braintrust | Langfuse | promptfoo | Statsig | Freeplay |
|---|---|---|---|---|---|
| No-code trace → dataset curation | ✅ UI, "add to dataset" | ✅ UI, one-click + bulk | ❌ (YAML/CSV/code) | ❌ (manual/CSV only) | ✅ UI, incl. "golden set" language |
| Dataset versioning | ✅ (snapshots, $249/mo+) | ✅ first-class (2025-12) | git-only | ❌ (prompt versions only) | ❌ (datasets mutable) |
| **A. Enforced holdout split (offline)** | ❌ (own blog hand-rolls it) | ❌ (no field, no concept) | ⚠️ optimizer-only, ephemeral, default-off | ❌ ("holdout" = online users) | ❌ (zero concept) |
| **B. One-change rounds / promotion gate** | ❌ (compare only, no promote state) | ⚠️ prompt-label promotion, unlinked to results | ❌ | ⚠️ promote-to-Live, no gate/rounds | ❌ (versions bundle changes) |
| **C. Written decision records (offline)** | ❌ | ❌ | ❌ | ⚠️ real ones — online experiments only | ❌ |
| PM-operable mid-loop (post-setup) | ✅ partial | ✅ | ❌ dev-first | ✅ console grading | ✅ explicitly |
| Open-source / self-hostable | ❌ (SDKs only) | ✅ MIT core | ✅ MIT | ❌ | ❌ (SDKs only) |

Legend: ⚠️ = adjacent ingredient exists but not the discipline itself. Full evidence with URLs: [teardowns-2026-08-17/](teardowns-2026-08-17/).

## What each teardown killed, kept, and taught

- **Braintrust** — *killed:* "PMs can't get traces into datasets without engineers." *Kept:* no holdout (their own blog builds holdouts by hand because the product can't), no promotion workflow, no decision records. *Taught:* they ship adjacent ingredients monthly — position Golden Loop as the decision/governance layer, never as "a better eval tool."
- **Langfuse** (the load-bearing one) — *killed:* most of the mechanical-substrate story; ~70% of the plumbing exists and most shipped in the last 9 months. *Kept:* the data model literally has no holdout field; promotion (prompt-label flip) requires no rationale; no round structure. *Taught:* the importer is comfortably feasible (~1 week: REST API + OpenAPI spec, MIT self-host runs free on a Mac via docker-compose); build against v2/v3 APIs on a pinned v4 server — the platform is mid-migration and a legacy API sunsets 2026-11-16.
- **promptfoo** — *killed:* nothing material. *Kept:* everything; dev-first by self-description. *Taught:* its optimizer's off-by-default validation split ships with an overfitting warning — the incumbents *know* the problem exists and haven't productized the discipline. Acquired by OpenAI (2026-03), roadmap tilted to security.
- **Statsig** — *killed:* "no incumbent lets a non-coder run offline evals" (console grading exists). *Kept:* no failure curation, no dataset versioning, "holdout" means online user-holdouts, promotion is a pointer flip. *Taught:* Statsig has genuine decision-record machinery — **wired exclusively to online experiments**. Nobody has carried that discipline to the offline loop; that seat is empty. Product churn: OpenAI acquired the team (2025-09), product moved to Amplitude (2026-05), AI Evals early-access closed to new customers.
- **Freeplay** (the most dangerous, per the pre-registered brief) — *killed:* the persona claim entirely — Freeplay already IS the PM-operable lab, docs naming "product managers, domain experts" as the no-code audience. *Kept:* zero holdout concept, mutable unversioned datasets, versions bundle arbitrary changes, deployment docs contain no approval/decision-record machinery. *Taught:* two durable-wedge properties Freeplay can't cheaply copy — **Golden Loop layers on the team's existing trace tooling** (Freeplay requires its own SDK instrumentation) and **self-serve accessibility** (Freeplay is sales-gated with unpublished pricing).

## Market-structure signal (unplanned finding)

Two of the five were acquired by OpenAI within twelve months (promptfoo 2026-03; Statsig's team 2025-09, with the product passed to Amplitude 2026-05), and both were redirected away from vendor-neutral workflow tooling. The eval-tool field is consolidating and being pointed at platform agendas — which both validates that the space matters and leaves the vendor-neutral, PM-first discipline seat emptier than it was a year ago.

## The re-scoped wedge (what v1 must now say and be)

1. **Lead with the discipline, not the dataset.** The dataset-building story is table stakes the incumbents already own. The pitch is: *the sealed holdout, the one-change round, the promote/reject gate, and the written decision record — enforced by the product, operated by the PM.*
2. **The teaching layer is the differentiator dramatized.** SHIPWRECK's holdout-title-fight beat (D3) is exactly the feature no incumbent has — the demo and the wedge are now the same thing.
3. **Layer on existing tooling; stay self-serve.** The two properties the closest competitor (Freeplay) structurally lacks.
4. **Shelf-life honesty.** This is a workflow-opinion moat, not a tech moat. Langfuse shipped most of its dataset machinery in nine months; Freeplay could ship holdout flags and decision logs in a quarter. The moat is speed, opinionation, and positioning — the verdict is "build now," not "defensible forever," and the decision log will say so in public.

## Second-ring check — does anyone else ship the discipline?

Five tools cannot prove a field-wide negative. A $0 named-candidate sweep across the second ring (LangSmith, Arize Phoenix/AX, W&B Weave, Humanloop, Comet Opik, Vellum, HoneyHive, Agenta, Confident AI/DeepEval, Galileo) is checking features A/B/C against primary docs.

**Result: no second-ring incumbent ships even one of the three features in full.** The three honest near-misses, disclosed because a clean negative claim requires them:

- **Arize Phoenix** ships dataset *split labels* framed as train/validation/test (12.0+, 2025-09) — A-infrastructure without A-discipline: splits are filters for targeted experiments; nothing seals a split from iteration. Arize's own "holdout" language appears only inside optimizer cookbooks (the excluded case).
- **Confident AI / DeepEval** *recommends* "only change one independent variable at a time" in its experiments docs — the only one-change language found anywhere in the sweep — but it is advice, not structure: no rounds, no champion/challenger mechanics, unenforced.
- **Vellum** ships required-approval "Deployment Release Reviews" with protected release tags — the closest thing to decision records — but it is deployment sign-off (SOC 2-shaped), with optional comments rather than required rationale, decoupled from eval results.

Also noted: **Humanloop is dead** (Anthropic acqui-hire; platform sunset 2025-09-08 — a third incumbent consumed by a lab); champion/challenger-with-approval exists as a mature pattern in classic MLOps (DataRobot, ModelOp) for *model deployment* and has simply never been ported to LLM offline evals; one vendor blog (Future AGI) and one arXiv paper recommend exactly the sealed-holdout / promote-hold-rollback practice as *advice*, with no product behind it.

## Verdict

**BUILD. The wedge is real, re-scoped, and time-boxed.**

Across fifteen named incumbents checked against primary sources, the claim that survives is precise: **no tool ships sealed holdouts, enforced single-variable promotion rounds, or required promote/reject rationale records for offline LLM evals.** The broad version of the original hypothesis ("PMs can't run eval labs without engineers") is dead and must never be pitched — three tools already sell that lab, one of them directly to PMs. Golden Loop's seat is the layer every lab is missing: **the product that makes the existing lab honest.** The demand-side tell is everywhere in the incumbents' own material — promptfoo's overfitting warning, Braintrust's hand-rolled-holdout blog, Confident AI's one-variable recommendation, Statsig's online-only decision framework — they all *say* the discipline matters; none of them *enforce* it.

Conditions attached to this verdict, in public: (1) it is a workflow-opinion moat with a shelf life — Langfuse built most of its dataset machinery in nine months, and any incumbent could ship these features in a quarter or two; speed and opinionation are the moat. (2) The hiring-manager mock test (D6) remains the demand-side check this document cannot supply — the teardown proves the feature gap, not that buyers want it filled. (3) Verdict recorded as decision-log entry D7 with its own falsifiers and review date.
