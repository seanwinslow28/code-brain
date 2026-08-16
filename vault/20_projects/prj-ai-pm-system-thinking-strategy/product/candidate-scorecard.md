---
title: Product Candidate Scorecard (v1, draft-for-sean)
type: decision-doc
status: draft-for-sean
created: 2026-08-16
evidence: ../../research/2026-08-16-ai-product-post-launch-loops-pm-idea-ledger.md
rubric: evidence strength · systems-thinking surface area · buildable in 5 wk @ 5-8 hrs/wk · recruiter demo-ability (1-5 each)
---

# Product Candidates — Phase 2 build

All four candidates trace to verified discovery pain. Scores are Claude's draft; council critique + Sean's call decide. **Standing check before final commitment (week 3): a named-candidate falsification pass** — 5-tool teardown per candidate to prove the gap is real, per the ledger's own proposed-bet tests and the verify-provenance rule.

## C1 — Silent Failure Radar
Monitoring for LLM features that flags quality degradation/drift **without ground-truth labels**, with trace-level diagnosis of *why* (retrieval defect vs tool error vs drift).
- Evidence: "AI fails silently… users just leave" (imp 5/5); "surface analytics cannot diagnose root causes"; gap 8 backfill.
- Scores: evidence **4** · surface **4** (drift + balancing loops + observability) · buildability **2** (real prod infra needed; crowded vendor field: Arize, Langfuse, Comet) · demo **3** → **13**

## C2 — Golden Loop (eval-first cockpit for PM-led teams)
Turns production failures into a **versioned golden dataset** and runs **champion/challenger improvement rounds with holdout discipline** — PM-grade workflow, not dev-grade tooling.
- Evidence: top pain "AI quality is difficult to define and measure" (3 domains); gap 9 (dataset build/version/maintain); champion-loop discourse (last30days).
- Scores: evidence **5** · surface **5** (the full M7 loop anatomy, Goodhart guards, stop conditions) · buildability **3** (adjacent incumbents: Braintrust, Langfuse datasets, promptfoo — differentiation burden) · demo **3** (hard for a recruiter to *feel* in 5 minutes) → **16**

## C3 — The AI PM Flight Simulator  ⭐ recommended
A playable web simulator: you are the PM of a fictional AI product; incidents unfold (drift, reward hacking, degenerate loops, silent failure); you diagnose through the iceberg/CLD and choose interventions; **consequences play out with realistic delays** across simulated weeks. Spaced-retrieval built in. LLM-generated scenario variation governed by its **own eval harness** (golden scenarios, quality rubric, champion/challenger on the scenario prompt) — which honestly satisfies the program's "instrumented loop" requirement.
- Evidence: "PMs lack confidence and evaluation skills" (70%-fear stat, 2 domains); DR Part III — **management flight simulators are the strongest evidence-backed pedagogy for systemic judgment** (MIT lineage); discovery whitespace = no training-shaped solution surfaced.
- Meta-strength: the artifact *demonstrates the curriculum by teaching it*. Recruiters and hiring managers are PMs — they can play it, feel the delayed feedback bite, and see Sean's systems fluency + creative craft (his game/animation strengths) in one artifact.
- Scores: evidence **4** · surface **5** (simulates the dynamics AND needs real evals for its generator) · buildability **4** (web app + scenario engine; no prod telemetry infra; Sean's frontend/game wheelhouse) · demo **5** (playable in five minutes) → **18**

## C4 — Launch Gate (pre-ship harness for AI features)
Checklist-as-code: golden-dataset eval run + rollout guardrails + rollback conditions gate an AI feature's ship.
- Evidence: gaps 1/5/9 backfills only — thinnest grounding.
- Scores: evidence **3** · surface **3** · buildability **4** · demo **2** → **12**

## Recommendation

**C3 (Flight Simulator), C2 as runner-up.** C3 wins on the two dimensions that can't be faked later: demo-ability to the actual hiring audience and honest systems-thinking surface (both the *content* it simulates and the *harness* it needs). Its main risk — "is it a toy?" — is countered by the eval harness + decision log being production-grade artifacts, and by the falsification pass (if a serious AI-PM simulator already exists, C2 takes the slot).
