---
title: AI PM System Design Thinking — Curriculum Map (v2, council-revised, LOCKED)
type: curriculum
status: locked (Sean, 2026-08-17)
created: 2026-08-17
revised: 2026-08-17 — four-model council pre-mortem folded (2026-08-17-council-premortem-curriculum-map.md)
owner: Sean Winslow
notebook: bcb4e6aa-9da7-49fe-8c65-46d27110313e
supersedes: prj-ai-pm-system-thinking-strategy (2026-08-16) — retired, not deleted
---

# Curriculum Map v2 — LOCKED

## The calibration (read this before writing any lesson)

Sean Winslow. Media career, discovered AI Feb/March 2025, self-taught, transitioning into AI product management. No engineering background. Runs a 12-agent autonomous fleet in production — circuit breakers, fail-closed cost guards, hybrid model routing, budget caps, grounding-verification gates, quality gates with rejection telemetry — **all built by instinct, none of it by name.**

**The assumption that governs every module** (corrected by the council; the v1 draft got this wrong):

> The gap is vocabulary **plus the decision surfaces his production path never forced him to touch.** Each module must diagnose which is which. It may never globalize "he already knows this."

The v1 draft said *"the gap is vocabulary, structure, and articulation — not knowledge."* All four council models independently flagged that as flattering and false. Grok's correction is the one to remember: the expertise-reversal effect says *don't make experts sit through novice explanations*. It does **not** say experts already hold the full conceptual graph and merely need nouns. Building circuit breakers by instinct does not confer knowing when a circuit breaker is the wrong primitive versus a bulkhead, admission control, or deadline propagation.

Teaching consequences:
- Never explain what an agent or a harness *is*.
- Do give the canonical name, a crisp repeatable definition, and provenance.
- **Never reference a company, incident, or paper without a one-sentence setup.** This was the documented failure of the retired M1 audio.
- State per module whether his fleet actually forced that decision (see *Mirror eligibility* below). Where it did not, teach it as new — do not flatter.

## What the retired program got wrong, and how v2 differs

The 2026-08-16 program (7 modules, 28 artifacts, notebook `0abf9bb0`) was consumed at M1 and rejected: too abstract, no design-thinking half, exercises pointed only at his own fleet. Retired, **not deleted** — `0abf9bb0` holds $4.12 of paid research and stays available.

The council's warning about v2 is the one that matters: *"The retired program died at M1 from quality failure. This one dies at M5 from schedule collision. Same corpse, different wound."* Every structural choice below exists to prevent a second corpse.

## The spine

Ordered by **the kind of decision the PM must make**, not by system layer. Replaces the v1 draft's Intent/Ground/Contact/Consequence, which the council correctly diagnosed as a checklist with a story about directionality — no forced sequencing, kill criteria at only one step, and no home for evaluation or cost.

1. Problem / User / Workflow
2. Decision & Error Economics
3. Data / Feedback / Model Path
4. Architecture Choice Under Constraints
5. Interaction, Trust, Control, Escalation
6. Evidence / Evaluation / Telemetry / Rollout
7. Operations / Cost / Drift / Abuse / Ownership

**Intent · Ground · Contact · Consequence survives as a private review checklist only.** Sean is explicitly trained never to name it in a room. Named aloud it reads as bootcamp framework-pitch; senior interviewers are inoculated after two years of homemade frameworks. Used silently and delivered as concrete judgment, it works. The distinction is the whole lesson.

## The five modules

Eight weeks. Roughly a week and a half each. **Honest arithmetic: the curriculum consumes the eight weeks at 5–8 hrs/week.** Golden Loop is not shipped by week 8 — the five written artifacts *are* its planning spine, so by week 8 it is fully specified and partially built. Shipping lands weeks 9–12. The v1 draft's "four-and-four" was the same over-scoping that killed v1, arriving in a new costume.

| # | Module | Covers | Mirror eligibility |
|---|---|---|---|
| **M1** | **Problem, Users & Decision Economics** | forward design from a dirty brief · non-AI baseline · why AI, why now · false-positive vs false-negative cost asymmetry · thresholds, error budgets, kill criteria · **who actually gets hurt, and why teams ship anyway** · precision/recall, calibration, class imbalance | **Partial.** His fleet forced cost caps and fail-closed policy. It never forced him to name an error budget or elicit an FP/FN asymmetry from a stakeholder. |
| **M2** | **Data, Feedback & the Model Path** | where eval and training data come from · who labels and how well · how human feedback re-enters · how product decisions contaminate the distribution · data contracts, provenance, freshness, bias · retrieval as part of the data plane | **No, and say so.** Council's sharpest catch: agent fleets do not accidentally confer labeling-pipeline judgment. **This is the largest genuine hole.** Teach from zero. |
| **M3** | **Architecture Under Constraints** | RAG vs fine-tune vs long-context vs agent vs workflow, each with kill criteria · the 12 harness primitives in build order · determinism boundary, frozen vs variable · permissions and trust tiers · workflow state vs conversation state, idempotency · stop-reason taxonomy · **security and abuse as a first-class surface** | **Yes, strongest.** Nearly every harness primitive exists in his fleet unnamed. This is the module where the mirror genuinely earns its place. |
| **M4** | **Interaction, Trust & Control** | the five relationship pairings (Human↔Software / ↔LLM / ↔Agent / Agent↔Agent / Agent↔Software) · trust **calibration**, not maximization · communicating uncertainty · failure UX, recovery, escalation · HITL insertion points and reviewer drift · Wizard-of-Oz before building · Amershi's 18 validated guidelines | **No.** A single-operator fleet never forced a trust surface. Teach from zero. |
| **M5** | **Evidence & Operations** | instrumentation, unit of analysis, sampling for human review · day-one invariants → golden datasets → holdout hygiene · champion/challenger · LLM-as-judge failure modes · rollout, A/B, kill switches · drift types (covariate/label/concept) · **unit economics at product level, not per-hop** · org ownership, review boards, incident response | **Partial.** He has telemetry and budget caps. He has never run an experiment, set a rollout gate, or negotiated ownership with anyone. |

### Anchors — two per module, never one

The council flagged single-anchor fragility: the Claude Code "three lines missing from a $2.5B product" anecdote is catnip, and if the leaked-source story proves partial the emotional payload of that module collapses. Every module carries a backup.

| # | Primary anchor | Backup anchor | Debate episode |
|---|---|---|---|
| M1 | Amazon's scrapped résumé screener | clinical triage / diagnostic thresholds | ship at 85%, or don't ship |
| M2 | Zillow Offers (data + adverse selection) | content-moderation labeling pipelines | buy labels, or build the loop |
| M3 | Claude Code leaked-source primitives | Perplexity's retrieval architecture | agents vs workflows |
| M4 | Intercom Fin (published confidence + handoff) | GitHub Copilot accept/reject | show confidence scores, or hide them |
| M5 | Rechat (Hamel Husain) | published routing/caching cost architectures | LLM-as-judge vs human eval |

## How each module runs

**Diagnose → learn → gym → label → calibrate.** Note what changed: mirror-on-self is no longer the universal opener.

1. **Diagnose (2 min).** The module states whether Sean's fleet forced this decision. If yes, open on the thing he already built, named. If no, say plainly: *your fleet never made you solve this, so this is new.* The v1 draft's universal mirror reintroduced the retired curriculum's inward-pointing defect and would have masked exactly the gaps that matter from M4 onward.
2. **Predict (written, before anything).** Predicted mechanism, expected failure, falsifier.
3. **Gym — and half of them are forward design.** Alternating:
   - **Forward:** a dirty brief (*"40k support tickets, two engineers, compliance review in Q1 — what do we build?"*) → architecture out, with rejected alternatives, kill criteria, and a defended bet. **This is the most common AI PM interview format and v1 never practiced it once.**
   - **Teardown:** an unfamiliar real product, never his fleet.
4. **Label the mode.** In every teardown Sean states **observed / inferred / designed** for each claim. Public teardowns without ground truth otherwise become architecture fanfic, and the labeling is itself a maturity signal.
5. **Constraint-shift drill.** One constraint changes mid-exercise — traffic 10×, latency budget halves, the vector store dies, the data becomes regulated — and he re-derives live. The documented discriminator between real and memorized competence.
6. **Calibrate.** Against the prediction. Claude critiques structure and reasoning, not correctness.

### Written artifacts — one per module

Verbal training was scheduled to the hour in v1 while written articulation was assumed to fall out. It won't. Each module ships one real PM artifact, and all five double as Golden Loop's planning spine and as portfolio:

| Module | Artifact | Golden Loop role |
|---|---|---|
| M1 | PRD for an AI feature, with error economics and kill criteria | Golden Loop's PRD |
| M2 | Data contract + labeling plan | its golden-dataset spec |
| M3 | Architecture decision record with rejected alternatives | its systems map |
| M4 | Failure-UX spec + model card | **closes one of Grok's three gaps** |
| M5 | Launch criteria, cost model, incident runbook | **closes the other two** |

## Verbal training

No interviews booked (confirmed 2026-08-17), so the evidence-backed ramp stands. Concurrent narration degrades expert performance (success 47% → 37%) and the expertise-reversal effect makes it worse for practitioners running on automated routines — so the hard condition is trained last, deliberately.

| Weeks | Mode | Why |
|---|---|---|
| 1–3 | Retrospective, untimed — design in silence, then narrate the finished design | Lowest cognitive load; builds vocabulary and structure without the dual-task penalty |
| 4–6 | Retrospective, timed | Pressure on delivery only, not on reasoning |
| 7–8+ | Concurrent, timed, interrupted with constraint shifts | Pressure Training (meta-analytic g = 0.77); the interview condition |

**Override clause:** if an interview lands inside weeks 1–6, the ramp is abandoned immediately and concurrent practice starts that week. Training the wrong condition is worse than paying the expertise-reversal penalty.

Delivery rules from the articulation research: reach conceptual clarity **before** speaking; use the private checklist as a structural roadmap to prevent information dumping; **name the pattern once, then explain it in plain words.** Glossary-dumping is the novice signal.

## Gates

- **Week 4 — fluency.** Narrate a full system design for an unfamiliar product, retrospectively, under 10 minutes, labeling observed/inferred/designed throughout.
- **Week 6 — judgment.** Cold **forward design** from a dirty brief he has not seen, with two constraint shifts injected, ending in a ship/no-ship disposition with written thresholds. Forward, not teardown — because that is the failure mode v1 would have produced.
- **Weekly:** one 20-minute cold exercise, alternating forward and teardown.

**Success criterion, Sean's words verbatim:** *look at an AI product or a regular product and fully envision how it runs under the hood, what could go wrong, how to fix it, and how to apply judgement — out loud, cold, unrehearsed.*

## Audio

Three episodes per module plus a spaced re-listen. Generation instructions carry the calibration above verbatim — especially *never reference a company or paper without a one-sentence setup*, which is the specific defect that killed the retired M1.

1. **Pre-brief** (~5 min, `--format brief`) — every term defined in plain language before it appears in context; the running product named in the first 30 seconds.
2. **Deep-dive** (long, `--format deep-dive`) — the module, anchored to one real product throughout.
3. **Debate** (`--format debate`) — the module's core trade-off argued honestly both ways. Trade-offs are the substance of system design; hearing the argument run both directions is what makes it runnable rather than memorized.
4. **Spaced re-listen** of the pre-brief roughly a week later.

Complement: local TTS (Kokoro, $0) narrating Sean's **own** written artifacts and decision log back to him — a different cognitive function from absorbing new material.

## Sources

**3–5 hand-vetted sources per module, not 8–12.** The council caught that 8–12 × 8 modules is the same over-research pathology that graded the retired notebook 17% A / 60% C / 20% D, arriving under better labels. Everything beyond 5 goes to a reference list, not the notebook.

- **No bulk research imports**, ever.
- Named `M<N> — <title>`, tracked in `notebooklm/source-manifest.md` with a tier label.
- Source-selected generation always (`-s`), never whole-notebook.

**Evidence discipline.** Build on brick, label the rest:

| Tier | Sources | Use |
|---|---|---|
| **Brick** | Sculley (NeurIPS 2015) · Amershi ×2 (CHI 2019, ICSE 2019) · STRIDE · the ACL TrustNLP RAG taxonomy's *evidenced* modes | Teach as established |
| **Fresh** | Microsoft agentic taxonomy v2.0 (2026) · ASTRIDE (arXiv 2512.04785 — a *platform* paper; teach STRIDE + the agentic categories, not the tooling) · STRIDE-AI · Stochastic Tax (arXiv 2605.27320) | Teach as current, name the date |
| **Hypothesis** | The TrustNLP taxonomy's 12 unevidenced modes — **all 8 agentic modes among them** · anything from the DR's §4 on interview assessment (vendor SEO) | Label as unproven when spoken |

The v1 draft quoted the "evidence desert" finding approvingly and then built its agentic content on exactly that unvalidated part. Caught by the council; corrected here.

## Portfolio — Golden Loop

**Kept.** Sean's call 2026-08-17, and the partner session (`~/.creative-harness/partner-sessions/2026-08-16-golden-loop-kickoff.md`, local-only) largely answers Grok's "ML-engineer artifact" objection — which was made against a one-line description the council never saw. The session's PROPOSALS LOG format is itself a decision record with killed alternatives and Sean's verbatim reasoning at every axis.

Three additions, from the parts of Grok's list that were genuinely absent, all delivered as module artifacts:
1. **Cost model** — per trace, per eval round, and at 10k traces/month for a team (M5).
2. **Failure UX** — what the product does when the import breaks, the format drifts, a trace is malformed, or the judge is uncertain (M4).
3. **Ship gate with written thresholds** for Golden Loop itself (M5).

Framing rule: **the decision log is the front door, not an appendix.** The teaching layer is the hook; the log is the proof. The craft is the thing Sean is already known for — the judgment is the scarce signal.

Open from the session, worth closing early: whether the demo dataset dramatizes a fictional product or the real job-feed data. Fiction weakens the honesty story.

## Budget

**This program: $10.66 of $15–25** — Gemini DR $2.80, DR Max $7.00, council premium $0.86.

**Gemini fleet-wide caps** (operative values from `agents-sdk/config.toml` `[gemini.budget]`, which are **$50/month and $20/day** — not the $20/$10 code defaults quoted in the skill doc): month-to-date **$21.00 of $50**, today **$12.60 of $20**. Headroom exists; an earlier claim in this session that Gemini was exhausted until September was wrong and is corrected here.

Note the ledger's sixth August entry (2026-08-17 12:02 EDT, $2.80) was **not** run by this program — it is Golden Loop Phase B offline-evaluation research, matching the partner session's L7 budget line.

Remaining work here is $0 hand-curation, with reserve for one council run at the Golden Loop systems-map gate.

## What the council did not settle

- **How much non-AI CS fundamentals to add.** Gemini argued for databases/API gateways/monoliths; ranked lowest and judged misaimed for an AI PM. Adopted instead: Opus's version — non-generative ML and general product mechanics, installed in M1 and M5.
- **Whether Golden Loop should be replaced.** Only Grok raised it, against a prior 3–1. Resolved by inspection of the session rather than by vote.
