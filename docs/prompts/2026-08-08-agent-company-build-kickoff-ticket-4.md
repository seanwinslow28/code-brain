# Agent-company BUILD kickoff — ticket #4: scaffold + groundwork interview (continuation)

**Where we are:** the research campaign is CLOSED (2026-08-08, ~$2.75 total
across two days). Everything is ratified and mapped: feasibility spike (GO) →
literature review → groundwork audit → architecture ratified (D1-D13 + six
amendments A1-A6 + six additions, incorporated by reference) → canon-extraction
test (PASS all four bars) → step-5 eval-stack implementation design → step-6
wayfinder map charted. The company repo exists and the first build decision
(ADR-001) is committed. **This session starts the build.**

## The company repo (all company work happens THERE, not in code-brain)

`seanwinslow28/driftgate` — **private; the name is a provisional codename.**
- Wayfinder map: issue **#1**; children #2-#18 as native sub-issues with
  native blocking dependencies. Conventions per
  [docs/agents/issue-tracker.md](../agents/issue-tracker.md) (claim =
  `--add-assignee`; resolve = comment answer → close → pointer appended to
  the map's Decisions-so-far).
- **#3 (system of record) is RESOLVED** — grilling session 2026-08-08, five
  Sean-confirmed decisions, recorded in-repo at
  `docs/adr/ADR-001-system-of-record.md`: (1) canon ledger = per-creator
  append-only JSONL events + rebuilt YAML snapshot (snapshot hash = the D13
  `canon_bible` stamp); (2) operational records = one shared SQLite DB, A2
  idempotency keys as UNIQUE constraints; (3) receipt evidence =
  content-addressed blobs under the tenant folder, fingerprints in verdict
  rows, never in Phoenix; (4) tenancy = `tenants/<creator-id>/` + keyed rows,
  cascade deletes, cross-tenant test; (5) export/delete contract binding now,
  data root `~/.driftgate/data/` outside the repo.
- **#2 (naming) is OPEN but PARKED by Sean's direction:** shortlist locked
  (partner-session sidecar L2) — **Selfsame, Onionskin, Recog/Rekog** — with
  the final lock deferred to the design/logo phase, where all three get drawn
  and felt out using anima's `art-department` skill
  (`/Users/seanwinslow/Code-Brain/anima/.claude/skills/art-department`) + the
  Higgsfield CLI, then the full availability sweep runs on the winner
  (Rekog must clear the Amazon Rekognition adjacency). Do NOT reopen naming
  outside that phase.

## THE TASK — ticket #4: repo scaffold + groundwork instance generation

The sole unblocked build ticket; six tickets sit directly behind it
(#5, #6, #7, #8, #9, #11, #17 all unblock or shed a blocker when it closes).
Claim it first (`gh issue edit 4 -R seanwinslow28/driftgate --add-assignee
seanwinslow28`). Scope per the ticket:

1. **Run the groundwork interview for real** — the company is groundwork's
   FIRST real adopter (the audit found the interview has only ever run
   simulated). Groundwork lives at `/Users/seanwinslow/Code-Brain/groundwork`
   (see `interview/`, `ontologies/`, `governance/`). **The interview needs
   Sean present** — it is a sitting, not a background job. Output: the
   company's governance instance (ontologies, org memory, constitution
   artifacts) committed into driftgate as **files the runtime reads as
   config** — groundwork stays a governance layer, not an engine.
2. **Scaffold the runtime skeleton around it:** Python project, pytest, CI
   green, `infra/`, `evals/`, lint.
3. **File interview friction upstream** as issues on the groundwork repo —
   never patch groundwork from inside driftgate work.

Acceptance (from the ticket): groundwork instance committed · runtime
skeleton with green CI · friction issues filed upstream.

## Read these first (the record governs)

1. [Ratification package](../../vault/20_projects/research/2026-08-08-architecture-ratification-package.md)
   (D1-D13, RATIFIED) + [second opinion](../../vault/20_projects/research/2026-08-08-architecture-second-opinion.md)
   (A1-A6 + additions — binding, incorporated by reference).
2. [Eval-stack design](../../vault/20_projects/research/2026-08-08-eval-stack-implementation-design.md)
   (step 5 — the spec tickets #11/#12/#14/#16 implement).
3. [Canon-extraction test](../../vault/20_projects/research/2026-08-08-canon-extraction-test.md)
   (D4 refinements: era-scoped defaults, two-era corroboration, occasion-wear).
4. driftgate `README.md` + `docs/adr/ADR-001-system-of-record.md` + map #1.
5. [Groundwork v1 audit](../../vault/20_projects/research/2026-08-08-groundwork-v1-audit.md)
   — read before the interview: it maps what groundwork satisfies vs what the
   runtime must own (enforcement parity caution lives here).

## Standing constraints

[L2] fleet builds and operates the product; build-in-public wraps it.
[L6] month-6 compound bar, autonomy-proof primary. [L7] ~25 hrs/week
co-primary with the job hunt, ≤$250/mo opex, quality over speed. Slice scope
is ratified — one creator (Sean), one series, stills + text, advisory drift
report with receipts, Phoenix-traced — **do not widen.** Meta-tooling ≤20% of
build hours (#17 counts against it). STOP ADDING DECISIONS (addition 6):
remaining unknowns are measured during the slice, not ratified.

## Conventions

Research/campaign artifacts → `vault/20_projects/research/` (commit vault
yourself on the MBP per memory). Deferred code-brain work → one-line ticket
under `## Todo` in [vault/00_inbox/tickets.md](../../vault/00_inbox/tickets.md);
company work tracks in driftgate issues. Partner-session decision record:
`~/.creative-harness/partner-sessions/2026-08-07-agent-company-founding.md`
(L1-L12) + `2026-08-08-company-naming.md` (naming shortlist L2). Sean ratifies
anything that changes a ratified decision; everything else, proceed
autonomously and report with receipts.
