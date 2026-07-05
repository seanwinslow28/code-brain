---
type: prd
product: "DriftCatch (working name)"
post: take-two-01-teach-the-model-your-hand
created: 2026-06-28
status: draft-v1
related:
  - "true-pain-and-opportunity-map.md"
  - "matrix-results-scored.md"
  - "../playbook/tool-shipping-playbook.md"
---

# PRD: DriftCatch (working name)

> Working names to choose later: DriftCatch, The Likeness Dial, Throughline, Selvedge, Still-You. Naming is a separate pass; this doc uses DriftCatch.

## The wedge in one sentence (read this first)

Every AI image tool can restyle your face. None of them tell you **when you stopped being you**, or hand you the fix. DriftCatch is the judgment layer: anchor your identity and style once, push any transformation, and it catches the drift and proposes the correction. The friction it kills: *keeping it recognizably me across every restyle without re-pasting a "do not change my face" paragraph and eyeballing eighty outputs by hand.*

This is table stakes vs wedge, named explicitly (playbook step 2): "make a consistent character" is table stakes, owned by every model and a hundred wrappers. The wedge nobody ships is **anchor → push → auto-catch-drift → propose-fix**, with the drift call as a visible, honest signal. It is a near-direct lift of the anima critic pattern, which is the asset, not something to re-research.

---

## 1. Summary

DriftCatch is a packaged skill that gives non-coders a controllable, repeatable dial for how much of a person survives an AI image transformation. You give it a face and a style; it generates a set, scores each output against the anchor on the features that actually carry identity, flags the ones that drifted, and proposes the exact prompt fix. It is the tool the flagship post "Teach the Model Your Hand" demonstrates and ships.

## 2. Contacts

| Name | Role | Comment |
|------|------|---------|
| Sean Winslow | Owner / PM / builder | Pencil & Prompt; reuses the anima critic + Character Bible pattern |
| (TBD) | Stranger dogfood persona | Required gate before "it works" (playbook step 6); a non-Sean creative |
| Readers of Pencil & Prompt | First users | Creatives, designers, animators, marketers shifting into AI |

## 3. Background

**Context.** Across five dated mid-2026 discovery streams, the loudest and most recent complaint about AI image generation is not "it can't render me," it is "it changes my face the moment I stylize, and I can't control how much." The field's actual workaround is shouting DO NOT CHANGE FACE in capital letters, which is proof there is no real control. Every additional edit compounds the drift (users report faces going "thirty years older" or "plastic" after three or four passes).

**Why now.** Two things changed. First, likeness got cheap: ChatGPT's current model (gpt-image-2) renders a recognizable person across any medium on the first try. Sean's own 12-style matrix scored likeness 2/2 across all twelve styles. So the bottleneck moved from "can it draw me" to "can I control how much of me survives, repeatably." Second, the consistency-wrapper market commoditized the easy half (lock one face), leaving the judgment half (catch and fix drift across a set) unowned.

**Why this is buildable now, and by Sean specifically.** The hard part is the judgment layer, and Sean already has a working reference implementation of it in anima: a Character Bible that locks identity as named markers, a tier-1 rule gate, and a tier-2 vision critic that "proposes prompt diffs, not pass/fail." DriftCatch is that pattern productized for a creative who will never open a code editor.

## 4. Objective

**Objective.** Turn the manual, high-toil "anchor, push, eyeball for drift, re-roll, cull" loop into a one-command loop that returns an on-model set plus an honest drift report. Give the user a *dial* (how much me vs how much style) that behaves predictably across runs.

**Why it matters.** It relieves the single loudest unmet pain in the category, it is defensible (commodity models improve underneath the critic layer while the critic layer stays valuable), and it produces the triple payout in the shipping playbook: an installable tool, a portfolio artifact, and the flagship post.

**Key results (SMART).**
- KR1: A first-time user goes from a photo to a five-image on-model set with a passing drift report in under 10 minutes, without writing a prompt from scratch.
- KR2: On a held-out test set, DriftCatch's drift verdict agrees with Sean's eye at least 90% of the time (the bar anima already hit for its tier-2 critic calibration).
- KR3: Across an iterative run, measured drift goes DOWN turn over turn (a visible convergence signal, the proof).
- KR4: Ships as an installable marketplace repo with a one-screen before/after demo within the post's launch window.

## 5. Market segment(s)

Defined by job, not demographic.

- **Primary: the serious solo creative** (illustrator, animator, designer, newsletter writer, indie filmmaker) who wants AI output that is recognizably *theirs* across a set and is tired of re-pasting identity descriptions and culling huge batches by hand.
- **Secondary: the small marketing / brand team** that needs a person or mascot to stay on-model across many assets and platforms.
- **Constraints they bring:** mostly non-coders; security-anxious about plugins that touch their accounts or cloud; already pay for ChatGPT and will not "clone a repo." Local-first and no-mandatory-API-key is a feature, not a footnote.

## 6. Value proposition(s)

**The job:** "Make AI produce work that is recognizably mine, across a whole set, without babysitting it."

**Gains:**
- A real dial: choose how far to push style while a named set of your features is held.
- An honest answer to "is this still me?" per image, instead of squinting.
- The fix handed to you, not just the flag.
- A reusable anchor (your face + your style as a saved spec), so run two is not run one all over again.

**Pains avoided:**
- Re-pasting a "DNA template" before every generation.
- Culling 80 outputs to find 4.
- Silent compounding drift across edits.
- Losing your whole library when the model updates.

**Where we beat competitors (the value curve):** consistency wrappers compete on "lock one face" and on raw output volume. DriftCatch dips below them on raw generation (it rides whatever model you already use) and spikes far above them on the axes nobody serves: **drift detection, the fix proposal, the controllable dial, and an honest convergence proof.** It counter-positions on honesty: competitors promise "80% on the first try," DriftCatch shows you the drift and the convergence.

## 7. Solution

### 7.1 UX / flow

Two surfaces, same engine. v1 ships the accessible one first.

- **Default (accessible): the ChatGPT companion.** The skill builds the likeness-lock + style-logic prompt blocks for you, walks you through the fan-out in the ChatGPT app (no key, no code), then you drop the outputs into a local folder and DriftCatch returns the drift report + fixes. Honors the playbook's local-first, no-mandatory-key rule.
- **Power mode (later): the automated loop.** With the user's own OpenAI key, DriftCatch runs the full anchor → generate (images.edit) → score → re-roll loop unattended.

Core flow (v1):
1. Drop in 1 to 3 anchor images of the subject.
2. DriftCatch drafts the likeness-lock spec (named identity markers) and you confirm or edit it once.
3. Pick or write a style-logic block and set the dial (how much me vs how much style).
4. Generate the set (companion mode: guided in ChatGPT; power mode: automatic).
5. DriftCatch returns: the on-model set, a per-image drift verdict (pass / drifted, on which markers), and the corrective prompt diff for each miss.
6. Re-roll the misses with one click; watch the drift shrink.

### 7.2 Key features

1. **Likeness-Lock spec.** A saved, reusable anchor: the five-field identity markers (the features that actually carry identity, per the face-recognition research) plus the reference bundle. Author once, reuse forever. (Reuses anima's Character Bible identity block.)
2. **Style-Logic block.** The swappable five-field style description (medium, mark-making, palette rule, register, signature move), so you change the look without disturbing the identity. (Reuses anima's register-clause library.)
3. **The Dial.** A target identity-retention level. Because gpt-image-2 exposes no parameter, the dial is enforced by the verify loop: generate, score against the anchor, re-roll or correct until it clears the target. The dial is a *workflow* promise, not a model knob, and the PRD says so plainly.
4. **Drift-Catcher (the wedge).** A vision-critic read that compares each output to the anchor on the named markers and returns pass / drifted-on-X. Leans on a vision model's judgment ("is this still him, on the brow, eye-spacing, jaw, hair") rather than a brittle similarity metric, because identity metrics are known to be unreliable across hard style changes (anima already documented this with DINOv2/CLIP). (Reuses anima's tier-2 critic.)
5. **Fix proposer.** For each drifted image, the exact prompt diff to correct it (the "propose diffs, not pass/fail" principle).
6. **Convergence proof.** A drift-over-iterations signal the user can watch go down, the deterministic before/after that makes the technical crowd trust it (mirrors VoicePrint's shrinking edit-diffs).
7. **Batch cull (fast-follow).** Rank a large output batch to the keepers with reject reasons (the second-loudest toil).

### 7.3 Technology

- Rides the user's existing image tool (ChatGPT / gpt-image-2 default; model-agnostic by design so it survives model churn).
- The drift check is the only "intelligence" DriftCatch owns; v1 can run it via a vision model (local where feasible, or the user's own key) so the package stays install-safe.
- Distribution: a GitHub marketplace repo (`marketplace.json`), not only a `.plugin`, since discovery is social-first and install is from the marketplaces.
- Reuse map (the unfair advantage, not re-researched): Likeness-Lock = anima Character Bible identity block; Style-Logic = anima register-clause library; Drift-Catcher = anima tier-2 vision critic; the Dial = anima draft-to-pro / retry-ladder discipline.

### 7.4 Assumptions (flag and validate)

- A1: A vision-critic read can judge "still them, on these markers" reliably across hard style changes. (Highest-risk; anima's tier-2 calibration is the evidence it can, but it must be re-proven for arbitrary user faces.)
- A2: Non-coders will tolerate the companion-mode handoff (generate in ChatGPT, return outputs to DriftCatch) for v1. Validate in the stranger dogfood.
- A3: Users want a reusable saved anchor enough to do the one-time setup. (The toil evidence strongly suggests yes.)
- A4: The dial-as-workflow (re-roll to a threshold) feels like control, not like more re-rolling. Validate that the convergence signal makes it feel controlled.

## 8. Release

Relative timeframes, no hard dates.

- **v0, proof (this exploration):** Sean's hand-run 12-style matrix and its scored results. Already done; it is the demo's raw material.
- **v1, the shippable skill:** Likeness-Lock spec + Style-Logic block + Drift-Catcher + Fix proposer + convergence proof, companion mode, marketplace repo, one-screen before/after, passed through both stranger-dogfood gates (zero-leakage + distinctness). This is what the post ships.
- **Fast-follow:** Batch cull; the power-mode automated loop (user's own key).
- **Roadmap (the bigger judgment-layer products, explicitly out of v1):** believable world/era insertion (identity-lock + era-fact-check + lighting-match); multi-character, long-series consistency with drift auditing (the deepest whitespace, and the closest to anima's full pipeline).

## Risks

- **The dial is what the whole field is racing toward.** Mitigation: own the model-agnostic workflow/critic layer, which survives and benefits from model upgrades; never claim a model feature.
- **The auto-diff is the make-or-break.** If the drift verdict is not trustworthy, the wedge collapses. Mitigation: calibrate against Sean's eye on a labeled set before launch (the anima Gate-2 method), and ship the agreement number honestly.
- **Companion-mode friction.** The ChatGPT handoff could feel clunky. Mitigation: dogfood a stranger; if it fails the gate, prioritize power mode.
- **Packaging trust.** New solo tool, no install count. Mitigation: local-first, no mandatory key, transparent build story, one-screen proof (all per the playbook distribution notes).

## Open decisions

1. Final name (separate naming pass).
2. v1 surface: confirm companion-mode-first, or push straight to power mode with the user's key.
3. Where the drift-check vision read runs (fully local model vs the user's own API key) for v1.
