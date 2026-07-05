---
name: skill-audit
description: Audit a Claude Code skill for downstream-intent seams, missing tool/handoff adapters, and "works-but-never-wows" gaps. Grounds itself with clarifying questions FIRST, then emits a seam report plus an intent-carrying improvement spec. Use to dial in a daily-driver skill, or to spec how to improve one.
---

# Skill Audit

## Purpose

Audit a Claude Code skill the way its most demanding downstream consumer would:
check whether every input the skill decides on actually survives to the moment
it's needed, whether each handoff lands in the shape the receiving tool expects,
and whether the output clears the bar the owner actually wants rather than just
the bar of "technically did what was asked." Never audit from assumption —
ground in the owner's real intent with four fixed questions first. Then run
three scans (seam, adapter, wow-gap) and emit two artifacts: a severity-tagged
seam report and an intent-carrying improvement spec that a weaker implementing
model can execute without losing the reasoning behind it. This skill critiques
and specs; it does not rewrite the audited skill itself.

## Provenance

Assembled from skill-system-mastery + intent-engineering + writing-critique's single-highest-leverage-fix pattern.

## When to Use

- Auditing an existing skill that feels "fine but not great" — output is
  technically correct but users keep fixing it by hand afterward.
- Before handing a skill off to a cheaper or weaker model to extend, fix, or
  maintain — the *why* behind each finding needs to survive the handoff, not
  just a diff.
- Preparing a batch review across several skills where findings need a
  consistent severity vocabulary from one skill to the next.
- Debugging why a skill's output looks right in isolation but breaks, or gets
  manually reformatted, once it reaches a downstream tool, agent, or file
  format.
- Not for critiquing a single piece of prose (`writing-critique`) or auditing
  CLAUDE.md files (`claude-md-improver`) — this skill is scoped to SKILL.md
  files and the behavior they produce.

## Step 1: Ground First (Hard Gate)

<HARD-GATE>
Do not scan the target skill, do not draft findings, and do not open the Seam
Scan step until the user has answered all four questions below. "This skill
obviously needs X" is exactly the shortcut this gate exists to block — an audit
built on your own guess about intent is an audit of a skill that doesn't exist.
This applies even when the target skill looks small or the fix looks obvious.
</HARD-GATE>

Ask these four, in order, and wait for real answers before scanning anything:

(a) **For** — What is this skill *for*, and who relies on it? (Sean directly in
    an interactive session? A headless agent running on a schedule? A specific
    downstream project?)
(b) **Feeds** — Which downstream skills, agents, tools, or file formats consume
    this skill's output? Name them specifically.
(c) **Disappoints** — Where does it "sometimes disappoint" today — the case
    where the output was technically correct but the owner had to fix it by
    hand anyway?
(d) **Wow** — What would a "wow" output from this skill look like — the version
    good enough that the owner would screenshot it or point someone else at it?

If the user's request already answers some of these in passing, restate your
understanding of each back to them and get explicit confirmation — do not
silently infer the rest just to save a round-trip. Only once (a)-(d) are
answered does Step 2 begin.

## Step 2: Seam Scan

A seam is a place where something the skill decided early should carry forward
into a later phase or handoff, and silently doesn't. Multi-step skills (ground →
draft → refine → output) are the most seam-prone: each step is a fresh reasoning
pass, and nothing forces a later step to remember what an earlier one settled
unless the skill text says so explicitly.

1. List every **decided input** the target skill builds or receives early — a
   brand-voice reference, a rubric or scoring criteria, a persona, a style
   guide, a specific design constraint, a file path or artifact handed over in
   an early step, an answer the user gave during a grounding or interview
   phase.
2. Walk each later phase, section, or handoff in the skill. For each decided
   input, ask: does this phase's instructions actually reference it, or could
   this phase run to completion having silently forgotten the input exists?
3. Every decided input that a later phase could drop without the skill text
   catching the omission is a seam. Name the phase, name the dropped input, and
   describe the concrete failure — e.g. "Step 3 (draft) never re-reads the
   brand-voice reference loaded in Step 1 — output drifts generic by the
   second paragraph."

## Step 3: Adapter Scan

Skills rarely emit into a vacuum — they hand off to a specific downstream tool,
agent, MCP, or file format (answer (b) above, plus anything the skill body
reveals that the owner didn't mention), and each of those has its own expected
shape. A skill that produces strong content in the wrong shape creates silent
breakage: a human reformats it by hand, or the receiving tool ignores fields it
doesn't recognize.

1. For each downstream handoff, identify the receiving format precisely — e.g.
   a Figma import wants component-and-variant structure, not a flat
   description; Claude-design wants a natural-language brief; Stitch wants a
   specific JSON schema; a generator script wants CLI flags in a specific
   order; another skill wants a specific section or tag vocabulary to chain
   off of.
2. Check whether the skill's output step actually produces that shape, or
   produces something generic and assumes the receiving side will cope.
3. Flag every missing adapter or format-conversion step — the point where the
   skill should say "convert X into the shape Y expects" and currently
   doesn't.

## Step 4: Wow-Gap Scan

Most skill output is correct and forgettable: it satisfies the literal ask and
nobody notices it happened. "Wow" output is the version the owner references
back to later. This scan finds the gap between the two, using answer (d) as the
target bar.

1. Walk the skill's actual (or instructed) output and mark every point where it
   stops at "technically satisfies the request" instead of pushing toward the
   wow bar the owner described.
2. For each point, name the *specific* missing move — never "make it better."
   Concrete examples: a missing second pass that checks against a named
   reference example, a missing step that surfaces the one non-obvious insight
   instead of stopping at the obvious ones, a missing verification loop, a
   missing "so what" synthesis, or an output format that undersells genuinely
   strong content.
3. Prioritize. Not every gap is worth closing — say explicitly which one or two
   gaps, if closed, would move this skill furthest toward the owner's wow bar,
   and which are lower-leverage polish.

## Step 5: Emit Two Artifacts

Combine every finding from Steps 2-4 into two deliverables. Emit both, every
time — an audit that stops at the report is half the job.

### Artifact 1 — Seam Report

A flat bulleted list. Every finding gets exactly one severity tag:

- `dangerously-wrong` — the skill will produce output the owner trusts but
  shouldn't: a silently dropped safety-relevant input, a downstream tool fed
  garbage it can't detect, output that contradicts the skill's own stated
  purpose.
- `structural` — the skill works but the architecture fights itself: a seam
  that degrades quality on every run, a missing adapter that forces manual
  cleanup, a real and closable gap to the owner's "wow" bar.
- `minor` — polish-level; the skill would be measurably better but nothing is
  currently broken.

Every finding names: where in the skill (which section/step), what the
seam/adapter/gap actually is, and what the owner would concretely observe when
it bites — never "could be an issue," always the actual failure mode.

### Artifact 2 — Intent-Carrying Improvement Spec

A fix spec for the target skill, structured using `intent-engineering`'s
scaffolding — not a bare instructions patch. The reason to borrow
intent-engineering's approach specifically: whoever implements this spec may be
a weaker or cheaper model than the one that audited, and a plain "change
section 3 to say X" loses the reasoning the instant that model hits an edge
case the patch didn't anticipate. The spec has to carry the *why*, not just the
*what*, so the motivational intent and the critical details survive the
handoff intact.

At minimum, structure the spec with:

- **Objective** — the problem this fix solves and why it matters, pulled from
  the grounding answers in Step 1, never invented.
- **Desired outcome** — the observable difference between the skill as-is and
  the skill after the fix, from the owner's perspective (answers (c) and (d)),
  not "section 3 now says X."
- **The fix, per finding** — for every `dangerously-wrong` and `structural`
  finding carried forward, the specific change plus the reasoning a weaker
  model would need to make the same call on an edge case the spec didn't spell
  out. `minor` findings can be listed without a full reasoning writeup.
- **What NOT to change** — anything the audit confirmed is already working, so
  the implementing model doesn't "fix" it out of over-eagerness.

If the improvement is large enough to justify it, invoke `intent-engineering`
directly and use its full 9-section template (or run its validation checklist
against your draft spec). For a small, contained fix, the four elements above
are the floor — never skip straight to a bare instruction list, even for a
one-line fix.

## Example

```
User: "Audit my daily-report skill — it works but nobody's excited about it."
Claude: [Uses skill-audit] Before I scan anything, four questions:

(a) For — who relies on this and how?
(b) Feeds — what does its output hand off to?
(c) Disappoints — where does it fall short today?
(d) Wow — what would make you screenshot the output?

User: (a) I read it every morning before standup. (b) Nothing downstream — it
posts straight to Slack. (c) The numbers are always right but it reads like a
cron log. (d) If it opened with the one number that actually changed instead
of a wall of every metric.

Claude: [Runs Seam Scan, Adapter Scan, Wow-Gap Scan]

## Seam Report
- `structural` — Step 2 (fetch metrics) tags each number with its source
  system's freshness, but Step 4 (render) drops that tag before formatting —
  a stale metric is now visually identical to a fresh one in the final report.
- `minor` — the Slack-formatting step doesn't escape underscores in ticket IDs,
  so `PROJ_142` renders as italic "142".

## Improvement Spec (intent-carrying)
**Objective:** Sean reads this every morning before standup and needs to trust
it at a glance; a report that reads like a cron log gets skimmed, not read,
which defeats the purpose.
**Desired outcome:** The first line names the one metric that moved most since
yesterday, in plain language; stale metrics are visibly marked, never silently
mixed in with fresh ones.
**Fix — seam (structural):** Carry the freshness tag from Step 2 through Step 4
by adding it as a field on the metric object, not a side note; the render step
must branch on it (e.g. render stale metrics with a `(stale)` suffix) — a
weaker model implementing this needs to know the reason is trust, not just
"add a tag," or it may drop the tag again at the next refactor.
**What NOT to change:** The metric-fetching logic itself (Step 2) is already
correct and matches the source-of-truth API; do not touch it.
```

## Success Criteria

- [ ] All four grounding questions (a)-(d) were asked and answered before any
      scanning began
- [ ] Seam scan names specific decided inputs and the specific phase each one
      fails to survive into
- [ ] Adapter scan names the specific receiving format for every downstream
      handoff, not just "the output should be better formatted"
- [ ] Wow-gap scan names a concrete missing move, not "make it better," and
      prioritizes which gap(s) matter most
- [ ] Seam report is a bulleted list with every finding tagged exactly one of
      `dangerously-wrong` / `structural` / `minor`
- [ ] Improvement spec carries Objective, Desired Outcome, per-finding
      fix-with-reasoning, and What NOT to Change — sufficient for a weaker
      model to implement without losing the why
- [ ] Both artifacts were emitted in the same pass — the audit never stops at
      the report alone

## Copy/Paste Ready

```
"Audit this skill for seams and gaps"
"Why does this skill feel flat — find the wow-gap"
"Find the missing adapters between this skill and its downstream tools"
"Spec an improvement for this skill that a weaker model could implement"
"Run a skill-audit on [skill-name] before I hand it off"
```
