# Tier-1 Improvement Spec (DRAFT): `writing-voice-modes`

## What this file is

An **Opus first-pass draft spec** produced by running the repo's `skill-audit`
harness against `.claude/skills/writing-voice-modes/SKILL.md`. It is **not** a
finished spec and **no skill file was edited** to produce it. In Phase B, **Fable
5 elevates this draft** into the change it actually applies — a strong draft means
Fable spends its cycles on the last 20% of quality (precision, wording, edge
cases), not on re-discovering the inventory of what to fix.

It contains the two `skill-audit` artifacts: a **severity-tagged seam report** and
an **intent-carrying improvement spec**. Where I am uncertain whether a fix is
right, I name the **open question** rather than assert false confidence.

## Grounding answers used (controller-supplied, as Sean's (a)–(d))

- **(a) For:** voice/tone control calibrated to Sean's real voice (Sean Mode 90% +
  four author techniques 10%); stage 3 of the Substack chain; every public word
  rides it.
- **(b) Feeds:** `writing-critique` (verdicts judged against voice),
  `writing-humanity-pass` (scrub must preserve voice choices); published Substack +
  portfolio.
- **(c) Disappoints:** mode-selection and enforcement scaffolding is loose — drafts
  drift toward generic-AI register mid-piece; the 90/10 split is stated but
  unenforced/unmeasured; downstream stages get no explicit record of which voice
  decisions were made (so critique/humanity-pass can't protect them).
- **(d) Wow:** enforcement so tight a reader can't tell an agent draft from Sean's
  hand, with drift caught in-line and voice decisions traveling as a named
  artifact.

## SCOPE CONSTRAINT (campaign-locked — read before implementing)

**Audit and improve the ELICITATION / ENFORCEMENT / RECORDING / MEASUREMENT
SCAFFOLDING ONLY** — i.e., *how a voice gets chosen, recorded, enforced, and
measured*. This spec must **NEVER** audit, critique, "improve," rewrite, extend,
re-weight, or otherwise touch:

- the voice **samples**, the **register** itself, or Sean's **taste**;
- the mode descriptions' *content*, the signature-move *definitions*, the
  anti-pattern *diagnoses*, the reference-universe, or the 90/10 *ratio*;
- anything in the private `references/` or `drafts/` directories.

**A model "improving" Sean's voice is the exact flattening this chain exists to
prevent.** Every fix below is a change to *plumbing* (selection prompts, a
decision-record artifact, an in-line self-check gate), and each is written so a
weaker implementing model can see the wall: *you are wiring how the voice is
carried and checked, not editing the voice.* If any proposed change starts to read
like a taste judgment about a sample or a rule, that is the signal to stop — it has
crossed the wall.

**Note on evidence:** This audit was performed from the **public `SKILL.md` only**.
`references/` and `drafts/` were not read. Line numbers below refer to
`SKILL.md` as of the audit (2026-07-04).

---

## Artifact 1 — Seam Report

Findings are tagged `dangerously-wrong` / `structural` / `minor`. Every finding
names where in the skill, what the seam/gap is, and what Sean would concretely
observe when it bites. All findings are scoped to scaffolding.

- `structural` — **Voice decisions never travel forward as a record (the core
  seam).** The skill composes prose and hands *only the prose* down the chain
  (Related Skills, lines 286–296). It never emits which **mode** was chosen, at
  what **Professional Dial %** (lines 188–198), or which **signature moves** (lines
  157–181) were deliberately deployed. Downstream, both consumers protect voice by
  deferring to the **static catalog**, not to this draft's actual choices:
  `writing-humanity-pass` line 12 states "The 'do-not-flag' allowlist IS the
  signature-move list in `writing-voice-modes`," and `writing-critique` line 86
  "Voice → defers to `writing-voice-modes` (signature moves present vs…)." **What
  Sean observes:** `writing-critique` cannot tell whether the intended dial or
  intended closer actually landed (it re-infers intent from prose), and
  `writing-humanity-pass` protects against the *whole* move catalog rather than the
  *specific* instances this piece committed to — so it either over-preserves an
  accidental pattern or scrubs a deliberate one it couldn't confirm was intentional.
  This is an **asymmetry**, not just a gap: the chain already uses named-artifact
  handoffs at *every other* seam — the beat map from `storytelling-architecture` /
  `substack-value-engine`, and the "named artifact — the critique fix list"
  (`writing-critique` line 161). Voice is the *one* handoff carried only implicitly.

- `structural` — **No in-line drift checkpoint during composition.** The skill's
  drift defenses (House Style lines 139–151; Anti-Patterns table lines 242–257;
  Success Criteria lines 298–307) are all **static reference prose and a
  post-hoc checklist** — nothing in the composition flow forces a mid-draft "am I
  still in the register?" pass. The nearest actual *measurement* (the stdlib
  analyzer: sentence-length burstiness, MATTR, opener variety, with a baseline from
  Sean's corpus) lives **downstream in `writing-critique`** (its description; and
  lines 119, 190), so drift toward generic-AI register is caught, if at all, a
  **full stage late** — after voice-modes has already declared done. **What Sean
  observes:** exactly the named disappointment — "drafts drift toward generic-AI
  register mid-piece," and the drift surfaces only when critique flags it (or when
  Sean reads it himself), forcing a revise round that a mid-draft self-check would
  have prevented.

- `structural` — **The 90/10 split is asserted but has no operational
  test.** Line 129 states "Sean Mode is 90% Sean and 10% borrowed technique" and
  "If a draft reads like any one author, the mix is wrong," and the Bad-Sean /
  over-Sedaris anti-patterns (lines 137, 250) describe the failure — but there is
  **no procedure** the composing model can run to *check* the ratio before handing
  off. It is a target with a described failure mode and no checkpoint. **What Sean
  observes:** the split is honored only as well as the model's unaided instinct on
  any given run; there is no repeatable step that catches an over-pulled author
  before the draft leaves the skill. (In-scope: this is about *measuring/enforcing*
  the ratio, **not** re-defining it.)

- `minor` — **Mode selection is a lookup table with no "commit and state the
  choice" step.** The Content Type → Mode Mapping (lines 200–211) and Professional
  Dial (lines 188–198) tell the model *how* to choose, but the skill never
  instructs it to **explicitly name** the chosen mode + dial at the top of a run.
  Because the choice is never surfaced, it can't be recorded (feeds the first
  finding) and Sean can't see/override it before the prose is written. **What Sean
  observes:** he learns which mode the model picked only by reading the finished
  prose and reverse-engineering it.

- `minor` — **Do-Not-Promote enforcement relies on recall, not a gate.** The
  Do-Not-Promote Topics section (lines 259–264) is a strong *rule* ("omit by
  default… not even once") but sits as reference prose with no confirmation step in
  the output. **What Sean observes:** a suppressed-backstory topic can still slip in
  on a run where the model doesn't re-read that section; there's no "confirmed: no
  do-not-promote topic present" checkpoint tied to the handoff. (In-scope: adding
  the *checkpoint*, not editing the topic list, which is local-only anyway.)

---

## Artifact 2 — Intent-Carrying Improvement Spec

Structured with `intent-engineering`'s scaffolding so the *why* survives the
handoff to Fable and to whatever model Fable dispatches. This is a **scaffolding**
spec end-to-end.

### Objective

Every public word Sean ships rides this skill (grounding (a)), and its job is to
make agent-written prose indistinguishable from Sean's own hand. Today the skill
*produces* voice well but *carries and checks* it poorly: the register drifts
mid-piece with no in-line catch, the 90/10 target has no test, and — most costly —
the specific voice decisions a draft makes evaporate at the handoff, leaving the
two downstream guardians (`writing-critique`, `writing-humanity-pass`) to protect
voice by guessing against a generic catalog. The fix matters because it is the
difference between "the voice was right on this run because the model happened to
hold it" and "the voice is *carried and defended* by the pipeline on every run."

### Desired Outcome (from Sean's perspective — answers (c) → (d))

- After a voice write, a **named voice-decision record** exists alongside the
  prose, stating the chosen mode, the dial %, the signature moves deliberately
  deployed (and where), and a do-not-promote clearance. `writing-critique` judges
  the draft **against that record** (did the intended dial/closer land?), and
  `writing-humanity-pass` preserves **exactly those recorded instances** instead of
  pattern-matching the whole catalog.
- Register drift is **caught in-line, during composition** — not a stage later in
  critique. A draft that starts sliding toward generic-AI register triggers a
  self-check before handoff, not a revise round after it.
- The observable end state is grounding (d) verbatim: a reader can't tell an agent
  draft from Sean's hand, drift is caught in-line, and voice decisions travel as a
  named artifact.

### The fix, per finding (with reasoning a weaker model needs)

**Fix 1 — Emit a named voice-decision record (`structural`, highest leverage).**
Add an output step to the skill: when composing a piece (chain mode especially),
voice-modes must emit a small, named **Voice Decision Record** artifact next to the
prose. Minimum fields: chosen **mode**; **Professional Dial %** with the audience
that set it; the **signature moves** deliberately used, each with a one-clause
"where/why" (e.g. "Callback Closer — final line echoes the ferry-horn open");
**do-not-promote clearance** (confirmed none present). Then update the chain
handoff description (Related Skills, lines 286–296) so the record is the thing that
travels forward, and so `writing-critique` and `writing-humanity-pass` are told to
read it.

*Reasoning for the implementer (do not lose this):* the record's purpose is **trust
transfer, not documentation.** The chain already proves this pattern works — the
beat map and the critique fix-list are both named artifacts that survive their
seams; voice is the only decision carried implicitly, and that is precisely why the
two downstream guardians fall back to the generic move-catalog. If you find
yourself tempted to make the record a freeform note, resist: it has to be
**structured enough that `writing-humanity-pass` can map "preserve this exact
instance" and `writing-critique` can map "verify this exact intent landed."** An
unstructured record re-creates the guessing this fix exists to kill. **Scope wall:**
the record captures *which* moves were chosen — it never contains a judgment about
whether a move is *good*, and it never edits the move definitions.

*Open question for Fable (named, not guessed):* **Where should the record live, and
how structured?** Options: (i) an inline fenced block the skill prints above/below
the prose; (ii) a machine-readable header (YAML/JSON) the two downstream skills
parse; (iii) a file the chain passes by path. I lean toward a lightweight,
**human-readable-but-parseable** inline block (option i/ii hybrid) so it survives an
interactive session without new file plumbing — but the right call depends on how
the chain actually passes state between skills today, which I could not fully
confirm from `SKILL.md` alone. Fable should check the live chain handoff mechanism
(how `writing-critique` currently receives the draft) before fixing the format, and
should confirm the record's field list against what `writing-humanity-pass`'s
voice-safe logic and `writing-critique`'s Voice axis actually consume.

**Fix 2 — Add an in-line drift self-check gate during composition (`structural`).**
Add an enforcement checkpoint the composing model runs **before** declaring the
voice write done: a brief self-audit against the register anchors and the
Anti-Patterns table (lines 242–257) — "is this still dive-bar House Style, or has
it slid refined/generic? Any Bad-Sean / over-Sedaris tells? Any Reference Gorging
or Lexical Repetition?" — with instruction to fix in place before handoff.

*Reasoning for the implementer:* the *measurement machinery already exists* — the
stdlib analyzer in `writing-critique` (burstiness, MATTR, opener variety, baseline
from Sean's corpus). The defect is purely one of **timing and ownership**: drift is
currently caught a full stage downstream, which costs a revise round. The cheapest
correct fix is **not** to duplicate the analyzer inside voice-modes; it is to add a
*self-check gate* that references the same anti-pattern taxonomy voice-modes already
owns, so obvious drift is corrected before the prose leaves the skill. **Scope
wall:** this gate checks the draft *against the skill's own already-written
anti-patterns* — it does not invent new voice rules and does not touch the samples.

*Open question for Fable:* **should the gate call `writing-critique`'s analyzer
in-line, or stay a prose self-check?** Calling the analyzer would give a real
measured number (closing Fix 3 too) but couples voice-modes to a downstream
skill's tooling mid-composition, which may be architecturally wrong (critique is
supposed to be the *gate after* voice). A prose self-check is looser but respects
the chain's separation of concerns. I lean prose-self-check for the drift gate and
letting the analyzer stay in critique — but flag it for Fable's judgment; it
depends on whether the analyzer is invokable standalone.

**Fix 3 — Give the 90/10 split an operational test (`structural`).** Add, to the
same in-line gate as Fix 2, a concrete "ratio check" the model performs: does the
draft read as Sean-with-a-technique-surfacing, or has any single author mode taken
over (the line-129 failure: "if a draft reads like any one author, the mix is
wrong")? Name the check as a step, not just a described failure.

*Reasoning for the implementer:* the target and its failure mode are **already
written** (line 129; anti-patterns lines 137, 250). The only thing missing is a
*procedure* that runs. Do **not** try to quantify "90%" numerically — that would be
false precision and risks becoming a taste judgment (scope violation). The check is
qualitative-but-forced: "point to the base-voice spine; confirm no borrowed author
dominates a section." **Scope wall:** you are adding a *checkpoint that the existing
ratio is met*, never re-defining the ratio or the authors.

*Open question for Fable:* is a qualitative forced check enough, or does Sean want a
lightweight measurable proxy (e.g., "no more than N consecutive sentences in a
single borrowed-author register")? I did not invent a threshold because any number
here is a taste call that belongs to Sean, not to an auditing model. Fable should
decide whether to propose a proxy or keep it qualitative.

**Fix 4 — Add an explicit "commit and state the mode" step (`minor`).** Before
composing, instruct the skill to state the chosen mode + dial + audience in one
line. This is the natural front-end of the Fix-1 record and lets Sean intercept a
wrong mode before prose exists.

**Fix 5 — Add a Do-Not-Promote clearance checkpoint (`minor`).** Fold a "confirmed:
no do-not-promote topic present" line into the Fix-1 record so the lines 259–264
rule is *checked at the handoff*, not just available as reference prose.

### What NOT to change (confirmed working — do not "fix" out of over-eagerness)

- **The voice content itself.** The mode descriptions (lines 75–137), the House
  Style register (139–151), the Signature Moves table (157–181), the Anti-Patterns
  diagnoses (242–257), the Professional Dial values (188–198), the 90/10 ratio, and
  every reference to `references/` files are **correct and calibrated** — this audit
  did not evaluate them and Fable must not either. They are the *content this spec
  exists to protect*, not to edit.
- **The chain's compose-vs-scrub separation.** voice-modes composes; critique
  gates; humanity-pass scrubs. The fixes add a *record* and a *self-check*; they do
  not move critique's or humanity-pass's responsibilities into voice-modes.
- **The lossy beat-map handoff by design.** Lines 288–290 deliberately keep the
  upstream handoff lossy on prose so voice isn't flattened. Leave that intact — the
  new record is *downstream* of composition, not a re-introduction of upstream
  drafted lines.
- **The private `references/` and `drafts/` files.** Off-limits, unread, unedited.

---

## Open questions for Fable (consolidated)

1. **Voice Decision Record format & location** (Fix 1): inline fenced block vs
   parseable header vs passed file — depends on the live chain state-passing
   mechanism, which `SKILL.md` alone doesn't reveal. Confirm before fixing format.
2. **Drift gate mechanism** (Fix 2): in-line call to `writing-critique`'s stdlib
   analyzer vs a prose self-check — trade-off is measured-but-coupled vs
   loose-but-clean-separation.
3. **90/10 operationalization** (Fix 3): forced qualitative check vs a Sean-owned
   measurable proxy — any numeric threshold is a taste call I deliberately did not
   invent.
4. **Record field list** (Fix 1): must be validated against what
   `writing-humanity-pass` (voice-safe preservation) and `writing-critique` (Voice
   axis) actually consume, so the record carries exactly what they need and no more.

## Self-review

- Both artifacts present (seam report + intent-carrying spec): **yes**.
- Every finding tagged exactly one severity: **yes** (2 `structural` core + 1
  `structural` + 2 `minor`; no `dangerously-wrong` — nothing here makes Sean *trust*
  bad output, it degrades quality/handoff).
- Spec carries the WHY + critical details for a weaker model: **yes** (each
  `structural` fix has explicit reasoning + a named scope wall).
- Scope constraint honored (scaffolding only, no voice/sample/taste edits, no
  private-dir reads): **yes** — every fix is plumbing; a "What NOT to change" wall
  is stated; private dirs were not read.
- Open questions named where uncertain: **yes** (4).
- No skill edits, no commits: **yes** — this file is the only artifact written.
