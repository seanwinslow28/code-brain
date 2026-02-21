---
type: moc
domain: [claude-mastery]
---
# Claude Mastery

## Active Projects
```dataview
TABLE status, ai-context
FROM "20_projects"
WHERE contains(domain, "claude-mastery")
AND status = "active"
SORT file.mtime DESC
```

## Knowledge Base
```dataview
TABLE ai-context, source
FROM "40_knowledge"
WHERE contains(domain, "claude-mastery")
SORT file.mtime DESC
LIMIT 20
```

## Recent Daily Mentions
```dataview
TABLE date
FROM "10_timeline/daily"
WHERE contains(file.outlinks, this.file.link)
SORT date DESC
LIMIT 7
```
