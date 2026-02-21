---
name: stakeholder-update
description: Stakeholder communication generator for product managers. Creates executive summaries, status reports, weekly updates, and cross-functional briefs tailored to audience level. Use when asked for a stakeholder update, status report, executive summary, leadership update, weekly update, or presentation outline.
---

# Stakeholder Update Generator

## Purpose

Generate professional stakeholder communications tailored to audience level. Translate technical work into business value for executives, provide detailed progress for engineering peers, and create balanced cross-functional updates. Automate recurring reports to save PM time on weekly and monthly communication cycles.

## When to Use

- User asks for a stakeholder update, status report, or progress summary
- User needs to write an executive summary or leadership brief
- User wants to create a weekly or monthly update
- User needs to tailor a message for a specific audience (technical vs non-technical)
- User asks to generate release notes or changelog communications
- User wants to present project status to different groups

## Examples

**Example 1: Executive summary from git history**
```
User: "Write an executive update for the VP of Engineering based on this week's work"
Claude: [Uses stakeholder-update] I'll analyze recent activity and translate to business impact:

## Executive Status Report: Campus Platform
**Week of Jan 27, 2026**

### Summary
Deployed user authentication overhaul, reducing login failures by 40%.
Payment integration on track for Feb 14 launch.

### Impact
- Velocity: Shipped 3 features (vs 2 planned)
- Quality: Zero critical bugs in production this week
- Risk: Third-party API rate limits may throttle growth next month

### Ask
Approval needed for Enterprise API plan upgrade ($2k/mo) to support Q2 traffic.
```

**Example 2: Cross-functional update**
```
User: "Write a project update for the product, design, and sales teams"
Claude: [Uses stakeholder-update]

## Project Update: CSV Export Feature

### Current Status
On Track for Beta Release by Feb 14.

### What Shipped
- Designers: New export dialog is live on staging (see screenshots)
- Sales: The bulk export feature requested by Client X is functional
- Product: All 5 acceptance criteria passing in QA

### Blockers
- Waiting on: Final legal copy for the data privacy modal
- Impact: Cannot ship to production until legal signs off

### Timeline
No changes to delivery date assuming legal approval by Friday.
```

**Example 3: Standup format**
```
User: "Generate my standup update"
Claude: [Uses stakeholder-update]

**Yesterday:**
- Merged 3 PRs for user authentication module
- Completed code review for dashboard redesign

**Today:**
- Finalizing database schema for reporting module
- Sprint planning meeting at 2pm

**Blockers:**
- Waiting on API credentials for email service provider
```

## The What-Why-How Framework

Use this framework to translate technical work for different audiences:

| Layer | What (Technical) | Why (Business Value) | How (Process) |
|-------|-------------------|---------------------|---------------|
| Executive | "Migrated auth to JWT" | "Enables 5x more concurrent users, preventing crashes during peak traffic" | "Implemented with Redis cache, 15-min TTL" |
| Technical | "Refactored UserService" | "Reduces latency by 200ms per request" | "Used dependency injection for testability" |
| Cross-functional | "New login flow deployed" | "Users can now sign in with SSO" | "Rolling out to 10% of users this week" |

**Rule:** Executives care about risk and ROI. Engineers care about architecture and trade-offs. Cross-functional teams care about timelines and dependencies.

## Templates by Audience

### Executive Summary

```markdown
## Executive Status Report: [Project Name]
**Date:** [Date] | **Author:** [Name] | **Period:** [Week/Month/Quarter]

### Summary
[2-3 sentences: what happened and why it matters to the business]

### Impact Assessment
- **Velocity:** [Features shipped vs planned]
- **Quality:** [Bug count trend, incident summary]
- **Reliability:** [Uptime, performance metrics]

### Key Risks
- **Risk:** [Description]
- **Mitigation:** [What we're doing about it]
- **Ask:** [What you need from leadership]

### Next Period Focus
- [Priority 1]
- [Priority 2]
```

### Technical Deep-Dive

```markdown
## Development Log: [Date/Sprint]

### Accomplishments
- Implemented [component] with [technology choice]
- Refactored [module] to [improvement]

### Architecture Decisions
- **Decision:** [What was decided]
- **Rationale:** [Why this approach]
- **Trade-offs:** [What we gave up]

### Files Modified
- `src/components/LoginForm.tsx`
- `src/hooks/useAuth.ts`

### Open Technical Debt
- [Item requiring future attention]
```

### Cross-Functional Update

```markdown
## Project Update: [Feature Name]
**Date:** [Date] | **Status:** On Track / At Risk / Blocked

### What Shipped
- **Design:** [What designers care about]
- **Sales:** [What sales cares about]
- **Engineering:** [What engineers care about]

### Blockers and Dependencies
- **Waiting on:** [Team/Person] for [Deliverable]
- **Impact:** [What happens if delayed]

### Timeline
- [Any changes to delivery date and why]
```

### Weekly/Monthly Summary

```markdown
## [Weekly/Monthly] Summary: [Period]

### Metrics
- PRs Merged: [Count]
- Issues Closed: [Count]
- Build Success Rate: [Percentage]

### Highlights
- [Key accomplishment 1]
- [Key accomplishment 2]

### Challenges
- [Issue encountered and resolution]

### Next Period Focus
- [Priority 1]
- [Priority 2]
```

### Standup (What/Next/Blockers)

```markdown
**Yesterday:**
- [Completed item 1]
- [Completed item 2]

**Today:**
- [Planned item 1]
- [Planned item 2]

**Blockers:**
- [Blocker with owner and expected resolution]
```

For additional templates including quarterly business reviews and release announcements, see `references/templates.md`.

## Automated Report Generation

### From Git History

Pipe recent commits into a summary:

```bash
git log --since="1 week ago" --oneline | claude -p "Summarize these changes into an executive status report for the VP of Engineering. Focus on business impact, not implementation details."
```

### From Jira/Sprint Data

Use MCP to pull sprint data and generate reports:

1. Query current sprint issues via JQL
2. Calculate completion percentage and velocity
3. Identify blockers and stale items
4. Generate formatted report for the target audience

### Recurring Reports

Configure in CLAUDE.md for consistency:

```markdown
## Communication Standards
- Tone: Professional, concise, direct
- Executive reports: Lead with financial or strategic impact
- Technical reports: Include file paths and architecture decisions
- All reports: Include a "Blockers" section even if empty ("None")
```

## Audience Adaptation Rules

When generating any communication:

1. **Identify the audience** before writing (ask if unclear)
2. **Executive audience:** Remove technical jargon, lead with business metrics, include asks
3. **Technical audience:** Include specific file names, code decisions, and trade-offs
4. **Mixed audience:** Use the cross-functional template with role-tagged sections
5. **External stakeholders:** Remove internal context, focus on deliverables and timelines
6. **Crypto/fintech context:** Include market conditions, regulatory updates, and on-chain metrics where relevant

## Release Notes Template

```markdown
## Release [Version] - [Date]

### New Features
- **[Feature Name]:** [User-friendly description]

### Bug Fixes
- Fixed [issue description] ([Issue Key])

### Configuration Changes
- **Action Required:** [What users need to do]

### Known Issues
- [Issue with workaround if available]
```

## Success Criteria

- [ ] Report matches the audience level (no technical jargon for executives)
- [ ] All sections populated (no placeholder text)
- [ ] Blockers section included even if empty
- [ ] Metrics are specific numbers, not vague descriptions
- [ ] Timeline impacts clearly stated
- [ ] Asks for leadership are explicit and actionable
- [ ] Report can be sent without additional editing

## Copy/Paste Ready

```
"Write a stakeholder update for the leadership team"
"Generate my weekly status report"
"Create an executive summary of this sprint"
"Write release notes for v2.1"
"Generate a standup update from my recent commits"
"Translate this technical update for the sales team"
```
