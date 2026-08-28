# Vision-model drift-detection feasibility spike — protocol (pre-registered)

Written 2026-08-08 BEFORE any judge run. The L12 gate for the agent-company
product shape (multimodal series-consistency keeper). Bars below are frozen;
results are scored against them, not the other way around.

## Question

Can current vision models judge character/style consistency of a new
installment against a character's own canon references reliably enough to
productize a pre-publish drift gate — including distinguishing canon-sanctioned
change from unintended drift (the haircut problem)?

## Task framing (product-shaped)

Judge receives: CANON REFERENCE image(s) → optional CANON UPDATE note →
CANDIDATE image. Output strict JSON: verdict consistent|drifted, drift_axes,
one-sentence receipt, confidence. No ground truth, no beat description, no
IR criteria text (a stranger's series has none at onboarding — this is
deliberately harder than anima's G6.1b criteria-text protocol).

## Corpus (32 cases, ground truth from anima's Sean-ratified corpora)

- Set A, 11 known-good: ratified clean frames across varied poses/views
  (sean C01,C02,C03,C04,C06,C08; mascot MC01,MC02,MC05,MC10,MC13) vs canon refs.
  Includes the view-variation traps that killed DINOv2 as a hard gate.
- Set B, 14 known-drift: single-axis ratified defects (proportion, palette,
  shading-register, construction-lines, anatomy-count) + 2 hard identity-drift
  specimens from the similarity-gate fixtures (sean-drifted romance-hero,
  mascot-drifted chibi humanoid).
- Set C, 7 haircut: kid wimpy→trained, grandma young→old, mascot pencil→8-bit
  register; each with-note (expect consistent) and without-note (expect
  drifted); +1 adversarial control: register-change note + identity-drifted
  candidate (expect drifted — a sanctioned register change must not excuse an
  identity change).

## Judges

- gemini-3.5-flash (anima's pinned production T2 model), N=3 majority vote,
  temp per production default.
- Claude (Fable 5) via blind subagents reading the same images, N=1,
  cases shuffled and batch-mixed so no batch is single-class.
- Escalation if signal is borderline: gemini-3.5-pro subset re-run.

## Pre-registered bars (GO requires all three on at least one judge)

1. Drift recall (Set B) ≥ 0.75.
2. Clean false-alarm rate (Set A) ≤ 0.20. (Trust: the verified pain evidence
   says creators distrust tools that automate their judgment; a gate that
   cries wolf dies. DINOv2 died here.)
3. Haircut discrimination: with-note sanctioned changes accepted in ≥2/3
   materials AND without-note changes flagged in ≥2/3 materials AND the
   adversarial control still flagged.

NO-GO shape: both judges fail bar 2 badly (false alarms >0.30) or bar 1
(<0.60), or haircut discrimination at chance — then the wedge premise
(closed-loop visual drift gate) is not productizable on current models and
[L12] returns to the drawing board via SUPERSEDES.

CONDITIONAL-GO shape: one bar narrowly missed with an identifiable, testable
fix path (e.g., per-view references, N>3 voting, criteria-text hybrid) — spike
extends before any build hours.

## Cost

Gemini: ~96 flash calls ≈ well under $1. Claude: subscription. Total ≪ $7
task cap.
