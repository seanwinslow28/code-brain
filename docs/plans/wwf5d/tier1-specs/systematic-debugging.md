# Tier-1 Improvement Spec (DRAFT): `systematic-debugging`

## What this file is

An **Opus first-pass draft spec** produced by running the repo's `skill-audit`
harness against **the repo's own** `.claude/skills/systematic-debugging/SKILL.md`
(NOT the superpowers plugin skill of the same name — that collision is itself the
top finding). **No skill file was edited.** In Phase B, **Fable 5 elevates this
draft** into the applied change — a strong draft means Fable spends its cycles on the
last 20% (the coexistence mechanism, the exact gate wording), not on re-discovering
what to fix.

It contains the two `skill-audit` artifacts — a **severity-tagged seam report** and
an **intent-carrying improvement spec** — plus **named open questions** where I'm
uncertain, because a named open question is more useful to Fable than false
confidence. The single biggest question here — *how* the repo skill should coexist
with the same-named plugin skill — is a fleet-architecture call I hand to Fable +
Sean with a lean, not a decision I fake.

## Grounding answers used (controller-supplied, as Sean's (a)–(d))

- **(a) For:** the 4-phase debugging discipline (evidence before hypotheses before
  fixes); the anti-band-aid backbone of all fix work.
- **(b) Feeds:** `zoom-out-and-think` (explicitly assembled from it); every bugfix
  session; TDD loops; and it **must coexist cleanly** with the
  `superpowers:systematic-debugging` plugin skill that fires on the same triggers.
- **(c) Disappoints:** phase discipline collapses under time pressure — sessions
  skip to fixes; Phase 1 is vague about what counts as **sufficient** evidence to
  move on; the relationship / division-of-labor with the superpowers plugin version
  is **undefined** (two skills, same name, same trigger).
- **(d) Wow:** root-cause-first becomes the **default motion even mid-incident**,
  with **hard gates** between phases and a **crisp answer to "which
  systematic-debugging fires when."**

## Repo evidence checked (per campaign hard-constraint: no harness-behavior claims without evidence)

- **Two live skills share the name `systematic-debugging` with near-identical
  triggers:**
  - Repo (my target), frontmatter: *"Use when encountering bugs, test failures, or
    unexpected behavior. Four-phase root cause process before proposing any fix."*
  - Plugin `superpowers:systematic-debugging`, frontmatter: *"Use when encountering
    any bug, test failure, or unexpected behavior, before proposing fixes."*
- **The active plugin version is `superpowers` 6.1.1** — confirmed in
  `~/.claude/plugins/installed_plugins.json` (`"version": "6.1.1"`, installPath under
  `claude-plugins-official/superpowers/6.1.1`). Read at
  `.../superpowers/6.1.1/skills/systematic-debugging/SKILL.md`.
- **The repo skill is a stale, condensed *subset* of the plugin.** The plugin 6.1.1
  version is a superset — it adds sections the repo fork lacks: "Don't skip when,"
  "When You Don't Know" (Phase 3), "your human partner's Signals You're Doing It
  Wrong," "When Process Reveals 'No Root Cause'," "Real-World Impact," and a longer
  Red Flags / Rationalizations set. The 4-phase spine, Iron Law, and supporting-file
  references are otherwise near-identical.
- **The two versions diverge on the downstream chain (silent breakage risk):**
  - Repo Phase 4, step 1 (line 98): *"Use `verification-loops` skill for TDD
    approach."* (`verification-loops` is a repo skill — confirmed present at
    `.claude/skills/verification-loops/SKILL.md`.)
  - Plugin Phase 4, step 1 (line 179) + Related skills (lines 287–288):
    `superpowers:test-driven-development` and `superpowers:verification-before-completion`.
  → Whichever fires routes the fix-verification step to a **different** skill.
- **Consumers name the skill ambiguously.** `zoom-out-and-think/SKILL.md` line 25
  ("Assembled from **systematic-debugging** + plan-and-think + intended-vs-implemented")
  and line 39 ("use `systematic-debugging` directly" for first-time bugs);
  `agents-sdk/CONTINUATION-2026-06-02-vault-critic-antigravity.md` line 15 ("Use the
  `systematic-debugging` skill. Do NOT propose a fix until you've found root cause.").
  None says **which** of the two.
- **Repo-only supporting asset:** the repo dir ships `find-polluter.sh` (listed in
  Supporting Techniques, line 146) which the plugin 6.1.1's Supporting Techniques does
  **not** list. Plus `root-cause-tracing.md`, `defense-in-depth.md`,
  `condition-based-waiting.md` (shared with the plugin).
- **Prior triage rated it "Keep" 5/5** (`docs/plans/2026-02-18-skills-audit-v2.md`
  line 389) — i.e. the owner wants it kept, which (with grounding (b)) means the
  target state is **clean coexistence**, not deletion.

### Scope notes

- **In scope for a Phase-B SKILL.md edit:** everything in Artifact 2 that is a body
  or frontmatter-description change to the **repo** skill. The plugin file under
  `~/.claude/plugins/...` is **not ours to edit** — the coexistence fix lives entirely
  in the repo skill's own text.
- **Bigger calls flagged as open questions:** the coexistence *mechanism*
  (differentiate-by-scope vs thin-pointer vs rename) and whether any true *enforcement*
  (a hook / required artifact) is in scope vs a skill that can only steer.
- **Privacy:** public skill, no `references/`/`drafts/`; no privacy surface.

---

## Artifact 1 — Seam Report

- `dangerously-wrong` — **Two skills named `systematic-debugging` with near-identical
  triggers fire non-deterministically and route to different downstream chains.** The
  repo skill and `superpowers:systematic-debugging` 6.1.1 have essentially the same
  auto-load trigger (grounding (b)/(c)), and the repo one is a stale *subset* of the
  plugin. **What Sean observes — two concrete failure modes:** (1) *Silent
  divergence* — a debugging session can follow a different playbook run-to-run
  depending on which fired, and the fix-verification step lands on a **different
  skill** (`verification-loops` vs `superpowers:test-driven-development`), so the "same"
  debugging discipline forks. (2) *The edit-masking trap* — Sean edits the **repo**
  skill to close a gap, the **plugin** fires instead, and the fix **silently
  no-ops**; he trusts the improvement took effect when it didn't. *Nuance for the
  implementer:* neither skill gives *wrong debugging advice* — both are sound. Tagged
  `dangerously-wrong` for the **silent non-determinism + false confidence that an edit
  took effect**, which is precisely "output the owner trusts but shouldn't." This is
  the finding grounding (c) names as "undefined" and grounding (d) demands "a crisp
  answer to which fires when."

- `structural` — **Phase gates are willpower, not structure — no forcing artifact, so
  discipline collapses under time pressure (a real seam).** The Iron Law (lines
  17–22), "You MUST complete each phase" (line 43), Red Flags (110–119), and
  Rationalizations (122–129) all *exhort* but nothing *forces* Phase 1's evidence to
  exist as a named artifact that a later phase must cite. The **seam**: the root cause
  named in Phase 1/3 should carry into Phase 4, yet Phase 4 ("Address the root cause
  identified," line 99) never requires the fix to reference the specific traced
  origin. **What Sean observes:** under pressure the model writes a plausible Phase-1
  paragraph, jumps to a symptom patch in Phase 4, and because nothing gates on a
  concrete evidence artifact, the skip is invisible — exactly grounding (c)'s "phase
  discipline collapses… sessions skip to fixes."

- `structural` — **Phase 1 has no sufficiency exit-gate.** Phase 1 lists five
  activities (lines 46–81) but the only "done" signal is the Quick Reference's
  "Understand WHAT and WHY" (line 135) — unmeasurable. **What Sean observes:** the
  model declares Phase 1 complete after reading the error and forming a hunch, with no
  checklist forcing *reproduced (or explicit why-not) + traced to origin + named the
  owning component* before Phase 2 — grounding (c)'s "Phase 1 is vague about what
  counts as sufficient." Note: the plugin 6.1.1 **also lacks** a crisp Phase-1 exit
  gate, so this is a place the repo skill can genuinely **lead**, not merely copy the
  plugin.

- `structural` — **Division of labor with the plugin is undefined *inside the skill
  body*.** Even setting aside which auto-loads, the skill never tells a reader (or a
  consumer that says "use systematic-debugging") when to prefer it over
  `superpowers:systematic-debugging`. **What Sean observes:** `zoom-out-and-think`
  ("assembled from systematic-debugging") and the agents-sdk continuation doc can't
  route deterministically; the provenance "assembled from systematic-debugging" is
  ambiguous about which lineage it inherited. Grounding (b) requires the two "coexist
  cleanly" — coexistence with no stated boundary is not clean.

- `minor` — **The downstream TDD/verify reference is a fork accident, not a stated
  choice.** Repo Phase 4 (line 98) points to `verification-loops`; the plugin points
  to `superpowers:test-driven-development`. **What Sean observes:** two same-named
  debugging skills hand off to two different verification skills; if the repo skill is
  kept, its choice of `verification-loops` should be *deliberate and stated*, not an
  artifact of when the fork was taken.

- `minor` — **`find-polluter.sh` is listed but never wired into a phase.** It's a
  test-pollution bisection tool (most relevant to Phase 1 when reproducing
  order-dependent test failures), listed in Supporting Techniques (line 146) but not
  referenced from any phase. **What Sean observes:** the tool ships in the dir but a
  model walking the phases never learns *when* to reach for it.

---

## Artifact 2 — Intent-Carrying Improvement Spec

Structured with `intent-engineering`'s scaffolding so the *why* survives to Fable and
any model it dispatches.

### Objective

`systematic-debugging` is the anti-band-aid backbone of all fix work (grounding (a)),
but two forces undercut it. First, it **collides** with a same-named, superset plugin
skill, so "which fires" is a coin flip with **silently divergent** downstream chains
(grounding (c)/(d)). Second, its phase gates are **exhortation, not structure**, so
discipline collapses under time pressure and Phase 1 has no sufficiency bar
(grounding (c)). The owner wants the two to **coexist cleanly** (grounding (b)) with
**hard gates** and a **crisp "which fires when"** (grounding (d)). This fix matters
because a debugging discipline that fires non-deterministically, or that a rushed
session can skip invisibly, is not a discipline — it's a suggestion.

### Desired Outcomes (from Sean's perspective — (c) → (d))

- **"Which systematic-debugging fires when" has a crisp, written answer** — stated in
  the repo skill's own frontmatter description *and* a short in-body "Relationship to
  `superpowers:systematic-debugging`" section — so coexistence is clean and consumers
  (`zoom-out-and-think`, agents-sdk docs) route deterministically.
- **Phase transitions have concrete gates**, not exhortation: a written Phase-1
  evidence artifact that Phase 3/4 must cite, plus a Phase-1 sufficiency checklist —
  so root-cause-first survives time pressure (grounding (d) "default motion even
  mid-incident," "hard gates between phases").
- **The fix must name the traced origin it addresses** — closing the Phase-1 → Phase-4
  seam so a symptom patch can't masquerade as a root-cause fix.
- **The TDD/verify handoff is a stated, deliberate choice**, and `find-polluter.sh`
  has a named trigger.

### The fix, per finding (with reasoning a weaker model needs)

**Fix 1 — Resolve the collision: state the division of labor and disambiguate the
trigger (`dangerously-wrong`, highest leverage).** Two coordinated edits to the **repo**
skill only:
- **Frontmatter description:** rewrite so the trigger is *distinct* from the plugin's
  and states its niche (see the coexistence options below — Fable/Sean pick the
  mechanism).
- **Body:** add a short "Relationship to `superpowers:systematic-debugging`" section
  that states, in one paragraph, when to use this one vs the plugin, so a consumer
  saying "use systematic-debugging" can route.

*Coexistence options (Fable + Sean decide the mechanism — grounding (b) rules out
deletion since the owner keeps it):*
  - **(A) Differentiate by scope** — repo skill becomes the **code-brain
    fleet/agent-incident** flavor (knows launchd agents, Ollama routing, local-model
    failure patterns, and chains to the repo's `verification-loops`); the plugin stays
    the generic 4-phase method. Frontmatter trigger narrows accordingly (e.g. "for
    code-brain fleet/agent/launchd bugs; for generic bugs use
    `superpowers:systematic-debugging`").
  - **(B) Thin overlay/pointer** — repo skill defers the generic 4-phase method to the
    plugin and keeps only the repo-specific additions (the sufficiency gate,
    `find-polluter.sh` trigger, `verification-loops` chain). Smallest surface, least
    duplication, but depends on the plugin staying installed.
  - **(C) Rename** — give the repo skill a distinct name (e.g. `fleet-debugging`) so
    there's no trigger collision at all. Cleanest for auto-load; costs the "assembled
    from systematic-debugging" provenance in `zoom-out-and-think` (would need updating).

*Reasoning for the implementer (do not lose this):* the danger is **not** bad advice —
it's silent non-determinism and the edit-masking trap (an edit to the repo skill that
no-ops because the plugin fired). Any option is acceptable *as long as the trigger
stops overlapping and the body states the boundary*; what is **not** acceptable is
leaving two near-identical triggers with no stated division. **I lean (A)
differentiate-by-scope**: it preserves the owner's kept skill, gives it a real reason
to exist next to the plugin, keeps the `verification-loops` chain intentional, and
keeps `zoom-out-and-think`'s provenance valid. But this is a fleet-architecture call —
Fable should confirm with Sean before committing the mechanism (Open Question 1).

**Fix 2 — Turn the phase gates into forcing artifacts, and close the Phase-1 → Phase-4
seam (`structural`).** Add an explicit, lightweight **Phase-1 evidence artifact** the
session must write before Phase 2 (the exact failing symptom + repro status + the
traced origin + the component that owns it), and require Phase 4's fix to **name which
traced origin it addresses**. Keep it lightweight — a few lines, not a form.

*Reasoning:* grounding (c) "discipline collapses under time pressure" and (d) "hard
gates between phases." A gate the model *narrates* is skippable under pressure; a gate
that produces a **named artifact a later phase must cite** makes the skip *visible* —
if Phase 4 can't name the origin from the Phase-1 artifact, the skip is caught. The
reason to require Phase 4 to cite the origin (not just "address root cause") is the
skill's own principle "fix at source, not at symptom" (line 82 / line 99): without the
citation, a symptom patch reads identical to a root-cause fix. Caveat the implementer
must hold: a SKILL.md can only **steer** — true enforcement would need a hook or a
checklist the harness verifies (Open Question 2); write the strongest steer a skill
can, and flag real enforcement as a follow-up rather than pretending prose enforces.

**Fix 3 — Add a Phase-1 sufficiency exit-checklist (`structural`).** Add an explicit
"You may enter Phase 2 only when" checklist: (i) you can state the exact failing
symptom (not "it's broken"); (ii) you can reproduce it, or have explicit evidence why
it's not reproducible; (iii) you've traced the bad value/behavior to its origin (not
just where it surfaced); (iv) you can name the component that owns that origin.

*Reasoning:* grounding (c) "Phase 1 is vague about what counts as sufficient." These
four are assembled from Phase 1's **own** activities (read errors, reproduce, trace
data flow, gather evidence at component boundaries — lines 46–81); do **not** invent
new criteria, just convert the activities into a pass/fail gate. This is also where the
repo skill can **lead** the plugin (which lacks this gate) — a genuine wow move, not a
copy.

**Fix 4 — Make the TDD/verify handoff a stated choice, and give `find-polluter.sh` a
trigger (`minor`).** If the repo skill is kept standalone (options A/C), state plainly
that Phase 4 chains to `verification-loops` **by design** (the repo-local verification
skill), so it doesn't read as an accidental fork divergence from the plugin's
`superpowers:test-driven-development`. Add one line in Phase 1 / Supporting Techniques
telling the model to reach for `find-polluter.sh` when a test failure is
order-dependent or only reproduces in the full suite.

*Reasoning:* grounding (b) "coexist cleanly" extends to the handoff — two same-named
skills routing to two different verify skills is confusing unless the repo one's choice
is deliberate and stated. The `find-polluter.sh` line costs nothing and turns a listed
tool into a used one.

### What NOT to change (confirmed working — don't "fix" out of over-eagerness)

- **The 4-phase structure itself** (Phases 1–4) — it's sound, and
  `zoom-out-and-think` is "assembled from" its 4-phase shape (line 25); changing the
  spine would break that provenance. Add gates *around* the phases; don't restructure
  them.
- **The Iron Law framing** (lines 17–22) and **"NO FIXES WITHOUT ROOT CAUSE
  INVESTIGATION FIRST"** — this is the skill's identity; keep it verbatim.
- **The Red Flags (110–119) and Common Rationalizations (122–129) tables** — these are
  the cultural backbone that makes root-cause-first the default motion; keep them
  (optionally sync in the plugin's extra rows, but don't cut).
- **The "3+ fixes → STOP and question the architecture" rule** (lines 101–108) — a
  genuinely valuable escape hatch; leave intact.
- **The supporting files** (`root-cause-tracing.md`, `defense-in-depth.md`,
  `condition-based-waiting.md`, `find-polluter.sh`) — keep all; only *reference*
  `find-polluter.sh` better (Fix 4).
- **The `superpowers:systematic-debugging` plugin file** — outside this repo; the fix
  lives entirely in the repo skill's text. Do not attempt to edit the plugin.

---

## Open questions for Fable (consolidated)

1. **Coexistence mechanism (Fix 1) — the biggest call.** Differentiate-by-scope (A) vs
   thin-overlay (B) vs rename (C). Owner intent (grounding (b) + prior "Keep" rating)
   rules out deletion. I lean **(A)**, but this is a fleet-architecture decision that
   touches `zoom-out-and-think`'s provenance and the agents-sdk usage — **Fable should
   confirm the mechanism with Sean before committing**, not pick it from wording alone.
2. **Enforcement vs steering (Fix 2).** A SKILL.md can only steer; a *hard* gate (the
   kind grounding (d) wants) would need a hook or a harness-verified checklist. Decide
   whether real enforcement is in scope for this campaign or a noted follow-up. (Same
   shape as the `intent-engineering` sibling spec's validation-gate open question.)
3. **Should the repo skill sync the plugin's superset content?** The plugin 6.1.1 has
   sections the repo fork lacks ("Don't skip when," "No Root Cause," human-partner
   signals). Under option (A)/(C) — keep standalone — does Fable pull those in (to stop
   drifting further behind), or under (B) — thin overlay — deliberately *not* duplicate
   them and defer to the plugin? Tied to Open Question 1.
4. **`verification-loops` vs `superpowers:test-driven-development`.** If differentiating
   by scope, is the repo-local `verification-loops` the intended verify chain, or should
   the repo skill also point at the superpowers TDD skill for consistency with the
   plugin? Sean's call on which verification skill is canonical for repo debugging.

## Self-review

- Both artifacts present: **yes** (seam report + intent-carrying spec).
- Every finding tagged exactly one severity: **yes** (1 `dangerously-wrong`, 3
  `structural`, 2 `minor`).
- Spec carries WHY + critical details for a weaker model: **yes** — each fix states the
  reasoning (why the collision is dangerous despite sound advice; why a *named
  artifact* gate beats exhortation; why the sufficiency criteria are assembled from
  Phase 1's own activities, not invented) so an edge case doesn't collapse the intent.
- Harness-behavior claims are evidence-backed: **yes** — the two triggers quoted from
  frontmatter; active plugin version from `installed_plugins.json`; the superset/subset
  and divergent-chain claims from a line-by-line read of both SKILL.md files;
  `verification-loops` presence from `ls`; consumers from grep. Cited inline.
- Open questions named where uncertain: **yes** (4) — including the explicit hand-off of
  the coexistence-mechanism decision to Fable + Sean rather than a faked pick.
- No skill edits, no commits: **yes** — this file only. The plugin file was read, never
  modified.
