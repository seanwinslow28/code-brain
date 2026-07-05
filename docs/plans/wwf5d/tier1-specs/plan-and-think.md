# Tier-1 Improvement Spec (DRAFT): `plan-and-think`

## What this file is

An **Opus first-pass draft spec** produced by running the repo's `skill-audit`
harness against `.claude/skills/plan-and-think/SKILL.md`. **No skill file was
edited.** In Phase B, **Fable 5 elevates this draft** into the applied change — a
strong draft means Fable spends its cycles on the last 20% (exact wording,
picking the right thinking-budget tiers, confirming live settings keys), not on
re-discovering what to fix.

It contains the two `skill-audit` artifacts — a **severity-tagged seam report**
and an **intent-carrying improvement spec** — plus **named open questions** where
I'm uncertain, because a named open question is more useful to Fable than false
confidence.

## Grounding answers used (controller-supplied, as Sean's (a)–(d))

- **(a) For:** Plan Mode vs Extended Thinking mastery in Claude Code. Repo
  CLAUDE.md **Non-Negotiable Rule #1** exists *precisely because* these two keep
  getting confused: Plan Mode = double `Shift+Tab` or `/plan`; Extended Thinking =
  single `Tab` — never confuse them.
- **(b) Feeds:** every planning session; superpowers `writing-plans` workflows;
  `zoom-out-and-think` (references it by name); architecture decisions across all
  projects.
- **(c) Disappoints:** the confusion Rule #1 guards against persists in practice;
  guidance on *when to use which mode* (and *how much thinking budget*) is generic
  rather than mapped to task shapes; unclear what to do when **both** apply.
- **(d) Wow:** the right mode chosen automatically per task shape; thinking budget
  matched to problem depth; the Plan-Mode-vs-Extended-Thinking distinction
  **impossible to get wrong even for a fresh session**.

## Repo evidence checked (per campaign hard-constraint: no harness-behavior claims without repo evidence)

- **`claude-mastery/reference/shortcuts.md` is the repo's canonical shortcut
  reference.** It states:
  - line 18: `` `Tab` `` = "Extended Thinking toggle — **Sticky toggle. NOT Plan
    Mode.**" (this is the *primary* toggle, and the one CLAUDE.md Rule #1 names)
  - line 19: `` `Alt+T` / `Option+T` `` = "Extended Thinking toggle — **Alternative
    to Tab**"
  - line 20: `` `Shift+Tab` `` = "Cycle permission modes — Normal > Auto-Accept > Plan"
  - line 13: `` `Ctrl+O` `` = "Toggle verbose mode — Shows tool inputs/outputs and
    **thinking blocks**"
  - line 23: `` `Ctrl+G` `` = "External editor — Opens **prompt** in `$EDITOR`"
  - line 53: `` `/plan` `` = "Enter Plan Mode explicitly"
  - line 117: `` `MAX_THINKING_TOKENS` `` = "Extended thinking budget" (env var)
- **CLAUDE.md Non-Negotiable Rule #1** (line 11): "Plan Mode = double `Shift+Tab`
  or `/plan`. Extended Thinking = single `Tab`. Never confuse the two." This is a
  **Non-Negotiable** and the identifier it uses for Extended Thinking is the single
  `Tab`.
- **The SKILL.md never mentions single `Tab`.** Its comparison table (line 46) and
  its Extended Thinking Activation section (line 80) list Extended Thinking's
  keyboard shortcut as **only** `Option+T (macOS) / Alt+T (Windows/Linux)` — the
  *alternative*, per shortcuts.md line 19 — and omit the primary `Tab` toggle
  entirely. Success Criteria (line 165) repeats "Option+T for Thinking."
- **`alwaysThinkingEnabled` (line 145) and `maxThinkingTokens` (line 146) are
  unverified.** A `grep` across `claude-mastery/`, `.claude/`, and the live
  `~/.claude/settings.json` finds these two settings.json keys **only inside the
  SKILL.md itself** — nowhere authoritative. Only the `MAX_THINKING_TOKENS` **env
  var** (shortcuts.md line 117) and the `/config` toggle are corroborated. Flagged
  as an open question, not asserted true or false.
- **`Ctrl+O` (SKILL line 82) is correct** (shortcuts.md line 13). **`Ctrl+G` (SKILL
  line 100) is imprecise:** shortcuts.md line 23 says it opens the *current prompt
  buffer* in `$EDITOR`, whereas the SKILL frames it as "open the generated plan."
- **Feeds confirmed by grep:** `zoom-out-and-think/SKILL.md` line 25 ("Assembled
  from systematic-debugging + **plan-and-think** + intended-vs-implemented") and
  `claude-mastery/README.md` line 21 (Advanced Techniques list). `writing-plans`
  (superpowers plugin) is a workflow consumer per grounding (b) but does **not**
  reference `plan-and-think` by name in its SKILL.md — treat that feed as a
  workflow relationship, not a by-name dependency.

### Scope notes

- **In scope for a Phase-B SKILL.md edit:** everything in Artifact 2 that is a body
  or frontmatter-description change to `.claude/skills/plan-and-think/SKILL.md`.
- **Bigger calls flagged as open questions, not silently actioned:** verifying the
  two settings.json keys against the live schema; choosing the exact
  thinking-budget token tiers.
- **Privacy:** `plan-and-think` is a public skill with no `references/`/`drafts/`;
  no privacy surface.

---

## Artifact 1 — Seam Report

- `dangerously-wrong` — **The skill teaches the Plan/Thinking distinction while
  omitting the exact `Tab` ↔ `Shift+Tab` adjacency that is the confusion it exists
  to prevent.** In the comparison table (line 46) and Extended Thinking Activation
  (line 80), Extended Thinking's shortcut is given as *only* `Option+T`/`Alt+T`. The
  single `Tab` toggle — which `shortcuts.md` line 18 calls the primary Extended
  Thinking toggle and which **Non-Negotiable Rule #1** uses as *the* identifier for
  Extended Thinking — is never named anywhere in the skill. **What Sean observes:** a
  fresh session reads this skill, builds the mental model "Extended Thinking =
  Option+T, Plan = Shift+Tab" (two shortcuts that look far apart and un-confusable),
  and is left with **no model at all** for what a single `Tab` does — so the one
  keystroke pair that actually collides (`Tab` = think in place vs `Shift+Tab` =
  cycle toward Plan/read-only) is exactly the pair the skill never disambiguates. A
  skill whose stated purpose (line 10) is "correctly use the keyboard shortcuts" and
  prevent this confusion instead reinforces the blind spot, in tension with the
  repo's own Non-Negotiable rule. *Nuance for the implementer:* `Option+T` is **not
  factually wrong** (shortcuts.md line 19 confirms it as a valid alternative) — the
  defect is the **omission** of the canonical `Tab` shortcut and the **un-named
  adjacency**, not a false claim. Tagged `dangerously-wrong` because it produces a
  confident-but-incomplete model on the skill's single most safety-relevant topic.

- `structural` — **"When to Use Each" is three generic bullet lists, not a
  task-shape → mode routing rule (the core (c)/(d) gap).** Lines 118–134 give a "Use
  Plan Mode when," a "Use Extended Thinking when," and a "Use both when" list — all
  correct, all generic. There is no single lookup that maps a *task shape* (explore
  unfamiliar code / stubborn regressing bug / multi-file refactor / quick decision /
  architecture on a large codebase) to the mode(s) it wants. **What Sean observes:** a
  fresh session still has to reason the choice out from scratch each time; the mode
  is *not* "chosen automatically per task shape" (grounding (d)) — the skill informs
  the choice but never makes it fall out of a table.

- `structural` — **Thinking budget is never mapped to problem depth.** The skill
  cites concrete budgets — `MAX_THINKING_TOKENS=20000` (line 86), `maxThinkingTokens:
  16000` (line 146) — but nowhere connects *how deep a problem* to *how large a
  budget*. **What Sean observes:** the token budget is picked by guess or left at
  default; grounding (c) ("how much thinking budget is generic") and (d) ("thinking
  budget matched to problem depth") both go unmet. There's no "shallow decision → low
  or off; stubborn multi-path bug → high" tiering the owner can act on.

- `structural` — **"When both apply" is presented as a heavyweight workflow, not as
  free composition of two orthogonal toggles.** The Deep Architect Workflow (lines
  104–116) and the "Use both together when" list (131–134) show *that* you can
  combine them, but the skill never states the key fact that makes "both" easy: Plan
  Mode (`Shift+Tab` ×2) and Extended Thinking (`Tab`) are **independent toggles on
  different keys** that compose freely — so "both" is not a special mode, it's just
  turning on two switches. It also never states which to reach for *first* on a task
  that wants both. **What Sean observes:** grounding (c)'s "unclear what to do when
  both apply" persists — the model treats "both" as a distinct third thing rather
  than understanding the two are orthogonal and stackable.

- `minor` — **`Ctrl+G` mislabeled.** Line 100 ("Refine (Ctrl+G): Open the generated
  plan in your text editor") implies Ctrl+G opens the plan Claude just produced.
  Per shortcuts.md line 23, Ctrl+G opens the **current prompt buffer** in `$EDITOR`.
  **What Sean observes:** a user presses Ctrl+G expecting to edit the generated plan
  and instead gets their own prompt input in the editor.

- `minor` (with an open question) — **Two settings.json keys are unverified in-repo.**
  `alwaysThinkingEnabled` (line 145) and `maxThinkingTokens` (line 146) appear in the
  Configuration Example but are corroborated **nowhere** in `claude-mastery/` or the
  live `settings.json` (only the `MAX_THINKING_TOKENS` env var and `/config` are).
  **What Sean observes:** a user copies the config block into `settings.json` and, if
  the camelCase keys aren't real, they're silently ignored — the "force thinking on"
  intent never takes effect. See Open Question 1.

---

## Artifact 2 — Intent-Carrying Improvement Spec

Structured with `intent-engineering`'s scaffolding so the *why* survives to Fable
and any model it dispatches.

### Objective

`plan-and-think` exists to make the Plan-Mode-vs-Extended-Thinking distinction
*masterful and un-confusable* — the repo cared enough to make it **Non-Negotiable
Rule #1** (grounding (a)). Yet the skill under-delivers on both halves of that
mandate: it (1) omits the single-`Tab` shortcut and the `Tab`/`Shift+Tab` adjacency
that *is* the confusion Rule #1 guards against, and (2) offers generic "when to use"
lists and un-tiered token budgets instead of a task-shape → mode+budget mapping.
Closing these turns the skill from "accurate reference the reader must still reason
over" into "the choice falls out automatically and the two modes are impossible to
mix up" — exactly grounding (d).

### Desired Outcomes (from Sean's perspective — (c) → (d))

- A fresh session **literally cannot confuse** Plan Mode and Extended Thinking:
  the skill leads with a disambiguation card that mirrors Rule #1, names the
  `Tab` (think in place) vs `Shift+Tab` (cycle toward Plan/read-only) collision
  explicitly, and states they are different keystrokes doing different things.
- The **right mode is chosen by lookup**: a task-shape table maps common task
  shapes to Plan / Extended Thinking / both, so the choice is automatic rather than
  re-reasoned each time.
- The **thinking budget is tiered to problem depth**, so the owner sets a defensible
  budget (off / low / high) from the problem, not a guess.
- "Both apply" is understood as **composing two orthogonal toggles**, with a stated
  first-move — no longer a fuzzy special case.

### The fix, per finding (with reasoning a weaker model needs)

**Fix 1 — Add a top-of-skill disambiguation card and complete the shortcut row
(`dangerously-wrong`, highest leverage).** Near the top (right after Purpose, before
the comparison table), add a short, unmissable block that mirrors Rule #1 and names
the collision:
- Plan Mode = **double `Shift+Tab`** (cycles Normal → Auto-Accept → Plan) or `/plan`
  — read-only exploration.
- Extended Thinking = **single `Tab`** (sticky toggle; `Option+T`/`Alt+T` is the
  same thing) — extra internal reasoning budget.
- State the trap in one line: *"`Tab` and `Shift+Tab` are one keystroke apart and do
  completely different things — this is the #1 confusion (repo Non-Negotiable Rule
  #1)."*
Then fix the comparison table (line 46) and Extended Thinking Activation (line 80,
and Success Criteria line 165) to lead with `Tab` and present `Option+T`/`Alt+T` as
the alternative.

*Reasoning for the implementer (do not lose this):* the skill's whole reason to
exist is preventing this confusion, and you cannot inoculate against a collision you
never name. The reason to lead with `Tab` (not `Option+T`) is that `Tab` is both the
primary toggle (shortcuts.md line 18) **and** the term the Non-Negotiable rule uses —
a skill that disagrees with the repo's canonical rule on its core topic is worse than
no skill. Do **not** delete `Option+T`; it's a real alternative — demote it, don't
drop it. The load-bearing move is naming the `Tab`↔`Shift+Tab` adjacency out loud;
that single sentence is what makes the distinction "impossible to get wrong for a
fresh session" (grounding (d)).

**Fix 2 — Replace the three "when to use" lists with a task-shape → mode routing
table (`structural`).** Convert lines 118–134 into a lookup keyed on task shape, e.g.
rows for: *explore unfamiliar codebase* → Plan; *stubborn/regressing bug* → Extended
Thinking; *multi-file or legacy refactor* → Extended Thinking (+ Plan to scope first);
*architecture decision on a large codebase* → both; *quick, low-stakes decision* →
neither. Keep a one-line "why" per row.

*Reasoning:* grounding (c) says the guidance is "generic rather than mapped to task
shapes" and (d) wants the mode "chosen automatically per task shape." A table makes
the choice a lookup instead of a fresh judgment each session. Preserve the existing
prose *rationale* underneath if useful, but the table is the primary artifact. Bonus:
this table is the **liftable recipe** `zoom-out-and-think` (assembled from this skill)
can point at for its "read the whole system deeply" step — today it can only borrow
prose.

**Fix 3 — Add a thinking-budget-to-depth tiering (`structural`).** Add a small tier
guide: e.g. *off/none* for quick decisions; *low (~4–8k)* for a focused single-file
reasoning task; *high (~16–32k)* for stubborn multi-path bugs and large architecture
work. Tie it to the same task shapes as Fix 2 so mode and budget are chosen together.

*Reasoning:* grounding (c)/(d) explicitly want budget "matched to problem depth." The
skill already surfaces `MAX_THINKING_TOKENS` (env var, confirmed) and a `maxThinking
Tokens` setting (unverified — see Fix 5/Open Q1); the missing piece is the mapping
from depth to number. **Do not invent precise numbers as gospel** — present them as
sane defaults and let Fable set the tiers against the harness's actual honored max
(Open Question 2).

**Fix 4 — State that Plan Mode and Extended Thinking are orthogonal, composable
toggles (`structural`).** In or just before the Deep Architect Workflow (lines
104–116), add one line: the two are independent toggles on different keys, so "use
both" just means turning both on; and give a first-move ("enter Plan Mode first to
bound the read-only surface, then toggle Extended Thinking for depth").

*Reasoning:* grounding (c) "unclear what to do when both apply." The confusion is
that "both" reads like a third mode; naming the orthogonality dissolves it. Keep the
Deep Architect Workflow — it's a good worked example — just precede it with the
one-line orthogonality fact so the reader understands *why* the workflow toggles two
things.

**Fix 5 — Correct `Ctrl+G`, and verify the two settings keys (`minor`).** Reword line
100 so Ctrl+G is described as "opens your current prompt in `$EDITOR`" (per
shortcuts.md line 23), not "open the generated plan." For `alwaysThinkingEnabled` /
`maxThinkingTokens` (lines 145–146): **do not assert them as canonical until
verified** — see Open Question 1. If Fable confirms they're unreal, replace the
config block's thinking portion with the confirmed mechanisms (`MAX_THINKING_TOKENS`
env var and the `/config` "Extended thinking" toggle).

*Reasoning:* both are small, but this is a *reference* skill whose entire value is
precision — a wrong shortcut or a phantom settings key silently erodes trust in the
rest. Fix the confirmed error (Ctrl+G) directly; gate the unverified keys behind
verification rather than guessing.

### What NOT to change (confirmed working — don't "fix" out of over-eagerness)

- **The Plan Mode Activation section** (lines 53–76) — `Shift+Tab` cycling and `/plan`
  and `--permission-mode plan` and `defaultMode: plan` are all confirmed
  (shortcuts.md lines 20, 53; standard CLI). Leave intact.
- **`Ctrl+O`** (line 82) — correct per shortcuts.md line 13. Do not touch.
- **`MAX_THINKING_TOKENS` env var** (line 86) — confirmed (shortcuts.md line 117).
- **The Explore-Plan-Code Workflow** (lines 91–102, aside from the Ctrl+G wording) and
  the **Deep Architect Workflow** (lines 104–116) and the **Headless Planning Script**
  (lines 150–159) — sound, load-bearing worked examples; keep them.
- **The comparison-table *format*** (lines 40–50) — the table is a good device; only
  the Extended Thinking *shortcut row* needs correcting (Fix 1), not the table itself.
- **The frontmatter description's Plan-Mode half** (line 3: "Plan Mode (Shift+Tab or
  /plan)") — correct; only consider adding a `Tab` cue for Extended Thinking (Open Q3).

---

## Open questions for Fable (consolidated)

1. **Are `alwaysThinkingEnabled` and `maxThinkingTokens` real `settings.json` keys?**
   They appear only inside this SKILL.md; no corroboration in `claude-mastery/` or the
   live `settings.json`. Fable should confirm against the current settings schema. If
   real, keep them (and add them to `claude-mastery/reference/` so they're
   corroborated); if not, replace with the confirmed `MAX_THINKING_TOKENS` env var +
   `/config` toggle. **Do not ship the config block as canonical until this is settled.**
2. **Exact thinking-budget tiers (Fix 3).** My off/low(~4–8k)/high(~16–32k) numbers are
   defensible defaults, not measured. Fable should set tiers against the max the
   harness actually honors and the current cost profile.
3. **Frontmatter description (line 3).** Worth adding a single-`Tab` cue for Extended
   Thinking to the description so the disambiguation is present at auto-load glance, or
   is the body-level card (Fix 1) enough? Low-stakes; Fable's call.
4. **Depth of the seam scan here.** `plan-and-think` is a *reference/technique* skill,
   not a multi-phase ground→draft→output skill, so the classic "decided input dropped
   in a later phase" seam scan yields little — the dominant defects are the factual
   omission (Fix 1) and the two wow-gaps (Fix 2/3). I'm flagging this so Fable doesn't
   read the short seam section as an under-audit; it's the honest shape of this skill.

## Self-review

- Both artifacts present: **yes** (seam report + intent-carrying spec).
- Every finding tagged exactly one severity: **yes** (1 `dangerously-wrong`, 3
  `structural`, 2 `minor`).
- Spec carries WHY + critical details for a weaker model: **yes** — each fix states
  the reasoning (why lead with `Tab`, why the table, why not to delete `Option+T`) so
  an edge case doesn't collapse the intent.
- Harness-behavior claims are evidence-backed: **yes** — every shortcut/settings claim
  cites `claude-mastery/reference/shortcuts.md`, CLAUDE.md Rule #1, or a grep result;
  the unverified keys are labeled unverified rather than asserted.
- Open questions named where uncertain: **yes** (4).
- No skill edits, no commits: **yes** — this file only.
