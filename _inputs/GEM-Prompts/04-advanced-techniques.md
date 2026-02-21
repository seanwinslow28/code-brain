# Advanced Techniques - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Advanced Techniques"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals, working across three domains: PM work, creative projects (React Native + Phaser game dev), and life optimization/automation. My stack is React, Python, Supabase, and I use Claude Code as my primary development tool.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers **power-user techniques** that make Claude Code dramatically more effective.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Advanced Techniques") contains deep research on advanced Claude Code patterns: multi-instance parallel development, context window management, CLAUDE.md optimization, verification loops, ephemeral agents, Plan Mode vs Extended Thinking, Chrome integration, security configurations, and experimental/bleeding-edge techniques. Sources include power user discussions, Anthropic documentation, community experiments, and workflow case studies.

## Your Task

Analyze all sources in this notebook and generate **6-7 Claude Skills** that unlock power-user capabilities. These skills represent the difference between basic Claude Code usage and expert-level productivity.

## Target Skills to Extract

### 1. Multi-Instance Parallel Development
**Priority**: High
**What to extract**: Running multiple Claude Code instances simultaneously, git worktree patterns for parallel work, CLAUDE_CODE_TASK_LIST_ID for shared task coordination, avoiding conflicts between instances (file locking, git merge strategies), optimal instance counts for different workflows, and when parallel > sequential.
**Trigger phrases**: "run in parallel", "multiple instances", "worktree", "parallel development", "split this work"

### 2. Context Window Management
**Priority**: High
**What to extract**: Understanding context limits, manual /compact vs auto-compact (when to use each), .tmp file strategy for context tiering (temporary context files that get cleaned up), what to put in CLAUDE.md vs say in conversation, strategies for long-running sessions, recognizing signs of context overflow (repetition, forgetting instructions, quality degradation), and recovery techniques.
**Trigger phrases**: "context window", "running out of context", "compact", "long session", "Claude forgot", "context management"

### 3. CLAUDE.md Optimization
**Priority**: High
**What to extract**: What makes an effective CLAUDE.md (concise, specific, action-oriented rules), what NOT to put in CLAUDE.md (verbose explanations, obvious instructions, things Claude already knows), ideal token size ranges for different project types, the hierarchy (project root > subdirectory > .claude/ folder), update cadence and process, anti-patterns that waste context tokens, and template structures for different project types.
**Trigger phrases**: "CLAUDE.md", "project instructions", "Claude keeps ignoring", "configure project", "improve CLAUDE.md"

### 4. Verification Loops & Quality Assurance
**Priority**: High
**What to extract**: Build-test-fix iteration patterns, PostToolUse hooks for auto-verification, browser verification with --chrome flag, "iterate until tests pass" prompting patterns, screenshot comparison workflows, type checking integration, linting integration, and creating custom verification pipelines.
**Trigger phrases**: "verify this works", "run tests", "check the build", "quality assurance", "iterate until passing", "verification loop"

### 5. Plan Mode & Extended Thinking Mastery
**Priority**: Medium
**What to extract**: Plan Mode activation (double Shift+Tab OR /plan — NEVER document Tab as Plan Mode), Extended Thinking activation (single Tab), when to use Plan Mode (complex multi-file changes, architecture decisions), when to use Extended Thinking (deep reasoning on single problems), structured ideation workflows, and combining both in complex projects.
**CRITICAL RULE**: Plan Mode = double Shift+Tab or /plan. Extended Thinking = single Tab. This distinction is non-negotiable and must be stated correctly in the skill.
**Trigger phrases**: "plan this", "think deeply", "Plan Mode", "Extended Thinking", "complex change", "architecture decision"

### 6. Security & Permissions Hardening
**Priority**: Medium
**What to extract**: Permission hierarchy (Enterprise managed > Project local > Project settings > User settings), evaluation order (Deny > Ask > Allow — first match wins), YOLO mode risks and appropriate use cases, sandboxing options, secret protection patterns, and enterprise vs personal security configurations. Include concrete settings.json examples for different security postures.
**Trigger phrases**: "permissions", "security", "YOLO mode", "lock down", "enterprise security", "sandbox"

### 7. Chrome Integration & Browser Workflows
**Priority**: Lower
**What to extract**: The --chrome flag for browser automation, UI testing patterns, build-then-verify loops (render → screenshot → evaluate → fix), Figma comparison workflows, requirements (Pro/Max plan, no WSL support), and practical browser-in-the-loop development patterns.
**Trigger phrases**: "browser testing", "screenshot", "visual verification", "Chrome", "UI testing"

## Extraction Guidance

- **These are force multipliers**: Each of these techniques can 2-5x productivity. Emphasize the "why this matters" and "when to reach for this" context.
- **Concrete over conceptual**: Include specific commands, flag combinations, and settings — not just descriptions of what's possible.
- **Plan Mode / Extended Thinking accuracy**: This is the #1 source of confusion in the community. The skill MUST get the keyboard shortcuts right: Plan Mode = double Shift+Tab, Extended Thinking = single Tab. Never swap these.
- **Beginner-accessible**: I'm not an expert. Skills should explain advanced techniques in terms I can follow and implement incrementally.
- **Failure recovery**: For each technique, include "what to do when it goes wrong" — context overflow recovery, merge conflicts from parallel instances, etc.
- **Honest limitations**: Include what doesn't work well or when a simpler approach is better.

## Cross-Domain Notes

- **Multi-Instance** is used across all domains (parallel game builds, simultaneous PM tasks)
- **Context Management** is critical for every domain — it's the universal limiting factor
- **CLAUDE.md** is the backbone of every domain playground
- **Verification Loops** connect to Creative Projects (visual verification) and Technical Stack (test suites)
- **Plan Mode** connects to PM Workflows (architecture decisions, complex specs)
- **Security** connects to Core Features (permissions, hooks) and Enterprise configurations

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include specific commands, keyboard shortcuts, and configuration snippets
- Be accurate about Plan Mode vs Extended Thinking shortcuts (this is non-negotiable)
- Help me recognize WHEN to use each technique, not just HOW
- Include progressive difficulty (start simple, build complexity)
- Reference concrete metrics where available (e.g., context window sizes, recommended token budgets)

---

## PROMPT END
