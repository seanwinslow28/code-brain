---
title: "Fleet architecture proposal v1 — campaign step 4 input (pre-ratification)"
date: 2026-08-08
project: agent-company-founding
type: architecture-proposal
status: draft-for-council
tags: [agent-company, architecture, orchestration, L10-campaign]
---

# Fleet architecture proposal v1

Input to the step-4 ratification. Ten proposed decisions on Codex's TOP-TEN
agenda, grounded in the feasibility spike (GO), the software-factory
literature review, and the groundwork v1 audit. Nothing here is locked until
Sean ratifies; [L10] holds — no company code before ratification.

Company context: a solo founder's fleet builds and operates a multimodal
series-consistency keeper (pre-publish drift gate with receipts) for serial
creators. Constraints: ~25 founder hrs/week, ≤$250/month opex, quality over
speed. Two eval layers: fleet-evals run the company; product-evals ARE the
product.

## D1 — Release-gate contract (the product's verdict semantics)

**Proposed:** Every check returns one of three verdicts — **Pass / Drift /
Needs Review** — never a bare confidence score. Every non-Pass verdict carries
receipts: the specific canon evidence (reference image, canon fact, prior
installment) the candidate conflicts with. Canon-update notes are first-class
events: a declared change is never drift, but a note only covers what it
declares — undeclared residuals still flag (spike-validated, including the
adversarial control). The gate defaults to **advisory**: it reports and the
creator decides; blocking-on-Drift is per-creator opt-in per axis.
*Grounds:* Ramp's three-way bucketing + citations-as-explainability; the
verified pain evidence that creators distrust tools automating their
judgment; the spike's haircut mechanism working end-to-end.

## D2 — Deterministic pipeline boundary

**Proposed:** The product pipeline is a **coded state machine** (Stripe
"blueprint" pattern): ingest → normalize assets → retrieve scoped
bible/canon → deterministic checks (schema, countable canon facts, palette
ranges, similarity floors as record-only signals) → LLM/vision judge for what
cannot be enumerated → aggregate → verdict + receipts → persist trace. Agents
never orchestrate the flow; code does. A failed stage retries alone, with a
**hard cap of 2 remediation rounds** before Needs Review.
*Grounds:* Stripe Minions (2-CI-run cap, determinism where judgment isn't
needed); OpenAI (code-orchestration "more deterministic and predictable");
corpus ("agents propose, code disposes"); the spike's leg-count failure mode
(countable facts belong to deterministic checks, not the judge).

## D3 — Eval constitution

**Proposed:** Seed product-evals from the 32-case spike corpus, grow to ~50
with real creator material. Structure: paired clean/defect cases, haircut
twins (with/without canon notes), adversarial controls; split
**capability** (improvement signal) vs **regression** (near-100% breakage
alarm) suites; grade bible-extraction, detection, and final verdict as
separate stages; **pass^k** on the judge lane for consistency. Every
production miss/false-alarm becomes a case. Fleet-evals use the same harness
and trace store. Pre-registered bars before every major change (the spike's
discipline, made standing).
*Grounds:* Anthropic demystifying-evals (20-50 cases from real failures,
capability/regression split, outcome grading); OpenAI eval-driven design
(stage-wise grading kills "telephone" failures); the spike itself.

## D4 — Canon/context model (the series bible)

**Proposed:** Per-creator series bible as **versioned files** with
provenance, following groundwork's memory doctrine: append-and-supersede
(never edit), provenance labels (observed/inferred/confirmed), canon-update
events as append-only records. Two tiers: **structured canon facts**
(countable/checkable: character-sheet fields, palette values, register
descriptors — these feed D2's deterministic checks) and **reference exemplars**
(images/passages — these feed the judge). Bible extraction at onboarding is
agent-proposed, **creator-confirmed**: the generator-refusal doctrine applied
to product data — the system never invents canon.
*Grounds:* the spike (errors concentrate exactly where canon facts were
unstated); anima's layer-ownership precedent; groundwork memory schema;
OpenAI ("anything the agent can't access in-context effectively doesn't
exist" → repo-local versioned artifacts).

## D5 — Model routing policy

**Proposed:** Ceiling-first routing: establish each lane's quality ceiling
with a frontier model, then downgrade where evals stay green (evals are the
license). The **judge lane runs a 2-model complementary panel** — one strict,
one calibrated (spike evidence: Gemini flash perfect recall/over-flags,
Claude calibrated/misses subtle counts); panel disagreement → Needs Review.
Batch/extraction/summarization lanes route to Sean's local open-model fleet
(Qwen/Gemma via Ollama, $0). Routing lives in a **table file** (groundwork
content); the router is runtime (hybrid_router pattern, `fallback="none"`
cost-safety on local lanes).
*Grounds:* OpenAI practical guide (prototype with best, downgrade on green
evals — validated 3x cost cut); spike cross-model finding; Sean's existing
HybridRouter + Tier-C precedent; ≤$250/mo cap.

## D6 — Verification stack

**Proposed:** Layered, zero-trust: (1) deterministic gates first (schema,
canon-fact checks, artifact existence — verify real artifacts, never agent
self-report); (2) LLM judge above with explicit rubric, pass/fail output, and
an **Unknown escape valve**; (3) worker never self-approves — judge runs in a
fresh context that sees only the artifact + criteria (writer/reviewer split);
(4) for fleet code: new tests must fail on the pre-patch tree (the
remove-the-patch check), agent-to-agent review always, **human PR gate stays
until a regression suite + rollback path exist** — autonomy is earned
per-lane, not granted globally.
*Grounds:* Stripe benchmark failure mode (agents accepting 400s as success);
corpus remove-the-patch practice; Anthropic writer/reviewer + adversarial-
reviewer caution; CMU velocity-paradox warning; [L6] autonomy-proof leg
reconciled with the lights-off warnings by earning autonomy per-lane.

## D7 — Autonomy and permission matrix

**Proposed:** Three permission profiles: **read-only / sandbox-write /
founder-approved-production-write**. Every tool rated low/med/high risk
(write scope, reversibility, blast radius, cost). Every fleet agent carries a
groundwork **Owner's Card** (owner = Sean, forbidden actions, pause +
retirement conditions) — and the runtime wires pause conditions to actual
kill switches. **Enforcement-parity rule:** non-Claude agents get
side-effectful capability only through runtime-mediated tools (never raw
shell/browser), because hook enforcement exists only on Claude Code. HITL
triggers: retry-cap breach and any high-risk action.
*Grounds:* OpenAI tool-risk ratings + HITL triggers; groundwork audit's
enforcement-parity caution; Ramp ("don't create a vector for unreviewed
code"); Stripe (safety from the sandbox boundary, not per-action approval).

## D8 — Orchestration topology

**Proposed:** **Single-orchestrator default; pipelines in code; fan-out is
the exception.** Named fleet roles (each an Owner's Card + a fleet-role
ontology entry — new groundwork content): Orchestrator (plans, dispatches,
owns effort-scaling rules), Builder (code/features), Validator (runs
deterministic gates), Judge panel (D5), Librarian (bible + docs gardening —
the doc-gardener pattern), Watchdog (production monitoring, daily digest to
the review inbox). Parallel fan-out only for read-heavy research and
fresh-context review, with explicit effort rules ("simple task = 1 agent, N
calls") so the fleet cannot spawn its way into a bill.
*Grounds:* Anthropic (multi-agent = ~15x tokens, poor fit for most coding;
effort-scaling rules); OpenAI (maximize single agent; orchestrate via code);
corpus factory roles (scout/plan/build/test) adapted; meta-tooling trap
warning.

## D9 — Observability operating loop

**Proposed:** One **Arize trace schema** from day one, covering both layers:
model + config versions, retrieved evidence IDs, tool calls, tokens, cost,
latency, stage outputs, grader results, retries, final disposition, human
override. Weekly **60-minute founder failure review** (transcript reading is
the production-monitoring team); every override feeds D3's eval growth. Cost
attribution per agent/lane rolls into a monthly budget report against the
$250 cap.
*Grounds:* Anthropic (full tracing, weekly transcript reading); OpenAI
(continuous evaluation, production-traffic mirroring); Ramp (evals live where
context lives, user-flagged errors become tests).

## D10 — Solo-founder operating envelope

**Proposed:** The ~25 hrs/week splits into named lanes: review inbox +
weekly failure review (~6h), product/build direction (~10h), build-in-public
(~4h), partner/ratification sessions (~3h), slack (~2h). The **review inbox
is built in the first runtime slice** (it is the founder-time bottleneck).
**Meta-tooling budget: ≤20% of build hours** may go to fleet tooling that
doesn't serve a named product need (the fleet-becomes-the-product trap).
Opex: local fleet carries $0 lanes; cloud spend budgeted per-lane with
pre-flight caps (cap_policy pattern), total ≤$250/mo. Rollback ownership:
founder, with a documented rollback path required before any lane earns
production-write.
*Grounds:* [L7]; the audit's review-inbox caution; the corpus meta-tooling
warning; Sean's existing cap-policy/spend-ledger machinery.

## Explicitly deferred (not in this ratification)

Wedge segment (which serial creators first) and business model — future
partner axes per the sidecar. Text-lane long-context depth (FlawedFictions
risk) and video drift — step-5/build-phase spikes. Groundwork interview
dogfooding timing. The Mac-Mini personal Arize learning track stays outside
the company per [L10].
