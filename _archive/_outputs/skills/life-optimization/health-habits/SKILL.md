---
name: health-habits
description: Health and Habit tracking assistant. Logs workouts, calculates streaks from CSV data, and visualizes fitness progress. Use this skill when the user mentions "workout", "track habits", "fitness", "health data", or "did I exercise today".
---

# Health & Habit Tracking

## Purpose

Transforms a text-based logger into a quantitative health coach. Uses Python (pandas) to analyze simple CSV/Markdown logs, calculate streaks, and visualize progress, keeping the user accountable without complex app integrations.

## When to Use

- **Logging:** "Log a 5k run."
- **Analysis:** "Am I getting faster?"
- **Streak Check:** "What's my current streak?"
- **Visualization:** "Graph my weight trend."

## Examples

**Example 1: Logging & Streak Check**
```
User: "Log a chest workout: Bench 185x5, Incline 135x8. Did I keep my streak?"
Claude: [Uses health-habits] Logged to `workouts.csv`.
Running streak calculation...
**Status:** 🔥 5 Day Streak!
You haven't missed a day since Thursday.
```

**Example 2: Data Analysis**
```
User: "Graph my average heart rate for runs in April."
Claude: [Uses health-habits] Running `health_audit.py` on `workouts.csv`...
generated `plots/apr_hr_trend.png`.

**Analysis:**
- Avg HR decreased from 165 to 158 (Fitness improving).
- Fastest pace: 7:30/mi on Apr 15.
```

## Health Workflow

### 1. The "Type-Adaptive" Logger

Store data in simple, flat CSVs or Markdown tables. Do not overengineer databases.

**Standard `workouts.csv` Format:**
```csv
date,activity,duration_mins,metric_value,metric_unit,notes
2023-10-01,Running,30,3.1,miles,"Felt good"
2023-10-02,Lifting,45,185,lbs,"Bench Press max"
```

### 2. PHIA (Personal Health Insights Agent)

Do not do math in your head. Write Python code to analyze the CSV.

**Calculations to Script:**
- **Streak:** Consecutive days where data exists.
- **Volume:** Sum of duration or weight.
- **Trend:** Rolling 7-day average.

### 3. Visual Feedback (ASCII/Plot)

For quick feedback, use ASCII charts in the terminal.

```text
Steps this week:
Mon: ██████ (6k)
Tue: █████████ (9k)
Wed: ████ (4k)
```

## Success Criteria

- [ ] New logs are successfully appended to the correct CSV.
- [ ] Streak calculation correctly handles "rest days" if configured.
- [ ] Python scripts use pandas for all aggregations.
- [ ] Visualizations clearly show the trend direction.

## Copy/Paste Ready

```
"Log a workout."
"Show my habit streak."
"Graph my progress."
"Analyze my running stats."
```
