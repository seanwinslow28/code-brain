---
name: health-habits
description: Health and Habit tracking assistant. Logs workouts, calculates streaks from CSV data, runs XP/level-up gamification, and visualizes fitness progress in the Obsidian vault. Use this skill when the user mentions "workout", "track habits", "fitness", "health data", "gym", "streak", "XP", "level up", "log exercise", "did I work out", "supplement", or "meal plan".
---

# Health & Habit Tracking

## Purpose

Sean's personal fitness tracker and gamification engine. Logs workouts to the Obsidian vault, calculates streaks, awards XP, tracks level-ups, and visualizes progress — all built around his actual PPL split, supplement stack, and meal patterns. Uses Python (pandas) for analysis and Apple Shortcuts for automated data ingestion from Apple Fitness.

## When to Use

- **Logging:** "Log today's push workout" / "Log a pull session"
- **Streaks:** "What's my current streak?" / "Did I break my streak?"
- **XP/Levels:** "What level am I?" / "How much XP this week?"
- **Analysis:** "Graph my workout frequency this month"
- **Nutrition:** "Log today's meals" / "Show my supplement schedule"
- **Planning:** "What's tomorrow's split?" / "What should I focus on today?"

## Sean's Actual Routine

### Weekly Split (PPL)

| Day | Focus | Style |
|-----|-------|-------|
| Monday | Push | Chest, shoulders, triceps |
| Tuesday | Pull (Arm Focus) | Back, biceps — emphasis on arms |
| Wednesday | Legs / Abs | Quads, hams, glutes, core |
| Thursday | Push | Chest, shoulders, triceps |
| Friday | Pull (Back Focus) | Back, biceps — emphasis on back |
| Saturday | Active Recovery | Treadmill walking + abs |
| Sunday | Active Recovery | Treadmill walking or outdoor activity |

### Training Style

- **Sets:** 3-4 per exercise, to failure (no rep counting)
- **Equipment rotation:** Free weights, calisthenics, machines, smith machine — mixed for variety
- **Philosophy:** Go by feel. No rigid program. Self-motivated. Progressive overload and mind/muscle connection.
- **Schedule:** 4:45 AM wake → coffee → 5:15-6:30 AM gym (60-70 min)
- **No injuries or limitations**

### Meal Patterns (Daily Defaults)

**Breakfast:**
- Eggs with spinach
- Greek yogurt bowl (berries, oats, nuts)

**Lunch:**
- Veggies, protein, healthy carbs

**Dinner:**
- Protein (chicken, turkey, ground turkey, fish, occasional red meat)
- Spinach
- Fruit bowl
- Protein yogurt bowl (protein powder, nuts, dates)

**Desserts:** Healthy versions — swap high-cal ingredients for high protein, healthy fats, monk fruit sweetener/honey/maple syrup.

**Philosophy:** Natural, healthy, whole food ingredients in most meals. No calorie/macro obsession (stopped tracking years ago — it became too stressful). Protein stays high intuitively.

### Supplement Stack

| Supplement | Timing |
|------------|--------|
| Green plant powders | Morning |
| Creatine | Daily |
| Protein powder | Post-workout + dinner yogurt bowl |
| Seed (gut health) | Daily |
| Zinc | Daily |
| Vitamin D | Daily |
| Melatonin | Evening |
| Mushroom powders | Daily |
| Maca | Daily |
| Ashwagandha | Daily |

## Examples

**Example 1: Quick Workout Log**
```
User: "Log today's push workout — felt strong, went heavy on bench"
Claude: [Uses health-habits] Logged to vault.

Push Day — Monday, Feb 17
   Style: Heavy bench focus
   Duration: ~65 min (from Apple Fitness)
   Calories: ~480 (from Apple Fitness)

Streak: 12 days!
+100 XP (workout) +25 XP (streak bonus)
Level 7 — 425/500 XP to Level 8

Updated: vault/Areas/Health/workout-log.csv
Updated: vault/Areas/Health/daily-note habit checkbox
```

**Example 2: Weekly Progress**
```
User: "Show my week"
Claude: [Uses health-habits]

Week of Feb 10-16:
Mon: ########## Push      (+100 XP)
Tue: ########## Pull/Arms (+100 XP)
Wed: ########## Legs/Abs  (+100 XP)
Thu: ########## Push      (+100 XP)
Fri: ########## Pull/Back (+100 XP)
Sat: ######     Treadmill  (+50 XP)
Sun: ######     Outdoor    (+50 XP)

Weekly Total: 600 XP | Streak: 14 days
Level 7 [========--] 75% -> Level 8
```

**Example 3: Split Check**
```
User: "What's today?"
Claude: It's Wednesday — Legs/Abs day.
Focus: Quads, hams, glutes, core.
Mix it up between free weights, machines, and bodyweight.
Current streak: 10 days
```

## Core Workflows

### 1. Workout Logging

Store data in a flat CSV in the Obsidian vault at `vault/Areas/Health/workout-log.csv`:

```csv
date,day,split,style,duration_mins,calories_burned,notes,xp_earned
2026-02-17,Monday,Push,Heavy bench focus,65,480,"Felt strong",100
2026-02-18,Tuesday,Pull-Arms,Arm emphasis,62,445,"Good pump",100
```

**Logging rules:**
- Always record date, day, and split type
- Duration and calories come from Apple Fitness data when available
- Notes are optional — capture feel/highlights
- XP is auto-calculated (see gamification section)

### 2. Apple Fitness Integration

Claude Code cannot connect directly to Apple Health. Use this pipeline:

**Setup (one-time):**
1. Create an Apple Shortcut called "Export Workout"
2. Shortcut actions: Get Latest Workout -> extract date, duration, calories, workout type -> Append to CSV file in iCloud/Obsidian vault folder
3. Trigger: Run after each workout, or automate via "When Workout Ends" trigger

**CSV output from Shortcut:**
```csv
date,duration_mins,calories_burned,workout_type
2026-02-17,65,480,Traditional Strength Training
```

**Claude Code reads this CSV** and merges it with the manual workout log for complete tracking.

### 3. Gamification Engine (XP + Levels)

**XP Awards:**

| Action | XP |
|--------|-----|
| Full workout (Push/Pull/Legs) | 100 |
| Active recovery (Sat/Sun) | 50 |
| 7-day streak bonus | 200 |
| 30-day streak bonus | 1000 |
| Personal best noted | 150 |
| Workout logged with Apple data | +25 bonus |

**Level Thresholds:**

| Level | Total XP | Title |
|-------|----------|-------|
| 1 | 0 | Recruit |
| 2 | 300 | Regular |
| 3 | 700 | Warrior |
| 4 | 1,200 | Veteran |
| 5 | 2,000 | Elite |
| 6 | 3,000 | Champion |
| 7 | 4,500 | Legend |
| 8 | 6,500 | Titan |
| 9 | 9,000 | Mythic |
| 10 | 12,000 | Immortal |

**Streak rules:**
- A "day" counts if any workout or active recovery is logged
- Rest days don't break streaks IF they follow 6 consecutive workout days (1 earned rest day per week)
- Streak resets after 2+ consecutive days with no log entry

### 4. Vault Integration

**Daily note habit checkbox** — append to the daily note in `vault/Daily/`:
```markdown
## Habits
- [x] Workout: Push Day (+100 XP)
- [x] Supplements taken
- [ ] Meals logged
```

**Weekly summary** — generate in `vault/Areas/Health/weekly/`:
```markdown
# Week of Feb 10-16, 2026

## Workouts: 7/7
| Day | Split | Duration | Calories | XP |
|-----|-------|----------|----------|----|
| Mon | Push | 65m | 480 | 100 |
...

## Stats
- **Streak:** 14 days
- **Weekly XP:** 600
- **Level:** 7 (Legend) — 425/500 to Level 8
- **Total XP:** 4,925

## Notes
- Heavy bench felt strong Monday
- Good pull session Friday
```

### 5. Analysis Scripts

Use Python (pandas) for all calculations. Never estimate in your head.

```python
import pandas as pd

def calculate_streak(df: pd.DataFrame) -> int:
    """Calculate consecutive workout days from most recent date backward."""
    df['date'] = pd.to_datetime(df['date'])
    dates = df['date'].dt.date.unique()
    dates = sorted(dates, reverse=True)

    streak = 0
    for i, date in enumerate(dates):
        if i == 0:
            streak = 1
            continue
        diff = (dates[i-1] - date).days
        if diff <= 1:
            streak += 1
        elif diff == 2 and streak >= 6:
            streak += 1  # Allow 1 earned rest day per week
        else:
            break
    return streak

def weekly_xp(df: pd.DataFrame, week_start: str) -> dict:
    """Calculate XP for a given week."""
    df['date'] = pd.to_datetime(df['date'])
    start = pd.to_datetime(week_start)
    end = start + pd.Timedelta(days=6)
    week = df[(df['date'] >= start) & (df['date'] <= end)]
    return {
        'total_xp': week['xp_earned'].sum(),
        'workouts': len(week),
        'streak': calculate_streak(df[df['date'] <= end])
    }
```

### 6. ASCII Progress Display

For terminal feedback:
```text
Level 7: Legend
[================----] 75% -> Level 8
XP: 4,925 / 6,500 | Streak: 14

This Week:
Mon: ########## Push       [done]
Tue: ########## Pull/Arms  [done]
Wed: ########## Legs/Abs   [done]
Thu: __________ Push       (today)
Fri: __________ Pull/Back
Sat: __________ Treadmill
Sun: __________ Rest/Walk
```

## Success Criteria

- [ ] Workouts logged to `vault/Areas/Health/workout-log.csv` with correct split type
- [ ] XP calculated correctly per the awards table
- [ ] Level displayed matches cumulative XP thresholds
- [ ] Streak handles earned rest days (1 per week after 6 consecutive days)
- [ ] Daily note in vault updated with habit checkbox
- [ ] Weekly summary generated with stats table
- [ ] Apple Shortcuts pipeline documented for data ingestion
- [ ] Python scripts use pandas for all aggregations
- [ ] ASCII progress bar renders correctly in terminal

## Copy/Paste Ready

```
"Log today's workout"
"What's my streak?"
"What level am I?"
"Show my week"
"What's today's split?"
"Graph my workout frequency this month"
"Generate weekly health summary"
"What's my XP progress?"
```