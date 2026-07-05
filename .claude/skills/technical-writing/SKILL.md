---
name: technical-writing
description: Technical writing craft for reader-first documents people actually finish — the decision or action visible in the first screen, not buried under the author's journey. Covers API getting-started guides, system design documents, onboarding guides, runbooks, release notes, changelogs, RFCs, internal proposals, and PR descriptions. Use when asked to "write an API guide", "system design doc", "onboarding guide", "runbook", "release notes", "changelog", "write an RFC", "internal proposal", "PR description", or "what's new announcement".
---

# Technical Writing

## Purpose

Write clear, audience-aware technical documents that humans actually read. This skill focuses on writing craft — structure, clarity, progressive disclosure — not automated doc generation (see `doc-workflows` for that). Every document type has a template, writing principles, and a review checklist.

## When to Use

- Writing API getting-started guides or tutorials (not OpenAPI specs)
- Drafting system design documents for mixed-technical audiences
- Creating onboarding guides for new team members or contributors
- Writing runbooks for operational procedures
- Crafting release notes users will read
- Writing internal RFCs or technical proposals
- Any document where the audience matters as much as the content

## Differentiation from Related Skills

| Skill | Focus |
|:------|:------|
| `doc-workflows` | Automated doc generation from code (READMEs, API refs, doc-code sync) |
| `tech-spec` | Engineering implementation blueprints (internal, for builders) |
| `decision-doc` | Capturing decision rationale (lightweight ADRs) |
| **technical-writing** | **Writing craft for audience-facing documents** |

## When This Craft Feeds Another Skill's Artifact

`decision-doc`, `stakeholder-update`, a portfolio case study, or a GitHub PR body each own their document *shape* — but they're only as good as the writing craft inside them. When you produce (or hand off to) one of those, the First-Screen Test and reader-first structure still apply: a decision record whose decision is buried, or a PR description that walks the files before it says what changed and why it's safe, fails the same way any other doc does. This skill supplies that craft layer; the other skill owns the artifact's structure.

## Writing Principles

Apply these to every document:

1. **Front-load the conclusion — reader's need, not author's journey.** Lead with what the *reader* needs to do or decide, not the story of how *you* got there. The single most important thing (the decision, the action, the outcome) goes in the first screen — never after a "Background" or "Current State" warm-up. Chronological author-narrative ("first we tried X, then Y, so we…") is the default failure mode; invert it. (Enforced by the First-Screen Test below.)
2. **Write for the scanner.** Most readers scan. Use headers, bullet lists, bold key terms, and tables. Wall-of-text paragraphs lose readers.
3. **Progressive disclosure.** Layer information: overview → quick start → detailed reference. Let readers stop when they have enough.
4. **Active voice, plain language.** "The server validates the token" not "The token is validated by the server." Avoid jargon unless the audience expects it.
5. **One idea per paragraph.** If a paragraph covers two topics, split it.
6. **Show, don't just tell.** Every concept needs an example. Code blocks, command outputs, screenshots, or diagrams.

## The First-Screen Test (the gate that makes docs get finished)

"Front-load the conclusion" is easy to nod along to and still bury the lede. This is the forcing check that makes it real. A hiring manager or a busy engineer skims; if the one thing that matters isn't visible before they scroll, they bounce — and for the public repo and PM portfolio, that reader is often deciding something about the author. So every document clears this gate before it ships:

**Cover the doc below the first paragraph (or the fold). From the title + first screen alone, can the reader state: (1) what this is, (2) the single most important decision / action / outcome, and (3) whether it's for them?** If not, the lede is buried — move it up.

Concretely:
- A system design doc's first screen names the *decision*, not just the system.
- A PR description's first screen says what changed and why it's safe to merge, before the file-by-file walk.
- Release notes lead with the one change users care about, not the version number.
- An RFC's first screen states the proposal, not three paragraphs of problem history.

If the most important sentence is currently in the middle or the end, that isn't a summary problem — that's the doc. Cut or move everything that delays it.

## Examples

**Example 1: API Getting-Started Guide**
```
User: "Write a getting-started guide for our data API"
Claude: [Uses technical-writing]

# Getting Started with the Crypto Market Data API

Get live and historical crypto market data in under 5 minutes.

## Quick Start

1. Get your API key at https://...
2. Make your first request:

```bash
curl -H "Authorization: Bearer YOUR_KEY" \
  https://api.example-crypto.com/v1/prices/BTC
```

3. Parse the response:
```json
{ "symbol": "BTC", "price": 98432.50, "timestamp": "..." }
```

## Next Steps
- [Authentication Guide] — API key management, rate limits
- [Endpoints Reference] — Full endpoint list with examples
- [Webhooks] — Real-time data streaming
```

**Example 2: Runbook**
```
User: "Write a runbook for when the API goes down"
Claude: [Uses technical-writing]

# Runbook: API Service Degradation

**Severity:** P1 | **On-call:** Backend team | **Escalation:** VP Eng after 30 min

## Symptoms
- 5xx error rate > 5% on /api/* endpoints
- Latency p99 > 2000ms for >5 minutes

## Immediate Actions (first 5 minutes)
1. Check Datadog dashboard: [link]
2. Verify database connectivity: `pg_isready -h db.example.com`
3. Check recent deploys: `gh run list --limit 5`
...
```

## Document Templates

### API Getting-Started Guide

```markdown
# Getting Started with [Product Name]

[One sentence: what this API does and who it's for.]

## Prerequisites
- [Account/API key requirement]
- [Runtime/SDK requirement]

## Quick Start
1. [Authentication step]
2. [First API call with curl/code]
3. [Parse the response]

## Core Concepts
### [Concept 1 — e.g., "Authentication"]
[Explanation + code example]

### [Concept 2 — e.g., "Pagination"]
[Explanation + code example]

## Common Use Cases
| Use Case | Endpoint | Example |
|----------|----------|---------|
| [Use case] | `GET /v1/...` | [Link to example] |

## Error Handling
| Code | Meaning | What to Do |
|------|---------|-----------|
| 401 | Invalid API key | Check key in dashboard |
| 429 | Rate limited | Back off, check limits |

## Next Steps
- [Link to full reference]
- [Link to SDKs]
- [Link to support]
```

### System Design Document

```markdown
# [System Name] Design Document

**Author:** [Name] | **Status:** Draft | **Last Updated:** [Date]

## Summary
[2-3 sentences: what this system does and why we're building/changing it.]

## Goals and Non-Goals
**Goals:**
- [Goal 1]

**Non-Goals:**
- [Explicitly out of scope item]

## Current State
[How things work today. Diagrams welcome.]

## Proposed Design
### Architecture Overview
[High-level diagram + explanation]

### Data Model
[Schema changes, new tables, relationships]

### API Changes
[New or modified endpoints]

### Key Trade-offs
| Decision | Alternative | Why This Choice |
|----------|------------|-----------------|
| [Choice] | [Option B] | [Reasoning] |

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| [Risk] | [Impact] | [Plan] |

## Rollout Plan
1. [Phase 1: Feature flag, internal testing]
2. [Phase 2: Canary deployment]
3. [Phase 3: Full rollout]

## Open Questions
- [ ] [Unresolved question needing input]
```

### Onboarding Guide

```markdown
# [Team/Project] Onboarding Guide

Welcome! This guide gets you productive in [timeframe].

## Day 1: Environment Setup
- [ ] Clone repos: `git clone ...`
- [ ] Install dependencies: `npm install`
- [ ] Set up environment: copy `.env.example`, fill in values
- [ ] Verify: `npm run dev` → see [expected output]

## Day 2-3: Architecture Walkthrough
- [ ] Read [Architecture doc]
- [ ] Read [CLAUDE.md] for project conventions
- [ ] Explore key directories: [list with descriptions]

## First Week: Starter Tasks
- [ ] [Small bug fix or docs PR — builds confidence]
- [ ] [Feature addition with guidance — learns patterns]

## Key Contacts
| Topic | Person | Channel |
|-------|--------|---------|
| [Area] | [Name] | [Slack/email] |

## Resources
- [Wiki/Confluence links]
- [Runbooks for common issues]
- [Design docs for major systems]
```

### Runbook

```markdown
# Runbook: [Incident Type]

**Severity:** P1/P2/P3 | **Owner:** [Team] | **Escalation:** [Person] after [time]

## Symptoms
- [Observable symptom 1]
- [Observable symptom 2]

## Diagnostic Steps
1. [Check dashboard/logs: specific URL]
2. [Run diagnostic command: exact command]
3. [Interpret results: what to look for]

## Resolution Steps
### Scenario A: [Root cause 1]
1. [Exact fix step]
2. [Verification step]

### Scenario B: [Root cause 2]
1. [Exact fix step]
2. [Verification step]

## Post-Incident
- [ ] Update incident channel with resolution
- [ ] Write post-mortem if P1
- [ ] Create tickets for follow-up work
```

### Release Notes

```markdown
# [Product] v[X.Y.Z] Release Notes

**Date:** [Date] | **Type:** Major / Minor / Patch

## Highlights
[1-2 sentence summary of the most important change.]

## New Features
- **[Feature name]** — [What it does and why users care. Not how it works internally.]

## Improvements
- [Improvement] — [User-visible benefit]

## Bug Fixes
- Fixed [user-visible behavior] that caused [problem] ([#issue])

## Breaking Changes
- [What changed] — **Migration:** [Exact steps to update]

## Known Issues
- [Issue] — Workaround: [steps]. Fix planned for v[next].
```

### Internal RFC

```markdown
# RFC: [Proposal Title]

**Author:** [Name] | **Date:** [Date] | **Status:** Open for Comment

## Problem Statement
[What problem are we solving? Include data if available.]

## Proposed Solution
[What we should do. Be specific enough to evaluate.]

## Alternatives Considered
| Option | Pros | Cons |
|--------|------|------|
| [This proposal] | [Pro] | [Con] |
| [Alternative A] | [Pro] | [Con] |
| [Do nothing] | No effort | [Problem persists] |

## Implementation Plan
[High-level phases and timeline.]

## Success Metrics
[How we'll know this worked.]

## Open Questions
- [ ] [Question for reviewers]
```

### PR Description

```markdown
## What & why (first screen)
[One or two sentences: what this PR changes and why it's safe to merge. A reviewer should be able to approve in principle from this alone.]

## Changes
- [User- or behavior-visible change]
- [Change 2]

## How to verify
[The exact commands or steps a reviewer runs to confirm it works.]

## Risk / rollback
[What could break, and how to undo it. "Low risk — revert the commit" is a valid answer.]
```

## Review Checklist

Before publishing any technical document:

- [ ] **Audience:** Is it clear who this is for? Does the language match their expertise level?
- [ ] **First-screen test:** From the title + first screen alone, can the reader name what this is, the key decision/action, and whether it's for them? (see The First-Screen Test)
- [ ] **Reader-first, not author-first:** Does it lead with what the reader needs to do/decide, not the chronology of what the author did?
- [ ] **Scannable:** Headers, lists, tables — not walls of text?
- [ ] **Examples:** Does every concept have a concrete example?
- [ ] **Actionable:** Can the reader do something with this information?
- [ ] **Accurate:** Do all commands, code blocks, and links work?
- [ ] **Complete:** No TODO placeholders, no "TBD" sections?

## Success Criteria

- [ ] Document has a clear audience and purpose statement
- [ ] Passes the First-Screen Test — the key decision/action/outcome is visible before the reader scrolls, in reader terms not author chronology
- [ ] Every technical concept has a working example
- [ ] Review checklist passes
- [ ] Document is appropriately differentiated from existing docs (no overlap with doc-workflows output)

## Copy/Paste Ready

```
"Write a getting-started guide for our API"
"Draft a system design document for [feature]"
"Create an onboarding guide for new engineers"
"Write a runbook for [incident type]"
"Draft release notes for this version"
"Write an RFC for [proposal]"
"Write a PR description for this change"
```