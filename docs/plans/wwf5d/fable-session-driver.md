# Fable Session Driver — literal steps

Follow top to bottom. You are mostly **pasting** pre-written prompts, not writing them.

**"Fresh context"** = type `/clear`, then glance at `/model` to confirm it still shows
`fable`. That's all a fresh context takes — you do NOT need to relaunch Claude Code.

**Why the fresh context matters:** each Opus baseline was generated on a blank slate. For the
Fable-vs-Opus diff to be fair, Fable must hit each battery task on a blank slate too. One long
chat would let task 1 prime task 2 and break the comparison.

---

## Pre-flight (once)

- [ ] `git add` + commit the runbook and the learnings log (both uncommitted on `main`)
- [ ] `mkdir -p docs/plans/wwf5d/fable-runs`
- [ ] Open `docs/plans/wwf5d/fable-learnings-log.md` in a side tab
- [ ] `/model fable` → run `/model` and confirm it shows `fable`

---

## SLICE 1 — WWF5D (~40%, do this whole slice first)

### 1a — Introspection (its own fresh context)
- [ ] `/clear` → confirm `/model` shows `fable`
- [ ] Paste this, then the 7 questions from `introspection-protocol.md`:
  > Answer these one at a time, from your own experience. These are hypotheses I'll verify
  > against your actual behavior later, so be candid and specific, not idealized.
- [ ] Save Fable's answers → `fable-runs/introspection.md`; commit
- [ ] Do NOT run a battery task in this context (it would prime the blind runs)

### 1b — Blind runs (ONE fresh context each — this is the fair-diff condition)
**BT1**
- [ ] `/clear` → confirm `/model` shows `fable`
- [ ] Open `task-battery.md`, copy the **entire "Run prompt" block for BT1**, paste verbatim
- [ ] Do NOT open or paste `baselines/bt1-opus.md` here — this run is blind
- [ ] Save Fable's full output → `fable-runs/bt1-fable.md`; commit

**BT2**
- [ ] `/clear` → confirm `/model` shows `fable`
- [ ] Paste BT2's **Run prompt** block verbatim (anima is read-only — never edit it)
- [ ] Save → `fable-runs/bt2-fable.md`; commit

**BT3**
- [ ] `/clear` → confirm `/model` shows `fable`
- [ ] Paste BT3's **Run prompt** block verbatim
- [ ] Save → `fable-runs/bt3-fable.md`; commit

### 1c — Diff (one shared context is fine — this is analysis, not a blind run)
- [ ] `/clear` → confirm `/model` shows `fable`
- [ ] For each n in 1, 2, 3, paste `fable-runs/bt{n}-fable.md` **and** `baselines/bt{n}-opus.md`, then:
  > You wrote the first output. A weaker model (Opus) wrote the second on the identical task
  > with identical inputs. What did you do that it missed or got wrong? Tag each real
  > difference `dangerously-wrong` / `structural` / `minor`. Ignore mere style — only quality deltas.
- [ ] Save each → `fable-runs/bt{n}-diff.md`; commit
- [ ] Jot the standouts into the learnings log

### 1d + 1e — Corroborate + co-author WWF5D (fresh context)
- [ ] `/clear` → confirm `/model` shows `fable`
- [ ] Paste `introspection.md` + the three `bt{n}-diff.md` files, then:
  > Fill the empty sections of `.claude/skills/wwf5d/SKILL.md`. Hard rule: a move goes in ONLY
  > if a diff shows you actually did it and Opus didn't (F1). Write abstracted recipes —
  > checklists, rubrics, procedures, templates — never transcripts (F2).
- [ ] Save → `.claude/skills/wwf5d/SKILL.md`; commit

### 1f — Save the creative-chain deliverable
- [ ] Copy BT3's chain-level spec out of `fable-runs/bt3-fable.md` → `docs/plans/wwf5d/creative-chain-spec.md`; commit

---

## SLICE 2 — Tier-1 audits (~30%, fresh context per skill)

For each of: `writing-voice-modes`, `intent-engineering`, `skill-system-mastery`,
`plan-and-think`, `systematic-debugging`:
- [ ] `/clear` → confirm `/model` shows `fable`
- [ ] Paste the skill's current `SKILL.md` + its draft `tier1-specs/<skill>.md`, then:
  > Elevate this skill to "wow" using the draft spec as a floor, not a ceiling. Edit the
  > public SKILL.md only — never references/ or drafts/.
  (For `writing-voice-modes` add: *never touch the voice samples/content — only the scaffolding.*)
- [ ] Save the improved `SKILL.md`; commit; run `python3 scripts/validate.py` (expect green)

---

## SLICE 3 — anima (~30%, decide from BT2's quality)

- [ ] Read `fable-runs/bt2-fable.md`. If its spec is production-grade → copy it to
      `docs/plans/wwf5d/anima-register-seam-spec.md`; commit. Slice 3 done — reclaim the time
      (generate BT4/BT5 Opus baselines on Opus, then run them on Fable as extra WWF5D diff tasks).
- [ ] If it's thin, or anima is the priority → `/clear`, re-run `zoom-out-and-think` with anima
      read-access widened past the four pinned files. Diagnosis + spec only; anima stays read-only.

---

## After Fable (Opus — costs zero Fable time)

- [ ] Validation per `validation-harness.md` (Opus-with-WWF5D vs the baselines; cross-family
      council, order-swapped, κ-gated; your eye final). Write results into `wwf5d/SKILL.md` §7.
- [ ] Phase C: implement the specs; load WWF5D as Opus standing context; re-run the Tier-2/3 tail.

---

## If the window closes early

Capture beats distill — raw can't be regenerated. In order, committing as you go:
`introspection.md` → `bt{1,2,3}-fable.md` → `bt{1,2,3}-diff.md`. Everything after that
(co-author, Tier-1, validation) finishes on Opus later.
