# Phase B — Fable Runbook (Sean drives)

The expensive, non-refundable part. Read this whole file once before `/model fable`.
Companion docs: `task-battery.md` (pinned run-prompts), `introspection-protocol.md`,
`validation-harness.md`, and the campaign + research docs in `docs/plans/`.

## Principles (hold these the whole session)

- **Fable audits/plans; Opus implements.** Don't spend Fable writing production code.
- **Capture before you distill.** Fable's raw outputs can't be regenerated once it's
  gone — the distillation into WWF5D can be finished on Opus later. Save every raw
  Fable output to `docs/plans/wwf5d/fable-runs/` and commit *before* co-authoring.
- **F1** — a self-report is a *hypothesis*; only a behavioral delta (Fable vs the Opus
  baseline) is evidence.
- **F2** — WWF5D holds *abstracted recipes* (procedures/checklists/rubrics/templates),
  never transcripts.
- **F3** — expect *partial* transfer; log what didn't port.
- **F4** — the validation judge is cross-family, order-swapped, κ-gated, your eye final —
  and it runs on **Opus after Fable**, so it costs zero Fable budget.

## Pre-flight (verified 2026-07-05 — re-check only if the tree moved)

- Pins reachable: `code-brain@93e5725` ✓, `anima@aa2007c` ✓.
- BT1 target + BT3 chain skills present ✓; BT2's four anima paths present ✓.
- Make the capture dir: `mkdir -p docs/plans/wwf5d/fable-runs`
- `/model fable`. Ground every run first — no cold kickoffs.

---

## Slice 1 — WWF5D deep dive (≈40%) — the crown jewel

### 1a. Introspection (hypotheses)
Run the 7 questions in `introspection-protocol.md`, one at a time. Save Fable's answers →
`fable-runs/introspection.md`, commit. These are hypotheses (F1) — none becomes a WWF5D
move without a corroborating delta in 1c.

### 1b. Battery — Fable runs BLIND
For each of BT1, BT2, BT3: open a **fresh** Fable session and paste that task's pinned Run
Prompt from `task-battery.md` verbatim. **Do not show Fable the Opus baseline** — the blind
run is what makes the diff clean. Save Fable's full output → `fable-runs/bt1-fable.md` /
`bt2-fable.md` / `bt3-fable.md`, commit after each.

### 1c. Behavioral diff — the evidence
For each BTn, now show Fable **both** its own output (`bt{n}-fable.md`) and the Opus
baseline (`baselines/bt{n}-opus.md`) and ask: what did you do that Opus missed or got
wrong? Tag each delta `dangerously-wrong | structural | minor`. Save →
`fable-runs/bt{n}-diff.md`. These deltas are the only admissible WWF5D evidence (F1).

### 1d. Corroborate
Cross the 1a hypotheses against the 1c deltas. A self-reported move enters WWF5D **only if**
a delta shows Fable actually did it and Opus didn't. Drop uncorroborated self-reports.

### 1e. Co-author WWF5D
Fill `.claude/skills/wwf5d/SKILL.md` sections 1–6 from corroborated moves — abstracted
recipes only, never transcripts (F2). Commit.

### 1f. Save the BT3 creative-chain spec
BT3's output includes a real chain-level improvement spec — save it →
`docs/plans/wwf5d/creative-chain-spec.md` for Opus to implement in Phase C (double duty).

**Done when:** `fable-runs/` holds introspection + 3 blind runs + 3 diffs (committed), and
`wwf5d/SKILL.md` §1–6 are filled from corroborated moves.

---

## Slice 2 — Tier-1 skill audits (≈30%)

For each of the five — `writing-voice-modes`, `intent-engineering`, `skill-system-mastery`,
`plan-and-think`, `systematic-debugging`:

- Give Fable the skill's current `SKILL.md` **plus** its Opus draft spec
  `docs/plans/wwf5d/tier1-specs/<skill>.md`, and have it **elevate** the skill to "wow"
  (the draft is a floor, not a ceiling).
- **Public `SKILL.md` only** — never `references/` or `drafts/` (privacy layer).
- `writing-voice-modes`: edit the scaffolding, **never** the voice samples/content.
- Commit per skill.

**Done when:** all five `SKILL.md` files are improved + committed. Re-run
`python3 scripts/validate.py` (expect green).

---

## Slice 3 — anima register-seam (≈30%) — note the overlap

BT2 in Slice 1 **is** the anima register-seam audit (`zoom-out-and-think`, run on Fable).
So this slice is mostly already done:

- **Default (recommended):** if BT2's Fable spec (`fable-runs/bt2-fable.md`) is
  production-grade, save it → `docs/plans/wwf5d/anima-register-seam-spec.md`. Slice 3 is
  then nearly free — reclaim the budget for a deeper WWF5D pass or a second Tier-1 loop.
- **Only if you want more depth:** re-run `zoom-out-and-think` with anima read-access
  widened beyond the four pinned files, for a fuller spec. Diagnosis + spec only; Opus
  implements in Phase C; **anima stays read-only** (never edit/stage/commit in it).

**Done when:** `docs/plans/wwf5d/anima-register-seam-spec.md` exists.

---

## After Fable (Opus — zero Fable budget)

- **Validation** (`validation-harness.md`): Opus-with-WWF5D vs each baseline; cross-family
  order-swapped panel (not Opus-led); κ-gate to ~10 of your labels; your eye final. Write
  results into `wwf5d/SKILL.md` §7 (the ceiling, F3).
- **Phase C:** implement the anima spec + Tier-1 spec items with Opus/subagents.

## If the window closes early (triage)

Raw beats distilled — raw can't be regenerated. Capture in this order, committing as you go:

1. `fable-runs/introspection.md`
2. `fable-runs/bt{1,2,3}-fable.md` (the blind runs)
3. `fable-runs/bt{1,2,3}-diff.md` (the deltas)

Everything after — co-authoring, Tier-1 elevation, validation — can be finished on Opus. So
if Fable is about to vanish, dump raw + commit, and distill later.
