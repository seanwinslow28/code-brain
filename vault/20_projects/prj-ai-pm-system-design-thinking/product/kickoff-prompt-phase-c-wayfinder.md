# KICKOFF PROMPT — Golden Loop Phase C: the Wayfinder Session (paste into a fresh Claude Code session)

> **Launcher:** start a fresh session in `/Users/seanwinslow/Code-Brain/code-brain` and say:
> *"Read `vault/20_projects/prj-ai-pm-system-design-thinking/product/kickoff-prompt-phase-c-wayfinder.md` and run Phase C with me."*

> **⚠ This file moved and its facts changed on 2026-08-17. Read this box before anything else.**
>
> Golden Loop relocated from `prj-ai-pm-system-thinking-strategy/` to **`prj-ai-pm-system-design-thinking/`**. The product files (`product/`, `posts/`, the Phase B verdict and the five teardowns) moved; the **retired seven-module curriculum stayed behind** in the old folder. Any reference below that still points at `prj-ai-pm-system-thinking-strategy/` does so deliberately, and is labelled.
>
> Three facts in the previous version of this file are now **wrong** and have been corrected in place — **the curriculum is five modules over eight weeks with no M7** (evals is M5), **Golden Loop ships weeks 9–12 rather than week 8**, and **the Phase D council reserve of $8–15 no longer exists** (~$7 remains at the ceiling). Details in *Budget and calendar facts*. Do not plan against remembered numbers.

---

## To the session running this: who you are and where we stand

You are Fable, partnering with Sean Winslow (PM, not a developer — explain technical jargon and trade-offs in plain language before asking him to decide). This kickoff opens **Phase C of Golden Loop**: the wayfinder session that charts the full build territory as a map of numbered decision tickets, so the build has a ratified backlog before any code exists. Phases A and B are DONE. Do not re-litigate their decisions; build on them.

**This project is a learning vehicle first and a portfolio proof second.** Sean drafts predictions and maps first, every time (anti-cognitive-offloading rule); you research, structure, critique, and execute. Every significant decision cites a systems concept by name and lands in the public decision log.

## What happened in Phases A and B (read the artifacts, but here is the shape)

- **Phase A (partner session, 2026-08-16):** six locked decisions, ported to the public decision log as D1–D6 — the import wedge (PM-on-top-of-existing-tooling), Langfuse-first ingress with a neutral JSONL format underneath, the teaching layer (SHIPWRECK with a holdout title-fight beat), the name (Golden Loop stays), build-in-public cadence (decision log + two milestone posts), and the research spend (light, with ~$8–15 reserved for a Phase D council pre-mortem).
- **Phase B (falsification, 2026-08-17):** verdict **BUILD**, wedge re-scoped. The broad pitch ("PMs can't run eval labs without engineers") is DEAD — never use it. The surviving claim, verified against 15 named incumbents: **no tool ships sealed holdouts, enforced one-change promotion rounds, or required promote/reject decision records for offline evals.** Golden Loop is the discipline/governance layer on top of existing trace tooling, not another eval lab. A demand-side Gemini DR run corroborated the pain. Name collision check: clear. D7 records the verdict with two standing tripwires (incumbent ships the discipline before week 8 → rewrite differentiation as "early not alone"; hiring-manager mock majority says "neat side project" → positioning reopens before the PRD locks).
- **Pending human steps (check status with Sean at session start):** (1) the mock one-pager forward test — has Sean sent `product/mock-one-pager.md` to 2–3 recent AI-PM hiring managers, and what did they say verbatim? Their words go into D7's review. (2) Milestone post #1 (`posts/2026-08-17-milestone-post-1-the-kill-condition.md`) — published yet? Neither blocks the wayfinder from being drafted, but the mock result gates the Phase D PRD lock, so ticket it accordingly.

## Read these before the first question (in order)

1. `vault/20_projects/prj-ai-pm-system-design-thinking/product/decision-log.md` — D0–D7, the standing decisions and their falsifiers. The wayfinder must not contradict a lock; a change is a new SUPERSEDES-style entry, never a silent drift.
2. `vault/20_projects/prj-ai-pm-system-design-thinking/research/2026-08-17-phase-b-falsification-verdict.md` — the re-scoped wedge, the scoreboard, the shelf-life honesty, the DR addendum. Per-tool evidence in `research/teardowns-2026-08-17/` (Langfuse's file matters most: it carries the importer feasibility notes — API surface, v3→v4 migration caution, legacy API sunset 2026-11-16).
3. `vault/20_projects/prj-ai-pm-system-design-thinking/product/kickoff-prompt-golden-loop.md` — the original roadmap (Phases A–G), the four standing council constraints, the non-negotiables, and the definition of done. All still binding.
4. **The curriculum changed underneath this project on 2026-08-17 — read both, in this order.**
   - `vault/20_projects/prj-ai-pm-system-design-thinking/curriculum/curriculum-map.md` — **the LIVE map. Five modules, not seven. There is no M7.** The evals content is now **M5 — Evidence & Operations**, and it has not been written yet (only M1 exists). The old program was consumed at M1 and rejected; it was rebuilt after a four-model council pre-mortem.
   - `vault/20_projects/prj-ai-pm-system-thinking-strategy/curriculum/m7-lesson-evals-metrics-loop-engineering.md` — **retired lesson, kept because its vocabulary IS the product's domain language**: golden dataset, improvement/holdout split, binary rubric, champion/challenger, target-budget-stall, promotion, decision record. The vocabulary survives intact. The module numbering does not.
   - **What this means for the wayfinder:** the "M7 capstone is the build's first artifact" plan still holds in substance — a golden dataset plus a binary rubric plus one champion/challenger round on the job-feed agent — but it is now **M5's capstone**, it lands later in the calendar (week 6–7, not week 3–4), and **it is still a wayfinder ticket that has not been done.** Do not assume the old timing.
5. `vault/20_projects/prj-ai-pm-system-design-thinking/product/mock-one-pager.md` — the product one-pager; its five-gate loop (Capture → Seal → Challenge → Title fight → Record) is the closest thing to a v1 feature list that exists.
6. `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` — where tickets live (GitHub Issues on `seanwinslow28/code-brain` via `gh`) and the canonical label vocabulary.

## What Phase C produces

A **ratified wayfinder map**: the full build territory charted as numbered decision tickets in the GitHub issue tracker — invariants named, dependencies drawn, sequenced against the build calendar (build proper = weeks 4–8, 5–8 hrs/week of Sean + Fable heavy lifting). The map is the build's backlog. Sean has run this practice before (the Company OS pattern); the map distinguishes:

- **Decided** (D0–D7) — carried as invariants, not tickets.
- **Decision tickets** — open calls that must be made, each with its owner (Sean decides / Fable proposes), its phase gate, and what it blocks. Known members from the open-questions ledger: SHIPWRECK's demo-dataset fiction (invented product vs. job-feed continuity); SHIPWRECK+Inspection-Desk combo in or out of v1 scope; the M7 capstone timing; the systems-map-before-PRD work items (CLD with degenerate-loop risk, leverage-point analysis, stakeholder-incentive map, pre-mortem ending in a disposition package — all Phase D, all Sean-pen-first); stack choice (Sean's comfort: Astro/React/TS; backend minimal); repo migration timing (Phase E rule: migrate to `/Users/seanwinslow/Code-Brain/golden-loop` once the map is ratified, clean history from commit one, public-repo hygiene); the "runs its own medicine" wiring (Golden Loop's own golden dataset + challenger rounds — no decorative evals); Langfuse self-host + job-feed instrumentation; the neutral trace format spec; the 2-min walkthrough production; the case study. **Plus the three added 2026-08-17 — see below; they are mandatory tickets, not optional polish.**
- **Build tickets** — work items that follow mechanically from decisions, labeled per the triage vocabulary (`ready-for-agent` vs `ready-for-human`).
- **Tripwires** — D7's two falsifiers and D2's integration-budget fallback, carried as scheduled checks, not vibes.

## Three mandatory additions (2026-08-17) — the PM-signal gaps

A four-model council pre-mortem run on the rebuilt curriculum raised one collateral objection against Golden Loop, from Grok: *"an eval-first golden-dataset cockpit is an ML-engineer portfolio piece, not an AI-PM portfolio piece. An AI PM portfolio should show a product decision process — problem framing, killed alternatives, evals tied to a ship gate, cost model, failure UX. He can already build tooling. That is the one fact not in dispute."*

**Sean kept Golden Loop, and the objection was made against a one-line description the council never saw** — the Phase A partner session's PROPOSALS LOG is itself a decision record with killed alternatives and Sean's verbatim reasoning at every axis, which answers most of it. But three items on Grok's list were genuinely absent, and they are the three that read most as *product manager* rather than *builder*. Each is a wayfinder ticket:

1. **Cost model.** What Golden Loop costs to run — per trace, per eval round, and at 10k traces/month for a team. Nothing in Phases A or B says. Cost reasoning is the first thing 2026 system-design rubrics probe, and its absence is conspicuous in a tool whose entire pitch is disciplined evaluation. *Also delivers curriculum M5's artifact.*
2. **Failure UX.** What the product does when the Langfuse import breaks, the format drifts (note D3's v3→v4 migration caution and the 2026-11-16 legacy API sunset), a trace is malformed, or the judge is uncertain. **A product that teaches failure discipline and has no designed failure behaviour of its own will be read as a demo.** *Also delivers curriculum M4's artifact.*
3. **A written ship gate for Golden Loop itself.** "The product runs its own medicine" is a standing rule with no numbers attached. Give it thresholds, an error budget, and kill criteria — the same disposition package the program demands of every other decision. *Also delivers curriculum M5's artifact.*

None is a detour: all three double as curriculum artifacts, so building them is the coursework.

**One framing rule to carry into the map:** the **decision log is the front door of the portfolio, not an appendix.** The teaching layer is the hook, and it is five scenes of pixel-art carnage and micro-interaction stations — real craft, and craft Sean is *already* known for. The scarce signal is the judgment. If a hiring manager reads exactly one artifact, it should be the log. Sequence and polish accordingly.

**Process:** draft the map WITH Sean interactively (he predicts the territory first — ask him to sketch the ticket list from memory before you reveal yours, then diff). Stress-test the drafted map with the `grilling` skill before ratifying. On ratification, file the tickets via `gh`, update the decision log (the map itself is a decision: entry D8, systems concept named), append a CHANGELOG-worthy note if repo conventions ask for one, and update `vault/00_inbox/tickets.md`.

## Non-negotiables carried forward (verbatim force)

- **Systems map before PRD** (Phase D gate; the wayfinder tickets it, never skips it). Sean's hand on the pen.
- **The decision log is the portfolio spine** — public-facing, hiring-manager-readable, systems concepts by name, falsifiers and review dates on everything.
- **The product runs its own medicine** — no decorative evals.
- **Honesty rules** — public repo; real failures as the mechanism's discoveries; nothing from the PRIVATE LAYER paths; the dead broad pitch stays dead.
- **Plans are starting points, not walls** — when Sean brings a new idea mid-session, evaluate and fold it in.
- **Council constraints 1–4** from the original kickoff still stand (2-min walkthrough demo; M7 capstone is the seed artifact; handcrafted scenarios only, no LLM scenario generation; B2B AI-PM hiring-manager audience).

## Budget and calendar facts (so the map is honest)

**All three of these changed on 2026-08-17. The previous version of this file understated every one of them.**

- **Research budget — two workstreams now draw on the same approval, and the map must not double-count.** Golden Loop has spent **$6.92**; the rebuilt curriculum program spent **$10.66** (Gemini DR $2.80 + DR Max $7.00 + council premium $0.86). Combined that is **$17.58 against a $15–25 approval** — near the top of the range, not the middle. The ~$8–15 previously "reserved" for the Phase D council pre-mortem **no longer exists at that size**; roughly $7 remains at the ceiling. Either re-scope the Phase D council to a single premium run (~$0.90, which is what the last one actually cost) or ask Sean to raise the approval. **Do not plan against the old reserve.**
  - Fleet-wide Gemini caps for context (operative values in `agents-sdk/config.toml`, **not** the $20/$10 the skill doc quotes): **$50/month, $20/day.** August month-to-date is $21.00 of $50.
- **Sean's time: 5–8 hrs/week, and the curriculum now consumes eight weeks, not three.** Five modules over eight weeks. M1 is done (lesson written, audio arc generated 2026-08-17); M2–M5 are not. The evals module is **M5** and lands week 6–7.
- **Definition of done — the week-8 ship date is dead, and this is the correction that matters most to the map.** The curriculum honestly takes the full eight weeks, so **Golden Loop ships weeks 9–12**, not week 8. What week 8 produces is a **fully specified and partially built** product: the five curriculum artifacts *are* its planning spine (M1 → its PRD, M2 → golden-dataset spec, M3 → systems map, M4 → failure-UX spec + model card, M5 → launch criteria + cost model + incident runbook). Sequence the wayfinder against 9–12 for ship. Pretending otherwise is the exact over-scoping that killed the first curriculum.
- Unchanged at ship: live champion/challenger loop · public decision log · 2-min walkthrough video · case study on seanwinslow.com · playable teaching layer · migrated to its own repo.

## First moves for the session running this

1. Read the six artifacts above, in order.
2. Ask Sean the two status questions (mock forward test results; post #1 published?) and log anything he reports (verbatim, into D7's review if it's mock feedback).
3. Ask Sean to sketch his predicted ticket map cold, before showing yours (the anti-offloading rep — this IS a curriculum exercise in disguise).
4. Then run the wayfinder: diff his map against yours, work the open decisions one at a time with recommendations first, draw the dependencies, grill the result, ratify, file.
