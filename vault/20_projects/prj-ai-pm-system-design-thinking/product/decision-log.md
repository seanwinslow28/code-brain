---
title: Golden Loop — Decision Log
type: decision-log
status: active
created: 2026-08-17
convention: every significant decision gets an entry — decision, alternatives, expected mechanism, the systems concept applied (by name), falsifier, review date. Public-facing; written to be read by a hiring manager.
---

# Golden Loop — Decision Log

> **What this is.** The running record of every significant product decision in the Golden Loop build, each one citing the systems-thinking concept it applies, the alternatives it beat, and — most importantly — what evidence would prove it wrong. Entries are append-only; a reversed decision gets a new entry pointing back, never an edit.

---

## D0 — Product choice: C2 "Golden Loop" over C3 "AI PM Flight Simulator" (2026-08-16)

- **Decision:** Build the eval-first cockpit (C2), with the flight-simulator energy preserved as a playable teaching layer inside it.
- **Alternatives:** C3 flight simulator (original scorecard leader), C1 silent-failure radar, C4 launch gate.
- **Mechanism:** A 4-model council pre-mortem voted C2 3–1 and exposed a scorecard bug — "recruiter demo-ability" had collapsed two anti-correlated signals (5-minute screen-share appeal vs 45-minute hiring-loop conviction). Re-scored with the split, C2 wins. Decisive argument: the curriculum's M7 capstone *is already a thin C2* — C2 continues the work, C3 forks it.
- **Systems concept applied:** Goodhart's law on the scorecard itself — the demo-ability column was a proxy metric being optimized at the expense of the goal it proxied.
- **Falsifier:** If the target-company list shifts consumer/creative-heavy (>5 of top 15), the C3 case reopens.
- **Review:** At Phase C wayfinder ratification. Full record: [candidate-scorecard.md](candidate-scorecard.md).

## D1 — Sharpest wedge: the PM on a team with existing trace tooling (2026-08-16)

- **Decision:** v1 is built for the PM on a team that already logs AI traces in an existing observability tool (Langfuse/Braintrust-class). Golden Loop imports those traces and adds the PM-grade decision layer on top: failure → golden-dataset item → champion/challenger round with holdout → written promote/reject decision.
- **Alternatives:** (a) solo PM instrumenting one feature, dogfooded end-to-end (the session recommendation); (b) PM+engineer pair with a shared handoff surface.
- **Mechanism:** Positioning v1 inside a team's real stack makes the artifact legible as company-scale product work rather than a personal tool, and forces the builder through the integration realities (schema mapping, API contracts, ecosystem positioning) that a self-contained build never touches. Dogfooding survives via self-hosting the upstream tool (see D2), so the demo remains lived, not staged.
- **Systems concept applied:** Boundary setting (M4) — deliberately drawing the system boundary to *include* the team's existing tooling, accepting external dependency as the cost of building at the real system's scale.
- **Falsifier:** The Phase B five-tool teardown. If Braintrust/Langfuse/promptfoo/Statsig/Freeplay already serve the PM decision layer well, the wedge is dead and the question reopens — that verdict gets its own entry here either way. Secondary falsifier: 2–3 recent AI-PM hiring managers decline to "forward it to a peer" on the mock.
- **Review:** End of Phase B, before any code.

## D2 — Data ingress: Langfuse-first live import over a neutral internal format (2026-08-16)

- **Decision:** v1 ships exactly one live integration: self-hosted open-source Langfuse receives real agent traces; Golden Loop imports flagged failures via the Langfuse public API. Internally, every trace is normalized into one neutral JSONL format (aligned to OpenTelemetry GenAI conventions), so a manual file-drop door falls out nearly free and additional importers become adapters, not rewrites.
- **Alternatives:** (a) Braintrust-first import (closed-source, cloud-dependent dogfood, and the incumbent whose PM-layer gap is most suspect — awkward to build *on* the tool v1 differentiates *from*); (b) file-drop only, no live integration (defers the integration proof the wedge exists to demonstrate).
- **Mechanism:** One importer done well honors the council's "one hard thing done well" warning. Langfuse is the only major incumbent that is open-source and self-hostable, which keeps dogfooding honest and free. The neutral internal format decouples the product from upstream schema churn.
- **Systems concept applied:** Buffering and decoupling (M1 stocks-as-shock-absorbers) — the neutral format is a buffer stock between an external flow we don't control (Langfuse's schema) and the system that depends on it.
- **Falsifier:** If Langfuse integration exceeds ~1 week of the 5-week build budget, or self-hosting proves impractical, fall back to file-drop-first and log the reversal here.
- **Review:** End of build week 1.

## D3 — Teaching layer: "SHIPWRECK with a holdout title-fight beat" (2026-08-16)

- **Decision:** The playable teaching layer is a failure-first arc: the visitor ships an AI change with no process, watches ~15–20 seconds of handcrafted consequence (with the rewind affordance visible early), rewinds, then redoes the workflow as micro-interaction stations where each completed step visibly erases a specific consequence from the disaster they caused. One structural addition to the sourced concept: in the eval/validate station, the visitor's chosen change goes green on the visible test set — and the holdout catches a regression; one honest, smaller retry passes both. Stations are styled to mirror the real cockpit UI.
- **Alternatives:** 20 options from a 4-frame divergence run (isolated generators + critic), 5 concepts from an independently-generated design document, and 7 earlier proposals — including a physics-toy centerpiece (Curtained Plinko, the machine critic's lean) and a real-data replay challenge ("Beat the PM"). All logged in the Phase A session record.
- **Mechanism:** Two fully independent generation processes converged on the failure-first shape — treated as replication. The added holdout beat exists because, across all 27 candidates, the single deepest lesson was the same: the moment that changes how a PM thinks is when the visible metric goes green and the hidden set says no. As sourced, SHIPWRECK narrated that lesson; the merge makes it *felt*. Cockpit-mirroring stations make the teaching layer transfer to the product instead of decorating it.
- **Systems concept applied:** Goodhart's law (M5), made experiential — the visible test set is the proxy, the holdout is the goal, and the teaching beat lets the visitor personally overfit and get caught. Constraint honored: handcrafted scenarios only, no LLM scenario generation (the council's unanimous budget-eater warning).
- **Falsifier:** If the playable build exceeds ~2 part-time weeks, or cold playtesters bounce before the rewind, cut to the guided-walkthrough fallback and log it.
- **Review:** At teaching-layer build start (≈week 6) and after first 3 cold playtests.

## D4 — Name: Golden Loop stays (2026-08-16)

- **Decision:** Product and future repo keep the working title: Golden Loop / `golden-loop`.
- **Alternatives:** "Holdout" (names one mechanism, weak searchability), "Title Fight" (reads sports-first to a cold B2B visitor).
- **Mechanism:** The name states both halves of the product (golden dataset + closed improvement loop) in two words, and every existing artifact already carries it.
- **Systems concept applied:** Leverage points (M1) — naming is a parameter-level intervention, the shallowest rung; effort belongs on the deeper rungs (structure, information flows) that the other decisions touch.
- **Falsifier:** Phase B collision check (GitHub/npm/product search). A live product with the same name in the eval space forces a rename before the repo is created.
- **Review:** At repo migration (Phase E).

## D5 — Build-in-public cadence: decision log + two milestone posts (2026-08-16)

- **Decision:** This log is the continuous public narrative. Exactly two Substack posts sit on top of it: one after the Phase B falsification verdict (the five-tool teardown story), one at ship (the case study, adapted).
- **Alternatives:** (a) decision log only — all narrative value arrives at week 8; (b) weekly build-log — 5–6 posts.
- **Mechanism:** There are exactly two moments in this build where a reader gets something they can use: the teardown verdict and the shipped loop. A weekly cadence would spend scarce build hours (5–8 hrs/week total) producing posts that fail the value gate; the teardown post is also shareable mid-job-hunt rather than only after ship.
- **Systems concept applied:** Stocks and flows (M1) — reader attention is a finite stock; posting is a flow matched to genuine value events rather than to the calendar.
- **Falsifier:** If a third genuinely transferable moment emerges mid-build (plans are starting points, not walls), add it and log the change here.
- **Review:** At ship.

## D6 — Phase B research spend: light spend now, reserve held for the systems-map gate (2026-08-16)

- **Decision:** Phase B runs on: the five-tool teardown in-session at $0 (web research + free tiers), one research-shaped Gemini Deep Research run (~$3) for competitive grounding, and the hiring-manager mock test (2–3 recent AI-PM hiring managers, "would you forward this to a peer?"). The remaining ~$8–15 of research budget is reserved for a second council pre-mortem at the Phase D systems-map/PRD gate.
- **Alternatives:** (a) $0-only path (skips the mock test — the council's single highest-EV recommendation); (b) full deploy now (DR Max + immediate second council run — fires the expensive critique before a map or verdict exists to critique).
- **Mechanism:** The teardown is free where it matters; money buys grounding only where free tools can't reach; and high-variance multi-model critique pays most when there is a concrete artifact to attack.
- **Systems concept applied:** Value-of-information timing (M5 decision policies) — spend on information when it changes a decision; hold reserve capacity for the decision point where it will.
- **Falsifier:** If the $0 teardown + $3 DR leave a material unknown that blocks the falsification verdict, escalate to DR Max from the reserve and log the escalation.
- **Review:** At the Phase B falsification verdict.

## D7 — Falsification verdict: build, on the re-scoped wedge (2026-08-17)

- **Decision:** Proceed with the build. The wedge is re-scoped from "the PM's eval lab" (falsified — Braintrust, Langfuse, and Freeplay already ship no-code trace→dataset labs, Freeplay marketing directly to PMs) to **the discipline layer no lab ships**: sealed holdout splits, enforced one-change promotion rounds, and required promote/reject decision records for offline evals. All v1 positioning, the PRD, and the teaching layer lead with the discipline, never with dataset-building.
- **Alternatives:** The pre-registered alternative was killing the project — "if the teardown kills the gap, say so plainly and reopen the candidate question." It did not: across 15 named incumbents checked against primary sources (5 deep teardowns + 10-candidate second-ring sweep), none ships even one of the three discipline features in full. Near-misses disclosed in the verdict: Phoenix (split labels without sealing), Confident AI (one-variable advice without structure), Vellum (deployment approvals without eval-linked rationale).
- **Mechanism:** The incumbents' own material admits the problem while not productizing the answer — promptfoo warns its own users about overfitting without a split; Braintrust's blog hand-builds holdouts its product can't express; Statsig ships real decision records but only for online experiments. The discipline pattern is proven in classic MLOps (champion/challenger with approval gates) and simply un-ported to LLM offline evals. Meanwhile the field is consolidating under platform agendas (OpenAI acquired promptfoo and Statsig's team inside twelve months; Anthropic acqui-hired Humanloop, which shut down) — leaving the vendor-neutral, PM-first seat emptier than a year ago.
- **Systems concept applied:** Pre-registered falsification (M5 decision policies) — the kill condition was written into D1 before any evidence was gathered, and the verdict was produced by trying to lose. Secondary: shifting the burden (M3 pattern library) — every incumbent shifts the discipline burden to user convention; Golden Loop moves it into structure, where M1's leverage-point hierarchy says it belongs.
- **Falsifier:** Two standing tripwires. (1) Shelf life: if any incumbent ships all three discipline features before Golden Loop's week-8 ship, the differentiation section of the case study is rewritten around being early rather than alone — checked at each phase gate. (2) Demand: if the hiring-manager mock test (D6) returns "wouldn't forward it to a peer" from a majority, the wedge is a feature gap without buyer pull, and the positioning question reopens before the PRD locks.
- **Review:** At Phase C wayfinder ratification, and again at the Phase D PRD gate. Full evidence: [../research/2026-08-17-phase-b-falsification-verdict.md](../research/2026-08-17-phase-b-falsification-verdict.md) + per-tool citation files in [../research/teardowns-2026-08-17/](../research/teardowns-2026-08-17/).

---

*Provenance: D1–D6 were decided in the Phase A partner-walkthrough session (2026-08-16); options, rejected alternatives, and the full deliberation are preserved in the session record. D0 predates this log; its full record is the candidate scorecard. D7 records the Phase B falsification verdict (2026-08-17).*
