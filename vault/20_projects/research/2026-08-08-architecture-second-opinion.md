---
title: "Architecture second opinion — Fable 5 master-architect review with fresh research"
date: 2026-08-08
project: agent-company-founding
type: opinion
status: final
tags: [agent-company, architecture, second-opinion, L10-campaign]
---

# Second opinion on the ratification package

Sean asked for my own view — with up-to-date research, since the council
members carry older training cutoffs. Four fresh research sweeps ran today
(2026-08-08), all primary-source: 2026 multi-agent failure literature, visual
consistency SOTA + live competitive check, LLM-judge evidence, and the Arize
stack. Reports mirrored in
[2026-08-08-architecture-second-opinion/](2026-08-08-architecture-second-opinion/).

## Verdict: the direction is right. Sign it — with the amendments below.

Three independent lines now converge on this architecture's core thesis:
the demand evidence (verification is the vacant seam), the factory literature
(verification is the scarce capability), and today's academic sweep — MAST's
canonical taxonomy attributes ~42% of multi-agent failures to bad
specification and ~21% to weak verification, which are precisely the two
things this architecture over-invests in (coded state machines with explicit
exit conditions; layered deterministic gates). Cognition's own revised 2026
position — "writes stay single-threaded; additional agents contribute
intelligence rather than actions" — is D8 almost verbatim. The 2025
single-vs-multi-agent debate collapsed into the shape we already chose.

And the wedge held up under a live check TODAY: Novarrium, Novelium, and
Bunsho remain text-only (Bunsho still pre-beta); no new entrant ships visual
consistency *verification*; every generation vendor exposes consistency as an
input (reference locking), never as an audit report. The trade press states
plainly that nobody ships end-to-end identity QA at production quality. The
moat is execution speed and stylized-domain calibration — the metric recipes
are public.

## Where fresh evidence amends the package

### A1 (D5) — The judge panel's job is disagreement detection, not voting
The council kept the 2-model panel; the freshest evidence sharpens WHY 2 is
right and 3+ is wrong: a May 2026 study found a 9-judge cross-family panel
carried only ~2 effective independent votes (correlated errors), and a single
best judge matched the panel. Keep exactly 2 judges, maximally diversified
(different vendor + different evidence access), and treat disagreement events
as the highest-information samples (judge disagreement = 44% of pipeline
variance in a 2026 decomposition) — logged and mined, not averaged away.
Additional binding requirements: judges run at **temp 0, version-pinned**
(provider silent updates are a documented drift source; a judge swap is a
recalibration event, not a config change); judgments are **pairwise against
the locked reference, never absolute scores** (April 2026: VLM judges rank
well, score badly — absolute-score intervals span 40-70% of the range);
agreement measured with **chance-corrected κ/α, never raw agreement** (98%
raw can mask α≈0 at high Pass rates); **OCR handles rendered text** (VLM
judges are <50% accurate there — deterministic escape, pre-registered);
structured forced-choice per axis (now shown to beat chain-of-thought for
bias reduction). The axis-specific disagreement policy the council and I
wrote is exactly what the June 2026 criterion-specific-agreement paper
prescribes — that part stands unchanged.

### A2 (D2/D13) — Durability is a gap the council missed
2026's new consensus: **checkpointing is not durable execution.** Saved state
without failure detection, automatic resumption, and idempotency keys on
side-effectful steps is theater — a crashed overnight run just sits there,
and a naive resume double-fires side effects. A solo founder cannot be the
watchdog. Binding requirements for the runtime: persist state at every
LLM/tool boundary; watchdog with automatic resume; **idempotency keys on
every state-writing call**; and **agent-to-agent conversational loops are
structurally banned** (the $47K and $48K documented cost incidents were both
two-agent loops with undefined "done"). Every stage carries a
machine-checkable success criterion and a per-run token/dollar kill-switch —
Sean's existing cap_policy pattern, made universal.

### A3 (D8) — Don't seat the smartest model as orchestrator
The 2026 "Reasoning Trap" result: frontier reasoning models often
*underperform* as orchestrators (context squeezing under coordination load),
and the god-agent is now a named anti-pattern. Our answer is already
"coordination lives in code," but make it explicit: the orchestrator-agent
does leaf-work planning only; a mid-tier model may hold that seat; the
frontier models belong in the judge and hard-reasoning lanes. Also: any model
swap re-earns its lane's autonomy **inside the harness** (one 2026 study saw
89%→11% accuracy collapse when a model moved into multi-agent context), and
escalation triggers live in code — weaker models demonstrably cannot
self-assess when to escalate.

### A4 (D2/D4) — The visual lane has a concrete technical recipe now
The SOTA stack for stylized-character identity: **detect (Grounding DINO) →
crop → embed (DINOv2 on character crops) → per-series reference anchoring →
bipartite matching**, reporting cross-similarity to locked references AND
self-consistency across the set — with the VLM judge layered on top strictly
in pairwise mode to explain *what* drifted in creator-actionable language.
Two important notes: (1) this **rehabilitates anima's DINOv2 negative
result** — the 2026-06 similarity-gate failure compared whole plates against
one anchor; the SOTA recipe's detect-crop-anchor pipeline addresses exactly
that view-variance failure, so the embedding layer returns to the
architecture as a cheap deterministic pre-filter feeding the judge; (2)
detector failure on heavily stylized panels is a known mode → **"unverifiable
panel" is a first-class verdict state**, never a silent skip. No
"ArcFace-for-stylized" checkpoint exists yet; the Anime-2026 ID-labeled
dataset is the calibration substrate if we ever fine-tune. FlawedFictions'
text-canon caution stands unchallenged — another reason visual-first
shipping order is right.

### A5 (D9) — Arize: Phoenix OSS self-hosted, $0
Concrete stack decision for step 5: **Phoenix open-source, self-hosted in
Docker on the Mac Mini, PostgreSQL-backed** — $0/month, no usage caps, evals
as pytest in CI, OpenInference/OTel tracing, and it ships an MCP server that
plugs into Claude Code. Config requirements that are footguns otherwise: set
`PHOENIX_WORKING_DIR` (default SQLite lives in a temp folder), set explicit
retention (default is infinite → unbounded growth), use Postgres not SQLite.
**Client-side masking/redaction before spans leave the app** — capture-
everything is the default and there is no one-flag privacy preset — this is
where D11's data-minimization requirement gets implemented. Optional: an AX
Free account (25k spans/mo, 15-day retention) pointed only at the
customer-facing production slice for managed alerting; otherwise alerting is
cron + Pushover (existing fleet pattern). Langfuse is the only credible
alternative; nothing else fits ≤$250/mo.

### A6 (D1/D12) — Receipts change behavior in a specific, budgetable way
A July 2026 study: detailed explanations raise *system* trust while
*increasing* per-verdict human overrides (users scrutinize more) — and no
explanation at all produces silent abandonment, not complaints. This
confirms receipts-mandatory (D1) and adds a planning fact: expect the
dispute/override rate to RISE as receipts improve. Budget D12's review flow
for engaged pushback — it's the desired behavior, and per-creator dispute
rate doubles as the calibration metric.

## My own additions (beyond council and research agents)

1. **Fix the Needs-Review denominator before pre-registering the 15%.** An
   installment with 40 panels × 6 axes is 240 checks; 15% of checks is still
   36 flags — spam by another name. The alarm the creator feels is
   **actionable items per installment**. Define the gate's UX budget: top-N
   items by severity (N≈5-7) surfaced actively, the tail folded into a
   digest, and the pre-registered alarm set on median actionable-items-per-
   installment, not on % of checks.
2. **Onboarding economics need a named bound.** Bible extraction over a
   200-installment back-catalog is the expensive, failure-prone step and the
   quiet path to becoming a services business. Add to D10: onboarding
   compute cost per series must be measured from the first extraction test,
   with a target ceiling (rule of thumb: < one month's subscription price at
   the intended tier). If real catalogs blow the ceiling, tiered onboarding
   (recent-N installments first, backfill lazily) is the fallback design.
3. **Declare modality maturity tiers and shipping order now.** The
   multimodal promise is the wedge, but the lanes differ in maturity: visual
   stills (spike-validated) > text canon (contested lane + FlawedFictions
   caution) > video (untested). Ship visual-first with text-canon as the
   companion check; video enters only behind its own feasibility spike. This
   protects the brand from launching on the weakest lane and keeps the
   "multimodal" claim honest ("one drift report" ≠ "every modality at parity
   on day one").
4. **Name the month-6 autonomy lanes now.** [L6]'s 30-day autonomy proof
   needs its lanes declared so the fleet is built toward them: intended
   lights-off by month 6 — monitoring/Watchdog, daily digests, re-checks on
   published installments, build-log drafting; never lights-off — product
   code merges, canon confirmations, D11-sensitive data actions, spend above
   caps. This makes the autonomy bar concrete and honest instead of
   retrofitted.
5. **The build-in-public layer has no decision.** [L2] makes it the
   attention engine, yet D1-D13 don't cover it. Small addition (fold into
   D10 or a lightweight D14): the museum-capture pattern from anima —
   approvals/rejections/retries write capture artifacts as they happen, a
   weekly build-log post assembles from them, and D11 governs what is
   publishable (never creator content without consent; fleet metrics and
   drift-report anatomy on Sean's own serials are the safe default corpus).
6. **Stop adding decisions after this.** Thirteen decisions plus these
   amendments is a complete constitution for v0.1. The failure mode from
   here is ratification as a substitute for contact with reality. After
   Sean signs: canon-extraction test (3 creators), then ONE thin vertical
   slice (one creator, one series, stills+text, advisory report,
   Phoenix-traced end to end). Every remaining unknown is cheaper to answer
   with that slice than with a fourteenth decision.

## Amended sequencing (supersedes the package's list)

1. Sean signs the package with amendments A1-A6 + additions 1-5 folded in.
2. Canon-extraction test on 3 real creators' back-catalogs (pre-lock
   condition for D2/D4/D5 stands; now also measures addition-2's onboarding
   cost bound).
3. Step 5 (eval-stack design) collapses mostly into implementation: Phoenix
   self-hosted per A5, trace schema per D9/D13, spike corpus as eval seed.
4. Step 6: wayfinder ticket map for the thin vertical slice.
5. Build the slice. Dogfood on Sean's serials. Then the wedge segment /
   business-model partner axes, informed by a running product.

## Provenance

Fresh research (all 2026-08-08, primary sources): [orchestration/failure
literature](2026-08-08-architecture-second-opinion/research-orchestration-2026.md) ·
[visual SOTA + competitive](2026-08-08-architecture-second-opinion/research-visual-consistency-sota.md) ·
[judge evidence](2026-08-08-architecture-second-opinion/research-llm-judge-evidence.md) ·
[Arize stack](2026-08-08-architecture-second-opinion/research-arize-stack.md).
Campaign inputs: [ratification package](2026-08-08-architecture-ratification-package.md) ·
[council transcript](2026-08-08-architecture-proposal-v1-council-premortem.md) ·
[spike](2026-08-08-vision-drift-feasibility-spike-go-no-go.md) ·
[lit review](2026-08-08-software-factory-literature-review.md) ·
[groundwork audit](2026-08-08-groundwork-v1-audit.md).
