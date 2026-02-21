---
type: moc
domain: [life-systems]
---
# Life Systems

## Active Projects
```dataview
TABLE status, ai-context
FROM "20_projects"
WHERE contains(domain, "life-systems")
AND status = "active"
SORT file.mtime DESC
```

## Knowledge Base
```dataview
TABLE ai-context, source
FROM "40_knowledge"
WHERE contains(domain, "life-systems")
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
