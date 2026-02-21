# Community Resources - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Community Resources"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals. I'm actively learning Claude Code and want to accelerate my growth by leveraging community knowledge, proven learning paths, and troubleshooting resources. My stack is React, Python, Supabase.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers **community knowledge, learning resources, and growth paths** for Claude Code mastery.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Community Resources") contains deep research on the Claude Code community ecosystem: power user communities (Reddit, Discord, Twitter/X, GitHub), learning paths and progression milestones, troubleshooting guides, version history and changelogs, and case studies/success stories. Sources include community discussions, official release notes, learning guides, and user testimonials.

## Your Task

Analyze all sources in this notebook and generate **4-5 Claude Skills** that help me learn and troubleshoot Claude Code more effectively. These skills are about the meta-game: learning faster, getting unstuck sooner, and staying current.

## Target Skills to Extract

### 1. Troubleshooting & Debug Guide
**Priority**: High
**What to extract**: Common Claude Code errors and their fixes (MCP connection failures, permission errors, context overflow symptoms, hook failures, sandbox issues), debugging techniques (verbose logging, isolating problems, reading error messages), where to find help (GitHub issues, Discord channels, Reddit threads), and a decision tree for "Claude is acting weird — what do I check first?"
**Trigger phrases**: "not working", "error", "broken", "debug", "troubleshoot", "help", "stuck", "why is Claude", "fix this"

### 2. Learning Path & Progression
**Priority**: High
**What to extract**: Structured progression from beginner to power user (specific milestones, not vague goals), skill-building exercises and drills (deliberate practice), recommended sequence for learning features (what first, what can wait), weekly/monthly progression checkpoints, and how to self-assess your skill level. Focus on someone with basic coding knowledge who learns by doing.
**Trigger phrases**: "learning path", "what should I learn next", "practice exercises", "skill level", "progression", "beginner to advanced"

### 3. What's New & Changelog Navigator
**Priority**: Medium
**What to extract**: How to stay current with Claude Code updates (official channels, release notes, community announcements), major feature releases and what they changed, deprecated features to avoid, breaking changes and upgrade paths, and a framework for evaluating "should I adopt this new feature now or wait?" Focus on 2025-2026 changes.
**Trigger phrases**: "what's new", "latest update", "changelog", "new features", "deprecated", "version", "breaking changes"

### 4. Community Navigation Guide
**Priority**: Medium
**What to extract**: Best communities for Claude Code discussion (subreddits, Discord servers, Twitter/X accounts, GitHub repos), what each community is good for (beginner questions vs advanced techniques vs bug reports), community etiquette, how to ask good questions, and notable community members/projects to follow.
**Trigger phrases**: "community", "where to ask", "Discord", "Reddit", "who to follow", "resources", "best practices"

### 5. Case Studies & Pattern Library
**Priority**: Lower
**What to extract**: Real-world success stories of Claude Code implementations (what was built, what approach was used, what were the results), productivity gains reported by users, workflow transformation patterns, lessons learned from failures, and extractable patterns that apply to my domains (PM, creative, life automation).
**Trigger phrases**: "case study", "success story", "what have people built", "real world example", "how did they", "workflow example"

## Extraction Guidance

- **Actionable troubleshooting**: The troubleshooting skill is the highest priority. When I'm stuck at 10 PM, I need a skill that helps Claude Code help me diagnose the problem — not a link to a community forum.
- **Progression over completeness**: The learning path should be opinionated about sequence. "Learn hooks before subagents because X" is more useful than listing all features equally.
- **Freshness matters**: Community resources and changelogs become stale. Structure skills so they're easy to update. Include instructions for Claude to check for more recent information.
- **Signal over noise**: Community resources include a lot of noise. Skills should help me find the signal — the truly useful discussions, the authoritative voices, the actionable threads.
- **Beginner empathy**: I'm the target user of the troubleshooting and learning path skills. They should never assume knowledge I don't have. Explain things progressively.

## Cross-Domain Notes

- **Troubleshooting** is used across ALL domains — every playground needs this
- **Learning Path** connects to Core Features (what to learn first), Advanced Techniques (what to learn later), and all domain skills (practice exercises)
- **Changelog** connects to Core Features (feature inventory) and Advanced Techniques (new capabilities)
- **Community** connects to all domains (finding domain-specific help and examples)
- **Case Studies** feed into every domain (PM patterns, creative patterns, automation patterns)

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Be a tool Claude can use to help me in real-time, not a static reference document
- Include decision trees or flowcharts for troubleshooting (not just lists of errors)
- Prioritize the most common scenarios (80/20 rule)
- Be structured for easy updating as new information emerges
- Include links or search terms for finding deeper help when the skill can't resolve the issue

---

## PROMPT END
