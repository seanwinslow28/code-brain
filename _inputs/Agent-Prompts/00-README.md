# Agent Extraction System

## What This Is

A system for extracting Claude Code Agents from NotebookLM notebooks. Each domain produces 1-3 focused agents that provide structured review, judgment, or behavioral workflows. Agents are extracted using Claude Code with the NotebookLM MCP server.

This parallels the Skill Extraction System at `_inputs/GEM-Prompts/`, but extracts agents (behavioral roles) instead of skills (domain knowledge).

## Key Principle

**Skills = knowledge for execution.** Claude Code + auto-loaded skills handles all building and creating.
**Agents = structured judgment and workflows.** Agents add review criteria, severity scoring, and formatted output that skills cannot encode.

## Usage

Open Claude Code in this project directory and say:

```
Read _inputs/Agent-Prompts/00-KICKOFF-PROMPT.md and process domain 2 - Product Management
```

Or by number:

```
Read _inputs/Agent-Prompts/00-KICKOFF-PROMPT.md and process domain 2
```

Process one domain per session to stay within context limits.

## What Happens

1. Claude reads the Agent Creator Instructions and target domain prompt
2. Discovers the relevant notebook(s) via NotebookLM MCP (`notebook_list`, `notebook_describe`)
3. Queries notebooks for behavioral knowledge (`notebook_query`, `source_get_content`)
4. Generates agents following the mandatory structure template
5. Validates against the output checklist
6. Writes files to `_outputs/agents/[domain-name]/`

## Domain-to-Prompt Mapping

| # | Domain | Prompt File | Notebooks Queried | Agents Produced |
|---|--------|-------------|-------------------|-----------------|
| 1 | Claude Mastery | `01-claude-mastery.md` | 01 Core Features, 04 Advanced Techniques | security-reviewer (upgrade), compliance-summarizer (upgrade) |
| 2 | Product Management | `02-product-management.md` | 02 PM Workflows, 08 Domain-Specific | data-analyst (upgrade), scrum-master (new) |
| 3 | Creative Studio | `03-creative-studio.md` | 03 Creative Projects, 11 Remotion Mastery | game-design-advisor (upgrade), video-director (new) |
| 4 | Life Systems | `04-life-systems.md` | 05 Life Optimization | life-systems-coach (new) |
| 5 | Vault | `05-vault.md` | 06 Obsidian Integration | vault-curator (new) |

Design Team is skipped — it already has 4 rich review agents.

## Support Files

| File | Purpose |
|------|---------|
| `00-KICKOFF-PROMPT.md` | 6-phase workflow for Claude Code agent extraction |
| `00-DEPTH-ADDENDUM.md` | Format + depth requirements |
| `00-README.md` | This file |
| `Agent Creator Instructions/` | Agent anatomy, design patterns, examples, agent-vs-skill framework |

## Agent Inventory (Target: 15 Total)

| Status | Count | Agents |
|--------|-------|--------|
| Keep as-is | 7 | checklist-validator, doc-reviewer, context-gatherer, ui-reviewer, accessibility-checker, design-system-enforcer, visual-polish-auditor |
| Upgrade | 4 | security-reviewer, compliance-summarizer, data-analyst, game-design-advisor |
| New | 4 | scrum-master, video-director, life-systems-coach, vault-curator |

## After Generation

Once agents are generated for a domain:
1. Review each agent for accuracy, completeness, and behavioral focus
2. Verify output format template is complete and actionable
3. Move agents from `_outputs/agents/` to `.claude/agents/`
4. Update `export-groups/*/playground.json` manifests with new agent names
5. Update domain workspace READMEs to reference their agents
6. Smoke test: invoke each agent on a real artifact to verify quality
7. Run `python3 scripts/validate.py` to check structural integrity
