# Phase 2 Session 2: Research-Informed Recommendations

**Date:** January 30, 2026
**Session Focus:** Community knowledge synthesis from ChatGPT, Perplexity, Gemini, and Grok research
**Profile:** Sean Winslow - Associate PM (Technical) at The Block

---

## Executive Summary

After reviewing 8 research documents across 4 AI platforms (totaling ~10,000+ lines of Claude Code insights), I've identified **15 high-impact improvements** to your Superuser Pack. The research reveals several patterns you're not yet leveraging: multi-agent orchestration, hook-based enforcement, headless automation for CI/CD, and MCP integrations for your specific tools (Jira, Figma, Slack).

**Top 3 Immediate Wins:**
1. **Hook-based secret blocking** - Prevent `.env` commits automatically (5 min setup)
2. **Monday Morning Dispatcher** - Auto-triage weekend bugs from Jira/Sentry (transforms PM workflow)
3. **Multi-instance parallel dev** - Run 3 Claude instances on 16BitFit (frontend/backend/reviewer)

**Biggest Gap Identified:** You have skills but no hooks. Research shows hooks are the "deterministic glue" that separates power users from regular users—84% reduction in permission prompts when combined with sandboxing.

---

## Quick Wins (< 30 min implementation each)

### 1. Block Secrets Hook (CRITICAL)
**Source:** Perplexity Handoff v1, Gemini Workflows #14
**Why:** Deterministic protection against committing API keys, `.env` files, or credentials.

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": {
      "matcher": { "tool": "Write", "input": { "path": "*.env*" } },
      "command": "exit 2",
      "blocking": true
    }
  }
}
```

**Exit codes:** 0 = allow, 1 = error continue, 2 = deny permission (blocks the action)

**Adaptation for The Block:** Extend to block `credentials.json`, `secrets.yaml`, and any file with "api_key" in the name.

---

### 2. Auto-Format on Save Hook
**Source:** Perplexity 30 Uses #7, Gemini Workflows #16
**Why:** Never manually run Prettier/ESLint again. PostToolUse hooks run deterministically after file writes.

```json
{
  "hooks": {
    "PostToolUse": {
      "matcher": { "tool": "Write", "input": { "path": "*.{ts,tsx,js}" } },
      "command": "npx prettier --write $FILEPATH && npx eslint --fix $FILEPATH",
      "blocking": false
    }
  }
}
```

**For 16BitFit:** This catches React Native and Phaser code automatically.

---

### 3. Plan Mode Default for Complex Tasks
**Source:** ChatGPT Contradiction Resolver, Perplexity Handoff
**Why:** Research shows confusion between Plan Mode (Shift+Tab twice) and Extended Thinking (Tab). They're different:
- **Plan Mode:** Reviews changes before execution (safer for beginners)
- **Extended Thinking:** More reasoning tokens, higher cost

**Add to CLAUDE.md:**
```markdown
## Project Preferences
- Default to Plan Mode (Shift+Tab twice) for any task touching >3 files
- Use Extended Thinking (Tab) only for algorithm design or complex refactors
```

---

### 4. Permission Presets via allowedTools
**Source:** Perplexity Capabilities Map, Handoff v1 #7
**Why:** Pre-approve trusted operations to reduce prompt fatigue.

```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm run *)",
      "Bash(npx expo *)",
      "Read(*)",
      "Glob(*)"
    ]
  }
}
```

**For your workflow:** This auto-approves git operations, npm scripts, and Expo commands for React Native development.

---

### 5. Background Tasks for Dev Servers (Ctrl+B)
**Source:** Perplexity Handoff #3, 30 Uses #5
**Why:** Run `expo start` or `npm run dev` in background while Claude continues working.

**Usage:**
1. Ask Claude to start your dev server
2. Press `Ctrl+B` while command is running (twice if using tmux)
3. Server runs in background, Claude continues coding

**For 16BitFit:** Background the Vite dev server while Claude works on Phaser game logic.

---

## Strategic Improvements (1-2 hours each)

### 6. NEW SKILL: "Monday Morning Dispatcher"
**Source:** Gemini Workflows #2
**Why:** As a PM, you start every week triaging bugs. This automates it.

**Create:** `.claude/skills/monday-dispatcher/SKILL.md`
```yaml
---
name: monday-dispatcher
description: Auto-triage weekend bugs from Jira and Sentry, correlate stack traces with source files
trigger: weekly-triage, monday-bugs, weekend-issues
allowed-tools: [mcp__jira, mcp__sentry, Grep, Read]
---

# Monday Morning Dispatcher

## Purpose
Fetch bugs/issues created since last Friday, auto-correlate with source code, and draft triage labels.

## Workflow
1. Query Jira for issues created `createdDate >= -3d`
2. Query Sentry for new errors (if available)
3. For each issue, search codebase for mentioned files/functions
4. Output: Markdown table with columns: Issue Key | Summary | Severity Guess | Related Files | Recommended Label

## Guardrails
- Only LABEL issues, never auto-close without explicit confirmation
- If similarity to existing issue > 98%, suggest as duplicate but require confirmation
- Mark any P0/Critical issues for immediate human review
```

---

### 7. NEW SKILL: "Ambiguity Crusher" for Spec Review
**Source:** Gemini Workflows #1
**Why:** Before writing tickets from PRDs, validate specs against actual codebase constraints.

**Create:** `.claude/skills/ambiguity-crusher/SKILL.md`
```yaml
---
name: ambiguity-crusher
description: Cross-reference PRD specs against codebase schema, API types, and existing tickets to find contradictions
trigger: vet-spec, review-prd, spec-triage, check-spec
allowed-tools: [Read, Grep, Glob, mcp__jira]
---

# Ambiguity Crusher

## Purpose
Identify logical contradictions between a spec and the actual codebase BEFORE coding begins.

## Workflow
1. Load the spec/PRD document
2. Extract technical requirements (auth methods, data models, API endpoints)
3. Cross-reference against:
   - schema.prisma or database models
   - API type definitions
   - Existing Jira tickets for conflicts
4. Output: "Clarification List" - questions that MUST be answered before implementation

## Guardrails
- CITE specific file and line number for every objection
- Never hallucinate constraints - only report what's actually in the code
- Output format: Requirements → Evidence → Clarification Needed
```

---

### 8. NEW AGENT: "Stakeholder Simulator"
**Source:** Gemini Workflows #4, Perplexity 30 Uses #15
**Why:** Pre-empt security/legal/performance concerns BEFORE sharing specs with stakeholders.

**Create:** `.claude/agents/stakeholder-simulator.md`
```yaml
---
name: stakeholder-simulator
description: Adopt a persona (CISO, Legal, Performance Lead) and critique code/specs from that perspective
trigger: simulate, persona-review, stakeholder-check
disallowed-tools: [Write, Edit, Bash]
---

# Stakeholder Simulator

## Available Personas
- **CISO**: OWASP Top 10, auth patterns, PII handling, crypto security (important for The Block)
- **Legal**: GDPR, data retention, terms of service implications
- **Performance**: N+1 queries, bundle size, memory leaks

## Usage
`/simulate --persona="CISO"` on current diffs

## Output Format
**Risk Assessment Report** saved to `artifacts/[persona]-review.md`
- Findings with severity (High/Medium/Low)
- Specific line references
- Recommended mitigations

## Guardrails
- Label all output as "Simulation" - does not block PRs
- Focus on pre-empting real stakeholder concerns
```

---

### 9. Multi-Instance Parallel Development Pattern
**Source:** Perplexity Delta Handoff #4, 30 Uses #12
**Why:** For 16BitFit, run 3 Claude instances simultaneously: frontend, backend, reviewer.

**Setup:**
```bash
# Terminal 1 - Frontend (React Native UI)
cd ~/16bitfit
export CLAUDE_CODE_TASK_LIST_ID=16bitfit-sprint
claude

# Terminal 2 - Backend (Supabase/API)
cd ~/16bitfit
export CLAUDE_CODE_TASK_LIST_ID=16bitfit-sprint
claude

# Terminal 3 - Reviewer (runs tests, catches issues)
cd ~/16bitfit
export CLAUDE_CODE_TASK_LIST_ID=16bitfit-sprint
claude
```

**Why it works:** Shared `CLAUDE_CODE_TASK_LIST_ID` means all instances see the same task list. The reviewer instance can flag issues the other two create.

**Risk mitigation:** Don't have two instances edit the same file simultaneously.

---

### 10. NEW HOOK: Release Notes Auto-Generator
**Source:** Gemini Workflows #3
**Why:** As a PM, you write release notes. Automate the first draft.

**Create:** `.claude/hooks/release-notes.sh`
```bash
#!/bin/bash
# Runs on git tag creation

LAST_TAG=$(git describe --tags --abbrev=0 HEAD^)
CURRENT_TAG=$(git describe --tags --abbrev=0 HEAD)

# Get commits between tags
COMMITS=$(git log $LAST_TAG..$CURRENT_TAG --pretty=format:"%s" --no-merges)

# Filter out internal/chore commits
FILTERED=$(echo "$COMMITS" | grep -v "\[internal\]" | grep -v "^chore:")

# Output for Claude to process
echo "RELEASE_NOTES_INPUT: $FILTERED"
```

**Then add a skill that transforms this into user-facing bullet points.**

---

### 11. MCP Integration: Jira + Slack + Figma
**Source:** Perplexity Capabilities Map, Handoff v1 #12
**Why:** Your current pack has skills that MENTION Jira/Figma but don't actually connect to them.

**Add to `~/.claude.json`:**
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-jira"],
      "env": {
        "JIRA_URL": "https://theblock.atlassian.net",
        "JIRA_TOKEN": "${JIRA_API_TOKEN}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-slack"],
      "env": {
        "SLACK_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-figma"],
      "env": {
        "FIGMA_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

**Note:** stdio transport is more reliable than HTTP for local MCP servers.

---

## Advanced/Experimental (Stretch goals)

### 12. Headless CI/CD for PR Review
**Source:** Perplexity 30 Uses #3, Handoff v1 #5
**Why:** Run Claude in CI pipelines to auto-review PRs, suggest fixes, or auto-fix linting issues.

**GitHub Action:**
```yaml
name: Claude Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          prompt: |
            Review this PR for:
            1. Security issues (especially crypto-related for The Block)
            2. Performance regressions
            3. Missing tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

### 13. Self-Healing CI Medic
**Source:** Gemini Workflows #11
**Why:** When CI fails, Claude auto-attempts a fix before pinging you.

**Pattern:**
1. GitHub Action triggers on workflow failure
2. Claude analyzes build logs via MCP
3. If fix is simple (missing dependency, snapshot update), auto-commits to `fix/auto-ci` branch
4. If complex, creates issue with diagnosis

**Guard rail:** Limit to 1 auto-fix attempt per failure type to prevent infinite loops.

---

### 14. Plugin Marketplace Distribution
**Source:** Perplexity Delta Handoff, Capabilities Map
**Why:** Package your entire Superuser Pack as a shareable plugin for your team at The Block.

**Create:** `.claude-plugin/marketplace.json`
```json
{
  "name": "block-pm-toolkit",
  "version": "1.0.0",
  "description": "The Block PM workflow automation - specs, tickets, stakeholder docs",
  "includes": [
    "commands/quick-prd.md",
    "commands/ticket-batch.md",
    "skills/ambiguity-crusher/SKILL.md",
    "skills/monday-dispatcher/SKILL.md",
    "agents/stakeholder-simulator.md",
    "hooks/block-secrets.json"
  ]
}
```

**Install command:** `/plugin marketplace add theblock/pm-toolkit`

---

### 15. Context Compressor (Session Memory)
**Source:** Gemini Workflows #20, Perplexity 30 Uses #25
**Why:** Auto-update CLAUDE.md with learned preferences at session end.

**Create:** `.claude/hooks/session-end.sh`
```bash
#!/bin/bash
# Extracts preferences from session and updates CLAUDE.md

echo "SESSION_PREFERENCES_TO_LEARN:"
echo "- Coding style preferences observed"
echo "- API patterns used"
echo "- Testing approaches preferred"
```

**Combined with a Stop hook to analyze the session transcript and propose CLAUDE.md updates.**

---

## Implementation Roadmap

### This Week (Quick Wins)
| Priority | Item | Time | Impact |
|----------|------|------|--------|
| 1 | Block secrets hook | 5 min | Prevents security disasters |
| 2 | Auto-format hook | 10 min | Eliminates manual linting |
| 3 | Permission presets | 10 min | Reduces prompt fatigue |
| 4 | Plan mode in CLAUDE.md | 5 min | Safer editing default |

### Next Week (Strategic)
| Priority | Item | Time | Impact |
|----------|------|------|--------|
| 5 | Monday Dispatcher skill | 1 hr | Transforms Monday mornings |
| 6 | Ambiguity Crusher skill | 1 hr | Better specs = less rework |
| 7 | Multi-instance pattern | 30 min | 3x parallel progress on 16BitFit |
| 8 | MCP integrations | 1 hr | Real Jira/Slack/Figma connections |

### When Ready (Advanced)
| Priority | Item | Time | Impact |
|----------|------|------|--------|
| 9 | Stakeholder Simulator | 2 hr | Pre-empt review cycles |
| 10 | Headless CI review | 2 hr | Auto-review all PRs |
| 11 | Plugin marketplace | 1 hr | Share with Block team |

---

## Key Insights from Research

### What Separates Power Users from Regular Users

1. **Hooks, not just skills** - Hooks provide deterministic control (exit codes) while skills provide expertise. Use hooks for binary decisions (allow/block), skills for analysis.

2. **Multi-agent orchestration** - Research shows 3 patterns:
   - **Codebase Brain:** Specialist agents per domain with leader routing
   - **Swarm:** Leader spawns workers claiming from shared queue
   - **Council:** Multiple agents analyze same problem from different angles

3. **CLAUDE.md hygiene** - Keep it lean (< 500 tokens), use `.claude/rules/` for modularity, update continuously as architecture evolves.

4. **Sandboxing + allowedTools = 84% fewer prompts** - Combine sandbox mode with pre-approved operations for near-autonomous coding.

5. **Tasks system > Todos** - v2.1.x introduced task dependencies and multi-session persistence. Set `CLAUDE_CODE_TASK_LIST_ID` for shared task lists across instances.

### Community Gotchas to Avoid

1. **Auto-compact can lose context** - Manual `/compact [focus]` is safer; store persistent rules in CLAUDE.md, not conversation.

2. **Plan mode may auto-enable acceptEdits** - Explicitly disable after plan approval if you want manual control.

3. **Background subagents can't ask questions** - Pre-approve all required tools; use foreground subagents for interactive tasks.

4. **Custom output styles lose coding expertise** - Set `keep-coding-instructions: true` in output style frontmatter.

5. **MCP OAuth can fail silently** - stdio transport more reliable than HTTP; test OAuth servers individually.

---

## Files to Create Summary

```
.claude/
├── settings.json (add hooks + permissions)
├── skills/
│   ├── monday-dispatcher/SKILL.md (NEW)
│   └── ambiguity-crusher/SKILL.md (NEW)
├── agents/
│   └── stakeholder-simulator.md (NEW)
├── hooks/
│   └── release-notes.sh (NEW)
└── rules/
    └── crypto-security.md (NEW - for The Block context)

~/.claude.json (add MCP servers for Jira, Slack, Figma)

.claude-plugin/
└── marketplace.json (for team distribution)
```

---

## Sources Referenced

| Source | Key Contribution |
|--------|------------------|
| ChatGPT Synthesis - Roadmap | 6-week mastery syllabus, Pack tiers |
| ChatGPT Synthesis - Contradictions | Plan vs Think mode clarification |
| Perplexity Capabilities Map | Comprehensive technical reference |
| Perplexity 30 Creative Uses | Multi-agent patterns, creative workflows |
| Perplexity Handoff v1 | Top 15 superuser moves, security notes |
| Perplexity Delta Handoff | Plugin marketplace, Remotion, parallel dev |
| Gemini 20 Workflows | PM-specific workflows, DevOps patterns |

---

## Next Steps for Session 3

Session 3 should focus on **gap analysis**:
1. Compare implemented items vs research recommendations
2. Identify any Grok PDF insights not covered
3. Validate configurations actually work in your environment
4. Create test prompts to verify skills trigger correctly
