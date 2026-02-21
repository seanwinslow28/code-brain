---
name: personal-task-management
description: Personal Task Management and GTD assistant. Helps prioritize tasks using a "Socratic" matrix, conducts weekly reviews, and organizes active projects. Use this skill when the user asks to "organize my tasks", "prioritize", "weekly review", or "what should I do next".
---

# Personal Task Management

## Purpose

Transforms a chaotic list of tasks into a prioritized plan. This skill uses a **Socratic Interview** pattern to force clarity on importance vs. urgency (Eisenhower Matrix) and provides a structured **Weekly Review** protocol to close open loops.

## When to Use

- **Prioritization:** When you feel overwhelmed or ask "What should I work on?"
- **Weekly Review:** Sunday night or Monday morning planning sessions.
- **Project Planning:** When breaking down a vague goal (e.g., "Plan vacation") into concrete steps.
- **Inbox Processing:** When you have a dump of random tasks that need organizing.

## Examples

**Example 1: Prioritization Session**
```
User: "I have too much to do. Help me prioritize."
Claude: [Uses personal-task-management] Let's triage. I'll read your active tasks.
First, answer these 3 questions to set the context:
1. What is the ONE absolute non-negotiable outcome for this week?
2. Are there any external deadlines (hard dates) hitting in the next 48 hours?
3. Which of these tasks is blocking other people?

User: "1. Ship the MVP. 2. The tax form is due tomorrow. 3. Reviewing the design blocks the designer."
Claude: Based on that, here is your **Priority Matrix**:

| Priority | Task | Reasoning |
| :--- | :--- | :--- |
| 🚨 **P0 (Do Now)** | Tax Form | Hard deadline < 24h. |
| 🔴 **P1 (Unlock)** | Design Review | Blocks others. |
| 🟡 **P2 (Goal)** | Ship MVP | Weekly goal, but P0/P1 take precedence today. |
| 🟢 **P3 (Defer)** | [Other tasks...] | |
```

**Example 2: Weekly Review**
```
User: "Let's do a weekly review."
Claude: [Uses personal-task-management] Starting **Weekly Review Protocol**.
Reading your calendar and task logs...

**1. Look Back (Last 7 Days)**
- Wins: Shipped v1, Paid taxes.
- Open Loop: "Email John" is still unchecked from Tuesday.

**2. Calendar Scan**
- Upcoming: Dentist on Tuesday, Team Offsite on Thursday.
- **Risk:** Thursday is blocked. You only have 3 workdays this week.

**3. Inbox Triage**
- You have 5 items in `/Inbox`. Should we process them now?
```

## Task Management Workflow

### 1. The Prioritization Matrix (P0-P3)

Do not just list tasks. ALWAYS categorize them into this matrix based on the user's constraints.

**The P-System:**
*   **P0 (Emergency):** Hard deadline < 48h OR System Down. *Must happen today.*
*   **P1 (Unlock/Blocker):** Unblocks others OR Unblocks your own P2s.
*   **P2 (Core Work):** The main goal for the week. High value, deep work.
*   **P3 (Admin/Chore):** Low energy, maintenance. Batch these.
*   **P4 (Someday):** Nice to have.

### 2. Socratic Triage (The Interview)

When the user asks "What should I do?", NEVER just guess. Run this 3-question loop:

1.  **"What is the 'Big Rock'?"** (The single most important accomplishment for the week).
2.  **"Who is waiting on you?"** (External blockers).
3.  **"What happens if you don't do this?"** (Consequence analysis: Minor annoyance vs. Catastrophe).

### 3. Weekly Review Protocol

This is a recurring ritual. Use the template in `references/weekly_review.md` to guide the user through a retrospective.

**Key Steps:**
1.  **Clear the Decks:** Process physical/digital inboxes.
2.  **Review Calendar:** Look back (what did I miss?) and look forward (what's coming?).
3.  **Check Goals:** Are my daily tasks aligned with my Quarterly Goals?

### 4. Project Breakdown (Scope Definition)

When a user adds a vague task like "Redesign website", force a breakdown using the **Definition of Done (DoD)** pattern.

> "A project is a desired result that requires more than one action step." - David Allen

**Breakdown Prompt:**
"That sounds like a project. Let's break it down:
1.  What is the very first physical action? (e.g., 'Email designer' vs 'Thinking about design')
2.  What does 'Done' look like? (screenshot? live URL?)
3.  Are there dependencies?"

## Success Criteria

- [ ] Prioritization output always uses the P0-P3 matrix.
- [ ] "What should I do" requests trigger the Socratic Interview.
- [ ] Weekly Reviews identify at least one "Risk" for the upcoming week (e.g., heavily booked days).
- [ ] Vague tasks are identified and broken down into actionable steps.

## Copy/Paste Ready

```
"Help me prioritize my list."
"Run a weekly review."
"Break down this project into next actions."
"What should I focus on today?"
```
