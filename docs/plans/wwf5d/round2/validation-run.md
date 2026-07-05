# WWF5D Step 4 — Validation Run (turnkey hand-off)

- **Date:** 2026-07-05
- **What this validates:** does WWF5D *transfer* — does Opus-**with**-WWF5D beat Opus-**without** on the battery? The artifact judged is the **transfer**, not Fable's work.
- **Status:** A/B material **generated** (below). The de-biased council + Sean's κ-labels are the **gate** — prepped here, pending Sean's go (budget) + labels.

## The A/B pairs (all in `docs/plans/wwf5d/round2/`)

| Task | Without WWF5D (baseline) | With WWF5D | What to watch |
|---|---|---|---|
| RT1 | `rt1-opus.md` | `rt1-opus-wwf5d.md` | Does WITH catch the two contradictions the baseline **shipped** — Open-Questions-written-but-unread (§2.3 paired change) and the cap-that-**drops** in a zero-loss spec (§6.9)? |
| RT2 | `rt2-opus.md` | `rt2-opus-wwf5d.md` | Does WITH add the live-docs version gap (§1.3) + the taught false-safety patterns the baseline missed? |
| RT3 | `rt3-opus.md` | `rt3-opus-wwf5d.md` | Does WITH run the **real** `audit_intent_spec` (§5.2) + surface the owner-fork honoring the prior kill-switch (§6.8), vs the baseline's hand-validation? |

**Preliminary (NON-authoritative) read:** the WITH arms' own self-reports claim they applied exactly these moves and caught exactly these items. **This is not evidence** — self-report is F1-unreliable (the arms were primed by the "name what you caught" instruction), and an Opus orchestrator judging Opus-vs-Opus is F4-contaminated (self-preference is causal). The verdict is the blind council + Sean's eye.

## Judge design (validation-harness.md, F4)

1. **Reference-blind + label-blind.** The judge sees the two outputs as "A" and "B" only — never which is WWF5D, never the task's provenance.
2. **Order-swapped.** Run each comparison twice with A/B flipped; a win counts only if it holds **both ways**, else tie.
3. **Length-controlled.** The WITH arms are longer (RT1 +14%, RT2 +146%, RT3 +121%) — instruct the judge explicitly not to reward length; judge on the premium moves (spec-decidedness, breadth, contract-contradiction, evidence-discipline), not word count. (The RT2 length gap is large — watch for verbosity bias hardest there.)
4. **Cross-family, NOT Opus-led.** ⚠ **Both stock council profiles have a Claude chairman** (variance → Sonnet; premium → Opus 4.7) — the *author's own family*, which F4 forbids as the deciding vote. Fix ONE of:
   - **(a) preferred** — use the **panel cross-rank** (the non-Claude members: GPT-5.x, DeepSeek, Mistral, Gemini) as the verdict and **discount the Claude chairman's synthesis** (read it, don't let it decide); or
   - **(b)** override the chairman to a non-Claude model (e.g. GPT-5.5 or Gemini Pro) for these runs.
5. **κ-gate to ~10 Sean labels.** Reuse the anima Em protocol: **N=5 majority, reference-blind**. Sean labels ~10 A/B comparisons (better-A / better-B / tie) blind to which is WWF5D; compute Cohen's **κ** between Sean's labels and the panel's majority; **gate κ ≥ 0.6** before trusting the panel verdict. (Only ~6 pairs exist here — 3 tasks × 2 order-swaps — so widen the label set by scoring per-premium-move, or accept a smaller κ sample and report it honestly.)
6. **Sean's eye is the Engine-Truth final call.**

## Turnkey command (per pair, order-swapped)

```bash
cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council
# Feed the comparison as the query. Do this TWICE per task with A/B order flipped.
uv run python -m council --profile variance --tag wwf5d-val-rt1-AB \
  <<'PROMPT'
You are judging two intent-carrying fix specs, A and B, for the same skill (preserve-session),
written from the SAME findings. Judge ONLY on: spec-decidedness (pre-made decisions, edge
guidance, done-criteria), breadth past the named seams, contract-contradiction detection, and
evidence-discipline. Do NOT reward length. Which better exhibits these — A, B, or tie — and why?
Flag any place a spec's own rule contradicts its stated objective.

--- SPEC A ---
<paste rt1-opus.md body>
--- SPEC B ---
<paste rt1-opus-wwf5d.md body>
PROMPT
```

Repeat with A/B swapped (`--tag wwf5d-val-rt1-BA`), and for rt2 (`skill-audit` outputs) and rt3
(`enhancement spec` outputs) with task-appropriate criteria. Budget: variance ≈ $0.10–0.40/query
× ~6 queries ≈ **$0.6–2.4 total** (Sean's OpenRouter budget — his OK to spend). Transcripts land
next to this file; session JSON in `tools/llm-council/data/sessions/`.

## Decision

- κ ≥ 0.6 AND panel (non-Claude) majority favors WITH on the premium moves, held both order-ways → **WWF5D transfers**; record which moves ported.
- Panel favors WITHOUT or ties → the move did **not** transfer for Opus (F3 ceiling) — record it in §7 as such.
- Sean's eye overrides either way (Engine Truth).

## Already-known ceiling (F3, independent of the council)

- **Research-trigger presence is promptable — retired as Fable-unique** (RT3: fired for both arms). WWF5D must not claim it.
- **The plain diagnosis / zoom-out loop is cheap-on-Opus** (BT2 + BT5) — §3's scope note already says don't spend premium effort there; the validation should show near-parity on that axis, and that's expected, not a failure.
- **Weaker-model (Sonnet) transfer is untested** — this A/B is Opus-with vs Opus-without; whether the folded recipes lift *Sonnet* is a separate, unrun measurement (the deployment target per the campaign is Opus/Sonnet standing context).
