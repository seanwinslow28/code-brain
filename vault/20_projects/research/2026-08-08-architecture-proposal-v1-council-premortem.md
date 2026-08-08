# Council Session — arch-ratification-premortem

- **Session ID:** `20260808-122044-e182fb`
- **Profile:** `premium`
- **Duration:** 152.4s
- **Tokens:** 53531 in, 16393 out
- **Cost:** unknown
- **Dropped models (Stage 1 failures):** x-ai/grok-4.5
- **Ranking-failed judges (Stage 2):** google/gemini-2.5-pro

## Original prompt

```
The author is a solo founder (a PM, not a professional developer) about to ratify the architecture for a company where a fleet of AI agents builds AND operates one product: a multimodal series-consistency checker for serial creators (a pre-publish gate that catches character/style/canon drift across installments, with receipts). A feasibility spike already passed (two vision models cleared pre-registered bars on drift detection including the declared-canon-change problem). Constraints: ~25 founder hrs/week, <=$250/month opex, quality over speed. The fleet mixes closed and open-source models. Evals and traces on everything (Arize). The founder already operates a personal agent fleet (local Ollama models, launchd schedules, budget caps, a hybrid model router) and a governance repo ("groundwork": files-not-engine, Owner's Cards with human-only kill conditions, blast-radius change routing).

Below are the TEN architecture decisions proposed for ratification. Before the founder locks them, surface the strongest objections. Each council member should independently answer:

1. WEAKEST DECISION: Which single decision (D1-D10) is most likely to fail in production as written, and what is the concrete failure scenario?
2. DANGEROUS ASSUMPTION: The one assumption baked into this architecture that the founder shouldn't be making.
3. MISSING DECISION: What eleventh decision is absent that will bite within 6 months? (The company's month-6 bar: live product with >=20 weekly active users >=1 paying, fleet runs maintenance 30 consecutive days with evals governing quality and founder <=10 hrs/week oversight, weekly build-log publishing.)
4. V1 DEBT: Which decision is fine for v0.1 but will hurt most at v1.0, and what should be written into the ratification now to de-risk it?
5. RATIFY AS-IS: Which decisions (if any) are sound enough to lock without modification?

Be ruthless and specific — name decisions by number, describe concrete failure scenarios, no generic advice. The author wants pre-mortem, not validation.

=== PROPOSED ARCHITECTURE (ten decisions) ===
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
```

## Council responses

### anthropic/claude-opus-4.7

# Pre-mortem: Fleet Architecture v1

## 1. WEAKEST DECISION: **D5 — Model routing policy**

The "2-model complementary panel → disagreement = Needs Review" is the failure I'd bet on. Concrete scenario: Gemini flash over-flags at its documented rate, Claude misses subtle counts. On real creator submissions (not the curated 32-case spike), the *baseline* disagreement rate on ambiguous panels will run 25-45%, not the ~10% you're implicitly modeling from the spike. Result: Needs Review becomes the modal verdict. Creators lose trust ("this thing punts on everything"), and *you* become the tiebreaker in your own review inbox — the exact bottleneck D10 says is the constraint. Worse, "Needs Review" is unfalsifiable in eval terms: it's not a miss and not a false-alarm, so the regression suite doesn't catch the drift toward it.

Also: "ceiling-first, downgrade on green evals" assumes your 50-case eval set can license a downgrade decision. It can't. 50 cases gives you ±14pp confidence intervals at best; you'll downgrade into silent quality regressions.

Fix before ratifying: pre-register a **max Needs-Review rate** (e.g., ≤15% of production traffic) as a regression alarm, and require ≥200 cases before any lane downgrade is authorized.

## 2. DANGEROUS ASSUMPTION

**That the 32-case spike's drift-detection performance generalizes to arbitrary creators' canons.**

The spike passed pre-registered bars on *your* selected material with *your* declared-canon-change taxonomy. Real serial creators have canons that are (a) partially tacit, (b) internally inconsistent (creators retcon constantly and don't declare it), and (c) stylistically idiosyncratic in ways your palette/schema checks won't parameterize. The whole architecture — especially D2's "countable canon facts" and D4's structured/exemplar split — assumes canon is *extractable into a schema*. For many serial creators (webcomic auteurs, especially) canon is a vibe with load-bearing exceptions. If canon-extraction quality is the real ceiling, D2's deterministic layer is doing less work than the proposal claims and the judge lane is doing more — which reroutes cost, latency, and failure modes.

Test this before locking: run the pipeline on 3 real creators' back-catalogs *before* ratification, not after.

## 3. MISSING DECISION: **D11 — Customer feedback → eval loop (the ground-truth ingestion contract)**

Nothing in D1–D10 specifies how a creator disputes a verdict and how that dispute becomes labeled data. D9 mentions "every override feeds D3's eval growth" in one clause — that's a hand-wave, not a decision. By month 6 with 20 WAU and 1 payer, you will have:

- Verdicts the creator disagrees with but no structured capture of *why* (was it a false Drift? a missed Drift the creator caught post-publish? a Needs-Review they thought was obvious?)
- No SLA on turning a dispute into a regression case
- No distinction between "creator is wrong about their own canon" (happens constantly) and "system is wrong"

Concrete D11: every verdict has a one-click dispute widget with a required taxonomy tag (missed-drift / false-drift / bad-receipt / canon-was-declared); disputes land in the review inbox with a 7-day resolution SLA; resolved disputes become eval cases within one review cycle; a creator's dispute rate is itself a tracked metric (per-creator calibration). Without this, your eval set stays synthetic and the regression suite protects you against last month's problems only.

## 4. V1 DEBT: **D4 — Canon/context model**

Append-and-supersede versioned files are correct for v0.1 and one creator. At v1.0 with 20+ creators this becomes a problem across three axes:

1. **Query performance:** reconstructing "current canon" from an append-only file log at judge-call time will dominate latency once bibles pass ~500 events.
2. **Provenance drift:** "observed/inferred/confirmed" labels are creator-confirmed at onboarding but there's no re-confirmation cadence. Six months in, "confirmed" facts are stale confirmations of a canon that has moved.
3. **Multi-tenancy:** files-not-engine works beautifully for governance; it will not work as a per-creator data plane once you have paying customers who expect their canon isolated, exportable, and deletable (GDPR-shaped concerns even pre-EU).

Write into ratification now: (a) a **materialized "current canon" snapshot** rebuilt on write, so read-path never traverses the log; (b) a **confirmation-decay policy** — facts older than N installments require re-confirmation or drop to "inferred"; (c) an explicit **per-creator data boundary** with export/delete primitives specified now even if unimplemented, so v1 migration isn't a rewrite.

## 5. RATIFY AS-IS

- **D1** — the three-way verdict with receipts and advisory-default is the most defensible piece of the whole design; it aligns the product's semantics with the actual pain (creator distrust of automation). Lock it.
- **D7** — the enforcement-parity rule (non-Claude agents get side effects only through runtime-mediated tools) is exactly the kind of specific, load-bearing constraint most solo founders miss. Lock it.
- **D10** — the ≤20% meta-tooling budget and the "review inbox built in the first runtime slice" are the two disciplines most likely to save the company from itself. Lock it.

D2, D3, D6, D8, D9 are directionally right but each has a smaller issue I'd flag in a longer pass (D3's 50-case ceiling is too low to license D5's downgrades; D8's "single-orchestrator default" is right but "fan-out is the exception" needs a token budget, not a topology rule; D9 needs a defined cost-per-verdict metric, not just monthly rollups). None of those rise to weakest-link.

---

**One meta-note:** the proposal is unusually well-grounded — the citations to Stripe/Ramp/Anthropic/OpenAI aren't decorative, they're load-bearing. The risk isn't sloppy thinking; it's *coherent thinking built on a 32-case spike*. The single highest-leverage thing you can do before locking is run the pipeline against 3 real creators' catalogs. If canon-extraction holds up there, most of D1-D10 is fine. If it doesn't, D2/D4/D5 all shift.

### openai/gpt-5.5

## 1. WEAKEST DECISION: **D5 — Model routing policy**

**Most likely to fail in production as written.**

The weak point is not “use multiple models.” The weak point is:

> “The judge lane runs a 2-model complementary panel… panel disagreement → Needs Review.”

That sounds safe, but in production it will likely convert the product into a **Needs Review generator**.

### Concrete failure scenario

A creator uploads a new installment with several images and text passages. The product checks character appearance, palette, clothing continuity, tone/register, canon facts, and declared canon changes.

- The “strict” model flags five possible drifts:
  - eye color slightly different due to lighting,
  - jacket shade outside palette range,
  - dialogue slightly less formal,
  - missing scar in one panel,
  - possible contradiction with an inferred relationship fact.
- The “calibrated” model passes three of them and only flags two.
- Because disagreement routes to **Needs Review**, the final result becomes littered with review items.

From the creator’s perspective, the product has not caught drift; it has handed them a second editing job.

The failure mode compounds:

- Strict model over-flags visual nuance.
- Calibrated model under-flags subtle countable or continuity issues.
- Disagreement becomes common, not exceptional.
- “Needs Review” stops meaning “rare ambiguity” and starts meaning “the system is unsure a lot.”
- The founder then becomes the hidden third judge during early customer support.
- Opex increases because every serious check uses two models, and maybe pass^k.
- The product’s promise — “pre-publish gate with receipts” — degrades into “AI comments you must adjudicate.”

The architecture currently treats model disagreement as a safety valve. In practice, for this product, disagreement is likely to be the **normal case** across subjective visual/style/canon judgments.

### What should change before ratification

D5 needs an axis-specific disagreement policy.

Example:

- **Countable canon facts**: disagreement should usually escalate to deterministic verification or hard Needs Review.
- **Visual identity drift**: disagreement should produce severity bands, not automatic Needs Review.
- **Style/register drift**: disagreement should require stronger evidence before Drift/Needs Review.
- **Declared canon changes**: disagreement should be resolved against the canon-update event and scoped note.
- **Low-severity differences**: route to “Pass with note” or “Watch item,” not Needs Review.

Right now the panel design optimizes for recall and safety, but it risks destroying usability.

---

## 2. DANGEROUS ASSUMPTION

The dangerous assumption is:

> **That evals from the spike plus a ~50-case growing suite can govern real production quality across creator-specific canon, visual style, and narrative ambiguity.**

This assumption appears in D3, D5, D6, and D9.

The spike passing is meaningful, but the production distribution will be nastier:

- creators have incomplete bibles;
- art style evolves intentionally;
- lighting/composition creates apparent visual drift;
- canon changes are often implied, not declared cleanly;
- installments contain contradictions the creator does not consider errors;
- different creators want different strictness;
- “style drift” is taste-laden;
- multimodal assets will vary wildly in quality and format;
- users will judge the product by whether it understands *their* series, not by global benchmark accuracy.

A 32-to-50-case eval set can prevent obvious regressions. It cannot prove the product is reliable across user-specific canon spaces.

The architecture says “evals are the license.” That is directionally right, but the founder should not assume early evals are a sufficient license for:

- model downgrades,
- autonomy increases,
- strong product claims,
- low human oversight,
- or broad creator onboarding.

The real eval unit is not merely “case.” It is **series × creator tolerance × canon maturity × asset modality × declared-change policy**.

If this is not acknowledged, the fleet will look governed while shipping brittle confidence.

---

## 3. MISSING DECISION: **Data/IP/security policy for unpublished creator material**

The absent eleventh decision should be:

## **D11 — Creator data, IP, retention, and model-provider boundary**

This will bite within six months.

The product asks creators to upload exactly the material they are most protective of:

- unpublished chapters,
- character designs,
- reference images,
- series bibles,
- plot plans,
- continuity notes,
- possibly spoilers and commercial IP.

The architecture discusses traces, Arize, model routing, local/open/closed models, receipts, and persistence. But it does not ratify a data governance boundary.

### Concrete failure scenario

A paying creator asks:

> “Are my unreleased pages being sent to OpenAI/Anthropic/Google? Are they retained? Are they used for training? Can I delete everything? Are traces storing my manuscript? Can you see my images? What happens if I leave?”

If the answer is improvised, the founder loses the sale or creates legal/trust debt.

Worse, Arize traces may accidentally retain sensitive snippets, image references, canon facts, or model inputs. The architecture says “trace everything,” but for this product, tracing everything can become a liability.

### D11 should decide at minimum

- Which data is stored.
- Which data is sent to each closed model provider.
- Whether users can opt into local/open-only processing.
- Retention periods for uploads, traces, receipts, and derived canon.
- Deletion/export policy.
- Tenant isolation.
- Whether raw manuscripts/images are stored in Arize or only redacted references.
- Whether model providers are allowed to retain inputs.
- Encryption and access policy.
- Founder/operator visibility.
- Incident response.
- Terms around “the creator owns their canon/bible/output.”

For this market, this is not enterprise bureaucracy. It is core product trust.

---

## 4. V1 DEBT: **D4 — Canon/context model as versioned files**

D4 is good enough for v0.1, but it is the decision most likely to hurt at v1.0.

The dangerous part is not versioning or append-and-supersede. Those are good. The risky part is using “versioned files” as the primary series bible substrate without specifying a future-proof entity/event model.

For one creator and a handful of test series, files are fine. At v1.0, the product will need to answer questions like:

- Which facts were true during installment 7 but superseded by installment 12?
- Which character reference image is canonical for which era/outfit/form?
- Is this contradiction against observed canon, inferred canon, or creator-confirmed canon?
- Which canon update note authorized which visual changes?
- Which facts are scoped to an arc, timeline, AU, dream sequence, flashback, or adaptation?
- Which facts are user-editable versus model-extracted?
- Which evidence IDs were used in this verdict?
- Can the creator export/migrate their bible?
- Can two users collaborate on the same bible?
- Can old verdicts be replayed against the exact canon version used at the time?

Plain files will become painful unless D4 imposes structure now.

### What should be written into ratification now

Keep files for v0.1, but ratify them as an **event-sourced canon ledger**, not loose documents.

Minimum requirements:

- Stable IDs for:
  - series,
  - installment,
  - character,
  - location,
  - object,
  - style rule,
  - canon fact,
  - reference exemplar,
  - canon update event,
  - evidence artifact.
- Typed canon events:
  - observed,
  - inferred,
  - creator-confirmed,
  - superseded,
  - deprecated,
  - canon-change-declared.
- Temporal/scoping fields:
  - applies_from,
  - applies_to,
  - installment/arc scope,
  - modality scope,
  - exception scope.
- Provenance fields:
  - source artifact,
  - source span/image region,
  - extractor model/version,
  - creator confirmation state.
- Migration rule:
  - the file format must be losslessly movable to SQLite/Postgres/vector store later.
- Replay rule:
  - every verdict must be reproducible against the exact canon snapshot used.

If D4 remains “versioned files with provenance” but not “typed event ledger with stable IDs,” the founder will eventually have a canon swamp.

---

## 5. RATIFY AS-IS

I would lock these without major modification:

### **D1 — Release-gate contract**

Sound. Pass / Drift / Needs Review is the right product-level semantic. Receipts are mandatory. Advisory default is correct. Declared canon change handling is essential and already validated by the spike.

Minor future addition: axis-level severity may be needed, but D1’s core contract is right.

### **D2 — Deterministic pipeline boundary**

Sound. Code owns orchestration; agents do not. Deterministic checks before judgment is exactly right for this product. The two-remediation cap is healthy.

### **D6 — Verification stack**

Sound. Zero-trust, fresh-context judge, no self-approval, remove-the-patch check, human PR gate until rollback/regression maturity — all appropriate for a solo founder using agents.

### **D7 — Autonomy and permission matrix**

Sound. The enforcement-parity rule is especially important. Non-Claude agents should not get raw shell/browser side effects just because the founder has a good personal fleet setup.

### **D8 — Orchestration topology**

Sound. Single-orchestrator default and fan-out only by exception is the right call under the cost and oversight constraints. This avoids the “agent company spends all day managing agents” trap.

---

## Not ratify as-is / needs tightening

### **D3 — Eval constitution**

Directionally right, but the architecture should explicitly admit that the early eval suite is a regression harness, not proof of market-grade quality. Also needs creator-level eval slices once real users arrive.

### **D4 — Canon/context model**

Good v0.1, dangerous v1.0 unless made into a typed event ledger with stable IDs and replayable snapshots.

### **D5 — Model routing policy**

Weakest as written. Disagreement → Needs Review will likely create review spam. Needs axis-specific escalation semantics.

### **D9 — Observability operating loop**

Good instinct, but unsafe until paired with D11 data minimization. “Trace everything” is wrong if everything includes unpublished creator IP.

### **D10 — Solo-founder operating envelope**

Good discipline, but it depends heavily on D5 not creating review overload and D4 not forcing manual canon curation. As written, the time budget is plausible only if onboarding and Needs Review volume are tightly constrained.

### google/gemini-2.5-pro

As a member of this Council, I have reviewed the ten proposed decisions. My analysis is as follows.

### 1. WEAKEST DECISION: D5 — Model routing policy

This decision is the most likely to cause a critical failure in production. While the "ceiling-first" and "2-model panel" concepts are sound, the dependency on the founder's local Ollama fleet for `$0` lanes, combined with a `fallback="none"` policy, creates a brittle single point of failure for the entire operation.

**Concrete Failure Scenario:** The founder is on a trip for three days. A power outage or a hardware failure (e.g., disk failure on the Mac Mini) takes the personal Ollama server offline. Because the router cannot fall back to a cloud model for cost-sensitive batch tasks (per `fallback="none"`), all essential-but-non-premium fleet operations—such as bible extraction for new user onboarding, document gardening by the Librarian agent, or even parts of the build process—grind to a halt. The production system is not merely degraded; it is broken. The company is functionally offline, unable to onboard new users or perform its own maintenance, until the founder can physically return and repair their personal hardware. This directly contradicts the goal of a fleet that *operates* the product.

### 2. DANGEROUS ASSUMPTION

The single most dangerous assumption baked into this architecture is that **the agent fleet is a force multiplier from Day One.**

The founder is a PM, not a professional DevOps or MLOps engineer. The architecture describes a sophisticated, multi-component, distributed system involving CI/CD, model routing, observability, and state management. The founder assumes that this "software factory" will quickly become efficient enough at building the *product* (the consistency checker) that it will not consume the entire 25-hour weekly time budget just to maintain the *factory itself*.

The reality is that for the first 6-12 months, this fleet will be a **force sink**. The overwhelming majority of the founder's time will be spent debugging the fleet's execution, fixing its flawed code, managing its configuration drift, and improving its core capabilities—not directing it to build product features. The meta-tooling budget of 20% (D10) is a wild underestimate. The founder is assuming the scaffolding is a one-time cost, when in fact, operating the agent factory will be the primary job, eclipsing work on the product it's meant to build.

### 3. MISSING DECISION: D11 — State & Artifact Promotion

A critical eleventh decision is missing: a defined policy for **State and Artifact Management and Promotion.**

The architecture describes numerous critical, versioned-file-based state components: the canon bibles (D4), the model routing table (D5), the eval corpus (D3), and the fleet's own source code. However, there is no decision defining how these artifacts are stored, versioned cohesively, and promoted through logical environments.

**Failure Scenario within 6 Months:** The `month-6 bar` requires 30 consecutive days of successful fleet maintenance. On day 15, the Watchdog agent flags a sudden spike in `Needs Review` verdicts for a specific user. The root cause is a subtle bug introduced by a recent change. The founder dives in to debug, but faces a critical question: the problematic trace in Arize was generated by `Builder-v0.2.1` using `routing-table-v1.4` and `eval-corpus-v3.1`, which was evaluating a user's `canon-bible-v7`. How can the founder reliably reproduce this exact configuration to debug it? Without a unified artifact registry and promotion strategy, the "versioned files" become a tangled mess of dependencies spread across git commits, file systems, and databases. The founder will burn the entire 10-hour oversight budget simply trying to reconstruct the state of the world that led to the failure, making the 30-day stability goal impossible to achieve.

### 4. V1 DEBT: D8 — Orchestration topology

The decision to default to a **single orchestrator** is pragmatic for v0.1 but will accrue significant technical debt by v1.0. As the fleet's responsibilities grow, this single agent will become a monolithic "god agent," making it difficult to debug, update, and reason about. Its prompt will become an unmaintainable thicket of instructions, and it will become a central bottleneck for execution.

**De-risking Action for Ratification:** An amendment should be added to D8 now to enforce modularity and prepare for future decomposition. Add the following clause:

"All communication between the Orchestrator and other named fleet roles (Builder, Validator, Judge, etc.) must occur over a standardized, versioned, and documented internal API (e.g., a simple JSON schema for tasks and results). The Orchestrator is forbidden from accessing the internal state or implementation details of other roles. This ensures that individual roles can be improved, replaced, or composed into different team structures in the future without requiring a rewrite of the entire orchestration logic."

This forces API--driven design from the start, making a future transition from a single orchestrator to a multi-team or specialized-pipeline model feasible.

### 5. RATIFY AS-IS

The following decisions are sound, well-grounded, and should be ratified without modification:

*   **D1 — Release-gate contract:** This is an excellent, user-centric design. The three-verdict system with mandatory receipts directly addresses the primary user pain point of trusting AI tools. It correctly places the creator as the final authority.
*   **D3 — Eval constitution:** This is state-of-the-art practice for building reliable AI systems. The split between capability and regression, growth from production failures, and stage-wise grading will be the engine of quality for both the product and the fleet.
*   **D4 — Canon/context model:** The "agent-proposes, creator-confirms" principle for canon is critical. Structuring the bible into deterministic facts vs. reference exemplars and using an append-only, versioned file store is a robust and correct approach to managing the system's core data.
*   **D6 — Verification stack:** This layered, zero-trust approach is exemplary. It demonstrates a mature understanding of agent safety, correctly prioritizing deterministic checks and enforcing a "writer/reviewer" split. Earning autonomy per-lane is the only viable path to reliable automation.
*   **D9 — Observability operating loop:** The commitment to a single trace schema and a weekly, dedicated failure review is the most important human process in the entire system. This is the core feedback loop that will allow the solo founder to maintain control and drive quality.

## Cross-rankings

### Judge: anthropic/claude-opus-4.7

- **Order:** A > B
- **Reasoning:** Response A is more ruthless and specific in the pre-mortem spirit the founder requested. Its D5 critique focuses on the substantive product-quality failure mode (Needs Review spam from routine panel disagreement on subjective judgments) which is more insightful than B's infrastructure-availability angle. A's missing decision (D11 data/IP/security for unpublished creator material) is more urgent and market-critical for this specific product than B's artifact-promotion policy, which is real but more operational. A's V1 debt analysis of D4 is deeply specific with a concrete event-ledger schema, whereas B's D8 API-boundary recommendation is more generic. B is competent and its artifact-reproducibility scenario is valuable, but overall less sharp and product-aware.

### Judge: openai/gpt-5.5

- **Order:** A > B
- **Reasoning:** Response A is more incisive and production-realistic: it identifies a concrete product-quality failure mode in D5 (Needs Review becoming the dominant outcome), ties it directly to founder-time collapse and eval blind spots, and proposes measurable mitigations. Its missing decision around dispute/override-to-eval ingestion is especially strong because it connects directly to the month-6 live-user bar. Response B has some good points, especially around artifact reproducibility/promotion, but its weakest-decision scenario leans too heavily on an infrastructure outage and somewhat overstates the role of local Ollama lanes; its dangerous assumption is also more generic than ruthless. A also better distinguishes v0.1 acceptability from v1.0 debt and is more selective in what it would ratify as-is.

## Chairman synthesis

_Chairman model: `anthropic/claude-opus-4.7`_

# Council Synthesis: Pre-Mortem on Fleet Architecture v1

Three council members responded (Claude Opus, GPT-5.5, Gemini 2.5 Pro). Convergence is unusually high on the biggest risks; divergence is instructive where it appears. I'll flag both.

---

## 1. WEAKEST DECISION — **Unanimous: D5 (Model routing policy)**

All three council members named D5. But they diagnosed **two different failure modes**, and both are real:

**Failure mode A — "Needs Review spam" (Claude + GPT-5.5, the stronger critique):**
The 2-model complementary panel with `disagreement → Needs Review` assumes disagreement is rare. On real creator material (not the curated 32-case spike), disagreement on subjective visual/style/canon judgments will likely run 25–45%, not ~10%. Claude's specific prediction: *Needs Review becomes the modal verdict.* GPT-5.5's concrete scenario: strict model flags 5 items, calibrated flags 2, creator receives an editing job instead of a verdict. The founder becomes the hidden tiebreaker — colliding directly with D10's review-inbox bottleneck.

Compounding this: "Needs Review" is unfalsifiable in eval terms (Claude's point) — it's neither miss nor false-alarm, so the regression suite can't detect drift toward it. And "downgrade on green evals" is uncashable when 50 cases give ±14pp confidence intervals.

**Failure mode B — Local fleet as SPOF (Gemini):**
`fallback="none"` on cost-safety plus dependency on the founder's Mac Mini Ollama fleet means a hardware failure while the founder is away takes production offline. Council rankers noted this scenario is real but less central than A.

**Fixes to write into ratification before locking D5:**
- Axis-specific disagreement policy (GPT-5.5): countable facts → escalate to deterministic verification; visual identity → severity bands, not automatic NR; style/register → require stronger evidence; low-severity → "Pass with note," not NR.
- Pre-register a **max Needs-Review rate** as a regression alarm — Claude suggests ≤15% of production traffic.
- Require **≥200 cases** before any lane downgrade is authorized (Claude).
- Define a **degraded-mode fallback** for local-fleet outages, even if it costs money above the cap during incidents (Gemini's concern, adapted).

---

## 2. DANGEROUS ASSUMPTION — Three candidates, ranked by council quality

**Claude's (strongest, most product-specific):** *The 32-case spike generalizes to arbitrary creators' canons.* The architecture — especially D2's "countable canon facts" and D4's structured/exemplar split — assumes canon is extractable into a schema. For many serial creators (webcomic auteurs, prose stylists), canon is a vibe with load-bearing exceptions. If canon-extraction quality is the real ceiling, D2's deterministic layer does less work than claimed and the judge lane does more — rerouting cost, latency, and failure modes. **Actionable test before ratification: run the pipeline against 3 real creators' back-catalogs.**

**GPT-5.5's (complementary, aimed at governance):** *Early evals can license production quality claims.* The real eval unit is `series × creator tolerance × canon maturity × asset modality × declared-change policy`, not a global case count. Evals are a regression harness, not proof of market-grade quality. Don't use them to license model downgrades, autonomy increases, or broad onboarding.

**Gemini's (broader but softer):** *The fleet is a force multiplier from Day One.* It will be a **force sink** for 6–12 months, and the 20% meta-tooling budget in D10 is a wild underestimate.

**Synthesis:** Claude's and GPT-5.5's are the same underlying assumption viewed from two angles (spike-generalization on the product side, eval-set-as-license on the governance side). Both should be treated as ratified concerns. Gemini's is worth internalizing as a time-budget stress test on D10 but is less falsifiable pre-launch.

---

## 3. MISSING DECISION — Divergence; the founder likely needs **all three**

The three councils named three different missing decisions. Notably, none overlap — which suggests the architecture has multiple 6-month blind spots, not one.

**GPT-5.5 — D11: Creator data, IP, retention, model-provider boundary.** *(Council-ranked strongest for this product.)* Creators upload their most protected material: unpublished chapters, character designs, reference images, plot plans. The architecture says "trace everything" (D9) without specifying what leaves the system, what closed providers retain, deletion/export primitives, or tenant isolation. First paying customer will ask these questions; improvised answers cost the sale or create legal debt. Arize traces themselves may become a liability if they retain manuscript content.

**Claude — D11: Dispute → eval ingestion contract.** D9's clause "every override feeds D3's eval growth" is a hand-wave. Needs: one-click dispute widget with required taxonomy (missed-drift / false-drift / bad-receipt / canon-was-declared), 7-day SLA to convert dispute → eval case, per-creator dispute rate as a tracked calibration metric. Without this, the eval suite stays synthetic and only defends against last month's problems. **This is the missing decision most directly tied to the month-6 bar (20 WAU, 1 payer, evals governing quality).**

**Gemini — D11: State & artifact promotion.** Reproducibility of a failing trace requires knowing exactly which `Builder-vX.Y` + `routing-table-vN` + `eval-corpus-vM` + `canon-bible-vK` produced it. Without a unified artifact registry, debugging a day-15 regression during the 30-day maintenance window will consume the entire 10-hour oversight budget.

**Recommendation:** All three are real. If forced to sequence: **GPT-5.5's data/IP boundary is the one that blocks paying customers**, so it must precede first payer. **Claude's dispute-loop is the one that makes the month-6 quality bar possible**, so it must precede WAU ramp. **Gemini's artifact promotion is the one that makes the 30-day maintenance bar possible**, so it must precede the maintenance window. Consider ratifying them as D11/D12/D13 rather than picking one.

---

## 4. V1 DEBT — Convergence on D4; one dissent on D8

**Claude + GPT-5.5 — D4 (Canon/context model):** Both independently identify D4 as v1 debt with nearly identical prescriptions. Append-and-supersede versioned files are correct for v0.1 and one creator; they degrade across three axes at v1.0:

1. **Query performance** — reconstructing "current canon" from an append-only log at judge-call time will dominate latency past ~500 events (Claude).
2. **Provenance staleness** — "observed/inferred/confirmed" labels are onboarding-time confirmations; without a re-confirmation cadence, "confirmed" facts confirm a canon that has moved (Claude).
3. **Multi-tenancy and data primitives** — files-not-engine is right for governance, wrong as a per-creator data plane; export/delete/isolation must be spec'd now (Claude).
4. **Missing typed event ledger** — need stable IDs (series, installment, character, canon fact, reference exemplar, canon-update event, evidence artifact), typed events (observed/inferred/confirmed/superseded/deprecated/declared), temporal/scoping fields (applies_from/to, arc scope, exception scope), and lossless migratability to SQLite/Postgres/vector store (GPT-5.5).
5. **Replay rule** — every verdict must be reproducible against the exact canon snapshot used (GPT-5.5).

**Write into ratification now (merged from both):**
- Materialized "current canon" snapshot rebuilt on write.
- Confirmation-decay policy (facts older than N installments demote to "inferred").
- Typed event ledger with stable IDs.
- Per-creator data boundary with export/delete primitives specified (even if unimplemented).
- Verdict-replay guarantee against exact canon version.

**Gemini's dissent — D8:** Single-orchestrator becomes a "god agent" by v1. Fix: mandate that all Orchestrator↔role communication uses a versioned, documented internal API (JSON schema for tasks/results), with the Orchestrator forbidden from touching other roles' internal state. This is a reasonable additional amendment, but Claude and GPT-5.5 both judged D8 sound-as-is with only minor caveats (token budgets on fan-out). Treat Gemini's fix as a low-cost amendment rather than a required rewrite.

---

## 5. RATIFY AS-IS — Convergence and the one true consensus lock

| Decision | Claude | GPT-5.5 | Gemini | Verdict |
|----------|--------|---------|--------|---------|
| **D1** — Release-gate contract | ✅ Lock | ✅ Lock | ✅ Lock | **Unanimous lock** |
| **D6** — Verification stack | (fine) | ✅ Lock | ✅ Lock | **Lock** |
| **D7** — Autonomy/permissions | ✅ Lock (enforcement-parity is the load-bearing bit) | ✅ Lock | — | **Lock** |
| **D8** — Orchestration | (right direction, needs token budget) | ✅ Lock | V1 debt | **Lock with Gemini's API-boundary amendment** |
| **D10** — Founder envelope | ✅ Lock (20% meta-tooling budget + review-inbox-first is the discipline) | Depends on D5 not exploding | — | Lock, but stress-test after D5 fix |
| **D3** — Eval constitution | (50-case ceiling too low) | Needs tightening (regression harness ≠ market quality) | ✅ Lock | **Lock with explicit "not a downgrade license below 200 cases"** |
| **D9** — Observability | (needs cost-per-verdict) | Unsafe until D11-data pairs with it | ✅ Lock | **Lock contingent on data-boundary D11** |
| **D2** — Deterministic pipeline | (fine) | ✅ Lock | — | **Lock** |
| **D4** — Canon model | V1 debt | V1 debt | ✅ Lock | **Lock with the merged amendments above** |
| **D5** — Model routing | **Weakest** | **Weakest** | **Weakest** | **Do not lock as written** |

**Cleanest unanimous ratifications: D1 and D6.** Claude flagged D1 as "the most defensible piece of the whole design" — the three-way verdict with receipts and advisory-default aligns product semantics with the actual pain (creator distrust of automation).

---

## Chairman's meta-note

Claude's closing observation deserves surfacing: *the proposal is unusually well-grounded — citations to Stripe/Ramp/Anthropic/OpenAI are load-bearing, not decorative. The risk isn't sloppy thinking; it's coherent thinking built on a 32-case spike.* Two of three council members converged on this framing.

**The single highest-leverage action before ratification** (Claude, endorsed here): run the pipeline against **3 real creators' back-catalogs**. If canon extraction holds up, D1/D2/D6/D7/D8 stand largely as written and only D4/D5 need the amendments above. If it doesn't, D2's deterministic layer and D5's panel design both need to be rethought before anything gets locked.

**Recommended sequencing:**
1. Run the 3-creator canon-extraction test (Claude).
2. Lock D1, D2, D6, D7, D8 (with Gemini's API-boundary amendment).
3. Amend and lock D4 (event ledger, materialized snapshot, replay guarantee, tenant primitives).
4. Rewrite D5 with axis-specific disagreement policy, max-NR-rate alarm, ≥200-case downgrade threshold, and degraded-mode local-fleet fallback.
5. Ratify D11 (data/IP boundary — GPT-5.5), D12 (dispute→eval loop — Claude), D13 (artifact promotion — Gemini) before their respective month-6 gates.
6. Lock D3, D9, D10 last, once D5 and the new decisions constrain them properly.
