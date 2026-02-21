<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Use the Context Packet + Handoff Packet above.

Your job:

1) Treat items marked COMMUNITY/VERIFY as hypotheses until confirmed.
2) Prioritize official Anthropic docs for “what is true.”
3) Produce answers that are implementation-ready (exact schemas, exact file paths, example configs).
4) End with a “Build my Superuser Pack next” checklist (files to create in .claude/, what goes in each).

Now answer the following prompt:

I want the most creative, unusual, high-leverage uses of Claude Code, beyond normal coding.

Brainstorm + source:

- creative pipelines (video editing automation, game dev scripting, asset pipelines)
- research assistants inside repos
- headless automation scripts
- multi-agent patterns (writer/reviewer/tester)
- hooks as enforcement mechanisms
- plugins/marketplaces as a distribution layer

Deliver:

- 30 ideas, sorted by difficulty and payoff
- for each: a 3-step “try it now” mini experiment
- link to any sources/examples that inspired the idea

Now I'll compile the research and create a comprehensive guide with 30 creative, high-leverage Claude Code use cases.

# 30 Creative, High-Leverage Uses of Claude Code (Beyond Normal Coding)

**Research Context:** Based on official Anthropic docs (Jan 2026), community implementations, and emerging patterns from video automation (Remotion AI), game development (Unity/Godot/Phaser), multi-agent orchestration systems, and headless automation workflows.

***

## **Tier 1: Quick Wins (Low Difficulty, High Payoff)**

### 1. **Code-Based Video Editor (Remotion + Claude Code)**

**What:** Turn text prompts into production-ready videos with animations, transitions, and branding—no timeline clicking required.

**Payoff:** 10+ hours saved per week on video editing; instant iteration via prompt.[^1][^2][^3]

**Try it now:**

1. Install Remotion skill: Create `.claude/skills/remotion-video.md` with frontmatter pointing to Remotion docs
2. Prompt: "Create a 30-second product demo video with blue/white branding, fade transitions, and upbeat background music"
3. Iterate: "Make transitions faster, add dopamine-inducing motion curves, change text to Geist font"

**Inspired by:** https://www.youtube.com/watch?v=Tt-hpp87pd0 (Jan 2026)

***

### 2. **Automated Issue Triage Bot**

**What:** Headless Claude reviews new GitHub issues, applies labels, assigns priority, and adds context from codebase.

**Payoff:** Zero manual issue sorting; instant team alignment.[^4]

**Try it now:**

1. Create `.github/workflows/issue-triage.yml` with `anthropics/claude-code-action@v1`
2. Add workflow trigger: `on: issues: types: [opened]`
3. Pass issue body to headless mode: `claude -p "Analyze this issue and suggest labels: $ISSUE_BODY" --output-format stream-json`

**Inspired by:** Anthropic's own public repo automation (https://www.anthropic.com/engineering/claude-code-best-practices)

***

### 3. **Living Documentation Writer**

**What:** PostToolUse hook automatically updates project docs after every code change; CLAUDE.md stays synchronized.

**Payoff:** Documentation never drifts from reality.[^4]

**Try it now:**

1. Create hook in `.claude/settings.json`: `"hooks": { "PostToolUse": { "command": "claude -p 'Update CLAUDE.md Architecture section based on recent changes'" } }`
2. Make any code change
3. Watch CLAUDE.md regenerate automatically

**Inspired by:** https://www.builder.io/blog/claude-md-guide

***

### 4. **Brand Consistency Enforcer**

**What:** PreToolUse hook blocks file writes that violate brand guidelines (wrong colors, fonts, spacing).

**Payoff:** Zero brand drift across team.[^5][^6]

**Try it now:**

1. Create `.claude/brand-rules.json` with design tokens (colors, fonts, spacing)
2. Add PreToolUse hook: `"matcher": { "tool": "Write" }`, script validates file content against brand rules
3. Hook returns exit code 2 to deny writes with violations

**Inspired by:** https://code.claude.com/docs/en/hooks

***

### 5. **Sentiment Analysis Pipeline**

**What:** Headless mode processes hundreds of customer reviews/logs in parallel via fan-out pattern.

**Payoff:** Hours of manual sentiment work → 5 minutes automated.[^4]

**Try it now:**

1. Create `analyze-sentiment.sh`: `for file in logs/*.txt; do claude -p "Analyze sentiment in $file" --output-format stream-json > results/$(basename $file).json; done`
2. Run script in background with `Ctrl+B`
3. Parse JSON results into dashboard

**Inspired by:** https://www.anthropic.com/engineering/claude-code-best-practices (fan-out pattern)

***

### 6. **Game Asset Index Generator**

**What:** Auto-generate `assets.json` from sprite sheets, tilesets, and audio files for game engines (Phaser, Unity, Godot).

**Payoff:** Zero manual asset management; instant game dev iteration.[^7][^8]

**Try it now:**

1. Create skill: `.claude/skills/game-assets.md` with frontmatter describing asset structure
2. Prompt: "Study assets in ./game/assets/ folder and create assets.json index accounting for sprite sheet animations and tilesets"
3. Reference in game code: `const assets = require('./assets.json')`

**Inspired by:** https://www.youtube.com/watch?v=QPZCMd5REP8 (Phaser + Claude Code tutorial)

***

### 7. **Pre-Commit Validation Gate**

**What:** PreToolUse hook blocks `git commit` if tests fail, linting errors exist, or TODOs are present.

**Payoff:** Zero broken commits reach CI/CD.[^9][^5]

**Try it now:**

1. Add PreToolUse hook: `"matcher": { "tool": "Bash", "input": { "command": "git commit*" } }`
2. Hook script runs `npm test && npm run lint && ! grep -r "TODO" src/`
3. Exit code 2 blocks commit with feedback message

**Inspired by:** https://hexdocs.pm/claude/guide-hooks.html

***

### 8. **Automated Refactor Swarm**

**What:** Multi-agent pattern: Leader identifies 47 service objects needing refactor, spawns workers to handle in parallel, verifier runs tests.

**Payoff:** Weeks of refactoring → hours.[^10][^11]

**Try it now:**

1. Create `.claude/agents/refactor-leader.md` and `.claude/agents/refactor-worker.md`
2. Prompt leader: "Refactor all service objects to use new BaseService pattern"
3. Leader spawns workers via TeammateTool, each claims tasks from shared queue

**Inspired by:** https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f

***

### 9. **Multi-Language Localization Generator**

**What:** Subagent reads English strings, spawns 10 translation subagents (one per language), outputs i18n files.

**Payoff:** Manual translation coordination eliminated.[^12]

**Try it now:**

1. Create translation skill with language expertise
2. Prompt: "Translate all strings in en.json to Spanish, French, German, Japanese, Chinese"
3. Use subagent delegation: Claude spawns parallel translation agents

**Inspired by:** https://www.anthropic.com/engineering/multi-agent-research-system

***

### 10. **Deployment Safety Net**

**What:** Multi-agent deploy workflow: pre-flight checks (tests, security scan), deploy, post-deploy smoke tests, log monitoring.

**Payoff:** Zero surprise production failures.[^10]

**Try it now:**

1. Create `.claude/agents/deploy-orchestrator.md` defining team roles
2. Prompt: "Deploy to production with full verification"
3. Orchestrator spawns: test-runner, security-scan, deployer, smoke-tester, perf-compare, log-watcher

**Inspired by:** https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f (Deploy use case)

***

## **Tier 2: Power User Moves (Medium Difficulty, Very High Payoff)**

### 11. **Codebase Brain (Distributed Knowledge System)**

**What:** 5-10 specialist subagents each "own" a domain (models, controllers, services, jobs, tests); leader routes questions to experts.

**Payoff:** Instant codebase understanding without re-reading; persists across sessions.[^10]

**Try it now:**

1. Create agents: `models-expert.md`, `controllers-expert.md`, `services-expert.md`, etc.
2. Leader prompt: "Understand this 500-file codebase and answer questions"
3. Each agent indexes their domain once, leader routes queries to appropriate expert

**Inspired by:** https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f (Codebase Brain pattern)

***

### 12. **Game Development Auto-Tester**

**What:** Playwright skill auto-generates and runs UI tests for game builds; catches regressions before player sees them.

**Payoff:** Continuous game testing without QA team.[^8]

**Try it now:**

1. Install playwright skill: `.claude/skills/playwright-game-testing.md`
2. Prompt: "Generate Playwright tests for all UI buttons and game state transitions"
3. Hook PostToolUse to run tests after every game code change

**Inspired by:** https://www.youtube.com/watch?v=QPZCMd5REP8 (Phaser + testing integration)

***

### 13. **Smart Linter (Beyond Syntax)**

**What:** Headless Claude reviews code for subjective issues: typos in comments, misleading variable names, stale TODOs.

**Payoff:** Code review quality jumps; human reviewers focus on architecture.[^4]

**Try it now:**

1. Create `.github/workflows/smart-lint.yml` triggered on PR
2. Action runs: `claude -p "Review PR #$PR_NUM for typos, misleading names, stale comments" --output-format stream-json`
3. Parse JSON, post findings as PR comments

**Inspired by:** https://www.anthropic.com/engineering/claude-code-best-practices (linter use case)

***

### 14. **6-Month Game Build (Solo Dev → Team)**

**What:** Build full game (120 files, career mode, stadium editor, 3 languages) using CLAUDE.md + skills + plan mode.

**Payoff:** 360 hours of work, solo developer output = 5-person team.[^7]

**Try it now:**

1. Initialize with detailed CLAUDE.md covering architecture, managers, state flow
2. Always start features with: "Here's what I want. Here's my approach. Issues?"
3. Use plan mode (Shift+Tab twice) before every implementation

**Inspired by:** https://www.reddit.com/r/ClaudeCode/comments/1qknr1v/what_i_learned_building_a_full_game_with_claude/ (Jan 2026)

***

### 15. **Plugin Marketplace Distribution**

**What:** Package your entire Claude Code setup (commands, skills, hooks, MCP servers) into installable plugin shared via GitHub.

**Payoff:** One-command setup for entire team; reusable workflows.[^13][^14]

**Try it now:**

1. Run `/plugin init my-workflow` to create manifest
2. Add to `.claude-plugin/marketplace.json`: list your skills/commands/agents
3. Push to GitHub, share: `/plugin marketplace add username/repo`

**Inspired by:** https://code.claude.com/docs/en/plugin-marketplaces

***

### 16. **Build-Test-Verify Loop (Chrome Integration)**

**What:** Claude builds feature, launches Chrome, visually verifies UI matches Figma, runs console checks, iterates.

**Payoff:** Design-dev parity enforced automatically.[^15]

**Try it now:**

1. Enable Chrome integration: `claude --chrome` (requires Pro/Max+)
2. Prompt: "Build login form, open in Chrome, verify against Figma design at [URL]"
3. Claude reads console errors, compares screenshots, suggests fixes

**Inspired by:** https://www.reddit.com/r/ClaudeAI/comments/1pthd5z/spent_this_weekend_with_claude_code_chrome/

***

### 17. **Research Assistant Inside Repos**

**What:** MCP server connects to Sentry, Linear, GitHub; Claude auto-investigates bugs by pulling logs + issues + commits.

**Payoff:** Bug investigation time: 2 hours → 10 minutes.[^10]

**Try it now:**

1. Install MCP servers: `claude mcp add sentry`, `claude mcp add linear`, `claude mcp add github`
2. Prompt: "Users report checkout fails intermittently"
3. Claude spawns parallel agents: log-analyst, code-archaeologist, reproducer, db-detective

**Inspired by:** https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f (Bug Hunt pattern)

***

### 18. **Unity/Godot 3D Scene Automation**

**What:** MCP server exposes Unity/Godot API; Claude creates GameObjects, adds components, adjusts transforms via natural language.

**Payoff:** Scene setup: manual hours → prompted minutes.[^16]

**Try it now:**

1. Install Unity MCP server (community-built or create stdio MCP wrapper)
2. Prompt: "Create 3D scene with player character, camera following at 5m distance, ground plane with collision"
3. Claude executes Unity API commands via MCP

**Inspired by:** https://blogs.infosys.com/.../the-digital-alchemist-vibe-coding-with-unity-mcp...

***

### 19. **Code Review Swarm (Multi-Perspective)**

**What:** Leader spawns 4 reviewers: security-sentinel, performance-oracle, rails-expert, test-coverage; aggregates findings.

**Payoff:** PR review quality = senior architect team.[^10]

**Try it now:**

1. Create 4 agents: `security-reviewer.md`, `performance-reviewer.md`, `conventions-reviewer.md`, `test-reviewer.md`
2. Prompt: "Review PR \#1588 with full team"
3. Leader aggregates findings, posts consolidated feedback

**Inspired by:** https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f (Code Review Swarm)

***

### 20. **Automated B2B Prospect Research**

**What:** Headless mode scrapes company websites, LinkedIn, news; MCP connects to CRM; outputs enriched lead profiles.

**Payoff:** Sales research time: 30 min/lead → 2 min/lead.[^17]

**Try it now:**

1. Create MCP server for CRM API (HubSpot, Salesforce)
2. Script: `claude -p "Research company $COMPANY_NAME, find decision makers, recent funding, tech stack" | post-to-crm.sh`
3. Run in batch for 100 leads

**Inspired by:** https://www.reddit.com/r/ClaudeCode/comments/1mow9gu/how_to_supercharge_your_coding_workflow/ (automation mention)

***

## **Tier 3: Advanced Patterns (High Difficulty, Transformative Payoff)**

### 21. **Multi-Instance Parallel Development**

**What:** 3 Claude Code instances via git worktree: one builds frontend, one builds backend, one reviews PRs; shared task list.

**Payoff:** 3x parallel development velocity.[^17]

**Try it now:**

1. Create worktrees: `git worktree add ../feature-a`, `git worktree add ../feature-b`
2. Start Claude Code in each terminal with shared `CLAUDE_CODE_TASK_LIST_ID=my-project`
3. Instances communicate via task dependencies and git branches

**Inspired by:** https://www.reddit.com/r/ClaudeCode/comments/1mow9gu/how_to_supercharge_your_coding_workflow/

***

### 22. **Self-Documenting API (Live Schema Gen)**

**What:** Stop hook detects API endpoint changes, regenerates OpenAPI schema, updates docs site, posts Slack notification.

**Payoff:** API docs never drift; integration partners always current.[^18]

**Try it now:**

1. Add Stop hook: `"hooks": { "Stop": { "command": "./scripts/regen-openapi.sh" } }`
2. Script extracts routes/models, generates OpenAPI 3.0 spec
3. Deploys to docs site, posts changelog to Slack

**Inspired by:** https://code.claude.com/docs/en/hooks (Stop hook examples)

***

### 23. **Security Policy Enforcement (Zero Trust)**

**What:** PreToolUse hook + LLM-based validation: blocks writes to `.env`, production config, or database migrations without approval workflow.

**Payoff:** Impossible to accidentally leak secrets or break production.[^6][^18]

**Try it now:**

1. Create PreToolUse hook with prompt-based validation: `"matcher": { "tool": "Write" }`
2. Hook prompt: "Is this write safe? Check for secrets, production config, or schema changes"
3. Claude returns `permissionDecision: deny` for violations

**Inspired by:** https://code.claude.com/docs/en/hooks (PermissionRequest decision control)

***

### 24. **Test-Driven Development Chain**

**What:** 5-agent pipeline: architect → test-writer → implementer → test-executor → code-reviewer; each waits for predecessor.

**Payoff:** TDD enforced automatically; zero implementation without tests.[^19][^11]

**Try it now:**

1. Create 5 agents with `blockedBy` dependencies in task system
2. Architect defines interfaces → test-writer creates tests → implementer makes tests pass → executor validates → reviewer checks quality
3. Use Neo4j knowledge graph to store preferred patterns

**Inspired by:** https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how_i_built_a_multiagent_orchestration_system/

***

### 25. **Video Ad Factory (Productized Service)**

**What:** Remotion skill + asset library + brand templates = type product description, render 5 video ad variants in 10 minutes.

**Payoff:** Agency workflow: 2 weeks → 1 hour per client.[^3][^1]

**Try it now:**

1. Create template library: `.claude/video-templates/` with reusable Remotion components
2. Prompt: "Create 3 video ads (15s, 30s, 60s) for SaaS product: [description]. Use brand colors \#1E90FF, Geist font."
3. Claude generates variants, renders with `npx remotion render`

**Inspired by:** https://www.reddit.com/r/AISEOInsider/comments/1qoh4gi/claude_code_remotion_ai_the_fastest_way_to_make/

***

### 26. **Cross-Repo Dependency Updater**

**What:** Multi-instance setup: each Claude monitors a microservice repo, leader coordinates breaking change migrations across 20 repos.

**Payoff:** Monorepo-level coordination without monorepo overhead.[^17]

**Try it now:**

1. Clone 20 repos, one worktree per repo
2. Leader agent reads breaking change, spawns worker per repo
3. Workers update dependencies, run tests, open PRs; leader tracks completion

**Inspired by:** https://www.reddit.com/r/ClaudeCode/comments/1mow9gu/how_to_supercharge_your_coding_workflow/

***

### 27. **Unity 8-Month Build (Career Mode Game)**

**What:** Build complete Unity game (shop system, contracts, finances, European cups) using skills + subagents + audit workflow.

**Payoff:** Solo indie dev output = AA studio team.[^20]

**Try it now:**

1. Create CLAUDE.md with Unity architecture: managers, autoload system, state persistence
2. Generate implementation plan for feature: "/plan Shop system with currency, items, purchase flow"
3. Run custom audit subagent: reviews plan, checks for Unity-specific issues, validates against architecture

**Inspired by:** https://www.youtube.com/watch?v=GxZLC00yJ5g (8 months Unity dev with Claude Code)

***

### 28. **Automated Course Content Pipeline**

**What:** Headless mode generates video scripts → Remotion renders videos → SubagentStop hook uploads to LMS → posts notifications.

**Payoff:** Course creation: weeks → hours.[^3]

**Try it now:**

1. Script: `claude -p "Generate 5-minute lesson script on [topic]" > lesson-$N.txt`
2. Remotion renders video from script
3. SubagentStop hook: `"command": "./upload-to-lms.sh $VIDEO_FILE"`

**Inspired by:** https://www.reddit.com/r/AISEOInsider/comments/1qoh4gi/claude_code_remotion_ai_the_fastest_way_to_make/ (course content use case)

***

### 29. **Contract Analyzer + Legal Assistant**

**What:** MCP connects to document storage; Claude extracts key terms, flags risks, compares to company standards, generates redline suggestions.

**Payoff:** Legal review time: 2 hours → 15 minutes.[^15]

**Try it now:**

1. Create MCP server for Dropbox/Google Drive: `claude mcp add dropbox`
2. Upload contract template with company-approved clauses
3. Prompt: "Review [contract.pdf], compare to template, flag deviations"

**Inspired by:** https://code.claude.com/docs/en/mcp (MCP OAuth use cases)

***

### 30. **Agentic Web Scraper (Self-Healing)**

**What:** Chrome integration + error-handling loop: Claude navigates sites, adapts to layout changes, extracts data, retries on failure.

**Payoff:** Web scraping that doesn't break when sites redesign.[^15]

**Try it now:**

1. Enable Chrome: `claude --chrome`
2. Prompt: "Navigate to [competitor-site], extract pricing table, handle cookie popups and captchas"
3. Claude uses vision to locate elements, adapts to layout changes, saves to CSV

**Inspired by:** https://www.reddit.com/r/ClaudeAI/comments/1pthd5z/spent_this_weekend_with_claude_code_chrome/

***

## **Difficulty × Payoff Matrix**

```
HIGH PAYOFF
    │
    │  [^24]      [^21]      [^27]
    │  [^11]      [^26]      [^30]
    │  [^14]      [^28]      [^23]
    │  ─────────────────────────
    │  [^8]       [^15]      [^22]
    │  [^17]      [^18]      [^25]
    │  [^12]      [^19]      [^29]
    │  ─────────────────────────
    │  [^1]       [^5]       [^10]
    │  [^2]       [^6]       [^13]
LOW │  [^3]       [^7]       [^16]
    │  [^4]       [^9]       [^20]
    └──────────────────────────→
    LOW        MED       HIGH
           DIFFICULTY
```

**Legend:**

- **[1-10]** = Tier 1 (Quick Wins)
- **[11-20]** = Tier 2 (Power User)
- **[21-30]** = Tier 3 (Advanced)

***

## **Build My Superuser Pack Next**

### **Files to Create in `.claude/`**

#### **1. `CLAUDE.md`** (Root Project Memory)

**Purpose:** Auto-loaded facts, architecture decisions, standards
**Contents:**

```markdown
# Project: [Your Project Name]

## Architecture
- Multi-repo setup with [list services]
- State managed via [Redux/Zustand/etc]
- API layer: REST endpoints at /api/v1/*

## Standards
- Use Prettier with 2-space indent
- All commits must pass pre-commit hook
- Components in src/components/, utilities in src/utils/

## Key Decisions
- [Date] Migrated from Class components to Hooks
- [Date] Switched to Tailwind for styling

## Active Constraints
- No browser storage APIs (SecurityError in sandbox)
- Max bundle size: 500KB
```


***

#### **2. `.claude/settings.json`** (Permissions + Hooks)

**Purpose:** Auto-approve trusted operations, run deterministic checks
**Contents:**

```json
{
  "permissions": {
    "allow": [
      { "tool": "Bash", "input": { "command": "git status" } },
      { "tool": "Bash", "input": { "command": "npm test" } },
      { "tool": "Bash", "input": { "command": "npm run build" } }
    ],
    "deny": [
      { "tool": "Write", "input": { "path": ".env" } },
      { "tool": "Write", "input": { "path": "**/production.json" } }
    ]
  },
  "hooks": {
    "PreToolUse": {
      "matcher": { "tool": "Bash", "input": { "command": "git commit*" } },
      "command": "npm test && npm run lint"
    },
    "PostToolUse": {
      "matcher": { "tool": "Write" },
      "command": "prettier --write $TOOL_INPUT_PATH"
    },
    "Stop": {
      "command": "./scripts/update-docs.sh",
      "blocking": false
    }
  }
}
```


***

#### **3. `.claude/commands/`** (Custom Slash Commands)

**`feature.md`** - Scaffold new feature with TDD

```markdown
---
name: feature
description: Create new feature with test-first approach
---

# New Feature Setup

You are creating a new feature: $ARGUMENTS

Follow this workflow:
1. Create test file in tests/ with describe block
2. Write failing tests for expected behavior
3. Implement feature to make tests pass
4. Run full test suite
5. Update CLAUDE.md with feature decision

Use plan mode before implementing.
```

**`review.md`** - Quick code review

```markdown
---
name: review
description: Perform security and performance review
---

# Code Review

Review selected code for:
- Security vulnerabilities (XSS, SQL injection, CSRF)
- Performance issues (N+1 queries, memory leaks)
- Convention violations (check CLAUDE.md standards)
- Test coverage gaps

Provide specific line numbers and fixes.
```


***

#### **4. `.claude/skills/`** (Auto-Loaded Expertise)

**`SECURITY.md`** - Security patterns

```markdown
---
name: security-expert
description: Security review for authentication, authorization, data validation, XSS/CSRF/SQL injection prevention
---

# Security Expertise

When reviewing code for security:

## Authentication
- Check for bcrypt/argon2 password hashing (never plaintext)
- Verify session timeout < 24 hours
- Ensure HTTPS-only cookies with Secure + HttpOnly flags

## Authorization
- Check role-based access control (RBAC) on all endpoints
- Verify user owns resource before modification
- Never trust client-side role checks

## Input Validation
- Sanitize all user input before DB queries
- Use parameterized queries (never string concatenation)
- Validate file uploads (type, size, malware scan)

## Output Encoding
- Escape HTML output to prevent XSS
- Use Content-Security-Policy headers
- Sanitize JSON responses

Auto-load when: auth code, API endpoints, form handling, DB queries.
```

**`REMOTION-VIDEO.md`** - Video generation skill

```markdown
---
name: remotion-video-expert
description: Video automation using Remotion framework for animations, transitions, and programmatic video generation
---

# Remotion Video Expertise

When creating videos with Remotion:

## Setup
```bash
npm install remotion @remotion/cli
npx remotion init
```


## Component Structure

- Each scene = React component with useCurrentFrame() hook
- Animations via interpolate(frame, [inputRange], [outputRange])
- Composition = sequence of scenes with timing


## Best Practices

- Use spring() for natural motion curves
- Sequence clips with <Sequence from={frame} durationInFrames={N}>
- Load assets via staticFile() for bundle optimization
- Render: npx remotion render src/index.ts Main output.mp4

Auto-load when: video, animation, motion graphics, Remotion mentioned.

```

***

#### **5. `.claude/agents/`** (Subagent Definitions)

**`code-reviewer.md`**
```markdown
---
name: code-reviewer
description: Reviews code for quality, conventions, and test coverage
tools: [Read, Grep, Bash]
disallowedTools: [Write, Edit]
---

# Code Reviewer Agent

Role: Review code without modifying it.

Workflow:
1. Read all changed files
2. Check against CLAUDE.md standards
3. Run tests to verify coverage
4. Grep for anti-patterns (TODO, console.log, hardcoded secrets)
5. Report findings with specific line numbers

Return structured feedback:
- Security issues (critical)
- Performance issues (high priority)
- Convention violations (medium priority)
- Suggestions (low priority)
```

**`test-writer.md`**

```markdown
---
name: test-writer
description: Writes comprehensive tests for new features
tools: [Read, Write, Bash]
---

# Test Writer Agent

Role: Write tests before implementation (TDD).

Workflow:
1. Read feature requirements from parent prompt
2. Create test file in tests/ directory
3. Write describe blocks covering:
   - Happy path
   - Edge cases
   - Error conditions
   - Integration scenarios
4. Run tests (should fail initially)
5. Report test structure to parent

Test standards:
- Use Jest/Vitest syntax
- Mock external dependencies
- Aim for 90%+ coverage
- Test behavior, not implementation
```


***

#### **6. `.claude.json`** (MCP Servers)

**Purpose:** Connect external APIs and tools
**Contents:**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sentry"],
      "env": {
        "SENTRY_AUTH_TOKEN": "${SENTRY_TOKEN}"
      }
    },
    "google-drive": {
      "transport": "http",
      "url": "https://mcp.google.com/drive",
      "oauth": {
        "clientId": "${GOOGLE_CLIENT_ID}",
        "clientSecret": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```


***

#### **7. Scripts in `scripts/`**

**`update-docs.sh`** (Stop hook)

```bash
#!/bin/bash
# Auto-update documentation after conversation ends

# Extract recent changes
CHANGES=$(git diff HEAD~1 HEAD --name-only)

# Update architecture doc if code changed
if echo "$CHANGES" | grep -q "src/"; then
  claude -p "Update CLAUDE.md Architecture section based on recent changes in: $CHANGES" > /dev/null
fi

# Regenerate API docs if routes changed
if echo "$CHANGES" | grep -q "routes/"; then
  npm run generate-api-docs
fi
```

**`upload-to-lms.sh`** (SubagentStop hook for video pipeline)

```bash
#!/bin/bash
VIDEO_FILE=$1

# Upload to learning management system
curl -X POST https://lms.example.com/api/videos \
  -F "file=@$VIDEO_FILE" \
  -H "Authorization: Bearer $LMS_API_KEY"

# Post to Slack
curl -X POST https://hooks.slack.com/services/$SLACK_WEBHOOK \
  -d "{\"text\": \"New course video uploaded: $VIDEO_FILE\"}"
```


***

### **Installation Order**

1. **Start with `CLAUDE.md`** - Establish project memory
2. **Configure `settings.json`** - Set permissions and basic hooks
3. **Add 2-3 commands** - Most frequent tasks (feature, review, deploy)
4. **Install 1-2 skills** - Domain expertise (security, performance)
5. **Create 1-2 agents** - Delegation patterns (reviewer, tester)
6. **Connect MCP servers** - External tools as needed
7. **Iterate based on patterns** - Watch which prompts you repeat, automate them

***

### **Validation Checklist**

- [ ] `claude plugin validate .` runs without errors
- [ ] CLAUDE.md auto-loads (check with `/context`)
- [ ] Slash commands appear in autocomplete (type `/`)
- [ ] Skills trigger on relevant prompts (check with `/skills`)
- [ ] Hooks execute at correct lifecycle points (test with dummy write)
- [ ] MCP servers connect successfully (`/mcp list`)
- [ ] Agents spawn when delegated (test with `/agents`)

***

## **Key Patterns Summary**

| Pattern | Use When | Tools | Example |
| :-- | :-- | :-- | :-- |
| **Fan-Out** | Process 100+ items in parallel | Headless mode + shell scripts | Sentiment analysis, image processing |
| **Pipeline** | Sequential handoffs with validation | Subagents with blockedBy dependencies | TDD chain, deploy workflow |
| **Swarm** | Embarrassingly parallel work | TeammateTool + shared task queue | Refactor 50 files, update translations |
| **Council** | Need diverse perspectives | Multiple agents with same task | Security review, architecture decision |
| **Codebase Brain** | Large repos, domain expertise | Specialist agents per directory | 500-file monolith understanding |
| **Enforcement** | Prevent bad actions deterministically | PreToolUse hooks with exit codes | Block secret leaks, brand violations |
| **Auto-Documentation** | Keep docs synchronized | PostToolUse/Stop hooks | Update CLAUDE.md, regenerate API specs |


***

**Sources:**
https://claudefa.st/blog/guide/changelog[^21]
https://code.claude.com/docs/en/mcp[^15]
https://www.youtube.com/watch?v=Tt-hpp87pd0[^1]
https://www.anthropic.com/engineering/claude-code-best-practices[^4]
https://dev.to/rajeshroyal/headless-mode-unleash-ai-in-your-cicd-pipeline-1imm[^22]
https://www.youtube.com/watch?v=44yrAiRf4r4[^2]
https://www.reddit.com/r/ClaudeCode/comments/1qknr1v/what_i_learned_building_a_full_game_with_claude/[^7]
https://www.reddit.com/r/AISEOInsider/comments/1qoh4gi/claude_code_remotion_ai_the_fastest_way_to_make/[^3]
https://www.youtube.com/watch?v=QPZCMd5REP8[^8]
https://www.reddit.com/r/ClaudeCode/comments/1mow9gu/how_to_supercharge_your_coding_workflow/[^17]
https://www.youtube.com/watch?v=GxZLC00yJ5g[^20]
https://blogs.infosys.com/.../the-digital-alchemist-vibe-coding-with-unity-mcp...[^16]
https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f[^10]
https://hexdocs.pm/claude/guide-hooks.html[^5]
https://code.claude.com/docs/en/plugin-marketplaces[^13]
https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how_i_built_a_multiagent_orchestration_system/[^19]
https://code.claude.com/docs/en/hooks[^18]
https://www.brandoncasci.com/2025/09/21/how-to-transform-yourself-into-a-dev-team-using-claude-codes-ai-agents.html[^11]
https://www.anthropic.com/engineering/multi-agent-research-system[^12]
https://www.gend.co/blog/configure-claude-code-hooks-automation[^6]
https://dev.to/rajeshroyal/plugins-share-your-entire-claude-code-setup-with-one-command-294n[^14]
<span style="display:none">[^31][^32]</span>

<div align="center">⁂</div>

[^1]: https://www.youtube.com/watch?v=Tt-hpp87pd0

[^2]: https://www.youtube.com/watch?v=44yrAiRf4r4

[^3]: https://www.reddit.com/r/AISEOInsider/comments/1qoh4gi/claude_code_remotion_ai_the_fastest_way_to_make/

[^4]: https://www.anthropic.com/engineering/claude-code-best-practices

[^5]: https://hexdocs.pm/claude/guide-hooks.html

[^6]: https://www.gend.co/blog/configure-claude-code-hooks-automation

[^7]: https://www.reddit.com/r/ClaudeCode/comments/1qknr1v/what_i_learned_building_a_full_game_with_claude/

[^8]: https://www.youtube.com/watch?v=QPZCMd5REP8

[^9]: https://github.com/anthropics/claude-code/issues/4834

[^10]: https://gist.github.com/kieranklaassen/d2b35569be2c7f1412c64861a219d51f

[^11]: https://www.brandoncasci.com/2025/09/21/how-to-transform-yourself-into-a-dev-team-using-claude-codes-ai-agents.html

[^12]: https://www.anthropic.com/engineering/multi-agent-research-system

[^13]: https://code.claude.com/docs/en/plugin-marketplaces

[^14]: https://dev.to/rajeshroyal/plugins-share-your-entire-claude-code-setup-with-one-command-294n

[^15]: HANDOFF-PACKET-Claude-Code-Mastery-v1.md

[^16]: https://blogs.infosys.com/emerging-technology-solutions/artificial-intelligence/the-digital-alchemist-vibe-coding-with-unity-mcp-and-claude-ai-to-craft-3d-immersive-xr-experiences.html

[^17]: https://www.reddit.com/r/ClaudeCode/comments/1mow9gu/how_to_supercharge_your_coding_workflow/

[^18]: https://code.claude.com/docs/en/hooks

[^19]: https://www.reddit.com/r/ClaudeAI/comments/1l11fo2/how_i_built_a_multiagent_orchestration_system/

[^20]: https://www.youtube.com/watch?v=GxZLC00yJ5g

[^21]: Sean-Winslow-Profile-Context-Compact.md

[^22]: https://dev.to/rajeshroyal/headless-mode-unleash-ai-in-your-cicd-pipeline-1imm

[^23]: https://www.youtube.com/watch?v=dRsjO-88nBs

[^24]: https://www.youtube.com/watch?v=dMpaPgLYj_U

[^25]: https://www.producttalk.org/how-to-build-ai-workflows-with-claude-code/

[^26]: https://www.tiktok.com/@rileybrown.ai/video/7598674903839165726

[^27]: https://code.claude.com/docs/en/common-workflows

[^28]: https://mcpmarket.com/tools/skills/claude-code-plugin-reference-2026

[^29]: https://www.reddit.com/r/ClaudeAI/comments/1qcwckg/the_complete_guide_to_claude_code_v2_claudemd_mcp/

[^30]: https://claudemarketplaces.com

[^31]: https://gist.github.com/kieranklaassen/4f2aba89594a4aea4ad64d753984b2ea

[^32]: https://github.com/claude-code-plugin-marketplaces

