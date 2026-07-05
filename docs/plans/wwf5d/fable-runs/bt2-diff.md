# BT2 diff — Fable vs Opus on zoom-out-and-think(anima register-transport seam)

**Compared:** `fable-runs/bt2-fable.md` vs `baselines/bt2-opus.md`.
**Method:** identical harness, identical four pinned anima paths @ `aa2007c`, identical pinned grounding; both ran real web research; both stayed read-only in anima. Deltas are quality-only, tagged `dangerously-wrong` / `structural` / `minor`, direction **FABLE+** (admissible WWF5D evidence, F1) or **OPUS+** (ceiling, F3).

**Headline:** this is the tightest pairing of the battery — Opus's diagnosis coverage is near-parity (same root-cause family, same four-part fix shape, several excellent analytic lines). Fable's edge concentrates in three clusters: *epistemic discipline about unobserved code*, *decided-not-optioned spec mechanics*, and *implementation-hazard anticipation*. The diagnosis zoom-out itself is largely **cheap on Opus**.

---

## FABLE+ deltas (admissible WWF5D evidence)

- `structural` — **FABLE+ — Unobserved code stays unasserted; Opus stated an unobserved failure mode as implemented fact.** The fail-loud-on-unwired-engine property lives in `character_designer._resolve_plate_model`, which neither model read (outside the four pins). Fable classified it precisely: "an **assumption about un-pinned code**... It must be made true by test, not asserted in prose" — and converted it into a spec obligation (prove by test that generating primal today raises). Opus — despite exemplary `[referenced, not read]` scope-marking elsewhere — wrote into its intended-vs-implemented table: "a missing/unrouted model **degrades to NB2 by default**, the exact silent fallback the intent forbids... implementation gives the opposite (silent NB2)." That conflates the observed data-level truth (an untranscribed decision leaves NB2 in the field) with an unobserved dispatch-level claim (unknown engine id silently falls back at runtime), asserting the latter in the row whose whole job is separating documented intent from *verified* behavior. The pinned grounding was deliberately narrowed before the runs to kill exactly this move (overclaim → "open risk, not confirmed failure"); Fable held the narrowed framing on both open questions, Opus held it on one (edit-identity) and broke it on the other (fallback behavior).

- `structural` — **FABLE+ — Consumed and amplified the prose-drift evidence; Opus dropped it.** The pinned answer (b) hands both models a drift fact: the field report's §4/§6 still listed grossout as pending-look-spike while grossout's own research.md recorded the spike RESOLVED the same day. Fable restated it, found a **second instance of the same class inside one file** (grossout research.md's header and §9 still say pending/unproven while its own §0/§4 record the resolved verdict), and promoted the pattern to root-cause evidence: the prose stores can't even stay consistent with *each other*, "which is what hand-copying state to N places always produces." Opus's restatement compressed the drift detail away ("each a separate event") and its analysis never used it — its doc-staleness row covers only primal's research.md vs the field report. Given that the task is literally about decided values failing to travel, dropping a pinned decided-input from the grounding restatement is the on-theme miss.

- `structural` — **FABLE+ — Domain-matched research; Opus's was adjacent-domain only.** Both searched for real. Opus cited LLM text-routing sources (RouteLLM, a model-routing guide, LiteLLM fallback docs) — sound for the generic routing shape — and honestly conceded its sources "don't cover" the validation-gate half, bridging by argument. Fable's citations land on the actual domain: per-style **image-generation** specialization literature (multi-style joint training degrades quality; one-specialist-per-style is the norm) that independently corroborates the spike's "model limit, not style limit" verdict; eval-gates-as-blocking-deployment-gates for the costed-Bible-pass gate; silent-quality-degradation as the named worst failure mode; plus a house-style precedent (code-brain's own hybrid-router `fallback="none"` → `RouteUnavailable`) showing the fail-loud pattern is already local doctrine. Net: Fable's two sharpest claims rest on prior art; Opus's rest on the field report plus analogy.

- `structural` — **FABLE+ — Decided mechanism, not optioned mechanism.** Opus's class-fix leaves design open at the decisive joint: "e.g. an explicit `transport_rationale` / `transport_validated` field, **or** by requiring `generation_model` to be set explicitly per register" — the implementer picks. Fable pre-makes the call: a `transport_status` record with three named states (`default-ratified-by-use` / `spike-ratified-edit-identity-pending` / `edit-identity-validated`), each carrying date + evidence path, plus **two named structural consumers** — a completeness test mirroring the existing suite pattern, and the costed-Bible-pass entry point refusing unvalidated escalations with an error naming the missing step. Same intent; one version survives a weaker implementer's tiebreakers, the other delegates the exact decision the whole diagnosis says keeps getting made ad hoc.

- `structural` — **FABLE+ — Anticipated the likeliest implementation breakage: the frozen-dataclass / characterization-oracle collision.** Fable's edge cases defuse the anima-specific landmines: add the new field **with a default** so the six byte-pinned legacy specs don't shift; if the oracle asserts whole-spec equality, extend it deliberately in its own commit — "never weaken it"; REGISTRY insertion order is load-bearing (stub-keyword precedence) and must not reorder; `reference_images` backfill is Sean's call — do not auto-populate from folder listings; grossout stays Sean-gated with its future transport state pre-decided. Opus's spec never engages the byte-pin oracle at all — the single most probable way a Phase-C implementer breaks the suite with this exact change.

- `minor` — **FABLE+ — Complete verdict-landing checklist.** Fable's part 2 lands the primal verdict everywhere it's stale, including the **in-spec comment block** still calling NB2 "the §3c transport HYPOTHESIS" and the research.md header's `PENDING SPIKE` status, and inverts prose to *reference* the registry as record. Opus catches the module docstring's stale line but never the per-spec comment — an implementer following Opus ships a commit whose field says gpt-image while the adjacent comment still says NB2-hypothesis.

- `minor` — **FABLE+ — Band-aid refusal covers both directions.** Both refuse the under-fix (flip primal's string and stop; silent fallback; verdict-in-a-comment). Fable additionally refuses the over-fix — "build a router service/classifier" — naming the registry-as-declarative-map as already architecturally correct. Bounding the fix from above is what keeps a weaker implementer from gold-plating.

## OPUS+ deltas (ceiling evidence — F3)

- `minor` — **OPUS+ — The two-axes guard.** Opus explicitly separates *register* defaulting (`DEFAULT_REGISTER`, empty→pencil-test back-compat — correct, keep) from *model* defaulting (the problem), with "do not entangle the two" in What-NOT-to-change. Fable protects the same code behaviorally but never names the axis-confusion hazard a hurried implementer could fall into.

- `minor` — **OPUS+ — Explicit anti-fabrication rule for the engine id.** Opus: "The exact gpt-image id... is a real dependency — **do not fabricate an id**; source it." Fable's spec requires adding the constant (and the sourcing is implied by TDD + deferral) but never states the don't-invent-the-string rule outright.

- `minor` — **OPUS+ — The state-aliasing articulation.** Opus's sharpest line: because an untranscribed decision still yields NB2, "'nobody routed this register' and 'this register is routed to NB2' are the **same observable state**." Both models' fixes encode the distinction (Fable's three-state record; Opus's ratified-vs-inherited marker), but Opus named the underlying aliasing most crisply — worth stealing as diagnostic vocabulary.

## Matched (no meaningful delta — cheap on Opus)

- The seam-cannot-express discovery (no gpt-image constant exists, so the verdict physically can't land) — both.
- The split-decider orchestration diagnosis (spike decides / prose records / code asserts; reconciliation is nobody's job) — both, independently phrased.
- Flagging the field report's own pending action (flip primal's field) as a band-aid if done alone, with the red-flag checklist run explicitly — both.
- `UnknownRegisterError` named as the in-repo philosophy to mirror at the engine level — both.
- Gating the costed Bible pass on across-edit identity as a structural precondition — both (Fable specifies the no-op scope and error content; Opus specifies the always-surface tiebreak rule — complementary accents).
- Grossout as the control case proving the default is right-often-enough-to-rot (Opus's row-7 framing; Fable's confirmed-correct list) — same substance.
- Read-only discipline in anima, and diagnosis-only scoping with explicit Phase-C deferral — both clean.
- Harness self-checks against the skill's success criteria — both complete.

## Slice-3 gate judgment (for the runbook's Slice 3 decision)

Fable's BT2 output is **production-grade as the anima register-seam spec**: decided mechanisms, TDD-sequenced, edge-case-armored against the repo's real tripwires, checkable done-criteria, band-aid tripwires for review. Recommend saving it as `anima-register-seam-spec.md` per the runbook default, with two small Opus-baseline guards worth folding in at Phase C: the two-axes non-entanglement note and the explicit don't-fabricate-the-id rule.

## Hypothesis pointers (for 1d corroboration)

- Q1 ("ground truth vs stated truth — verify against artifacts before believing") → corroborated: the unverified-property discipline (assumption-flagged, converted to test) vs Opus's row-4 assertion.
- Q3 ("trace to point-of-effect; duplicated sources of truth as seam class") → corroborated: the seven-store state table with freshness/owner columns; the prose-vs-prose drift amplification.
- Q6 ("research trigger: expensive-to-reverse design with prior art; domain-matched, not generic") → corroborated: per-style image-gen literature + eval-gate sources vs adjacent-domain-only.
- Q7 ("pre-made decisions; exact anchors; negative space; edge guidance for the weaker implementer") → corroborated: three-state record with named consumers; oracle-collision defusal; both-direction band-aid bounds.
- Q4 (zoom-out to root cause) → **matched, cheap on Opus** — the zoom-out itself is not where Fable's premium lives on this task.
