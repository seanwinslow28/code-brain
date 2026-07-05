# Tier-1 Improvement Spec (DRAFT): `skill-system-mastery`

## What this file is

An **Opus first-pass draft spec** produced by running the repo's `skill-audit`
harness against `.claude/skills/skill-system-mastery/SKILL.md`. **No skill file was
edited.** In Phase B, **Fable 5 elevates this draft** into the applied change — a
strong draft means Fable spends its cycles on the last 20% (verifying current
harness specifics against a live client, exact wording), not on re-discovering what
to fix.

It contains the two `skill-audit` artifacts — a **severity-tagged seam report** and
an **intent-carrying improvement spec** — plus **named open questions**.

## Grounding answers used (controller-supplied, as Sean's (a)–(d))

- **(a) For:** how skills get authored in this repo; gates the quality of all 127
  skills and every future one.
- **(b) Feeds:** every SKILL.md authoring session, `skill-audit` (built on its
  conventions), installer/export presets.
- **(c) Disappoints:** trigger/description-optimization advice predates current
  harness behavior (deferred tool schemas, how the Skill tool lists/invokes skills,
  description-as-trigger-surface); thin guidance on progressive disclosure (when to
  split reference files, what belongs in frontmatter description vs body).
- **(d) Wow:** skills that fire exactly when they should and never when they
  shouldn't, authored right the first time.

## Repo / harness evidence checked (per campaign hard-constraint: no behavior claim without evidence)

I verified every current-behavior claim below against `claude-mastery/` reference
docs and **directly observable behavior in this live session**. What I checked:

- **`/skills` — still current.** `claude-mastery/reference/shortcuts.md:57` lists
  `/skills` = "List discovered skills." → the skill's "Run `/skills` to verify
  discovery" advice (lines 44, 239) is **correct and current**.
- **Deferred / lazy tool schemas — real and live.** `shortcuts.md:123` documents
  `ENABLE_TOOL_SEARCH` = "MCP tool lazy loading." In *this* session, tools are
  surfaced by name but their **schemas are not loaded until `ToolSearch` fetches
  them** (I used `ToolSearch` to load three MCP-tool schemas during this audit).
  This is the "deferred tool schemas" reality grounding-(c) says the skill predates
  — and the skill says **nothing** about it.
- **The Skill tool is the invocation mechanism (observed).** Skills are presented to
  the model as a **name + description list** ("The following skills are available
  for use with the Skill tool"), and are invoked by an **explicit `Skill` tool
  call**. The tool's own contract states: "When users reference a 'slash command' or
  '/<something>', they are referring to a skill. Use this tool to invoke it," and
  "If you see a `<command-name>` tag … the skill has ALREADY been loaded — follow
  the instructions directly instead of calling this tool again." → The
  **description is literally the trigger surface** (the skill gets this right in
  spirit), but the *mechanism* is an explicit tool invocation, **not** a hidden
  "auto-load," which the skill's wording (line 90) blurs.
- **Plugin-namespaced skills use `plugin:skill` form (observed).** The Skill tool
  contract: "For plugin-namespaced skills use the fully qualified `plugin:skill`
  form." The skill's "name doubles as /slash-command" (line 85) and "type
  `/skill-name`" (line 242) are **incomplete** — they don't cover namespacing.
- **`--debug` — exists, but the skill over-claims its specificity.** `shortcuts.md:99`
  documents `--debug` = "Enable debug logging" (generic). The skill claims `claude
  --debug` "shows skill **triggering decisions** in logs" (line 244) — that specific
  behavior is **not confirmed** by the reference doc. Flag as unverified.
- **Corpus facts.** `ls .claude/skills/ | wc -l` = **127** skills; **32** have a
  `references/` dir; **8** have `scripts/`. So progressive disclosure via
  `references/` is used by ~25% of skills — the pattern is real but far from
  universal, which matters for the "when to split" guidance gap.

---

## Artifact 1 — Seam Report

- `structural` — **The loading model is described as "auto-load," but the observed
  mechanism is an explicit `Skill` tool call.** Line 90: "Claude reads it before
  every user turn and decides whether to load the full SKILL.md." Observed behavior
  (evidence above): skills are a name+description list the model invokes via the
  `Skill` tool; a `<command-name>` tag signals "already loaded, follow directly." 
  **What Sean observes:** an author following this skill optimizes for a
  passive-autoload mental model that no longer matches how invocation works, so
  advice about *why* a skill fires is subtly miscalibrated — the description isn't a
  passive load-trigger, it's the **selection surface the model reads to decide
  whether to call the Skill tool**. (The skill's practical conclusion —
  "description = trigger surface" — survives; the mechanism story behind it is
  stale.)

- `structural` — **No coverage of deferred/lazy tool schemas — the exact gap
  grounding-(c) names.** The skill's progressive-disclosure model (lines 134–153)
  covers only *this skill's own* three levels (metadata / SKILL.md / references).
  It never mentions that in the current harness **tool schemas themselves are
  deferred** (`ENABLE_TOOL_SEARCH`, `ToolSearch`) — which changes how a skill that
  depends on MCP or other tools should be authored (a skill can't assume its
  helper tools' schemas are already in context). **What Sean observes:** skills that
  lean on tools are authored as if those tools are always fully loaded, when in a
  tool-search environment they may need to be fetched first — a failure mode the
  skill gives no guidance on.

- `structural` — **Progressive-disclosure guidance is thin exactly where
  grounding-(c) says.** Lines 144–153 give one 50-line threshold and a short
  inline-vs-reference list, but are silent on the two decisions authors actually
  agonize over: **(1) what belongs in the frontmatter `description` vs the SKILL.md
  body**, and **(2) when to split into one reference file vs several.** **What Sean
  observes:** authors overload descriptions (raising always-present metadata cost
  across all 127 skills) or dump everything inline, and get no rule for slicing
  references — so the "authored right the first time" wow (d) misses on structure.

- `structural` — **The "never when they shouldn't" half of the wow bar is
  unserved.** Grounding-(d) is two-sided: fire when they should **and never when
  they shouldn't.** The skill covers positive triggering (put trigger phrases in the
  description) and the CSO "don't summarize the workflow" rule (lines 110–123), but
  gives **no technique for negative triggering** — how to keep a skill from firing
  on adjacent-but-wrong prompts (scoping language, "do NOT use for…" constraints are
  mentioned once at line 108 but not developed). **What Sean observes:** skills that
  over-fire on neighboring intents, with no authored defense — half the wow bar
  unaddressed.

- `minor` — **`--debug` over-claim.** Line 244 says `claude --debug` "shows skill
  triggering decisions in logs"; the reference doc only confirms generic "Enable
  debug logging." **What Sean observes:** an author runs `--debug` expecting a
  skill-trigger trace and may not find one framed that way. Soften to the verified
  claim or verify against a live run.

- `minor` — **Slash-invocation guidance omits plugin namespacing.** Lines 85 and 242
  present `/skill-name` as the manual trigger but don't mention the `plugin:skill`
  fully-qualified form the current harness requires for plugin-provided skills.
  **What Sean observes:** manual-invocation advice fails for the many
  plugin-namespaced skills now present (e.g. `superpowers:*`, `voiceprint:*`).

- `minor` — **Token-efficiency targets are under-nuanced vs the real always-loaded
  cost.** Lines 126–132 target "<200 words" / "<500 words" *total*, but the
  genuinely always-present cost is the **description** (all 127 sit in the metadata
  layer every session); several high-value skills (e.g. `writing-voice-modes`) far
  exceed 500 body-lines by design. **What Sean observes:** the word-count target
  reads as a hard rule the best skills already violate, when the real lever is
  description tightness + `references/` offloading.

- **Open-question finding (not tagged — needs Sean's intent):** **"Mandatory Section
  Order — Do not add or remove sections" (lines 156–166) is contradicted by the
  repo's own best skills.** `skill-audit` uses `Provenance` + `Step 1–5` (not
  `Examples` + `Domain Content`); `writing-voice-modes` adds many custom sections.
  Either the rule is meant only for *simple* skills (and should say so), or it's
  genuinely too rigid. I did **not** tag this because whether the rigidity is
  intended is a call for Sean/Fable — see Open Questions.

---

## Artifact 2 — Intent-Carrying Improvement Spec

### Objective

This skill gates the quality of all 127 skills and every future one (grounding
(a)/(b)) — it is the authoring standard the whole corpus inherits, including
`skill-audit` which is "built on its conventions." But its model of *how skills
fire* predates the current harness (explicit `Skill`-tool invocation, deferred tool
schemas, plugin namespacing), and its structural guidance is thin exactly where
authors make the decisions that determine whether a skill fires correctly. Fixing it
matters because every stale trigger claim and every missing progressive-disclosure
rule is **multiplied across 127 downstream skills** — this is the highest-fan-out
skill in the set.

### Desired Outcomes (from Sean's perspective — (c) → (d))

- The skill's account of triggering/loading **matches observed current harness
  behavior**: description = the selection surface the model reads to decide whether
  to call the `Skill` tool; tool schemas can be deferred; plugin skills are
  `plugin:skill`.
- Authors get **real decision rules** for progressive disclosure: what goes in the
  `description` vs the body, and when to split references into one file vs several.
- The skill teaches **both** halves of grounding-(d): fire-when-you-should **and**
  don't-fire-when-you-shouldn't (negative triggering / scoping).
- Every current-behavior claim in the skill is either **verified** or removed —
  no more stale mechanism stories.

### The fix, per finding (with reasoning a weaker model needs)

**Fix 1 — Rewrite the loading/triggering model against observed behavior
(`structural`, highest leverage).** Replace the "Claude reads it before every user
turn and decides whether to load" framing (line 90, and the CSO framing lines
110–123) with the observed mechanism: the harness presents skills as a
**name+description list**; the model **reads the description to decide whether to
invoke the `Skill` tool**; once invoked (or when a `<command-name>` tag is present)
the body is in context and is followed directly. Keep the CSO *conclusion* — a
description that summarizes the workflow invites the model to act on the summary
instead of the body — because that failure is **still live** (the `<command-name>`
"already loaded, follow directly" behavior makes an over-summarized description
genuinely risky).

*Reasoning for the implementer (do not lose this):* the skill's *practical advice*
("make the description a trigger surface, not a workflow summary") is **correct and
must survive** — only the *mechanism explanation* under it is stale. Do not throw
out the CSO section; re-ground it. **Verify before finalizing:** confirm the
invocation details against a live client at implementation time (the Skill-tool
contract wording can move between harness versions); cite what you check, the same
way this draft does. The point is a *true* mechanism story, not a *confident* one.

**Fix 2 — Add a "deferred tool schemas" note to progressive disclosure
(`structural`).** In the Progressive Disclosure section (lines 134–153), add that in
a tool-search harness (`ENABLE_TOOL_SEARCH`) **tool schemas are themselves
deferred** — a skill that depends on MCP or other non-core tools should not assume
those schemas are pre-loaded, and should say (in its body) to fetch/confirm the
tool before relying on it. *Reasoning:* this is grounding-(c)'s named gap; it's a
real authoring consideration (a skill that hard-codes a tool call can fail if the
schema isn't loaded). Keep it short — it's a note, not a new subsystem.

**Fix 3 — Add real progressive-disclosure decision rules (`structural`).** Extend
lines 144–153 with two explicit rules:
- **description vs body:** the `description` carries *only* what the model needs to
  decide *whether to invoke* (what it does + when to use + trigger/negative
  phrases); everything about *how to execute* goes in the body. (This is the same
  principle as the CSO section — unify them.)
- **one reference file vs several:** split by *when-read* boundary — each reference
  file should correspond to a distinct "read this only when [condition]" trigger the
  SKILL.md can name (mirror how `intent-engineering` and this repo's multi-reference
  skills actually slice). If two bodies of content are always read together, keep
  them in one file; if they're read under different conditions, split.

*Reasoning:* grounding-(c) names both gaps; the fix is decision *rules*, not more
prose. Anchor the "when to split" rule to the **"when to read" guidance the skill
already requires** (line 149, 262) — the split boundary and the read-trigger are the
same boundary, which keeps the advice self-consistent.

**Fix 4 — Add a negative-triggering / scoping technique (`structural`).** Develop
the one-line "add negative constraints" note (line 108) into a real subsection:
how to keep a skill from firing on adjacent intents — explicit "Do NOT use for…"
clauses naming the *neighboring* skills/tasks it's confused with, and trigger
phrases specific enough to disambiguate. *Reasoning:* this is the unserved half of
grounding-(d) ("never when they shouldn't"). Use the repo's own examples of skills
that disambiguate against neighbors (e.g., `skill-audit`'s "Not for critiquing a
single piece of prose (`writing-critique`)…" line, or `writing-critique` vs
`writing-humanity-pass`) as the pattern to codify.

**Fix 5 — Fix the `--debug` over-claim (`minor`).** Either soften line 244 to the
verified "enable debug logging" or verify the skill-trigger-trace behavior against a
live `--debug` run and cite it. Don't leave an unverified specific claim standing in
the corpus's authoring standard.

**Fix 6 — Add plugin-namespaced invocation (`minor`).** Note at lines 85/242 that
plugin-provided skills are invoked as `plugin:skill` (fully qualified), not bare
`/skill-name`.

**Fix 7 — Reframe token targets around the real always-loaded cost (`minor`).**
Reword lines 126–132 so the primary lever is **description tightness** (the
genuinely always-present cost across all 127 skills) + `references/` offloading, and
present the body word-counts as *guidance, not a hard cap* that the best complex
skills legitimately exceed.

### What NOT to change (confirmed working — don't "fix" out of over-eagerness)

- **The CSO *conclusion*** ("description = when-to-use, not a workflow summary,"
  lines 112–123) — this is *correct and current*; only re-ground its mechanism
  explanation. Do not delete it.
- **`/skills` for discovery, YAML-frontmatter checks, directory-name-matches-`name`,
  the debug checklist ordering** (Debugging Skills, lines 236–244) — the
  *procedure* is sound; only the `--debug` specificity needs softening.
- **The TDD-for-skills and Rationalization-Prevention sections** (lines 168–234) —
  strong, current, and load-bearing; leave intact.
- **The Component Selection Guide** (lines 246–254) — accurate; leave intact.
- **The overall "progressive disclosure" three-level framing** — correct; the fixes
  *add* rules within it, they don't replace it.

---

## Open questions for Fable (consolidated)

1. **"Mandatory Section Order" rigidity** (Artifact 1, untagged finding): the repo's
   own best skills break it. Is the fixed order meant only for *simple* skills (then
   say so, and note complex skills may add task-specific sections), or is it a rule
   Sean wants enforced corpus-wide? This is a taste/standard call I won't guess. My
   lean: soften to "this order for standard skills; complex multi-step skills may add
   sections but should keep Purpose / When to Use / Success Criteria / Copy-Paste as
   anchors" — but confirm with Sean/Fable.
2. **Live-harness re-verification** (Fix 1): the Skill-tool invocation contract and
   `<command-name>` behavior I observed are from *this* session; harness versions
   move. Fable should re-confirm against the client in play at implementation time
   and cite it — a *true* mechanism story is the goal, not a confident one.
3. **`--debug` behavior** (Fix 5): does the current client actually surface
   skill-trigger decisions under `--debug`? If yes, keep the claim and cite the run;
   if no, soften. I could only confirm generic debug logging from the reference doc.
4. **Depth of the deferred-schemas note** (Fix 2): a short awareness note vs a full
   "authoring skills that depend on deferred tools" subsection. I lean short (most
   skills don't call MCP tools), but Fable may know of enough tool-dependent skills
   to justify more.

## Self-review

- Both artifacts present: **yes**.
- Every finding tagged exactly one severity (plus one explicitly-untagged item
  flagged as needing Sean's intent): **yes** (4 `structural`, 3 `minor`, 1 flagged
  open); no `dangerously-wrong` — stale mechanism advice degrades authoring quality
  but doesn't make Sean trust a broken skill as good.
- Spec carries WHY + critical details for a weaker model: **yes** (each `structural`
  fix names what to preserve vs re-ground, so nothing correct gets deleted).
- Behavior claims are evidence-backed and cited: **yes** — `/skills`,
  `ENABLE_TOOL_SEARCH`, `--debug` from `shortcuts.md` (line-cited); Skill-tool
  invocation, `<command-name>`, deferred schemas, `plugin:skill` from direct
  session observation; counts from `ls`/`find`. Unverified claims are flagged as
  such rather than repeated.
- Open questions named where uncertain: **yes** (4, incl. the section-order call I
  deliberately did not resolve).
- No skill edits, no commits: **yes**.
