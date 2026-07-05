# Round 2 Session Driver — literal steps (subagent mechanism)

Follow top to bottom. The orchestrator is Opus; each blind run is a fresh **`model:"fable"`**
subagent and each baseline a fresh **`model:"opus"`** subagent, both dispatched with the
**identical** pinned run prompt from [`round2-task-battery.md`](round2-task-battery.md). No
`/clear` — subagent isolation is the fresh-context guarantee.

**Blindness rule:** subagents **return** their output as their final message (they do NOT write
files, and the run prompt forbids reading sibling `bt*`/`rt*` outputs), so nothing a sibling ran
is ever on disk for another to read. The orchestrator writes every raw output to disk itself,
**before** diffing (capture-first).

**Commit constraint:** the Cowork sandbox mount denies `unlink`/`rename`, so the orchestrator
**cannot `git commit`**. Every raw output is written to `docs/plans/wwf5d/round2/` (durable on
Sean's disk — that IS the preservation guarantee). Commit commands are handed to Sean (§Commit
handoff). Distillation into WWF5D can finish on Opus later regardless.

---

## Pre-flight (once)

- [x] `mkdir -p docs/plans/wwf5d/round2` (done)
- [x] Scope design + shared inputs written (`2026-07-05-round2-scope-design.md`, `rt1-preserve-session-findings.md`, this battery + driver)
- [ ] Confirm the `Agent` tool accepts `model:"fable"` and `model:"opus"` (it does — proven in the Step-1 eye-check)
- [ ] Open `docs/plans/wwf5d/fable-learnings-log.md` mentally as the running log (append standouts as you go)

---

## Per task — run RT1, then RT2, then RT3 (each is one self-contained cycle)

For task `RT{n}`:

- [ ] **Dispatch the pair, in parallel (one message, two `Agent` calls):**
  - `Agent(subagent_type:"general-purpose", model:"opus",  prompt: <RT{n} run prompt, verbatim from the battery>)`
  - `Agent(subagent_type:"general-purpose", model:"fable", prompt: <RT{n} run prompt, verbatim — identical>)`
  - (RT3 note: the run prompt names web + animation tooling as *available*; do not add "please research" — proactive use is the measured variable.)
- [ ] **Capture-first — write both raw outputs to disk immediately, before any analysis:**
  - baseline → `docs/plans/wwf5d/round2/rt{n}-opus.md`
  - blind → `docs/plans/wwf5d/round2/rt{n}-fable.md`
  - (Prefix each file with a one-line provenance header: task, model, date.)
- [ ] **Diff** (orchestrator, one shared analysis context is fine — analysis, not a blind run): compare the two against the premium lenses (spec-decidedness · breadth · contract-contradiction · evidence-discipline/verify-the-world), tag each real delta `dangerously-wrong`/`structural`/`minor` + direction FABLE+/OPUS+, ignore style → write `docs/plans/wwf5d/round2/rt{n}-diff.md`.
  - RT2 extra: record in the diff whether Fable caught the existence-check / false-safety class, or its BT1 blind spot recurred.
- [ ] **Append standouts** to `docs/plans/wwf5d/fable-learnings-log.md` (one row per notable delta; tags `strength`/`surprise`/`ceiling`/`cheap-on-opus`).
- [ ] Surface a one-paragraph read of the pair to Sean before moving on (his eye is the arbiter).

---

## After all three pairs — fold + extract (Opus; costs zero Fable time)

- [ ] Fold **corroborated** deltas into `.claude/skills/wwf5d/SKILL.md` §1–6 (new items or refinements of existing ones) + the evidence index. Hard rule: a move enters ONLY if a diff shows Fable did it and Opus didn't (F1); write abstracted recipes, never transcripts (F2). Note any ceiling (F3) for §7 / Step 4.
- [ ] Extract the deliverables Sean asked for:
  - RT1 → the winning preserve-session fix spec (Fable's if it wins the diff, else the reconciled best) → keep in `rt1-fable.md`/`rt1-opus.md`; note which is canonical.
  - RT3 → the winning enhancement spec → `docs/plans/wwf5d/round2/portfolio-explainer-enhancement-spec.md`.
- [ ] Hand RT2's run prompt to Step 4's validation battery (Opus-with-WWF5D vs without, to measure §2.4 efficacy for the deployment models).

---

## If the Fable window closes early

Capture beats distill — raw Fable output can't be regenerated; distillation finishes on Opus.
Priority order, banking each to disk as you go: `rt1-fable.md` → `rt2-fable.md` → `rt3-fable.md`
(the blind Fable runs first), then the matched `rt{n}-opus.md` baselines (Opus is always
available), then diffs → fold → extract. If only one Fable run fits, run **RT1** (the cleanest
single-axis spec-decidedness read).

---

## Commit handoff (Sean runs these on his machine — the sandbox can't commit)

```bash
cd ~/Code-Brain/code-brain
rm -f .git/index.lock                 # clears the stale lock from the sandbox's failed commit
git add docs/plans/wwf5d/eye-check/ docs/plans/wwf5d/round2/ .claude/skills/wwf5d/SKILL.md docs/plans/wwf5d/fable-learnings-log.md
git commit -m "feat(wwf5d): Round 2 — eye-check, scope+battery+driver, paired RT1-RT3 runs, folded deltas"
```
(Run after the batch; adjust the message per what actually landed. `SKILL.md` + the learnings log only if they changed.)
