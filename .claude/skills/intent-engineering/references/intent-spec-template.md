# Unified Intent Spec Template

Use this YAML template when defining any new agent or skill. Each field includes
an inline comment explaining its purpose and where it should live in the codebase.

---

## Blank Template

```yaml
# ==========================================
# UNIFIED INTENT SPECIFICATION
# ==========================================
# Agent/Skill Name: [NAME]
# Date: [YYYY-MM-DD]
# Author: [NAME]

# 1. OBJECTIVE (Location: SKILL.md — top of file)
# The primary mission. Include trade-off guidance for ambiguous situations.
objective: >
  [What problem are you solving, for whom, and why it matters.]
  [When facing trade-offs, prioritize X over Y.]

# 2. USER GOAL (Location: SKILL.md)
# The job-to-be-done from the USER's perspective, not the agent's.
user_goal: >
  [The user wants to JOB so they can END_STATE.]
  [They currently struggle with FRICTION.]

# 3. DESIRED OUTCOMES (Location: SKILL.md)
# 2-4 observable, measurable STATES (not activities).
# Test: "After the agent runs, [STATE] exists."
desired_outcomes:
  - "[Observable state change 1]"
  - "[Observable state change 2]"
  - "[Observable state change 3]"

# 4. HEALTH METRICS (Location: SKILL.md)
# What must NOT degrade while pursuing outcomes. Prevents Goodhart's Law.
# For each outcome, ask: "How could the agent achieve this in a way I'd hate?"
health_metrics:
  - metric: "[What to protect]"
    threshold: "[above/below THRESHOLD]"
    if_trending_wrong: "[Behavioral adjustment]"

# 5. STRATEGIC CONTEXT (Location: SKILL.md)
# Where this agent fits in the larger system.
strategic_context:
  system_role: "[Part of X pipeline, runs after Y]"
  upstream: "[What feeds into this agent]"
  downstream: "[Who consumes this agent's output]"
  business_context: "[Relevant strategy or constraints]"

# 6. CONSTRAINTS (Location: SKILL.md for steering, Hooks/config.toml for hard)
# Steering: influence reasoning (live in the prompt)
steering_constraints:
  - "[Prefer A over B when CONDITION]"
  - "[When uncertain, DEFAULT_BEHAVIOR]"
# Hard: enforce compliance (live in architecture — NOT in the prompt)
hard_constraints:
  - constraint: "[Never FORBIDDEN_ACTION]"
    enforced_via: "[disallowedTools / PreToolUse hook exit code 2 / config.toml]"
  - constraint: "[Rate limited to N per TIME]"
    enforced_via: "[config.toml max_turns / max_budget_usd]"

# 7. DECISION AUTHORITY (Location: SKILL.md & config.toml)
# Map each decision type to an autonomy level.
# Levels: full-autonomous | guarded-autonomous | proposal-first | human-required
decision_authority:
  full_autonomous:
    - decision: "[Low-risk, reversible action]"
      why: "[Why this is safe to automate]"
  guarded_autonomous:
    - decision: "[Medium-risk action]"
      rollback: "[How to undo if wrong]"
  proposal_first:
    - decision: "[High-impact action]"
      approval_from: "[Who must approve]"
  human_required:
    - decision: "[Irreversible or sensitive action]"
      why: "[Why human must execute]"

# 8. EDGE CASES (Location: SKILL.md)
# Every unhandled edge case is a potential hallucination point.
edge_cases:
  - when: "[Unusual condition]"
    behavior: "[Expected behavior]"
  - when: "[System failure / API down]"
    behavior: "[Fallback behavior]"
  - when: "[Conflicting requirements]"
    behavior: "[Priority order]"

# 9. STOP RULES & VERIFICATION (Location: SKILL.md & agents-sdk preamble)
stop_rules:
  halt_when:
    - "[Critical condition] → [Action: halt, alert, rollback]"
  escalate_when:
    - "[Confidence below THRESHOLD]"
    - "[N consecutive failures]"
  complete_when:
    - "[Completion criteria 1]"
    - "[All verification checks pass]"

verification:
  - check: "[Automated validation]"
    validates: "[What it proves]"
  - check: "[Manual review]"
    validates: "[What human checks]"

# EXECUTION LIMITS (Location: config.toml)
execution_limits:
  max_turns: 0       # Set per agent/mode in config.toml
  max_budget_usd: 0  # Set per agent/mode in config.toml
```

---

## Completed Example: Autonomous Daily Driver Agent

This applies the template to the `daily_driver.py` agent — a high-risk autonomous
agent that runs via macOS launchd while the user sleeps.

```yaml
# ==========================================
# INTENT SPEC: AUTONOMOUS DAILY DRIVER
# ==========================================
# Agent: agents-sdk/agents/daily_driver.py
# Skills: daily-driver, vault-read-write
# Schedule: morning 6:00 AM, evening 5:00 PM, weekly Friday 4:00 PM
# Date: 2026-02-28

# 1. OBJECTIVE
objective: >
  Synthesize yesterday's open tasks and today's calendar events into a
  prioritized daily plan, so Sean starts each day knowing exactly what to
  focus on. Trade-off: Prioritize accurately capturing all hard-scheduled
  meetings over creatively brainstorming new tasks.

# 2. USER GOAL
user_goal: >
  Sean wants to start each morning with a clear daily plan and end each
  day with a concise reflection — without spending time manually reviewing
  notes and calendars. He struggles with carry-forward items falling through
  the cracks between days.

# 3. DESIRED OUTCOMES
desired_outcomes:
  - "A daily note exists at vault/10_timeline/daily/YYYY-MM-DD.md for the current date"
  - "The note contains a 1-3-5 priority plan (1 big, 3 medium, 5 small)"
  - "Calendar events from both sean.winslow28@gmail.com and swinslow@theblock.co are included"
  - "Carry-forward items from yesterday's note are captured"

# 4. HEALTH METRICS
health_metrics:
  - metric: "Data Non-Destruction"
    threshold: "Zero existing content overwritten"
    if_trending_wrong: "Switch to PATCH-only operations at anchors"
  - metric: "Truth Anchoring"
    threshold: "Zero hallucinated calendar events or task completions"
    if_trending_wrong: "If source unavailable, note gap explicitly with [ERROR] tag"
  - metric: "Content Integrity"
    threshold: "All frontmatter remains valid YAML after agent writes"
    if_trending_wrong: "If frontmatter unparseable, do NOT modify — log error and skip"

# 5. STRATEGIC CONTEXT
strategic_context:
  system_role: "First agent in daily workflow; output feeds evening review and weekly aggregation"
  upstream: "Yesterday's daily note, Google Calendar events, active project notes in vault/20_projects/"
  downstream: "Evening mode reads morning output; weekly mode aggregates 7 daily notes"
  business_context: "Part of personal productivity system. Low external impact but high personal value."

# 6. CONSTRAINTS
steering_constraints:
  - "Keep the daily briefing concise — under 2 minutes to read"
  - "When priorities conflict, use the 1-3-5 framework: 1 must-do, 3 should-do, 5 could-do"
  - "Prefer carry-forward items over new brainstormed tasks"
hard_constraints:
  - constraint: "No Bash execution"
    enforced_via: "allowed_tools whitelist in build_options() — Bash not included"
  - constraint: "Cannot modify .env or credentials"
    enforced_via: "block-secrets.py PreToolUse hook (exit code 2)"
  - constraint: "Budget capped per run"
    enforced_via: "config.toml [agents.daily_driver.modes.morning] max_budget_usd = 0.25"

# 7. DECISION AUTHORITY
decision_authority:
  full_autonomous:
    - decision: "Create today's daily note from template"
      why: "Reversible, low blast radius, well-understood"
    - decision: "Write 1-3-5 priority plan"
      why: "Additive operation, no destructive risk"
    - decision: "Extract carry-forwards from yesterday"
      why: "Read-only operation on existing note"
  guarded_autonomous:
    - decision: "Inject content at <!-- claude-sessions --> anchor"
      rollback: "Content appended below anchor; can be manually removed"
  human_required:
    - decision: "Delete or restructure existing vault notes"
      why: "Irreversible data loss; must never happen autonomously"

# 8. EDGE CASES
edge_cases:
  - when: "Yesterday's daily note doesn't exist"
    behavior: "Note the absence, proceed without carry-forwards"
  - when: "Today's daily note already exists (manual or earlier run)"
    behavior: "Read existing note, only append NEW content at anchors — never overwrite"
  - when: "Google Calendar MCP fails to connect"
    behavior: "Create note with empty Schedule section, append [ERROR: CALENDAR SYNC FAILED]"
  - when: "Template file tpl-daily.md is missing"
    behavior: "Create a minimal daily note with standard headings and anchors"
  - when: "Frontmatter of yesterday's note is corrupted/unparseable"
    behavior: "Log error, skip frontmatter extraction, use note body text only"
  - when: "Agent hits max_turns limit mid-task"
    behavior: "Save whatever progress has been made, log partial completion"

# 9. STOP RULES & VERIFICATION
stop_rules:
  halt_when:
    - "ZERO-INTERACTION MANDATE: Never ask clarifying questions. Running at 6:00 AM via launchd — no human available. Any prompt for input causes silent timeout hang."
    - "Safe Deferral: If file operations fail twice, create error note at <!-- agent-error --> anchor and halt"
  escalate_when:
    - "N/A — no escalation path in autonomous mode. Errors are logged for post-hoc review."
  complete_when:
    - "Daily note exists with frontmatter, 1-3-5 plan, and schedule section"
    - "Run logged to agent-run-history.csv with status and cost"

verification:
  - check: "Daily note file exists at expected path"
    validates: "Note was created successfully"
  - check: "Note contains ## Morning Focus heading"
    validates: "Template was applied correctly"
  - check: "agent-run-history.csv has new row with status != error"
    validates: "Agent completed without fatal errors"
  - check: "Cost in CSV is under max_budget_usd"
    validates: "Budget constraints were respected"

# EXECUTION LIMITS (config.toml)
execution_limits:
  morning:
    max_turns: 15
    max_budget_usd: 0.25
  evening:
    max_turns: 10
    max_budget_usd: 0.25
  weekly:
    max_turns: 20
    max_budget_usd: 0.50
```
