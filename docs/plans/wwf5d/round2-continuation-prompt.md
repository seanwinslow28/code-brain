# Fable 5 Campaign — Round 2 Continuation Prompt (fresh Cowork session)

**How to use:** open a fresh Cowork session and paste: *"Read and execute
`docs/plans/wwf5d/round2-continuation-prompt.md` in the code-brain repo."* This file is
self-contained — you (the fresh session) need none of the prior conversation.

---

## Who you are and what this is

You are picking up the **Fable 5 campaign** for Sean, a PM deep in agentic engineering.
Fable 5 is Anthropic's scarce, expensive, soon-to-expire flagship model. The campaign's bet:
spend Fable only on what *only Fable* can do, and capture its edge into durable artifacts that
outlive it. The crown jewel is **WWF5D ("What Would Fable 5 Do")** — a portable skill
(`.claude/skills/wwf5d/SKILL.md`) that distills Fable's *observed* cognition into abstracted
recipes so cheaper models (Opus/Sonnet) behave more Fable-like.

**Status:** Phase A (Opus prep) and Phase B (the Fable burn) are DONE and merged.
WWF5D §1–6 are filled from corroborated behavioral diffs; **§7 (validation) is still open.**
Fable is **still available for a few more days** — so there is a live window for more
Fable-only work before it's gone.

**The single most important finding from Phase B** (from the run's diffs): Fable's premium is
**evidence-discipline** (verify the world before asserting), **breadth past the named seams**,
**spec-decidedness**, and **contract-contradiction detection**. The plain diagnosis / zoom-out
loop is **cheap-on-Opus** (Opus matched it twice) — do NOT spend Fable there. This scopes
everything below.

## Your mission: run this exact 4-step sequence, in order

> **Why this order (the logic to preserve):** validation costs *zero Fable time* (it's
> Opus + council, runnable any day after Fable's gone), while Round 2 can *only* happen while
> Fable is here. So we do the Fable-only work now and validate once at the end. The eye-check
> is a cheap hedge that de-risks the premise before spending the scarce resource.

### Step 1 — Quick eye-check (Opus only; no Fable, no council; ~minutes)

Cheaply confirm WWF5D actually lifts Opus before committing Fable to Round 2.
- Pick ONE small, self-contained audit-or-root-cause task (e.g., a `skill-audit` on a small
  skill, or a quick `zoom-out-and-think`-style read of a small subsystem).
- Dispatch **two Opus subagents** on the identical task: one **with** `wwf5d` loaded in its
  context, one **without**. Diff the two outputs.
- Judge against the run's own yardstick: does the with-WWF5D output exhibit the premium moves
  Opus-without lacks — verify-the-world, breadth past the named seams, existence-checking
  "enforced via X" claims, spec-decidedness? Surface both to Sean; **his eye is the call.**
- **Gate:** visibly helps → proceed to Step 2. Looks like a placebo → STOP, tell Sean, and
  recommend running the formal validation (Step 4) *first* instead of Round 2.
- This is a gut-check, not the formal validation — say so honestly.

### Step 2 — Scope Round 2 (tight brainstorm → plan; Opus)

Use **`superpowers:brainstorming`** to scope Round 2 against Fable's proven premium + the
**Round 2 parking lot** in the learnings log. Do NOT re-litigate settled decisions — the
inputs are rich; keep it tight. The three parked candidates:
1. **Paired same-day subagent runs** — `model=opus` baseline + `model=fable` blind, from one
   orchestrator over a shared tree snapshot (kills pin-drift). This is the proven Phase B
   mechanism (see below).
2. **Targeted round-2 introspection** — re-run only the hypotheses the Phase-B diffs *couldn't*
   test (deliverable-shape grounding; research triggers; second-occurrence fix-shape), with
   tasks designed to exercise them.
3. **Ceiling probes** — design a task around the false-sense-of-safety seams Fable *missed* in
   BT1 (enforcement existence-check; write-path trigger), to measure whether WWF5D §2 now
   closes the gap for both models.

**Hard scoping rule:** every Round 2 task must exercise Fable's *premium* (spec end, breadth,
contract-contradiction, evidence-discipline). Do not spend Fable on plain diagnosis/zoom-out
loops — that's cheap-on-Opus and wastes the window.

Then use **`superpowers:writing-plans`** to turn the scope into a Round 2 **task battery +
session driver**, mirroring `task-battery.md` + `fable-session-driver.md` (pinned inputs,
self-contained run-prompts, blind-run discipline, capture-first). Save under
`docs/plans/wwf5d/round2/`.

### Step 3 — Drive Round 2 on Fable (Cowork, via `model=fable` subagents)

Execute the Round 2 battery using the **proven Phase B protocol**: the orchestrator (you, Opus)
holds the analysis; each blind run is a **fresh subagent dispatched with `model: "fable"`**
receiving the pinned prompt verbatim, seeing neither the baselines nor the other runs. Generate
matched Opus baselines with **`model: "opus"`** subagents on the same tree snapshot (the paired
pattern — kills pin-drift). Discipline carried from Phase B:
- **Capture before you distill** — save every raw Fable output to `docs/plans/wwf5d/round2/`
  and commit *before* folding anything into WWF5D. Raw Fable output can't be regenerated once
  it's gone; distillation can finish on Opus later.
- **F1** — self-report is a hypothesis; only a behavioral delta earns a place in WWF5D.
- **F2** — WWF5D holds abstracted recipes, never transcripts.
- Append notable moments to `fable-learnings-log.md` (the running log) as you go.
- Fold corroborated Round 2 deltas into WWF5D (new/《refined》 §1–6 items + the evidence index).

### Step 4 — One council validation on the FINAL WWF5D (Opus + council; zero Fable budget)

After Round 2 is folded in, run the validation once on the finished skill, per
`validation-harness.md`:
- Compare **Opus-with-WWF5D vs the Opus-without baselines** on the battery tasks (the artifact
  being judged is the *transfer*, not Fable's work).
- Judge with the **cross-family LLM Council** (`.claude/skills/llm-council` + `tools/llm-council/`),
  **order-swapped**, **length-controlled**, **NOT Opus-led** (self-preference is causal), κ-gated
  to ~10 Sean labels (reuse the anima Em protocol: N=5 majority, reference-blind). **Sean's eye
  is the final call.**
- Write the result into **WWF5D §7** (the honest ceiling: what ported, what didn't — F3).
- Note: the council step needs API keys / Sean's infra; if unavailable in Cowork, prep it
  turnkey and hand off, or fall back to a Sean-eye-only pass and mark §7 accordingly.

## Context files — read these first, in this order

1. `CLAUDE.md` (repo root) — project rules (privacy layer, hooks, domains).
2. `docs/plans/wwf5d/fable-learnings-log.md` — **the richest context**: the run's premium /
   ceilings / cheap-on-Opus findings, the protocol note, and the Round 2 parking lot.
3. `docs/plans/2026-07-04-fable5-audit-campaign.md` — the campaign (3-phase spine, budget logic).
4. `docs/plans/2026-07-04-wwf5d-research-findings.md` — the four method constraints **F1–F4**
   (self-report unreliable; recipes-not-transcripts; partial transfer; de-biased judge).
5. `.claude/skills/wwf5d/SKILL.md` — the built skill (§1–6 filled + evidence index; §7 open).
6. `docs/plans/wwf5d/phase-b-fable-runbook.md` + `fable-session-driver.md` — the Phase B
   runbook + literal driver; **templates to mirror for Round 2**.
7. `docs/plans/wwf5d/task-battery.md` — the pinned battery format to mirror.
8. `docs/plans/wwf5d/introspection-protocol.md` — the 7 introspection questions.
9. `docs/plans/wwf5d/validation-harness.md` — the Step-4 design.
10. `docs/plans/wwf5d/fable-runs/` (raw: introspection + bt{1,2,3,5}-fable + diffs) and
    `docs/plans/wwf5d/baselines/` (Opus-without baselines) — the Phase B evidence.
11. `docs/plans/wwf5d/tier1-specs/` — the elevated-skill draft specs (for reference).

## The Fable-run mechanism (proven in Phase B — reuse it)

The `Agent` tool accepts `model: "fable"`. Phase B ran blind battery tasks as fresh
`model="fable"` subagents (blindness + pinned-input parity held without manual `/clear`), with
matched `model="opus"` baseline subagents on the same tree. That's the Round 2 mechanism —
paired subagents from one orchestrator, shared tree snapshot, no pin-drift.

## Guardrails (carry all of these)

- **F1–F4** as above (they're the method's spine).
- **Target Fable's premium, not cheap-on-Opus work** (the run's central lesson).
- **Fleet-ops:** any costed run bills the **subscription / OAuth, never `ANTHROPIC_API_KEY`**.
- **Privacy layer (CLAUDE.md):** never `git add` private paths; never write real
  income/medical/contact/employer data into tracked files; `writing-voice-modes`/
  `personal-finance`/`life-admin` edit public `SKILL.md` only.
- **Capture-first**, commit as you go; if the Fable window closes early, bank raw + distill later.

## Out of scope this session (do NOT wander into these)

- **The Mac Mini BT5 fleet fix** — `docs/plans/wwf5d/bt5-mac-mini-fix-prompt.md`, runs on the
  Mac Mini later (agents live there), with two owner forks for Sean.
- **Phase C implementation** of the `anima-register-seam-spec.md` and `creative-chain-spec.md`
  (deferred; anima work is a separate repo/session).
- **The elevated-skill deferred tickets** in `vault/00_inbox/tickets.md` (paired MCP change,
  reference-file halves, claude-mastery drift) — separate cleanups.

## Skills you'll use (Cowork)

- **`superpowers:brainstorming`** — Step 2, to scope Round 2 (the regroup trigger mandates it).
- **`superpowers:writing-plans`** — Step 2, to produce the Round 2 battery + driver.
- **`wwf5d`** (`.claude/skills/wwf5d`) — load it for the Step 1 eye-check (the with-WWF5D arm)
  and for Round 2 orchestration.
- **`llm-council`** (`.claude/skills/llm-council`) — Step 4 validation.
- **`skill-audit`** / **`zoom-out-and-think`** — the harnesses for eye-check + Round 2 tasks.
- Optional: **`honest-thinking-partner`** or **`grilling`** to pressure-test the Round 2 scope
  before committing Fable to it.
- Cowork will manage the task list and use `AskUserQuestion` for the genuinely-Sean decisions
  (which Round 2 candidates, the eye-check target, the validation go/no-go).

## First actions for the fresh session

1. Read the context files (order above); set up a task list for the 4 steps.
2. Propose the Step-1 eye-check target to Sean (one small task), then run it and show him both
   arms.
3. On his green-light, move to Step 2 (`brainstorming`) — and keep the scarcity logic in view:
   Fable-only work now, validation last.
