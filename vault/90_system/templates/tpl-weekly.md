---
type: weekly
week: <% tp.file.title %>
date-start: <% tp.date.now("YYYY-MM-DD", 0, tp.file.title, "gggg-[W]ww") %>
date-end: <% tp.date.now("YYYY-MM-DD", 6, tp.file.title, "gggg-[W]ww") %>
---
# Weekly Review — <% tp.file.title %>

## Wins This Week
<!-- auto-wins -->

## Blockers & Open Loops
<!-- auto-blockers -->

## Claude Code Session Summary
```dataview
TABLE WITHOUT ID
  file.link AS "Day",
  length(file.tasks.completed) AS "Tasks Done"
FROM "10_timeline/daily"
WHERE date >= date(<% tp.date.now("YYYY-MM-DD", 0, tp.file.title, "gggg-[W]ww") %>) AND date <= date(<% tp.date.now("YYYY-MM-DD", 6, tp.file.title, "gggg-[W]ww") %>)
SORT date ASC
```

## Domain Progress
- **PM Work:**
- **16BitFit:**
- **Animation:**
- **Life Systems:**

## Next Week's Priorities
1.
2.
3.

## Decisions Made
<!-- auto-decisions -->
