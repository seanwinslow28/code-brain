---
title: "Eval-stack implementation design — campaign step 5"
date: 2026-08-08
project: agent-company-founding
type: design
status: final
tags: [agent-company, evals, phoenix, observability, L10-campaign, D3, D9, D12, D13]
---

# Eval-stack implementation design (step 5)

This is the concrete implementation design the ratified architecture calls
for. It consumes: **A5** (Phoenix OSS self-hosted), **D3** (eval
constitution), **D9** (observability loop + data minimization), **D12**
(dispute→eval ingestion), **D13** (version-tuple promotion), **A1** (judge
panel requirements), **A2** (durability fields), and second-opinion
**addition 1** (Needs-Review denominator). Nothing here changes a ratified
decision; where a choice was left open, the choice is made and marked
**[impl choice]**. Fresh-source grounding:
[Arize research report](2026-08-08-architecture-second-opinion/research-arize-stack.md).

## 0. Two layers, one stack

- **Fleet-evals** — grade the agents that build and operate the company
  (Builder, Validator, Orchestrator, Librarian, Watchdog).
- **Product-evals** — grade the product pipeline itself (extraction,
  detection, judge, verdict). These ARE the product.

Both layers emit the same trace schema (§3) to the same Phoenix instance,
separated by Phoenix **projects**, and both are graded by pytest suites over
the same versioned corpus store (§5). One stack, two projects — no parallel
tooling.

## 1. Phoenix deployment (Docker on the Mac Mini)

**[impl choice] Topology:** one `docker-compose.yml` in the company repo
(`infra/phoenix/`), two services:

```yaml
services:
  phoenix:
    image: arizephoenix/phoenix:<PINNED_VERSION>   # exact tag, never :latest
    environment:
      - PHOENIX_SQL_DATABASE_URL=postgresql://phoenix:${PHOENIX_DB_PASSWORD}@phoenix-db:5432/phoenix
      - PHOENIX_WORKING_DIR=/mnt/phoenix           # explicit; never the temp-dir default
      - PHOENIX_DEFAULT_RETENTION_POLICY_DAYS=90   # explicit; never the infinite default
      - PHOENIX_ENABLE_AUTH=true
      - PHOENIX_SECRET=${PHOENIX_SECRET}           # from Keychain via env injection
    ports: ["6006:6006", "4317:4317"]              # UI/HTTP + OTLP gRPC, LAN only
    volumes: [phoenix-home:/mnt/phoenix]
  phoenix-db:
    image: postgres:16.<PINNED>                    # pinned
    environment: [POSTGRES_DB=phoenix, POSTGRES_USER=phoenix, POSTGRES_PASSWORD=${PHOENIX_DB_PASSWORD}]
    volumes: [phoenix-pgdata:/var/lib/postgresql/data]
```

The three documented footguns are each closed by an explicit line above:
temp-dir SQLite (`PHOENIX_WORKING_DIR` + Postgres), infinite retention
(90 days), and capture-everything privacy (client-side, §4 — server config
cannot fix it). Secrets resolve Keychain-first per the fleet's existing
`keychain.py` pattern; nothing lands in the compose file or the repo.

**System of record:** Phoenix is observability, **not** the system of
record. Verdicts, receipts, canon ledgers, and dispute records live in the
product's own store under the creator's tenant (D4/D11). Losing Phoenix
loses debugging history, never product truth. Consequence: weekly `pg_dump`
is sufficient backup **[impl choice]**, and 90-day retention is safe.

**Version pinning is a D13 event:** the Phoenix image tag and Postgres tag
are recorded in the fleet-config version (§6). Upgrading Phoenix is a
promotion, not a drift.

**AX Free (deferred):** an AX Free account (25k spans/mo, 15-day retention)
pointed only at the customer-facing production slice is pre-approved as an
option for managed alerting *when strangers arrive*. Not deployed for the
thin slice — 25k spans/mo evaporates under fleet chatter, and §7's cron
alerting covers the slice. Revisit at first external creator.

## 2. Projects and span routing (designed up front, per A5)

Three Phoenix projects **[impl choice]**:

| Project | What lands there | Sampling |
|---|---|---|
| `product` | Every D2 pipeline run (ingest→…→verdict), end to end | 100% — this is the product's audit trail |
| `fleet` | Builder/Validator/Orchestrator/Librarian/Watchdog work sessions | 100% of runs, but **span filtering**: drop sub-agent chatter spans below tool/LLM-call granularity |
| `evals` | Experiment runs (pytest suites, judge calibration re-runs) | 100% |

Routing rule: the exporter's project header is set by the emitting process's
role, never inferred. Local $0 fleet agents (nightly synthesizer etc.) do
**not** trace to this Phoenix — company Phoenix carries company spans only;
the personal fleet keeps its existing manifests. This keeps volume tiny
(hundreds of spans/day at slice scale — no head-sampling needed) and keeps
the company's observability surface auditable on its own.

## 3. Trace schema — one schema, both layers

OpenInference/OTel base plus a custom namespace `sk.*` **[impl choice —
"sk" = series-keeper, provisional; rename rides the naming ticket]**. Every
span carries the common block; stage spans add their block. Schema lives in
the company repo as a versioned JSON-schema doc + a thin emit helper —
**agents never hand-roll attributes**.

**Common block (every span):**

| Attribute | Content |
|---|---|
| `sk.version.fleet_config` | D13 tuple, part 1 — git SHA of fleet agents/config |
| `sk.version.routing_table` | D13 tuple, part 2 — routing-table version |
| `sk.version.eval_corpus` | D13 tuple, part 3 — corpus git tag (§5) |
| `sk.version.canon_bible` | D13 tuple, part 4 — `{series_id}@{snapshot_id}` (content-hash) |
| `sk.run_id` / `sk.idempotency_key` | A2 durability — resumable run identity; key on every state-writing call |
| `sk.model.id`, `sk.model.temp`, `sk.prompt_hash` | exact model + config; judges additionally pin provider version string |
| tokens / cost / latency | standard OpenInference attributes |

**Stage spans (D2 state machine — one span per stage):** `sk.stage` (ingest
/ normalize / bible-retrieve / det-checks / judge / aggregate / verdict),
`sk.stage.success_criterion` + pass/fail (A2: machine-checkable per stage),
`sk.retry_count` (2-round cap), `sk.evidence.ids` (retrieved canon-fact /
exemplar IDs — IDs only, §4), `sk.stage.output_ref` (artifact-store ref,
never content).

**Verdict spans:** `sk.verdict` (pass / drift / needs-review /
**unverifiable-panel** — A4's first-class state), `sk.verdict.axis` +
severity band (D5 axis policy), `sk.receipt.ids`, `sk.judge.votes` +
`sk.judge.disagreement` (bool — the high-info sample flag, A1),
`sk.human.override` (bool + direction), `sk.dispute.tag` (D12 taxonomy:
missed-drift / false-drift / bad-receipt / canon-was-declared),
`sk.cost_per_verdict` (first-class metric, D9 — computed at aggregate stage
as the run's total cost / verdicts emitted).

## 4. Data minimization (D11, implemented client-side)

Capture-everything is Phoenix's default and there is no one-flag privacy
preset — so minimization is code we own, running **before** spans export:

1. **TraceConfig masking**: base64 images and raw input/output bodies
   masked category-wide.
2. **Redaction span processor**: a custom OTel span processor that (a)
   replaces any attribute matching registered content patterns with
   `[redacted:{artifact_ref}]`, (b) allowlists the `sk.*` namespace — an
   attribute not in the schema doc is dropped, not exported.
3. **The rule**: traces carry **IDs, hashes, refs, and verdict metadata —
   never manuscript text, never creator images**. Receipts (which do
   contain cropped evidence) live in the product store under the creator's
   tenant; Phoenix holds only `sk.receipt.ids`.
4. **CI canary** **[impl choice]**: a pytest that runs a pipeline pass over
   a sentinel-marked fixture (unique strings + a steganographic-marker
   image), captures the exported spans, and fails if any sentinel appears
   in any attribute. Minimization becomes a regression-tested property, not
   a convention.

## 5. Eval corpus and suites (D3)

**Corpus store [impl choice]:** `evals/corpus/` in the company repo — one
YAML case file per case, referenced media in `evals/fixtures/` (small) or
by stable pointer into the vault mirror (large). **Corpus version = git tag
(`corpus-vN`)** — that tag is the D13 tuple's third element. A case schema
mirrors the spike manifest, generalized:

```yaml
id: X26            # stable, never reused
lane: detection    # extraction | detection | judge | verdict | fleet
modality: visual   # visual | text | (video later, behind its own spike)
suite: capability  # capability | regression
refs: [...]        # reference/anchor artifact refs
candidate: ...     # artifact under test
note: ...          # canon-update note, when the case exercises D1 note-scoping
truth: consistent  # + truth_label taxonomy from the spike
provenance: {source: vision-drift-spike, added: 2026-08-08}
```

**Seed migration:** the 32 spike cases
([2026-08-08-vision-drift-spike/](2026-08-08-vision-drift-spike/) —
11 clean / 14 drifted / 7 haircut incl. the no-note control) migrate as the
**detection + judge lanes'** seed and the initial judge **gold set**; the
extraction-test materials
([2026-08-08-canon-extraction-test/](2026-08-08-canon-extraction-test/) —
3 corpora, proposed bibles, change reports, blind maps) migrate as the
**extraction lane's** seed, with the P&C sequential-era protocol preserved
as the evolution-handling suite. Target ~50 cases per D3; production
failures and resolved disputes (D12) grow it from there.

**Suites and bars (pre-registered — inherited, not invented):**

| Lane | Bars (from the two spikes' pre-registered thresholds) |
|---|---|
| extraction | fact precision ≥0.80 · identity coverage ≥0.70 · evolution 2/3 · onboarding cost ≤~$20/50-installment catalog |
| detection | recall ≥ spike bar, false-alarm ≤ spike bar, haircut-note scoping incl. the control case |
| judge | **pass^k** (k=3 [impl choice]: a case passes only if 3/3 repeat runs agree) · κ/α vs gold set |
| verdict | D5 axis-policy conformance · Needs-Review ≤15% of checks · **median actionable-items-per-installment** vs pre-registered alarm (addition 1: top-N≈5-7 surfaced, tail to digest) |

**Capability vs regression:** every case tagged one or the other; the
regression suite runs nightly and on every PR (evals-as-pytest, Phoenix
experiment recording); the capability suite runs on demand when trying to
*earn* something. **Standing constraint restated:** the early suite is a
regression harness — no model downgrades, autonomy increases, or product
claims below **200 cases per lane** (D3/D5).

## 6. Judge lane calibration (A1 — binding)

- **Exactly 2 judges**, maximally diversified: different vendor + different
  evidence access **[impl choice for the slice]:** Judge-A = Claude
  (frontier tier) seeing candidate + retrieved canon facts + reference
  exemplars; Judge-B = Gemini (the anima-validated pin) seeing candidate +
  references only, canon facts withheld — diversity in both lineage and
  evidence.
- **Temp 0, version-pinned** (provider version string recorded per span).
  A judge model/prompt change is a **recalibration event**: re-run the gold
  set, record κ/α before/after, log it as a D13 promotion. Never a config
  tweak.
- **Pairwise against the locked reference, never absolute scores**;
  structured **forced-choice per axis** output.
- **Agreement measured with chance-corrected κ/α only** — raw agreement is
  banned from dashboards (98% raw can mask α≈0 at high Pass rates).
- **Disagreement is the product's richest signal**: disagreement events are
  logged (`sk.judge.disagreement`), mined weekly (§7), and resolved by the
  D5 axis policy — never averaged away.
- **OCR escape**: rendered text in panels routes to deterministic OCR
  comparison before any judge sees it (VLM judges <50% accurate there).
- **Monthly gold-set re-runs** (cron), κ/α trend on the dashboard; the
  deterministic visual pre-filter (A4 detect→crop→DINOv2→anchor) feeds the
  judges, and its detector failures emit `unverifiable-panel`, never a
  silent skip.

## 7. Alerting and the operating loop (D9 + D12)

No AX, so alerting is the fleet's proven pattern — **cron + eval +
Pushover** — five pre-registered alarms **[impl choice]**:

1. Median **actionable-items-per-installment** exceeds the pre-registered
   bar (set from the first 5 dogfood installments, then frozen).
2. **Needs-Review rate >15%** of production checks (7-day window).
3. **Judge κ/α drop** below the calibration floor on the monthly gold-set
   re-run, or any unlogged judge-version change detected.
4. **Cost-per-verdict** trend breaches its per-lane cap (D10 cap policy).
5. **Dispute SLA**: any dispute open >5 days fires a warning (7-day SLA,
   D12); any resolved dispute not converted to an eval case within one
   review cycle appears on the weekly review agenda.

**Weekly 60-min founder failure review** (D9): reads Phoenix directly —
the week's disagreement events, overrides, disputes, alarm history, and
cost rollup; output is (a) new eval cases, (b) at most one process change,
logged. Overrides and disputes feed the corpus via the D12 path: dispute →
review inbox → resolution → eval case within one cycle → per-creator
dispute rate tracked as the calibration metric (A6 predicts this rate
*rises* as receipts improve — budget review time for engaged pushback, and
read a rising-with-receipts rate as adoption, not failure).

## 8. Cost

$0/month recurring (Phoenix ELv2 self-hosted — internal use, which is
exactly our use; we are not offering Phoenix itself as a service). Compute:
existing Mac Mini. Worst-case future: AX Pro $50/mo — inside the ≤$250/mo
[L7] cap with room to spare. Judge-lane inference is the real variable cost
and is capped per-lane by the D10 cap policy, with `sk.cost_per_verdict`
making it visible per-run from day one.

## 9. What this doc deliberately does not decide

Per addition 6 (STOP ADDING DECISIONS): no new architectural decisions
here. The remaining unknowns — exact pinned image versions, gold-set κ
floors, the actionable-items bar's numeric value — are **measured during
the slice build**, not ratified in advance. Each has a ticket on the step-6
map.

## Provenance

Governing record: [ratification package](2026-08-08-architecture-ratification-package.md)
(D3/D9/D12/D13) · [second opinion](2026-08-08-architecture-second-opinion.md)
(A1/A2/A4/A5, additions 1, 6) · [canon-extraction test](2026-08-08-canon-extraction-test.md)
(extraction-lane bars, onboarding economics) ·
[drift spike](2026-08-08-vision-drift-feasibility-spike-go-no-go.md)
(detection-lane bars, gold set) ·
[Arize research](2026-08-08-architecture-second-opinion/research-arize-stack.md)
(deployment facts, footguns, pricing).
