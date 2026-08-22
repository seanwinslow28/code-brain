# CONTINUATION PROMPT — AI PM System Design Thinking (paste into a fresh session)

> **Launcher:** start a fresh session in `/Users/seanwinslow/Code-Brain/code-brain` and say:
> *"Read `vault/20_projects/prj-ai-pm-system-design-thinking/CONTINUE-HERE.md` and pick up where we left off."*

**Written 2026-08-22, end of the session that built M1–M3.** Last commit: `2051ede`.

---

## 1. Who you're working with — read this before anything else

**Sean Winslow.** Media career, discovered AI around Feb/March 2025, taught himself, now transitioning into AI product management and job-hunting. **No engineering background.**

But he runs a **twelve-agent autonomous fleet in production** — circuit breakers, fail-closed cost guards, hybrid model routing, hierarchical budget caps, grounding-verification gates, quality gates with rejection telemetry. **He built all of it by instinct and none of it by name.**

**The governing assumption, and the single most important line in this document:**

> The gap is vocabulary **plus the decision surfaces his production path never forced him to touch.** Each module must diagnose which is which. Never globalise "he already knows this."

An earlier draft of this curriculum said *"the gap is vocabulary, structure, and articulation — not knowledge."* A four-model council pre-mortem unanimously flagged that as flattering and false. Building circuit breakers by instinct does not confer knowing when a circuit breaker is the wrong primitive versus a bulkhead or admission control. **Do not re-make that error.**

### How to talk to him

- **Never explain what an agent, a harness, a model, or an API is.** He uses these daily.
- **Do** give the canonical name, a crisp repeatable definition, and where it comes from.
- **Never reference a company, incident, paper, or researcher without a one-sentence setup first.** Assume no prior familiarity. *This is the specific defect that got the first version of this curriculum rejected* — its audio name-dropped Zillow and Rechat as though he'd been in the room.
- Explain jargon and trade-offs in plain language **before** asking him to decide.
- Label your own claims **observed / inferred / designed**. He is being taught to do it; model it.

---

## 2. The teaching contract — non-negotiable, and it replaced an earlier rule

Sean's instruction, 2026-08-17, mid-M1: *"Change it up so that Fable 5 guides me and explains everything instead of asking me to figure it out based on the teachings. This is part of the teachings as well."* And later the same day: *"No, I don't want to write a prediction before the exercise. I enjoy the 3 audio file teachings so far and I want to keep going with that."*

**Prediction-before-exercise is abolished.** So is "sketch it cold before I show you mine." The evidence backs him: worked examples precede faded scaffolding, and discovery-style prompting is counterproductive for material someone is new to.

**Every module and every build decision runs this loop:**

1. Name the thing and say why it exists — what breaks downstream if it goes wrong.
2. Define the jargon in the same breath.
3. Lay out the real fork with honest trade-offs. Not a quiz with a withheld answer.
4. **Commit to a recommendation and show the reasoning chain.** "It depends" is not guidance.
5. **Then he decides**, informed, and free to overrule you.
6. Capture his reasoning **verbatim** — his words, not your paraphrase.

**The fade:** first few decisions fully worked out loud; then he calls them with you analysing; late on, *invite* him to try a move he has seen three times. An invitation he can decline, never a gate.

**Verbal reps are deferred** and not on a calendar. He asked to get through the modules and feel comfortable first. No interviews are booked. **Ask occasionally; wait for a yes.** The ramp when it starts: retrospective untimed → retrospective timed → concurrent, timed, interrupted.

---

## 3. What this program is, and why it was rebuilt

**Goal, in Sean's own words:** *"look at an AI product or a regular product and fully envision how it runs under the hood, what could go wrong, how to fix it, and how to apply judgement throughout. It should be second nature. I should be able to discuss the full AI PM design system thinking and problem solving as if I'm discussing the ingredients in my breakfast this morning."*

**A previous program was built 2026-08-16, consumed at M1, and rejected.** Three defects: too abstract (its architecture module taught RAG as "retrieval quality is measurable," which doesn't let you draw a pipeline); no design-thinking half; every exercise pointed at his own fleet so nothing transferred. It lives at `vault/20_projects/prj-ai-pm-system-thinking-strategy/` — **retired, not deleted**, with a superseded banner. Its notebook `0abf9bb0` holds $4.12 of paid research and **must not be deleted.** Its `m7-lesson-evals-metrics-loop-engineering.md` survives as the vocabulary source for Golden Loop's domain language.

**The current program: five modules over eight weeks**, spine ordered by *the kind of decision a PM must make* — Problem/User/Workflow → Decision & Error Economics → Data/Feedback/Model Path → Architecture Under Constraints → Interaction/Trust/Control → Evidence/Evaluation/Telemetry/Rollout → Operations/Cost/Drift/Abuse/Ownership, compressed into five.

Read `curriculum/curriculum-map.md` for the full locked map and `curriculum/2026-08-17-council-premortem-curriculum-map.md` for the four-model attack that shaped it.

---

## 4. State — what exists right now

**Notebook: `bcb4e6aa-9da7-49fe-8c65-46d27110313e`** ("System Design Thinking for AI PM"). 19 sources, all fetch-verified. Sean listens in the notebook; **nothing is downloaded**, by his choice.

### Modules built: M1, M2, M3 — all nine audio episodes complete

| Module | Lesson file | Audio (pre-brief / deep-dive / debate) |
|---|---|---|
| **M1** Problem, Users & Decision Economics | `curriculum/m1-lesson-problem-users-decision-economics.md` | `747416f7` *Who Pays for Inevitable System Mistakes* · `5f88a198` *Choosing Which AI Mistakes You Can Afford* · `164db4c4` *Should you ship AI at 85% accuracy* |
| **M2** Data, Feedback & the Model Path | `curriculum/m2-lesson-data-feedback-model-path.md` | `b7b84c07` *Why human messiness breaks AI pipelines* · `afd5322f` *Why your data pipeline feeds on poison* · `d1583ba7` *Buying Versus Building Your Data Labels* |
| **M3** Architecture Under Constraints | `curriculum/m3-lesson-architecture-under-constraints.md` | `63351ebb` *Hardening Agentic Systems with Threat Modeling* · `5671f806` *The Invisible Plumbing of Production AI* · `5d9b1bef` *AI Agents versus Workflows for Legal Contracts* |

**Sean's feedback on M1, mid-deep-dive:** *"this is MUCH better and what I was expecting."* Calibration confirmed. Keep the format.

### Source IDs by module (for `-s` selection)

- **M1:** `2251b249` lesson · `bb367054` PAIR User Needs · `f0988a1f` Google ML thresholds · `66c038cd` Amazon case
- **M2:** `5b756d4b` lesson · `1ab0974b` PAIR Data Collection · `9ac74ee9` Datasheets for Datasets · `dbb721bc` RAG failure taxonomy · `d269db15` Zillow (JISE)
- **M3:** `37b21bfc` lesson · `8641160f` Anthropic Building Effective Agents · `ce870d74` Sculley Hidden Technical Debt · `a06dd429` Microsoft agentic failure taxonomy · `9d283700` Harrison Chase harness talk

Full manifest with tiers: `notebooklm/source-manifest.md`. Artifact log: `notebooklm/artifact-tracker.md`. Audio prompts, reusable as templates: `notebooklm/audio-instructions/`.

---

## 5. What still needs building — M4 and M5

Both specs come from the locked map. **Neither lesson, sources, nor audio exists yet.**

### M4 — Interaction, Trust & Control

**Mirror eligibility: NO. Teach from zero, and say so.** A single-operator fleet never forced him to design a trust surface. This is the design-thinking half the retired program lacked entirely — and the council warned that claiming error-cost tables *are* the human half is asserting it, not installing it. Ethnography of who gets hurt, incentive analysis of why teams ship anyway, and the politics of model ownership belong here with real depth.

**Covers:** the five relationship pairings (Human↔Software / Human↔LLM / Human↔Agent / **Agent↔Agent** / **Agent↔Software**) each with primary mode, design levers, failure modes and metrics · trust **calibration, not maximization** · communicating uncertainty · failure UX, recovery and escalation · HITL insertion points, confidence thresholds, reviewer drift and fatigue · Wizard-of-Oz prototyping *before* training · Amershi's 18 validated guidelines · the three relational metrics (relational trust, behavioural alignment, friction recovery) which are longitudinal rather than task-completion.

**Anchor:** Intercom Fin (published confidence + handoff design). **Backup:** GitHub Copilot accept/reject.
**Debate:** show confidence scores to users, or hide them.
**Artifact:** failure-UX spec + model card → **closes one of Grok's three Golden Loop gaps.**

**Candidate sources** (verify before use — see §6):
- Amershi et al., *Guidelines for Human-AI Interaction*, CHI 2019 — 18 guidelines, validated with 49 practitioners against 20 products. PDF at `microsoft.com/en-us/research/wp-content/uploads/2019/01/Guidelines-for-Human-AI-Interaction-camera-ready.pdf`
- Google PAIR chapters on Mental Models, Explainability + Trust, Feedback + Control, **Errors + Graceful Failure** — use `/guidebook-v2/chapters/<slug>/`, **not** `/guidebook/chapters/`, which redirects to the homepage
- Nate B Jones + Ryan Wilson, *Stop Designing AI Chatbots, Start Designing AI Relationships* — **take the 5×5 pairings grid and the three relational metrics; leave the "Reflexive Intelligence" framing**, which is coinage and ChatGPT-assisted by disclosure. Reachable via the Executive Circle MCP, post id `b87d7b60-b804-482a-b502-0e07c2deeb1b`

### M5 — Evidence & Operations

**Mirror eligibility: PARTIAL.** He has telemetry and budget caps. He has never run an experiment, set a rollout gate, or negotiated ownership with another person.

**Covers:** instrumentation, unit of analysis, sampling for human review · **day-one invariants → golden datasets → holdout hygiene** (the progression matters; M3 already planted the invariant suite as a day-one primitive) · champion/challenger · LLM-as-judge and its failure modes, including weak-judge Goodharting · rollout, A/B, kill switches · drift types (covariate / label / concept) · **unit economics at product level, not per-hop** — gross margin, pricing, when inference cost exceeds LTV · org ownership, review boards, incident response.

**Anchor:** Rechat (Hamel Husain's "whack-a-mole" story). **Backup:** published routing/caching cost architectures.
**Debate:** LLM-as-judge vs. human eval.
**Artifact:** launch criteria + cost model + incident runbook → **closes the other two Golden Loop gaps.**

**Candidate sources:** Hamel Husain's eval writing; Sculley (`ce870d74`, already in the notebook); the Stochastic Tax preprint (arXiv 2605.27320 — **fresh preprint, date it when spoken**); Nate B Jones' Moat Audit (12 questions, Executive Circle post `de715ba3-14b2-4a90-8279-2ef06ad78507`).

### The build recipe — exactly what M1–M3 did

1. **Find 3–5 sources.** Never 8–12. The retired notebook bulk-imported 83 and graded 17% A / 60% C / 20% D.
2. **Add each, then VERIFY IT CONTAINS ANYTHING** (§6). Delete and re-source anything that doesn't.
3. **Write the lesson** (~2,300–3,500 words) following the M1–M3 shape: §0 diagnose what he already knows vs what is new → content sections with every term defined and every reference set up → compressed vocabulary list → exercises (worked-then-attempted, one teardown and one forward-design-from-a-dirty-brief, constraint shift walked the first time) → the written artifact, named as its Golden Loop deliverable → sources table with tiers and honesty notes.
4. **Add the lesson to the notebook**, capture its source ID.
5. **Write three audio prompts** into `notebooklm/audio-instructions/` — copy an M3 prompt and adapt. Every one carries the calibration block verbatim, especially *never reference a company or paper without a one-sentence setup*.
6. **Generate three episodes** with explicit `-s` flags, then **verify against `artifact list`** (§6).
7. Update `source-manifest.md` and `artifact-tracker.md`. Commit.

---

## 6. Operational rules learned the hard way — do not rediscover these

**A source that added successfully is not a source that contains anything.** Verify substance before building on it:
```bash
notebooklm source fulltext <id> --notebook <nb> --json 2>/dev/null | python3 -c "
import sys,json; raw=sys.stdin.read(); i=raw.find('{'); d=json.loads(raw[i:]); c=d.get('content','')
print(len(c)); [print(k, c.lower().count(k)) for k in ['keyword1','keyword2']]"
```
Three failures caught this way in one sitting: the PAIR data-collection URL **redirected to the guidebook homepage** and imported 11,456 chars of navigation with zero hits on *label* or *bias*; **arXiv and ACL Anthology landing pages import the abstract, not the paper** (the RAG taxonomy landing page had zero hits on *chunking*, one of its own 33 failure modes) — always use `/pdf/`; and **terminal-rendered `source fulltext` is truncated**, so parse `--json` from the first `{` or you measure the renderer.

**`generate audio` can fail while exiting 0.** A loop once reported three M2 episodes queued when only one existed. **Always count against `artifact list` afterwards** — expect `modules × 3`.

**`-s` flags must be written out explicitly.** A shell variable holding several `-s` pairs does not word-split through this CLI; it fails with `VALIDATION_ERROR` naming the whole string as one ID.

**PDFs import with their URL as the title.** Cosmetic, but `source list` alone won't tell you what a source is.

**Reuters blocks automated fetching** (`RPCError rpc_code=9`), as do the Irish Times and NC State's Data Ethics Repository. The Amazon case uses a Built In retelling, labelled as such.

---

## 7. Golden Loop — the portfolio build, and it is live

**Kept** as the portfolio piece. An eval-first golden-dataset cockpit with a playable teaching layer, chosen 3–1 over an "AI PM flight simulator." Phases A and B are **done** — six locked decisions, a falsification verdict of BUILD with the wedge re-scoped, five competitor teardowns, a mock one-pager, and a milestone post drafted.

All of it lives in this project now (`product/`, `posts/`, `research/`), migrated 2026-08-17 from the retired project with history intact.

**Phase C is written and ready to paste:** `product/kickoff-prompt-phase-c-wayfinder.md`. It carries the teaching contract, a warning box about facts that changed, and three mandatory additions.

**The three additions** came from the council's one collateral objection — Grok: *"an eval-first golden-dataset cockpit is an ML-engineer portfolio piece, not an AI-PM portfolio piece... He can already build tooling. That is the one fact not in dispute."* The objection was made against a one-line description; the Phase A partner session largely rebuts it. But three items were genuinely missing: **a cost model**, **a failure UX**, and **a written ship gate for Golden Loop itself.** Each doubles as an M4 or M5 artifact.

**Framing rule:** the decision log is the portfolio's **front door**, not an appendix. The teaching layer is craft Sean already demonstrates; judgment is the scarce signal.

**Three facts corrected in the Phase C prompt that must not drift back:** the curriculum is five modules with **no M7** (evals is M5, week 6–7); **Golden Loop ships weeks 9–12**, not week 8, because the curriculum honestly consumes the eight weeks; and the **$8–15 Phase D council reserve no longer exists** (~$7 remains at the ceiling).

**`product/decision-log.md` and `product/candidate-scorecard.md` still say "M7" and are CORRECT as written** — they record what was decided on 2026-08-16. **Do not "fix" them.** Editing a dated record to match new facts is the silent drift this program forbids; a superseding entry is how change gets recorded.

---

## 8. Budget

| | |
|---|---|
| This program | **$10.66** of a $15–25 approval — Gemini DR $2.80, DR Max $7.00, council premium $0.86 |
| Golden Loop | **$6.92** — same $15–25 approval |
| **Combined** | **$17.58**, near the ceiling. ~$7 left |
| Gemini fleet-wide caps | **$50/month, $20/day** per `agents-sdk/config.toml` `[gemini.budget]` — **not** the $20/$10 the skill doc quotes. August MTD **$21.00 of $50** |

Everything since 2026-08-17 has been **$0** — hand-curation and `yt-dlp`. M4 and M5 need no paid research.

---

## 9. Open items

1. **Phase C wayfinder session** — prompt ready, not run.
2. **M4 and M5** — §5.
3. **Two Golden Loop status questions** Phase C asks at start: has the mock one-pager gone to 2–3 hiring managers, and is milestone post #1 published?
4. **Transcription for verbal reps** — Sean said don't bother setting it up. Leave it.
5. Sean is saving a **YouTube playlist** built 2026-08-22 from `yt-dlp` searches — real titles/IDs/view counts, in that session's chat. Not in the notebook by his choice. Regenerate with `yt-dlp --flat-playlist --print "%(duration)s|%(channel)s|%(view_count)s|%(id)s|%(title)s" "ytsearchN:<query>"` if he wants more.

---

## 10. Answering his questions

He will ask about the material, not just ask you to build. The three lessons are the substance — **read the relevant one before answering**, and the audio prompts in `notebooklm/audio-instructions/` show how each concept was framed for him.

The through-lines worth holding in your head:

- **M1:** a single accuracy number destroys the only information that matters, because the two errors are never equally expensive. The threshold is where the decision physically lives, and it is a product decision. Diagnosis without disposition is academic.
- **M2:** *if your product's behaviour decides which data comes back, your data is not a sample of the world — it is a sample of your product's mistakes.* That is the Zillow mechanism, and it generalises to every system with a human choosing.
- **M3:** the model call is ~20% of a production system; the other 80% is plumbing. Workflows beat agents whenever the structure is stable enough to encode, because compounding error is arithmetic — 95% per step over ten steps is ~60% end to end.

**Things he already built, named** — this table is the highest-value page in the curriculum for him and worth having ready: `fallback = "none"` is a **fail-closed degradation policy**; the synthesizer's `partial` is a **circuit breaker**; `wol-deferred` is **idempotent retry**; `check_caps` projecting `mtd + predicted` is a **pre-flight budget check**; PreToolUse hooks exiting 2 are a **policy enforcement point**; the discovery council's URL rule is a **grounding verification gate** and also a **precision-over-recall decision**.

**Things he has genuinely never done:** written labeling instructions for a stranger, measured inter-rater agreement, threat-modelled his own agents, built session resumability, run an experiment, or negotiated data ownership with another person. Teach those from zero without flattering him that he half-knows them.
