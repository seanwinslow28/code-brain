---
title: "Vision-model drift detection — feasibility spike (L12 gate): GO/NO-GO evidence memo"
date: 2026-08-08
project: agent-company-founding
type: feasibility-spike
status: final
tags: [agent-company, series-consistency, evals, vision-models, L12-gate]
---

# Vision-model drift detection — the L12 feasibility spike

**Verdict: GO — both judges cleared all three pre-registered bars.** The
multimodal series-consistency wedge is not a fool's errand on current vision
models. [L12] stands; the campaign proceeds to the software-factory
literature review.

The [L12] lock (multimodal series-consistency keeper) was research-gated on one
question, in Sean's words: *"if research and testing shows it's a fools errand,
than we should go back to the drawing board before I spend months of my time on
an impossible task."* This memo is that test.

## Question

Can current vision models judge character/style consistency of a new
installment against a character's own canon references reliably enough to
productize a pre-publish drift gate — including the **haircut problem**
(distinguishing canon-sanctioned change from unintended drift)?

## Method (pre-registered before any judge ran)

- **Corpus:** 32 cases built entirely from anima's Sean-ratified ground truth
  (the named L12 testbed): 11 known-good frames across varied poses/views,
  14 known-drifted frames (single-axis ratified defects: proportion, palette,
  shading-register, construction-lines, anatomy-count; plus 2 hard
  identity-drift specimens), and 7 haircut cases (kid wimpy→trained,
  grandma young→old, mascot pencil→8-bit register — each with and without a
  declared canon-update note, plus 1 adversarial control: a register-change
  note paired with an identity-drifted candidate).
- **Task framing is product-shaped:** canon reference images + optional
  canon-update note + candidate → verdict + drift axes + receipt. No criteria
  text, no beat description — deliberately harder than anima's G6.1b protocol,
  because a stranger's series has neither at onboarding.
- **Blinding:** Claude judged via subagents over neutrally renamed copies
  (filenames like `sean-drifted.png` leak ground truth); batches were
  class-mixed; with-note/without-note twins never shared a judge. Gemini
  received raw bytes (no filename leak by construction).
- **Judges:** gemini-3.5-flash (anima's pinned production T2 model, N=3
  majority) and Claude Fable 5 (N=1 blind subagents).
- **Pre-registered bars (GO = all three on ≥1 judge):** drift recall ≥ 0.75;
  clean false-alarm rate ≤ 0.20; haircut discrimination (≥2/3 sanctioned
  changes accepted with note, ≥2/3 flagged without note, adversarial control
  still flagged).

Protocol + harness + full per-case results (receipts included):
[2026-08-08-vision-drift-spike/](2026-08-08-vision-drift-spike/) alongside this
memo.

## Results

### Claude (Fable 5, blind subagents, N=1)

| Bar | Result | Threshold | |
|---|---|---|---|
| Drift recall (Set B) | **0.86** (12/14) | ≥ 0.75 | PASS |
| Clean false-alarm rate (Set A) | **0.09** (1/11) | ≤ 0.20 | PASS |
| Haircut discrimination | **3/3 with-note accepted, 3/3 without-note flagged, control flagged** | ≥2/3 + ≥2/3 + control | PASS |

All three pre-registered bars pass. Every receipt cited real, checkable visual
evidence (e.g., the adversarial control: "the note only declares the 8-bit
register… but the candidate swaps the six stub legs and side-mounted arm stubs
for a two-armed, two-legged humanoid body plan — undeclared anatomy drift").

**Failure anatomy — all 3 errors are the same case shape.** The two misses
(X21, X22) and the one false alarm (X07) are all *leg-count* judgments on the
multi-legged mascot, where the visible stub count legitimately varies with
pose and occlusion (canon anchor shows ~5, a ratified-clean front view shows
2, a "defect" shows 3). Verified by direct inspection: these are undecidable
from reference images alone — they require a stated canon fact ("this
character has N legs"). That is precisely the product's series-bible layer,
and anima independently reached the same conclusion (its layer-ownership map
assigns anatomy-count to the deterministic Bible-lock, not the vision critic).
The residual failure mode is **addressable by architecture already in the
product shape, not a model-capability wall.**

### gemini-3.5-flash (production pin, N=3 majority)

| Bar | Result | Threshold | |
|---|---|---|---|
| Drift recall (Set B) | **1.00** (14/14) | ≥ 0.75 | PASS |
| Clean false-alarm rate (Set A) | **0.18** (2/11) | ≤ 0.20 | PASS |
| Haircut discrimination | **2/3 with-note accepted, 3/3 without-note flagged, control flagged** | ≥2/3 + ≥2/3 + control | PASS |

All three bars pass. Run cost: well under $1 (96 flash calls).

### Cross-model read

The two judges fail in **complementary directions**, which is itself a design
finding:

- **Gemini is maximally strict:** perfect drift recall, but it over-flags fine
  detail — both false alarms cite sub-features (eye specular highlights,
  eyelid detail on an extreme close-up) that the ratified ground truth treats
  as legitimate variation. Its one haircut "miss" (X30, the pixel-art register
  swap) is a strictness disagreement, not note-blindness: two of three votes
  flagged a *real* residual detail the note didn't declare (the pixel sprite's
  snout-like protrusion — which a Claude judge independently flagged in the
  no-note twin). The note mechanism itself was honored in the other votes.
- **Claude is calibrated but misses subtle counts:** lower false-alarm rate
  (0.09), perfect note-conditioning, but it missed the two subtlest
  anatomy-count defects.
- **The one case both models got wrong (X07)** is the leg-count-from-front
  case that is genuinely undecidable without a stated canon fact.

Product implications, all of which land in architecture the shape already
carries: (1) a structured series bible converting countable canon facts into
checkable criteria (anima's G6.1b showed criteria-text grounding lifts
citation accuracy 0.03→0.97 on exactly this class); (2) a multi-model judge
panel exploiting the complementary strict/calibrated profiles rather than a
single judge; (3) canon-update notes must enumerate what they sanction —
undeclared residuals SHOULD flag, and did.

## Feasibility cautions from the record, addressed

- **DINOv2/embedding gating fails** (anima similarity-gate, 2026-06): drifted
  specimens score inside the good-plate range across views. The spike's Set A
  deliberately included those view-variation traps; MLLM judging with canon
  references handled them (1 false alarm in 11, and it was the leg-count case,
  not a view case).
- **FlawedFictions (arxiv 2504.11900):** SOTA LLMs struggle at long-story
  plot-hole detection — a caution for the TEXT-canon modality at long context,
  not falsified here. The spike tested the visual modality (the unclaimed
  wedge per the round-3 prior-art sweep). Text-lane depth remains a risk to
  manage (incumbents: Novarrium/Novelium/Bunsho).
- **Haircut problem (Sean's named design question):** the declared-canon-update
  mechanism worked end-to-end in this spike — sanctioned changes accepted,
  the same changes flagged when undeclared, and a note did NOT bleed into
  excusing an unrelated identity change (control case). The design answer is
  a first-class "canon update" event in the series bible.

## What this spike does NOT establish

- Scale: 32 cases, 2 characters, one visual register family, one-shot judging.
  A production gate needs per-creator calibration corpora and N>1 voting.
- Video drift (Veo-specimen shape from the evidence ledger) untested — stills
  only.
- Text+visual+voice in ONE report (the actual product promise) untested as an
  integrated artifact.
- Cost/latency at production volume unmeasured (spike cost: <$1 Gemini,
  subscription Claude).

## Recommendation

**GO.** Proceed with [L12] as locked. The gate question — can current vision
models judge cross-installment character/style consistency against a
character's own canon, including the haircut problem — comes back yes, on both
a frontier model and a cheap production-pinned flash model, under a
deliberately product-shaped (reference-only, no-criteria-text) protocol, with
all failures concentrated in one architecturally-addressable case shape.

Carry into the campaign's next steps:

1. **Architecture ratification (step 4)** should treat the series bible as the
   load-bearing component: canon facts (counts, colors, register) extracted at
   onboarding become checkable criteria; the vision judge owns what can't be
   enumerated. This mirrors anima's ratified layer-ownership split and is now
   evidence-backed for the product.
2. **Eval-stack design (step 5)** inherits this spike's corpus design (paired
   clean/defect, haircut twins, adversarial controls, pre-registered bars) as
   the seed pattern for product-evals — the evals ARE the product [product-shape
   round 1].
3. **Open risks to retire later:** video drift, long-context text canon
   (FlawedFictions), integrated multimodal report, per-creator calibration at
   scale, production cost/latency.

## Provenance

- Decision record: `~/.creative-harness/partner-sessions/2026-08-07-agent-company-founding.md` (L1-L12)
- Kickoff: [docs/prompts/2026-08-08-agent-company-research-campaign-kickoff.md](../../../docs/prompts/2026-08-08-agent-company-research-campaign-kickoff.md)
- Ground truth: anima `evals/vision_critic/cases.yaml` (Sean-ratified 2026-06-03/04), `evals/similarity-gate/fixtures`, `characters/{kid,grandma,claude-mascot,sean-anchor}`
