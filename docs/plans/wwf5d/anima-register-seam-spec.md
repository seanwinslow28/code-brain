# anima register-seam spec (register-transport / per-register model routing)

> Provenance: the BT2 blind Fable run (`fable-runs/bt2-fable.md`), saved verbatim per
> the Phase B runbook Slice-3 default — the diff (`fable-runs/bt2-diff.md`) judged it
> production-grade. anima pinned @ `aa2007c`, read-only; implementation is Phase C,
> Opus, own branch, TDD. Two Opus-baseline guards to honor at implementation:
> (1) do not entangle the register-default axis (`DEFAULT_REGISTER`) with the
> model-routing axis; (2) do not fabricate the gpt-image engine id — source it.

# BT2 — zoom-out-and-think: anima's register-transport / per-register model-routing seam

**Run:** 2026-07-05 · Fable (Phase B blind run)
**Harness:** `.claude/skills/zoom-out-and-think/SKILL.md` @ code-brain `93e5725`
**Subsystem:** anima @ `aa2007c` (working tree verified at exactly this SHA; repo untouched — read-only throughout)
**Pinned inputs read (nothing else in anima):**
- `docs/active/2026-07-04-register-backlog-and-transport-findings.md` (the field report)
- `registers/90s-nicktoon-grossout/` — `research.md` + `refs/README.md` (+ refs file listing: `AI-Guru-ChatGPT-{1,2,3}.png`, `AI-Guru-NB-Pro-1.jpeg`, `AI-Guru-NB2-{2,3}.jpeg`)
- `registers/primal-sketch-grit/` — `research.md` + `refs/README.md` (+ refs file listing: `grandmaster-chosen-pose-{1,2,3}.png`, `spike-2026-07-04/{A-register-verbatim,B-grit-amplified,C-route-c-pencil}.png`)
- `pipeline/registers.py`

Grounding answers pre-pinned per `docs/plans/wwf5d/task-battery.md` §"BT2 — Pinned grounding answers"; restated below, then Step 2 entered directly per the run prompt. This document is diagnosis and spec only — no implementation.

---

## Step 1 — Grounding (pre-pinned; my restatement of each)

**(a) What keeps recurring.** The failure class is: *register transport gets decided per-register by ad hoc spike rather than through the one routing seam built to hold it.* Concretely, three live instances: (1) `pipeline/registers.py` hardcodes `generation_model=NB2_FLASH` for every one of its seven registers — the routing map exists as a field but expresses only a universal default; (2) that universal default (NB2) demonstrably fails `primal-sketch-grit` — Sean's 2026-07-04 four-engine test confirmed NB2 cannot render the Tartakovsky-*Primal* grit and specifically cannot *edit* a frame into it, a **model limit, not a style limit** (gpt-image was best by far); (3) for any register whose transport escalates off NB2 (e.g., to gpt-image), that engine's ability to hold identity across the edit pipeline's handoffs (anchor → turnarounds → expressions) is **unvalidated — a real open risk the field report flags, not yet a confirmed failure**. I hold that narrowed framing throughout: the across-edit identity question is an open gate, not an observed break.

**(b) What's been tried.** Three patch shapes, none of which changed the seam: (1) *universal NB2* as the hardcoded default for all seven registers — confirmed in `pipeline/registers.py` (every spec: `generation_model=NB2_FLASH`); (2) *per-register prompt nudges* — e.g., `90s-nicktoon-grossout`'s gross-up-ratio correction after Sean rejected the first draft's constantly-grotesque output (`registers/90s-nicktoon-grossout/research.md` §0: the corrected register makes the appealing warm cel-human the ≈90% default and the gross-up a sparse punctuation); (3) *per-register look-spikes ratified case-by-case* — the `primal-sketch-grit` go/no-go spike (field report §1) and the `90s-nicktoon-grossout` cross-engine spike (its research.md §0, §4 — noting the field report's own §4/§6 still listed that register as pending look-spike as of 2026-07-04, i.e., the two prose records were already out of step with each other on the same day).

**(c) What "coherent/correct" looks like end-to-end.** Per-register model routing that actually routes: each register rendered by the model that can hold its look, with `RegisterSpec.generation_model` / `final_model` populated as a first-class architectural decision — "the deliverable, not a comment," in the field report's words — rather than a default nobody revisits; identity validated across every edit-pipeline handoff *before* a register's first costed Bible pass; and the routing decision living in exactly one place (`pipeline/registers.py`) instead of scattered per-register patches.

---

## Step 2 — Read the Whole System

### 2.1 State — where transport truth lives, and who thinks they own it

| Store | What it holds today (@ `aa2007c`) | Owner-in-theory | Freshness |
|---|---|---|---|
| `pipeline/registers.py` — `REGISTRY` (7 frozen `RegisterSpec`s) | `generation_model=NB2_FLASH` for **all seven**; `final_model` = NB2 ×3, NB_PRO ×4 (painterly-final seam, documented consumer-less); primal's spec comment (lines 241–253) still calls NB2 "the §3c transport HYPOTHESIS — the go/no-go spike judges it" | **The designated system of record** — the field report §1: this field "**is** the 'which model for which style' map. Setting it is the deliverable, not a comment." | **Most stale of all stores.** The spike judged the hypothesis on 2026-07-04 (NB2 NO); neither the field nor the comment moved. |
| Engine constants in `registers.py` | Only `NB2_FLASH` (`gemini-3.1-flash-image-preview`) and `NB_PRO` (`gemini-3-pro-image-preview`); module comment (lines 44–47) frames NB2 as "the generation/editing default for **every** register" | Same file | No gpt-image id exists anywhere in the module — the seam **cannot express** the ratified verdict even if someone tried to record it. |
| Field report (`docs/active/2026-07-04-…-transport-findings.md`) | The transport rule (§1), primal's verdict (gpt-image; NB2 no), the edit-identity open question, the roster table (§6: primal "transport-escalated, **gpt-image**"), pending actions (§7) | A "living backlog" — explicitly *not* the record; §1 says the record is the RegisterSpec field | Ahead of the code on primal; **behind its own neighbor** on grossout (§4/§6 say "look-spike first / TBD" while the register's research.md records the spike RESOLVED the same day). |
| `registers/primal-sketch-grit/research.md` | §1 row + §4: `generation_model` "NB2 … **hypothesis**, judged by the go/no-go spike"; header: "transport verdict `PENDING SPIKE`" | Register-local research record | Stale — field report §7 lists updating its §4 transport line as pending. |
| `registers/90s-nicktoon-grossout/research.md` + `refs/README.md` | §0/§4: cross-engine spike **RESOLVED 2026-07-04, NB2 GO**, Sean-ratified, 6 exemplars in `refs/`; draft RegisterSpec (§1) deliberately **not** authored into the registry (Sean-gated) | Register-local research record | Internally uneven: the header still says "look-spike PENDING" and §9 still says "Transport … is unproven" while §0/§4 of the *same file* record the resolved verdict. |
| `refs/` folders (both registers) | Spike evidence images (primal `spike-2026-07-04/`, grossout's 6 exemplars); primal also holds `grandmaster-chosen-pose-{1,2,3}.png` | Human-eye ratification evidence | On-disk evidence has landed, but `RegisterSpec.reference_images` is still `()` for every register — the READMEs say to update the tuple "in the same commit that adds them." A minor echo of the same lag pattern (flagged, not adjudicated — which files count as confirmed exemplars is Sean's call). |
| `briefs/2026-07-02-grandmaster/go-no-go.md` (referenced by the pinned docs; outside the pinned read set) | The escalation ladder and the edit-consistency gate ("the real GRANDMASTER production gate") | Brief-local prose | The *only* home of the before-first-costed-Bible-pass gate — nothing in code or tests knows it exists. |

The classic recurring-bug shape from the skill's Step 2.1 is present exactly: **transport state has two components that both behave as its owner** — the registry (what the pipeline reads) and the prose docs (where verdicts actually land) — and the designated single home is the one place the truth never arrives. Worse, the prose can't even stay consistent with *itself* (field report §4/§6 vs grossout research.md §0/§4; grossout research.md header/§9 vs its own §0/§4), which is what hand-copying state to N places always produces.

### 2.2 Control flow — the three lifecycles

**Generation lifecycle (the consumer path):** character folder `character.yaml` `style_register` → caller applies the back-compat rule `get_register(value or DEFAULT_REGISTER)` → empty/missing coerces to `pencil-test-colored`; nonempty-unknown raises `UnknownRegisterError` **loud** (never a silent coercion) → the returned `RegisterSpec` feeds `character_designer._build_plate_prompt` (clause fields) and `character_designer._resolve_plate_model` (`generation_model` / `final_model`) → engine call → Cy's Bible pass, an **edit** pipeline (anchor → turnarounds → expressions) that must hold identity across every plate. Note the asymmetry: the register *name* has hardened, loud, tested failure semantics; the register's *engine id* has none that the pinned code demonstrates.

**Authoring lifecycle (the five-step drill):** research → one `RegisterSpec` entry → Cy `## What good looks like` block → template-comment line → run the suite (completeness tests refuse to pass until all exist — `tests/test_register_registry.py` enforces the prose touch-points, `test_register_characterization.py` byte-pins the six legacy registers, `test_prompt_style_neutrality.py` checks markers). The drill structurally enforces *taste* artifacts per register. It does **not** structurally enforce that the transport verdict lands: nothing in the drill or the suite fails when a ratified spike verdict and the spec's `generation_model` disagree.

**Spike lifecycle (the actual transport decider):** cheap cross-engine look-spike → Sean's eye ratifies → verdict is written into research.md §4 / the field report → a "pending code change" bullet is filed (field report §1, §7) → *(intended)* the verdict lands in `RegisterSpec.generation_model` → *(actual)* it never has. The escalation ladder is pre-agreed and disciplined (primal research.md §4: NB2-from-text → NB2 + style-feed → NO-GO → Route C; "**never a new transport mid-Bible-pass**") — the *procedure* is sound; the missing edge in the graph is the last arc, spike verdict → registry field. That arc currently runs through human memory and a backlog bullet.

### 2.3 Orchestration — who decides vs. who executes

- **Sean's eye** decides looks and transport verdicts, per-register, via cheap spikes. This is correct by doctrine ("validators cannot recover taste that was absent at generation time") and is not the problem.
- **`pipeline/registers.py`** is *documented* as the decider — "the 'which model for which style' map" — but as-built it decides nothing: it uniformly asserts one constant. It executes a default while wearing the decider's title.
- **The edit-identity gate** ("small edit-consistency spike before its first costed Bible pass," field report §1) has **no structural owner at all** — it lives in a brief's prose. No field records whether a register's transport has been edit-validated; no code path can refuse a costed Bible pass on an unvalidated escalated transport.

Recurring bugs cluster exactly where "who decides this" is split (skill Step 2.3). Here the split is threefold: the human decides, the prose records, the code asserts something else — and reconciliation is nobody's job.

### 2.4 Intended vs. implemented (the field report's documented intent vs. `pipeline/registers.py` today)

| # | Documented intent (field report, 2026-07-04) | Implemented (`pipeline/registers.py` @ `aa2007c`) | Gap |
|---|---|---|---|
| 1 | "Transport is **per-register**, decided by a cheap spike. NB2 is the **default**" — a default, not a universal | All seven specs: `generation_model=NB2_FLASH`; module comment: NB2 "is the generation/editing default for **every** register" | The code still encodes the pre-finding worldview (universal NB2). Per-register routing exists only as a field name. |
| 2 | "`RegisterSpec.generation_model` / `final_model` … **is** the 'which model for which style' map. Setting it is the deliverable, not a comment." | The map can only spell two Gemini ids; no gpt-image constant, no third-engine vocabulary, no way to record a verdict's status or evidence | The seam is under-expressive for the decisions it is documented to own — verdicts physically cannot land in it without inventing conventions on the spot. |
| 3 | §1/§6: `primal-sketch-grit` → **gpt-image** ("NB2 no"; four-engine test; roster row says "transport-escalated") | `primal-sketch-grit.generation_model=NB2_FLASH`, comment still calling NB2 the "transport HYPOTHESIS — the go/no-go spike judges it" | The spike judged it — NO — on 2026-07-04. Code, comment, and primal research.md §4 all still say hypothesis/NB2. The registry's own roster disagrees with the field report's roster table. |
| 4 | "A gpt-image id with no wired runner will **fail loud** at generation (correct — never silently fall back to NB2)." | Nothing in the pinned code demonstrates this. The loud-failure guarantee that *does* exist (`UnknownRegisterError`) is register-**name**-level, not engine-**id**-level | Fail-loud on an unwired engine is currently an **assumption about un-pinned code** (`_resolve_plate_model`), not a verified property. It must be made true by test, not asserted in prose. |
| 5 | "Any register whose transport is gpt-image needs a **small edit-consistency spike before its first costed Bible pass** — the real GRANDMASTER production gate." | No field, no test, no gate. `RegisterSpec` carries no validation state; the Bible pass has no structural reason to refuse an unvalidated escalated transport | The production gate exists only as prose in `go-no-go.md`. A future session that forgets it loses the money-safety property silently. |
| 6 | Spike evidence stays with the register; `reference_images` updates "in the same commit that adds them" (refs READMEs) | Evidence files have landed in both `refs/` folders; every spec's `reference_images` is still `()` | Minor echo of the same lag class (which files are confirmed exemplars is Sean's call — flagged, not adjudicated). |

**Where intent and implementation agree (confirmed correct — protected in Step 5's "What NOT to change"):** the closed vocabulary with `UnknownRegisterError` loud-on-unknown and the caller-owned `value or DEFAULT_REGISTER` back-compat; the load-bearing REGISTRY insertion order (stub-keyword precedence, oracle-pinned); all seven registers' taste fields (identity_lock / preserve / style_token / markers — Sean-ratified, byte-pinned for the legacy six); `90s-nicktoon-grossout` deliberately **not** authored (candidate gating working exactly as intended — its NB2 GO verdict is recorded for the authoring session, and authoring stays Sean-gated); the refs non-derivative conventions; and the spike doctrine itself (cheap spike + Sean's eye is the right instrument — the grossout spike *prevented* a wrong escalation by finding NB2 GO where the primal precedent predicted otherwise).

---

## Step 3 — Current best practice for per-content-type generative-model routing (real web search, 2026-07-05)

The precise domain: **a multi-model generative pipeline that must route each content type (here: style register) to the engine that can actually hold it, with the routing policy in one declarative seam, human-ratified quality verdicts as the routing signal, validation gates before production spend, and explicit failure semantics when a route is unavailable.** Four searches were run; findings that ground the diagnosis:

1. **Routing policy as declarative, human-preference-aligned data in one seam — not scattered decisions.** Arch-Router ([arXiv 2506.16655, "Arch-Router: Aligning LLM Routing with Human Preferences"](https://arxiv.org/abs/2506.16655)) is the current reference pattern: routing criteria are written as a *declarative policy* mapping a content taxonomy (Domain–Action) to the preferred model, explicitly so that **subjective, human-ratified preferences** — not just benchmark scores — drive the route, and so that "route selection is decoupled from model assignment, allowing seamless addition of new models without retraining or architectural changes." This is exactly anima's shape: `REGISTRY` *is* the declarative policy table, Sean's spike verdicts *are* the human preference signal, and the fix is making the table able to hold them — not building a router service. Industry guides state the same consensus: route each task class to the model that can handle it, and keep "per-request records of which model was selected, why, and what the outcome was — without this, you're flying blind" ([Redis — LLM router architecture: best practices for 2026](https://redis.io/blog/llm-router-architecture-best-practices/); [Genta — LLM Routing: Pick the Right Model for Every Request](https://genta.dev/resources/llm-routing-guide)). The cheap-default-with-escalation economics anima wants (NB2 default, escalate only where it fails) is the canonical RouteLLM result — a router sending only the queries that *need* the strong model to it ([RouteLLM, LMSYS/Berkeley, via the Redis writeup](https://redis.io/blog/llm-router-architecture-best-practices/)).

2. **Niche visual styles routinely exceed a generalist image model's capability — per-style specialization is standard, and "prompt harder" is not the fix.** The image-generation literature treats one-specialist-per-style as the norm: "joint optimization of multiple styles within a single LoRA module significantly degrades generation quality," so production pipelines adopt a one-style-per-module strategy and route to style-specialized models ([arXiv 2507.11986, "Style Composition within Distinct LoRA modules"](https://arxiv.org/html/2507.11986v1); [arXiv 2402.16843, "Multi-LoRA Composition for Image Generation"](https://arxiv.org/abs/2402.16843)). This independently corroborates the spike's conclusion that NB2-fails-Primal-grit is a **model limit, not a style limit** — and anima's own research already holds the direct precedent: the SD community needed dedicated Primal LoRAs because "text prompting under-delivered" ([Civitai, cited in `registers/primal-sketch-grit/research.md` §4](https://civitai.com/models/502844/genndy-tartakovsky-style-series-for-pony)). Patch shape (b)(2) — prompt nudges — was therefore structurally incapable of fixing instance (a)(2).

3. **Silent fallback below the quality floor is the named anti-pattern; unavailable routes must fail loud.** Production-failure writeups converge on this: "silent quality degradation is the worst failure mode — your API returns 200 OK, but the output is [wrong]" ([buildmvpfast — LLM Error Handling and Fallback Strategies for Production, 2026](https://www.buildmvpfast.com/blog/building-with-unreliable-ai-error-handling-fallback-strategies-2026)); fallback chains must be *explicit policy* with quality floors, never an implicit default absorbed downstream ([Zylos Research — Graceful Degradation Patterns in AI Agent Systems, 2026](https://zylos.ai/research/2026-02-20-graceful-degradation-ai-agent-systems/)). Falling back from gpt-image to NB2 for primal would be precisely a silent drop below the quality floor — the engine already proven unable to hold the look. The field report's "fail loud … never silently fall back to NB2" is the correct call; best practice adds: that property must be *implemented and tested*, not asserted (intended-vs-implemented gap #4). Note the local echo: code-brain's own hybrid-router applies this rule (`fallback = "none"` raising `RouteUnavailable` on the Tier-C route) — the pattern is already house style.

4. **Validation gates before costed production runs.** "Development evals should become deployment gates — if a change fails quality thresholds, your pipeline should block the release automatically" ([Galileo — Best Practices for AI Model Validation](https://galileo.ai/blog/best-practices-for-ai-model-validation-in-machine-learning)). Mapped here: the edit-consistency spike before a register's first costed Bible pass is an eval gate, and best practice is to make it a *blocking, structural* gate the pipeline enforces — not a reminder in a brief (intended-vs-implemented gap #5).

No claim above rests on prior art not existing — the pattern is well-trodden, and the diagnosis below cites it inline.

---

## Step 4 — Root cause (one sentence), and the band-aids refused

**Root cause:** anima's model-routing seam is under-built for the decisions it is documented to own — `RegisterSpec.generation_model` can express only the two default Gemini engines and records neither spike verdicts nor edit-identity validation state — so every ratified per-register transport decision is forced to live as prose scattered *around* the seam while the code keeps asserting universal NB2, including the NB2-for-primal hypothesis the 2026-07-04 four-engine spike already falsified.

**Convergence check (every instance and every failed patch traces to this one point):**
- (a)(1) all seven hardcoded NB2 → the seam's only expressible vocabulary *is* the default engine pair; universal-NB2 is what an under-expressive map degenerates to.
- (a)(2) NB2 fails primal and the falsified hypothesis still ships → the verdict had no landing slot (no gpt-image constant, no runner, no status field), so it parked in prose and a backlog bullet — per Arch-Router's pattern ([arXiv 2506.16655](https://arxiv.org/abs/2506.16655)), a routing policy that can't encode the human's preference verdict isn't a policy seam yet.
- (a)(3) escalated transports' across-edit identity hold unvalidated with no gate → validation state has no representation anywhere in the seam, so the gate can only exist as prose ([Galileo](https://galileo.ai/blog/best-practices-for-ai-model-validation-in-machine-learning): eval gates belong in the pipeline, blocking).
- (b)(1) universal NB2 → the seam's degenerate expressible policy (above).
- (b)(2) prompt nudges → capability gaps worked around in the prompt layer because the model layer wasn't steerable per register; structurally incapable of fixing a model limit ([arXiv 2507.11986](https://arxiv.org/html/2507.11986v1): per-style specialization, not harder prompting).
- (b)(3) case-by-case spikes with prose verdicts → the spike is the right instrument, but its output has nowhere structural to go, so each verdict becomes one more scattered patch — including prose-vs-prose drift *between* the field report and the register docs on the same day.

**Band-aids surfaced during diagnosis, named and refused (skill Step 4.2):**
1. *"Just flip primal's `generation_model` to a gpt-image string and move on."* Band-aid: changes behavior only at the call site where the class last surfaced; `samurai-jack-s5` (gpt-image predicted, field report §3) would re-run the whole scatter pattern at its authoring; relies on a person remembering next time. The flip is *part* of the fix (it's the field report's §7 pending action) but only inside the seam-level change below.
2. *"Add a silent NB2 fallback when the escalated engine's runner is missing"* (or leave fail-loud as an untested assumption). The exact anti-pattern: a 200-OK render in a look the model provably cannot hold ([buildmvpfast](https://www.buildmvpfast.com/blog/building-with-unreliable-ai-error-handling-fallback-strategies-2026)); the field report explicitly forbids it.
3. *"Record the verdict in a comment / one more doc."* The field report's own words rule this out — "setting it is the deliverable, **not a comment**" — and §2.1 shows N prose copies already can't stay mutually consistent.
4. *"Build a router service/classifier."* Over-engineering in the other direction: the registry-as-declarative-map is already the architecturally correct shape (policy as data, decoupled from mechanism — [Arch-Router](https://arxiv.org/abs/2506.16655)); the fix is making the map expressive and authoritative, not adding indirection.

---

## Step 5 — Intent-Carrying Spec

*(For the Phase C implementer — Opus. You did not run Steps 1–4; this section carries everything you need so you don't drift back into the patch pattern. Scope: the anima repo, next build, TDD per the field report. The four elements below are the contract; the edge-case notes are load-bearing, not optional color.)*

### Real ask

Make per-register model routing real, permanently — not patch one more register. Sean's ask ("make a note about what models we use for which styles") is, by the field report's own ruling, the `RegisterSpec.generation_model` / `final_model` fields: each register rendered by the engine that can actually hold its look, the decision recorded first-class in `pipeline/registers.py` and consumed from there, and identity validated across every edit-pipeline handoff (anchor → turnarounds → expressions) before any escalated register's first **costed** Bible pass. When the next spike ratifies a verdict, it must have exactly one place to land — and landing it must be the drill's enforced final step, not a backlog bullet.

### Root cause (carry this into every judgment call)

The routing seam is under-built for the decisions it is documented to own: it can express only the two default Gemini engines and records neither spike verdicts nor edit-identity validation, so ratified transport decisions accumulate as prose around the seam while the code asserts universal NB2 — including a hypothesis the 2026-07-04 spike falsified. Grounding: declarative preference-aligned routing policy in one seam ([Arch-Router, arXiv 2506.16655](https://arxiv.org/abs/2506.16655)); per-style model specialization because generalists fail niche styles ([arXiv 2507.11986](https://arxiv.org/html/2507.11986v1)); no silent fallback below the quality floor ([buildmvpfast 2026](https://www.buildmvpfast.com/blog/building-with-unreliable-ai-error-handling-fallback-strategies-2026)); evals as blocking deployment gates ([Galileo](https://galileo.ai/blog/best-practices-for-ai-model-validation-in-machine-learning)). Every edge case you hit, resolve toward: **the registry is the single system of record for transport; prose references it; unavailable routes fail loud; unvalidated escalations cannot start costed work.**

### The change (four parts — all one build; TDD: write the failing test first for each)

**1. Make the seam able to express any ratified engine.**
Add an engine-id constant for gpt-image (ChatGPT Image 2) beside `NB2_FLASH` / `NB_PRO` in `pipeline/registers.py`, with a comment naming its status (generates the gritty registers NB2 cannot; across-edit identity hold unproven). Rule going forward: every `generation_model` / `final_model` value in the registry must be one of this module's named constants — the "which model for which style" map stays readable in one file. Do not add engines nobody has ratified; the constant set grows one spike verdict at a time.

**2. Land the ratified primal verdict (the field report §7 pending action, done properly).**
In one commit: `primal-sketch-grit.generation_model` → the gpt-image constant; rewrite the spec's stale comment block (it still calls NB2 "the §3c transport HYPOTHESIS — the go/no-go spike judges it") to record the verdict: 2026-07-04 four-engine spike, NB2 cannot render or edit into the grit (model limit, not style limit), gpt-image best by far, across-edit identity hold **pending** validation; update `tests/test_primal_sketch_grit.py` to pin the new value; update `registers/primal-sketch-grit/research.md` §1 row + §4 transport line and its header's "PENDING SPIKE" status to *reference* the registry as the record. The other six registers stay `NB2_FLASH` — that is their ratified-by-use truth, not an oversight.

**3. Make fail-loud structural, not assumed.**
The field report asserts "a gpt-image id with no wired runner will fail loud at generation (correct — never silently fall back to NB2)." Today that is an untested assumption about code outside this diagnosis's pinned view. Find the engine-id → runner resolution point (start at `character_designer._resolve_plate_model`) and make the property true by construction: an engine id with no wired runner raises a dedicated, loud error (mirror `UnknownRegisterError`'s shape and message quality — name the register, the engine id, and where wiring/validation status lives), and **prove by test** that generating a `primal-sketch-grit` plate today raises rather than rendering via NB2. A silent NB2 render of primal is the single worst outcome this change exists to prevent — it is a 200-OK frame in a look the model provably cannot hold. Do **not** wire an actual gpt-image runner in this build; that is explicitly deferred, gated on the GRANDMASTER build (field report §7).

**4. Give the transport decision and its validation state a first-class record, and gate costed work on it.**
Add a minimal transport-status record to `RegisterSpec` — the smallest honest shape, e.g. a `transport_status` field (or equivalently structured field the tests can read) distinguishing three states with date + evidence path: `default-ratified-by-use` (the NB2 six; grossout's future authoring lands here too, per its NB2 GO), `spike-ratified-edit-identity-pending` (primal today — evidence: `refs/spike-2026-07-04/`, field report §1), `edit-identity-validated` (nothing yet). Then two consumers:
   - a **completeness test** (mirror `tests/test_register_registry.py`'s pattern): every register has a coherent record; any register whose `generation_model` is not the NB2 default without a transport-status record fails the suite;
   - the **costed Bible-pass entry point** (locate where multi-plate paid generation begins) refuses to start on a register whose transport is escalated but not `edit-identity-validated`, with an error that names the missing step (the small edit-consistency spike, per `briefs/2026-07-02-grandmaster/go-no-go.md`). The gate is a no-op for default-NB2 registers — NB2's across-edit hold is *why* it is the default (Flo-B), and the grossout spike re-confirmed it through a real edit.
   This moves the "real GRANDMASTER production gate" from prose into the pipeline, per eval-gate best practice. It must **not** block authoring or un-costed spikes — primal ships in the pending state; only costed Bible work is gated.

**Doctrine stitch (small, same build):** the authoring drill's transport step ends with the verdict landing in the `RegisterSpec` *in the same commit as ratification* — add that line where the field report §1 says the rule gets baked ("the extension pattern + doctrine"), and have the field report's roster table (§6) point at the registry as its source rather than restating transport values.

**What "done" looks like:** grep finds no transport verdict that exists only in prose; `pipeline/registers.py` alone answers "which model renders register X, and has that route been validated for edits?" for all seven registers; a costed Bible pass on an unvalidated escalated transport is structurally impossible; generating primal today fails loud with a message that says why; the full suite passes, including the untouched byte-identical characterization oracle for the six legacy registers.

**What would still count as a band-aid (reject these in review):** flipping primal's field without the status record or the fail-loud test (the next escalated register re-scatters); any code path that quietly substitutes NB2 when an escalated engine is unavailable; recording status in a comment or doc instead of a field tests can read; a gate implemented as a doc reminder; wiring a half-tested gpt-image runner "while you're in there."

**Edge cases the spec anticipates:**
- *Dataclass change vs. the frozen oracle:* add the new field with a default so the six legacy specs need no edits; `tests/test_register_characterization.py` byte-pins the **existing** field values for locked Bibles — those must not shift by one byte. If the oracle asserts whole-spec equality rather than per-field, extend the oracle deliberately in its own commit with a note, never weaken it.
- *Insertion order:* REGISTRY's ordering is load-bearing (stub-keyword precedence, oracle-pinned). Adding constants or fields must not reorder entries.
- *`reference_images` backfill:* both refs folders now hold Sean-ratified evidence while every spec's tuple is `()`. Populating it is Sean's call per file (which images are confirmed exemplars) — surface the question at the next authoring session; do not auto-populate from folder listings.
- *`90s-nicktoon-grossout`:* its NB2 GO verdict and draft spec are recorded in its research.md for the authoring session. Authoring it is **Sean-gated** — do not author it as part of this fix. When authored, its transport lands as `default-ratified-by-use` with the 2026-07-04 spike as evidence, and its remaining question (NB2 identity hold across a *full* Bible, not just the one gross-up edit) rides the same gate machinery from part 4.
- *`final_model`:* the NB_PRO painterly-final seam is documented and consumer-less. It participates in the constants rule and the status record like any route, but build no consumer for it.

### What NOT to change (Steps 1–4 confirmed these are correct — do not "fix" them)

- **The closed-vocabulary semantics:** `UnknownRegisterError` loud on nonempty-unknown; the caller-owned `get_register(value or DEFAULT_REGISTER)` back-compat rule; `DEFAULT_REGISTER` itself. These are the register-*name* analogue of the failure semantics you are adding at the engine level — the model to copy, not a thing to refactor.
- **REGISTRY insertion order** and the stub-keyword precedence it carries (oracle-pinned).
- **Every taste field on all seven registers** — `identity_lock`, `preserve`, `style_token`, `markers`, `summary`, `stub_keywords`. Sean-ratified content; the legacy six are byte-pinned. This fix routes registers to engines; it does not touch what the registers *say*.
- **The per-register spike doctrine itself** — cheap cross-engine spike + Sean's eye is the correct decision instrument (it both caught primal's escalation and *prevented* a needless one for grossout). The fix changes where verdicts land, not how they're made. The pre-agreed escalation ladder and "never a new transport mid-Bible-pass" stand.
- **The six legacy registers' `generation_model=NB2_FLASH`** — ratified by use; and grossout's candidate status (unauthored until Sean greenlights).
- **The refs conventions and the non-derivative rule** — no third-party frames in `refs/`, genericized attribute-only production prompts, the style-not-person rule for `90s-nicktoon-grossout`. Untouched by this change.
- **No register-family metadata, no renames, no router service** — the ≥2-Tartakovsky family question is explicitly held until `samurai-jack-s5` is greenlit (field report §5), and the registry-as-declarative-map architecture is right as-is.
- **anima was read-only for this diagnosis** — every change above is for the Phase C build, on its own branch, TDD.

---

## Harness self-check (skill success criteria)

- Grounding (a)–(c): pre-pinned per the run prompt; restated in Step 1 before any subsystem reading. ✓
- Whole-subsystem map — state / control flow / orchestration, not just the failing file: Step 2.1–2.3. ✓
- `intended-vs-implemented` run with gaps named explicitly (6 gaps + confirmed-correct list): Step 2.4. ✓
- Best practice web-searched (4 real searches, 2026-07-05) and cited inline in the diagnosis, not as a tacked-on bibliography: Steps 3–5. ✓
- Single-sentence system-level root cause; symptoms and failed patches shown converging on it: Step 4. ✓
- Patch-shaped fixes explicitly flagged as band-aids and refused (4): Step 4. ✓
- Output is an intent-carrying spec (real ask / root cause / change / what NOT to change) sized for a lesser model to implement without drift — contained fix, so the four-element floor plus edge cases and done-criteria, rather than the full 9-section template: Step 5. ✓
