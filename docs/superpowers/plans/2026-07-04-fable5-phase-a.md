# Fable 5 Campaign — Phase A Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce the Opus/Sonnet "warm-start" artifacts so that when Sean switches to Fable 5, its scarce cycles go straight to irreplaceable reasoning — not inventory, drafting, or setup.

**Architecture:** Assemble two audit tools from Sean's existing meta-skills; triage the 127-skill library into ranked tiers; do the cheap first-pass improvements; and scaffold WWF5D (protocol + task battery + pre-generated Opus baseline traces + validation harness). Everything here runs on Opus 4.8 / Sonnet 5.0. Phase B (Fable, human-in-the-loop) and Phase C (Opus harvest) are staged as runbooks, not executed here.

**Tech Stack:** Claude Code in the `code-brain` repo · `.claude/skills/<name>/SKILL.md` authoring (YAML frontmatter + markdown body) · `python3 scripts/validate.py` (skill/structure validator) · existing skills `skill-system-mastery`, `intent-engineering`, `systematic-debugging`, `plan-and-think`, `intended-vs-implemented`, `writing-critique`, `decision-doc`, `llm-council` · the anima Em calibration protocol (reference only).

---

## Required reading (do this before Task 0)

Read these two committed docs — they carry the full rationale and the hard constraints this plan assumes. Do not re-derive them.

1. `docs/plans/2026-07-04-fable5-audit-campaign.md` — the campaign (3-phase spine, 40/30/30 Fable budget, forks resolved, guardrails).
2. `docs/plans/2026-07-04-wwf5d-research-findings.md` — the four method constraints on WWF5D (cited).

**The four WWF5D constraints (load-bearing — repeated so you can't miss them):**
- **F1.** A model's self-report of its own reasoning is unreliable → Fable's introspection output is a *hypothesis*, and only enters WWF5D if a behavioral delta (Fable-vs-Opus) corroborates it.
- **F2.** Only *abstracted recipes* transfer via prompting → WWF5D encodes procedures/checklists/rubrics/templates, never raw Fable transcripts. Copy the recipe, not the trace.
- **F3.** There is a real ceiling → expect *partial* transfer; validation decides per-move; document what didn't port.
- **F4.** De-bias the validation judge → order-swapped, length-controlled, cross-family panel (never Opus-led when the artifacts are Opus-authored), κ ≥ 0.6 against a few Sean labels, Sean's eye as final call.

## Scope

**This plan is Phase A only.** It produces standalone, verifiable artifacts. Phase B (Fable) and Phase C (harvest) are delivered as runbooks in Task 8 — they require Fable access and Sean in the loop, so they are not executable tasks here.

## Privacy guardrail (applies to every task)

`code-brain` is a public repo with a hard private layer. Never `git add` private-layer paths; never weaken `.gitignore`; never write real income/medical/contact/employer data into tracked files. When auditing/improving `writing-voice-modes`, `personal-finance`, or `life-admin`, edit the public `SKILL.md` only — never the local-only `references/` or `drafts/`.

## File structure (created/modified by this plan)

- Create: `.claude/skills/skill-audit/SKILL.md` — the grounded skill auditor
- Create: `.claude/skills/zoom-out-and-think/SKILL.md` — the root-cause oracle
- Create: `.claude/skills/wwf5d/SKILL.md` — WWF5D scaffold (sections empty, filled by Fable in Phase B)
- Create: `docs/plans/2026-07-04-fable5-skill-triage.md` — the 127-skill triage table + rubric
- Create: `docs/plans/wwf5d/introspection-protocol.md` — the fixed Fable question set
- Create: `docs/plans/wwf5d/task-battery.md` — the 3–5 diff tasks
- Create: `docs/plans/wwf5d/baselines/<task-id>-opus.md` — pre-generated Opus traces (one per battery task)
- Create: `docs/plans/wwf5d/validation-harness.md` — the held-out A/B design
- Create: `docs/plans/wwf5d/tier1-specs/<skill>.md` — Opus draft improvement specs for the Tier-1 five
- Create: `docs/plans/wwf5d/phase-b-fable-runbook.md` — the steps Sean runs on Fable
- Modify: `CHANGELOG.md` — one entry at the top of `## [Unreleased]`

---

### Task 0: Isolate the work + orient

**Files:**
- Create: none (branch/worktree setup)

- [ ] **Step 1: Create an isolated branch off a clean base**

The current branch `feat/discovery-e1-loose-ends` has unrelated uncommitted work. Do not build on top of it.

Run:
```bash
cd /Users/seanwinslow/Code-Brain/code-brain
git stash list   # note anything already stashed; do not disturb it
git checkout main && git pull --ff-only
git checkout -b feat/fable5-campaign
```
Expected: on a fresh `feat/fable5-campaign` branch, clean tree.

- [ ] **Step 2: Read the spec + research docs**

Read `docs/plans/2026-07-04-fable5-audit-campaign.md` and `docs/plans/2026-07-04-wwf5d-research-findings.md` in full. Internalize constraints F1–F4.

- [ ] **Step 3: Confirm the toolchain**

Run:
```bash
python3 scripts/validate.py
ls .claude/skills | wc -l
```
Expected: validator passes; skill count is printed (the "127" is approximate — use the real number as your triage denominator).

- [ ] **Step 4: Commit the orientation marker (empty scaffold dirs)**

```bash
mkdir -p docs/plans/wwf5d/baselines docs/plans/wwf5d/tier1-specs
git add docs/plans/wwf5d/.gitkeep 2>/dev/null; touch docs/plans/wwf5d/.gitkeep
git add docs/plans/wwf5d/.gitkeep
git commit -m "chore(fable5): scaffold Phase A working dirs"
```

---

### Task 1: Build the `skill-audit` harness skill

**Files:**
- Create: `.claude/skills/skill-audit/SKILL.md`

- [ ] **Step 1: Author the skill using `skill-system-mastery` conventions**

Invoke `skill-system-mastery` to match your repo's SKILL.md format. The frontmatter (use verbatim):

```yaml
---
name: skill-audit
description: Audit a Claude Code skill for downstream-intent seams, missing tool/handoff adapters, and "works-but-never-wows" gaps. Grounds itself with clarifying questions FIRST, then emits a seam report plus an intent-carrying improvement spec. Use to dial in a daily-driver skill, or to spec how to improve one.
---
```

The body MUST contain these sections, with this exact behavior (this is the content, not a placeholder — write it out):

1. **Ground first (hard gate).** Before auditing, ask the user: (a) what this skill is *for* and who relies on it; (b) which downstream skills/tools it feeds; (c) where it "sometimes disappoints"; (d) what a "wow" output would look like. Do not audit until answered.
2. **Seam scan.** Trace every input the skill builds (brand voice, criteria, design specifics, references) and check whether it survives into every later phase/handoff. Report each place a decided input fails to travel downstream.
3. **Adapter scan.** Check whether the skill hands off to downstream tools in *each tool's* required format (e.g., Claude-design vs Figma vs Stitch vs a generator). Flag missing adapter/format-conversion steps.
4. **Wow-gap scan.** Identify where the skill produces "correct but forgettable" output and name the specific missing move that would push it to memorable.
5. **Output.** Emit two artifacts: a **seam report** (bulleted findings, each tagged `dangerously-wrong | structural | minor`) and an **intent-carrying improvement spec** (authored via `intent-engineering` scaffolding) that a lesser model can implement without losing the "why."

Add a one-line provenance note in the body: "Assembled from skill-system-mastery + intent-engineering + writing-critique's single-highest-leverage-fix pattern."

- [ ] **Step 2: Verify structure**

Run:
```bash
python3 scripts/validate.py
```
Expected: passes with `skill-audit` recognized.

- [ ] **Step 3: Smoke-test the skill on a throwaway target**

In a scratch prompt, invoke `skill-audit` against a small existing skill (e.g., `commit-checklist`). Confirm it (a) asks the four grounding questions before auditing, and (b) emits both the seam report and the intent-carrying spec.
Expected: grounding questions appear first; both artifacts produced.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/skill-audit/SKILL.md
git commit -m "feat(fable5): add skill-audit harness skill"
```

---

### Task 2: Build the `zoom-out-and-think` harness skill

**Files:**
- Create: `.claude/skills/zoom-out-and-think/SKILL.md`

- [ ] **Step 1: Author the skill**

Frontmatter (verbatim):

```yaml
---
name: zoom-out-and-think
description: System-level root-cause oracle for a codebase or subsystem stuck in repeated band-aid patches. Reads the whole subsystem, researches current best practice for the domain, names the root cause instead of the symptom, and emits an intent-carrying spec for a lesser model to implement. Use when the same class of bug keeps recurring.
---
```

Body sections (write them out):

1. **Ground first (hard gate).** Ask: (a) what keeps recurring; (b) what's been tried; (c) what "coherent/correct" looks like end-to-end. Do not diagnose until answered.
2. **Read the whole system.** Map how the subsystem actually works (state, control flow, where orchestration lives) before touching any single bug. Reference `intended-vs-implemented` to compare documented intent vs live behavior.
3. **Research current best practice.** Web-search the modern best practice for this specific domain/pattern; ground the diagnosis in it (cite sources).
4. **Name the root cause, refuse the symptom.** State the single system-level cause. Explicitly resist proposing another patch; if a proposed fix is a band-aid, say so.
5. **Output.** An intent-carrying spec: the real ask, the root cause, and the change — carrying motivational intent + all critical details so a lesser model (Opus) implements it without drift.

Provenance note: "Assembled from systematic-debugging + plan-and-think + intended-vs-implemented."

- [ ] **Step 2: Verify structure**

Run: `python3 scripts/validate.py`
Expected: passes with `zoom-out-and-think` recognized.

- [ ] **Step 3: Smoke-test**

Invoke `zoom-out-and-think` on a small real recurring annoyance (any). Confirm it grounds, maps the system, researches, and names a root cause rather than a patch.

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/zoom-out-and-think/SKILL.md
git commit -m "feat(fable5): add zoom-out-and-think root-cause skill"
```

---

### Task 3: Triage the full skill library into tiers

**Files:**
- Create: `docs/plans/2026-07-04-fable5-skill-triage.md`

- [ ] **Step 1: Inventory every skill**

Run:
```bash
for d in .claude/skills/*/; do
  name=$(basename "$d")
  desc=$(grep -m1 '^description:' "$d/SKILL.md" 2>/dev/null | sed 's/^description: *//')
  echo "| $name | ${desc:-(no description)} | | | | |"
done
```
This prints one table row per skill.

- [ ] **Step 2: Write the triage doc with the scoring rubric**

Create `docs/plans/2026-07-04-fable5-skill-triage.md`. Header + rubric:

```markdown
# Fable 5 — Skill Triage (2026-07-04)

Score each skill 1–5 on three axes, then assign a tier.
- **Frequency** — how often Sean actually uses it.
- **Leverage** — how much its quality gates other work (meta-skills score high).
- **Wow-gap** — how far today's output is from "wow" (5 = often disappoints).

Priority = Frequency + Leverage + Wow-gap.

- **Tier 1 (Fable elevates — LOCKED 5):** writing-voice-modes, intent-engineering, skill-system-mastery, plan-and-think, systematic-debugging.
- **Tier 2 (Opus improves now):** high priority, improvable on the cheap model this window.
- **Tier 3 (spec-only / leave):** low frequency or niche — draft an improvement spec, no edit this window.

| Skill | Description | Freq | Lev | Wow-gap | Tier |
|---|---|---|---|---|---|
<!-- paste rows from Step 1, fill scores -->
```

Paste the Step-1 rows and fill in scores. The five Tier-1 skills are fixed; assign every other skill to Tier 2 or Tier 3.

- [ ] **Step 3: Verify completeness**

Run:
```bash
# every skill dir should appear exactly once in the table
comm -23 <(ls .claude/skills | sort) <(grep -oE '^\| [a-z0-9-]+ ' docs/plans/2026-07-04-fable5-skill-triage.md | tr -d '| ' | sort)
```
Expected: no output (every skill is triaged). The five Tier-1 rows match the locked set.

- [ ] **Step 4: Commit**

```bash
git add docs/plans/2026-07-04-fable5-skill-triage.md
git commit -m "docs(fable5): triage skill library into tiers"
```

---

### Task 4: Opus first-pass — improve Tier-2, draft Tier-1 specs

**Files:**
- Modify: `.claude/skills/<tier-2 skill>/SKILL.md` (one per Tier-2 skill)
- Create: `docs/plans/wwf5d/tier1-specs/<skill>.md` (one per Tier-1 skill)

- [ ] **Step 1: Improve each Tier-2 skill (loop)**

For each Tier-2 skill, in priority order: invoke `skill-audit` on it, apply the improvement directly to its `SKILL.md`, run `python3 scripts/validate.py`, and commit per skill:
```bash
git add .claude/skills/<skill>/SKILL.md
git commit -m "feat(fable5): improve <skill> (Opus first-pass)"
```
Privacy: for `writing-voice-modes`/`personal-finance`/`life-admin`, edit the public `SKILL.md` only — never `references/` or `drafts/`.

- [ ] **Step 2: Draft an improvement spec for each Tier-1 skill**

For each of the five Tier-1 skills, run `skill-audit` and save its intent-carrying spec (do NOT edit the skill — Fable elevates it in Phase B) to `docs/plans/wwf5d/tier1-specs/<skill>.md`. The spec is a *strong draft* so Fable elevates rather than drafts from scratch.

- [ ] **Step 3: Verify**

Run: `python3 scripts/validate.py`
Expected: passes. Confirm five files exist under `docs/plans/wwf5d/tier1-specs/`.

- [ ] **Step 4: Commit the Tier-1 specs**

```bash
git add docs/plans/wwf5d/tier1-specs/
git commit -m "docs(fable5): draft Tier-1 improvement specs for Fable to elevate"
```

---

### Task 5: WWF5D introspection protocol

**Files:**
- Create: `docs/plans/wwf5d/introspection-protocol.md`

- [ ] **Step 1: Write the fixed question set**

Create the file with these exact questions (constraint F1 caveat included):

```markdown
# WWF5D — Fable Introspection Protocol

> Output is a set of HYPOTHESES about Fable's cognition, NOT ground truth (constraint F1).
> No answer here enters WWF5D unless a behavioral delta in the battery corroborates it.

Ask Fable, one at a time:
1. Grounding — Before acting on a task, what do you establish about context and intent, and how? What do you ask?
2. Intent preservation — How do you keep the user's motivational intent intact across multi-step work and handoffs? Where does intent typically get lost?
3. Seam detection — Auditing a multi-phase system, how do you find where a decided input fails to travel downstream?
4. Root cause — How do you tell a symptom from a system-level root cause? What makes you zoom out instead of patch?
5. Triage — How do you decide dangerously-wrong vs structural vs minor?
6. Research trigger — When and why do you proactively stop to research best practice mid-task?
7. Spec authoring — Writing a spec for a weaker model to implement, what do you include so intent and critical detail survive?
```

- [ ] **Step 2: Verify**

Confirm the file covers all four cognition dimensions (grounding, intent-preservation/seams, root-cause, triage) and carries the F1 caveat at top.

- [ ] **Step 3: Commit**

```bash
git add docs/plans/wwf5d/introspection-protocol.md
git commit -m "docs(fable5): WWF5D introspection protocol"
```

---

### Task 6: WWF5D task battery + pre-generated Opus baselines

**Files:**
- Create: `docs/plans/wwf5d/task-battery.md`
- Create: `docs/plans/wwf5d/baselines/<task-id>-opus.md` (one per battery task run)

- [ ] **Step 1: Define the battery**

Create `docs/plans/wwf5d/task-battery.md`. Core three (must-run) + two optional:

```markdown
# WWF5D — Task Battery (Fable-vs-Opus diff)

Each task lists matched, reproducible inputs so Fable and Opus get identical context.

CORE (run all three):
- BT1 — skill-audit on `intent-engineering`. Input: .claude/skills/intent-engineering/SKILL.md.
- BT2 — zoom-out-and-think on anima's register-transport / per-register model-routing seam. Input: the anima register docs + the 2026-07-04 register-transport field report.
- BT3 — creative-chain seam audit (double duty). Input: the writing chain — storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass. Find where taste/intent leaks between stages.

OPTIONAL (run if the window holds):
- BT4 — author a PRD/tech-spec for a defined feature (pick one real backlog item).
- BT5 — systematic-debugging root-cause on one real recurring bug.
```

- [ ] **Step 2: Generate the Opus baseline for each core task NOW**

For BT1, BT2, BT3: run the task on Opus 4.8 in this session and save the full output to `docs/plans/wwf5d/baselines/<task-id>-opus.md` (e.g., `bt1-opus.md`). This is the efficiency multiplier — Fable only adds its half + the critique in Phase B.

- [ ] **Step 3: Verify**

Run:
```bash
ls docs/plans/wwf5d/baselines/
```
Expected: `bt1-opus.md`, `bt2-opus.md`, `bt3-opus.md` present and non-empty; each records the exact inputs used (so Fable's run is matched).

- [ ] **Step 4: Commit**

```bash
git add docs/plans/wwf5d/task-battery.md docs/plans/wwf5d/baselines/
git commit -m "docs(fable5): WWF5D battery + pre-generated Opus baselines"
```

---

### Task 7: WWF5D skill scaffold + validation harness

**Files:**
- Create: `.claude/skills/wwf5d/SKILL.md`
- Create: `docs/plans/wwf5d/validation-harness.md`

- [ ] **Step 1: Scaffold the WWF5D skill (sections empty, filled by Fable)**

Frontmatter (verbatim):
```yaml
---
name: wwf5d
description: What Would Fable-5 Do — portable recipes distilled from Fable 5's OBSERVED cognition (grounding, seam-catching, root-cause, intent-preserving triage and spec-writing) so Opus/Sonnet behave more Fable-like. Load as standing context for planning, auditing, and spec work.
---
```
Body: create the section skeleton below with a one-line note in each that it is filled in Phase B from *corroborated* moves only (constraints F1/F2). Do not invent content — these are filled by Fable.

```markdown
> BUILD RULE (F2): each section holds an ABSTRACTED RECIPE (procedure/checklist/rubric/template), never a Fable transcript.
> BUILD RULE (F1): a move appears here only if a battery behavioral delta corroborated it.

## 1. Grounding protocol
## 2. Seam / handoff checklist
## 3. Root-cause ("zoom out") procedure
## 4. Triage rubric (dangerously-wrong / structural / minor)
## 5. Handoff / tool-adapter pattern
## 6. Intent-preserving spec template
## 7. Known ceiling — what did NOT transfer (from validation)
```

- [ ] **Step 2: Write the validation harness spec**

Create `docs/plans/wwf5d/validation-harness.md`:

```markdown
# WWF5D — Validation Harness (held-out A/B)

For each battery task, compare Opus-with-WWF5D vs the saved Opus baseline.

Judge design (constraint F4):
- Order-swapped: run each comparison twice with A/B order flipped; a win counts only if it holds both ways, else tie.
- Length-controlled: do not let the longer answer win by default.
- Cross-family panel, NOT Opus-led (self-preference is causal): use the LLM Council `variance`/cross-family profile; the chairman must not be the author's family.
- Calibrate to ~10 Sean labels with Cohen's κ (target ≥ 0.6). Reuse the anima Em protocol (N=5 majority, reference-blind).
- Sean's eye is the Engine-Truth final call.

Success = WWF5D-Opus beats baseline on the core battery, κ-gated, with a written transfer analysis (what ported / what hit the F3 ceiling → Section 7 of the skill).
```

- [ ] **Step 3: Verify**

Run: `python3 scripts/validate.py`
Expected: passes; `wwf5d` recognized (scaffold is valid even with empty sections).

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/wwf5d/SKILL.md docs/plans/wwf5d/validation-harness.md
git commit -m "feat(fable5): WWF5D scaffold + validation harness spec"
```

---

### Task 8: Phase B runbook + closeout

**Files:**
- Create: `docs/plans/wwf5d/phase-b-fable-runbook.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Write the Fable runbook (what Sean drives)**

Create `docs/plans/wwf5d/phase-b-fable-runbook.md`:

```markdown
# Phase B — Fable Runbook (Sean drives, budget order)

Switch model: `/model fable`. Ground every run first (no cold kickoffs).

1. WWF5D deep dive (40%)
   - Run introspection-protocol.md → capture hypotheses.
   - Run the core battery (BT1–BT3) on Fable; Fable critiques each saved Opus baseline, tagged dangerously-wrong/structural/minor.
   - Co-author .claude/skills/wwf5d/SKILL.md — corroborated moves only (F1), recipes not transcripts (F2).
   - Validate per validation-harness.md; write Section 7 (the ceiling, F3).
2. Tier-1 audits (30%)
   - For each of the five Tier-1 skills, run skill-audit from its docs/plans/wwf5d/tier1-specs/<skill>.md draft; Fable elevates to "wow." Public SKILL.md only.
3. anima register-seam (30%)
   - Run zoom-out-and-think on the register-routing seam; Fable writes the intent-carrying spec. Implementation deferred to Opus (Phase C).
```

- [ ] **Step 2: Add the CHANGELOG entry**

At the very top of the `## [Unreleased]` section in `CHANGELOG.md`, add:

```markdown
### Fable 5 audit campaign — Phase A prep (2026-07-04)
- **Fable 5 campaign scaffolding.** Added the campaign + research-grounding docs
  (`docs/plans/2026-07-04-fable5-audit-campaign.md`, `-wwf5d-research-findings.md`),
  two audit-harness skills (`skill-audit`, `zoom-out-and-think`), the skill triage,
  and the WWF5D scaffold (introspection protocol, task battery + Opus baselines,
  validation harness, Phase B runbook). Phase A (Opus/Sonnet prep) only; Phase B
  runs on Fable per the runbook. WWF5D encodes abstracted recipes corroborated by
  behavioral diffs, never raw transcripts.
```

- [ ] **Step 3: Final verification**

Run:
```bash
python3 scripts/validate.py
ls .claude/skills/skill-audit .claude/skills/zoom-out-and-think .claude/skills/wwf5d
ls docs/plans/wwf5d docs/plans/wwf5d/baselines docs/plans/wwf5d/tier1-specs
```
Expected: validator green; all three skills present; all WWF5D artifacts present.

- [ ] **Step 4: Commit + open PR (or hand back to Sean)**

```bash
git add CHANGELOG.md docs/plans/wwf5d/phase-b-fable-runbook.md
git commit -m "docs(fable5): Phase B runbook + CHANGELOG; close Phase A prep"
git push -u origin feat/fable5-campaign
```
Then tell Sean Phase A is complete and the Fable runbook is ready to drive.

---

## Self-Review (completed by plan author)

- **Spec coverage:** Every campaign-doc element maps to a task — harness (T1–T2), triage (T3), Opus first-pass + Tier-1 specs (T4), WWF5D introspection/battery/baselines/scaffold/validation (T5–T7), creative-chain audit (BT3 in T6), Phase B handoff (T8). Constraints F1–F4 are embedded in T5/T6/T7.
- **Placeholder scan:** Skill *bodies* are specified by enumerated required sections + exact rules (not vague "add X"); frontmatter is verbatim. WWF5D section bodies are intentionally empty — they are filled by Fable in Phase B by design, not a placeholder gap.
- **Consistency:** Tier-1 five identical across campaign doc and T3/T4. Battery IDs (BT1–BT3) consistent across T6, T7 harness, and T8 runbook. Skill names (`skill-audit`, `zoom-out-and-think`, `wwf5d`) consistent throughout.

## Note on adapted TDD

Phase A is skill-authoring + analysis, not app code, so "write the failing test" is replaced by concrete *verification* steps (`validate.py`, structure/inventory checks, smoke-tests). The bite-sized, one-commit-per-unit discipline is preserved.
