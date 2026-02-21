# Skill Extraction Kickoff Prompt

## How to Use

Open Claude Code (or Anti-Gravity IDE) in this project and specify which notebook to process:

```
Read _inputs/GEM-Prompts/00-KICKOFF-PROMPT.md and process notebook 11 - Remotion Mastery
```

Or process by number:

```
Read _inputs/GEM-Prompts/00-KICKOFF-PROMPT.md and process notebook 11
```

Process one notebook per session to stay within context limits.

---

## KICKOFF INSTRUCTIONS

You are extracting Claude Code Skills from a NotebookLM notebook using the NotebookLM MCP server. Follow this workflow exactly. Do not skip phases or reorder steps.

---

### Phase 1: Absorb Context

Read these files to understand the skill format, structural requirements, and quality bar. Read them in this order:

**Skill anatomy and design patterns** (read all 4):
- `_inputs/GEM-Prompts/Skill Creator Instructions/claude-skill-anatomy.md`
- `_inputs/GEM-Prompts/Skill Creator Instructions/skill-design-patterns.md`
- `_inputs/GEM-Prompts/Skill Creator Instructions/skill-examples.md`
- `_inputs/GEM-Prompts/Skill Creator Instructions/gem-setup.md`

**Quality and format requirements**:
- `_inputs/GEM-Prompts/00-DEPTH-ADDENDUM.md`

**Target extraction prompt** (match the notebook number the user specified):
- `_inputs/GEM-Prompts/[NN]-[name].md` (e.g., `11-remotion-mastery.md`)

**Exemplar skills** (read these to calibrate quality — these represent the bar):
- `packs/sean-custom/.claude/skills/rn-debug/SKILL.md` (172 lines, decision trees, diagnostic commands)
- `packs/sean-custom/.claude/skills/quick-prd/SKILL.md` (105 lines, interview workflow, templates)
- `packs/starter/.claude/skills/commit-checklist/SKILL.md` (short but well-structured)

After reading all files, confirm what you absorbed:
- How many skills the extraction prompt targets
- The notebook name to search for
- The domain context (who is Sean, what stack, what goal)

---

### Phase 2: Discover the Notebook

1. Call `notebook_list` to find all NotebookLM notebooks
2. Match the notebook by name from the extraction prompt (e.g., "Claude Code - Remotion Mastery")
3. Call `notebook_describe` on the matched notebook to get the AI-generated overview and suggested topics
4. Call `source_list_drive` to list all sources in the notebook
5. Report what you found: notebook name, number of sources, suggested topics

If no notebook matches, stop and ask the user to verify the notebook name.

---

### Phase 3: Extract Knowledge

For EACH target skill listed in the extraction prompt, run a focused extraction loop:

#### Step 3a: Broad Query
Call `notebook_query` with a breadth question:
```
What are the key patterns, techniques, best practices, and complete code examples
related to [SKILL TOPIC]? Include specific parameter values, configuration options,
and any lookup tables or reference data.
```

#### Step 3b: Deep Query
If the broad query reveals dense content, call `notebook_query` with a depth follow-up:
```
For [SKILL TOPIC], give me:
1. Complete working code examples (not snippets — full components with imports)
2. Specific parameter values and their effects
3. Common mistakes and how to avoid them
4. Any decision trees or conditional workflows
```

Use the `conversation_id` from Step 3a for continuity.

#### Step 3c: Source Deep Dive (when needed)
If queries reference specific sources that contain critical code or tables:
- Call `source_get_content` on those sources to get the raw text
- Extract the specific patterns, parameter tables, and configuration snippets

#### Step 3d: Cross-Reference
Check the extraction prompt's guidance for this specific skill:
- What trigger phrases should the description include?
- What priority level is it (High/Medium/Lower)?
- What specific content does the prompt say to extract?
- How does this skill connect to other domains?

Prioritize High-priority skills for deeper extraction. Lower-priority skills can be thinner but must still meet the 80-line minimum.

---

### Phase 4: Generate Skills

For each skill, generate a SKILL.md following this MANDATORY structure. Do not add, remove, or reorder sections.

```markdown
---
name: skill-name-in-kebab-case
description: One sentence describing what this does AND when Claude should auto-load it. Embed trigger phrases naturally — this is the ONLY field Claude reads to decide whether to load the skill.
---

# Skill Title

## Purpose

One paragraph explaining what this skill does and why it exists. Use imperative form. No fluff.

## When to Use

Bullet list of specific situations when Claude should activate this skill:
- Situation 1
- Situation 2
- Situation 3

## Examples

**Example 1: [Scenario name]**
```
User: "[realistic user prompt that would trigger this skill]"
Claude: [Uses skill-name] [Show the actual output pattern — what Claude produces, not a description of what it does]
```

**Example 2: [Scenario name]**
```
User: "[realistic user prompt]"
Claude: [Uses skill-name] [Show actual output]
```

## [Domain Content Sections]

This is the bulk of the skill (60-150 lines). Organize by TASK, not by concept.

Rules for this section:
- Every pattern mentioned MUST include a complete, working code example with imports
- Use tables for lookup data (spring parameters, platform specs, etc.)
- Use decision trees for troubleshooting or conditional workflows
- Reference files in references/ directory with "when to read" guidance:
  "For the complete pattern library, see references/patterns.md"
- Code must be TypeScript with proper interfaces

## Success Criteria

- [ ] Criterion 1 (testable yes/no)
- [ ] Criterion 2
- [ ] Criterion 3

## Copy/Paste Ready

```
"[Natural language trigger phrase 1]"
"[Natural language trigger phrase 2]"
"[Natural language trigger phrase 3]"
```
```

#### Reference Files

Generate a `references/` file when:
- A skill has a lookup table (spring parameters, platform specs, easing functions) exceeding 50 lines
- A skill has more than 3 complete code patterns — put the pattern library in `references/patterns.md`
- A skill has configuration templates — put them in `references/`

In SKILL.md, tell Claude WHEN to read each reference file:
```markdown
For the complete library of text animation components, see `references/text-patterns.md`.
For spring parameter combinations by motion style, see `references/motion-vocabulary.md`.
```

---

### Phase 5: Validate

Before writing ANY file, run this checklist against each skill. If a skill fails any item, fix it before proceeding.

- [ ] YAML frontmatter has `name` and `description` (description embeds trigger phrases naturally)
- [ ] Section order: Purpose > When to Use > Examples > Domain Content > Success Criteria > Copy/Paste Ready
- [ ] Examples section has 2-3 user/Claude dialog exchanges showing realistic usage
- [ ] Copy/Paste Ready section has 3-5 natural language trigger phrases
- [ ] SKILL.md body is 80-200+ lines (not under 80)
- [ ] Every mentioned pattern has a complete, working code example (with imports and interfaces)
- [ ] Reference files exist for lookup tables and pattern libraries exceeding 50 lines
- [ ] SKILL.md references its reference files with "when to read" guidance
- [ ] All code is TypeScript with proper interfaces (not loose JavaScript)
- [ ] No human-facing sections (no Design Notes, Packaging Notes, Reference Links)
- [ ] Imperative form throughout (not "This skill does X" but "Do X")
- [ ] Zero emoji anywhere — headings, body, bullet points, reference file names
- [ ] Clean markdown — no escaped characters, saveable directly as .md
- [ ] Skill directory name matches the `name` field in frontmatter

---

### Phase 6: Write to Disk

Create the output directory structure:

```
_outputs/skills/[domain-name]/
├── [skill-name-1]/
│   ├── SKILL.md
│   └── references/          (only if needed)
│       └── [name].md
├── [skill-name-2]/
│   └── SKILL.md
└── ...
```

**Domain name mapping:**

| Notebook # | Domain Name |
|------------|-------------|
| 01 | core-features |
| 02 | pm-workflows |
| 03 | creative-projects |
| 04 | advanced-techniques |
| 05 | life-optimization |
| 06 | obsidian-integration |
| 07 | technical-stack |
| 08 | domain-specific |
| 09 | community-resources |
| 10 | master-designer |
| 11 | remotion-mastery |

After writing all files, present a summary table:

| Skill Name | Lines | Reference Files | Priority | Notes |
|------------|-------|-----------------|----------|-------|
| ... | ... | ... | ... | ... |

Include:
- Total skills generated
- Any skills that couldn't meet the 80-line minimum (and why)
- Any notebook sources that were particularly useful or surprisingly empty
- Suggested next steps: review specific skills, test trigger phrases, iterate on thin ones

---

## Notebook-to-Prompt Mapping

| # | Notebook Name | Extraction Prompt | Target Skills |
|---|---------------|-------------------|---------------|
| 01 | Claude Code - Core Features | `01-core-features.md` | 6-7 |
| 02 | Claude Code - PM Workflows | `02-pm-workflows.md` | 6-7 |
| 03 | Claude Code - Creative Projects | `03-creative-projects.md` | 5-6 |
| 04 | Claude Code - Advanced Techniques | `04-advanced-techniques.md` | 6-7 |
| 05 | Claude Code - Life Optimization | `05-life-optimization.md` | 5-7 |
| 06 | Claude Code - Obsidian Integration | `06-obsidian-integration.md` | 5-6 |
| 07 | Claude Code - Technical Stack | `07-technical-stack.md` | 5-6 |
| 08 | Claude Code - Domain Specific | `08-domain-specific.md` | 4-5 |
| 09 | Claude Code - Community Resources | `09-community-resources.md` | 4-5 |
| 10 | Claude Code - Master Designer | `10-master-designer.md` | 6-8 |
| 11 | Claude Code - Remotion Mastery | `11-remotion-mastery.md` | 6-8 |

---

## Format Rules (Quick Reference)

Internalize these before generating any skill. They are non-negotiable.

1. **YAML frontmatter**: `name` + `description` only. No other fields.
2. **Description**: Embed trigger phrases naturally. This is the ONLY field Claude reads to decide whether to load the skill. Write it like: "React Native debugging assistant. Diagnoses build failures, red screens, and performance issues systematically." NOT a keyword list.
3. **Imperative form**: "Use spring() for natural motion" not "This skill uses spring()"
4. **No human-facing sections**: No Design Notes, Packaging Notes, Installation Guide, README content. If you want to tell Sean something, put it in your response text, not in the SKILL.md.
5. **No emoji**: Zero. None in headings, bullet points, file names, or body text.
6. **TypeScript only**: All code uses strict TypeScript with proper interfaces. No loose JavaScript.
7. **Clean markdown**: No escaped characters (`\---`, `\#\#`). Output raw markdown saveable as .md.
8. **Directory = name**: The skill folder name must match the `name` field in frontmatter.
9. **80-200+ lines**: Per SKILL.md body. Under 80 means you compressed too far.
10. **Complete code examples**: Every pattern includes a working example with imports and interfaces. "Use text.split().map()" is NOT enough.

---

## Compression Rules

- **DO compress**: Conceptual explanations Claude already knows (what React is, what TypeScript is, what animation means, how imports work)
- **DO NOT compress**: Specific parameter values, component code, configuration snippets, lookup tables, domain-specific patterns, spring configs, platform specs — these are WHY the skill exists
- **The test**: After writing the skill, could Claude implement every pattern from ONLY what's in the skill, without guessing? If not, you compressed too far.

---

## Sean's Context (for skill content)

- Associate PM (Technical) at The Block (crypto data/news)
- Beginner coder learning fundamentals through Claude Code
- Stack: React, TypeScript, Python, Supabase, Expo/React Native
- Building domain-specific Claude Code playgrounds (one per notebook topic)
- Has `remotion-docs` MCP server installed globally
- The Block brand: Primary #1A1A2E, Accent #E94560, Background #0F3460, Text #FFFFFF
