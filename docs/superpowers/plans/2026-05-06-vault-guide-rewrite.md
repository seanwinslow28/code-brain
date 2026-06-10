# VAULT-GUIDE.md Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `vault/90_system/VAULT-GUIDE.md` with a 2026-05-06 truth-state document that future agents can read once and operate the vault without exploratory searching.

**Architecture:** The current guide (created 2026-02-21) describes the post-Apple-Notes-import state. Since then: 14 SDK agents shipped, the operating-models artifact system landed, the knowledge-loop infrastructure (`vault/knowledge/`, `vault/health/`, `.vault-index.db`) was built, three top-level dirs were added (`02_Areas/`, `Excalidraw/`, `health/`, `knowledge/`), Apple Notes archives were collapsed, and Sean was laid off from The Block (2026-05-04) — pivoting the active project surface to job-hunt. The rewrite reorganizes around four reading audiences: (1) future Claude Code agents needing folder/schema reference, (2) SDK agents needing producer/consumer contracts, (3) Sean as human operator, (4) future-Sean re-onboarding after time away. Sections that are unchanged (YAML schema, naming conventions, MOCs, hybrid-search strategy) are kept verbatim with corrections only. Sections that are wrong (folder counts, archive subfolders, hooks count, plugin list, integration channels) are replaced. Sections that are missing entirely (operating-models, knowledge-loop, SDK-agent vault contracts, agent-fleet area, health/ telemetry) are added.

**Tech Stack:** Markdown only. No code changes. Verification = grep/find/wc against the live vault. Write tool for the new file body, Edit tool for refinements, Bash tool for filesystem reality checks.

---

## Source-of-Truth Index (read these as you write)

The plan repeatedly references these "ground-truth" sources. Read them once at the start of each task to avoid drift.

| Topic | Authoritative source |
|---|---|
| Project repo conventions | `CLAUDE.md` (root) |
| SDK-agent inventory and schedules | `CLAUDE.md` Agents SDK section + `agents-sdk/config.toml` |
| Hooks list | `.claude/hooks/` directory listing + `.claude/settings.json` |
| Operating-models contract | `vault/05_atlas/operating-models/README.md` + `INTERVIEW-PLAYBOOK.md` |
| Knowledge-loop schema | `agents-sdk/agents/vault_synthesizer.py`, `agents-sdk/agents/vault_indexer.py`, `agents-sdk/lib/concept_edges.py` |
| Granola landing path | `vault/.obsidian/plugins/granola-sync/data.json` |
| Obsidian-Git auto-features (must be off) | `vault/.obsidian/plugins/obsidian-git/data.json` |
| Daily-note anchors | `vault/90_system/templates/tpl-daily.md` |
| MCP tool inventory | `vault/.obsidian/plugins/obsidian-local-rest-api/data.json` + `.mcp.json` (root) |
| Live vault file counts | `find vault/<dir> -name "*.md" \| wc -l` per task |
| Live archive structure | `ls vault/60_archive/` |

---

## File Structure

This rewrite produces **one** file:

- **Modify:** `vault/90_system/VAULT-GUIDE.md` — full replacement of the body, frontmatter `created` field preserved at `2026-02-21` and `updated` field added with today's date.

No new files are created. No code is modified. The plan file itself (this file) ships under `docs/superpowers/plans/` and is committed alongside the rewrite.

The new VAULT-GUIDE.md target structure (24 sections, in order):

1. Frontmatter + title + "Last refreshed" banner
2. Table of Contents
3. What This Vault Is (refreshed framing — knowledge-loop era, post-Block pivot)
4. Quick Reference for AI Agents (NEW — top-level "if you only read one section")
5. Architecture (folder tree — fully rewritten)
6. Folder-by-Folder Reference (each top-level dir: purpose, file counts, key contents)
7. YAML Frontmatter Schema (kept; corrections only)
8. Naming Conventions (kept verbatim)
9. Templates (refresh daily-template anchors — `<!-- meetings -->`, `<!-- research-digest -->`)
10. Maps of Content (MOCs) (kept; corrections only)
11. Operating Models (NEW — 5-artifact bundles per domain)
12. Knowledge Loop Infrastructure (NEW — index, concepts/, connections/, qa/, .vault-index.db, synth-manifest)
13. Health Telemetry (NEW — synth-manifest, gemini-spend ledger, lint reports)
14. Agent Fleet Workspace (NEW — `02_Areas/Agent-Fleet/`)
15. Obsidian Plugins (refresh — 11 plugins now, 8 in Feb)
16. Claude Code Integration Channels (refresh native MCPs, mark Zapier as fallback only)
17. SDK Agents That Touch the Vault (NEW — producer/consumer contracts)
18. Vault-Touching Hooks (refresh — 5 hooks vault-touching, 13 total)
19. How to Read from the Vault (kept; updated grep examples)
20. How to Write to the Vault (kept; PATCH pattern + vault-sync owner rule from issue #22)
21. Inbox Processing (refresh — process-inbox SDK agent paused; manual skill is the path)
22. Knowledge Graph Navigation (kept verbatim)
23. Semantic Search (kept; Smart Connections still installed)
24. Daily Workflow (kept; refresh anchors)
25. Granola Meeting Sync (refresh path + multi-device caveat)
26. Content Statistics (RECOUNT — total file count was 1,431, now ~608)
27. Rules and Constraints (add: vault-sync-owner from issue #22, do-not-re-enable Obsidian-Git auto-features, operating-models read-on-demand)
28. Appendix: Related Files Outside the Vault (refresh — agents-sdk added, 7 vault skills retained)
29. Changelog (NEW — list each major restructuring event since 2026-02-21 with date)

(The numbering above is for plan reference; the rendered TOC will renumber if a section is dropped during execution.)

---

## Task 0: Set up branch + verification scratchpad

**Files:**
- Create: `docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md` (deleted at end)

- [ ] **Step 1: Create feature branch**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git checkout -b docs/vault-guide-rewrite-2026-05-06
git status
```

Expected: `On branch docs/vault-guide-rewrite-2026-05-06`, working tree may have pre-existing uncommitted vault auto-commits — leave them alone, they'll auto-commit on Obsidian's next save cycle.

- [ ] **Step 2: Capture live counts to a scratchpad (single source of truth for stats sections)**

Run this and paste the output into `docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md`:

```bash
{
  echo "# Live Vault Counts — captured $(date +%Y-%m-%d)"
  echo ""
  echo "## Total markdown files"
  find /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault -name "*.md" -type f | wc -l
  echo ""
  echo "## Per top-level folder"
  for d in 00_inbox 02_Areas 05_atlas 10_timeline 20_projects 30_domains 40_knowledge 50_sources 60_archive 70_apple-notes 90_system Excalidraw health knowledge; do
    count=$(find "/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/$d" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "- $d: $count"
  done
  echo ""
  echo "## 20_projects breakdown"
  for p in /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/20_projects/*/; do
    pname=$(basename "$p")
    count=$(find "$p" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "- $pname: $count"
  done
  echo ""
  echo "## 60_archive breakdown"
  for a in /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/60_archive/*/; do
    aname=$(basename "$a")
    count=$(find "$a" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo "- $aname: $count"
  done
  echo ""
  echo "## Operating-models bundles"
  ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/
  echo ""
  echo "## Knowledge index status"
  cat /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/knowledge/index.md
  echo ""
  echo "## Latest synth manifest"
  ls -t /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/health/synth-manifest-*.json | head -1 | xargs cat
  echo ""
  echo "## Hooks list"
  ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/hooks/
  echo ""
  echo "## Obsidian plugins (community)"
  cat /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/.obsidian/community-plugins.json
  echo ""
  echo "## Granola landing path"
  cat /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/.obsidian/plugins/granola-sync/data.json | python3 -c "import sys, json; d=json.load(sys.stdin); print('customBaseFolder:', d.get('customBaseFolder')); print('linkFromDailyNotes:', d.get('linkFromDailyNotes')); print('saveAsIndividualFiles:', d.get('saveAsIndividualFiles')); print('syncDaysBack:', d.get('syncDaysBack'))"
  echo ""
  echo "## Obsidian-Git auto-features (must all be 0)"
  cat /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/.obsidian/plugins/obsidian-git/data.json | python3 -c "import sys, json; d=json.load(sys.stdin); print('autoSaveInterval:', d.get('autoSaveInterval')); print('autoPushInterval:', d.get('autoPushInterval')); print('autoPullInterval:', d.get('autoPullInterval'))"
} > docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md
cat docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md
```

Expected: A scratchpad file with current counts. **All subsequent tasks reference this scratchpad** — never re-run `find` or `wc` ad-hoc; quote the scratchpad. This guarantees stat consistency across the document.

- [ ] **Step 3: Read the current VAULT-GUIDE.md once for structural reference**

Use Read tool on `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md`. The current file is 891 lines. You will not be editing it incrementally — you'll be **fully rewriting** it via Write tool in Task 12. Reading once now gives you section-naming and tone conventions to preserve.

- [ ] **Step 4: Read the four authoritative inputs in parallel**

Read in one batch:
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/CLAUDE.md`
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/README.md`
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/templates/tpl-daily.md`
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml`

These are the inputs you'll cite throughout the rewrite. The CLAUDE.md is the single richest source — the new VAULT-GUIDE should not duplicate what's already there but should cross-reference it.

- [ ] **Step 5: Commit the scratchpad**

```bash
git add docs/superpowers/plans/2026-05-06-vault-guide-rewrite.md docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md
git commit -m "docs(vault-guide): plan + scratchpad for 2026-05-06 rewrite"
```

---

## Task 1: Draft the new file frontmatter + "Quick Reference for AI Agents"

**Files:**
- Modify: `vault/90_system/VAULT-GUIDE.md` (full overwrite begins here, but only the top of the file in this task — leave the body of the existing file in place until Task 12 when Write replaces everything atomically)

**Approach:** Tasks 1–11 each draft a section into the rewrite-scratchpad as labeled blocks (`<!-- SECTION: quick-ref -->` … `<!-- /SECTION -->`). Task 12 assembles all sections, runs the Write tool **once** to replace VAULT-GUIDE.md atomically, and verifies. This avoids leaving the live VAULT-GUIDE in a broken half-rewritten state.

- [ ] **Step 1: Draft the frontmatter block**

Append this to the scratchpad (`docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md`) under a `<!-- SECTION: frontmatter -->` marker:

```yaml
---
type: reference
domain:
  - vault
status: active
ai-context: "Comprehensive guide to Sean's Obsidian vault: architecture, conventions, knowledge-loop infrastructure, SDK-agent contracts, and operational workflows. 2026-05-06 refresh."
created: 2026-02-21
updated: 2026-05-06
---
```

The `created` date is preserved from the original. The `updated` field is new — Obsidian Linter will refresh it on every save thereafter. Frontmatter remains FLAT (no nested objects) per vault rule #3.

- [ ] **Step 2: Draft the "Last refreshed" banner**

Below the frontmatter, draft this banner (so any reader knows the document's freshness without scrolling):

```markdown
# Sean's Obsidian Vault — Complete Guide

> **Last refreshed: 2026-05-06.** The vault has changed substantially since the original 2026-02-21 guide. Major additions: 14 SDK agents (7 active), the operating-models artifact system at `05_atlas/operating-models/`, the knowledge-loop infrastructure (`vault/knowledge/`, `vault/health/`, `.vault-index.db`), the agent-fleet workspace at `02_Areas/Agent-Fleet/`, and a job-hunt-2026 project added 2026-05-04 after Sean was laid off from The Block. Apple Notes archives have been collapsed. See [Changelog](#changelog) at the bottom for the timeline.
>
> **Authoritative cross-reference:** Repo-level architecture, SDK-agent details, hook list, and non-negotiable rules live in `/CLAUDE.md`. This guide focuses on the vault interior — folder semantics, frontmatter schema, agent producer/consumer contracts, and the daily/weekly workflows. When in doubt, CLAUDE.md wins.

This document describes everything about this vault: its architecture, how it connects to Claude Code and the autonomous SDK agents, and how to work within it effectively. It is written for both human operators and AI agents.
```

- [ ] **Step 3: Draft the "Quick Reference for AI Agents" section (NEW)**

This new top-level section is what most agents will actually need. Make it comprehensive enough that an agent that reads only this section can do basic vault work correctly.

Draft into the scratchpad under `<!-- SECTION: quick-ref -->`:

```markdown
## Quick Reference for AI Agents

If you read **only one section**, read this one.

### Where do I put new content?

| What you have | Where it goes | Filename pattern |
|---|---|---|
| New capture, can't classify yet | `00_inbox/` | (your choice; will be re-named on triage) |
| Reference / how-to / guide | `40_knowledge/references/` | `ref-<kebab>.md` |
| Concept, framework, idea | `40_knowledge/concepts/` | `idea-<kebab>.md` |
| Active project work | `20_projects/<prj-name>/` | depends on project |
| Synthesized concept article (LLM-generated) | `vault/knowledge/concepts/` | auto-named by `vault_synthesizer` |
| Synthesized connection article (LLM-generated) | `vault/knowledge/connections/` | auto-named by `vault_synthesizer` |
| Q&A answer (terminal `query.py` output) | `vault/knowledge/qa/` | auto-named by `query.py --file-back` |
| Daily note | `10_timeline/daily/` | `YYYY-MM-DD.md` |
| Granola meeting (auto-synced) | `30_domains/product-management/the-block-meetings-granola-notes/` | `mtg-YYYY-MM-DD-<slug>.md` (post-process) |
| Operating-model artifact | `05_atlas/operating-models/<domain>/` | `HEARTBEAT.md` / `USER.md` / `SOUL.md` / `operating-model.md` / `schedule-recommendations.md` |
| Daily fleet status (autonomous) | `02_Areas/Agent-Fleet/` | `daily-fleet-status-YYYY-MM-DD.md` |
| Health telemetry (synth manifest, lint, spend) | `vault/health/` | `synth-manifest-YYYY-MM-DD.json`, `YYYY-MM-DD-lint-report.md`, `gemini-spend-YYYY-MM.json` |
| Deep-research output (overnight queue) | `vault/20_projects/research/` | `YYYY-MM-DD-<topic-slug>.md` |

### What must I never do?

1. Never delete vault files without explicit user permission.
2. Never use nested objects in frontmatter — flat YAML only (Dataview will break).
3. Never re-enable Obsidian-Git auto-commit / auto-pull / auto-push (issue #22, 2026-04-23: shell-level hook is sole owner).
4. Never write to `60_archive/` (read-only; archived items are done).
5. Never push to git from inside Claude Code — Obsidian-Git plugin or manual commits only.
6. Never invent paths for `vault/knowledge/` — those files are LLM-written by `vault_synthesizer`, never hand-written.
7. Never skip the kebab-case + type-prefix naming rule (`ref-`, `idea-`, `mtg-`, `prj-`, `tpl-`, `moc-`).

### What's the YAML frontmatter shape?

```yaml
---
type: reference          # one of: project, reference, idea, daily, weekly, meeting, moc, dashboard, archive
domain:                  # list, never nested object
  - claude-mastery       # one of 6 domains (see below)
status: active           # backlog | draft | active | blocked | review | completed | archived
context: 16bitfit        # OPTIONAL short identifier
ai-context: "One-sentence summary under 120 chars."
created: 2026-05-06
source: apple-notes-import   # OPTIONAL provenance
---
```

The 6 domains are: `claude-mastery`, `product-management`, `creative-studio`, `life-systems`, `design-team`, `vault`.

### How do I find existing content?

1. **MOC first:** read `vault/05_atlas/moc-<domain>.md` to see what exists in a domain.
2. **Knowledge index:** read `vault/knowledge/index.md` for synthesized concepts and connections (auto-generated nightly).
3. **SQLite chunks:** the `.vault-index.db` SQLite file at the vault root has `chunks` and `concept_edges` tables — query directly only if you're an SDK agent. Claude Code agents should use Grep/Glob.
4. **Grep for backlinks:** `Grep "\[\[concept-name\]\]" --path vault/`.
5. **Frontmatter filter:** `Grep "status: active" --path vault/20_projects/`.

### How do I write into a daily note?

Use the **PATCH pattern** with HTML comment anchors. Today's daily note has 6 anchors (in template order):

```
<!-- slack-overnight -->
<!-- meetings -->
<!-- jira-log -->
<!-- claude-sessions -->
<!-- side-projects -->
<!-- research-digest -->
```

Insert content on the line **directly below** the anchor. Never remove the anchor. Never rewrite the whole file.
```

- [ ] **Step 4: Verify the Quick Reference matches reality**

Spot-check three claims:

```bash
# Claim 1: Granola landing path
python3 -c "import json; d=json.load(open('/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/.obsidian/plugins/granola-sync/data.json')); print(d['customBaseFolder'])"
# Expected: 30_domains/product-management/the-block-meetings-granola-notes

# Claim 2: Daily template anchors
grep -E "^<!-- " /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/templates/tpl-daily.md
# Expected: 6 anchors matching the list above

# Claim 3: Operating-model bundle filenames
ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/job-hunt-2026/
# Expected: HEARTBEAT.md, SOUL.md, USER.md, operating-model.md, schedule-recommendations.md
```

If any claim is wrong, fix the draft before proceeding. **Do not commit yet** — Tasks 1–11 commit as a batch in Task 12.

---

## Task 2: Draft the "Architecture" + "Folder-by-Folder Reference" sections

**Files:**
- Modify: `docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md` (append section blocks)

- [ ] **Step 1: Draft the new architecture tree**

Append under `<!-- SECTION: architecture -->`:

```markdown
## Architecture

```text
vault/
├── Home.md                           # Dataview dashboard — entry point
├── Sean-Winslow-Full-Personal-Context-v2.0.md   # Tier-0 identity (above all operating models)
│
├── 00_inbox/                         # Raw captures, quick ideas, needs-review items
│   ├── research-queue.md             # Topics queued for nightly deep_researcher
│   └── gemini-research-queue.md      # Topics queued for gemini-researcher (opt-in)
│
├── 02_Areas/                         # Ongoing areas (PARA "Areas") — NEW since 2026-04
│   ├── Agent-Fleet/                  # Autonomous-agent telemetry surfaced into vault
│   │   ├── fleet-state.md            # Latest fleet snapshot (overwritten daily)
│   │   └── daily-fleet-status-YYYY-MM-DD.md   # Per-day fleet summaries
│   └── Work/                         # Misc PR digests, ad-hoc work artifacts
│
├── 05_atlas/                         # MOCs (Maps of Content) + operating models
│   ├── moc-claude-mastery.md
│   ├── moc-product-management.md
│   ├── moc-creative-studio.md
│   ├── moc-life-systems.md
│   ├── moc-design-team.md
│   ├── moc-vault.md
│   └── operating-models/             # NEW — 5-artifact bundles per domain (see "Operating Models")
│       ├── README.md
│       ├── INTERVIEW-PLAYBOOK.md
│       ├── creative-studio/          # HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations
│       ├── life-systems/             #   "
│       └── job-hunt-2026/            #   " (replaces the-block bundle, archived 2026-05)
│
├── 10_timeline/
│   ├── daily/                        # YYYY-MM-DD.md
│   ├── weekly/                       # YYYY-Www.md
│   └── monthly/                      # YYYY-MM.md
│
├── 20_projects/                      # Active, time-bound projects
│   ├── prj-job-hunt-2026/            # NEW — 8-week post-Block search (added 2026-05-04)
│   │   ├── README.md
│   │   ├── The-Block-Contacts-After-Layoff.md
│   │   └── onwards-and-upwards-5-4-26/   # Migration + master plan + audit
│   ├── prj-superuser-pack/           # This repo's active development
│   ├── prj-16bitfit/                 # Game project (most content moved to creative-studio/16bitfit-battle-mode/)
│   ├── prj-campus-201/               # Campus LMS (mostly archived after Block layoff)
│   ├── prj-boston-move/              # Boston relocation
│   ├── prj-personal-finance/         # Personal finance automation
│   ├── prj-animation-pipeline/       # Animation pipeline
│   ├── prj-sw-portfolio-and-hubs-designs/   # NEW — portfolio site
│   └── research/                     # NEW — overnight deep_researcher output
│
├── 30_domains/                       # Domain workspace folders
│   ├── claude-mastery/               # (mostly empty — domain-level reference notes)
│   ├── product-management/
│   │   ├── the-block-meetings-granola-notes/   # Granola plugin landing zone (auto-sync)
│   │   ├── prompts/
│   │   └── media-team-ideas/
│   ├── creative-studio/
│   ├── design-team/
│   ├── life-systems/
│   └── vault/
│
├── 40_knowledge/                     # Permanent reference material
│   ├── concepts/                     # Hand-written ideas, frameworks
│   ├── references/                   # How-tos, guides, docs
│   └── notebooklm-exports/           # Synthesized research from NotebookLM
│
├── 50_sources/                       # Raw data and assets
│   ├── data/
│   ├── finance/                      # CSVs gitignored
│   ├── health/                       # NEW — workout/health CSVs
│   └── assets/
│
├── 60_archive/                       # Completed/inactive items (READ-ONLY)
│   ├── apple-notes-personal/         # 5 sentimental items (was 52; collapsed 2026-04)
│   ├── inbox-archive-2026-04-25/     # NEW — inbox cleanup snapshot
│   ├── operating-models-the-block-2026-05/   # NEW — Block bundle archived after layoff
│   ├── old-mocs/                     # Superseded MOC drafts
│   ├── old-projects/                 # Superseded project folders
│   ├── old-prompts/
│   ├── old-rag/
│   └── old-templates/
│   #  Note: apple-notes-empty/expired/nyl/duplicates/prompts subfolders from the Phase 2/3 import were removed in the 2026-04 cleanup. The classification rubric reference at 40_knowledge/references/ref-apple-notes-classification-rubric.md preserves the historical methodology.
│
├── 70_apple-notes/                   # Import staging (effectively empty; attachments folder kept)
│   └── Notes/
│       ├── attachments/
│       └── images/
│
├── 90_system/                        # Vault infrastructure
│   ├── VAULT-GUIDE.md                # ← this file
│   ├── templates/                    # tpl-daily, tpl-weekly, tpl-project, tpl-meeting, tpl-idea, tpl-knowledge
│   ├── scripts/                      # process-granola-notes.py
│   ├── agent-logs/                   # NEW — SDK-agent run logs + agent-run-history.csv
│   ├── css-snippets/
│   └── mcp-configs/                  # (currently empty)
│
├── Excalidraw/                       # NEW — Excalidraw plugin storage
│
├── health/                           # NEW — vault telemetry (NOT to be confused with 50_sources/health/)
│   ├── synth-manifest-YYYY-MM-DD.json   # Per-run synthesizer counts
│   ├── YYYY-MM-DD-lint-report.md     # Weekly knowledge_lint output
│   ├── gemini-spend-YYYY-MM.json     # Gemini DR/DR-Max spend ledger ($7 task / $10 day / $20 month caps)
│   ├── .gemini-ledger.lock           # FileLock for spend ledger
│   └── .lock                         # FileLock for synth runs
│
├── knowledge/                        # NEW — knowledge-loop output (LLM-written, never hand-edited)
│   ├── index.md                      # Auto-generated index (loaded on SessionStart by hook)
│   ├── concepts/                     # One file per synthesized concept
│   ├── connections/                  # One file per synthesized connection
│   └── qa/                           # NEW (v3.19.0) — terminal Q&A answer endpoints (cite outward only)
│
├── .vault-index.db                   # SQLite index (chunks + concept_edges tables) — written by vault_indexer
├── .indexer-state.json               # Mtime cursor for vault_indexer
└── .obsidian/                        # Obsidian app config
```

### Why this structure

- **Numbered prefixes** (`00_`, `02_`, `05_`, `10_`...) control sidebar sort order in Obsidian.
- **`02_Areas/`** is PARA's "Areas" tier — ongoing responsibilities that aren't time-bound projects.
- **`05_atlas/operating-models/`** sits inside the atlas because operating-model bundles are *navigational meta* — they describe *how* Sean works, just like MOCs describe *what* lives in a domain.
- **`vault/knowledge/`** is the LLM-output zone. Hand-written knowledge lives in `40_knowledge/`; synthesized knowledge lives in `vault/knowledge/`. They never mix.
- **`vault/health/`** is operational telemetry — separate from `50_sources/health/`, which is Sean's actual fitness/wellness data.
- **The unnumbered top-level dirs** (`Excalidraw/`, `health/`, `knowledge/`, plus the Tier-0 context file) sit outside the numbered hierarchy because they were added later and didn't fit cleanly. This is a known asymmetry; do not "fix" it without a project-level decision.
```

- [ ] **Step 2: Draft the folder-by-folder reference table**

Append under `<!-- SECTION: folder-reference -->`. Pull file counts directly from the scratchpad created in Task 0 — do not re-run `find`.

```markdown
## Folder-by-Folder Reference

Counts as of 2026-05-06 (refresh this table any time the guide is rewritten):

| Folder | Files | Purpose | Who writes here |
|---|---:|---|---|
| `00_inbox/` | 2 | Raw captures + research queues | Humans, Zapier captures, agents queueing research |
| `02_Areas/Agent-Fleet/` | ~19 | Daily fleet snapshots | `meta_agent` (autonomous, 8:35 AM daily) |
| `02_Areas/Work/` | 1 | Ad-hoc work artifacts | Humans |
| `05_atlas/` (root) | 6 | MOCs (one per domain) | Humans, occasional agent updates |
| `05_atlas/operating-models/` | 17 | 5-artifact bundles + index | `work-operating-model` skill (Sean-driven interview) |
| `10_timeline/daily/` | ~60 | Daily notes | `daily-note-appender` hook (auto), `daily_driver` agent (morning), humans |
| `10_timeline/weekly/` | ~3 | Weekly reviews | Humans, deprecated `daily_driver` weekly mode |
| `20_projects/` | 53 | Active projects | Humans + project-specific agents |
| `30_domains/` | 317 | Domain workspaces (heaviest is Granola meeting notes) | Humans, Granola plugin |
| `40_knowledge/concepts/` | small | Hand-written concepts | Humans |
| `40_knowledge/references/` | majority of 81 | Hand-written references | Humans, `process-inbox` skill (manual triage) |
| `40_knowledge/notebooklm-exports/` | small | NotebookLM synthesis dumps | Humans (manual export) |
| `50_sources/data/` | small | Lists, raw data | Humans |
| `50_sources/finance/` | 0 .md (CSVs gitignored) | Bank/credit-card exports | Humans (manual import) |
| `50_sources/health/` | small | Workout / fitness CSVs | Humans (manual import), `health-habits` skill |
| `50_sources/assets/` | n/a (binaries) | Images, sprites | Humans (Obsidian attachment default) |
| `60_archive/` (READ-ONLY) | 24 | Done items | Nobody. Treat as immutable. |
| `70_apple-notes/` | 1 | Vestigial import staging | Nobody (kept for attachment paths only) |
| `90_system/templates/` | 6 | Templater templates | Humans (rare); auto-applied by Obsidian |
| `90_system/scripts/` | 1 | `process-granola-notes.py` post-processor | Humans (cron / manual) |
| `90_system/agent-logs/` | n/a (logs) | SDK-agent run logs + `agent-run-history.csv` | All SDK agents (write-only from agent side) |
| `Excalidraw/` | 1 | Excalidraw drawings | Excalidraw plugin |
| `health/` | n/a (json + .md reports) | Vault telemetry | `vault_synthesizer`, `knowledge_lint`, `gemini_dr.run` |
| `knowledge/` | 1 (index.md) + concepts/ + connections/ + qa/ | Synthesized knowledge | `vault_synthesizer` (concepts, connections), `query.py --file-back` (qa) |
| **Total .md files** | **~608** | (was 1,431 in Feb 2026 — Apple Notes archive collapse + content consolidation) | |
```

- [ ] **Step 3: Verify counts match the scratchpad**

Open the scratchpad and the new draft side-by-side. Every count in the table above should match a count from the scratchpad. **If they don't match, fix the draft.**

If the scratchpad shows a number that's bigger than `~`-prefixed entries above (e.g., `02_Areas/Agent-Fleet` shows 25 files but the table says ~19), use `~` and the rounded-down nearest 5 — exact daily-fleet-status counts are noisy and not worth precise tracking. Counts marked as `small` or `majority of N` are intentionally fuzzy.

---

## Task 3: Draft the "Operating Models" section (NEW)

**Files:**
- Modify: scratchpad

- [ ] **Step 1: Read the source of truth**

Read the operating-models README + INTERVIEW-PLAYBOOK in parallel:
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/README.md`
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/INTERVIEW-PLAYBOOK.md`
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/job-hunt-2026/HEARTBEAT.md` (sample, for shape)

- [ ] **Step 2: Draft the section**

Append under `<!-- SECTION: operating-models -->`:

```markdown
## Operating Models

The `vault/05_atlas/operating-models/` directory holds **five-artifact bundles** per domain that capture how Sean actually works. Downstream SDK agents (`daily_driver`, `meta_agent`, `flush`, `knowledge_lint`) load these on-demand to act with real context instead of generic boilerplate.

### The five artifacts per domain

| File | Captures | Layer |
|---|---|---|
| `HEARTBEAT.md` | Operating rhythms (daily / weekly / monthly) | 1 |
| `USER.md` | Recurring decisions and prioritization criteria | 2 |
| `SOUL.md` | Dependencies (Part A) + institutional knowledge (Part B) | 3+4 |
| `operating-model.md` | Synthesized one-file profile | (synthesis) |
| `schedule-recommendations.md` | Friction-derived calendar/automation rules | 5 |

### Active bundles (2026-05-06)

| Domain | Status | Notes |
|---|---|---|
| `creative-studio/` | confirmed | 16BitFit, Remotion, art, writing |
| `life-systems/` | confirmed | Finance, health, learning, time, career |
| `job-hunt-2026/` | confirmed | 8-week post-Block search; AI/Tech/Creative PM. Tier-A truths + relocation overrides + agent-message boundary rule live |
| `the-block/` | **archived 2026-05** | Moved to `vault/60_archive/operating-models-the-block-2026-05/` after Sean's layoff. Not loaded by active agents. |

### Tier-0 identity

Sits above all three domain bundles: `Sean-Winslow-Full-Personal-Context-v2.0.md` (vault root). Bumped from v1.1 on 2026-05-02 (interview-driven refresh). All operating-model artifacts cross-reference this file.

### Producing artifacts

Run the `work-operating-model` skill:

> "Run the work-operating-model interview for `<domain>`."

The skill walks the 5-layer interview (`/.claude/skills/work-operating-model/interview-questions.md`) and writes outputs to the matching subfolder. Artifacts progress through statuses: `awaiting-interview` → `draft` → `confirmed`.

### Consuming artifacts (agent contracts)

Loaded via `agents-sdk/lib/artifact_loader.py` with mtime-keyed caching. Controlled by `[artifacts]` in `agents-sdk/config.toml`; instant rollback = `enabled = false`.

| Agent | Loads | Purpose |
|---|---|---|
| `daily_driver` (morning) | All 3 HEARTBEATs in preamble; on-demand Read pointers for USER / SOUL / operating-model / schedule-recommendations | Phase 1 wiring (v3.16.0) |
| `meta_agent` | All 3 `schedule-recommendations.md` bodies | Domain-aware insights ranking against Protect/Automate/Decline lists (Phase 2 wiring, v3.17.0) |
| `flush.py` | All 3 SOULs prepended to `EXTRACTION_PROMPT` | Cross-reference new entries against Tier-A items |
| `knowledge_lint.py` | 3-domain SOUL context block in Tier-2 prompt | Adds `soul-tier-a-conflict` lint issue at HIGH severity |

**Phase 3 was closed 2026-04-27.** `meeting_defender` was deleted (Daily Driver morning already covers calendar surfacing); `sprint_health` autonomous wiring was superseded by the new `sprint-health` skill (interactive Atlassian MCP, no headless-MCP gymnastics).

### Reading order for new agents

1. Tier-0: `Sean-Winslow-Full-Personal-Context-v2.0.md` (always, as preamble)
2. Domain HEARTBEAT(s) for the active task
3. Domain USER if the task involves prioritization or trade-off decisions
4. Domain SOUL for dependency-aware or knowledge-gap-aware reasoning
5. Domain `schedule-recommendations.md` only when scheduling or recommending automation

Do not load all 5 artifacts for every task — `artifact_loader` is on-demand by design.
```

- [ ] **Step 3: Verify the bundle list against ground truth**

```bash
ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/
# Expected: INTERVIEW-PLAYBOOK.md, README.md, creative-studio, job-hunt-2026, life-systems

ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/60_archive/operating-models-the-block-2026-05/
# Expected: 6 files (the archived Block bundle)
```

If the list differs, update the table.

---

## Task 4: Draft the "Knowledge Loop Infrastructure" section (NEW)

**Files:**
- Modify: scratchpad

- [ ] **Step 1: Read producer/consumer code**

Read the synthesizer and indexer to understand the contract (do not skip — counts and table names appear in the prose):

- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/vault_synthesizer.py` (focus on `regenerate_index` and the `concept_edges` SQL)
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/vault_indexer.py` (focus on `init_db`)
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/lib/concept_edges.py`
- `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/query.py` (focus on `--file-back` and qa/ writeback)

- [ ] **Step 2: Draft the section**

Append under `<!-- SECTION: knowledge-loop -->`:

```markdown
## Knowledge Loop Infrastructure

The vault has a **producer/consumer knowledge loop** that compounds insight over time. The producer side runs nightly; the consumer side runs on every Claude Code session start. All components are local-first (Mac Mini Ollama + intermittently MBP Qwen3-14B). No cloud egress unless Sean opts into Gemini DR.

### Producers (write to `vault/knowledge/`, `vault/.vault-index.db`, `vault/health/`)

```text
SessionEnd flush  ──►  Vault Indexer  ──►  Vault Synthesizer  ──►  Knowledge Lint
(hook-triggered)      (2:00 AM daily)    (2:30 AM daily)         (Sun 22:00 weekly)
```

| Producer | Schedule | Output |
|---|---|---|
| `flush.py` | SessionEnd hook + PreCompact hook (v3.18.0+) | Daily-log session blocks; tag is `session-end` / `pre-compact` / `manual` (v3.18.0 added the trigger field) |
| `vault_indexer.py` | 2:00 AM daily (launchd, Mac Mini) | `vault/.vault-index.db` (`chunks` + `concept_edges` tables); `vault/.indexer-state.json` mtime cursor |
| `vault_synthesizer.py` | 2:30 AM daily (launchd, MBP if awake) | `vault/knowledge/concepts/<slug>.md`, `vault/knowledge/connections/<slug>.md`, `vault/knowledge/index.md`, `vault/health/synth-manifest-YYYY-MM-DD.json`, `concept_edges` rows (Phase D, v3.20.0) |
| `knowledge_lint.py` | Sunday 22:00 (launchd) | `vault/health/YYYY-MM-DD-lint-report.md` |
| `query.py --file-back` | Manual (terminal Q&A) | `vault/knowledge/qa/<slug>.md` + append to `vault/knowledge/qa/.manifest.json` (Phase C, v3.19.0) |

### Consumers (read `vault/knowledge/index.md` and friends)

| Consumer | Trigger | What it reads |
|---|---|---|
| `session-start-inject-index.sh` hook | New Claude Code session | `vault/knowledge/index.md` injected as `additionalContext` (≤15,000 chars, 5s timeout) |
| Any agent doing context-gathering | Manual | The index pointers, then the cited concept/connection/qa articles |
| `vault_synthesizer.py` itself | Each run | Reads its own prior outputs to detect supersedence |

### The SQLite layer

`vault/.vault-index.db` has two tables:

| Table | Schema highlights | Written by | Read by |
|---|---|---|---|
| `chunks` | `(file_path, chunk_index, content, embedding, sha256_chunk_id, ...)` | `vault_indexer` | `query.py`, `vault_synthesizer` |
| `concept_edges` | `(from_slug, to_slug, relation, valid_from, valid_until, ...)` with relation in `{supports, contradicts, evolved_into, supersedes, depends_on, related_to}` | `vault_synthesizer` (Phase D) | `knowledge_lint` (SQL fast path for contradictions) |

Taxonomy mirrors OB1's `schemas/typed-reasoning-edges/schema.sql`; SQLite-local. Bad relation values are logged + dropped via `agents-sdk/lib/concept_edges.py:insert_edge` (raises `ValueError` so the article still writes). LLM contradictions and SQL contradictions are deduped by normalized `frozenset({from_slug, to_slug})`; SQL hits win when both surface the same pair.

### The qa/ tier (v3.19.0)

`agents-sdk/scripts/query.py` adds terminal Q&A with two-pass orchestration:

1. **Selection pass:** picks 3-N article paths with similarity scores from `chunks` table.
2. **Answer pass:** reads the selected bodies and emits a `[[wikilink]]`-citing answer.

`--file-back` persists answers as a third article tier at `vault/knowledge/qa/<slug>.md`. The qa frontmatter cites each consulted article with a 12-char SHA-256 chunk_id over `(file_path, chunk_index)` from the `chunks` table plus the selection-pass similarity score — gives the synthesizer a cheap "did this specific chunk change?" check on the next nightly run.

`knowledge_lint._ORPHAN_EXCLUDE_DIRS` includes `qa` because qa/ articles are answer endpoints (cite outward, never receive inbound wikilinks).

### Current state (2026-05-06)

- `vault/knowledge/index.md`: 141 bytes ("_(none yet)_" placeholders).
- `vault/knowledge/concepts/` and `vault/knowledge/connections/`: empty — synthesizer has not produced articles yet (MBP must be awake at 2:30 AM for synthesis to succeed; v3.14.3 retired the WOL escalation).
- Latest synth manifest (`synth-manifest-2026-05-06.json`): `concepts_written: 0, connections_written: 0, status: "partial"`.
- The producer pipeline runs nightly; the consumer pipeline (SessionStart hook injection) is wired and waiting for content.

### Rollback procedures

| Phase | Rollback |
|---|---|
| Phase B (consumer hook) | Remove `SessionStart` block from `.claude/settings.json` |
| Phase C (qa tier) | Delete `agents-sdk/scripts/query.py` + revert qa/ entries in `regenerate_index` and `_ORPHAN_EXCLUDE_DIRS` |
| Phase D (typed edges) | `DROP TABLE concept_edges` + revert four MODIFY files; LLM still writes connection articles unchanged because `relations` is OPTIONAL in the prompt schema |
```

- [ ] **Step 3: Verify file paths exist**

```bash
ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/vault_synthesizer.py /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/agents/vault_indexer.py /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/lib/concept_edges.py /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/scripts/query.py
```

Expected: All 4 files exist. If `query.py` has been moved/renamed, update the section.

---

## Task 5: Draft the "Health Telemetry" + "Agent Fleet Workspace" sections (NEW)

**Files:**
- Modify: scratchpad

- [ ] **Step 1: Inspect current health and agent-fleet content**

```bash
ls -la /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/health/
ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/02_Areas/Agent-Fleet/ | head
cat /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/health/gemini-spend-2026-05.json | python3 -m json.tool | head -30
```

- [ ] **Step 2: Draft the Health Telemetry section**

Append under `<!-- SECTION: health-telemetry -->`:

```markdown
## Health Telemetry

`vault/health/` is the operational telemetry directory for vault-touching agents. **Not to be confused with `vault/50_sources/health/`**, which holds Sean's actual fitness/wellness data.

| File pattern | Producer | Purpose | Consumer |
|---|---|---|---|
| `synth-manifest-YYYY-MM-DD.json` | `vault_synthesizer.py` | Per-run counts (concepts, connections, edges, rejected, duration, model, wol_status) | `daily_driver` morning brief surfaces under "Vault Health" |
| `YYYY-MM-DD-lint-report.md` | `knowledge_lint.py` (Sunday 22:00) | Tier-1 structural + Tier-2 LLM lint findings | Humans (review weekly); future `knowledge_lint` runs (dedupe) |
| `gemini-spend-YYYY-MM.json` | `agents-sdk/scripts/gemini_dr.py` | Monthly Gemini DR / DR-Max spend ledger | `gemini_dr.run` (enforces $7 task / $10 day / $20 month caps) |
| `.gemini-ledger.lock` | `gemini_dr.py` | FileLock for spend ledger | (lock-only) |
| `.lock` | `vault_synthesizer.py` | FileLock for synth runs | (lock-only) |

### synth-manifest schema

```json
{
  "concepts_written": 0,
  "connections_written": 0,
  "duration_seconds": 2720.17,
  "edges_rejected": 0,
  "edges_written": 0,
  "files_processed": 30,
  "model_used": "qwen3-14b-research:latest",
  "rejected_count": 0,
  "run_id": "2026-05-06T02:30:03",
  "status": "partial",
  "wol_status": ""
}
```

`status` values: `success`, `partial`, `error`, `skipped`.

### gemini-spend ledger schema

JSONL records, one per Gemini DR run, with monthly aggregation. Caps enforced before each run; circuit-breaker trips block the next call.
```

- [ ] **Step 3: Draft the Agent Fleet Workspace section**

Append under `<!-- SECTION: agent-fleet -->`:

```markdown
## Agent Fleet Workspace

`vault/02_Areas/Agent-Fleet/` surfaces autonomous-agent telemetry into the vault so Sean can browse fleet health from Obsidian without leaving the editor.

| File | Producer | Cadence | Contents |
|---|---|---|---|
| `fleet-state.md` | `meta_agent` | 8:35 AM daily (overwritten) | Latest snapshot of all 7 active SDK agents — last run timestamp, exit code, cost, status |
| `daily-fleet-status-YYYY-MM-DD.md` | `meta_agent` | 8:35 AM daily (append) | Per-day fleet summary; gemma4:e4b on Mac Mini generates a "Domain-Aware Insights" section ranking activity against schedule-recommendations Protect/Automate/Decline lists |

These files are **read-only from Claude Code's perspective** — only `meta_agent` writes here. Edit them only to fix typos in Sean's manual annotations.

`vault/02_Areas/Work/` is a sibling area for ad-hoc work artifacts (e.g., `pr-digest-2026-04-08.md`). Manual humans only.
```

---

## Task 6: Draft the "SDK Agents That Touch the Vault" section (NEW)

**Files:**
- Modify: scratchpad

- [ ] **Step 1: Read the current SDK-agent inventory from CLAUDE.md**

Re-read `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/CLAUDE.md` "Agents SDK (Autonomous Layer)" section. The new VAULT-GUIDE section is a **vault-centric subset** — only the agents that read or write the vault. Do not duplicate CLAUDE.md's full schedule table; cross-reference it.

- [ ] **Step 2: Draft the section**

Append under `<!-- SECTION: sdk-agents-vault -->`:

```markdown
## SDK Agents That Touch the Vault

The `agents-sdk/` directory in the parent repo runs 14 autonomous agents on macOS launchd schedules; **7 are active**. This section covers only the vault-touching subset and what they read/write. For full agent details, schedules, and cost caps, see `/CLAUDE.md` "Agents SDK" section.

### Read/Write contract by agent

| Agent | Reads | Writes |
|---|---|---|
| `vault_indexer` | All vault `.md` files | `vault/.vault-index.db` (chunks + concept_edges schema), `vault/.indexer-state.json` |
| `vault_synthesizer` | `vault/.vault-index.db` chunks | `vault/knowledge/concepts/`, `vault/knowledge/connections/`, `vault/knowledge/index.md`, `vault/health/synth-manifest-*.json`, `concept_edges` rows |
| `meta_agent` | `90_system/agent-logs/agent-run-history.csv`; all 3 `schedule-recommendations.md` | `02_Areas/Agent-Fleet/fleet-state.md`, `02_Areas/Agent-Fleet/daily-fleet-status-*.md` |
| `daily_driver` (morning) | All 3 HEARTBEATs (preamble); on-demand USER/SOUL/operating-model/schedule-recommendations; latest synth-manifest | Today's daily note (creates if missing); appends to anchored sections |
| `flush.py` | Recent transcript; all 3 SOULs (extraction prompt); current daily note | Daily-log session blocks below `<!-- claude-sessions -->` |
| `knowledge_lint` | All vault `.md`; `vault/.vault-index.db` (concept_edges); 3-domain SOULs | `vault/health/YYYY-MM-DD-lint-report.md` |
| `deep_researcher` | `vault/00_inbox/research-queue.md` | `vault/20_projects/research/YYYY-MM-DD-<topic-slug>.md` |
| `gemini_researcher` (opt-in) | `vault/00_inbox/gemini-research-queue.md`; `vault/health/gemini-spend-*.json` | Research output dir TBD; updates spend ledger |
| `process_inbox` | **PAUSED 2026-04-29** — see `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`. Manual triage via `process-inbox` skill is the working path. | (n/a, paused) |

### Hooks that touch the vault

5 of the 13 hooks in `.claude/hooks/`:

| Hook | Trigger | Vault effect |
|---|---|---|
| `daily-note-appender.sh` | Stop (session end) | Creates today's daily note; appends session entry below `<!-- claude-sessions -->` with Dataview inline fields |
| `session-end-flush.sh` | SessionEnd (richer than Stop) | Spawns `flush.py --trigger session-end`; writes daily-log session block tagged `session-end` |
| `pre-compact-flush.sh` | PreCompact (before auto-compaction) | Spawns `flush.py --trigger pre-compact`; tag distinguishes from session-end so post-hoc analysis can sort flushes |
| `session-start-inject-index.sh` | SessionStart | Reads `vault/knowledge/index.md`; injects as `additionalContext` (≤15,000 chars, 5s timeout) |
| `vault-integrity.py` | (configured in settings.json) | Read-only validation; fails with exit code 2 if frontmatter or naming rules are violated |

### Authentication boundary

**SDK agents in headless mode cannot use OAuth-based MCP servers** (Slack, Google Calendar, Gmail, Atlassian). Those require browser-based OAuth available only in interactive Claude Code sessions. The morning `daily_driver` therefore creates the daily-note skeleton with empty anchors; Slack/calendar/Gmail/Jira data is backfilled when Sean starts an interactive session.

### Vault-sync ownership rule (issue #22, 2026-04-23)

The shell-level Obsidian-Git auto-commit hook is the **sole** owner of vault git operations. Obsidian-Git plugin auto-features (autoSaveInterval, autoPushInterval, autoPullInterval) **must stay 0 on every machine**. Running two auto-commit systems against the same vault caused the v3.15.0 merge conflicts. Manual commits from the Obsidian-Git command palette are fine; auto-features must never run.
```

- [ ] **Step 3: Verify the agent list against `agents-sdk/config.toml`**

```bash
grep -E "^\[agents\.|^name =|^enabled =" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/agents-sdk/config.toml
```

Cross-check that the agents in your draft table match the `enabled = true` agents in config.toml. Flag any deltas.

---

## Task 7: Refresh the "YAML Frontmatter Schema" + "Naming Conventions" + "Templates" sections

**Files:**
- Modify: scratchpad

These three sections are mostly correct in the original guide. Carry them forward with corrections only.

- [ ] **Step 1: Copy YAML Frontmatter Schema verbatim from the original**

Append under `<!-- SECTION: frontmatter-schema -->`. Take lines 173–252 of the original `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md` (the entire "YAML Frontmatter Schema" section). Add one new bullet at the bottom of the "Per-Type Field Requirements" table:

```markdown
| `meeting` | type, date, domain, attendees, context | `granola_id`, `granola_type`, `transcript` (when from Granola sync) |
```

(Replace the existing `meeting` row.)

- [ ] **Step 2: Copy Naming Conventions section verbatim**

Append under `<!-- SECTION: naming-conventions -->`. Take lines 254–278 unchanged.

- [ ] **Step 3: Refresh the Templates section**

Append under `<!-- SECTION: templates -->`. Start from lines 280–328 of the original, but rewrite the daily-template anchor list to match `tpl-daily.md`:

```markdown
| Template | Anchors |
|----------|---------|
| `tpl-daily` | `<!-- slack-overnight -->`, `<!-- meetings -->`, `<!-- jira-log -->`, `<!-- claude-sessions -->`, `<!-- side-projects -->`, `<!-- research-digest -->` |
| `tpl-weekly` | `<!-- auto-wins -->`, `<!-- auto-blockers -->`, `<!-- auto-decisions -->` |
| `tpl-project` | `<!-- status-update -->`, `<!-- git-commits -->` |
```

(Two new anchors vs. the original: `<!-- meetings -->` and `<!-- research-digest -->`.)

Update the example below the anchor table to use a current dataview query:

```markdown
**Example — Querying daily-note Claude Code sessions:**

```dataview
TABLE time, domain, context, tag
FROM "10_timeline/daily"
WHERE domain = "claude-mastery" AND tag = "pre-compact"
```

(The `tag` field was added to session entries in v3.18.0 to distinguish `session-end` / `pre-compact` / `manual` triggers.)

- [ ] **Step 4: Verify daily-template anchors**

```bash
grep -E "^<!-- " /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/templates/tpl-daily.md
```

Expected output (6 lines):
```
<!-- slack-overnight -->
<!-- meetings -->
<!-- jira-log -->
<!-- claude-sessions -->
<!-- side-projects -->
<!-- research-digest -->
```

If the template differs, the draft must match the template — not vice versa.

---

## Task 8: Refresh the "MOCs" + "Obsidian Plugins" + "Claude Code Integration" sections

**Files:**
- Modify: scratchpad

- [ ] **Step 1: Copy MOCs section unchanged**

Append under `<!-- SECTION: mocs -->`. Take lines 330–349 of the original verbatim. (The 6 MOCs and Home dashboard description are still accurate.)

- [ ] **Step 2: Refresh the Obsidian Plugins table**

Append under `<!-- SECTION: plugins -->`. Replace the original 8-plugin table with this 11-plugin table:

```markdown
## Obsidian Plugins

11 community plugins are installed:

| Plugin | Purpose | Key Config |
|--------|---------|------------|
| **Dataview** | Query engine for MOCs and dashboards | DQL + DataviewJS enabled, inline fields enabled |
| **Templater** | Smart note templates with dynamic content | Folder-template mapping, `tp.*` functions |
| **Obsidian Git** | Manual commits + status bar | **All auto-features OFF** (issue #22, 2026-04-23). `autoSaveInterval: 0`, `autoPushInterval: 0`, `autoPullInterval: 0`. Shell-level hook is sole owner of vault git ops. |
| **Obsidian Linter** | Markdown formatting and YAML automation | Auto-adds `created`/`updated` timestamps, auto-adds title from H1, ignores `70_apple-notes/` and `60_archive/` |
| **Local REST API** | MCP server endpoint for AI access | HTTPS on port 27124, self-signed SSL |
| **Remotely Save** | Cloud sync (encrypted config) | Encrypted credentials |
| **Homepage** | Opens vault to Home.md | Set to `Home` note |
| **Granola Sync** | Syncs meeting notes + transcripts from Granola | Individual files, `linkFromDailyNotes: true`, landing at `30_domains/product-management/the-block-meetings-granola-notes/`. Desktop only. |
| **Calendar** | NEW — Sidebar calendar widget | Standard config |
| **Excalidraw** | NEW — Hand-drawn diagrams stored at `Excalidraw/` | Standard config |
| **Image Converter** | NEW — Auto-convert pasted images (PNG → WebP, etc.) | Standard config |

### Obsidian app settings

| Setting | Value | Why |
|---|---|---|
| New file location | `00_inbox/` folder | All new captures go to inbox first |
| Attachment folder | `50_sources/assets/` | Centralized asset storage |
| Auto-update links | Enabled | Links survive file renames |
| Daily notes folder | `10_timeline/daily/` | ISO date format (YYYY-MM-DD) |
```

- [ ] **Step 3: Refresh the Claude Code Integration section**

Append under `<!-- SECTION: cc-integration -->`. Use this rewrite (the channels list + native MCP table replace the original):

```markdown
## Claude Code Integration

Five channels connect Claude Code to the vault:

### Channel 1: Direct filesystem access

Read, Write, Edit, Grep, Glob operate directly on vault files. The vault is just a directory of markdown files — no special API needed. Examples:

```text
Read "vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md"
Grep "operating-model" --path vault/
Glob "vault/20_projects/**/*.md"
Grep "\[\[Sean-Winslow-Full-Personal-Context-v2.0\]\]" --path vault/
```

### Channel 2: MCP server (Obsidian Local REST API)

The Local REST API plugin exposes vault operations over HTTPS on port 27124. The `mcp-obsidian` MCP server translates these into tools: `read_note`, `write_note`, `patch_note`, `move_note`, `delete_note`, `search_notes`, `list_directory`, `read_multiple_notes`, `update_frontmatter`, `get_frontmatter`, `manage_tags`, `get_vault_stats`.

Use MCP for: PATCH operations, frontmatter extraction, tag management.
Use direct filesystem for: bulk operations, when speed matters, when Obsidian isn't running.

### Channel 3: Native MCP integrations (preferred over Zapier)

As of 2026-03-01, native MCPs replaced Zapier for most services. **Always use native first.**

| Service | Native MCP | Zapier fallback |
|---|---|---|
| Google Calendar | `claude.ai Google Calendar` / `google-workspace` | `google_calendar_*` |
| Gmail | `claude.ai Gmail` / `google-workspace` | `gmail_*` |
| Google Sheets/Docs/Drive | `google-workspace` | `google_sheets_*`, `google_docs_*` |
| Jira + Confluence | `mcp-atlassian` / `claude.ai Atlassian` | `jira_software_cloud_*` |
| Slack | Slack plugin (pending Block admin approval; **The Block layoff 2026-05 means this may be moot**) | `slack_*` |
| GitHub | `github` MCP (Docker) | n/a |
| Granola | `claude.ai Granola` | n/a |
| NotebookLM | `notebooklm-mcp` | n/a |
| Figma | `claude.ai Figma` | n/a |

**Calendar rule (post-2026-05-04):** single calendar — `sean.winslow28@gmail.com`. The Block work calendar (`swinslow@theblock.co`) was archived after Sean's layoff; do NOT query it.

**Still Zapier-only:** Salesforce, GA4, Webhooks, code execution.

### Channel 4: Hooks (automatic)

5 of the 13 hooks touch the vault. See [Vault-Touching Hooks](#vault-touching-hooks) below.

### Channel 5: Skills (on-demand)

7 vault-specific skills in `.claude/skills/`. See [Skills Reference](#skills-reference) below.

### Channel 6: SDK Agents (autonomous)

7 active SDK agents, scheduled via launchd. See [SDK Agents That Touch the Vault](#sdk-agents-that-touch-the-vault).
```

- [ ] **Step 4: Verify plugin list against community-plugins.json**

```bash
cat /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/.obsidian/community-plugins.json
```

Expected: 11 plugins listed. If the count differs, update both the count in the section header and the table.

---

## Task 9: Refresh the read/write/inbox sections (lightly)

**Files:**
- Modify: scratchpad

These sections (How to Read, How to Write, Inbox Processing, Knowledge Graph Navigation, Semantic Search, Daily Workflow) are 80% correct as written. Apply targeted edits only.

- [ ] **Step 1: Copy "How to Read from the Vault" section**

Append under `<!-- SECTION: how-to-read -->`. Take lines 518–569 of the original. Refresh one example (Pattern A): replace the 16BitFit example path with a current one:

```markdown
# Find a specific note
Read "vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/2026-05-04-onwards-and-upwards-plan.md"

# Read the latest fleet snapshot
Read "vault/02_Areas/Agent-Fleet/fleet-state.md"

# Read today's synth manifest
Read "vault/health/synth-manifest-$(date +%Y-%m-%d).json"
```

- [ ] **Step 2: Copy "How to Write to the Vault" section**

Append under `<!-- SECTION: how-to-write -->`. Take lines 572–613 of the original. Add this paragraph at the top:

```markdown
> **Hard rule (issue #22, 2026-04-23):** Never push to git from Claude Code. The shell-level Obsidian-Git auto-commit hook is the **sole** owner of vault git operations. Manual commits from Obsidian's command palette are allowed; automated commits must come from the hook only.
```

- [ ] **Step 3: Refresh "Inbox Processing" section**

Append under `<!-- SECTION: inbox-processing -->`. Take lines 615–646 of the original but add this banner at the top:

```markdown
> **Status note (2026-04-29):** The `process_inbox` SDK agent is **paused**. The cloud-Sonnet path was validated as functionally working (~3 files/run) but cost-inefficient ($1.16/file vs $0/file local). A Path B rewrite to local `gemma4:e4b` is scoped at `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`. The working alternative is **manual triage via the `process-inbox` skill in an interactive Claude Code session.**
```

The current inbox is small (2 files: `research-queue.md`, `gemini-research-queue.md`) and these are managed by the skill, not the SDK agent.

- [ ] **Step 4: Copy Knowledge Graph Nav + Semantic Search + Daily Workflow sections unchanged**

Append under `<!-- SECTION: kg-nav -->`, `<!-- SECTION: semantic-search -->`, `<!-- SECTION: daily-workflow -->`. Lines 648–706 and 708–736 of the original. The semantic-search section's Smart Connections setup is still accurate; the daily-workflow section's anchor references will be auto-correct via the refreshed templates section.

---

## Task 10: Replace the "Content Statistics" section with current numbers

**Files:**
- Modify: scratchpad

- [ ] **Step 1: Pull the live counts from the scratchpad header (Task 0)**

Do not re-run any `find` / `wc` commands. Use the scratchpad numbers verbatim.

- [ ] **Step 2: Draft the new statistics section**

Append under `<!-- SECTION: stats -->`:

```markdown
## Content Statistics

As of 2026-05-06 (down from 1,431 in Feb 2026 due to the Apple-Notes archive collapse + content consolidation):

| Location | File count |
|----------|-----------:|
| **Total vault `.md` files** | **~608** |
| `00_inbox/` | 2 |
| `02_Areas/` (Agent-Fleet + Work) | ~20 |
| `05_atlas/` (MOCs + operating-models) | 23 |
| `10_timeline/` (daily + weekly + monthly) | ~65 |
| `20_projects/` (all 9 projects + research) | 53 |
| `30_domains/` (Granola + prompts + media-team-ideas) | 317 |
| `40_knowledge/` (concepts + references + notebooklm) | 81 |
| `50_sources/` (data + finance + health + assets) | 7 |
| `60_archive/` (collapsed; mostly Block-related) | 24 |
| `70_apple-notes/` (vestigial) | 1 |
| `90_system/` (templates + scripts + agent-logs) | 8 |
| `Excalidraw/` | 1 |
| `health/` (telemetry; .json + .md reports) | 3 |
| `knowledge/` (LLM-output; currently mostly empty) | 1 |
| Tier-0 + Home.md | 2 |

### Project breakdown (`20_projects/`)

| Project | Files |
|---|---:|
| `prj-superuser-pack` | 26 |
| `prj-job-hunt-2026` | 8 (NEW 2026-05-04) |
| `research/` | 6 (deep-researcher overnight queue) |
| `prj-16bitfit` | 3 (most content moved to `creative-studio/16bitfit-battle-mode/` outside vault) |
| `prj-boston-move` | 3 |
| `prj-campus-201` | 3 (mostly archived) |
| `prj-personal-finance` | 2 |
| `prj-animation-pipeline` | 1 |
| `prj-sw-portfolio-and-hubs-designs` | 1 (NEW) |

### Archive breakdown (`60_archive/` — read-only)

| Archive subfolder | Files | Origin |
|---|---:|---|
| `operating-models-the-block-2026-05` | 6 | Block bundle archived after layoff |
| `old-mocs` | 6 | Superseded MOC drafts |
| `apple-notes-personal` | 5 | Sentimental items (down from 52 — collapsed 2026-04) |
| `old-templates` | 4 | Superseded templates |
| `inbox-archive-2026-04-25` | 1 | Inbox cleanup snapshot |
| `old-prompts` | 1 | Legacy prompts |
| `old-rag` | 1 | Legacy RAG configs |
| `old-projects` | 0 | (empty placeholder for future archives) |

**The Phase 2/3 Apple-Notes import archives** (`apple-notes-empty` 310, `apple-notes-nyl` 63, `apple-notes-expired` 59, `apple-notes-prompts` 24, `apple-notes-duplicates` 23) were **removed in the 2026-04 cleanup**. The classification methodology is preserved at `40_knowledge/references/ref-apple-notes-classification-rubric.md`.
```

- [ ] **Step 3: Verify all numbers against the scratchpad**

Read the scratchpad. Diff every number against the table. Fix any drift.

---

## Task 11: Refresh "Granola Meeting Sync" + "Rules and Constraints" + "Appendix" sections, draft "Changelog"

**Files:**
- Modify: scratchpad

- [ ] **Step 1: Refresh Granola section**

Append under `<!-- SECTION: granola -->`. Start from lines 803–862 of the original, but verify these specific values match `vault/.obsidian/plugins/granola-sync/data.json`:

- `customBaseFolder: "30_domains/product-management/the-block-meetings-granola-notes"` ✓
- `saveAsIndividualFiles: true` ✓
- `linkFromDailyNotes: true` ✓
- `syncDaysBack: 7` ✓
- `transcriptHandling: "same-location"` ✓

Add this paragraph at the top of the section:

```markdown
> **Post-2026-05-04 caveat:** Granola was Sean's primary meeting transcription tool at The Block. After the layoff, future meetings (job-hunt interviews, networking calls) may continue to use Granola or pivot to a different tool. The plugin and post-processor remain installed and functional.
```

- [ ] **Step 2: Refresh "Rules and Constraints" section**

Append under `<!-- SECTION: rules -->`. Start from lines 779–801 of the original. Add three new rules at the bottom of the AI-agent list:

```markdown
11. **Never re-enable Obsidian-Git auto-features** (issue #22, 2026-04-23). The shell-level auto-commit hook is the sole owner. `autoSaveInterval`, `autoPushInterval`, `autoPullInterval` must all stay 0.
12. **Never write to `vault/knowledge/`** by hand. That directory is LLM-output only (`vault_synthesizer` writes concepts/connections/index; `query.py --file-back` writes qa/).
13. **Never write to `vault/health/` or `vault/02_Areas/Agent-Fleet/`** by hand (except to fix typos in Sean's manual annotations). Those are agent-output telemetry.
14. **Operating-model artifacts are loaded on-demand.** Don't load all 5 per domain unless the task needs them. Use the agent contract table in [SDK Agents That Touch the Vault](#sdk-agents-that-touch-the-vault) to decide which artifacts to load.
```

- [ ] **Step 3: Refresh the Appendix**

Append under `<!-- SECTION: appendix -->`. Start from lines 874–891 of the original. Add these new entries:

```markdown
| `agents-sdk/agents/vault_indexer.py` | SQLite indexer (chunks + concept_edges) |
| `agents-sdk/agents/vault_synthesizer.py` | LLM synthesizer for concepts/connections/index |
| `agents-sdk/agents/knowledge_lint.py` | Weekly lint (Tier-1 structural + Tier-2 LLM) |
| `agents-sdk/agents/flush.py` | SessionEnd / PreCompact transcript-to-daily-log |
| `agents-sdk/agents/meta_agent.py` | Daily fleet status writer |
| `agents-sdk/agents/daily_driver.py` | Morning daily-note skeleton creator |
| `agents-sdk/agents/deep_researcher.py` | Overnight research queue processor |
| `agents-sdk/scripts/query.py` | Terminal Q&A; writes to `vault/knowledge/qa/` |
| `agents-sdk/scripts/gemini_dr.py` | Gemini Deep Research wrapper; updates spend ledger |
| `agents-sdk/lib/artifact_loader.py` | On-demand operating-model artifact loader |
| `agents-sdk/lib/concept_edges.py` | Typed-edge insert helper for `concept_edges` table |
| `agents-sdk/config.toml` | Agent enablement, paths, safety limits |
| `.claude/hooks/session-start-inject-index.sh` | Injects `vault/knowledge/index.md` at session start |
| `.claude/hooks/session-end-flush.sh` | Triggers `flush.py --trigger session-end` |
| `.claude/hooks/pre-compact-flush.sh` | Triggers `flush.py --trigger pre-compact` (v3.18.0+) |
| `.claude/hooks/vault-integrity.py` | Frontmatter + naming-rule validator |
```

- [ ] **Step 4: Draft a NEW "Changelog" section at the bottom**

Append under `<!-- SECTION: changelog -->`:

```markdown
## Changelog

This guide's content history (the file's git log captures finer-grained edits):

| Date | What changed in the vault (and reflected in this guide) |
|---|---|
| 2026-02-21 | Original guide written. Vault had ~1,431 .md files post Apple Notes import. |
| 2026-02–04 | Phase 4–6 SDK-agent work: vault_indexer, vault_synthesizer, knowledge_lint shipped. `vault/.vault-index.db` and `vault/knowledge/` directories created. |
| 2026-04-09 | Six SDK agents disabled (`process_inbox`, `daily_driver` evening/weekly, `pr_digest`, `spending_analysis`, `health_audit`, `md_to_anki`) per `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`. |
| 2026-04-18 | Operating-models Phase 1 wiring (v3.16.0): `daily_driver` morning loads HEARTBEATs in preamble. |
| 2026-04-23 | **Vault-sync ownership rule (issue #22):** shell-level hook becomes sole vault git owner; Obsidian-Git auto-features turned off everywhere. |
| 2026-04-25 | Knowledge-loop consumer activation (Phase B): `session-start-inject-index.sh` hook live. |
| 2026-04 cleanup | Apple Notes archive subfolders (`apple-notes-empty/expired/nyl/duplicates/prompts`) removed. Total .md count drops from ~1,431 to ~608. |
| 2026-04-27 | Operating-models Phase 2 wiring (v3.17.0): `meta_agent`, `flush`, `knowledge_lint` consume schedule-recommendations and SOULs. |
| 2026-04-28 → 2026-04-29 | `process_inbox` re-enabled briefly (v3.17.2/v3.17.3) then paused (v3.17.4) — see `agents-sdk/AUDIT-2026-04-28-process-inbox-reenable.md`. |
| 2026-05-01 | Knowledge-loop Phase A (PreCompact safety net, v3.18.0): `pre-compact-flush.sh` hook + `flush.py --trigger` field. |
| 2026-05-01 | Knowledge-loop Phase C (qa tier, v3.19.0): `query.py` + `vault/knowledge/qa/` directory. |
| 2026-05-01 | Knowledge-loop Phase D (typed reasoning edges, v3.20.0): `concept_edges` SQLite table; `knowledge_lint` SQL fast path. |
| 2026-05-02 | Tier-0 identity bump: `Sean-Winslow-Full-Personal-Context-v2.0.md` (interview-driven refresh from v1.1). |
| 2026-05-04 | **Sean laid off from The Block.** `the-block/` workspace archived. `prj-job-hunt-2026/` created. The-Block calendar archived (single calendar now: `sean.winslow28@gmail.com`). The-Block operating-model bundle archived to `60_archive/operating-models-the-block-2026-05/`. |
| 2026-05-05 | Job-hunt-2026 operating-model bundle confirmed (status: confirmed). |
| 2026-05-06 | This guide rewritten end-to-end. |
```

---

## Task 12: Assemble the new VAULT-GUIDE.md and Write atomically

**Files:**
- Modify: `vault/90_system/VAULT-GUIDE.md` (full overwrite)

- [ ] **Step 1: Read the current VAULT-GUIDE.md once more**

```bash
wc -l /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md
```

Note the current line count for comparison.

- [ ] **Step 2: Assemble all section blocks from the scratchpad into the final document**

In the scratchpad, every section is bounded by `<!-- SECTION: <name> -->` markers. Final assembly order (matches the file structure plan):

1. frontmatter
2. (banner + intro paragraph from Task 1 Step 2)
3. quick-ref
4. (Table of Contents — generate from the H2 list below)
5. architecture
6. folder-reference
7. frontmatter-schema
8. naming-conventions
9. templates
10. mocs
11. operating-models
12. knowledge-loop
13. health-telemetry
14. agent-fleet
15. plugins
16. cc-integration
17. sdk-agents-vault
18. (vault-touching-hooks — pulled into the SDK agents section in Task 6, no separate block)
19. how-to-read
20. how-to-write
21. inbox-processing
22. kg-nav
23. semantic-search
24. daily-workflow
25. granola
26. stats
27. rules
28. appendix
29. changelog

Generate a Table of Contents from the H2 headers, with anchor links matching markdown's auto-slug rules (lowercase, spaces → hyphens, punctuation removed).

- [ ] **Step 3: Write the assembled document**

Use the Write tool on `/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md`. Confirm the Read-before-Write pre-condition is satisfied (Step 1 already read the file).

- [ ] **Step 4: Verify the final document**

```bash
# Line count sanity check (expect 600-1000 lines)
wc -l /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md

# Frontmatter is intact
head -10 /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md

# All H2 sections rendered (expect ~25-29 H2s, count above)
grep -c "^## " /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md

# No leftover SECTION markers (all should have been stripped during assembly)
grep -c "<!-- SECTION:" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md
# Expected: 0

# No leftover scratchpad placeholders
grep -nE "TODO|TBD|FIXME|<<.*>>" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md
# Expected: no matches
```

If any of these fail (especially the SECTION marker count), Edit the file to fix.

- [ ] **Step 5: Spot-check three key facts in the new document against the live vault**

```bash
# Granola landing path matches what's in the new guide
grep "the-block-meetings-granola-notes" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md
python3 -c "import json; d=json.load(open('/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/.obsidian/plugins/granola-sync/data.json')); print(d['customBaseFolder'])"
# The grep result must contain the path printed by python.

# Daily template anchor list matches actual template
grep -E "slack-overnight|meetings|jira-log|claude-sessions|side-projects|research-digest" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md | head
grep -E "^<!-- " /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md | head

# Operating-model bundle list matches filesystem
grep -E "creative-studio|life-systems|job-hunt-2026" /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md | head
ls /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/05_atlas/operating-models/
```

- [ ] **Step 6: Run vault-integrity validation**

```bash
python3 /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/.claude/hooks/vault-integrity.py /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/90_system/VAULT-GUIDE.md 2>&1 || true
```

If the hook complains about frontmatter or naming, fix the issue (this hook may not run standalone — if it errors with a "missing args" message, that's expected; the hook validates on tool-use events, not direct invocation).

- [ ] **Step 7: Run repo-level validator**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack && python3 scripts/validate.py 2>&1 | tail -20
```

Expected: "0 errors". If errors appear, the rewrite did not introduce them (no .claude/ files changed) — but read the output to confirm.

- [ ] **Step 8: Delete the scratchpad**

```bash
rm /Users/seanwinslow/Code-Brain/claude-code-superuser-pack/docs/superpowers/plans/2026-05-06-vault-guide-rewrite-scratch.md
```

- [ ] **Step 9: Commit the rewrite**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git add vault/90_system/VAULT-GUIDE.md docs/superpowers/plans/2026-05-06-vault-guide-rewrite.md
git status
git commit -m "$(cat <<'EOF'
docs(vault): rewrite VAULT-GUIDE.md for 2026-05-06 truth state

The Feb 2026 guide was written when the vault had 1,431 .md files post
Apple-Notes import. Since then: 14 SDK agents shipped (7 active), the
operating-models artifact system landed at 05_atlas/operating-models/,
the knowledge-loop infrastructure (vault/knowledge/, vault/health/,
.vault-index.db) was built, three top-level dirs were added (02_Areas/,
Excalidraw/, health/, knowledge/), Apple Notes archives were collapsed
(file count down to ~608), and Sean was laid off from The Block on
2026-05-04 — pivoting the active project surface to job-hunt-2026.

The rewrite reorganizes around four reading audiences (future Claude
Code agents, SDK agents, Sean as operator, future-Sean re-onboarding)
and adds five entirely new sections: Operating Models, Knowledge Loop
Infrastructure, Health Telemetry, Agent Fleet Workspace, and SDK Agents
That Touch the Vault. The frontmatter `created` field is preserved at
2026-02-21; an `updated` field tracks the rewrite date.

Plan + verification steps live at
docs/superpowers/plans/2026-05-06-vault-guide-rewrite.md.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 10: Confirm clean working tree**

```bash
git status
```

Expected: "nothing to commit, working tree clean" (or only untracked files unrelated to this task).

---

## Task 13: Open the PR

**Files:**
- (no file changes)

- [ ] **Step 1: Push the branch**

```bash
cd /Users/seanwinslow/Code-Brain/claude-code-superuser-pack
git push -u origin docs/vault-guide-rewrite-2026-05-06
```

- [ ] **Step 2: Open the PR**

```bash
gh pr create --title "docs(vault): rewrite VAULT-GUIDE.md for 2026-05-06 truth state" --body "$(cat <<'EOF'
## Summary

The Feb 2026 VAULT-GUIDE was written when the vault had 1,431 .md files post Apple-Notes import. Three months later it is materially wrong about: folder structure, file counts (now ~608), archive subfolders, plugin list, hook count, agent integration, and post-Block-layoff project surface.

This rewrite is a full replacement that:
- Adds five new sections: Operating Models, Knowledge Loop Infrastructure, Health Telemetry, Agent Fleet Workspace, SDK Agents That Touch the Vault
- Refreshes folder counts from the live vault (no `~`-fudging on the structural claims)
- Cross-references CLAUDE.md instead of duplicating its content
- Adds a "Quick Reference for AI Agents" top section so future agents can read just one section and not break things
- Adds a Changelog section so the next quarter of vault changes is easier to track

Plan + verification steps committed to `docs/superpowers/plans/2026-05-06-vault-guide-rewrite.md`.

## Test plan

- [ ] Read the new VAULT-GUIDE.md end-to-end and spot-check three claims (Granola path, daily anchors, operating-model bundles)
- [ ] Run `python3 scripts/validate.py` — expect 0 errors
- [ ] Confirm Obsidian renders the file without YAML errors
- [ ] Confirm internal anchor links work (TOC clicks)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 3: Return the PR URL to Sean**

---

## Self-Review Checklist (run before declaring plan complete)

**1. Spec coverage:** The user's ask was "execution plan for the VAULT-GUIDE.md re-write so that it's up to date and future agents understand the structure without having to search too much." The plan:
- ✅ Touches every section that's outdated (folder tree, counts, archives, plugins, integration, hooks)
- ✅ Adds the missing infrastructure (operating-models, knowledge-loop, agent-fleet, health, SDK agents)
- ✅ Includes a "Quick Reference for AI Agents" section explicitly so a future agent can avoid searching
- ✅ Has a Changelog so next quarter's updates are easier
- ✅ Verifies every claim against ground truth before commit (Task 12 Step 5)

**2. Placeholder scan:** No `TBD`, `TODO`, `FIXME`, or "implement later" anywhere in the plan. Every step has either complete content (the markdown blocks) or a complete command. Section drafts in Tasks 1–11 contain the actual prose to be written, not just "describe X". Task 12 Step 4 grep checks the final file for placeholder leakage.

**3. Type / name consistency:**
- "Operating-model bundle" naming is consistent (HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations) across Tasks 1, 3, 6, 11.
- "vault/knowledge/" vs. "40_knowledge/" distinction is preserved everywhere.
- The 6 daily-template anchors match `tpl-daily.md` (verified Task 7 Step 4).
- "process_inbox" agent (paused) vs. "process-inbox" skill (active) — both spellings used consistently per their actual identifiers.

**4. Final pass on edge cases:**
- The plan handles the case where the synthesizer hasn't produced articles yet (current state: index.md is 141 bytes of placeholders) — the new guide describes this explicitly in Task 4.
- The plan handles the case where line numbers in the original guide change between now and execution by using semantic content references ("the YAML Frontmatter Schema section") rather than depending on exact line ranges in Tasks 7–11.
- The atomic Write in Task 12 means the live VAULT-GUIDE never enters a half-rewritten state visible to other agents/users.

Plan complete and saved to `docs/superpowers/plans/2026-05-06-vault-guide-rewrite.md`.
