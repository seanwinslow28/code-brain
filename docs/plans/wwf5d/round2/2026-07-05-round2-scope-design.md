# WWF5D Round 2 — Scope & Design

- **Date:** 2026-07-05
- **Status:** Approved (shape + substrates ruled by Sean 2026-07-05). Ready for `writing-plans` → battery + driver.
- **Predecessor:** the Step-1 eye-check ([`../eye-check/2026-07-05-preserve-session-eye-check.md`](../eye-check/2026-07-05-preserve-session-eye-check.md)) confirmed WWF5D lifts Opus → Round 2 is worth Fable.
- **Budget:** 3 paired tasks, **3 Fable runs total** (one Fable blind + one Opus baseline each). Fable access: ~2–3 days, ~40% of the weekly allowance left.

## Scoping principle (the hard rule)

Every Round 2 task must exercise Fable's **proven premium** — spec-decidedness, breadth past named seams, contract-contradiction detection, evidence-discipline — via the proven **paired-subagent** mechanism. **No task is the plain diagnosis/zoom-out loop** (cheap-on-Opus, matched twice in BT2+BT5). The three tasks target the facets Phase B left **under-sampled or untested**:

1. **Spec-authoring as a paired diff** — corroborated on BT1/BT3 only as a *byproduct* of diagnosis/audit runs. RT1 isolates it as the **primary** axis on a **fresh** substrate. (Correction 2026-07-05: the anima register-seam is *already* fully diffed as BT2 — `bt2-opus`/`bt2-fable`/`bt2-diff` — so re-running it is redundant, not a gap. RT1 pivoted to `preserve-session`.)
2. **The existence-check ceiling** — Fable *missed* the unwired-enforcement seam in BT1 (its clearest blind spot). RT2 re-probes it on a fresh, enforcement-claim-dense substrate.
3. **Proactive-research + deliverable-shape grounding** — two introspection hypotheses the Phase-B battery never exercised (no task had a live external-research surface). RT3 is built to need both.

## The three tasks

All three share one shape: **one Opus baseline subagent (`model:"opus"`) + one Fable blind subagent (`model:"fable"`)**, identical pinned prompt, shared working-tree snapshot, neither seeing the other. The orchestrator (Opus) holds the diff. This is the Phase-B mechanism (kills pin-drift).

### RT1 — preserve-session fix-spec → axis: spec-decidedness + intent-preservation (§6)

- **Correction (2026-07-05):** RT1's original substrate (anima register-seam) is **already fully diffed** — it ran as **BT2** (`baselines/bt2-opus.md` + `fable-runs/bt2-fable.md` + `bt2-diff.md`; the diff judged the Fable spec production-grade and its diagnosis half was tagged *cheap-on-Opus*). Re-running would re-litigate settled evidence. RT1 pivots to a fresh substrate (Sean's call, 2026-07-05).
- **Substrate:** author the intent-carrying **fix spec for `preserve-session`** — the skill the Step-1 eye-check audited. Both arms get: `.claude/skills/preserve-session/SKILL.md` + `.claude/skills/resume-session/SKILL.md` (the consumer) + the pinned grounding (a–d) + a shared, neutral consolidated findings list ([`rt1-preserve-session-findings.md`](rt1-preserve-session-findings.md), merged from the two eye-check audits). Harness: `intent-engineering`.
- **Why this isolates the axis:** identical findings in → the only variable is the *spec*. Does Fable pre-make every decision (write transport, the two-anchor discipline split, error shapes, done-criteria, band-aid tripwires) and **surface-not-silently-pick** the genuine owner-forks (auto-scaffold the missing note vs redirect to CLAUDE.md; reconcile with the flush hook vs stay separate) — vs Opus offering options / hedging?
- **Arms:** Opus baseline + Fable blind, identical prompt + findings.
- **Deliverable:** the paired diff (`rt1-diff.md`) + a real, implementable preserve-session fix spec (closes the eye-check loop: Fable's fix-spec vs Opus's on the exact skill we just audited).

### RT2 — ceiling-probe audit → axis: existence-check / false-sense-of-safety (§2.4)

- **Substrate (primary):** `skill-audit` on **`.claude/skills/hooks-configuration/`** — the densest enforcement-claim skill in the library (49 "enforced/hook/exit-code/deny" hits) and, being *about* hooks, maximally existence-checkable against the real `.claude/hooks/` + `settings.json`. **Alt:** `security-hardening` (safety-critical claims). Final pick pinned in the plan after a read.
- **Why not cheap-on-Opus:** it's a real premium-harvest audit (breadth, contract-contradiction, dangerously-wrong triage) on a substrate chosen to maximize false-sense-of-safety findings.
- **The ceiling question, honestly factored:** Opus already caught the existence-check *without* WWF5D in BT1 — so a with/without-WWF5D arm would mostly re-confirm Opus's existing competence and waste Fable. Instead RT2 is a **paired premium-harvest** (Opus baseline + Fable blind), and the ceiling question becomes a **watch-for**: *does Fable's BT1 existence-check blind spot recur?* The "does §2.4 close the gap for the deployment models (Opus/Sonnet)" question **routes to Step 4** — RT2 becomes one of the held-out validation tasks there, so §2.4's efficacy gets measured properly at zero extra Fable cost.
- **Deliverable:** the paired diff (`rt2-diff.md`) + a note on blind-spot recurrence + this task handed to Step 4's battery.

### RT3 — portfolio explainer-graphics enhancement spec → axis: proactive-research + deliverable-shape grounding

- **Substrate:** the portfolio's six explainer components (`sw-ai-pm-portfolio/src/components/case-study/{CodeBrain,Intent,AnimationPipeline,SixteenBitFit,TheBlock}Explainer.astro` + `ExplainerGraphic.astro` / `InteractiveExplainer.astro` + `src/scripts/interactive-explainer.ts`; assets in `public/assets/projects/explainers/`). Currently basic; Sean wants them "more creative, technical, interesting."
- **Scope:** author an intent-carrying enhancement spec for the explainer-graphics **system** (the harness + tools + elevation pattern), worked through on **1–2 exemplars** — not six full specs. Understand-intent-first: read each graphic + the project it explains, name what it's *trying to communicate* and to whom (recruiters **and** creative technologists), then propose the most impressive/creative realization and **recommend the right harness + tools**.
- **⚠️ Constraint lifted (Sean's call, 2026-07-05):** the subagents **must NOT be bound by the portfolio's old "no GSAP/Framer/Lenis" stack note** — that was a months-old decision Sean is explicitly reopening. Any technique/library is on the table (WebGL/shaders, Rive, Three.js, scroll-driven, generative/interactive, Lottie, canvas islands, …); recommending the harness is *part of* the spec. Ground in the *medium* (web / Astro / recruiter-facing) and each graphic's *intent* — not in the retired lock.
- **Why not cheap-on-Opus:** with every technique on the table, the *right* answer requires researching **current** best-practice (what creative technologists ship now) and grounding in each graphic's communicative intent — the exact place Opus tends to propose generic dazzle from stale priors while (hypothesis) Fable verifies-the-world and pre-decides the harness with reasoning. Both arms get web research (`WebSearch`/`WebFetch`) + the local animation skills (`gsap-scrolltrigger`, `animation-components`, `lottie-animations`, `react-spring-physics`, `animejs`, `locomotive-scroll`) + the portfolio repo. The premium test = *do they proactively use them.*
- **Deliverable:** the paired diff (`rt3-diff.md`) **and** the enhancement spec Sean's been wanting (the higher-value creative-technical brief).

## Shared run protocol (carried from Phase B)

- **Paired subagents, one orchestrator.** Fable blind run sees only its pinned prompt; Opus baseline is a matched subagent on the same tree. No `/clear` needed — subagent isolation holds blindness + pinned-input parity.
- **Capture-first → disk, then commit-handoff.** Save every raw output to `docs/plans/wwf5d/round2/` **before** distilling. (The Cowork sandbox mount denies `unlink`/`rename`, so I cannot `git commit` from here — files persist to disk durably; commit commands are handed to Sean. Raw Fable output written to disk is the preservation guarantee; distillation can finish on Opus later.)
- **F1** — self-report is a hypothesis; only a behavioral delta earns a WWF5D entry.
- **F2** — WWF5D holds abstracted recipes, never transcripts.
- **F3** — partial transfer is the honest outcome; log ceilings too.
- Append notable moments to [`../fable-learnings-log.md`](../fable-learnings-log.md) as we go.
- Fold corroborated deltas into WWF5D §1–6 + the evidence index; note anything that refines an existing item.

## What routes to Step 4 (not spent on Fable)

- Whether WWF5D §2.4 closes the existence-check gap for Opus/Sonnet (RT2 becomes a held-out validation task).
- The full transfer measurement: Opus-with-WWF5D vs Opus-without on the RT1/RT2/RT3 briefs, judged by the cross-family council (order-swapped, length-controlled, not-Opus-led, κ-gated), Sean's eye final → WWF5D §7.

## Out of scope (carried from the mission)

- Mac Mini BT5 fleet fix; Phase C *implementation* of any spec (anima routing, creative-chain, the RT1/RT3 specs — those implement later, on Opus); the elevated-skill deferred tickets.

## Next

`superpowers:writing-plans` → the Round 2 **task battery** (`round2-task-battery.md`, mirroring [`../task-battery.md`](../task-battery.md): pinned inputs + self-contained run-prompts per arm) + **session driver** (`round2-session-driver.md`, mirroring [`../fable-session-driver.md`](../fable-session-driver.md): the literal dispatch order + capture steps).
