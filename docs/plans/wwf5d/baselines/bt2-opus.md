# BT2 — Opus baseline
- Task: zoom-out-and-think on anima register-transport / per-register model-routing seam (chain of custody: docs/plans/wwf5d/task-battery.md § BT2)
- Model: Claude Opus 4.8 (fresh subagent, no prior session context)
- Date: 2026-07-04
- Inputs used: .claude/skills/zoom-out-and-think/SKILL.md @ 93e5725; anima @ aa2007c — the four pinned paths only; grounding answers pinned in task-battery.md § BT2 (restated below)
- Research: live web search performed (citations inline)

---

## Step 1: Grounding (hard gate) — pinned answers, restated for confirmation

Per the run prompt, zoom-out-and-think's Step-1 hard gate is satisfied by the
pre-pinned answers in `docs/plans/wwf5d/task-battery.md` § "BT2 — Pinned
grounding answers." I restate my understanding of each below and proceed
directly to Step 2 without asking the user. I did **not** re-derive these; I am
confirming I read them as intended before mapping anything.

**(a) What keeps recurring — my understanding.** The *transport* decision for a
register (which generative model actually renders and edits that register's
look) is made one register at a time, by an ad-hoc look-spike, instead of
through a single routing seam. Concretely: `pipeline/registers.py` hardcodes
`generation_model=NB2_FLASH` for **all seven** registers. That universal NB2
default cannot render `primal-sketch-grit`'s Tartakovsky-*Primal* grit and
specifically cannot *edit* a frame into it — a four-engine test established this
is a **model limit, not a style/prompt limit** (gpt-image was best; NB Pro and
NB2 both fell short). And for any register that escalates *away* from NB2 (e.g.
to gpt-image), that model's ability to hold character identity across the
edit-pipeline handoffs (anchor → turnarounds → expressions) is **unvalidated** —
a real open risk the field report flags, not yet a confirmed failure. The
recurrence is the *pattern*, not a single crash: every new register re-opens the
same "what model, decided how" question from zero.

**(b) What's been tried — my understanding.** Three things, all still leaving
the pattern in place: (1) **universal NB2 as the hardcoded default** for every
register (confirmed live in `registers.py`); (2) **per-register prompt nudges** —
e.g. `90s-nicktoon-grossout`'s gross-up-ratio correction after Sean rejected the
first draft's constantly-grotesque output, a prompt-layer fix; (3) **per-register
look-spikes ratified case-by-case** — the `primal-sketch-grit` go/no-go spike and
the `90s-nicktoon-grossout` cross-engine spike, each judged by Sean's eye, each a
separate event (field report §1, §4, §6).

**(c) What "coherent/correct" looks like end-to-end — my understanding.**
Per-register model routing where **each register is rendered by the model that
can actually hold its look**, with `RegisterSpec.generation_model` /
`final_model` populated as a **first-class architectural decision** ("the
deliverable, not a comment," per the field report) rather than a default nobody
revisits — **and** identity validated across every edit-pipeline handoff *before*
a register's first costed Bible pass, so the whole routing decision lives in one
place (`pipeline/registers.py` and the seam that reads it) instead of scattered
per-register patches and stale docs.

Confirmed. Proceeding to Step 2.

---

## Step 2: Read the Whole System (the zoom-out)

Scope note (honesty): I read exactly the four pinned anima paths at `aa2007c` —
`docs/active/2026-07-04-register-backlog-and-transport-findings.md` (the field
report), `registers/primal-sketch-grit/` (research.md + refs/README), 
`registers/90s-nicktoon-grossout/` (research.md + refs/README), and
`pipeline/registers.py`. Where the mapping below references a file I did **not**
open (e.g. `character_designer._resolve_plate_model`, `test_primal_sketch_grit.py`,
`briefs/2026-07-02-grandmaster/go-no-go.md`, the Cy context prompt), I mark it
**[referenced, not read]** and scope my claim to what the four files state about
it. This matters for the spec: the routing *data* lives in `registers.py`, but
the routing *dispatch* lives in `character_designer`, which the implementing
model must open before editing anything.

### 2.1 State — where the routing state lives and who owns it

- **The registry is the single home of the data.** `pipeline/registers.py`
  declares itself "the canonical home of anima's closed style_register
  vocabulary … every register touch-point reads from here instead of carrying
  its own copy" (module docstring, lines 1–8). The state is a module-level
  `REGISTRY: dict[str, RegisterSpec]` of **seven** frozen specs
  (`pencil-test-colored`, `pixel-art-8bit`, `watercolor`, `line-art-only`,
  `photoreal`, `3d-rendered`, `primal-sketch-grit`).
- **Each spec carries the transport as data.** `RegisterSpec` has
  `generation_model: str` and `final_model: str` fields (lines 88–89), explicitly
  documented as the former `_REGISTER_MODELS[name]["generation"/"final"]` tables.
  So the *mechanism* to hold a per-register model already exists and is
  single-owned — good.
- **The model vocabulary is tiny and NB2-centric.** Only two model-id constants
  exist: `NB2_FLASH = "gemini-3.1-flash-image-preview"` and
  `NB_PRO = "gemini-3-pro-image-preview"` (lines 48–49). **There is no gpt-image
  constant and no gpt-image runner anywhere in this file** — the model the field
  report says `primal-sketch-grit` needs does not exist as a routable value yet.
- **Two different "defaults" are in play and must not be conflated.**
  `DEFAULT_REGISTER = "pencil-test-colored"` (line 54) is a *register* back-compat
  default (empty/missing `style_register` → pencil-test). That is a separate axis
  from the *model* default (NB2 for every register). The register-default axis is
  correct and well-guarded (see 2.2); the model-default axis is the problem.
- **Actual generation-model values, as built:** `generation_model=NB2_FLASH` for
  **all seven** registers (lines 124, 151, 174, 197, 215, 236, **282**).
  `final_model` splits `NB2_FLASH` (pencil, pixel, line-art) vs `NB_PRO`
  (watercolor, photoreal, 3d, primal) — the "painterly-final seam with no
  consumer yet" (docstring lines 44–47). The load-bearing line is **282**:
  `primal-sketch-grit.generation_model = NB2_FLASH`, the exact model the field
  report says cannot render it.

### 2.2 Control flow — the real lifecycle of a routing decision

1. A caller resolves a register: `get_register(value or DEFAULT_REGISTER)`
   (lines 300–309). A **nonempty, unknown** register raises `UnknownRegisterError`
   loud (lines 57–73); an **empty** one falls back to pencil-test. This is the
   registry's one enforced invariant, and it is a *good* one: unknown register →
   fail loud, never silent coercion.
2. The resolved `RegisterSpec.generation_model` is then read by
   `character_designer._resolve_plate_model` / `_build_plate_prompt`
   **[referenced, not read; docstring lines 5–8]** — that is where the model is
   actually dispatched to a runner. `registers.py` itself is pure data + lookup;
   it performs no routing, no capability check, no fallback.
3. `final_model` rides a "documented seam with no consumer yet" (docstring lines
   44–47) — declared, not exercised.

The critical observation: **the control flow enforces exactly one thing about a
register — that its *name* is known.** It enforces **nothing** about its *model*:
not that the model is wired, not that the model can render the register, not that
the model was validated across the edit pipeline. A register can name any model
string (or, today, silently inherit NB2) and the flow is happy.

### 2.3 Orchestration — who actually *decides* the model (this is where it clusters)

The skill's orchestration lens (Step 2.3: "recurring bugs cluster exactly where
'who decides this' is unclear or split across two places") lands directly on the
seam:

- **The registry's data says it decides.** Field report §1: "`RegisterSpec.generation_model`
  / `final_model` … **is** the 'which model for which style' map. Setting it is
  the deliverable, not a comment."
- **But the real decision is made outside the code and only sometimes transcribed
  back in.** The model for a register is chosen by a **per-register look-spike +
  Sean's eye** (field report §1 "transport is per-register, decided by a cheap
  spike"; §4; primal `go-no-go.md` **[referenced, not read]**; the 90s-nicktoon
  cross-engine spike). The spike produces a verdict; a human is then supposed to
  hand-edit `generation_model` to match. Nothing binds the two.
- **So "who decides the model" is split three ways with no owner of the whole:**
  the *spike* decides, the *field* is supposed to record, the *dispatcher*
  executes — and no component checks that the recorded value equals the ratified
  verdict, that the model is runnable, or that it survives the edit pipeline. The
  default-to-NB2 masks the gap: because an un-transcribed decision *still yields
  NB2*, "nobody routed this register" and "this register is routed to NB2" are
  the **same observable state**. You cannot tell a deliberate NB2 from an
  unrevisited one.

### 2.4 Intended-vs-implemented comparison

Running the `intended-vs-implemented` move — field report (documented intent) vs.
`pipeline/registers.py` (live behavior):

| # | Documented intent (field report / research.md) | Implemented reality (`pipeline/registers.py` @ `aa2007c`) | Gap |
|---|---|---|---|
| 1 | "**NB2 is not the universal generation engine**" (§1 title). Transport is per-register, escalated when the model can't hold the look. | Module docstring lines 44–47 still assert "**NB2 is the generation/editing default for every register**"; every spec sets `generation_model=NB2_FLASH`. | The code's own doctrine comment still states the premise the field report **retired**. |
| 2 | `primal-sketch-grit` is "**transport-escalated → gpt-image (NB2 no)**" (§6 roster); NB2 "cannot render … and specifically cannot **edit** a frame into it" (§1). | Line **282**: `primal-sketch-grit.generation_model = NB2_FLASH`. | The one register proven to need escalation is coded to the one model proven to fail it. |
| 3 | "`RegisterSpec.generation_model` … **is** the 'which model for which style' map. Setting it is the deliverable, not a comment." (§1) | The field exists but holds a uniform default (NB2 ×7). No per-style *decision* is expressed; a default is. | The field is a *mechanism* with no *policy* driving it — a map with every road pointing the same way. |
| 4 | Pending code change (§1, §7): set `primal-sketch-grit.generation_model` → gpt-image id + update `test_primal_sketch_grit.py` + `research.md` §4; "a gpt-image id with no wired runner will **fail loud** at generation (correct — **never silently fall back to NB2**)." | Not applied. No gpt-image id, no fail-loud-on-unwired path; a missing/unrouted model degrades to NB2 by default, the exact silent fallback the intent forbids. | Intent explicitly wants loud failure on an unwired model; implementation gives the opposite (silent NB2). |
| 5 | `primal-sketch-grit/research.md` header: "transport verdict **PENDING SPIKE**"; §1 table "`generation_model` = NB2 — **hypothesis**." Field report §1 says the spike **resolved** to gpt-image. | research.md still records NB2-as-hypothesis; §7 lists "research.md §4 update" as pending. | The register's own research doc is **stale** relative to the ratified verdict — the doc-vs-doc gap that hides the decision. |
| 6 | Any gpt-image register "needs a **small edit-consistency spike before its first costed Bible pass** — this is the real GRANDMASTER production gate" (§1); (c) wants "identity validated across every edit-pipeline handoff before a register's first costed Bible pass." | No such gate exists in code: `RegisterSpec` has no validation-status field; the dispatcher **[referenced, not read]** has no across-edit check; nothing blocks a costed Bible pass on an unvalidated escalated model. | The validation gate is a *remembered human step*, not a structural one. |
| 7 (control) | `90s-nicktoon-grossout`: "**NB2 GO** … stays on the pipeline default" (research.md §4); correctly a **candidate**, not authored. | Correctly **absent** from `REGISTRY`; when authored it would take NB2. | *No gap* — and this is the tell: the default is genuinely correct for the pencil/flat family **and** for 90s-nicktoon, which is exactly why a *blanket* default is wrong: it is right often enough that the one place it's wrong (primal) rots unnoticed. |

**Summary of the zoom-out:** the *data model* is healthy (single-owned registry,
loud on unknown *register*). The *routing policy* is absent (no loud on unwired
*model*, no capability match, no across-edit gate), and the transport *decision*
lives in a per-register spike whose verdict is hand-carried into a passive
default that already reads NB2 whether or not anyone decided. The recurrence is
structural, not incidental.

---

## Step 3: Current best practice (live web search, cited inline)

**Precise domain/pattern:** per-content-type (capability-based) routing of
generation requests across multiple generative models, with a cheap default and
**explicit, non-silent** escalation/fallback. Anima's case is the *capability-match*
variant of model routing (does model X render style Y **at all**), which is a
stricter cousin of the more-documented *difficulty/cost* routing (route hard
queries to a stronger model to save money). I searched both and note where the
literature transfers exactly and where anima is stricter.

1. **Route by required capability, not a single universal model — a router must
   reason about each model's capabilities.** The peer-reviewed **RouteLLM** work
   (LMSYS Org) frames the core tradeoff exactly as anima's: "routing all queries
   to the largest, most capable model … can be expensive, while routing … to
   smaller models can save costs but may result in lower-quality responses," and
   prescribes that "all queries that can be handled by weaker models should be
   routed to these models, with all other queries routed to stronger models." Its
   load-bearing point for this diagnosis: "the routing system has to infer both
   the characteristics of an incoming query **and different models' capabilities**
   when routing" — i.e. the model choice is a *decision that reasons about model
   capability*, not a static default. (RouteLLM achieved "cost reductions of over
   85% … while still achieving 95% of GPT-4's performance," establishing the
   cheap-default/escalate-on-need shape as sound.)
   — <https://www.lmsys.org/blog/2024-07-01-routellm/>
2. **A single default model is an explicit anti-pattern; centralize the per-route
   model assignment in one place.** Karl Weinmeister's "A Developer's Guide to
   Model Routing" (Google Cloud Community): "Use a top-tier model for everything,
   and you pay a premium … Use a smaller model for everything, and you sacrifice
   quality on complex queries … why are we still forcing ourselves to choose just
   one?" It maps *task types* to *specific models* and — directly on anima's
   intent — keeps "**all routing logic, including … the specific LLM assigned to
   each route** … defined in a single `router.yaml` file," so routing lives in one
   maintainable place rather than scattered through application code. This is
   precisely the field report's "`RegisterSpec.generation_model` **is** the map"
   intent — anima has the single-file map, but has not made it an actual
   per-route *assignment* (every route still says NB2).
   — <https://medium.com/google-cloud/a-developers-guide-to-model-routing-1f21ecc34d60>
3. **Fallback/escalation must be explicit and ordered — never a silent
   substitution.** The official **LiteLLM Router** docs treat fallbacks as an
   explicitly-configured, ordered chain (per-deployment `fallbacks` to keep
   control explicit; ordered lists like `["gpt-3.5-turbo","gpt-4","gpt-4-32k"]`),
   and the design principle is to "**prefer compatible models to avoid silent
   behavior shifts**" — stripping unsupported params so a model switch does not
   "fail silently." The transferable rule: an unavailable/unrouted target should
   surface as an explicit, ordered decision, not a quiet degrade to whatever the
   default is. Anima's field report reaches the identical conclusion
   independently ("a gpt-image id with no wired runner will **fail loud** …
   **never silently fall back to NB2**"), which is strong corroboration that the
   fix direction is the domain-standard one.
   — <https://docs.litellm.ai/docs/routing>

**How the research grounds the diagnosis (not a bibliography):** best practice
says the model choice is a *capability-reasoned decision*, centralized in one
route-map, with *explicit, never-silent* fallback. Anima has the centralized map
(good — RouteLLM/Google Cloud both endorse the single-file route table) but has
implemented it as a *uniform default*, not a per-capability *assignment*, and its
"fallback" is the silent NB2 degrade that LiteLLM names as the thing to avoid.
The one place anima is *stricter* than the cost-routing literature: NB2 cannot
render primal grit at **any** cost or difficulty — this is a hard capability
gate, so anima additionally needs a *validation* precondition (across-edit
identity) before a model is allowed to serve a register's costed Bible pass,
which the generic cost-routing sources don't cover but which follows the same
"reason about the model's proven capability before routing to it" logic.

---

## Step 4: Root cause (one sentence)

**anima has no routing seam that *owns* per-register transport as a validated,
enforced decision — `RegisterSpec.generation_model` is a passive default (NB2 for
all seven registers) that the real decision (a per-register look-spike + Sean's
eye) is hand-transcribed *into* rather than *driven by*, with no capability
match, no fail-loud on an unwired/unvalidated model, and no across-edit-identity
gate, so "nobody routed this register" and "this register routes to NB2" are the
same state, every register's transport is re-litigated ad hoc, and a ratified
escalation like `primal-sketch-grit`'s still reads NB2 in code.**

### Why this is the root cause and not a symptom (traceability)

- It explains **every recurring instance in 1(a):** transport decided per-register
  by spike (because the decision has no enforced home), NB2 hardcoded ×7 (the
  passive default), NB2 failing primal (a default can't match a capability it
  lacks), and the escalation-model's across-edit hold being unvalidated (no gate
  exists to require validation).
- It explains **why every patch in 1(b) didn't hold:**
  - *Universal NB2 default* couldn't hold because a single default is a known
    anti-pattern across genuinely different content-type capability needs
    (RouteLLM / Google Cloud: one model forces a compromise; NB2's compromise is
    that it can't render grit at all).
  - *Per-register prompt nudges* couldn't hold for primal because it is a **model**
    limit, not a **prompt/style** limit (field report §1's four-engine finding) —
    the nudge operates one layer below the router, so it cannot fix a wrong-model
    problem no matter how good the prompt.
  - *Per-register look-spikes* couldn't hold **structurally** because the verdict
    they produce has no enforced destination: it is hand-copied (or, for primal,
    not yet copied) into a passive default with no fail-loud and no across-edit
    gate, so the verdict rots in a doc while the code keeps saying NB2 and the
    next register starts the whole ad-hoc dance again.

### Band-aid check (skill Step 4.2 red flags) — the obvious fix is a partial one

The fix already on the table (field report §1 / §7 pending action #1): *"set
`primal-sketch-grit.generation_model` → gpt-image id + update the test +
`research.md` §4."* Checked against the red flags, **doing only that is a
band-aid**, and I am naming it as one:

- ✅ *changes behavior only at the exact call site that last surfaced* — it fixes
  primal alone.
- ✅ *would need to be repeated at every other call site sharing the pattern* —
  `90s-nicktoon-grossout`, `samurai-jack-s5`, `warm-storybook-pencil`, and the
  roster remainder each re-run the same spike-then-hand-edit cycle.
- ✅ *requires a person to remember to do it again next time* — someone must
  remember to transcribe each future spike verdict, wire each escalated runner,
  and run each across-edit gate, forever.

The value-change is **necessary** (primal is genuinely mis-routed today and must
be corrected), but it is the *instance* fix. The *class* fix is the routing-policy
layer that makes the instance fix structural instead of remembered. The spec
below requires both, and tells the implementer exactly why the value-only version
would leave the recurrence intact.

---

## Step 5: Intent-Carrying Spec (for the implementing model — Opus, Phase C)

> Framing for the implementer: you did not run Steps 1–4. Read this whole spec,
> then read the seam it points at, before editing. The tempting one-line fix
> (change primal's model string) is real work but is **half** the task — the
> other half is the reason the string was wrong in the first place. anima is
> **read-only for the diagnosis run that produced this**; Phase C implementation
> happens under its own separate authorization — this artifact does not grant it.

### Real ask

Make **per-register generative-model transport a first-class, validated,
enforced decision that lives in one seam** — so each register is rendered by a
model proven to hold its look, an unwired/unvalidated model **fails loud** (never
a silent NB2 degrade), and a register on an escalated model **cannot enter a
costed Bible pass** until its identity is validated across the edit pipeline. The
immediate concrete want inside that: `primal-sketch-grit` must route to gpt-image
(NB2 is proven unable to render or edit its grit), and the next register must not
require re-inventing any of this. (Restated from grounding (a)/(b)/(c); not
invented.)

### Root cause (carry this — it is why the change is shaped the way it is)

`RegisterSpec.generation_model` is a **passive default (NB2 ×7)**, not an owned
decision: the real transport choice is made by a per-register spike and
hand-copied into the field, with nothing enforcing capability match, model
wiring, or across-edit validation — so an unrouted register is indistinguishable
from an NB2 one, and a ratified escalation (primal → gpt-image) still reads NB2.
Grounded in the domain standard for model routing: route by **reasoned model
capability**, not a single default (RouteLLM,
<https://www.lmsys.org/blog/2024-07-01-routellm/>); keep the per-route model
assignment centralized in one map (Google Cloud "A Developer's Guide to Model
Routing", <https://medium.com/google-cloud/a-developers-guide-to-model-routing-1f21ecc34d60>);
and make escalation/fallback **explicit and never silent** (LiteLLM Router,
<https://docs.litellm.ai/docs/routing>). anima independently reached the
"fail loud, never silently fall back to NB2" conclusion (field report §1) — the
fix is to make the code obey the intent the field report already states.

### The change (at the level that removes the whole class)

Do all four. #1 is the instance; #2–#4 are the class fix that makes #1 stick.
The routing **data** lives in `pipeline/registers.py`; the routing **dispatch**
lives in `character_designer._resolve_plate_model` (referenced by registers.py's
docstring but **not read during diagnosis**) — **open and read that seam and
`test_primal_sketch_grit.py` and `briefs/2026-07-02-grandmaster/go-no-go.md`
first**, because the fail-loud and gate belong at dispatch, not bolted onto the
pure data registry.

1. **Correct the instance (the field report's pending action #1), TDD.** Set
   `primal-sketch-grit.generation_model` to the gpt-image model id and update
   `test_primal_sketch_grit.py` and `registers/primal-sketch-grit/research.md`
   §4 (which still records "NB2 — hypothesis / PENDING SPIKE") to the resolved
   gpt-image verdict. The exact gpt-image id + its runner wiring is a real
   dependency the field report defers (§7 "gpt-image transport wiring … gated on
   GRANDMASTER build") — **do not fabricate an id**; source it, and if the runner
   is not yet wired, that is fine *only because* #2 makes it fail loud.
2. **Make transport a validated decision, fail-loud on unwired — mirror the
   existing `UnknownRegisterError` philosophy.** The registry already fails loud
   on an unknown *register*; extend the same discipline to the *model*: a
   register's `generation_model` must be one of a **known, wired** set, and an
   unwired/unknown model must raise loud **at routing/dispatch time** (an
   `UnknownGenerationModelError` sibling, or equivalent at
   `_resolve_plate_model`), never degrade to NB2. This is the field report's
   "fail loud … never silently fall back to NB2" made structural, and LiteLLM's
   "no silent behavior shift" principle applied.
3. **Make "escalated" explicit so it is not confusable with "unrevisited
   default."** Today NB2 means both "chosen" and "never chosen." Add a way for a
   spec to mark its transport as a *ratified decision* vs an *inherited default*
   (e.g. an explicit `transport_rationale` / `transport_validated` field, or by
   requiring `generation_model` to be set explicitly per register rather than
   defaulting) so that "nobody decided" becomes a **detectable** state, not a
   silent NB2. Keep NB2 as the correct value for the pencil/flat family and the
   confirmed `90s-nicktoon-grossout` — the point is that it is *chosen*, not
   *defaulted into*.
4. **Gate the costed Bible pass on across-edit identity validation for escalated
   models.** A register whose `generation_model` is a non-default (escalated)
   engine must not proceed to its first *costed* Bible pass until an
   across-edit-identity spike (anchor → turnarounds → expressions) has validated
   that engine — the field report's "real GRANDMASTER production gate." Encode
   this as a structural precondition (a check the pipeline enforces), not a
   comment or checklist a human must remember.

**What "done" looks like:** adding the next register is "author the spec, run one
spike, record the ratified model in one place"; a register pointing at an unwired
or unvalidated model **stops the pipeline loudly**; `primal-sketch-grit` routes to
gpt-image with its research doc and test in agreement; and no register can reach a
costed Bible pass on an unvalidated escalated model. If, at any edge case the spec
didn't spell out, you're deciding between "silently pick a working model" and
"stop and surface the decision" — **always surface it** (that is the entire root
cause).

**What still counts as a band-aid (reject these):** changing only primal's
string and stopping; a one-off `if register == "primal-sketch-grit"` special-case
in the dispatcher; any silent try-gpt-image-then-NB2 fallback (explicitly
forbidden by both the field report and LiteLLM's no-silent-shift rule); leaving
the across-edit gate as a doc/checklist rather than an enforced precondition; or
"fixing" the module docstring's stale "NB2 is the default for every register"
line without making the code actually route per-capability (the comment is a
symptom, not the bug).

### What NOT to change (Steps 1–4 confirmed these are already correct)

- **The closed-vocabulary design and `UnknownRegisterError`** (fail-loud on an
  unknown *register* name) — correct, orthogonal, and the model of the philosophy
  #2 extends. Do not loosen it.
- **`DEFAULT_REGISTER` / the empty→`pencil-test-colored` back-compat rule** — this
  is *register* defaulting, a different axis from *model* routing. Correct as-is;
  do not entangle the two.
- **NB2 as the generation model for the pencil/flat family** (`pencil-test-colored`,
  `pixel-art-8bit`, `line-art-only`) **and for the confirmed `90s-nicktoon-grossout`**
  (research.md §4 "NB2 GO") — do not escalate these; the fix is to make NB2 a
  *recorded choice*, not to change the value.
- **The `final_model` = NB Pro "painterly-final seam with no consumer yet"** — a
  documented, unexercised seam. Do not wire a consumer as part of this change.
- **`90s-nicktoon-grossout` staying a candidate (not authored into the registry)**
  — correct and Sean-gated. Do not author it as part of this fix.
- **The deliberate prompt-authoring choice** of *not* placing negative-control
  vocabulary in `preserve` (both research docs, §1) — orthogonal to routing;
  leave it.
- **The genericization / non-derivative rules and all register *taste* content**
  (Cy blocks, research.md analysis, refs/) — this is a routing-seam fix, not a
  taste fix. Do not touch the look definitions.

---

## Success-criteria self-check (zoom-out-and-think § Success Criteria)

- [x] All three grounding questions (a)–(c) were confirmed (pinned, restated)
      before any system-mapping.
- [x] Whole-subsystem state / control flow / orchestration mapped — not just the
      one line (registers.py:282) where the mis-route lives.
- [x] `intended-vs-implemented` run explicitly (§2.4 table): documented intent vs.
      live behavior, gaps named per row.
- [x] Current best practice web-searched and cited **by source inline** in the
      diagnosis (RouteLLM / Google Cloud model-routing guide / LiteLLM Router).
- [x] Single system-level root cause in one sentence (Step 4), traced to explain
      every 1(a) instance and every 1(b) failed patch.
- [x] The patch-shaped fix that surfaced (set primal's string only) was explicitly
      flagged as a band-aid and the level above it specified.
- [x] Output is an intent-carrying spec (real ask + root cause + change + what NOT
      to change), sufficient for a lesser model to implement without drift.
