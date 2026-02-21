# NotebookLM Synthesis & Follow-Up Questions

**Purpose:** Questions to ask NotebookLM Chat after importing Deep Research sources
**Goal:** Extract maximum value, filter for quality, and build actionable knowledge

---

## Part 1: General Synthesis Questions (Use for ANY Notebook)

### Understanding the Landscape

```
What are the top 10 most actionable insights across all sources?
```

```
Summarize the key themes that appear in multiple sources. What do experts agree on?
```

```
What are the most frequently mentioned tools, commands, or techniques?
```

```
Create a "TL;DR" summary of everything I need to know in under 500 words.
```

```
What would a complete beginner need to understand first before diving into advanced topics?
```

### Finding Contradictions & Debates

```
What do sources disagree about? List the specific contradictions and which sources take which position.
```

```
Are there any outdated claims in these sources? Flag anything that might have changed since publication.
```

```
What topics are controversial or have multiple valid approaches? Explain the tradeoffs of each.
```

```
Which sources seem most authoritative and why? Which seem less reliable?
```

### Discovering Hidden Gems

```
What's the most surprising or unexpected insight that I probably wouldn't have found on my own?
```

```
What "non-obvious" techniques or workflows do power users mention that beginners typically miss?
```

```
Are there any "hidden features" or lesser-known capabilities mentioned across sources?
```

```
What creative or unconventional use cases are described that go beyond typical usage?
```

### Making It Actionable

```
Create a prioritized checklist of things I should try, ordered from easiest to most complex.
```

```
What can I implement TODAY with minimal setup? List quick wins.
```

```
What requires more preparation or learning before I can use it effectively?
```

```
Create a "30-day learning plan" based on the insights from these sources.
```

### Building Mental Models

```
Create a visual diagram or mental model that explains how all the concepts relate to each other.
```

```
What's the "big picture" framework I should use to think about this topic?
```

```
Explain this topic as if I'm a beginner coder who understands fundamentals but not advanced concepts.
```

```
What analogies or metaphors do sources use to explain complex concepts?
```

---

## Part 2: Source Quality & Filtering Questions

### Evaluating Source Quality

```
Rank all sources from most to least useful for someone at my skill level (beginner coder, PM background). Explain your ranking.
```

```
Which sources are official documentation vs community content vs opinion pieces? Categorize them.
```

```
Which sources have the most concrete, copy-paste-ready examples vs abstract explanations?
```

```
Flag any sources that seem outdated (pre-2025) or reference deprecated features.
```

```
Which sources are from verified experts or Anthropic employees vs anonymous users?
```

### Filtering for Relevance

```
Which 5 sources are MOST relevant for a Product Manager learning Claude Code?
```

```
Which sources focus on beginner-friendly content vs advanced/expert content?
```

```
Which sources have practical tutorials vs conceptual overviews?
```

```
Are any sources redundant or cover the same information? Which one is better?
```

### Deciding What to Keep

```
If I could only keep 5 sources in this notebook, which should they be and why?
```

```
Which sources should I move to a different topic notebook? Suggest the better fit.
```

```
Which sources are comprehensive references I'll return to often vs one-time reads?
```

```
Create a "source quality scorecard" rating each source on: accuracy, actionability, recency, depth.
```

---

## Part 3: Topic-Specific Notebook Questions

### 📁 Notebook: "Claude Code - Core Features"

#### Understanding the Architecture
```
Create a complete map of Claude Code's architecture: CLI → Skills → Hooks → Subagents → MCP → Plugins. How do they interact?
```

```
What's the execution order when I run a Claude Code command? Walk me through the lifecycle.
```

```
What are the configuration files I need to know about and what does each one control?
```

#### Skills Deep Dive
```
What makes a SKILL.md file effective vs ineffective? Extract best practices from sources.
```

```
What are the exact YAML frontmatter fields and which ones are required vs optional?
```

```
How does Claude Code decide which skill to auto-load? What triggers skill selection?
```

```
What are examples of poorly-written skills and how should they be improved?
```

#### Hooks Deep Dive
```
Create a complete reference of all hook types, their triggers, and exit codes.
```

```
What are the most commonly used hooks in the community? Compile examples.
```

```
What's the difference between blocking:true and blocking:false hooks?
```

```
What can go wrong with hooks? List common pitfalls and how to avoid them.
```

#### Subagents Deep Dive
```
When should I use a subagent vs a skill vs a hook? Create a decision framework.
```

```
How do I restrict what tools a subagent can access? Show the syntax.
```

```
What are the limitations of subagents? What can't they do?
```

```
How do background subagents differ from foreground subagents?
```

#### MCP Deep Dive
```
What MCP servers are most commonly used by the community? List with descriptions.
```

```
What's the difference between user scope, project scope, and managed scope for MCP?
```

```
How do I troubleshoot when an MCP connection fails?
```

```
What are the security implications of MCP servers? What should I be careful about?
```

#### Commands & Shortcuts
```
Create a complete keyboard shortcuts cheat sheet from all sources.
```

```
What CLI flags are mentioned and what does each one do?
```

```
What's the difference between / commands vs @ mentions vs keyboard shortcuts?
```

---

### 📁 Notebook: "Claude Code - PM Workflows"

#### Jira Integration
```
What are all the ways to integrate Claude Code with Jira mentioned across sources?
```

```
Create a step-by-step guide for setting up Jira automation with Claude Code.
```

```
What JQL queries are commonly used with Claude Code? Compile examples.
```

```
How can I batch-create or batch-update Jira tickets using Claude Code?
```

#### PRD & Spec Writing
```
What PRD templates or structures do sources recommend? Compare approaches.
```

```
How should I structure a skill that helps generate PRDs? What questions should it ask?
```

```
What makes a PRD "engineering-ready"? Extract quality criteria from sources.
```

```
How can Claude Code help validate specs before sending to engineering?
```

#### Stakeholder Communication
```
What templates exist for stakeholder updates, executive summaries, or status reports?
```

```
How can I tailor the same information for technical vs non-technical audiences?
```

```
What automation patterns help with recurring stakeholder communication?
```

#### Data Analysis
```
How can a non-data-scientist use Claude Code for basic data analysis?
```

```
What file formats can Claude Code process for analysis? (CSV, JSON, etc.)
```

```
How can I generate charts or visualizations from data using Claude Code?
```

```
What skills would help me analyze product metrics and create reports?
```

#### PM-Specific Workflows
```
What PM workflows are specifically mentioned in sources? List all of them.
```

```
How can Claude Code help with user research synthesis or interview analysis?
```

```
What automation patterns help with sprint planning or backlog grooming?
```

```
How do PMs use Claude Code differently than engineers? Extract patterns.
```

#### Beginner-Friendly Approaches
```
What PM workflows are easiest to automate for someone new to Claude Code?
```

```
What are common mistakes PMs make when first using Claude Code for work?
```

```
Create a "PM Quick Start" guide based on what sources recommend.
```

---

### 📁 Notebook: "Claude Code - Creative Projects"

#### Game Development
```
What game development patterns are mentioned across sources? Focus on 2D games.
```

```
How do people use Claude Code for Phaser 3 specifically? Compile all mentions.
```

```
What game dev tasks is Claude Code particularly good or bad at?
```

```
How can Claude Code help with game design (mechanics, balance, progression)?
```

#### React Native
```
What React Native patterns or workflows are mentioned in sources?
```

```
How can Claude Code help debug React Native issues?
```

```
What's the recommended setup for using Claude Code with Expo?
```

```
How do people integrate Phaser games into React Native apps?
```

#### Asset Pipelines
```
What asset pipeline automation is mentioned? (sprites, audio, etc.)
```

```
How can Claude Code work with image generation tools like ComfyUI?
```

```
What file formats and conversions can Claude Code handle for game assets?
```

```
How do people automate sprite sheet generation or animation workflows?
```

#### AI Creative Tools
```
What AI creative tool integrations are mentioned? (image, video, audio, music)
```

```
How can Claude Code orchestrate multi-tool creative workflows?
```

```
What MCP servers or APIs are used for creative work?
```

```
How do people use Claude Code with ElevenLabs, Midjourney, or similar tools?
```

#### Video & Animation
```
What video editing automation is possible with Claude Code?
```

```
How does Remotion integration work? Is it practical?
```

```
What ffmpeg commands are commonly automated through Claude Code?
```

#### Creative Workflow Patterns
```
What's the typical creative workflow when using Claude Code? Describe the loop.
```

```
How do artists/creators who aren't programmers use Claude Code effectively?
```

```
What creative projects have people built entirely with Claude Code assistance?
```

---

### 📁 Notebook: "Claude Code - Life Optimization"

#### Personal Finance
```
What personal finance automations are mentioned in sources?
```

```
How can Claude Code help categorize expenses or track spending?
```

```
What integrations exist for banking, budgeting apps, or financial tools?
```

```
How do people use Claude Code for investment tracking or analysis?
```

#### Task & Project Management
```
What personal productivity systems (GTD, etc.) are mentioned with Claude Code?
```

```
How can Claude Code integrate with personal task managers (Todoist, Things, etc.)?
```

```
What automation patterns help manage personal projects alongside work projects?
```

#### Time Management
```
How can Claude Code help with calendar management or scheduling?
```

```
What meeting prep automations do people use?
```

```
How can Claude Code help with time tracking or time audits?
```

#### Knowledge Management
```
How do people use Claude Code for personal knowledge bases or note-taking?
```

```
What second-brain or PKM integrations are mentioned? (Obsidian, Notion, etc.)
```

```
How can Claude Code help synthesize information from multiple sources?
```

#### Learning & Skill Building
```
How do people use Claude Code to learn new technical skills faster?
```

```
What learning patterns or drills are mentioned for Claude Code mastery?
```

```
How can Claude Code generate practice exercises or flashcards?
```

#### Health & Habits
```
What health or fitness tracking integrations are mentioned?
```

```
How can Claude Code help with habit tracking or habit formation?
```

```
What wellness-related automations do people use?
```

#### Life Admin Automation
```
What "life admin" tasks have people successfully automated?
```

```
What's the ROI on life automation - is it worth the setup time?
```

```
What are the easiest life optimizations to implement for quick wins?
```

---

### 📁 Notebook: "Claude Code - Advanced Techniques"

#### Multi-Instance Patterns
```
What multi-instance patterns are described? How do people coordinate them?
```

```
How does CLAUDE_CODE_TASK_LIST_ID work for sharing tasks between instances?
```

```
What problems arise with multiple instances and how do you avoid them?
```

```
What's the optimal number of parallel instances for different workflows?
```

#### Context Management
```
What context management strategies are mentioned? Compare approaches.
```

```
How do power users prevent context overflow in long sessions?
```

```
What's the .tmp file strategy and how does it work?
```

```
How does manual /compact differ from auto-compact? When use each?
```

#### CLAUDE.md Optimization
```
What makes an effective CLAUDE.md file? Extract best practices.
```

```
What should NOT go in CLAUDE.md? What are anti-patterns?
```

```
How often should CLAUDE.md be updated and by what process?
```

```
What's the ideal token size for CLAUDE.md for different project types?
```

#### Verification & Quality Loops
```
What verification loop patterns are described for ensuring quality?
```

```
How do people integrate automated testing with Claude Code workflows?
```

```
What "iterate until passing" patterns exist?
```

#### Security & Permissions
```
What security best practices are emphasized across sources?
```

```
What are the risks of different permission configurations?
```

```
How do teams balance productivity with security in Claude Code setups?
```

#### Experimental Techniques
```
What experimental or bleeding-edge techniques are mentioned?
```

```
What do sources say about features that might change or are in beta?
```

```
What techniques work but aren't officially documented?
```

---

## Part 4: Cross-Notebook Synthesis Questions

After building multiple notebooks, use these questions in Gemini by importing notebooks as sources:

### Connecting the Dots
```
Looking across all my Claude Code notebooks, what are the universal principles that apply everywhere?
```

```
What skills or hooks would benefit MULTIPLE areas (PM, Creative, Life)? Identify crossover.
```

```
Where do my notebooks have gaps? What topics am I missing coverage on?
```

### Building Your System
```
Based on all sources, design my ideal Claude Code setup including: settings.json, CLAUDE.md, skills, hooks, and agents.
```

```
Create a "Day 1 Setup Checklist" that configures Claude Code optimally for my profile.
```

```
What's the minimum viable setup vs the full power-user setup? Compare.
```

### Prioritization
```
If I have 10 hours to invest in Claude Code mastery, how should I allocate them based on sources?
```

```
What gives the highest ROI for someone with my profile (PM, beginner coder, game dev hobby)?
```

```
What should I learn first vs what can wait until I'm more advanced?
```

---

## Part 5: Output Generation Questions

After synthesis, use these to generate learning materials:

### For Audio Overviews
```
Create a podcast-style conversation explaining Claude Code to a Product Manager who codes as a hobby.
```

```
Generate a debate between "Skills-first" vs "Hooks-first" approaches to Claude Code mastery.
```

### For Flashcards
```
Generate flashcards for all Claude Code keyboard shortcuts and commands.
```

```
Create flashcards for the most important configuration options and what they do.
```

### For Study Guides
```
Create a structured study guide for Claude Code mastery, organized by week.
```

```
Generate a "concept map" showing how all Claude Code features relate.
```

### For Quizzes
```
Create a quiz to test my understanding of Claude Code architecture.
```

```
Generate scenario-based questions: "When would you use X vs Y?"
```

---

## Quick Reference: Best Questions by Goal

| If You Want To... | Ask This |
|-------------------|----------|
| Get started fast | "What can I implement TODAY with minimal setup?" |
| Find quality sources | "Rank sources by usefulness for my skill level" |
| Discover hidden features | "What non-obvious techniques do power users mention?" |
| Resolve confusion | "What do sources disagree about?" |
| Filter your sources | "If I could only keep 5 sources, which ones?" |
| Build understanding | "Create a mental model of how all concepts relate" |
| Make a plan | "Create a 30-day learning plan based on sources" |
| Go deep on one topic | "Extract all mentions of [specific topic]" |
