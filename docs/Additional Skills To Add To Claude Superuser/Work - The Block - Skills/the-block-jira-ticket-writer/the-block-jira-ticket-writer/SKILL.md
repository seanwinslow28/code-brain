---
name: the-block-jira-ticket-writer
description: Generate Jira tickets following The Block's standards - Epics, Design Stories, and Implementation Stories for .Co and Campus products
---

# the-block-jira-ticket-writer

## Overview

This skill generates Jira tickets that follow The Block's established standards. It creates properly formatted Epics, Design Stories (`[Design]` prefix), and Implementation Stories (`[Implementation]` prefix) with the correct structure, acceptance criteria, and metadata.

**Key Patterns:**
- Separate tickets for Design and Implementation work
- Design tickets grouped with Implementation tickets under the same Epic
- User stories follow "As a user, I want... so that..." format
- Components: `Campus` for LMS features, `theblock.co` for free site
- Labels: `NeedsDesign`, `frontend`, `BACKEND`

## When to Use This Skill

Use this skill when:
- Breaking down a PRD into Jira tickets
- Creating a new feature Epic with child stories
- Writing individual Design or Implementation stories
- Converting feature requirements into development-ready tickets

## Quick Reference

| Ticket Type | Prefix | Use Case |
|-------------|--------|----------|
| Epic | None | Container for related feature work |
| Design Story | `[Design]` | UI/UX specs, Figma deliverables |
| Implementation Story | `[Implementation]` | Developer work with acceptance criteria |
| Task | `[Implementation]` or none | Focused technical work |

---

## Epic Template

**Title Format:** `{Feature Name}` (concise, no prefix needed)

**Description Structure:**

```markdown
{One-sentence summary of what we're building}

**Problem:** {What problem are we solving? Include data if available}

**Solution:** {High-level approach to solving the problem}

**Scope:**
• {Major deliverable 1}
• {Major deliverable 2}
• {Major deliverable 3}
• {Continue as needed}

**Success Metrics:**
• {Metric 1 with target, e.g., "Completion rate >60%"}
• {Metric 2 with target}
• {Continue as needed}

{Optional: Attach diagram, mockup, or flow image}
```

**Required Fields:**
- Summary (title)
- Description
- Components (Campus and/or theblock.co)
- Priority

**Example - Job Board Epic:**

```markdown
Summary: .CO Job Board

Description:
The Block Job Boards will extend our brand into the crypto jobs market by leveraging our strong distribution and reputation.

**Problem:** Unlike niche job boards with limited reach, The Block can provide both visibility for employers and trusted opportunities for candidates.

**Solution:** Launch a V1 job board with aggregated listings, manual upload process, and homepage visibility to drive traffic.

**Scope:**
• Basic job board functionality with aggregated job listings
• Manual upload of jobs (no client-facing management interface)
• Core discovery and filtering features for candidates
• Homepage visibility to drive traffic
• Basic reporting for employers (clicks, impressions, apply clicks via GA4)

**Success Metrics:**
• Job listing views >10,000/month
• Apply click-through rate >5%
• 50+ active job listings within 3 months

Components: theblock.co
Priority: High
```

---

## Design Story Template

**Title Format:** `[Design] {Feature or Component Name}`

**Description Structure:**

```markdown
As the product team, we need {what designs are needed} so that {why engineering needs them}.

**Summary:** {1-2 sentence overview of design deliverables}

**Acceptance Criteria:**
• {Specific design deliverable 1}
• {Specific design deliverable 2}
• {Mobile/responsive requirements}
• {Handoff requirements - typically "Design specs handed off in Figma with component documentation"}
```

**Required Fields:**
- Summary (title with `[Design]` prefix)
- Description
- Components
- Priority
- Labels: `NeedsDesign`
- Epic Link (parent Epic)

**Example - Sponsored Courses Design:**

```markdown
Summary: [Design] Sponsored Courses Integration

Description:
As the product team, we need complete designs for all sponsored course touchpoints so that engineering can implement a consistent, high-quality user experience across .Co and Campus.

**Summary:** Design all UI components and user flows for the Sponsored Courses MVP, including discovery surfaces on theblock.co (homepage module, learn page module, in-article component), course description landing pages, authentication flow, and completion states.

**Acceptance Criteria:**
• Homepage sponsored course module design (extends CryptoIQ pattern)
• Learn page free courses module design (1-3 cards initially, scales to 5)
• In-article course teaser component design (appears after paragraph 3)
• Course description page design (/learn/[course-slug])
• X authentication flow design (reuses CryptoIQ pattern)
• Optional wallet input field design (post-auth)
• Completion state and shareable social card design
• Mobile-responsive variants for all components
• Design specs handed off in Figma with component documentation

Components: Campus, theblock.co
Priority: High
Labels: NeedsDesign
```

---

## Implementation Story Template

**Title Format:** `[Implementation] {Feature or Component Name}`

**Description Structure:**

```markdown
As a user, I want to {action/capability} so that {benefit/value}.

**Summary:** {1-2 sentence technical overview of what's being built}

**Acceptance Criteria:**
• {Functional requirement 1}
• {Functional requirement 2}
• {Analytics/tracking requirement}
• {Responsive/cross-browser requirement}
• {Error handling requirement}
• {Continue as needed}

**Technical Notes:**
• {Implementation detail 1}
• {Dependency or integration note}
• {Data source or API note}
```

**Required Fields:**
- Summary (title with `[Implementation]` prefix)
- Description
- Components
- Priority
- Labels: `frontend` or `BACKEND` (or both)
- Epic Link (parent Epic)

**Example - Homepage Module:**

```markdown
Summary: [Implementation] Homepage Sponsored Course Module

Description:
As a user, I want to see a sponsored course promotion with clear actions so that I can either learn more about the course or start it immediately.

**Summary:** Implement the homepage sponsored course module extending the CryptoIQ pattern, with dual CTAs routing to the course description page or directly to the Campus login flow.

**Acceptance Criteria:**
• Module renders in designated homepage position
• "See Details" CTA routes to /learn/[course-slug]
• "Take the Course" CTA routes to auth flow, then deep-links to Campus course
• Sponsor branding displays correctly (logo, tagline, "Sponsored by" label)
• Module content is CMS-configurable (course title, sponsor, image)
• Responsive behavior matches design specs
• Analytics events fire on module impression and CTA clicks
• Cross-browser testing (Chrome, Safari, Firefox, Edge)

**Technical Notes:**
• Extend existing CryptoIQ module component
• Course data fetched from CMS or config
• Deep link URL pattern: /campus/courses/[course-slug]

Components: theblock.co
Priority: High
Labels: frontend
```

**Example - Backend Story:**

```markdown
Summary: [Implementation] Sponsor Lead Data Export

Description:
As a user, I want my course completion data securely captured so that sponsors can receive performance reports.

**Summary:** Implement backend systems to capture, store, and export sponsor lead data including user information, completion status, and quiz scores.

**Acceptance Criteria:**
• Captured data fields: email, X handle, wallet address (if provided), completion date, quiz score
• Data stored securely with user consent timestamp
• Export mechanism available (CSV format for MVP)
• Export filtered by sponsor/course
• Sponsor performance metrics available: starts, completions, signups
• Manual report generation acceptable for MVP (dashboard deferred)
• Data export complies with privacy review requirements
• xAPI completion events logged and queryable

**Technical Notes:**
• xAPI events from Campus LMS
• Privacy review needed for specific shareable fields
• Format: CSV for MVP, webhook for scale

Components: Campus
Priority: High
Labels: BACKEND
```

---

## Component Reference

| Component | Description | Use When |
|-----------|-------------|----------|
| `Campus` | LMS/education platform | Course features, learning paths, Campus UI |
| `theblock.co` | Free site | Homepage, articles, navigation, public pages |
| `Pro Research` | Pro tier research | Research tools, reports |
| `Pro News` | Pro tier news | Premium news features |
| `Pro Deals` | Pro tier deals | Deal tracking features |
| `Pro Data` | Pro tier data | Data/analytics features |
| `Pro API` | API integrations | External API work |
| `Launchpad` | Launchpad product | Launchpad-specific features |
| `Wordpress` | CMS | Content management, publishing |

**Rule:** If a feature spans both Campus AND theblock.co, add BOTH components.

---

## Label Reference

| Label | Use When |
|-------|----------|
| `NeedsDesign` | Story requires design work before implementation |
| `frontend` | Story involves UI/frontend development |
| `BACKEND` | Story involves backend/API/database work |

---

## Project Keys

Primary project for Product & Engineering work: **PRO** (Team 1)

Other relevant keys:
- `GD` - Design requests
- `DE` - Data Engineering
- `OP` - Infrastructure/DevOps

---

## Workflow: PRD to Tickets

When given a PRD, follow this sequence:

### Step 1: Create the Epic
Extract from the PRD:
- Problem statement
- Solution overview  
- Scope items
- Success metrics

### Step 2: Create Design Story
One `[Design]` story covering all UI/UX deliverables for the feature.

### Step 3: Create Implementation Stories
Break down by:
- **User-facing surfaces** (Homepage, Learn page, Article page, etc.)
- **Technical systems** (Auth, Deep linking, Data export, etc.)

Each Implementation story should be completable by one developer in roughly one sprint or less.

### Step 4: Link Everything
- All stories link to the parent Epic
- Add appropriate components and labels
- Set priority consistently

---

## Figma Link Format

When referencing designs:
```
https://www.figma.com/design/{fileKey}/{fileName}?node-id={nodeId}
```

---

## Quality Checklist

Before finalizing tickets, verify:

- [ ] Epic has Problem, Solution, Scope, and Success Metrics
- [ ] Design story covers all UI deliverables with Figma handoff requirement
- [ ] Each Implementation story has user story format
- [ ] Each Implementation story has clear acceptance criteria
- [ ] Technical Notes included where implementation details matter
- [ ] Components correctly assigned (Campus vs theblock.co vs both)
- [ ] Labels assigned (NeedsDesign, frontend, BACKEND)
- [ ] Stories are sized appropriately (break down if >1 sprint of work)

---

## Examples from The Block

### Real Epic: Sponsored/Elective Courses Integration (PRO-4354)

**Structure:**
```
Epic: Sponsored/Elective Courses Integration
├── [Design] Sponsored Courses Integration (PRO-4355)
├── [Implementation] Homepage Sponsored Course Module (PRO-4361)
├── [Implementation] Learn Page Courses Module (PRO-4362)
├── [Implementation] In-Article Course Recirculation Component (PRO-4363)
├── [Implementation] Course Description Page (PRO-4364)
├── [Implementation] X Authentication Integration (PRO-4365)
├── [Implementation] Campus Deep Linking and Entitlements (PRO-4366)
├── [Implementation] Sponsor Lead Data Export (PRO-4367)
└── [Implementation] Completion Shareable Social Card (PRO-4368)
```

### Real Epic: .CO Job Board (PRO-3513)

**Structure:**
```
Epic: .CO Job Board
├── [Design] .CO Job board aggregate & individual pages (PRO-3517)
├── DB > Jobs database on Laravel (PRO-3518)
├── [Implementation] Aggregate job board (PRO-3514)
├── [Implementation] Job Board Homepage presence (PRO-3515)
├── [Implementation] Individual job page (PRO-3516)
└── [Implementation] Adding email to SendGrid contact list (PRO-4207)
```

---

## Usage Instructions

**To generate tickets from a PRD:**
```
"Here's a PRD for [feature]. Please create Jira tickets following The Block's standards."
```

**To create a single ticket:**
```
"Create a [Design/Implementation] story for [feature description]"
```

**To break down an existing Epic:**
```
"Here's an Epic description. Please create the child Design and Implementation stories."
```
