---
title: "Architecture ratification package — campaign step 4 (awaiting Sean's lock)"
date: 2026-08-08
project: agent-company-founding
type: ratification-package
status: ratified
tags: [agent-company, architecture, ratification, L10-campaign]
---

# Architecture ratification package — the L10 gate

> **RATIFIED by Sean 2026-08-08** ("Signed."), together with the six amendments
> and six additions in the [second opinion](2026-08-08-architecture-second-opinion.md),
> which are incorporated by reference. D2/D4/D5 carry the standing condition
> that the canon-extraction test may reopen them if it falsifies
> canon-extractability. The [L10] research gate is satisfied; build may follow
> the amended sequencing.

Step 4 of the campaign. The [proposal v1](2026-08-08-architecture-proposal-v1.md)
went through an LLM-council pre-mortem (premium profile: Opus 4.7 + GPT-5.5 +
Gemini 2.5 Pro; the fourth member failed mid-run and the council continued
N-1; full transcript with cross-rankings at
[council premortem](2026-08-08-architecture-proposal-v1-council-premortem.md);
cost $0.54). This package folds every council amendment into final proposed
text. **Nothing below is locked until Sean ratifies — [L10] holds; no company
code before that signature.**

## Council verdict in one view

| Decision | Council verdict | Disposition here |
|---|---|---|
| D1 Release-gate contract | **Unanimous lock** ("most defensible piece of the design") | As written |
| D2 Deterministic pipeline | Lock | As written |
| D3 Eval constitution | Lock with amendment | Amended (downgrade license, creator slices) |
| D4 Canon model | Lock with amendments (Claude+GPT-5.5 convergent v1-debt) | Amended (event ledger, snapshot, replay) |
| D5 Model routing | **Unanimous weakest — do not lock as written** | **Rewritten** |
| D6 Verification stack | Unanimous lock | As written |
| D7 Autonomy/permissions | Lock ("enforcement-parity is the load-bearing bit") | As written |
| D8 Orchestration | Lock with Gemini's API-boundary amendment | Amended |
| D9 Observability | Lock contingent on D11 | Amended (data minimization, cost-per-verdict) |
| D10 Founder envelope | Lock, stress-tested against D5 fix | Amended (meta-tooling hours tracked) |
| D11–D13 | Three non-overlapping missing decisions — ratify all three | **New** |

## Pre-lock condition (council's highest-leverage action)

**Run a canon-extraction test on 3 real creators' back-catalogs before final
lock of D2/D4/D5.** The council's shared dangerous-assumption finding: the
32-case spike proves drift *detection* works when canon is stated; it does not
prove canon is *extractable into a schema* from arbitrary creators' real
material ("canon is a vibe with load-bearing exceptions"). This is research
under [L10] (same class as the feasibility spike, $0-to-cheap) and it decides
how much work D2's deterministic layer can actually do. Candidate corpora:
Sean's own serials (P&P, Grandmaster) plus 2 external creators' public
back-catalogs.

## The decisions (final proposed text)

### D1 — Release-gate contract — UNCHANGED, unanimous lock
Pass / Drift / Needs Review with mandatory receipts; canon-update notes
first-class (a note covers only what it declares); advisory by default,
blocking per-creator opt-in per axis.

### D2 — Deterministic pipeline boundary — UNCHANGED
Coded state machine (ingest → normalize → bible-retrieve → deterministic
checks → judge → aggregate → verdict + receipts → trace); agents never
orchestrate; failed stage retries alone, 2-round cap. *Council note: how much
the deterministic layer carries depends on the canon-extraction test.*

### D3 — Eval constitution — AMENDED
As proposed (spike corpus seed → ~50 cases, capability/regression split,
stage-wise grading, pass^k on judge lane, production failures become cases,
pre-registered bars), PLUS: **the early suite is a regression harness, not
proof of market-grade quality** — it may not license model downgrades below
**200 cases per lane**, autonomy increases, or product claims; per-creator
eval slices (series × tolerance × canon maturity × modality) begin with the
first real users.

### D4 — Canon/context model — AMENDED (the convergent v1-debt fix)
Per-creator series bible as an **event-sourced canon ledger** (not loose
files): stable IDs for series/installment/character/canon-fact/reference-
exemplar/canon-update-event/evidence-artifact; typed events
(observed/inferred/confirmed/superseded/deprecated/declared); temporal +
scope fields (applies_from/to, arc/modality/exception scope); provenance
(source artifact + span/region, extractor model+version, confirmation state).
**Materialized current-canon snapshot rebuilt on write** (read path never
traverses the log). **Confirmation-decay**: facts older than N installments
demote to inferred pending re-confirmation. **Per-creator data boundary with
export/delete primitives specified now** (implementation may lag). **Replay
guarantee**: every verdict reproducible against the exact canon snapshot it
used. File format must migrate losslessly to SQLite/Postgres later.
Agent-proposes / creator-confirms stands (the system never invents canon).

### D5 — Model routing policy — REWRITTEN (unanimous weakest-as-written)
Ceiling-first routing stands, but the judge panel gets an **axis-specific
disagreement policy** instead of blanket disagreement→Needs Review:
- **Countable canon facts:** panel disagreement escalates to deterministic
  verification against the bible; only unresolvable conflicts reach Needs
  Review.
- **Visual identity drift:** disagreement produces severity bands
  (Pass-with-note / Watch / Drift), not automatic Needs Review.
- **Style/register drift:** Drift requires agreement or strong single-model
  evidence; disagreement defaults to Pass-with-note.
- **Declared canon changes:** resolved against the canon-update event scope.
Pre-registered **max Needs-Review rate ≤15% of production checks** as a
regression alarm (Needs Review is otherwise unfalsifiable in eval terms).
**No lane downgrade below 200 eval cases.** **Degraded-mode fallback:** the
local $0 fleet is not a production SPOF — batch lanes defer with typed
deferrals (BT5 pattern), but customer-facing lanes carry a bounded cloud
fallback with a per-incident budget line, pre-authorized in the cap policy.

### D6 — Verification stack — UNCHANGED, unanimous lock
Layered zero-trust; deterministic gates verify real artifacts; judge with
rubric + Unknown in fresh context; worker never self-approves;
remove-the-patch test check; agent-to-agent review always; human PR gate
until regression suite + rollback path exist; autonomy earned per-lane.

### D7 — Autonomy and permission matrix — UNCHANGED
Three permission profiles; tool risk tiers; Owner's Cards on every fleet
agent with runtime-wired kill switches; **enforcement parity** (non-Claude
agents get side effects only through runtime-mediated tools); HITL on
retry-cap breach and high-risk actions.

### D8 — Orchestration topology — AMENDED
Single-orchestrator default, code-orchestrated pipelines, named roles
(Orchestrator, Builder, Validator, Judge panel, Librarian, Watchdog), fan-out
as exception — PLUS: **all Orchestrator↔role communication over a versioned,
documented JSON task/result schema; the Orchestrator never reaches into a
role's internal state** (keeps roles replaceable; prevents the v1 god-agent),
and fan-out carries an explicit **per-run token budget**, not just a topology
rule.

### D9 — Observability operating loop — AMENDED
One Arize trace schema, weekly 60-min founder failure review, overrides feed
evals, per-lane cost attribution — PLUS: **data minimization is part of the
schema**: traces store redacted references and evidence IDs, never raw
manuscripts/unpublished images (D11 governs what may leave the system); add
**cost-per-verdict** as a first-class metric alongside monthly rollups.

### D10 — Solo-founder operating envelope — AMENDED
As proposed (named weekly lanes, review inbox in the first runtime slice,
≤20% meta-tooling budget, per-lane caps, founder owns rollback) — PLUS:
**meta-tooling hours are logged weekly against the 20% line** (Gemini's
force-sink warning made falsifiable: if the fleet is consuming the budget
instead of multiplying it, the log shows it by week 4, not month 6).

### D11 — Creator data, IP, and provider boundary — NEW (blocks first payer)
Decide before any paying creator: what is stored; what is sent to which
closed-model provider and under what retention terms; an opt-in
local/open-only processing tier; retention periods for uploads, traces,
receipts, derived canon; deletion/export as product primitives; tenant
isolation; creator owns their canon/bible/outputs; provider training-use
prohibited; founder-visibility policy; incident response. The product's
customers upload exactly the material they most protect — improvised answers
here cost the sale or create legal debt.

### D12 — Dispute → eval ingestion contract — NEW (blocks WAU ramp)
Every verdict carries a one-click dispute with a required taxonomy tag
(missed-drift / false-drift / bad-receipt / canon-was-declared); disputes
land in the review inbox with a **7-day resolution SLA**; resolved disputes
become eval cases within one review cycle; per-creator dispute rate is a
tracked calibration metric. This is what makes the month-6 "evals governing
quality" bar real instead of synthetic.

### D13 — State and artifact promotion — NEW (blocks the 30-day window)
Unified versioning across the four moving artifact families (fleet
agents/config, routing table, eval corpus, canon bibles): every trace records
the exact version tuple that produced it, and any failing trace is
reproducible from that tuple alone. Without this, one day-15 regression eats
the entire ≤10-hr oversight budget and the 30-day maintenance bar dies.

## Sequencing (chairman's, adopted)

1. Canon-extraction test on 3 real creators' back-catalogs.
2. Lock D1, D2, D6, D7, D8.
3. Lock D4 as amended.
4. Lock D5 as rewritten.
5. Ratify D11/D12/D13 before their respective month-6 gates.
6. Lock D3, D9, D10 last (they're constrained by the above).

Then: step 5 (Arize eval-stack design, consuming D3/D9/D12/D13) → step 6
(wayfinder ticket map) → build.

## Provenance

Proposal: [architecture-proposal-v1](2026-08-08-architecture-proposal-v1.md) ·
Council transcript: [council premortem](2026-08-08-architecture-proposal-v1-council-premortem.md) ·
Inputs: [spike (GO)](2026-08-08-vision-drift-feasibility-spike-go-no-go.md) ·
[literature review](2026-08-08-software-factory-literature-review.md) ·
[groundwork audit](2026-08-08-groundwork-v1-audit.md) ·
Decision record: `~/.creative-harness/partner-sessions/2026-08-07-agent-company-founding.md`
