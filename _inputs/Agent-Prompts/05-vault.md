# Vault — Agent Extraction Prompt

Use this prompt with the **Agent Extraction Kickoff** after connecting to the **"Claude Code - Obsidian Integration"** NotebookLM notebook.

---

## PROMPT START — Process this domain with the Kickoff Prompt

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I maintain an Obsidian vault as my second brain, organized with the PARA methodology (Projects, Areas, Resources, Archive). The vault lives at `vault/` in this repo and includes Maps of Content (MOCs), note templates, a prompts library, and a RAG directory for AI-compatible knowledge chunks.

I'm creating a new agent for the Vault domain. This agent provides **structured vault health evaluation and organization recommendations** — the 6 vault skills handle Obsidian feature knowledge (MCP setup, Dataview queries, semantic search, etc.).

## What's in This Notebook

**Notebook: "Claude Code - Obsidian Integration"** (321 sources)
Obsidian vault architecture, PARA methodology, knowledge management, Zettelkasten principles, MOC patterns, frontmatter conventions, Dataview queries, semantic search, MCP integration, note linking strategies, vault maintenance workflows. Extensive source coverage.

## Your Task

Extract behavioral knowledge from this notebook and generate **1 new agent** for the Vault domain.

## Target Agents

### 1. NEW: vault-curator
**Priority**: Medium
**Type**: Workflow agent (read-write, needs to read vault files and potentially organize/move notes)
**disallowedTools**: (none — needs full tool access to scan and organize vault)

**What to extract from notebooks**:
- Vault health dimensions:
  - **Structural Health**: PARA folder compliance (are notes in the right category?), folder depth (too flat? too nested?), consistent naming conventions, README/index note presence in key folders
  - **Frontmatter Completeness**: Do notes have required fields (title, created, tags, domain, status)? Are tags from a controlled vocabulary? Are dates in ISO format?
  - **Linking Health**: Bidirectional link density (orphan notes with zero links?), link-to-note ratio, broken links, dead-end notes (links out but nothing links in), hub notes that connect clusters
  - **Inbox Processing**: How many notes are in `00-Inbox/`? How old are they? Are they being processed or accumulating? Time-to-process metric.
  - **Tag Consistency**: Are similar concepts tagged differently? Tag sprawl (too many low-use tags)? Missing tags on recent notes?
  - **Content Freshness**: Notes not updated in 90+ days, stale project notes for completed projects, archive candidates
- MOC maintenance: when to create a new MOC (cluster of 5+ related notes without a hub), when to split an overgrown MOC, how to identify emerging topic clusters from link patterns
- PARA compliance: criteria for each category (Projects = active with deadline, Areas = ongoing responsibility, Resources = reference material, Archive = inactive/completed)
- Vault maintenance workflow: inbox triage → categorize → link → tag → archive cycle
- Knowledge graph health: what a healthy graph looks like vs an unhealthy one (isolated clusters, star topology around one hub, etc.)

**Output format requirements**:
- Vault Health Report with scan date
- Per-dimension assessment:
  - Status (Healthy / Needs Attention / Unhealthy)
  - Key metric (e.g., "12 orphan notes", "87% frontmatter complete")
  - Specific findings list
- Inbox Status: count, oldest note age, recommendation
- Orphan Notes list (notes with zero inbound links)
- Stale Content list (notes not updated in 90+ days in active folders)
- Archive Candidates (completed project notes still in Projects)
- Tag Health: most-used tags, unused tags, suggested consolidations
- Top 3 recommended actions (prioritized by impact)

**Trigger phrases**: "vault review", "vault health check", "organize my notes", "clean up Obsidian", "knowledge graph maintenance", "process my inbox", "find orphan notes", "vault audit"

## Extraction Guidance

- This agent is a DIAGNOSTIC WORKFLOW agent — it scans vault structure, evaluates health metrics, and produces a structured report with recommendations.
- Focus on CONCRETE METRICS: number of orphan notes, frontmatter completion percentage, inbox age, link density. Not vague "is the vault organized?"
- The PARA methodology is central: the agent should know what belongs where and flag misplacement.
- Include practical thresholds: e.g., "inbox > 20 notes → Needs Attention", "orphan notes > 10% of total → Unhealthy", "frontmatter completion < 80% → Needs Attention"
- The vault structure is:
  ```
  vault/
  ├── .obsidian/
  ├── 00-Inbox/
  ├── 01-Projects/
  ├── 02-Areas/
  ├── 03-Resources/
  ├── 04-Archive/
  ├── Prompts/
  ├── MOCs/
  ├── Templates/
  └── RAG/
  ```

## Cross-Domain Notes

- Pairs with `vault-architecture`, `vault-read-write`, `vault-automation`, `obsidian-mcp-setup`, `knowledge-graph-nav`, `obsidian-semantic-search` skills
- Pairs with `life-systems-coach` agent (weekly reviews may generate notes that need vault processing)
- The RAG/ directory connects to MCP-based retrieval — agent should check RAG chunk health too
- MOCs link to domain workspaces (Claude Mastery MOC, PM MOC, Creative Studio MOC, etc.)

## Quality Bar

The generated agent should:
- Be 80-120 lines (Rich tier)
- Have concrete health metrics with specific thresholds (not "check if vault is organized")
- Include a complete vault health report template
- Reference the PARA structure and MOC patterns
- Reference real skills from the vault domain

---

## PROMPT END
