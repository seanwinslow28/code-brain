---
name: skill-system-mastery
description: Claude Code skill creation and optimization assistant. Guides building effective SKILL.md files with proper YAML frontmatter, progressive disclosure, trigger phrase optimization, negative triggers, and reference file architecture. Use when creating a new skill, writing a SKILL.md, improving an existing skill description, debugging why a skill does not auto-load or fires on the wrong prompts, deciding what belongs in the description versus the body versus references/, or structuring a skill directory. Not for end-to-end audits of a finished skill (use skill-audit), agent intent specs (use intent-engineering), or CLAUDE.md files (use claude-md-improver).
---

# Skill System Mastery

## Purpose

Create, debug, and optimize Claude Code skills that fire exactly when they should — and never when they shouldn't — and deliver domain expertise without wasting context tokens. Follow the progressive disclosure architecture: the description wins selection, SKILL.md provides workflow, and references/ holds deep content Claude reads only when needed.

## When to Use

- Creating a new skill from scratch (need the directory structure and SKILL.md template)
- Improving a skill description so it gets selected more reliably on user prompts
- Debugging a skill that is not firing when expected — or firing on prompts it shouldn't
- Deciding what belongs in the frontmatter description vs the SKILL.md body vs references/
- Structuring a large skill with scripts, references, and assets
- Reviewing a skill for quality (token efficiency, completeness, section order)
- Not for: auditing a finished skill for downstream-intent seams (`skill-audit`), writing intent specs for agents (`intent-engineering`), or CLAUDE.md quality (`claude-md-improver`)

## Examples

**Example 1: Creating a new skill**
```
User: "Create a skill for reviewing database migrations"
Claude: [Uses skill-system-mastery] Creates the directory structure:

db-migration-review/
  SKILL.md
  references/
    common-antipatterns.md

Generates SKILL.md with:
- Frontmatter: name + description with trigger phrases ("review migration", "check schema change", "audit SQL")
  and a negative trigger ("Not for application-layer ORM code changes")
- Purpose, When to Use, Examples sections
- Domain content: migration review checklist, rollback verification, index analysis
- Success Criteria and Copy/Paste Ready sections
```

**Example 2: Debugging a skill that never fires**
```
User: "My deploy-checker skill never fires when I ask about deployments"
Claude: [Uses skill-system-mastery] Checks:
1. Run /skills — is it discovered at all?
2. Run python3 scripts/validate.py — frontmatter parses, name matches directory, description present?
3. Type /deploy-checker — does manual invocation work? (Then the body is fine when loaded.)
4. Manual works but selection doesn't → inspect the description: does it contain trigger
   phrases like "deploy", "release", "ship to production"?
Identifies: description says "Validates infrastructure" but lacks deployment trigger words. Rewrites description.
```

**Example 3: Optimizing token usage**
```
User: "My API integration skill is 400 lines and slowing things down"
Claude: [Uses skill-system-mastery] Applies progressive disclosure:
- Moves the 200-line endpoint reference table to references/api-endpoints.md
- Moves authentication flow details to references/auth-patterns.md
- Keeps core workflow (50 lines) and 2 inline examples in SKILL.md
- Adds "when to read" guidance: "For endpoint specifications, see references/api-endpoints.md"
Result: SKILL.md drops from 400 to 120 lines; references load only when needed.
```

## How Skills Load (mechanism — verified 2026-07)

Verified against the live harness (`claude --help`, `claude-mastery/reference/shortcuts.md`, direct session observation). Harness behavior moves between releases — re-verify before repeating these claims elsewhere; a true mechanism story beats a confident one.

1. **Discovery.** The harness scans skill directories and presents every discovered skill to the model as a **name + description list** attached to an explicit `Skill` tool. `/skills` shows you the same inventory.
2. **Selection.** Before invocation, the model sees *only* that list. "Auto-loading" is not a hidden background pass — it is the model reading your description and deciding to call the `Skill` tool. Every selection failure is a description failure.
3. **Loading.** Invocation — or the user typing `/skill-name` — puts the full SKILL.md body into context. A `<command-name>` tag in the turn means the body is already loaded; the model follows it directly instead of re-invoking.
4. **Namespacing.** Plugin-provided skills are fully qualified as `plugin:skill` (e.g. `superpowers:writing-skills`, `voiceprint:voiceprint-mine`). Bare `/skill-name` only reaches local, unnamespaced skills.
5. **Kill switch.** `claude --disable-slash-commands` disables all skills (per `claude --help`) — the fastest check of whether a behavior comes from a skill at all.

Two consequences drive everything below:

- **The description is the selection surface.** It is the only part of your skill the model ever sees before deciding whether to invoke.
- **The body does not exist until selection is won.** A brilliant workflow behind a weak description never runs.

## Skill Directory Structure

```
skill-name/
  SKILL.md              # REQUIRED - core logic and metadata
  scripts/              # OPTIONAL - executable code Claude runs via Bash
  references/           # OPTIONAL - docs Claude reads on demand via Read
  assets/               # OPTIONAL - templates/images used in output (not loaded into context)
```

Never hardcode corpus counts in docs — they go stale. Live checks: `ls .claude/skills | wc -l` for the skill count; `find .claude/skills -maxdepth 2 -type d -name references | wc -l` for how many use references/ (about a quarter of this corpus as of 2026-07).

## YAML Frontmatter Specification

Only two fields are required — and only these two influence selection. The description is the single most important line in the entire skill.

```yaml
---
name: kebab-case-name
description: What this does AND when Claude should load it. Embed trigger phrases naturally.
---
```

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Kebab-case identifier. Must match the directory name. Doubles as the /slash-command (plugin skills: `/plugin:skill`). |
| `description` | Yes | The ONLY field the model reads to decide whether to invoke. Trigger phrases and negative triggers live here. |

A skill with a missing description surfaces in the list as a bare name the model has no reason to pick — effectively manual-invocation-only. Optional fields appear in this corpus but do not influence selection: `allowed-tools` (declares the tools the skill uses — see `gemini-deep-research` for the shape), `argument-hint`, `user-invocable`, and packaging metadata (`version`, `license`, `homepage`) on imported third-party skills. `python3 scripts/validate.py` machine-checks frontmatter presence, the name↔directory match, and the description on every skill in this repo.

### Writing Effective Descriptions

The description controls selection — it is what the model weighs against the user's prompt.

**Pattern**: `[What it does] + [When to use it with trigger phrases] + [When NOT to use it]`

Bad:
```yaml
description: Helps with databases.
```

Good:
```yaml
description: PostgreSQL query optimizer and schema reviewer. Use when analyzing slow queries, reviewing table schemas, checking index coverage, or debugging connection pool issues in Supabase or PostgreSQL databases. Not for application-layer ORM code.
```

**Optimization techniques:**
- Include the exact verbs users type: "create", "review", "debug", "fix", "generate"
- Include file extensions if relevant: ".tf", ".prisma", ".sql"
- Include tool/framework names: "Supabase", "Prisma", "Jira"
- Include error messages, symptoms, and synonyms users actually search for
- Author the negative space deliberately — see Negative Triggers below

### Negative Triggers: Never Fire When You Shouldn't

A skill that over-fires on neighboring intents erodes trust as fast as one that never fires. Author the negative space explicitly:

1. **Name the neighbors.** List the 2-3 skills or tasks a prompt could plausibly confuse with this one. Write one clause per *real* neighbor — generic disclaimers select for nothing.
2. **Route, don't just block.** "Skip for X (use Y)" gives the model somewhere to go; a bare "not for X" leaves it guessing. Corpus exemplars: `gemini-deep-research` ("Skip for simple lookups (answer in-session), social-media trend questions (use last30days)"); `llm-council` ("Skip for coding tasks (use Claude Code directly), for research with citations (use gemini-deep-research)").
3. **Disambiguate shared verbs.** If two skills share a verb ("review", "research", "write"), the description needs the noun that separates them ("review *migrations*" vs "review *UI code*").
4. **Two layers.** Description-level "Skip for…" shapes selection; body-level "Not for…" bullets in When to Use (see `skill-audit`) catch the case where the skill loaded anyway.

Test it: for each named neighbor, write the prompt that *should* route to the neighbor and confirm your description reads as a clear "not me."

### Claude Search Optimization (CSO)

**CRITICAL: Description = When to Use, NOT What the Skill Does.**

When a description summarizes the skill's workflow, the model can act on the summary instead of the loaded body — the description ends up competing with the very instructions it was supposed to gate.

```yaml
# BAD: Summarizes workflow - Claude takes shortcut
description: Use when executing plans - dispatches subagent per task with code review

# GOOD: Just triggering conditions, no workflow summary
description: Use when executing implementation plans with independent tasks
```

### Token Economics

Two separate bills:

- **Metadata is always paid.** Every discovered skill's name + description rides into every session whether or not the skill fires. Across a corpus this size (`ls .claude/skills | wc -l`), description bloat taxes every session — description tightness is the number-one lever. Cut the description before touching the body.
- **The body is paid only on invocation.** Targets are guidance, not caps: <200 words for frequently-invoked skills, <500 words for standard ones — while the corpus's best complex skills exceed this by design (`writing-voice-modes` runs ~300 lines). When a body outgrows its job, offload to references/ rather than deleting substance.
- Use cross-references instead of repeating content from other skills
- Reference `--help` for CLI flags instead of documenting them inline
- One excellent example beats three mediocre ones

## Progressive Disclosure Architecture

Three layers of information loading, each with increasing token cost:

| Level | What Loads | Token Cost | Strategy |
|-------|-----------|-----------|----------|
| 1. Metadata | name + description only | ~50-100, paid every session | Dense trigger phrases, no implementation details |
| 2. Instructions | Full SKILL.md body | 1k-5k, paid on invocation | Core workflow, decision trees, 2-3 inline examples |
| 3. Resources | references/ and scripts/ | Variable, paid on Read | Loaded only when Claude decides it needs them |

### What Goes Where: Description vs Body vs References

Two rules settle most authoring debates:

**Rule 1 — description vs body.** The description carries only what the model needs to decide *whether to invoke*: what it does, when to use it, trigger and negative-trigger phrases. Everything about *how to execute* goes in the body. Litmus test: if a sentence changes how Claude performs the task, it belongs in the body; if it changes whether Claude picks the skill, it belongs in the description. (This is the CSO rule and the token rule wearing the same hat.)

**Rule 2 — one reference file vs several.** Split at the *when-read* boundary: each reference file should map to exactly one "read this when [condition]" trigger you can name in SKILL.md. Content always read together stays in one file; content read under different conditions gets different files. If you cannot name a distinct read-condition for a file, it should not be a separate file. (`intent-engineering` keeps exactly one reference — one condition: writing a spec from the template.)

### When to Use references/ vs Inline

- **Inline in SKILL.md**: Content under 50 lines OR critical for every execution
- **references/ file**: Conditional content (e.g., "if using React"), lookup tables over 50 lines, pattern libraries with 3+ code examples, configuration templates

In SKILL.md, always tell Claude when to read each reference — the read-trigger and the split boundary are the same boundary:
```markdown
For the complete list of API endpoints, see references/api-endpoints.md.
For authentication flow patterns, see references/auth-patterns.md when the user mentions OAuth or JWT.
```

### Skills That Call Deferred Tools

In a tool-search harness (`ENABLE_TOOL_SEARCH` — MCP tool lazy loading, per `claude-mastery/reference/shortcuts.md`), MCP and other non-core tool schemas are deferred: the session lists tool *names* only, and the schema must be fetched with `ToolSearch` before the tool can be called. If your skill's workflow depends on such tools:

- Do not assume the schema is in context — a direct call fails validation until the schema is fetched
- Put the fetch in the body: "Load the schema first: `ToolSearch` query `select:mcp__server__tool`" — then call it
- Name exact tool strings so the fetch is copy-pasteable

Most skills never call MCP tools; add this only when yours does.

## Standard Section Order

The template for a standard skill:

1. YAML frontmatter (name + description)
2. `# Skill Title`
3. `## Purpose` - one paragraph, imperative form
4. `## When to Use` - bullet list of trigger situations, including "Not for" bullets
5. `## Examples` - 2-3 user/Claude dialog exchanges
6. `## [Domain Content]` - the bulk (60-150 lines), organized by task
7. `## Success Criteria` - testable yes/no checklist
8. `## Copy/Paste Ready` - 3-5 natural language trigger phrases

**Anchors are fixed; the middle flexes.** Frontmatter, Purpose, When to Use, Success Criteria, and Copy/Paste Ready are anchors — every skill keeps them, in this order. Complex multi-step skills may add task-specific sections in the middle: in this corpus, `skill-audit` inserts Provenance and Step 1-5 hard gates; `writing-voice-modes` adds a dozen mode sections — both keep every anchor in anchor order. What a skill may not do is drop an anchor or reshuffle them.

## TDD for Skills

Apply RED-GREEN-REFACTOR to skill creation to ensure the skill actually changes Claude's behavior:

### 1. RED: Baseline Without Skill
Test what Claude does without the skill loaded. Use a subagent so your main context stays clean:

```
Launch a subagent WITHOUT the skill loaded.
Give it the exact prompt a user would type.
Record Claude's default behavior — this is your baseline.
```

(For a quick global baseline, run the same prompt under `claude --disable-slash-commands` — all skills off. The subagent pass remains the precise isolation.)

### 2. GREEN: Write the Skill
Write the SKILL.md following the standard section order. Then test again:

```
Launch a subagent WITH the skill loaded.
Give it the same prompt.
Compare behavior to baseline — the skill should produce measurably different output.
```

If behavior is identical, the skill is not triggering or not providing actionable instructions.

### 3. REFACTOR: Close Loopholes
Test with pressure scenarios — prompts where Claude might rationalize skipping the skill's guidance:

```
"This is a simple case, just do it quickly"
"Skip the checklist, I trust you"
"We're in a hurry, just make it work"
```

If Claude bypasses the skill under pressure, add explicit loophole closers (see Rationalization Prevention below). Also red-team selection itself: feed it the neighbor prompts from Negative Triggers and confirm the skill stays quiet.

## Rationalization Prevention

For discipline-enforcing skills (verification, checklists, review gates), Claude will rationalize skipping steps under perceived time pressure. Counter this with explicit patterns:

### Loophole Closers
Add a `<HARD-GATE>` block for non-negotiable steps:

```markdown
<HARD-GATE>
Do NOT skip verification even if the fix seems obvious.
"Simple" bugs are where unexamined assumptions cause the most damage.
This applies to EVERY fix regardless of perceived simplicity.
</HARD-GATE>
```

### Common Rationalizations to Block

| Rationalization | Why It Fails | Counter |
|----------------|-------------|---------|
| "This is too simple to need X" | Simple cases are where assumptions hide | "Especially for simple cases" |
| "I already verified mentally" | Mental verification has no evidence trail | "Show the output" |
| "The user is in a hurry" | Rushing causes rework that wastes more time | "Fast is slow without verification" |
| "I just need to change one line" | One-line changes cause cascading failures | "Run the full check" |
| "The tests passed before" | Prior state is not current state | "Run tests NOW" |

### Red Flags in Skill Output
If Claude's output contains these phrases, the skill's discipline gates are being bypassed:
- "Since this is straightforward..." (skipping verification)
- "I'm confident that..." (substituting assertion for evidence)
- "Based on my earlier check..." (stale verification)
- "This should work because..." (reasoning instead of testing)

## Debugging Skills

If a skill is not firing or behaving incorrectly:

1. **Check discovery**: Run `/skills` — is it in the discovered list at all?
2. **Machine-check the basics**: `python3 scripts/validate.py` verifies SKILL.md exists, frontmatter has opening and closing `---`, `name` matches the directory, and a description is present
3. **Force invocation**: Type `/skill-name` (plugin skills need the qualified form `/plugin:skill`) — if this works, the body is fine when loaded
4. **Manual works but selection doesn't**: The description is failing on the selection surface — add the trigger phrases users actually type
5. **Fires on the wrong prompts**: Add negative triggers with routes (see Negative Triggers)
6. **Isolate skill effects**: Re-run the prompt under `claude --disable-slash-commands` (disables all skills) to confirm the behavior is skill-driven at all
7. **Debug logging**: `claude --debug` with optional category filtering (e.g. `claude --debug "api,hooks"`), or `--debug-file <path>` to capture logs for diffing

## Component Selection Guide

| Need | Use | Why |
|------|-----|-----|
| Teach Claude HOW to do something | **Skill** | Injects procedural knowledge into context |
| FORCE something to happen every time | **Hook** | Deterministic shell execution, not probabilistic |
| Offload heavy cognitive work | **Agent** | Isolated context prevents pollution |
| Quick user-triggered action | **Command** | Slash-command shortcut |

## Success Criteria

- [ ] SKILL.md has valid YAML frontmatter with name and description (`python3 scripts/validate.py` passes)
- [ ] Description states only when-to-use — trigger phrases embedded naturally, never a workflow summary
- [ ] Negative triggers name real neighbors with routes ("Skip for X — use Y") wherever adjacent skills exist
- [ ] Directory name matches the name field in frontmatter
- [ ] Anchor sections present in anchor order (Purpose, When to Use, Success Criteria, Copy/Paste Ready)
- [ ] Body within token guidance, or overflow moved to references/ — each file with a nameable "read when" condition in SKILL.md
- [ ] Any deferred-tool (MCP) dependency tells Claude to fetch the schema before calling
- [ ] Imperative form throughout (not "This skill does X")

## Copy/Paste Ready

```
"Create a new skill for [topic]"
"Improve this skill's description so it triggers better"
"Why isn't my skill auto-loading?"
"My skill keeps firing on the wrong prompts — add negative triggers"
"Write a SKILL.md for [workflow]"
"Help me structure a skill with reference files"
```
