---
name: pm-jira
description: Creates and manages Jira tickets with proper formatting, acceptance criteria, and linking
---

# PM Jira Skill

## When to Use

Use this skill when:
- Creating new Jira tickets
- Writing user stories and acceptance criteria
- Updating ticket descriptions
- Linking related tickets
- Preparing sprint planning materials

## Examples

**Example 1: Creating a user story**
```
User: "Create a Jira ticket for the login feature"
Claude: [Uses pm-jira skill] Creating user story ticket:

**Title:** As a user, I want to log in with email and password

**Description:**
Users need a secure way to authenticate and access their accounts.

**Acceptance Criteria:**
- [ ] User can enter email and password
- [ ] System validates credentials
- [ ] Error messages display for invalid login
- [ ] Successful login redirects to dashboard
- [ ] Session persists across page refreshes

**Technical Notes:**
- Use JWT for session management
- Implement rate limiting for failed attempts
```

**Example 2: Ticket linking**
```
User: "Link this ticket to the authentication epic"
Claude: [Uses pm-jira skill] Linking ticket PROJ-123 to epic PROJ-100 (User Authentication). Also adding related tickets:
- Blocks: PROJ-124 (Password Reset)
- Relates to: PROJ-125 (Session Management)
```

## Jira Best Practices

This skill ensures tickets have:
- Clear user story format (As a... I want... So that...)
- Specific, testable acceptance criteria
- Proper labeling and categorization
- Epic and story linking
- Estimation points (if using)
- Technical notes and dependencies

## Copy/Paste Ready

To use this skill:
- "Create a Jira ticket for [feature]"
- "Format this as a Jira user story"
- "Add acceptance criteria to this ticket"
