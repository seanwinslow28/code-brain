# Life Optimization - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Life Optimization"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals. Beyond work and creative projects, I use Claude Code to automate personal life tasks: finance tracking, task management, knowledge management, health/fitness tracking, and general life admin. My stack is React, Python, Supabase.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers using Claude Code for **personal life automation and optimization**.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Life Optimization") contains deep research on using Claude Code for personal productivity: finance automation, task management systems, knowledge management (PKM), time management, health/habit tracking, learning acceleration, and life admin automation. Sources include productivity guides, personal automation examples, PKM methodologies, and community workflows.

## Your Task

Analyze all sources in this notebook and generate **5-7 Claude Skills** that turn Claude Code into a life management assistant. These skills handle personal tasks that don't fit into PM or creative work but consume significant time and mental energy.

## Target Skills to Extract

### 1. Personal Finance Automation
**Priority**: High
**What to extract**: Budget tracking workflows (CSV import, categorization, monthly summaries), expense categorization patterns (regex matching, merchant mapping), financial report generation (monthly/quarterly/annual), savings goal tracking, investment portfolio overview, and integrating with banking exports. Focus on Python scripts that process financial data and generate actionable summaries.
**Trigger phrases**: "budget", "expenses", "finance report", "spending analysis", "financial summary", "track spending", "categorize transactions"

### 2. Task & Project Management System
**Priority**: High
**What to extract**: Personal task management automation (beyond work Jira), GTD-style inbox processing, project organization patterns, recurring task handling, priority frameworks for personal projects, integration patterns with task managers (Todoist, Things, Apple Reminders), and weekly review automation.
**Trigger phrases**: "personal tasks", "organize my projects", "weekly review", "GTD", "inbox zero", "task management", "what should I work on"

### 3. Learning Acceleration & Skill Building
**Priority**: High
**What to extract**: Spaced repetition generation (flashcard creation from study material), concept explanation workflows (ELI5, progressive depth), coding drill generation, learning path creation, practice exercise generation, study guide creation, and techniques for using Claude Code as a tutor for technical topics.
**Trigger phrases**: "teach me", "explain", "create flashcards", "learning plan", "practice exercises", "study guide", "drill"

### 4. Knowledge Management & Second Brain
**Priority**: Medium
**What to extract**: Note organization patterns, information synthesis workflows (combine multiple sources into structured notes), personal wiki maintenance, capturing insights from conversations, linking related concepts, and building a searchable personal knowledge base. (Note: Obsidian-specific patterns are in the Obsidian Integration notebook — this skill covers the general methodology.)
**Trigger phrases**: "organize my notes", "synthesize", "knowledge base", "second brain", "link these concepts", "summarize and store"

### 5. Time Management & Scheduling
**Priority**: Medium
**What to extract**: Calendar analysis patterns (where does my time go?), time blocking workflows, meeting prep automation (agenda creation, context gathering, pre-reads), scheduling optimization, and time audit scripts that process calendar exports.
**Trigger phrases**: "meeting prep", "time audit", "calendar analysis", "schedule", "time blocking", "prepare for meeting"

### 6. Health & Habit Tracking
**Priority**: Lower
**What to extract**: Fitness data processing (workout logs, progress tracking), habit loop automation (cue → routine → reward tracking), health data analysis patterns, nutrition tracking helpers, and streak/consistency visualization. Focus on simple CSV/JSON processing rather than complex health APIs.
**Trigger phrases**: "track habits", "workout log", "fitness progress", "habit tracking", "health data", "streak"

### 7. Life Admin Automation
**Priority**: Lower
**What to extract**: Recurring life admin task automation (bills, subscriptions, renewals), document organization, email processing patterns, comparison shopping helpers, travel planning workflows, and general "adulting" task automation. Focus on templates and scripts for tasks that are annoying but necessary.
**Trigger phrases**: "life admin", "automate this recurring task", "organize files", "compare options", "travel planning"

## Extraction Guidance

- **Privacy-first**: These skills handle personal data (finances, health, habits). Include reminders about data privacy — never send sensitive personal data to external APIs unnecessarily. Prefer local processing.
- **CSV/JSON focus**: Most personal data comes as CSV exports from banks, health apps, and productivity tools. Skills should be excellent at processing these formats.
- **Python scripts**: Life automation leans heavily on Python. Include runnable Python snippets for data processing, not just conceptual descriptions.
- **Low-friction entry**: The biggest barrier to life automation is setup cost. Skills should start with "minimum viable automation" that provides value immediately, with optional enhancements.
- **Sustainability**: Overly complex systems get abandoned. Emphasize simple, maintainable automation over clever but brittle solutions.
- **Templates over code where possible**: For things like meeting prep or weekly reviews, a good template is more valuable than a script.

## Cross-Domain Notes

- **Finance skill** connects to PM Workflows (data analysis patterns) and Technical Stack (Python scripting)
- **Task Management** connects to PM Workflows (sprint planning, Jira) — but this skill is for PERSONAL tasks, not work
- **Learning Acceleration** connects to Community Resources (learning paths) and Core Features (understanding Claude Code itself)
- **Knowledge Management** connects directly to Obsidian Integration (the technical implementation) — this skill covers the methodology
- **Time Management** connects to PM Workflows (meeting prep) — overlap is fine, different context
- **Health Tracking** connects to Creative Projects (16BitFit fitness RPG game data)

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include concrete Python scripts or templates that work immediately
- Default to local data processing (no unnecessary API calls for personal data)
- Start with the simplest useful version, with "Level 2" and "Level 3" enhancements
- Be maintainable by a beginner coder — no complex infrastructure
- Include example input/output so I know what to expect

---

## PROMPT END
