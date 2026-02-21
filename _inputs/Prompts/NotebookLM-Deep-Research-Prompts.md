# NotebookLM Deep Research Prompts for Claude Code Mastery

**Purpose:** Targeted prompts to discover Claude Code superuser tips, tricks, and workflows from the community
**Profile Source:** Sean Winslow's Research Profile Templates
**How to Use:** Copy each prompt into NotebookLM's Deep Research feature, one at a time, to build a comprehensive knowledge base

---

## Understanding NotebookLM Deep Research

### What It Does
NotebookLM's Deep Research feature acts as an "Agentic Researcher" - it analyzes your topic, hunts for ~50 related sources, evaluates them, adapts its search, and builds a research report with citations that can be imported into your notebook.

### Best Practices for These Prompts
1. **Run one prompt at a time** - Don't combine topics
2. **Import the report + sources** - Click "Import" after each Deep Research
3. **Use the Chat feature** - After importing, ask follow-up questions
4. **Create topic-specific notebooks** - Consider separate notebooks for PM, Creative, and Life domains

### Prompt Template Pattern
Each prompt below follows this structure:
- Specific topic focus (not vague)
- Context about your skill level (beginner coder)
- What you want to discover (tips, tricks, workflows)
- Request for practical examples

---

## SECTION 1: Claude Code Core Features

### 1.1 Commands & CLI Basics
```
Claude Code CLI commands and keyboard shortcuts for power users 2025-2026. Include hidden commands, lesser-known flags, and efficiency shortcuts. Focus on commands beyond the basics that intermediate-to-advanced users leverage daily. Provide examples of command combinations and workflows.
```

### 1.2 Skills System
```
Claude Code Skills system deep dive: creating custom SKILL.md files, YAML frontmatter schema, auto-loading triggers, and skill optimization. Include real examples from community power users showing creative skill implementations for PM workflows, game development, and automation tasks.
```

### 1.3 Hooks & Lifecycle Events
```
Claude Code Hooks system for automation: PreToolUse, PostToolUse, Stop, and SubagentStop events. Focus on practical hook implementations including auto-formatting, secret blocking, test running, and custom validation. Include Python and Bash hook examples with exit codes.
```

### 1.4 Subagents & Task Delegation
```
Claude Code subagents for parallel task execution and context isolation. Cover ephemeral agents, tool restrictions with disallowedTools, background subagents, and multi-agent orchestration patterns (swarm, council, codebase brain). Include real workflow examples.
```

### 1.5 MCP (Model Context Protocol)
```
Claude Code MCP server integration guide 2025-2026: connecting external APIs, databases, and tools. Cover stdio vs HTTP transport, OAuth flows, user vs project scope, and practical MCP server implementations for Jira, Slack, Figma, and databases.
```

### 1.6 Plugins & Marketplace
```
Claude Code plugins and marketplace distribution: creating shareable plugin bundles, marketplace.json manifest schema, installing community plugins, and packaging skills/hooks/commands for team distribution. Include examples of popular community plugins.
```

### 1.7 Headless Mode & CI/CD
```
Claude Code headless mode for CI/CD pipelines and automation scripts: -p flag usage, stream-json output format, GitHub Actions integration with anthropics/claude-code-action, and batch processing patterns. Include real CI/CD workflow examples.
```

### 1.8 Permissions & Security
```
Claude Code permissions system and security best practices: allowedTools, permission hierarchy (deny→ask→allow), sandboxing, YOLO mode risks, and enterprise security configurations. Focus on balancing productivity with safety.
```

---

## SECTION 2: PM Workflows in Claude Code

### 2.1 Jira Automation
```
Claude Code workflows for Jira automation: ticket creation, bulk updates, sprint management, and JQL queries. Cover MCP server setup, custom skills for ticket templates, and integration patterns. Include examples for technical PM workflows.
```

### 2.2 PRD & Technical Spec Generation
```
Claude Code for generating Product Requirements Documents and technical specifications: custom PRD skills, interview-style clarifying questions, template structures, and validation workflows. Focus on actionable PRDs that engineering can implement.
```

### 2.3 Stakeholder Communication
```
Claude Code for stakeholder presentations and updates: generating executive summaries, status reports, and communication templates. Cover skills for different audience levels (technical vs non-technical) and automated report generation.
```

### 2.4 Data Analysis & Reporting
```
Claude Code for PM data analysis: CSV processing, metrics dashboards, trend analysis, and automated report generation. Cover integration with analytics tools (GA4, Looker) and creating analysis skills for beginner coders.
```

### 2.5 Documentation & Knowledge Bases
```
Claude Code for documentation workflows: README generation, API docs, knowledge base creation, and doc maintenance. Cover skills for doc-driven development and keeping documentation in sync with code changes.
```

### 2.6 Sprint & Roadmap Planning
```
Claude Code for agile PM workflows: sprint planning automation, roadmap generation, capacity planning, and backlog grooming. Include skills and prompts that bridge PM planning with engineering implementation.
```

---

## SECTION 3: Creative Project Workflows

### 3.1 Phaser 3 Game Development
```
Claude Code for Phaser 3 game development: scene management patterns, sprite animations, physics systems, and game state management. Focus on skills and workflows for a beginner coder building a fitness RPG game with pixel art aesthetics.
```

### 3.2 React Native Mobile Development
```
Claude Code for React Native development: component patterns, navigation setup, state management, debugging workflows, and Expo commands. Cover integration with game engines (Phaser) and skills for mobile app development.
```

### 3.3 Sprite & Asset Pipeline Automation
```
Claude Code for game asset pipelines: sprite sheet generation, animation workflows, asset organization, and integration with AI image generation tools (ComfyUI, Vertex AI). Focus on automation for pixel art and retro-style game assets.
```

### 3.4 AI Creative Workflows
```
Claude Code integration with AI creative tools: ComfyUI workflows, image generation APIs, video generation, and music/audio tools (ElevenLabs). Cover automation patterns for AI-assisted content creation and asset generation.
```

### 3.5 Video & Animation Production
```
Claude Code for video editing and animation workflows: ffmpeg automation, Remotion integration, subtitle generation, and batch video processing. Include skills for automating repetitive video production tasks.
```

### 3.6 Pixel Art & Digital Art
```
Claude Code assistance for pixel art creation: palette management, sprite conventions, animation frame patterns, and art style consistency. Cover workflows that help a non-artist create cohesive game art.
```

---

## SECTION 4: Technical Stack Integration

### 4.1 React/Vite/Tailwind Development
```
Claude Code workflows for React development with Vite and Tailwind CSS: component generation, styling patterns, build optimization, and project scaffolding. Focus on skills that help a beginner coder write clean, modern React code.
```

### 4.2 Python Automation Scripts
```
Claude Code for Python automation: script generation, error handling patterns, file processing, API integrations, and scheduling. Cover skills for a beginner Python developer automating business workflows.
```

### 4.3 Supabase Backend Development
```
Claude Code for Supabase development: database schema design, Row Level Security policies, Edge Functions, real-time subscriptions, and authentication. Include skills for common Supabase patterns and debugging.
```

### 4.4 Cursor IDE Integration
```
Claude Code used alongside Cursor IDE: complementary workflows, when to use each tool, context sharing between them, and productivity patterns for developers using both AI coding assistants.
```

### 4.5 Docker & DevOps
```
Claude Code for Docker workflows: Dockerfile generation, docker-compose setup, container debugging, and deployment automation. Cover skills for developers learning containerization.
```

### 4.6 Git & GitHub Workflows
```
Claude Code for Git workflows: commit message generation, branch management, PR creation, code review automation, and GitHub Actions. Include skills for maintaining clean git history and collaborative development.
```

---

## SECTION 5: Tool Integrations

### 5.1 Figma Integration
```
Claude Code and Figma integration: MCP server setup, design-to-code workflows, component extraction, and design system management. Cover workflows for PMs and developers working with design files.
```

### 5.2 Notion Integration
```
Claude Code with Notion: database syncing, page generation, knowledge base automation, and documentation workflows. Cover MCP servers and skills for Notion power users.
```

### 5.3 Slack Automation
```
Claude Code Slack integration: message automation, channel notifications, bot workflows, and team communication automation. Include MCP server setup and skills for PM communication workflows.
```

### 5.4 WordPress Development
```
Claude Code for WordPress: theme development, plugin creation, content automation, and site maintenance. Cover workflows for technical PMs managing WordPress properties.
```

### 5.5 Salesforce Integration
```
Claude Code with Salesforce: data queries, automation workflows, report generation, and CRM integration patterns. Focus on RevOps and AdOps automation use cases.
```

### 5.6 Analytics (GA4/Looker)
```
Claude Code for analytics workflows: GA4 data extraction, Looker report automation, metrics analysis, and dashboard generation. Cover skills for data-driven PM decision making.
```

---

## SECTION 6: Life Optimization Workflows

### 6.1 Personal Finance Automation
```
Claude Code for personal finance: budget tracking automation, expense categorization, financial report generation, and investment tracking. Cover skills that help automate money management without complex accounting knowledge.
```

### 6.2 Task Management Systems
```
Claude Code for personal productivity: task management automation, to-do list workflows, project organization, and GTD-style systems. Focus on skills that reduce cognitive load for busy professionals.
```

### 6.3 Knowledge Management
```
Claude Code for personal knowledge management: note organization, second brain systems, learning workflows, and information synthesis. Cover skills for capturing and organizing professional knowledge.
```

### 6.4 Time Management & Scheduling
```
Claude Code for time optimization: calendar automation, time blocking workflows, meeting prep automation, and scheduling assistance. Include skills for busy PMs managing multiple projects.
```

### 6.5 Health & Habit Tracking
```
Claude Code for health and habits: fitness tracking automation, habit loop systems, health data analysis, and wellness workflows. Focus on automation for health-conscious professionals.
```

### 6.6 Learning & Skill Development
```
Claude Code for accelerated learning: study workflows, flashcard generation, concept explanation, and skill-building drills. Cover how to use Claude Code as a learning accelerator for technical topics.
```

---

## SECTION 7: Advanced & Experimental Techniques

### 7.1 Multi-Instance Parallel Development
```
Claude Code multi-instance parallelism: running multiple Claude instances simultaneously, shared task lists via CLAUDE_CODE_TASK_LIST_ID, git worktree patterns, and coordination between instances. Include real workflow examples.
```

### 7.2 Context Management Tactics
```
Claude Code context window optimization: CLAUDE.md best practices, context tiering with .tmp files, manual vs auto-compact, and strategies for long-running sessions. Focus on avoiding context overflow in complex projects.
```

### 7.3 Verification Loops
```
Claude Code verification loop patterns: automated testing integration, browser verification, iterating until tests pass, and quality assurance workflows. Cover PostToolUse hooks for continuous verification.
```

### 7.4 Ephemeral Agent Patterns
```
Claude Code ephemeral agents: creating temporary subagents for scoped tasks, auto-cleanup patterns, and dynamic agent generation. Include examples of on-the-fly agent creation and deletion.
```

### 7.5 Plan Mode & Extended Thinking
```
Claude Code Plan Mode vs Extended Thinking: when to use each, keyboard shortcuts (Shift+Tab, Tab), structured ideation workflows, and best practices for complex multi-file changes.
```

### 7.6 Chrome Integration
```
Claude Code Chrome browser integration: --chrome flag, browser automation, UI testing, build-verify loops, and Figma comparison workflows. Cover requirements (Pro/Max plan) and limitations (no WSL).
```

---

## SECTION 8: Domain-Specific Applications

### 8.1 Crypto/Web3 Industry Context
```
Claude Code for crypto and Web3 product development: blockchain terminology, DeFi concepts, crypto news integration, and industry-specific workflows. Focus on PM work at a crypto data/news company.
```

### 8.2 Education Platform Development
```
Claude Code for education platform development: LMS features, course content automation, student progress tracking, and educational content generation. Cover PM workflows for edtech products.
```

### 8.3 API Product Management
```
Claude Code for API product management: API documentation generation, endpoint testing, SDK creation, and developer experience optimization. Focus on technical PM workflows for API products.
```

### 8.4 RevOps & AdOps Automation
```
Claude Code for Revenue Operations and Ad Operations: reporting automation, pipeline management, ad campaign analysis, and operations workflows. Cover skills for operations-heavy PM roles.
```

### 8.5 AI-Native Product Development
```
Claude Code for AI-first product development: prompt engineering workflows, LLM integration patterns, AI feature development, and emerging practices for building AI-powered products.
```

---

## SECTION 9: Community & Learning Resources

### 9.1 Power User Communities
```
Claude Code power user communities and resources 2025-2026: Reddit threads, Discord servers, Twitter/X accounts to follow, GitHub repositories, and forums where advanced users share tips and workflows.
```

### 9.2 Learning Path & Skill Building
```
Claude Code learning path for beginners to power users: progression milestones, skill-building exercises, recommended tutorials, and deliberate practice patterns. Focus on someone with basic coding knowledge.
```

### 9.3 Troubleshooting & Debugging
```
Claude Code troubleshooting guide: common errors, debugging techniques, permission issues, MCP connection problems, and where to find help. Include community resources for getting unstuck.
```

### 9.4 Version Updates & Changelog
```
Claude Code version history and changelog 2025-2026: major feature releases, breaking changes, deprecated features, and upgrade paths. Cover what's new and what's changed for long-term users.
```

### 9.5 Case Studies & Success Stories
```
Claude Code success stories and case studies: real-world implementations, productivity gains, workflow transformations, and lessons learned from power users across different industries.
```

---

## How to Build Your NotebookLM Knowledge Base

### Step 1: Create Topic-Specific Notebooks
Create separate notebooks for:
- "Claude Code - Core Features"
- "Claude Code - PM Workflows"
- "Claude Code - Creative Projects"
- "Claude Code - Life Optimization"
- "Claude Code - Advanced Techniques"

### Step 2: Run Deep Research Systematically
1. Start with Section 1 (Core Features) - run all 8 prompts
2. Import each report and its sources
3. Move to sections most relevant to your current needs
4. Save the best sources to your notebook

### Step 3: Use Chat to Synthesize
After importing research, use NotebookLM's chat to ask:
- "What are the top 5 actionable tips across all sources?"
- "Create a cheat sheet for [specific topic]"
- "What do sources disagree about?"
- "What's the most surprising finding?"

### Step 4: Generate Learning Materials
Use NotebookLM's tools to create:
- Audio Overviews (AI podcasts) for passive learning
- Flashcards for memorization
- Quizzes to test understanding
- Study Guides for structured learning

### Step 5: Export to Gemini
Import your NotebookLM notebooks as sources in Gemini to:
- Combine multiple notebooks
- Generate custom tools/apps
- Build on research with fresh online searches

---

## Quick Reference: High-Priority Prompts

**If you only have time for 10 prompts, start with these:**

1. **1.2 Skills System** - Foundation for customization
2. **1.3 Hooks & Lifecycle Events** - Automation foundation
3. **1.4 Subagents & Task Delegation** - Parallel work
4. **1.5 MCP Integration** - External tool connections
5. **2.1 Jira Automation** - Your daily PM work
6. **3.1 Phaser 3 Game Development** - Your 16BitFit project
7. **3.2 React Native Development** - Your mobile stack
8. **6.1 Personal Finance Automation** - Life optimization
9. **7.1 Multi-Instance Parallel Development** - Power user pattern
10. **9.2 Learning Path & Skill Building** - Your growth trajectory

---

## Sources

This prompt guide was informed by:
- [NotebookLM 2026 Guide - Geeky Gadgets](https://www.geeky-gadgets.com/notebooklm-complete-guide-2026/)
- [NotebookLM + Deep Research - KDnuggets](https://www.kdnuggets.com/notebooklm-deep-research-the-ultimate-learning-hack)
- [How To Use NotebookLM Better Than 99% - Medium](https://medium.com/@ferreradaniel/how-to-use-notebooklm-better-than-99-of-people-deep-research-workflow-guide-4e54199c9f82)
- [10 NotebookLM Super Prompts - Analytics Vidhya](https://www.analyticsvidhya.com/blog/2026/01/notebooklm-super-prompts-for-pro-level-productivity/)
- [Google Workspace NotebookLM Updates](https://workspaceupdates.googleblog.com/2025/12/google-ai-ultra-business-enhanced-notebooklm.html)
