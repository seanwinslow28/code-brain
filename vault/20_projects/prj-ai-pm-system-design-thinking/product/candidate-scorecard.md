---
title: Product Candidate Scorecard (v1 + decision record)
type: decision-doc
status: decided (Sean, 2026-08-16) — see Decision Record at bottom
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

---

## Decision Record (2026-08-16)

**Chosen: C2 — "Golden Loop", with a playable teaching layer.** Council pre-mortem (premium, 4 models) voted C2 over C3 3–1 and exposed a scoring bug that produced the v1 recommendation.

**The scorecard bug, acknowledged:** "recruiter demo-ability" collapsed two anti-correlated signals — 5-minute screen-share appeal and 45-minute hiring-loop conviction. C3's advantage lived almost entirely in the first; the job offer lives in the second. Re-scored with the split column, C2 wins.

**Decisive arguments:**
1. *"M7's exercise is already a thin C2"* (Grok) — the curriculum capstone (golden dataset + champion/challenger on a real agent) is the build's week-4 starting artifact. C2 continues the curriculum; C3 forks it.
2. C2's weakness (hard to feel quickly) is solvable — a 2-min walkthrough: production trace → failure → dataset addition → challenger run → holdout regression caught → shipped. C3's "toy" weakness is not solvable in the B2B-heavy segment Sean is targeting.
3. All four models predicted C3's scenario engine eats the 5-week budget and its eval harness becomes "a simulation of rigor about a simulation."

**The teaching layer (C3's energy, preserved):** the cockpit ships with a playable "how a PM uses this" walkthrough — Sean's game/frontend craft as the *teaching layer of a real tool*, not the artifact itself.

**Standing condition (Opus dissent):** if the target-company list shifts consumer/creative/games-heavy (>5 of top 15), the C3 case reopens. Current pipeline (Clipboard, Crunchbase, Makai) is B2B-leaning, consistent with C2.

**Falsification pass still owed before week-4 build start:** 5-tool teardown of adjacent incumbents (Braintrust, Langfuse datasets, promptfoo, Statsig, Freeplay) to sharpen the PM-grade-vs-dev-grade differentiation; optionally show the C2 mock to 2–3 recent AI-PM hiring managers.
