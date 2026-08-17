---
title: AI PM System Design Thinking — Curriculum Map (DRAFT v1, pre-council)
type: curriculum
status: draft — awaiting adversarial council critique
created: 2026-08-17
owner: Sean Winslow
supersedes: prj-ai-pm-system-thinking-strategy (2026-08-16, retired — see below)
---

# Curriculum Map — DRAFT v1

## Who this is for (calibration — this drives everything)

Sean Winslow. Media background, fell into AI Feb/March 2025, transitioned toward product. **No engineering background, but substantial hands-on tacit skill**: runs a 12-agent autonomous fleet in production with circuit breakers, fail-closed cost guards, hybrid model routing, budget caps, grounding-verification gates, and quality gates with rejection telemetry — **all built by instinct, none of it by name.**

The gap is **vocabulary, structure, and articulation — not knowledge.** He can build these things and cannot yet say what they are called or defend them in a room.

Pedagogical consequence (evidence-backed, see §Research):
- Never explain what an agent or a harness *is*.
- Do give canonical names, crisp repeatable definitions, and provenance.
- **Never reference a company, incident, or paper without a one-sentence setup.** This was the documented failure of the retired curriculum's M1 audio.
- The expertise-reversal effect means concurrent narration *degrades* his performance. Train retrospective articulation first; add time pressure deliberately and later.

## Why the previous program was retired

The 2026-08-16 program (7 modules, 28 artifacts, notebook `0abf9bb0`) was consumed at M1 and rejected. Three defects, in Sean's words plus evidence:

1. **Too abstract.** Its architecture module taught RAG as "retrieval quality is measurable" — true, and insufficient to draw a pipeline.
2. **No human half.** Zero design-thinking content despite the seed doc's Design Thinking × Systems Thinking thesis.
3. **Exercises pointed inward.** Every exercise ran on his own fleet, so nothing transferred.

Retired, not deleted. Notebook `0abf9bb0` and the prior research are preserved and reusable.

## The evidence base

| Source | Answers | Tier |
|---|---|---|
| Gemini DR Max, 2026-08-17 (4 literatures: process models, RE4AI, human-AI interaction canon, ML technical debt) | **What to decide** | 41% A / 38% C / 16% D (floor — auditor misclassifies IEEE TSE as trade) |
| Gemini DR, 2026-08-17 (failure-analysis frameworks, failure taxonomies, expertise research, assessment) | **What breaks** | 31% A / 56% C / 8% D. §1–3 trustworthy; **§4 (interviews) is vendor SEO — hypothesis only** |
| Nate B Jones, Executive Circle (3 posts) | **What to build, and how to audit it** | Practitioner-primary; plumbing post explicitly labels confirmed / inferred / hypothesis |
| last30days + WebSearch (interview assessment) | **Failed** — no primary discourse exists at this specificity. Vendor convergence only | D |

Verified primary artifacts to pull into the notebook:
- Amershi et al., *Guidelines for Human-AI Interaction*, CHI 2019 — 18 guidelines, validated with 49 practitioners against 20 products
- Sculley et al., *Hidden Technical Debt in ML Systems*, NeurIPS 2015 — CACE, glue code (95%+ of mature ML codebases), pipeline jungles, undeclared consumers
- *A Systematic Taxonomy of Failure Modes in RAG Systems*, ACL TrustNLP 2026 — 33 modes / 7 stages, evidence-graded; **12 modes have no peer-reviewed evidence, all 8 agentic modes among them**
- Microsoft, *Taxonomy of Failure Modes in Agentic AI Systems v2.0*, June 2026 — 12 months of red-teaming deployed systems
- Amershi et al., *Software Engineering for ML: A Case Study*, ICSE 2019 — 9-stage workflow
- Hydari, Iqbal & Ramasubbu, *Modeling Agentic Technical Debt and Stochastic Tax*, arXiv 2026 — debt is a stock, tax is a flow (fresh preprint, not settled canon)

## The method (what Sean carries in his head)

Four commitments. Run **forwards** to design a system; run **backwards** — *which of these did they skip?* — to tear one down.

| Commitment | Plain words | The questions |
|---|---|---|
| **Intent** | what it's for | Quantifiable objective? Does this genuinely need probabilistic AI, or would rules do? What does a false positive cost vs. a false negative? What's the error budget, and is it on a dashboard? |
| **Ground** | what it knows | Provenance, freshness, representation, structural bias. Is the *reasoning* documented — why these sources, why this model? |
| **Contact** | how people meet it | How does it communicate uncertainty to **calibrate** trust rather than maximize it? Were failure states prototyped Wizard-of-Oz **before** training? |
| **Consequence** | what it sets in motion | Who is the undeclared consumer? What hidden feedback loops are we creating? How do we pay the ongoing operating burden? |

Derived from the DR Max ordered decision procedure (4 phases, 9 questions), which is itself grounded in CRISP-ML(Q), the RE4AI literature, the Amershi guidelines, and Sculley's anti-patterns.

**Interrogation lenses** (the "what breaks" toolkit, used inside Consequence and in every teardown): **lifecycle** (ML-FMEA), **boundaries** (ASTRIDE — prompt injection, context poisoning, unsafe tool use), **emergence** (STPA — multi-agent hazards no single component causes).

## The eight modules

Four weeks of curriculum, two modules per week, then four weeks of build.

| # | Module | What Sean can draw afterward | Real anchor (never his fleet) | Debate episode |
|---|---|---|---|---|
| M1 | **Intent & Error Economics** | the error-cost table; the "should this be AI at all" call | Amazon's scrapped résumé screener | ship at 85%, or don't ship |
| M2 | **Ground: Context & Retrieval** | a full RAG pipeline with the failure mode at every hop | Perplexity | RAG vs. fine-tune vs. long context |
| M3 | **Orchestration** | the agent loop with stop conditions; the head/tail routing map | Cursor; Harvey | agents vs. workflows |
| M4 | **The Harness** | the plumbing diagram: registry, permissions, session + workflow state, budget checks, stop reasons | Claude Code (leaked source analysis) | autonomy vs. deterministic checkpoints |
| M5 | **Contact: The Trust Surface** | the state machine of a low-confidence answer; the five relationship pairings | Intercom Fin; Copilot accept/reject | show confidence scores, or hide them |
| M6 | **Evaluation & Guardrails** | the eval plan, from day-one invariants to golden datasets | Rechat (Hamel Husain) | LLM-as-judge vs. human eval |
| M7 | **Cost, Latency & Scale** | the cost and latency budget per hop | published routing/caching architectures | cheap-model routing vs. one good model |
| M8 | **Consequence: Drift & Operations** | the drift detection and response plan | Zillow Offers autopsy | automate retraining vs. gate it |

Design thinking is load-bearing at **M1** (whose pain, what a wrong answer costs, who bears it) and **M5** (trust calibration, uncertainty communication, failure prototyping) — the two places it does real work, not a module that gets skipped.

### M4 detail (the module the retired curriculum entirely lacked)

Taught in Nate's build order, because sequencing is the lesson:

- **Day one:** tool registry (metadata before implementation) · permission system with trust tiers · session persistence that survives crashes · **workflow state and idempotency** (conversation state ≠ task state) · pre-turn token budget checks · structured streaming events · system event logging · **a basic invariant test suite**
- **Week one:** tool pool assembly · transcript compaction · permission audit trail · the `/doctor` pattern · staged boot · stop-reason taxonomy · provenance-aware context assembly
- **Month one:** agent type system · memory with provenance · skills/extensibility

Anchor anecdote: Claude Code's `autoCompact` retried indefinitely on failure — one session failed 3,272 consecutive times, silently burning tokens. The fix was three lines. **Three lines of budget guardrail, missing from a $2.5B product.**

Governing principle: *"The most common mistake isn't under-engineering. It's over-engineering — building multi-agent coordination before you have a working permission system."*

## How each module runs

**Mirror → gym → calibrate.**

1. **Mirror (recognition, ~20 min).** Opens on something Sean already built, named. *You set `fallback = "none"` on the Tier C route so an off-hours miss raises `RouteUnavailable` instead of falling back to paid Claude. That's a fail-closed degradation policy — you chose cost safety over availability, which is an explicit SLO trade-off.* Fast, motivating, supplies the vocabulary.
2. **Predict (written, before anything else).** Predicted mechanism, expected failure, falsifier. Written before the teardown, so calibration is possible.
3. **Gym (transfer).** Teardown and design work on an **unfamiliar real product**, never his fleet. This is the half the retired curriculum lacked.
4. **Constraint-shift drill.** Mid-exercise, one constraint changes — traffic 10×, latency budget halves, the vector store goes down, the data becomes regulated — and he re-derives live. This is the documented discriminator between real and memorized competence.
5. **Calibrate.** Compare against the prediction. Claude critiques structure, not correctness.

## Verbal training (the piece both prior designs missed)

Knowing it and saying it fluently are different skills, and only one is graded. The research is explicit: concurrent narration degrades expert performance (success 47% → 37%), and the expertise-reversal effect makes it worse for practitioners running on automated routines. So the ramp is deliberate:

| Weeks | Mode | Why |
|---|---|---|
| 1–2 | **Retrospective, untimed.** Design in silence, then narrate the finished design. | Lowest cognitive load; builds vocabulary and structure without the dual-task penalty |
| 3–4 | **Retrospective, timed.** Same, against a clock. | Introduces pressure on delivery only, not on reasoning |
| 5–8 | **Concurrent, timed, interrupted.** Narrate while designing; Claude interrupts with constraint shifts. | Pressure Training (meta-analytic g = 0.77) — the interview condition, trained last |

Delivery rules, from the articulation research: achieve conceptual clarity **before** speaking; use the structural roadmap (the four commitments) to prevent information dumping; **name the pattern once, then explain it in plain words.** Glossary-dumping is the novice signal; naming-then-plain-explaining is the expert one.

## Gates

- **Week 4 — fluency.** Narrate the four commitments cold against an unfamiliar product, retrospectively, in under 10 minutes.
- **Week 6 — judgment.** Cold teardown of an unfamiliar real product, concurrent narration, with two constraint shifts injected, ending in a ship/no-ship disposition with thresholds.
- **Weekly during build:** one 20-minute cold teardown of an unfamiliar product.

Success criterion, in Sean's words, verbatim: *look at any AI product or regular product and fully envision how it runs under the hood, what could go wrong, how to fix it, and how to apply judgement — out loud, cold, unrehearsed.*

## Audio design

Three episodes per module plus a spaced re-listen:

1. **Pre-brief** (~5 min, `--format brief`) — every term defined in plain language before it appears in context. Generation instruction states Sean's actual calibration: deep hands-on agent experience, missing formal vocabulary; never explain what an agent is; **never reference a company or paper without a one-sentence setup**; name the running product in the first 30 seconds.
2. **Deep-dive** (long, `--format deep-dive`) — the module, anchored to one real product throughout.
3. **Debate** (`--format debate`) — the module's core trade-off argued honestly both ways. Trade-offs are the substance of system design; hearing the argument run both directions is what makes it runnable.
4. **Spaced re-listen** of the pre-brief roughly a week later.

Complement: local TTS (Kokoro, $0) narrating Sean's **own** design docs and decision log back to him — a different function from absorbing new material.

## Notebook policy

New notebook `bcb4e6aa` ("System Design Thinking for AI PM"). Seeded with the Google AI Search doc plus 5 hand-picked YouTube sources.

- **No bulk research imports.** The retired notebook took 83 sources in one deep-research import and graded 17% A / 60% C / 20% D. Every source here is hand-vetted and tier-labeled before entry.
- 8–12 sources per module, named `M<N> — <title>`, tracked in `notebooklm/source-manifest.md`.
- Source-selected generation always (`-s`), never whole-notebook.

## Portfolio

**Golden Loop** survives from the retired program — it was not among the rejected elements. Eval-first golden-dataset cockpit with a playable teaching layer; chosen 3–1 over an AI PM flight simulator by a 4-model council pre-mortem. M6's capstone is its seed artifact. Product docs to move from the retired project.

## Budget

$9.80 of $15–25 spent (DR $2.80 + DR Max $7.00). Gemini monthly cap nearly exhausted ($18.20 of $20) — **no further Gemini DR until September.** Remaining: council critique gate (~$0.80), then hand-curation at $0.

## Open questions for the council

1. Is the four-commitment method the right spine, or does it omit something load-bearing?
2. Is eight modules in four weeks at 5–8 hrs/week honest, or is it the same over-scoping that killed the last program?
3. Does the mirror/gym split actually produce transfer, or does opening on his own systems re-anchor him to them?
4. Is the retrospective-first verbal ramp right, given he needs concurrent performance in interviews within weeks?
5. What is missing entirely?
