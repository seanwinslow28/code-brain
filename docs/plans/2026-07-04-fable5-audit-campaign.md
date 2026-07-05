# Fable 5 Audit & Improvement Campaign

- **Date:** 2026-07-04
- **Owner:** Sean
- **Window:** ~3–5 days of Fable 5 access (est. through ~2026-07-07 to 07-09), then usage-based/expensive
- **Status:** Design approved (shape + three forks ruled 2026-07-04). Phase A ready to start.
- **Thesis in one line:** Fable is a scarce, expensive, expiring resource — so spend it only on what *only Fable* can do (auditing, root-cause, intent-carrying specs, and cloning its own cognition), and let Opus 4.8 / Sonnet 5.0 do everything before and after.

---

## 0. TL;DR — the bet

Fable's real advantage isn't raw intelligence, it's two things Opus reliably misses: (1) the **seams** where carefully-built inputs silently fail to travel downstream between phases, and (2) the **system-level root cause** under a pile of band-aid patches. It also preserves *motivational intent* — the "why" — through the details to completion.

Because the window is days, not weeks, the campaign is a **triage funnel**, not a sweep. Three moves:

1. **Prep on the cheap models first.** Opus/Sonnet inventory, triage, first-pass improve, and scaffold — so Fable never spends a cycle on mechanical work.
2. **One deep dive: WWF5D ("What Would Fable 5 Do").** Reverse-engineer Fable's cognition into a portable skill so Opus/Sonnet inherit the behavior. This is the crown jewel — it compounds across every skill and project *after* Fable is gone.
3. **A focused skill sweep + one project root-cause audit.** Fable elevates the top-5 most-important skills and writes one intent-carrying spec for anima's hardest architecture seam. Opus implements later.

---

## 1. Operating principles (extracted from the source transcript)

- **Fable plans, Opus implements.** Fable authors specs and audits; a lesser model does the build. The spec must *carry forward motivational intent and all critical details of what needs to be implemented and why.*
- **Motivational-intent preservation is the through-line** — and the thing we measure. It's both Fable's edge and the failure mode we're hunting (details decided but not enforced downstream).
- **Prep on cheap models; reserve Fable for the irreplaceable.** Every hour of Fable spent drafting or inventorying is an hour stolen from auditing.
- **Fable's edge, concretely:** catches downstream seams + missing handoff/adapter steps; zooms out to system-level root cause instead of patching symptoms; proactively researches current best practice (web/docs) without being told; triages findings as *dangerously-wrong / structural / minor*.
- **Ground before you burn.** Every Fable run starts by asking clarifying questions to ground in context — never a cold, open-ended kickoff.

---

## 2. Durable outputs (Sean's picks — what must exist after Fable is gone)

1. **Committed specs for Opus to implement** (intent-carrying).
2. **Improved skills, edited + committed** (the top-5, elevated).
3. **Root-cause diagnoses of nagging bugs** (captured as decision-docs).

Plus the campaign's signature artifact: **WWF5D**, a committed, eval-validated skill.

---

## 3. Allocation (locked)

**Targets:** code-brain skills + fleet · anima pipeline · sw-ai-pm-portfolio · individual most-used skills. (agent-fleet-observability deprioritized.)

**Fable budget split:**

| Slice | Share | What Fable does |
|---|---|---|
| WWF5D deep dive | 40% | Introspect → diff vs Opus → co-author → validate |
| Tier-1 skill audits | 30% | Elevate the **top 5** most-important skills to "wow" |
| anima register-seam root-cause | 30% | One system-level diagnosis + intent-carrying spec |

**Forks resolved (2026-07-04):**

- **WWF5D depth:** Introspect + behavioral diff + validation (full method). Not a self-report vibes doc.
- **Fable reach:** WWF5D + **top 5** skills + one project spec. Everything else is Opus/Sonnet (prep + long tail via WWF5D-Opus).
- **Deep audit target:** anima — the Outward Turn / per-register model-routing seam.
- **Creative skills:** No extra direct Fable edits. `writing-voice-modes` stays Tier-1 but scoped to its *elicitation/enforcement scaffolding*, not the voice samples. The wider creative chain (storytelling-architecture, creative-director, the writing chain) gets one **creative-chain seam audit** → spec, run as a WWF5D battery task (double duty). UX/UI + image-gen → WWF5D-Opus in Phase C.
- **Research grounding:** One focused, time-boxed deep-research pass on WWF5D's method — done 2026-07-04, see [`2026-07-04-wwf5d-research-findings.md`](2026-07-04-wwf5d-research-findings.md).

**Tier-1 five (confirmed):** `writing-voice-modes`, `intent-engineering`, `skill-system-mastery`, `plan-and-think`, `systematic-debugging`.

---

## 4. Phase A — Prep (Opus 4.8 / Sonnet 5.0, before touching Fable)

### A0. Method grounding — DONE (2026-07-04)

Focused deep-research pass complete: [`2026-07-04-wwf5d-research-findings.md`](2026-07-04-wwf5d-research-findings.md). Four findings now bind the WWF5D build: (1) self-report is unreliable → the behavioral diff is load-bearing; (2) only *abstracted recipes* transfer via prompting → encode procedures, not Fable transcripts; (3) there's a real ceiling → validate per-move, partial transfer is the honest outcome; (4) de-bias the judge (order-swap, length-control, cross-family panel, κ-gate, Sean's eye final).

### A1. Assemble the Fable Audit Harness (you already own ~70%)

Two runnable tools, grounded-first (each asks clarifying questions before running), each emitting an **intent-carrying spec** as its handoff artifact:

- **`skill-audit`** — audits a skill for downstream-seam leaks, missing adapters, and "never-wows" gaps. Assembled from `skill-system-mastery` + `intent-engineering` + `writing-critique`'s "single highest-leverage fix" pattern + a grounding preamble.
- **`zoom-out-and-think`** — system-level root-cause oracle: reads the whole subsystem, web-searches current best practice for the domain, names the needle-in-the-haystack, refuses to patch symptoms. Assembled from `systematic-debugging` (4-phase) + `plan-and-think` + `intended-vs-implemented`.

Spec emission uses the `intent-engineering` scaffold + `decision-doc`. Validation/critique can call `llm-council`.

### A2. Triage the 127 skills → tiers

Score each by **frequency × leverage × "never-wows" gap**. Output three tiers:

- **Tier 1 — Fable touches (the top 5).** Recommended candidates (Sean confirms/swaps): `writing-voice-modes`, `intent-engineering`, `skill-system-mastery`, `plan-and-think`, `systematic-debugging`. Swap bench: `prompt-engineering`, `writing-critique`, `prd-generator`.
- **Tier 2 — Opus improves now.** Directly upgraded on the cheap model during prep.
- **Tier 3 — spec-only / leave.** Improvement spec drafted; no edit this window.

Meta-skills (`skill-system-mastery`, `prompt-engineering`, `plan-and-think`) are weighted up: improving them improves the whole sweep downstream — the most "Fable" kind of leverage.

### A3. Opus first-pass

Improve Tier-2 skills directly, and draft **strong** improvement specs for Tier-1 — so Fable *elevates a draft*, not authors from a blank page. Fable's cycles go to the last 20% of quality, where its edge lives.

### A4. Scaffold WWF5D

- Write the **introspection protocol** (fixed question set: grounding, intent preservation, root-cause method, dangerously-wrong-vs-minor triage). Treat its output as *hypotheses*, never ground truth (finding 1).
- Define the **WWF5D artifact shape up front**: abstracted, portable recipes only — a grounding protocol, a seam/handoff checklist, a root-cause procedure, a triage rubric, an adapter pattern, an intent-preserving spec template. **Copy the recipe, not the raw trace** (finding 2).
- Assemble the **task battery**: 3–5 real tasks spanning code-brain / anima / portfolio. Include the **creative-chain seam audit** as one battery task (double duty — a real creative spec *and* a diff task showing Fable's seam-eye).
- **Generate the Opus-side baseline traces now** — so in Phase B, Fable only adds its half + the critique. Pure efficiency multiplier.
- Stand up the **validation harness**: reuse the anima Em protocol (N=5 majority, reference-blind, κ-gated). Judge panel is cross-family and order-swapped — **not** Opus-led — with Sean's eye as the final call (finding 4).

---

## 5. Phase B — Fable's scarce cycles (the irreplaceable work)

### B1. WWF5D deep dive — 40%

1. **Introspect** — Fable answers the fixed protocol. Output = candidate moves (hypotheses), not ground truth.
2. **Behavioral diff** — run the battery on both models; Fable critiques Opus's baseline output, categorized *dangerously-wrong / structural / minor*. The **deltas are the load-bearing evidence.** A self-reported move only enters WWF5D if a behavioral delta corroborates it.
3. **Co-author** — Fable distills corroborated moves into **abstracted recipes** (grounding protocol, seam checklist, root-cause procedure, triage rubric, adapter pattern, intent-preserving spec template). Recipes, not transcripts — that's what ports across models.
4. **Validate** — Opus-with-WWF5D vs Opus-without on a held-out task. Judge: cross-family, order-swapped, reference-blind panel (not Opus-led), κ-gated to a few Sean labels, Sean's eye as final call. Iterate once.

Honesty gate: if it transfers, we've cloned the edge cheaply; if it only partially transfers, we document exactly which moves are promptable vs capability-gated. Partial transfer is the *expected* outcome (finding 3) — a map of Fable's edge, not a failure.

### B2. Tier-1 skill audits — 30%

Fable elevates the top-5 from their Opus drafts to "wow." `writing-voice-modes` is audited on its *elicitation/enforcement scaffolding* only — never the voice samples (taste is Sean's; a model "improving" voice is the flattening the writing chain exists to prevent). The wider creative chain rides the creative-chain seam audit in §B1. **Privacy:** edit the public `SKILL.md` only — never the local-only `references/`/`drafts/` (writing-voice-modes, personal-finance, life-admin), and never write real personal data into tracked files.

### B3. anima register-seam root-cause — 30%

Point `zoom-out-and-think` at the Outward Turn: multi-character / multi-style + **per-register model routing** (NB2 fails Tartakovsky *Primal* grit; per-register model selection needed, not universal NB2). A true "does intent survive the handoffs" target. Fable writes the intent-carrying spec; **implementation deferred to Opus in Phase C.**

---

## 6. Phase C — Harvest (Opus / subagents, after Fable)

- **C1.** Implement Fable's specs (anima register routing; Tier-1 spec items) via subagent-driven development.
- **C2.** Roll **WWF5D into Opus/Sonnet standing context**, then re-run Tier-2/Tier-3 skills as "WWF5D-Opus" to lift the long tail cheaply. This is the compounding payoff.
- **C3.** Capture root-cause diagnoses as decision-docs; add CHANGELOG entries per repo convention.

---

## 7. Guardrails

- **Privacy layer (code-brain).** Never `git add` the private-layer paths; never weaken ignores; never write real income/medical/contact/employer data into tracked files. Verify before every commit touching writing-voice-modes / personal-finance / life-admin / job-hunt.
- **Costed runs (anima).** Subscription billing, never `ANTHROPIC_API_KEY`; follow the fleet-ops protocol (isolated worktree, single owner, clean teardown) for any multi-step costed run.
- **Ground-first.** No cold Fable kickoffs — clarifying questions before cycles burn.
- **Spec fidelity.** Every Fable-authored spec must carry motivational intent + the "why," so an Opus implementer can't drift.

---

## 8. Success criteria

- **WWF5D:** measurable lift of Opus-with-WWF5D over baseline on the held-out task (Council majority), with a written transfer-analysis (what ported, what didn't).
- **Skill sweep:** top-5 improved + committed; Tier-2 improved + committed; Tier-3 specced.
- **anima:** one intent-carrying root-cause spec, ready for Opus, on the register-routing seam.
- **Zero private data committed;** all privacy guardrails held.

---

## 9. Immediate next actions

- [x] Method grounding (A0) — done, findings folded in.
- [x] Tier-1 five confirmed.
1. Move to `writing-plans` for the **Phase A implementation plan** (harness assembly + 127-skill triage + WWF5D scaffolding/baseline-trace generation).
2. Execute Phase A on Opus 4.8 / Sonnet 5.0 so Fable walks into a warm start.
3. On Fable access, run Phase B in budget order: WWF5D → Tier-1 audits → anima register-seam spec.

---

## Appendix — component map

**Harness assembled from existing pieces:** `intent-engineering`, `systematic-debugging`, `skill-system-mastery`, `plan-and-think`, `intended-vs-implemented`, `writing-critique`, `decision-doc`, `llm-council`, `pm-execution:pre-mortem`, `ship-check`.

**WWF5D task-battery candidates (pick 3–5):** a skill-audit on one Tier-1 skill · the anima register-seam root-cause · a portfolio explainer spec · a prd/tech-spec authoring task · a systematic-debugging root-cause on a real bug.

**Deprioritized this window:** agent-fleet-observability; portfolio deep audit (execution-heavy — spec-the-polish only if the window holds).
