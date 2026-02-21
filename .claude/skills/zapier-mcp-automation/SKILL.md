---
name: zapier-mcp-automation
description: Patterns for the ~175 Zapier MCP tools available in Claude Code. Covers multi-tool workflow chains, task budget optimization, cross-app automation (Jira+Slack+Sheets+Calendar), and common recipes. Use when user says "Zapier automation", "connect apps via MCP", "Zapier workflow", "cross-app automation", or "Zapier task budget".
---

# Zapier MCP Automation

## Purpose

Master the ~175 Zapier MCP tools available to Claude Code. Build multi-step cross-app workflows, optimize Zapier task budgets, and chain tools for automation that would otherwise require manual app-switching.

## When to Use

- Building multi-app workflows (e.g., Jira ticket → Slack notification → Calendar event)
- Automating repetitive PM or admin tasks across SaaS tools
- Pulling data from one app and pushing to another
- When the user has Zapier MCP configured and wants to leverage it

## Examples

**Example 1: Sprint Kickoff Automation**
```
User: "Create a sprint kickoff workflow"
Claude: [Uses zapier-mcp-automation]
Chaining 4 Zapier MCP tools:
1. jira_software_cloud_find_issues_via_jql → Get sprint backlog
2. google_calendar_create_detailed_event → Book sprint planning
3. slack_send_channel_message → Post sprint goals to #engineering
4. google_docs_create_document_from_text → Create sprint doc

Total Zapier tasks: 8 (4 calls × 2 tasks each)
```

**Example 2: Daily Standup Summary**
```
User: "Summarize yesterday's Jira activity and post to Slack"
Claude: [Uses zapier-mcp-automation]
1. jira_software_cloud_find_issues_via_jql →
   JQL: "updated >= -1d AND project = BLOCK"
   Found 12 updated issues.
2. Synthesizing changes...
3. slack_send_channel_message → Posted to #standup:
   "Yesterday: 5 tickets closed, 3 in review, 4 in progress.
    Blockers: BLOCK-234 waiting on API access."

Total Zapier tasks: 4
```

## Tool Categories

### Communication (Slack, Gmail)

| Tool | Use Case | Tasks |
|:-----|:---------|:------|
| `slack_send_channel_message` | Post updates, summaries, alerts | 2 |
| `slack_send_direct_message` | Notify specific people | 2 |
| `slack_find_message` | Search conversation history | 2 |
| `slack_find_user_by_email` | Resolve user IDs for mentions | 2 |
| `gmail_send_email` | Send stakeholder updates | 2 |
| `gmail_find_email` | Search inbox for context | 2 |
| `gmail_create_draft` | Stage emails for review | 2 |

### Project Management (Jira)

| Tool | Use Case | Tasks |
|:-----|:---------|:------|
| `jira_software_cloud_create_issue` | Create tickets from natural language | 2 |
| `jira_software_cloud_find_issues_via_jql` | Query tickets with JQL | 2 |
| `jira_software_cloud_update_issue` | Bulk update ticket fields | 2 |
| `jira_software_cloud_add_comment_to_issue` | Add context to tickets | 2 |
| `jira_software_cloud_find_issue_by_key` | Get single ticket details | 2 |
| `jira_software_cloud_get_sprint_information` | Sprint status | 2 |

### Data & Docs (Sheets, Docs, Calendar)

| Tool | Use Case | Tasks |
|:-----|:---------|:------|
| `google_sheets_lookup_spreadsheet_row` | Read specific data | 2 |
| `google_sheets_create_spreadsheet_row` | Write data rows | 2 |
| `google_sheets_get_many_spreadsheet_rows_advanced` | Bulk read | 2 |
| `google_docs_create_document_from_text` | Generate documents | 2 |
| `google_docs_append_text_to_document` | Add to existing docs | 2 |
| `google_calendar_find_events` | Check availability | 2 |
| `google_calendar_create_detailed_event` | Book meetings | 2 |

### Analytics (GA4)

| Tool | Use Case | Tasks |
|:-----|:---------|:------|
| `google_analytics_4_run_report_for_a_property` | Pull metrics | 2 |
| `google_analytics_4_find_conversion` | Lookup conversions | 2 |

### Storage & Compute

| Tool | Use Case | Tasks |
|:-----|:---------|:------|
| `storage_by_zapier_set_value` | Persist state between runs | 2 |
| `storage_by_zapier_get_value` | Retrieve persisted state | 2 |
| `code_by_zapier_run_python` | Custom data transforms | 2 |
| `code_by_zapier_run_javascript` | Custom data transforms | 2 |

## Workflow Recipes

### Recipe 1: Ticket-to-Slack Pipeline

When a Jira ticket is created or updated, post a formatted summary to Slack.

```
1. jira_software_cloud_find_issue_by_key("BLOCK-123")
   → Get ticket details (title, status, assignee, description)
2. Format message: "🎫 BLOCK-123: [title] | Status: [status] | Assigned: [assignee]"
3. slack_send_channel_message(channel, message)
```
**Cost: 4 tasks**

### Recipe 2: Meeting Notes to Action Items

After a meeting, extract action items and create Jira tickets.

```
1. User provides meeting notes (paste or file)
2. Claude extracts action items with owners and deadlines
3. For each action item:
   jira_software_cloud_create_issue(project, summary, description, assignee)
4. slack_send_channel_message → Post summary with ticket links
```
**Cost: 2 tasks per ticket + 2 for Slack**

### Recipe 3: Weekly Metrics Report

Pull GA4 data, analyze, write to Sheets, and share.

```
1. google_analytics_4_run_report_for_a_property → Last 7 days metrics
2. Claude analyzes trends, computes week-over-week changes
3. google_sheets_create_spreadsheet_row → Append to tracking sheet
4. google_docs_create_document_from_text → Create formatted report
5. gmail_send_email → Send to stakeholders
```
**Cost: 10 tasks**

### Recipe 4: Cross-App Search

Find context across multiple tools.

```
1. slack_find_message("deployment issue") → Recent Slack discussions
2. jira_software_cloud_find_issues_via_jql("text ~ 'deployment'") → Related tickets
3. gmail_find_email("deployment") → Related emails
4. Claude synthesizes findings into a unified brief
```
**Cost: 6 tasks**

## Task Budget Optimization

Each Zapier MCP tool call consumes **2 Zapier tasks** from your plan. Optimize by:

### Batching
- Use JQL to find multiple Jira issues in one call instead of querying one at a time
- Use `get_many_spreadsheet_rows_advanced` instead of multiple single-row lookups
- Use `create_multiple_spreadsheet_rows` to write many rows at once

### Caching
- Use `storage_by_zapier` to cache frequently-accessed data (team member IDs, project keys)
- Read from cache instead of re-querying the source app

### Minimizing Round-Trips
- Gather all needed data in parallel before processing
- Only write final results (don't write intermediate data to Sheets)
- Use `code_by_zapier_run_python` for complex transforms instead of multiple tool calls

### Budget Planning

| Plan | Monthly Tasks | Effective MCP Calls |
|:-----|:-------------|:-------------------|
| Free | 100 | ~50 |
| Starter | 750 | ~375 |
| Professional | 2,000 | ~1,000 |
| Team | 50,000 | ~25,000 |

## Error Handling

Common issues and solutions:

| Error | Cause | Fix |
|:------|:------|:----|
| "Action not available" | Tool not configured in Zapier | Set up the app connection at zapier.com |
| "Rate limit exceeded" | Too many calls too fast | Add delays between calls, batch where possible |
| "Authentication failed" | OAuth token expired | Re-authenticate the app in Zapier |
| "Missing required field" | Tool parameter not provided | Check tool schema for required fields |

## Success Criteria

- [ ] Multi-tool workflows complete end-to-end
- [ ] Task budget is tracked and optimized
- [ ] Error handling for failed individual steps in a chain
- [ ] Results are formatted for human consumption (not raw JSON)
- [ ] Cross-app workflows connect 2+ services meaningfully

## Copy/Paste Ready

```
"Create a Jira ticket and notify the team on Slack"
"Pull GA4 data and write it to the tracking spreadsheet"
"Find all Jira tickets updated yesterday and summarize"
"Send a weekly metrics email using Zapier tools"
"How many Zapier tasks will this workflow cost?"
```