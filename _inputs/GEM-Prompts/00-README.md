# Skill Extraction System

## What This Is

A system for extracting Claude Code Skills from 11 NotebookLM notebooks. Each notebook covers a specific domain and produces 4-8 focused skills that form a cohesive playground.

Two extraction methods are available:

| Method | Tool | Best For |
|--------|------|----------|
| **Kickoff Prompt** (recommended) | Claude Code / Anti-Gravity IDE + NotebookLM MCP | Direct control, native format, writes to disk |
| **GEM Prompts** (original) | Gemini GEM + manual copy/paste | When MCP access isn't available |

## Method 1: Kickoff Prompt (Recommended)

Uses Claude Code (or Anti-Gravity IDE) with the NotebookLM MCP server to query notebooks directly and generate skills in the correct format.

### Usage

Open Claude Code in this project directory and say:

```
Read _inputs/GEM-Prompts/00-KICKOFF-PROMPT.md and process notebook 11 - Remotion Mastery
```

Or by number:

```
Read _inputs/GEM-Prompts/00-KICKOFF-PROMPT.md and process notebook 3
```

### What Happens

1. Claude reads the Skill Creator Instructions, addendum, and target extraction prompt
2. Discovers the notebook via NotebookLM MCP (`notebook_list`, `notebook_describe`)
3. Queries the notebook for each target skill (`notebook_query`, `source_get_content`)
4. Generates skills following the mandatory structure template
5. Validates against the output checklist
6. Writes files to `_outputs/skills/[domain-name]/`

### Why This Is Better

- Claude Code knows its own skill format natively — no translation layer
- Direct MCP access to notebook sources — no manual copy/paste
- Reads existing project skills for quality calibration
- Writes files directly to disk
- Validates output in real-time

### One Notebook Per Session

Process one notebook at a time to stay within context limits. Each session produces 4-8 skills for that domain.

## Method 2: GEM Prompts (Original)

Uses the Gemini Claude SKILL Creator GEM. Requires manual copy/paste of prompts and output.

### Usage

1. Open your **Claude SKILL Creator** GEM in Gemini
2. Ensure the target NotebookLM notebook is connected as a source
3. Copy-paste the relevant prompt file (e.g., `11-remotion-mastery.md`) into the GEM
4. **Append the Depth Addendum** — paste `00-DEPTH-ADDENDUM.md` after the prompt
5. Review and manually export the generated Skills

### Why the Depth Addendum Matters

The GEM's default compression produces skills that are structurally correct but too thin (~15 lines per skill). The addendum overrides this by setting minimum content depth (80-200 lines), requiring complete code examples, and enforcing the mandatory section structure.

## Prompt Files

| # | File | NotebookLM Notebook | Target Skills |
|---|------|---------------------|---------------|
| 01 | `01-core-features.md` | Claude Code - Core Features | 6-7 skills |
| 02 | `02-pm-workflows.md` | Claude Code - PM Workflows | 6-7 skills |
| 03 | `03-creative-projects.md` | Claude Code - Creative Projects | 5-6 skills |
| 04 | `04-advanced-techniques.md` | Claude Code - Advanced Techniques | 6-7 skills |
| 05 | `05-life-optimization.md` | Claude Code - Life Optimization | 5-7 skills |
| 06 | `06-obsidian-integration.md` | Claude Code - Obsidian Integration | 5-6 skills |
| 07 | `07-technical-stack.md` | Claude Code - Technical Stack | 5-6 skills |
| 08 | `08-domain-specific.md` | Claude Code - Domain Specific | 4-5 skills |
| 09 | `09-community-resources.md` | Claude Code - Community Resources | 4-5 skills |
| 10 | `10-master-designer.md` | Claude Code - Master Designer | 6-8 skills |
| 11 | `11-remotion-mastery.md` | Claude Code - Remotion Mastery | 6-8 skills |

## Support Files

| File | Purpose |
|------|---------|
| `00-KICKOFF-PROMPT.md` | Kickoff prompt for Claude Code / Anti-Gravity IDE |
| `00-DEPTH-ADDENDUM.md` | Format + depth requirements (used by both methods) |
| `00-README.md` | This file |
| `Skill Creator Instructions/` | Skill anatomy, design patterns, examples, GEM setup |

## Architecture

Each extraction prompt contains:
- **Shared preamble**: Sean's profile, goals, and quality standards
- **Domain context**: What this notebook covers and why it matters
- **Target skills**: Specific skills to extract with descriptions and priority
- **Extraction guidance**: Domain-specific instructions
- **Cross-domain notes**: How these skills connect to other playgrounds

## Design Principle

Each notebook becomes its own **domain-specific playground** — a self-contained Claude Code environment with skills tailored to that topic. Skills within a playground should work together as a cohesive toolkit, not as isolated capabilities.

## After Generation

Once skills are generated for a domain:
1. Review each SKILL.md for accuracy and completeness
2. Test the skill in Claude Code to verify trigger phrases work
3. Place skills in the appropriate domain pack directory
4. Update the domain's CLAUDE.md to reference the new skills
5. Cross-reference with other domains where skills overlap
