# Technical Stack - Skill Extraction Prompt

Use this prompt with the **Claude SKILL Creator GEM** after connecting your **"Claude Code - Technical Stack"** NotebookLM notebook as a source.

---

## PROMPT START — Copy everything below this line into the GEM

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I'm a beginner coder learning fundamentals. My primary tech stack is React (Vite + Tailwind), Python, and Supabase. I also work with Docker, Git/GitHub, and use Cursor IDE alongside Claude Code. I'm learning these tools through projects rather than formal CS education.

I'm building a system of **domain-specific Claude Code playgrounds** — each a self-contained environment with skills tailored to a specific topic. This notebook covers my **technical stack and development tools** — the languages, frameworks, and infrastructure I use daily.

## What's in This Notebook

This NotebookLM notebook ("Claude Code - Technical Stack") contains deep research on using Claude Code with specific development technologies: React/Vite/Tailwind development patterns, Python automation scripting, Supabase backend development, Docker/DevOps workflows, Git/GitHub workflows, and Cursor IDE integration. Sources include framework documentation, tutorial content, development best practices, and AI-assisted coding guides.

## Your Task

Analyze all sources in this notebook and generate **5-6 Claude Skills** that make Claude Code an expert pair programmer for my specific tech stack. These skills should help a beginner coder write clean, modern code with best practices baked in.

## Target Skills to Extract

### 1. React + Vite + Tailwind Development
**Priority**: High
**What to extract**: React component generation patterns (functional components, hooks, custom hooks), Vite project scaffolding and configuration, Tailwind CSS utility patterns for common layouts, responsive design patterns, component composition best practices, state management approaches (useState, useReducer, Context, when to reach for Zustand), and project structure conventions. Focus on patterns that produce clean, modern React code.
**Trigger phrases**: "React component", "Tailwind", "Vite", "frontend", "create a component", "styling", "responsive design", "state management"

### 2. Python Automation Scripts
**Priority**: High
**What to extract**: Script generation patterns for common automation tasks (file processing, API calls, data transformation, CSV manipulation, web scraping), error handling patterns (try/except with useful messages), virtual environment management, dependency management (pip, requirements.txt), scheduling scripts (cron patterns), and writing scripts that are maintainable by a beginner. Focus on practical automation, not software engineering fundamentals.
**Trigger phrases**: "Python script", "automate", "process files", "API call", "web scraping", "CSV", "cron job", "data processing"

### 3. Supabase Backend Development
**Priority**: High
**What to extract**: Database schema design patterns (tables, relationships, indexes), Row Level Security (RLS) policies for common patterns (user-owned data, team data, public data), Edge Functions (Deno runtime), real-time subscriptions, authentication setup (email, OAuth, magic links), storage buckets for file uploads, and common Supabase client patterns in React. Include actual SQL for migrations and RLS policies.
**Trigger phrases**: "Supabase", "database", "RLS", "Edge Function", "authentication", "real-time", "storage", "migration"

### 4. Git & GitHub Workflows
**Priority**: Medium
**What to extract**: Clean commit message conventions, branch management strategies (feature branches, release branches), PR creation and review workflow, GitHub Actions basics (CI/CD templates for React and Python), resolving merge conflicts, git history management (squash, rebase — when and why), and .gitignore patterns for React/Python/Supabase projects.
**Trigger phrases**: "git commit", "branch", "pull request", "PR", "merge conflict", "GitHub Actions", "CI/CD", "gitignore"

### 5. Docker & DevOps Basics
**Priority**: Medium
**What to extract**: Dockerfile patterns for React and Python apps, docker-compose for local development (app + Supabase + database), debugging container issues, environment variable management, basic deployment patterns, and when containerization helps vs adds complexity for a beginner. Focus on practical "get it running in Docker" patterns, not Kubernetes-level orchestration.
**Trigger phrases**: "Docker", "Dockerfile", "docker-compose", "containerize", "deploy", "environment variables"

### 6. Cursor IDE + Claude Code Integration
**Priority**: Lower
**What to extract**: When to use Cursor vs Claude Code (complementary use cases), context sharing patterns between tools, Cursor-specific features that complement Claude Code (inline edits, Composer), workflow patterns for developers using both AI assistants, and avoiding conflicts between them.
**Trigger phrases**: "Cursor", "which tool should I use", "Cursor vs Claude Code", "use both"

## Extraction Guidance

- **Beginner-appropriate**: I'm learning these tools. Skills should explain patterns, not just dump code. Include "why this approach" context.
- **Modern patterns only**: React hooks (not class components), modern Python (3.10+, type hints), Vite (not Create React App), Tailwind v4, Supabase v2. Don't include legacy patterns.
- **Copy-paste ready**: Include actual code snippets that work — import statements, file paths, all dependencies listed.
- **Common patterns first**: For each technology, focus on the 10 patterns that cover 90% of daily use cases. Don't try to be comprehensive.
- **Error handling**: Include what errors I'll commonly see and how to fix them. Beginners spend most time debugging, not writing.
- **Security awareness**: Flag common security mistakes (exposed API keys, SQL injection in raw queries, XSS in React) and include the safe pattern.

## Cross-Domain Notes

- **React skill** connects to Creative Projects (React Native), Master Designer (UI components), and Remotion Mastery (React-based video)
- **Python skill** connects to Life Optimization (automation scripts) and PM Workflows (data analysis)
- **Supabase skill** connects to Creative Projects (16BitFit game backend) and Domain Specific (crypto product backends)
- **Git skill** connects to Core Features (headless mode CI/CD) and Advanced Techniques (multi-instance coordination)
- **Docker skill** connects to Advanced Techniques (deployment) and Domain Specific (production infrastructure)

## Quality Bar

Each generated skill should:
- Have a description that clearly states BOTH what it does AND when Claude should auto-load it
- Include modern, current-version patterns (not deprecated APIs)
- Provide code that works out of the box — all imports included, no undefined variables
- Include both the pattern AND when to use it (decision framework)
- Flag common beginner mistakes for each pattern
- Be stack-specific (React, not Angular; Vite, not Webpack; Supabase, not Firebase)

---

## PROMPT END
