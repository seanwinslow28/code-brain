---
name: jira-automation
description: Jira automation assistant for Claude Code. Creates tickets from natural language, runs bulk operations, manages sprints, and executes JQL queries via MCP. Use when asked to create Jira tickets, update Jira, bulk create issues, run JQL queries, manage sprints, or work with Jira templates.
---

# Jira Automation

## Purpose

Automate Jira workflows directly from Claude Code using MCP server integration. Handle ticket creation, bulk operations, sprint management, and JQL queries without leaving the terminal. Guide the user through natural language to structured Jira API calls.

## When to Use

- User asks to create a Jira ticket, bug report, feature request, tech debt item, or spike
- User wants to bulk create or update multiple tickets
- User needs to run JQL queries to find or filter issues
- User asks about sprint planning, grooming, or sprint management
- User wants to link tickets or manage dependencies
- User needs a Jira ticket template applied

## Examples

**Example 1: Create a bug ticket**
```
User: "Create a Jira bug for the login page 500 error we found today"
Claude: [Uses jira-automation] Before creating the ticket, let me gather key details:

1. What project key? (e.g., PROJ)
2. Can you paste the error message or stack trace?
3. What environment? (Production/Staging/Dev)
4. Priority? (High/Medium/Low)

[After answers, creates structured bug report via MCP with reproduction steps,
expected/actual behavior, and environment details]
```

**Example 2: Bulk ticket creation from epic**
```
User: "Break down epic PROJ-100 into implementation tickets for the new payment flow"
Claude: [Uses jira-automation] I'll decompose this into individual stories:

1. PROJ-101: [Implementation] Payment gateway integration
2. PROJ-102: [Implementation] Checkout form validation
3. PROJ-103: [Design] Payment confirmation screen
4. PROJ-104: [Implementation] Error handling and retry logic

Creating all 4 tickets linked to PROJ-100...
[Creates tickets via MCP with descriptions, acceptance criteria, and epic links]
```

**Example 3: Sprint health check via JQL**
```
User: "Show me stale tickets in the current sprint"
Claude: [Uses jira-automation] Running JQL query:
sprint in openSprints() AND status != Done AND updated < -7d

Found 3 stale issues:
| Key | Summary | Assignee | Last Updated |
|-----|---------|----------|-------------|
| PROJ-45 | API rate limiting | @dev1 | 12 days ago |
...
```

## MCP Server Setup

Two approaches for connecting Claude Code to Jira:

### Option A: Atlassian Rovo MCP (Cloud)

Best for Jira Cloud with OAuth-based access:

```bash
claude mcp add atlassian --transport sse https://mcp.atlassian.com/v1/mcp
```

This triggers browser-based OAuth 2.1 authorization. Permissions inherit from the authenticated user's Jira roles.

### Option B: Self-Hosted MCP (Node.js)

Best for Jira Data Center or when needing custom field control:

```json
{
  "mcpServers": {
    "jira": {
      "command": "node",
      "args": ["/path/to/mcp-jira-server/dist/index.js"],
      "env": {
        "JIRA_HOST": "https://your-company.atlassian.net",
        "JIRA_EMAIL": "your-email@company.com",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}",
        "JIRA_DEFAULT_PROJECT": "PROJ"
      }
    }
  }
}
```

Never hardcode API tokens. Use environment variables or the secure MCP configuration.

## Ticket Creation Workflow

### Step 1: Identify ticket type

| Type | Prefix Convention | Required Fields |
|------|-------------------|-----------------|
| Bug | None | Repro steps, expected/actual, environment |
| Feature | [Feature] | User story, acceptance criteria, success metrics |
| Tech Debt | [Tech Debt] | Current state, proposed change, risk if deferred |
| Spike | [Spike] | Question to answer, timebox, deliverable |
| Design | [Design] | User flow, mockup links, design criteria |
| Implementation | [Implementation] | Technical approach, dependencies, test plan |

### Step 2: Apply template

**Bug Report Template:**
```markdown
**Environment**: Production / Staging / Dev
**Component**: [Detected from error or user input]
**Browser/Device**: [If applicable]

**Reproduction Steps**:
1. [Step 1]
2. [Step 2]

**Expected**: [Expected behavior]
**Actual**: [Error message or observed behavior]

**Root Cause Analysis**:
[Summary if known, otherwise "Investigation needed"]

**Logs/Screenshots**:
[Attach relevant data]
```

**Feature Request Template:**
```markdown
**User Story**: As a [persona], I want [action] so that [outcome].

**Acceptance Criteria**:
- [ ] Criterion 1 (testable)
- [ ] Criterion 2 (testable)

**Out of Scope**: [Explicit exclusions]

**Success Metric**: [Measurable KPI]

**Technical Notes**: [Dependencies, constraints, API changes]
```

### Step 3: Create via MCP

Map natural language to the `create_issue` tool call:

```json
{
  "name": "create_issue",
  "arguments": {
    "projectKey": "PROJ",
    "summary": "Fix login 500 error on /auth/login",
    "description": "[Filled template from above]",
    "issueType": "Bug",
    "priority": "High",
    "labels": ["production-incident"],
    "assignee": "currentUser()"
  }
}
```

## Bulk Operations

For batch ticket creation, follow this sequence to avoid rate limits:

1. Verify the parent Epic exists via `get_issue`
2. Execute `create_issue` for each item (pause 2 seconds between calls if >20 items)
3. Execute `link_issues` to associate with the Epic
4. Confirm all tickets with a summary table

For batch updates (e.g., commenting on stale tickets):

1. Run a JQL search to get the issue list
2. Iterate through results applying the update
3. Report what was changed

## JQL Query Patterns

For the complete JQL reference with crypto/fintech-specific queries, see `references/jql-patterns.md`.

Common queries for a technical PM:

| Goal | JQL |
|------|-----|
| Stale issues | `project = PROJ AND status not in (Done, Closed) AND updated < -14d` |
| Sprint blockers | `sprint in openSprints() AND priority = High AND flag = Impeded` |
| Unassigned work | `project = PROJ AND sprint in openSprints() AND assignee is EMPTY` |
| Scope creep | `sprint in openSprints() AND created > startOfDay("-5d")` |
| Epic progress | `parent = EPIC-123 AND status != Done` |
| My open items | `assignee = currentUser() AND status != Done ORDER BY priority DESC` |

## Sprint Management Commands

| Action | Tool Pattern |
|--------|-------------|
| List sprints | `get_sprints(board_id)` |
| Create sprint | `create_sprint(name, startDate, endDate)` |
| Move to sprint | `move_issue_to_sprint(issueKey, sprintId)` |
| Sprint report | JQL: `sprint = [sprintId] AND status = Done` vs total |

## Field Mapping

Jira instances use custom field IDs. Identify yours with `get-fields` or `diagnose-fields`, then configure:

```env
JIRA_FIELD_STORY_POINTS=customfield_10023
JIRA_FIELD_ACCEPTANCE_CRITERIA=customfield_10050
JIRA_FIELD_EPIC_LINK=customfield_10008
```

When mapped, the MCP server translates `storyPoints: 5` to `customfield_10023: 5` automatically.

## Linking Tickets

Model dependencies using `link_issues`:

| Link Type | Meaning |
|-----------|---------|
| Blocks | Issue A prevents work on Issue B |
| is blocked by | Inverse of Blocks |
| relates to | General relationship |
| is cloned by | Duplicate tracking |

## Success Criteria

- [ ] Tickets created with all required fields populated
- [ ] Bulk operations complete without rate limit errors
- [ ] JQL queries return expected results
- [ ] All tickets linked to correct epics and sprints
- [ ] Templates applied consistently across ticket types
- [ ] No API tokens exposed in prompts or CLAUDE.md

## Copy/Paste Ready

```
"Create a Jira bug for [describe the issue]"
"Bulk create tickets for epic PROJ-100"
"Run a JQL query to find stale tickets in the current sprint"
"Create a feature request ticket for [feature name]"
"Move these tickets to Sprint 24"
"Show me unassigned work in the current sprint"
```
