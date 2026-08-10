# Agent-company BUILD — ticket #5: Owner's Cards + kill switches for the fleet roles (continuation)

**Where we are:** ticket #4 CLOSED 2026-08-10. The groundwork interview ran
FOR REAL (groundwork's first non-simulated adopter — 8 frozen layers in
`driftgate/interview/`, all checkpoints Sean-approved), the governance
instance is generated and validator-clean (commit `a632f31`, pin @ engine
`8479480`), the runtime skeleton has green CI (`a4d0d17`), and 6 friction
issues were filed upstream (groundwork #24–#29). Map #1's Decisions-so-far
carries the resolution pointer. **This session picks up the build frontier.**

## The company repo (all company work happens THERE, not in code-brain)

`seanwinslow28/driftgate` — private; name is a provisional codename; local
clone at `/Users/seanwinslow/Code-Brain/driftgate`.

- Wayfinder map: issue **#1**; frontier = first open child in map order
  with no open blocker and no assignee. **Verify the frontier with `gh`
  before claiming** (native sub-issue blocking relations are the truth) —
  expected frontier: **#5 Owner's Cards + kill switches for the initial
  fleet roles (D7/D8, A3)**. Claim = `--add-assignee seanwinslow28`;
  resolve = comment answer → close → pointer appended to map #1's
  Decisions-so-far.
- **#2 (naming) stays PARKED** — final lock happens in the design/logo
  phase. Do NOT reopen.

## What the repo now contains (read before building)

1. `AGENTS.md` — the routing file. Read it first; it inherits every agent
   into the standing rules.
2. `interview/` — 8 frozen layers. Layer 2 carries the master governance
   artifacts verbatim: the **45-item forbidden list**, the **two-scope
   pause condition** (30 triggers + 12 binding semantics incl. loud-pause
   and re-verify-on-resume), the **three-tier retirement condition** (Sean
   is sole confirmation authority). Layers 3-5 carry per-skill deltas.
   **Frozen layers are never edited** — corrections are new layers.
3. `ontologies/` + `skills/` + `governance/` + `memory/` — the generated
   instance. 4 skill work packages, all `provisioned: no` until the
   runtime that mediates them exists. 5 founding rules (tools-before-jobs,
   roles-before-agents, memory-is-governed, context-budgets,
   ambient-instructions-are-not-guardrails).
4. `docs/generation-report-2026-08-10.md` — what shipped, what couldn't,
   and the `--diff` boundary note: **CI diff bases must be commit
   `a632f31` or later** (a diff spanning the generation commit false-fires
   the proposal tripwire; that's groundwork issue #28).
5. `docs/adr/ADR-001-system-of-record.md` — storage architecture (JSONL
   canon ledger + snapshot, shared SQLite, content-addressed evidence,
   `tenants/<creator-id>/`, data root `~/.driftgate/data/` outside the
   repo).

## Governing record (the record governs; cite, don't restate)

- Ratification package (D1-D13) + second opinion (A1-A6 + additions,
  binding): `code-brain vault/20_projects/research/2026-08-08-architecture-*`
- Eval-stack design (step 5): `2026-08-08-eval-stack-implementation-design.md`
- Canon-extraction test: `2026-08-08-canon-extraction-test.md`
- Groundwork engine (validator + schemas): `/Users/seanwinslow/Code-Brain/groundwork`
  — pull-only; friction goes upstream as issues, never patches from here.

## THE TASK — ticket #5 (after verifying it is the frontier)

Owner's Cards + kill switches for the initial fleet roles (D7/D8, A3).
The interview already produced the substrate: the master lists, the
per-skill deltas, and four Owner's Cards in `skills/*/owner-card.md`.
What #5 adds (per its ticket text — read it first):

- The named fleet roles (Orchestrator, Builder, Validator, Judge panel,
  Librarian, Watchdog — D8) as governed artifacts the runtime reads as
  config, honoring founding rules R1 (tools before jobs) and R2 (roles
  before agents): each role needs its ontology-backed definition,
  non-overlapping description, tool loadout, and permission profile
  BEFORE its first production run.
- Kill switches wired per D7: runtime-wired, not prose — where the
  runtime doesn't exist yet, register the gap honestly in the
  enforcement-gap register per R5 and the tracked-gap framing (adopted at
  the layer-2 checkpoint).
- A3 constraint: the orchestrator seat is a mid-tier model doing bounded
  leaf-work planning; frontier models sit in judge/hard-reasoning lanes;
  escalation triggers live in code.
- Governed changes to `skills/`, `governance/`, or cards are **escalating**
  under the pin: they land via `proposals/` with Sean's sign-off (the
  repo is a governed root since generation).

Acceptance: per the ticket on the map. Validate with
`python3 /Users/seanwinslow/Code-Brain/groundwork/scripts/validate.py .`
(and `--diff a632f31`) after any governed change; keep CI green.

## Standing constraints

[L2] fleet builds and operates; build-in-public wraps it. [L6] month-6
compound bar, autonomy-proof primary. [L7] ~25 hrs/week co-primary with
the job hunt, ≤$250/mo opex, quality over speed. Slice scope ratified —
one creator (Sean), one series, stills + text, advisory drift report with
receipts, Phoenix-traced — **do not widen.** Meta-tooling ≤20% of build
hours. STOP ADDING DECISIONS (addition 6): remaining unknowns are
measured during the slice.

## Sean-confirmed decisions this build must honor (do not reopen)

- All 8 interview checkpoints (2026-08-09/10) — the layers are the record.
- Skills stay `provisioned: no` until each actually runs under the
  executor/CI; flipping one is a governed change with evidence.
- Backup owner is "no one — work pauses" until a trusted human joins
  (then: a NEW layer, never an edit).
- Only Sean confirms retirement triggers; only Sean resolves pause
  packets; Sean owns every merge, publication, production action, and
  above-cap spend.
- Shadow rate $100/hr; baselines in `memory/` are the comparison floor.

## Interview second pass (parked, in the manifest — do not do now)

Corpus & ground-truth stewardship deep record · review-inbox deep record ·
the channel question (P&P vs dedicated driftgate channel).

## Conventions

Company work tracks in driftgate issues; research artifacts →
`vault/20_projects/research/` (commit vault yourself on the MBP);
deferred code-brain work → one-line ticket under `## Todo` in
`vault/00_inbox/tickets.md`. Sean ratifies anything that changes a
ratified decision; everything else, proceed autonomously and report with
receipts. Sean is a PM, not a dev — explain jargon and trade-offs in
plain language before asking him to decide.
