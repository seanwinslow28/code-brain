---
type: dashboard
---
# Sean's Command Center

## Active Projects
```dataview
TABLE WITHOUT ID
  file.link AS "Project",
  status AS "Status",
  domain AS "Domain",
  ai-context AS "Current Focus"
FROM "20_projects"
WHERE status = "active"
SORT file.mtime DESC
```

## Today's Note
```dataview
LIST
FROM "10_timeline/daily"
WHERE date = date(today)
```

## This Week's Wins
```dataview
TASK
FROM "10_timeline/daily"
WHERE completed AND date >= date(today) - dur(7 days)
LIMIT 10
```

## Domain Quick Links
- [[moc-product-management|PM Work]]
- [[moc-creative-studio|Creative Studio]]
- [[moc-claude-mastery|Claude Mastery]]
- [[moc-life-systems|Life Systems]]
- [[moc-design-team|Design Team]]
- [[moc-vault|Vault Meta]]

## Blockers Across All Projects
```dataview
LIST ai-context
FROM "20_projects"
WHERE status = "blocked"
```
