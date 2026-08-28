# Agent-company founding — eval-stack design + wayfinder map (continuation)

**Where we are:** the entire [L10] research front-load completed 2026-08-08 in
one campaign day (~$2.20 total): feasibility spike (GO) → software-factory
literature review → groundwork v1 audit → architecture ratified by Sean with
council pre-mortem + Fable 5 second opinion folded in → canon-extraction test
(PASS, all four pre-registered bars; D2/D4/D5 stand). Every research gate is
closed. What remains before build: **step 5 (eval-stack implementation
design)** and **step 6 (wayfinder ticket map for the thin vertical slice)**.

## Read these first (the record governs)

1. **Ratified architecture:** [vault/20_projects/research/2026-08-08-architecture-ratification-package.md](../../vault/20_projects/research/2026-08-08-architecture-ratification-package.md)
   — thirteen decisions D1-D13, RATIFIED banner at top. The
   [second opinion](../../vault/20_projects/research/2026-08-08-architecture-second-opinion.md)
   is incorporated by reference — its six amendments (A1-A6) and six additions
   are binding: judge panel = 2 diversified judges doing disagreement
   detection (temp 0, version-pinned, pairwise-vs-reference, κ/α metrics, OCR
   escape); durable execution (watchdog, auto-resume, idempotency keys,
   agent-to-agent loops banned, per-run kill switches); mid-tier orchestrator
   seat; detect→crop→embed(DINOv2)→per-series-anchor visual recipe;
   Phoenix OSS self-hosted; Needs-Review alarm defined on actionable-items-
   per-installment; onboarding cost ceiling; modality order visual→text→video;
   named month-6 autonomy lanes; museum-pattern build-in-public; STOP ADDING
   DECISIONS.
2. **Extraction test** (closed the last condition): [vault/20_projects/research/2026-08-08-canon-extraction-test.md](../../vault/20_projects/research/2026-08-08-canon-extraction-test.md)
   — includes the adopted D4 policy refinement (era-scoped defaults, two-era
   corroboration, occasion-wear states) and the boundary both spikes agree
   on: models own structure/judgment, stated canon facts own fine attributes.
3. **Supporting record** (consult as needed): drift spike
   ([go/no-go memo](../../vault/20_projects/research/2026-08-08-vision-drift-feasibility-spike-go-no-go.md)),
   [literature review](../../vault/20_projects/research/2026-08-08-software-factory-literature-review.md),
   [groundwork audit](../../vault/20_projects/research/2026-08-08-groundwork-v1-audit.md),
   [council transcript](../../vault/20_projects/research/2026-08-08-architecture-proposal-v1-council-premortem.md),
   fresh-research reports in
   [2026-08-08-architecture-second-opinion/](../../vault/20_projects/research/2026-08-08-architecture-second-opinion/).
   Partner-session decision record (L1-L12): `~/.creative-harness/partner-sessions/2026-08-07-agent-company-founding.md`.

## Standing constraints

[L2] the fleet builds and operates the product; factory is internal infra
wrapped in build-in-public. [L6] month-6 compound bar, autonomy-proof primary.
[L7] ~25 hrs/week co-primary with job hunt, ≤$250/mo opex, quality over speed.
[L10] satisfied — build may follow the amended sequencing. Product: multimodal
series-consistency keeper (D1 contract: Pass/Drift/Needs-Review with receipts,
advisory default). Groundwork = governance layer as-is (files, not engine);
runtime is a separate layer reading groundwork artifacts as config; company
code lives in its own new repo (NOT in code-brain, NOT in groundwork).

## Step 5 — eval-stack implementation design

Mostly settled by A5 + D3/D9/D12/D13; produce the concrete design doc:

- **Phoenix OSS self-hosted** (Docker on the Mac Mini): Postgres-backed
  (`PHOENIX_SQL_DATABASE_URL`), explicit `PHOENIX_WORKING_DIR`, explicit
  retention days, pinned image, local auth. Client-side masking/redaction
  before spans export (implements D11 data minimization — no raw creator
  manuscripts/images in traces). Alerting = cron + eval + Pushover (existing
  fleet pattern); optionally AX Free (25k spans/mo) for the customer-facing
  production slice only. Span sampling/routing design up front.
- **One trace schema, both layers** (fleet-evals + product-evals): model +
  config versions, retrieved evidence IDs, tool calls, tokens, cost, latency,
  stage outputs, grader results, retries, disposition, human override —
  plus the D13 version tuple (fleet-config / routing-table / eval-corpus /
  canon-bible versions) on every trace, and cost-per-verdict as a metric.
- **Eval seed:** the 32-case drift-spike corpus
  ([vault/20_projects/research/2026-08-08-vision-drift-spike/](../../vault/20_projects/research/2026-08-08-vision-drift-spike/))
  + extraction-test materials
  ([2026-08-08-canon-extraction-test/](../../vault/20_projects/research/2026-08-08-canon-extraction-test/)).
  Structure per D3: capability vs regression suites, stage-wise grading
  (extraction / detection / verdict), pass^k on the judge lane, evals as
  pytest in CI. Judge calibration per A1 (gold set with known answers, κ/α,
  monthly re-runs, judge model+prompt-hash pinned).

## Step 6 — wayfinder ticket map for the thin vertical slice

The slice (scope is ratified — do not widen): **one creator (Sean), one
series, stills + text modalities, advisory drift report with receipts,
Phoenix-traced end to end**, dogfooded on Sean's serials. Chart the map with
the wayfinder/mattpocock skills the way groundwork's map was charted (GitHub
issues, decision tickets, blocking edges) — in the NEW company repo (name
TBD — a naming ticket belongs on the map; check availability before locking).
The map should cover at minimum: repo scaffold + groundwork instance
generation (dogfooding the interview — the company is groundwork's first
real adopter), the D2 pipeline state machine with durability requirements,
the canon-ledger store (D4 schema incl. the extraction-test refinements),
judge lane (A1 requirements), Phoenix deployment (step 5 doc), eval-seed
migration, review inbox (D10: first runtime slice), Owner's Cards for the
initial fleet roles (D8: Orchestrator, Builder, Validator, Judge panel,
Librarian, Watchdog), and the build-in-public capture layer. Respect the
meta-tooling budget (≤20% of build hours) when sizing tickets.

## Conventions for the session

Research/campaign artifacts → `vault/20_projects/research/` (commit vault
yourself on the MBP per memory). Deferred work → one-line ticket under
`## Todo` in [vault/00_inbox/tickets.md](../../vault/00_inbox/tickets.md)
(the campaign ticket is there — update it as steps close). Cross-cutting
prompts → `docs/prompts/`. Pre-register bars before any new empirical run.
Sean ratifies anything that changes a ratified decision; everything else,
proceed autonomously and report with receipts.
