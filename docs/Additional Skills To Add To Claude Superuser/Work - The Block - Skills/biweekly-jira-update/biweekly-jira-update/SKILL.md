---
name: biweekly-jira-update
description: Generate bi-weekly Product & Engineering status updates from The Block's Jira. Use when the user needs to create recurring status updates, compile recent work progress, or generate the bi-weekly update document summarizing completed work, in-progress items, and upcoming focus areas for Product & Engineering teams.
---

# Bi-Weekly Jira Status Update Generator

## Overview

This skill generates The Block's Product & Engineering bi-weekly status updates by querying Jira and organizing tickets into three sections: completed work (past 2 weeks), in-progress work (next few weeks), and upcoming focus (upcoming months).

## Team Scope

**Include tickets assigned to these team members:**

- Claudine Daumur
- Edvinas Rupkus
- Josh Gragg
- Koray Baspinar
- Maria Zhynko
- Marina Ardytskaya
- Martin Petkov
- Michael Elshahat
- Mike Price
- Nikita Gulis
- Nikita Orobenko
- Nikola Pivcevic
- Ramuald Vishneuski
- Serena Ho
- Aliaksandr Kryvanosau
- Ana Benitez
- Bohdan Panasenko
- Brian Mendoza
- Cesar Paz

**Projects to search:** PRO, RBS, CM (primary focus on PRO and RBS)

## Status Mappings

### Section 1: "Things we've done in the past two weeks"

**Jira Status:** Done, Closed, Completed
**Time Filter:** Updated in the last 14 days
**Criteria:** Tickets that were marked as done/completed in the past 2 weeks

### Section 2: "Things being worked on, likely to be released in the next few weeks"

**Jira Status:** In Progress, Ready for Review, Ready for Testing, In Test, Awaiting Deploy
**Manager's Definition:** "Everything that's gone through design and is with one of the Devs (or QA)"
**Criteria:** Active development work that's beyond the design phase

### Section 3: "A few of the things we're focused on for upcoming months"

**Jira Status:** To Do, Backlog
**Plus Always Include:** Tech Debt (recurring theme)
**Criteria:** Planned work that hasn't started development yet

## JQL Query Templates

### Query 1: Completed Work (Past 2 Weeks)

```jql
project IN (PRO, RBS, CM) 
AND status IN (Done, Closed, Completed) 
AND updated >= -14d
AND assignee IN (assignee1, assignee2, ...)
ORDER BY updated DESC
```

### Query 2: In-Progress Work

```jql
project IN (PRO, RBS, CM)
AND status IN ("In Progress", "Ready for Review", "Ready for Testing", "In Test", "Awaiting Deploy")
AND assignee IN (assignee1, assignee2, ...)
ORDER BY status ASC, updated DESC
```

### Query 3: Upcoming Work

```jql
project IN (PRO, RBS, CM)
AND status IN ("To Do", Backlog)
AND assignee IN (assignee1, assignee2, ...)
ORDER BY priority DESC, created DESC
```

## CRITICAL: Tool Usage Constraints

**This workflow requires EXACTLY 3 tool calls for data gathering. No more.**

### Allowed Tools:
- `Atlassian:searchJiraIssuesUsingJql` - Use 3 times ONLY

### Forbidden Tools (DO NOT USE):
- ❌ `Atlassian:search` (Rovo search)
- ❌ `Atlassian:searchConfluenceUsingCql` 
- ❌ `Atlassian:getJiraIssue` (individual ticket lookups)
- ❌ `conversation_search`
- ❌ Any Confluence tools
- ❌ Any pagination/follow-up searches

### Efficiency Rules:
1. **One query per section** - Don't break queries into multiple searches
2. **Set maxResults=100** - Get all results at once, no pagination
3. **No individual lookups** - Bulk queries only, never fetch tickets one-by-one
4. **Stop after 3 queries** - Even if results seem incomplete

### Why These Constraints:
- Prevents conversation limit exhaustion
- Ensures predictable, fast execution
- Historical updates prove 3 queries are sufficient
- Reference files provide phrasing context without additional searches

## Workflow

### Step 1: Calculate Date Range

- Current date: Use today's date
- Past 2 weeks: Today minus 14 days
- Format dates in Jira-compatible format (YYYY-MM-DD or -Nd notation)

### Step 2: Execute Searches (EXACTLY 3 QUERIES)

**CRITICAL: Run these 3 queries and STOP. Do not do any follow-up searches.**

Run three Jira searches using **ONLY** the `Atlassian:searchJiraIssuesUsingJql` tool:

**Query 1 - Completed Work:**
```jql
project IN (PRO, RBS, CM) 
AND status IN (Done, Closed, Completed) 
AND updated >= -14d
ORDER BY updated DESC
```
- Set `maxResults: 100`
- This captures ALL completed work from past 2 weeks

**Query 2 - In-Progress Work:**
```jql
project IN (PRO, RBS, CM)
AND status IN ("In Progress", "Ready for Review", "Ready for Testing", "In Test", "Awaiting Deploy")
ORDER BY status ASC, updated DESC
```
- Set `maxResults: 100`
- This captures ALL active development work

**Query 3 - Upcoming Work:**
```jql
project IN (PRO, RBS, CM)
AND status IN ("To Do", Backlog)
ORDER BY priority DESC, created DESC
```
- Set `maxResults: 100`
- This captures ALL planned work

**After these 3 queries, proceed directly to Step 3. DO NOT:**
- Search Confluence
- Use Rovo search
- Look up individual tickets
- Paginate for more results
- Search for missing information

**If results seem incomplete:** Use the reference files (historical-updates.md, team-roles.md) to fill gaps, don't search more.

### Step 3: Categorize and Format Results

**Formatting Rules:**

1. **Product/Area Prefix:** Start each bullet with:
   - `.Co` - Main website (theblock.co)
   - `Campus` - Education platform
   - `SFMC` - Salesforce Marketing Cloud
   - `Ad Server` / `GAM` - Google Ad Manager
   - `Crypto IQ` - Competition/quiz feature
   - `Analytics` / `Looker` - Data/analytics work
   - `Wordpress` / `SEO` - CMS/SEO work
   - `Sendgrid` - Email infrastructure
   - `Ratings Pages` / `Indices` / `Charts` - Data features

2. **Context Tags:** Add inline status when relevant:
   - "in test" (for Ready for Testing, In Test)
   - "in test" (for Ready for Review - awaiting review)
   - "awaiting deploy" (for Awaiting Deploy)

3. **Consolidation:** Combine related tickets into single bullets:
   - Multiple tickets about same feature → One bullet describing the feature
   - Example: "PRO-1234: GAM setup" + "PRO-1235: GAM testing" → ".Co - GAM Ad support"

4. **Specificity Balance:**
   - Be specific enough to understand the work
   - Not so detailed that it's cluttered
   - Focus on user/business impact, not technical implementation details

### Step 4: Structure the Output

Format the final update using exactly this structure:

```
[Date in format: Month DD, YYYY]

Things we've done in the past two weeks:
● [Product] - [Accomplishment]
● [Product] - [Accomplishment]
● .Co & Campus - Visual bugs, UX improvements, SEO fixes

Things being worked on, likely to be released in the next few weeks:
● [Product] - [Feature], in test
● [Product] - [Feature], awaiting deploy
● [Product] - [Feature]
● Chart improvements & bug fixes

A few of the things we're focused on for upcoming months:
● [Initiative]
● [Initiative]
● Multi-language support on .co
● Tech Debt
```

**Section-Specific Guidelines:**

**Section 1 (Completed):**
- Focus on shipped features and completed initiatives
- Always include catch-all: ".Co & Campus - Visual bugs, UX improvements, SEO fixes"
- Highlight major launches or milestones

**Section 2 (In Progress):**
- Include status tags (in test, awaiting deploy) when known
- Group related work items together
- Always include catch-all: "Chart improvements & bug fixes"
- This is typically the longest section (10-15 items)

**Section 3 (Upcoming):**
- Higher-level initiatives, not individual tickets
- Strategic/roadmap items
- Always include: "Tech Debt" as the last item
- Usually 3-5 items total

## Common Patterns from Historical Updates

**Recurring Items (appear frequently):**
- Nuxt 3/4 migration → GAM Ad support
- Multi-course support, CMI-5
- Tech Debt (always in upcoming months)
- Chart improvements & bug fixes (always in being worked on)
- Visual bugs, UX improvements (always in completed)
- Additional Indices
- Job Boards
- Sponsored Courses

**Project-Specific Patterns:**
- `.Co` items often relate to: articles, homepage, data features, SEO, ads
- `Campus` items often relate to: courses, marketing site, checkout, performance
- `SFMC` items often relate to: Marketo migration, email campaigns, forms

## Quality Checks

Before finalizing the update:

1. **Verify all three sections are populated** - Each section should have at least 3-4 items
2. **Check for duplicates** - Same work shouldn't appear in multiple sections
3. **Validate team scope** - Only include work from the defined team members
4. **Review formatting** - Bullets start with product prefix, proper grammar
5. **Include recurring items** - Tech Debt in section 3, bug fixes in section 2
6. **Date accuracy** - Section 1 only includes work from past 14 days

## Example Output

```
Dec 12, 2025

Things we've done in the past two weeks:
● .Co - Fully migrated all article pages from Nuxt2 to Nuxt4 (close monitor for performance)
● Crypto IQ - Week 1 is completed and was a success. Final 4 next Wed (or Thurs)
● .Co - Data chart Request Data CTA
● .Co & Campus - Visual bugs, UX improvements, SEO fixes

Things being worked on, likely to be released in the next few weeks:
● LMAX Navigator Page - LMAX Company-specific page, in test
● .Co - Advertise With Us refreshed experience, in test
● .Co - A/B Test for Ratings recirculation components in articles, in test
● .Co - Nuxt 4 rewrite/migration, most pages in test → GAM Ad support
● .Co - Replacing Sticky Footer With GAM Ad Unit (adding color changing setting in the meantime)
● .Co - 'Layer One' Podcast & Newsletter
● Campus - Marketing Site Stripe Checkout flows
● Campus - Multi-course support, CMI-5
● Ad Server - New ad hosting experience on .Co awaiting deploy
● .Co - Job boards
● SFMC - migration of Marketo forms
● Additional Indices
● Chart improvements & bug fixes

A few of the things we're focused on for upcoming months:
● .Co - 'Sponsored Courses' funnel into Campus
● Campus - Prerequisite Schema & Knowledge Token Taxonomy
● Multi-language support on .co
● Tech Debt
```

## Reference Files

This skill includes two reference files to help with consistency and context:

### `references/historical-updates.md`

Contains 10 past bi-weekly updates (Jul 2025 - Dec 2025) showing exact phrasing, formatting, and patterns.

**When to use:**
- When uncertain how to phrase a complex feature
- To understand which items typically get consolidated
- To see progression of long-running initiatives (e.g., Nuxt migration, Multi-course support)
- When deciding level of detail for bullets

**Example use case:** If you see tickets about "GAM" but aren't sure how to describe them, search the historical updates to see: ".Co - Nuxt 4 rewrite/migration → GAM Ad support"

### `references/team-roles.md`

Lists all 17 team members with their roles and specialties.

**When to use:**
- To understand who works on what types of features
- When consolidating related tickets by team ownership
- To identify if a ticket belongs to Product, Engineering, Design, or QA

**Example use case:** Multiple tickets assigned to Marina Ardytskaya about GAM → These likely belong together in one bullet about GAM work

## Important Notes

- **CRITICAL: Exactly 3 Tool Calls** - Run the 3 JQL queries and STOP. Do not search Confluence, use Rovo, or look up individual tickets
- **Manager Guidance:** Section 2 should only include "everything that's gone through design and is with one of the Devs (or QA)"
- **Don't Over-Search:** If information seems missing after 3 queries, use reference files to fill gaps - never do additional searches
- **Consistency:** Follow the established patterns from historical updates
- **Brevity:** Keep bullets concise - one line per item when possible
- **Focus:** Emphasize product/user impact over technical implementation details
- **Use References Strategically:** When phrasing is unclear or you need context about team ownership, read the relevant reference file
- **Incomplete Results Are OK:** Historical updates show this process works with just 3 queries - trust the process
