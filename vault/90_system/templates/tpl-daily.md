---
type: daily
date: <% tp.file.title %>
energy-peak: null
mood: null
---
# <% tp.file.title %>

## Fleet Overnight Digest
<!-- fleet-overnight -->
_Auto-filled by Daily Driver at 08:45. Do not edit manually._

## Fleet Activity Today

### Today's Fleet Snapshot
```dataview
LIST file.link
FROM "02_Areas/Agent-Fleet"
WHERE file.name = "daily-fleet-status-" + dateformat(date(today), "yyyy-MM-dd")
```

### New Knowledge (last 24h)
```dataview
LIST file.link
FROM "knowledge/concepts" OR "knowledge/connections"
WHERE file.mtime > date(today) - dur(1 day)
SORT file.mtime DESC
```

### New Research (last 24h)
```dataview
LIST file.link
FROM "20_projects/research"
WHERE file.mtime > date(today) - dur(1 day)
SORT file.mtime DESC
```

### Latest Lint Report
```dataview
LIST file.link
FROM "health"
WHERE regexmatch("\d{4}-\d{2}-\d{2}-lint-report", file.name)
SORT file.name DESC
LIMIT 1
```

## Slack Overnight
<!-- slack-overnight -->

## Meetings
<!-- meetings -->

## Morning Focus (Manual — <2 min)
> What's the ONE thing that makes today successful?

**Focus:**

## Tasks
```dataview
TASK FROM "20_projects"
WHERE status = "active" AND !completed
SORT file.name ASC
```

## Work Log
<!-- jira-log -->

## Claude Code Sessions
<!-- claude-sessions -->

## Side Project Notes
<!-- side-projects -->

## Deep Research
<!-- research-digest -->

## Evening Reflection (Manual — <2 min)
> What worked? What didn't? Carry forward?

**Win:**
**Lesson:**
**Carry forward:**
