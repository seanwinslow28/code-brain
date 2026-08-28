---
title: Curriculum Map — Systems Thinking AI PM (v2, council-revised, LOCKED)
type: curriculum
status: locked (Sean, 2026-08-16)
created: 2026-08-16
revised: 2026-08-16 (council pre-mortem folded — see ../2026-08-16-council-premortem-curriculum-and-candidate.md)
inputs:
  - research/2026-08-16-last30days-practitioner-discourse.md
  - ../research/2026-08-16-what-do-the-academic-literature-and-authoritative-practition.md (Gemini DR)
  - ../research/2026-08-16-ai-product-post-launch-loops-pm-idea-ledger.md (discovery)
  - ../2026-08-16-council-premortem-curriculum-and-candidate.md (premium council, 4 models)
---

# Curriculum Map v2 — council-revised

**v1 → v2 surgery (all four council models aligned):**
- **M3 (archetypes) folded into M2 + M4** as a pattern library — archetype recognition is cheaper than a module; the freed slot funds the biggest gap.
- **New M3: Cost, Latency & Unit Economics as System Variables** — the council's #1 missing topic, "table-stakes AI PM work in 2026," previously absent.
- **Organizational/stakeholder systems** made first-class inside M5 (stakeholder-incentive CLDs, winning the meeting where the fix gets resourced).
- **HITL design** made first-class inside M6 (when/where to insert humans, confidence thresholds, escalation UX, reviewer drift).
- **Decision policies** added to M5 (ship/no-ship with thresholds, rollback triggers, written decision records — "diagnosis without disposition is academic").
- **Metrics architecture** added to M7 (offline/online/guardrail/business/trust; proxy choice that won't Goodhart; threshold setting).
- **Prediction-before-exercise, every module:** before diagnosing, Sean writes predicted mechanism, time horizon, falsifier, expected side-effects — then diagnoses, then gets Claude critique, then calibrates against the prediction. Moves exercises from lexical to judgmental.
- **Honest gates:** week 3 = *fluency* (vocabulary + recognition). *Judgment* is gated at week 6+ via spaced re-quizzes, cold-case drills during build weeks, and build decisions that cite concepts correctly. The v1 "second nature by week 3" claim contradicted its own spaced-retrieval pedagogy.
- **Curriculum feeds the product:** M7's capstone exercise IS the seed of the C2 build (golden dataset + champion/challenger round on a real agent). No forked effort.

## Modules (7, weeks 1–3, then drilled through week 8)

| # | Module | Anchor concepts | Case anchor | Exercise (prediction-first, real system) |
|---|--------|----------------|-------------|------------------------------------------|
| M1 | Systems Thinking Foundations | stocks/flows, reinforcing vs balancing loops, delays, Meadows' leverage points (shallow→deep), iceberg model | OpenAI Nov-2023 board crisis through the iceberg | Iceberg-model a real fleet incident (e.g., the 2026-04 agent downsizing) — predict the structural cause before digging |
| M2 | AI Product Feedback Loops **+ archetype pattern library I** | data flywheels, model/concept drift, degenerate loops & performativity, RLHF reward hacking & distribution shift; *fixes-that-fail, shifting-the-burden as AI loop patterns* | Zillow Offers ($881M concept-drift + adverse-selection collapse) | CLD one 16BitFit/portfolio loop; predict where drift or adverse selection enters, then trace it |
| M3 | **Cost, Latency & Unit Economics as System Variables** *(new)* | cost-quality-latency triangle, token economics, routing/caching loops, verification tax as $/quality-point, latency budgets, cost caps as balancing loops | "The bill goes down, the quality goes down with it, and you find out from customer tickets two or three days later"; Sean's own fleet cost-cap architecture | Model the unit economics of one of Sean's paid pipelines (discovery/DR/council caps) as stocks & flows; find the loop that would blow the budget if uncapped |
| M4 | Causal Loop Diagramming & Systems Mapping **+ archetype pattern library II** | CLD notation/polarity, stock-and-flow modeling, boundary setting, delayed feedback; *success-to-the-successful, limits-to-growth as mapping drills* | Unity fee-per-install (exogenous shock); Knight Capital (open-loop automation) | Full systems map of the Code-Brain fleet **including a stakeholder-incentive CLD** — the map becomes a portfolio artifact; N=3 mapping drills with decreasing scaffolding |
| M5 | Second-Order Effects, Organizational Systems & Decision Policies | 2nd/3rd-order mapping, Goodhart's law, verification tax, model monoculture, cognitive offloading; **stakeholder/org leverage points (winning the resourcing meeting)**; **kill criteria, rollback triggers, written decision records** | Air Canada / NYC MyCity (epistemic uncertainty → liability); the pre-mortem that predicts who blocks the fix | Pre-mortem a real upcoming change ending in a **ship/no-ship disposition with thresholds**, plus the org map of who must say yes |
| M6 | AI Architecture as Systems: the Harness **& HITL Design** | model→harness (planning × context × evals), RAG as system, long-horizon context decay, multi-agent commons dynamics; **where/when to insert humans, confidence thresholds, escalation UX, reviewer drift & fatigue** | "There is no compiler for PRDs"; Zillow as HITL-removal disaster | Diagram agents-sdk as a harness; identify the weakest loop AND design its HITL insertion point (threshold + escalation path) |
| M7 | Evals, Metrics Architecture & Loop Engineering *(capstone → C2 seed)* | evals as PM-core; loop anatomy (goal/context/evals/memory/guardrails/stop); champion/challenger + holdouts; weak-judge Goodharting; epistemic vs aleatoric uncertainty; golden datasets (build/version/maintain); **metrics architecture: offline/online/guardrail/business/trust; proxy selection; threshold & stop-the-line criteria**; offline↔online gap; diagnosis over delivery | Rechat "whack-a-mole" (Hamel Husain); champion-loop holdout-regression story | **The C2 seed:** build a 25/15 golden dataset + binary rubric for one real agent (job-feed relevance), run one champion/challenger round, write the decision record. This artifact carries directly into week 4 |

## Cadence & gates

- **Week 1:** M1 + M2 · **Week 2:** M3 + M4 · **Week 3:** M5 + M6 + M7 (M7 last — it hands off to the build)
- Per module: audio overview (source-selected, never whole-notebook) → quiz ≥80% → prediction-first exercise → Claude critique + calibration → spaced re-quiz ~1 week later
- **Week 3 gate (fluency):** narrate one fleet decision in systems vocabulary, cold
- **Week 6 gate (judgment):** cumulative cold-case quiz (unfamiliar incident, no scaffolding: name mechanism, loop, leverage point, disposition) + build decision log audited for correct concept citations
- **Build weeks 4–8 carry weekly 20-min archetype cold-read drills** (one unfamiliar public AI incident each week) so recognition→generation keeps compounding after the curriculum weeks end

## Feedback honesty rule

Claude is the default reviewer but rewards coherent explanation, not decision quality (council: Gemini). Counterweights: prediction-first calibration (the falsifier is written before the diagnosis), spaced cold-cases with objective answer keys, and the build's decision log — where reality, not Claude, grades the call.
