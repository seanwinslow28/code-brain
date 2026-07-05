# WWF5D — Validation Harness (held-out A/B)

For each battery task, compare Opus-with-WWF5D vs the saved Opus baseline.

Judge design (constraint F4):
- Order-swapped: run each comparison twice with A/B order flipped; a win counts only if it holds both ways, else tie.
- Length-controlled: do not let the longer answer win by default.
- Cross-family panel, NOT Opus-led (self-preference is causal): use the LLM Council `variance`/cross-family profile; the chairman must not be the author's family.
- Calibrate to ~10 Sean labels with Cohen's κ (target ≥ 0.6). Reuse the anima Em protocol (N=5 majority, reference-blind).
- Sean's eye is the Engine-Truth final call.

Success = WWF5D-Opus beats baseline on the core battery, κ-gated, with a written transfer analysis (what ported / what hit the F3 ceiling → Section 7 of the skill).
