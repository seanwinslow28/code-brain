---
title: Curriculum Map — Systems Thinking AI PM (v1, research-refined)
type: curriculum
status: draft-for-sean
created: 2026-08-16
inputs:
  - research/2026-08-16-last30days-practitioner-discourse.md
  - ../research/2026-08-16-what-do-the-academic-literature-and-authoritative-practition.md (Gemini DR, $2.80, tier mix 17%A/60%C/20%D — A-tier claims weighted, trade claims treated as leads)
  - ../research/2026-08-16-ai-product-post-launch-loops-pm-idea-ledger.md (discovery)
---

# Curriculum Map v1 — research-refined

**Change from the spec's draft:** research promoted one new module (M7) and materially reshaped M2, M3, M5, M6. Weeks 1–3 now carry 7 modules (2–3/week). Every module keeps the audio-first artifact set (audio overview, quiz, flashcards, mind map, study guide) + one real-system exercise.

**Pedagogy findings that shape the mechanics (evidence-backed, DR Part III):**
- **Spaced retrieval practice** beats massed consumption — so quizzes/flashcards are re-run on a spaced schedule (fresh quiz at module close, retrieval quiz ~1 week later, cumulative quiz at week 6), not one-and-done. Validates the audio+flashcard loop Sean already planned.
- **Management flight simulators** are the strongest documented way to build systemic judgment — the Phase 2 build *is* the simulator, and M4's exercise adds a small simulated-loop exercise so consequences of interventions are felt, not read.
- **Cognitive offloading warning**: using AI purely for speed atrophies the judgment being trained. Exercises therefore require Sean's own diagnosis first, AI critique second.

## Modules

| # | Module | Anchor concepts | Case anchor | Exercise (real system) |
|---|--------|----------------|-------------|------------------------|
| M1 | Systems Thinking Foundations | stocks/flows, reinforcing vs balancing loops, delays, Meadows' leverage points (shallow→deep), iceberg model | OpenAI Nov-2023 board crisis read through the iceberg (events→patterns→structures→mental models) | Iceberg-model a real incident from Sean's agent fleet (e.g., the 2026-04 agent downsizing: 8 of 10 agents producing no value) |
| M2 | AI Product Feedback Loops | data flywheels, model/concept drift, degenerate loops & performativity (rec systems, synthetic-text recursion), RLHF reward hacking & distribution shift | Zillow Offers: concept drift + adverse selection + HITL removal = $881M write-down | Draw the CLD of one 16BitFit or portfolio-site loop; identify where drift or adverse selection could enter |
| M3 | System Archetypes in AI Failures | fixes-that-fail, shifting the burden (prompt-engineering-as-symptomatic-fix), success-to-the-successful, limits to growth (data/energy ceilings, model collapse) | Unity fee-per-install (exogenous ecosystem shock); Knight Capital (open-loop automation, runtime awareness) | Written teardown of one public AI failure using an archetype template: name the archetype, the loops, the leverage point that would have prevented it |
| M4 | Causal Loop Diagramming & Systems Mapping | CLD notation & polarity, stock-and-flow modeling, boundary setting, mapping delayed feedback | Taiwan smart-medical-device ecosystem CLD (funding loops vs validation bottlenecks) | Full systems map of Sean's Code-Brain fleet: agents, caps, manifests, drift risks — the map that later becomes a portfolio artifact |
| M5 | Second-Order Effects, Pre-mortems & the Omitted Topics | second/third-order mapping, Goodhart's law, **verification tax & true ROI**, **model monoculture risk**, **cognitive offloading**, exogenous shocks | Air Canada / NYC MyCity: epistemic uncertainty → legal liability; the "verification tax" that flips AI ROI negative | Pre-mortem a real upcoming change (fleet or portfolio) mapping 1st/2nd/3rd-order effects; council pre-mortem cross-check |
| M6 | AI Architecture as Systems: the Harness | model→harness shift (planning × context × evals), RAG as a system, long-horizon context decay, multi-agent dynamics & tragedy of the commons, observability/tracing | "There is no compiler for PRDs" — why learning loops break outside coding | Diagram Sean's own agents-sdk as a harness: where planning, context, evals, and stop conditions live; find the weakest loop |
| **M7 (new)** | **Evals & Loop Engineering** | evals as PM-core; loop anatomy (goal/context/evals/memory/guardrails/stop = target+budget+stall); champion/challenger with holdout sets; weak-judge Goodharting; **epistemic vs aleatoric uncertainty**; golden datasets (build/version/maintain); offline↔online gap; **diagnosis over delivery** | Rechat "whack-a-mole" case (Hamel Husain); champion-loop holdout-regression story | Build a 25/15 split golden dataset + binary rubric for one of Sean's own agents (e.g., job-feed relevance) and run one champion/challenger round |

**Why M7 earned promotion (module expansion rule):** it recurs across every independent research stream — r/ProductManagement threads, the Maven course ecosystem (Husain/Shankar), YouTube practitioner explainers, the DR competency map's "Evaluation & QA" domain, AND the discovery run's top pain ("AI quality is difficult to define and measure", 3 domains). No other candidate topic came close to that convergence.

**Folded rather than promoted:** verification tax, model monoculture, cognitive offloading → M5; epistemic uncertainty, golden datasets, diagnosis-over-delivery → M7; multi-agent commons dynamics → M6. Each recurred but shares mechanism and pedagogy with an existing module — a module is a coherent mental move, not a topic list.

## Weekly cadence (weeks 1–3)

- Week 1: M1 + M2 (foundations + AI loops)
- Week 2: M3 + M4 (archetypes + mapping practice)
- Week 3: M5 + M6 + M7 (judgment + architecture + evals) — M7 lands last deliberately: it's the bridge into the build, and its exercise (golden dataset + champion round) is the build's first real muscle
- Spaced retrieval: week-later quizzes for M1–M4 land in weeks 2–4; cumulative quiz at week 6

## Success gates per module

Audio listened → quiz ≥80% → exercise submitted → Claude review → spaced re-quiz passed. Vocabulary check at week 3: Sean narrates one fleet decision in systems vocabulary, cold.
