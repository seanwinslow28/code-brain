# Tier-1 Improvement Spec (DRAFT): `intent-engineering`

## What this file is

An **Opus first-pass draft spec** produced by running the repo's `skill-audit`
harness against `.claude/skills/intent-engineering/SKILL.md`. **No skill file was
edited.** In Phase B, **Fable 5 elevates this draft** into the applied change — a
strong draft means Fable spends its cycles on the last 20% (precision, wording,
tool-routing exactness), not on re-discovering what to fix.

It contains the two `skill-audit` artifacts — a **severity-tagged seam report** and
an **intent-carrying improvement spec** — plus **named open questions** where I'm
uncertain, because a named open question is more useful to Fable than false
confidence.

## Grounding answers used (controller-supplied, as Sean's (a)–(d))

- **(a) For:** design/review/retrofit intent specs for agents and skills; the
  "carry the why" backbone of Sean's whole agent fleet.
- **(b) Feeds:** `skill-audit`'s Step-5 spec output and `zoom-out-and-think`'s spec
  output (both reference it by name), every agent build, the local
  intent-engineering MCP tools.
- **(c) Disappoints:** the 9-section template is heavyweight for small retrofits;
  retrofit levels are fuzzy in practice (when is Level 1 enough?); the validation
  checklist exists but nothing forces it to run.
- **(d) Wow:** specs that survive three handoffs (Fable→Opus→subagent) with zero
  intent drift, right-sized per retrofit level, validation actually gating.

## Repo evidence checked (per campaign hard-constraint: no behavior claims without evidence)

- **Three `intent-engineering` MCP tools are live in this session** (schemas loaded
  via `ToolSearch` at audit time):
  - `generate_intent_spec_scaffold` — "Return the appropriate intent-spec template
    (blank, Level-1 MVR, or full 9-section) with optional pre-filled objective_hint,
    autonomy_level, and agent_name."
  - `audit_intent_spec` — "Audit an intent spec against the **25-item validation
    checklist and the 5 fatal anti-patterns** from the intent-engineering skill."
  - `assess_retrofit_level` — "recommend the right retrofit level
    (L1-mvr / L2-structured / L3-full) with reasoning grounded in the … blast-radius
    / complexity / autonomy framework."
- **`SKILL.md` references none of these tools.** `grep -niE
  "mcp|assess_retrofit|audit_intent|generate_intent|scaffold"` over the file returns
  only one incidental hit ("Calendar MCP" inside an example, line 392). The skill
  teaches a **manual** process for the exact three things its own tools automate.
- **The `audit_intent_spec` tool implements the skill's own checklist.** The
  SKILL.md Validation Checklist (lines 299–341) totals **25 items** (Objective 4 +
  Outcome 4 + Health 3 + Constraint 3 + Autonomy 3 + Stop Rule 4 + Edge Case 4),
  matching the tool's "25-item validation checklist" description exactly. The
  deterministic enforcer for grounding-(c)'s "nothing forces it to run" **already
  exists** — it just isn't wired.
- **Feeds confirmed by grep:** `skill-audit/SKILL.md` lines 157–180 and
  `zoom-out-and-think/SKILL.md` lines 149, 168 both name `intent-engineering` and
  instruct implementers to "structure the spec using `intent-engineering`'s
  scaffolding" / "run its validation checklist." Neither knows the MCP tools exist,
  because the parent skill never surfaces them.
- **Stale count:** SKILL.md says "107 in `.claude/skills/`" (lines 227, 258).
  Actual count today is **127** (`ls .claude/skills/ | wc -l`).
- **Server boundary:** the repo's root `.mcp.json` declares only `obsidian-vault`,
  `zapier`, and `ldr` — **not** intent-engineering. No server-impl file for these
  tools was found in the repo tree. So the MCP server is **user-scoped or
  plugin-provided, outside this repo**. Implication: Phase B's job is to make the
  SKILL.md **route to** these live tools — **not** to build or edit the server.

---

## Artifact 1 — Seam Report

- `structural` — **The skill's three MCP tools are invisible to the skill itself
  (the core adapter gap).** `generate_intent_spec_scaffold`, `audit_intent_spec`,
  and `assess_retrofit_level` map one-to-one onto the skill's three stated modes
  ("write / review / retrofit," How to Use, lines 418–442), yet the SKILL.md never
  mentions them. **What Sean observes:** every intent-spec task runs the slow manual
  path — the model hand-copies the 9-section template instead of calling the
  scaffold tool, and hand-walks a 25-item checklist (or skips it) instead of calling
  the deterministic audit tool. The tools and the skill were built to be two halves
  of one workflow and are currently disconnected.

- `structural` — **Validation is described but never routed to its enforcer
  (grounding-(c) defect, now with a fix in hand).** The Validation Checklist (lines
  299–341) and "run this against every intent spec before shipping" is a *prose
  instruction with no gate* — exactly the "nothing forces it to run" disappointment.
  The `audit_intent_spec` MCP tool runs precisely this checklist deterministically.
  **What Sean observes:** specs ship unvalidated whenever the model is under
  pressure or forgets, and the one mechanism that would make validation *actually
  gate* sits unused. This is the single most direct line from grounding-(c) to
  grounding-(d) ("validation actually gating").

- `structural` — **Retrofit-level selection is fuzzy and has no decision rule (the
  named-(c) fuzziness).** Levels 1/2/3 are defined by *effort* ("30 min," "2–4
  hours," "4–8 hours," lines 230–265) and a general prioritization list, but there
  is **no crisp test** for "when is Level 1 enough?" The `assess_retrofit_level`
  tool exists to answer exactly that question with blast-radius/complexity/autonomy
  reasoning, and it too is un-wired. **What Sean observes:** on a small retrofit the
  model either over-applies the full 9-section template (grounding-(c)'s "heavyweight
  for small retrofits") or guesses a level inconsistently run-to-run.

- `structural` — **The 9-section template is all-or-nothing at the point of use.**
  Line 33 mandates "Every intent spec you write or review MUST include all 9
  sections," while the MVR guide (lines 225–265) says small skills should get Level
  1 (3 sections). These coexist but the *entry point* ("How to Use," lines 418–442)
  always says "Draft using the full 9-section template" for writes — so the
  right-sizing only happens on the *retrofit* path, not the *author-new* path.
  **What Sean observes:** authoring a small new skill still pulls the heavyweight
  template; the "right-sized per retrofit level" wow (d) doesn't extend to new
  authoring.

- `minor` — **Stale skill count.** Lines 227 and 258 say "107 … in
  `.claude/skills/`"; the real count is 127. **What Sean observes:** a factual drift
  that quietly ages the skill and undercuts trust in its other specifics.

- `minor` — **Downstream consumers can't route to the tools they're told to use.**
  `skill-audit` (lines 157–180) and `zoom-out-and-think` (lines 149, 168) tell
  implementers to "use `intent-engineering`'s scaffolding / run its validation
  checklist," but because the parent skill hides the MCP tools, those consumers also
  do the manual version. Fixing the parent skill's routing unlocks the whole chain.
  (Tagged `minor` because the fix is *in this skill*; the observable cost lands in
  the consumers.)

---

## Artifact 2 — Intent-Carrying Improvement Spec

Structured with `intent-engineering`'s own scaffolding (fittingly) so the *why*
survives to Fable and its dispatched model.

### Objective

`intent-engineering` is the "carry the why" backbone of Sean's whole fleet
(grounding (a)) — its entire reason to exist is that intent must survive handoffs.
Yet the skill itself loses intent at its own most important seam: it never tells the
model that a **deterministic scaffold generator, a deterministic 25-item validator,
and a deterministic retrofit-level advisor already exist and are callable.** The
result is that the skill's three real pain points — heavyweight template,
fuzzy levels, unforced validation (grounding (c)) — all have **ready-made adapters
that aren't wired**. This fix matters because wiring them is the difference between
"the model might validate if it remembers" and "validation is a tool call that
either ran or didn't," which is exactly the "validation actually gating" wow (d).

### Desired Outcomes (from Sean's perspective — (c) → (d))

- Authoring or reviewing an intent spec **routes to the MCP tools by default**:
  `generate_intent_spec_scaffold` for the template (right-sized via `kind`),
  `audit_intent_spec` before any spec is called done, `assess_retrofit_level` to
  pick a retrofit level — with the manual process retained as the fallback when the
  tools are unavailable.
- Validation **actually gates**: a spec is not "done" until `audit_intent_spec`
  has run and its findings are addressed — no more silently-skipped checklist.
- Retrofit level is **chosen by a rule, not a vibe**: the skill states a crisp "when
  Level 1 is enough" test and/or defers to `assess_retrofit_level`, so small
  retrofits stop pulling the full template.
- Specs survive Fable→Opus→subagent with zero intent drift because the *validator is
  a deterministic tool*, not a paragraph the next model may skim.

### The fix, per finding (with reasoning a weaker model needs)

**Fix 1 — Wire the three MCP tools into the skill as the default path
(`structural`, highest leverage).** Add a section (near "How to Use," lines
418–442) that names each tool, states exactly when to call it, and makes the tool
call the **default** with the manual process as an **explicit fallback**:
- write a new spec → call `generate_intent_spec_scaffold` (choose `kind`:
  `blank` / `level-1-mvr` / `full-9-section`; pass `objective_hint`,
  `autonomy_level`, `agent_name` when known);
- review/ship a spec → call `audit_intent_spec` (pass `file_path` or `spec_text`)
  and treat its output as the validation gate;
- retrofit an existing skill/prompt → call `assess_retrofit_level` first, then
  scaffold at the recommended level.

*Reasoning for the implementer (do not lose this):* the tools and this skill are
**two halves of one system that were never introduced to each other.** The tool
descriptions state they are "grounded in the intent-engineering skill" — they are
the deterministic execution of this skill's own method. The reason to make the tool
call the *default* (not just "an option") is grounding-(c)/(d): a validator the
model *may* run is the exact failure; a validator that is the *documented default
call* is what makes validation gate. **Fallback matters:** the MCP server is
user/plugin-scoped and not in the repo (evidence above), so the tools can be absent
in some environments — the manual 9-section path and 25-item checklist must remain
in the skill as the graceful degradation, **not** be deleted. If a weaker model
reads "use the tool" and then can't find it, it must fall back to the prose method,
not stall.

*Open question for Fable:* **How hard should the validation gate be?** Options: (i)
soft — "call `audit_intent_spec` and address findings" (steering); (ii) hard —
make it a genuine stop-rule ("a spec is not done until the audit tool reports no
fatal anti-patterns"). intent-engineering's own philosophy (lines 20–26: "If a
constraint matters, don't trust the prompt to enforce it") argues for the hard
version — but a SKILL.md can only *steer*; true hard enforcement would need a hook,
which is out of scope for a skill edit. I lean: state it as a strong stop-rule in
the skill *and* name (as an open item) that real enforcement would be a PreToolUse
hook — but Fable should decide whether to scope the hook in or leave it as a noted
follow-up.

**Fix 2 — Make `audit_intent_spec` the validation gate, explicitly
(`structural`).** Rewrite the Validation Checklist framing (lines 299–341) so it
says: the checklist *is* what `audit_intent_spec` runs; call the tool to execute it;
the manual checklist below is the fallback / the human-readable reference for what
the tool checks. Keep the 25 items visible (they document the standard) but stop
presenting them as a thing the model hand-walks by default.

*Reasoning:* this directly converts grounding-(c)'s "nothing forces it to run" into
"the default is a tool call that either ran or didn't." The 25 items must stay
*visible* because (a) they're the spec of the standard and (b) they're the fallback
when the tool is absent — deleting them would break the degradation path. **Keep the
count in sync:** the tool says "25-item"; if Fable ever changes the checklist, the
tool and the number must move together (flag this coupling in the edit).

**Fix 3 — Add a crisp retrofit-level decision rule and route to
`assess_retrofit_level` (`structural`).** In the MVR guide (lines 225–265), add a
short decision rule for "when Level 1 is enough" (candidate, grounded in the skill's
own framework: *Level 1 if the skill is interactive-only AND single-task AND low
blast-radius; escalate to L2 when it runs autonomously OR is multi-step; L3 only for
autonomous + high-blast-radius or a spec that's actively producing wrong outputs*),
and state that `assess_retrofit_level` is the tool that makes this call when in
doubt. Also extend right-sizing to the **author-new** path (Fix 4).

*Reasoning:* grounding-(c) names level-fuzziness explicitly, and (d) wants
"right-sized per retrofit level." The skill already contains the raw
criteria (blast radius / autonomy / complexity, lines 258–265) — they're just not
assembled into a one-look rule. Do **not** invent new criteria; assemble the
existing ones into a test, and point to the tool as the tiebreaker. **Validate my
candidate rule against the tool's actual logic** before committing it — I derived it
from the skill's framework, but `assess_retrofit_level`'s real reasoning is the
source of truth (see open question).

**Fix 4 — Right-size the author-new path too (`structural`).** Reconcile the
"MUST include all 9 sections" mandate (line 33) with the MVR levels: the entry point
for *authoring a new* skill/agent (lines 420–424) should choose a scaffold `kind`
by the same blast-radius/complexity rule as retrofits, instead of always saying
"full 9-section template."

*Reasoning:* grounding-(c)'s "heavyweight for small retrofits" applies equally to
small *new* skills; today only the retrofit path is leveled. Keep the rule that
*autonomous / high-blast-radius* specs get the full 9 sections — that's a genuine
safety property, not bureaucracy. The change is: *small, interactive, single-task*
new skills may start at Level 1 and grow, same as retrofits.

**Fix 5 — Correct the stale count (`minor`).** Change "107" → "127" at lines 227 and
258. *Reasoning:* trivial, but it's a trust signal on a skill whose whole value is
precision. **Better still:** reword to avoid a hard-coded count that re-goes-stale
(e.g., "the ~130 skills in `.claude/skills/`" or "the skills in `.claude/skills/`
(run `ls` for the live count)"), so the next audit doesn't re-find this.

### What NOT to change (confirmed working — don't "fix" out of over-eagerness)

- **The 9-section template content** (Sections 1–9, lines 38–194) and the **5 Fatal
  Anti-Patterns** (lines 268–296) — these are the skill's substance and are sound.
  The fixes wire *routing and gating* around them; they don't rewrite the method.
- **The 25 validation items** (lines 299–341) — keep them visible as the standard
  and the fallback; do not delete them when routing to the tool.
- **The Autonomy Levels table and architecture mapping** (lines 198–222) and the
  four Domain Examples (lines 344–415) — correct and load-bearing; leave intact.
- **The manual process as fallback** — the MCP server is not in-repo and may be
  absent in some environments; the prose method must survive as graceful
  degradation. Do **not** turn this skill into a thin tool-wrapper that breaks when
  the tools aren't mounted.
- **The `intent-engineering` MCP server itself** — it's outside this repo. Phase B
  edits the *SKILL.md routing only*, not the server.

---

## Open questions for Fable (consolidated)

1. **Validation gate hardness** (Fix 1/2): steering ("call the tool and address
   findings") vs a true stop-rule vs an actual PreToolUse hook. The skill's own
   "don't trust the prompt" philosophy argues for hard enforcement, but that exceeds
   a skill edit. Decide the scope.
2. **Retrofit decision rule accuracy** (Fix 3): my candidate "when Level 1 is
   enough" rule is *derived from the skill's stated framework*, but the source of
   truth is `assess_retrofit_level`'s real logic. Fable should call the tool on a
   few sample skills (or inspect its reasoning) and reconcile the written rule with
   the tool's behavior before committing wording — otherwise the skill and its tool
   could disagree.
3. **Tool-call exactness:** the parameter names/enums I cite come from the loaded
   schemas at audit time (`kind` ∈ blank/level-1-mvr/full-9-section; `audit_intent_spec`
   takes `file_path` XOR `spec_text` with pagination). Fable should re-confirm these
   against the live schemas at implementation time in case the server version moved.
4. **Stale-count wording** (Fix 5): hard number vs count-agnostic phrasing — I
   recommend count-agnostic so it can't re-stale.

## Self-review

- Both artifacts present: **yes**.
- Every finding tagged exactly one severity: **yes** (4 `structural`, 2 `minor`; no
  `dangerously-wrong` — the skill doesn't make Sean *trust bad output*, it leaves
  leverage and a validator on the table).
- Spec carries WHY + critical details for a weaker model: **yes** (each `structural`
  fix has reasoning + a preserved-fallback note so the tools' absence doesn't break
  the skill).
- Behavior claims are evidence-backed: **yes** — MCP tools' existence and
  descriptions from loaded schemas; feeds from grep; count from `ls`; server scope
  from `.mcp.json`. Cited inline.
- Open questions named where uncertain: **yes** (4).
- No skill edits, no commits: **yes**.
