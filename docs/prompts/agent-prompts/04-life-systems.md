# Life Systems — Agent Extraction Prompt

Use this prompt with the **Agent Extraction Kickoff** after connecting to the **"Claude Code - Life Optimization"** NotebookLM notebook.

---

## PROMPT START — Process this domain with the Kickoff Prompt

---

## Who I Am

I'm Sean, an Associate PM (Technical) at a crypto company. I track personal finance, health habits, learning goals, and task management through automated systems. I have 5 automation scripts in `life-systems/scripts/` that process spending data, health metrics, Anki cards, inbox organization, and calendar audits.

I'm creating a new agent for the Life Systems domain. This agent provides **structured weekly review and life systems evaluation** — the 8 life-systems skills handle individual domain knowledge (budgeting, health tracking, learning, etc.).

## What's in This Notebook

**Notebook: "Claude Code - Life Optimization"** (49 sources)
Personal productivity, finance tracking, health habit management, learning acceleration, task prioritization, time management, weekly reviews. Sources include GTD methodology, personal finance frameworks, habit tracking research, and automation patterns.

## Your Task

Extract behavioral knowledge from this notebook and generate **1 new agent** for the Life Systems domain.

## Target Agents

### 1. NEW: life-systems-coach
**Priority**: High
**Type**: Workflow agent (read-write, needs to read CSV files and run Python analysis scripts)
**disallowedTools**: (none — needs full tool access to read data and run scripts)

**What to extract from notebooks**:
- Weekly review framework:
  - **Financial Health**: Review spending against budget categories, identify overspending patterns, track savings rate, flag unusual transactions. Key question: "Am I living within my means?"
  - **Health & Habits**: Evaluate workout consistency (streak tracking), sleep patterns, habit completion rates, trend direction (improving/declining/stable). Key question: "Am I maintaining my health commitments?"
  - **Learning Velocity**: Anki review completion, learning hours logged, skill progression milestones, topic coverage breadth vs depth. Key question: "Am I learning effectively?"
  - **Task Management**: Inbox zero status, overdue tasks, weekly task completion rate, project progress against milestones. Key question: "Am I on top of my commitments?"
  - **Time Allocation**: Calendar audit results, meeting load, deep work hours, time spent per domain (PM, creative, personal), balance assessment. Key question: "Am I spending time on what matters?"
- System health evaluation: which systems are working (sustainable, low friction) vs struggling (skipped frequently, data gaps, too complex), when to simplify vs double down
- Goal tracking: are current activities aligned with quarterly/annual goals? What's the gap between aspiration and action?
- Trend analysis: week-over-week comparisons, 4-week rolling averages, seasonal patterns
- Intervention recommendations: when to adjust a system, when to drop one, when to add friction/remove friction

**Output format requirements**:
- Weekly Review Report with date range
- Per-dimension assessment (Financial, Health, Learning, Tasks, Time)
  - Status indicator (On Track / Needs Attention / Off Track)
  - Key metric with trend arrow
  - Notable findings
  - Recommended action (if any)
- System Health scorecard (which systems are working, which need attention)
- Top 3 priorities for next week
- Reflection prompt (one question to consider)

**Trigger phrases**: "weekly review", "how am I doing", "life systems check", "review my habits", "am I on track", "analyze my spending this week", "life coach", "accountability check"

## Extraction Guidance

- This agent is a WORKFLOW agent, not a review agent. It actively reads data files, runs analysis scripts, and produces a structured report. It needs full tool access.
- Focus on the EVALUATION FRAMEWORK — how to assess whether each life dimension is healthy, what thresholds trigger "Needs Attention" vs "Off Track", what constitutes a useful recommendation.
- The weekly review should be structured enough to run consistently but flexible enough to adapt when data is missing for some dimensions.
- Include practical thresholds: e.g., "spending > 110% of category budget → Needs Attention", "missed 3+ workouts in a week → Off Track"
- The agent should be encouraging but honest — not just reporting numbers but contextualizing them.

## Cross-Domain Notes

- Pairs with `personal-finance`, `health-habits`, `learning-accelerator`, `personal-task-management`, `time-management` skills
- Uses scripts in `life-systems/scripts/`: `analyze_spending.py`, `health_audit.py`, `md_to_anki.py`, `organize_inbox.py`, `audit_calendar.py`
- Pairs with `budget-entry` skill for quick expense logging
- Pairs with `vault-curator` agent for organizing life review notes in Obsidian

## Quality Bar

The generated agent should:
- Be 100-150 lines (Rich tier)
- Have concrete evaluation dimensions with specific thresholds (not "check if things are going well")
- Include a complete weekly review output template
- Reference the 5 automation scripts and how they feed into the review
- Reference real skills from the life-systems domain

---

## PROMPT END
