# Agent-company BUILD — ticket #6: the canon-ledger store (continuation)

**Where we are:** ticket #5 CLOSED 2026-08-10. D8's six fleet seats are
carded and governed (`roles/`), the kill switches trip under test, the
task/result schema v1 is documented, and R5's enforcement-gap register is
open with 25 rows. Two governed change-proposals signed by Sean the same
day. Commits `2214611` (build), `a5e2200` (sign-off), `d40043b` (G18
correction) — CI green, validator 0 errors stateless and `--diff a632f31`,
60 tests. Map #1's Decisions-so-far carries the resolution pointer.
**This session picks up the build frontier.**

## The company repo (all company work happens THERE, not in code-brain)

`seanwinslow28/driftgate` — private; name is a provisional codename; local
clone at `/Users/seanwinslow/Code-Brain/driftgate`.

- Wayfinder map: issue **#1**; frontier = first open child in map order
  with no open blocker and no assignee. **Verify the frontier with `gh`
  before claiming** (native sub-issue blocking relations are the truth) —
  expected frontier: **#6 Canon-ledger store (D4 as amended +
  extraction-test refinements)**, size **L**. Its blockers #3 and #4 are
  both closed. #7 and #8 are both blocked ON #6, so this ticket unblocks
  two-thirds of the remaining slice.
- Claim = `--add-assignee seanwinslow28`; resolve = comment answer → close
  → pointer appended to map #1's Decisions-so-far.
- **#2 (naming) stays PARKED** — final lock happens in the design/logo
  phase. Do NOT reopen.

## What the repo now contains (read before building)

1. `AGENTS.md` — the routing file. Read it first; it inherits every agent
   into the standing rules, and it now carries the `roles/` entry, the role
   table, and the **two proposal routes**.
2. `interview/` — 8 frozen layers, never edited; corrections are new
   layers. Layer 2 carries the master governance artifacts verbatim: the
   **45-item forbidden list**, the **two-scope pause condition** (30
   triggers + 12 binding semantics), the **three-tier retirement
   condition** (Sean is sole confirmation authority).
3. `ontologies/` + `skills/` + `governance/` + `memory/` — the generated
   instance. 4 skill work packages, all `provisioned: no`. 5 founding rules.
4. **`roles/`** (new, ticket #5) — six seats: orchestrator (mid-tier per
   A3), builder, validator, judge-panel, librarian, watchdog
   (deterministic). All `provisioned: no`. **The librarian's card is the
   one this ticket must satisfy** — read `roles/librarian/role-card.md`
   before writing any store code; its forbidden deltas ARE this ticket's
   acceptance criteria in prose form.
5. **`src/driftgate/`** (new) — `roles.py` (card loader + R1/R2 promotion
   gate), `killswitch.py` (per-run meter, all-of-run by construction),
   `task_result.py` (strict reference-only envelopes), `escalation.py`
   (nine coded triggers), `permissions.py` (tool registry + three
   profiles), `frontmatter.py`. Zero third-party dependencies — keep it
   that way unless there's a real reason not to.
6. **`governance/enforcement-gaps.md`** (new) — R5's register, 25 rows.
   **Ticket #6 must add its own rows and flip G22** (`append-only and
   content-addressed write APIs`, currently `instruction-strength`,
   tracked to #6) to whatever is then true. Use the register's honest
   vocabulary: `enforced` / `enforced-unreached` / `blocking-in-ci` /
   `instruction-strength`. `enforced-unreached` is not a synonym for
   enforced.
7. `docs/adr/ADR-001-system-of-record.md` — **the spec this ticket
   implements.** §1 canon ledger (append-only JSONL + rebuilt YAML
   snapshot, snapshot content hash IS the D13 `canon_bible` stamp), §3
   content-addressed evidence, §4 `tenants/<creator-id>/` + creator-keyed
   rows, §5 the binding export/delete contract. Data root
   `~/.driftgate/data/`, outside the repo by construction.
8. `docs/schemas/task-result-v1.md` — the D8 channel contract. Anything
   the ledger returns to a stage travels as a **reference**, never inline
   content.

## Governing record (the record governs; cite, don't restate)

- Ratification package (D1-D13) + second opinion (A1-A6, binding):
  `code-brain vault/20_projects/research/2026-08-08-architecture-*`
- **Canon-extraction test — the refinement source for this ticket:**
  `2026-08-08-canon-extraction-test.md` (era-scoped defaults vs timeless
  facts, two-consecutive-era corroboration, occasion-wear states)
- Eval-stack design (step 5): `2026-08-08-eval-stack-implementation-design.md`
- Groundwork engine (validator + schemas):
  `/Users/seanwinslow/Code-Brain/groundwork` — pull-only; friction goes
  upstream as issues, never patches from here. Six filed so far (#24–#30).

## THE TASK — ticket #6 (after verifying it is the frontier)

Read the ticket body first; it is specific. In summary — the event-sourced
canon ledger per D4 as amended:

- **Stable IDs:** series / installment / character / canon-fact /
  reference-exemplar / canon-update-event / evidence-artifact.
- **Typed events:** observed / inferred / confirmed / superseded /
  deprecated / declared. Append-only — a correction is a new superseding
  event, never an edit (forbidden 16).
- **Temporal + scope fields:** `applies_from`/`applies_to`, arc / modality
  / exception scope.
- **Provenance on every event:** source artifact + span or region,
  extractor model + version, confirmation state.
- **Materialized snapshot rebuilt on write** — the read path never
  traverses the log. Where log and snapshot disagree, the log wins.
- **Confirmation-decay:** facts older than N installments demote to
  inferred pending re-confirmation.
- **Replay guarantee:** every verdict reproducible against the exact
  snapshot it used (D13).
- **Extraction-test refinements as encoded policy**, not prose: era-scoped
  defaults vs timeless facts; two-consecutive-era corroboration before an
  appearance evolution overwrites a default; occasion-wear as first-class
  states.
- **Lossless migration to SQLite/Postgres** must stay possible (ADR-001 §1).
- **Agent-proposes / creator-confirms stubbed** — the system never invents
  canon, and nothing but a creator action can produce a `confirmed` event
  (forbidden 14, 15).

**Acceptance (from the ticket):** schema doc + store module · snapshot
rebuild + replay round-trip tested · refinement policies encoded ·
agent-proposes/creator-confirms interface stubbed.

**Also required by the work already landed:**

- Tenant isolation proven by a test asserting no read crosses tenants
  (ADR-001 §4, forbidden 10). The librarian's pause delta makes a suspected
  cross-tenant read a pause-everything event.
- Content-addressed evidence immutable by construction (forbidden 17).
- Enforcement-gap rows added/updated, G22 revisited honestly.
- **Nothing under `~/.driftgate/data/` is ever committed.** Company code in
  the repo; creator content never.

## How governed changes land here

The repo is a governed root under the pin. Two routes, and the split
matters:

- `proposals/` — the groundwork engine's route. A proposal's `target` MUST
  be a `skills/` path or `governance/constitution/`; anything else is a
  validator ERROR.
- `governance/change-proposals/` — driftgate's own route for role cards,
  permission profiles, the enforcement-gap register, and the schemas. Same
  contract (diff, reason, evidence, blast radius, Sean's sign-off), and it
  is append-only rather than pending-only.

Nothing enforces either for those paths (register row G25; upstream
groundwork #30). Follow it anyway.

Validate with
`python3 /Users/seanwinslow/Code-Brain/groundwork/scripts/validate.py .`
and `--diff a632f31` after any governed change. **CI diff bases must be
`a632f31` or later** — a diff spanning the generation commit false-fires
the proposal tripwire (groundwork #28). Keep CI green:
`uv run ruff check .` and `uv run pytest` (currently 60 passing).

## Standing constraints

[L2] fleet builds and operates; build-in-public wraps it. [L6] month-6
compound bar, autonomy-proof primary. [L7] ~25 hrs/week co-primary with the
job hunt, ≤$250/mo opex, quality over speed. Slice scope ratified — one
creator (Sean), one series, stills + text, advisory drift report with
receipts, Phoenix-traced — **do not widen.** Meta-tooling ≤20% of build
hours. STOP ADDING DECISIONS (addition 6): remaining unknowns are measured
during the slice.

## Sean-confirmed decisions this build must honor (do not reopen)

- All 8 interview checkpoints (2026-08-09/10) — the layers are the record.
- Skills and roles stay `provisioned: no` until each actually runs under
  the executor/CI; flipping one is a governed change with evidence.
- Backup owner is "no one — work pauses" until a trusted human joins
  (then: a NEW layer, never an edit).
- Only Sean confirms retirement triggers; only Sean resolves pause packets;
  Sean owns every merge, publication, production action, and above-cap
  spend.
- Shadow rate $100/hr; baselines in `memory/` are the comparison floor.
- **Ticket #5's five implementation calls, signed 2026-08-10:** profile
  names (`observer`/`worker`/`escalator`) and tiers T0–T3; `notify.sean` as
  the single allowlisted T3 tool, watchdog only; per-seat model tiers; the
  validator backed by "code review and release" with the merge bit staying
  Sean's; `roles/` as a top-level directory.
- **G18 (branch protection) is closed as blocked, not deferred.** Private
  repo on a Free GitHub plan — protection and rulesets both 403. Revisit
  only when the fleet holds its own credential. Do not re-litigate, and do
  not purchase anything (forbidden 37).

## Known open, not this ticket

- **G17** (mediated tool layer) and **G19** (secret broker) are unbuilt,
  buildable, and have no child on the map. Most of #5's machinery is
  `enforced-unreached` until #8's executor calls it. Raise with Sean if a
  map child seems warranted; don't add one unilaterally.
- Interview second pass (parked, in the manifest): corpus & ground-truth
  stewardship deep record · review-inbox deep record · the channel question
  (P&P vs a dedicated driftgate channel).

## Conventions

Company work tracks in driftgate issues; research artifacts →
`vault/20_projects/research/` (commit vault yourself on the MBP); deferred
code-brain work → one-line ticket under `## Todo` in
`vault/00_inbox/tickets.md`. Sean ratifies anything that changes a ratified
decision; everything else, proceed autonomously and report with receipts.
Sean is a PM, not a dev — explain jargon and trade-offs in plain language
before asking him to decide. Check claims before making them: #5's closing
comment called branch protection a two-minute setting without testing it,
and it was wrong twice over.
