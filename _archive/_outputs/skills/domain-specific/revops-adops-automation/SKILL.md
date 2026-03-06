---
name: revops-adops-automation
description: Revenue operations and ad operations automation for media and data companies. Generates pipeline reports, revenue forecasts, campaign audit checklists, yield analysis, CRM hygiene workflows, and operations dashboards. Use when building revenue reports, analyzing ad campaign performance, automating Salesforce or HubSpot workflows, creating forecast models, or specifying RevOps/AdOps features.
---

# RevOps and AdOps Automation

## Purpose

Provide revenue operations and ad operations automation patterns for media and data companies like The Block. Enable Claude to generate pipeline analyses, campaign audits, forecast models, CRM integration specs, and operations dashboards. Frame everything as PM-level specifications and workflows, not engineering implementation.

## When to Use

- Building revenue reporting dashboards or pipeline analyses
- Creating ad campaign performance reports or audits
- Automating CRM data hygiene (Salesforce, HubSpot)
- Generating revenue forecasts with historical data
- Specifying AdOps workflows (campaign setup, yield optimization)
- Writing PRDs for operations tooling

## Examples

**Example 1: Pipeline health report**
```
User: "Create a quarterly pipeline health report template"
Claude: [Uses revops-adops-automation]

# Q[N] Pipeline Health Report

## Executive Summary
- **Total Pipeline Value:** $[X]M ([+/-N%] vs last quarter)
- **Weighted Pipeline:** $[X]M (using stage-based probabilities)
- **Coverage Ratio:** [X]:1 (target: 3:1 minimum)
- **Average Deal Size:** $[X]K ([+/-N%] vs trailing 4Q average)

## Pipeline by Stage

| Stage | Count | Value | Avg Age (days) | Conversion Rate |
|-------|-------|-------|----------------|-----------------|
| Qualified | [N] | $[X]K | [N] | [N]% |
| Discovery | [N] | $[X]K | [N] | [N]% |
| Proposal | [N] | $[X]K | [N] | [N]% |
| Negotiation | [N] | $[X]K | [N] | [N]% |
| Closed Won | [N] | $[X]K | - | - |
| Closed Lost | [N] | $[X]K | - | - |

## Risk Flags
- [ ] [N] deals stale >45 days in same stage
- [ ] [N] deals missing Next Step field
- [ ] [N] deals in Negotiation with <50% probability
- [ ] Coverage ratio below 3:1 for [segment]

## Recommendations
1. [Specific action for stale deals]
2. [Specific action for pipeline gaps]
```

**Example 2: Ad campaign audit**
```
User: "Audit our Q4 display ad campaigns"
Claude: [Uses revops-adops-automation]

# Q4 Display Campaign Audit

## Performance Summary

| Campaign | Impressions | CTR | eCPM | Fill Rate | Revenue |
|----------|------------|-----|------|-----------|---------|
| Homepage Takeover | 2.1M | 0.12% | $18.50 | 94% | $38,850 |
| Data Page Sidebar | 850K | 0.08% | $12.20 | 87% | $10,370 |
| Newsletter Sponsor | 120K | 2.1% | $45.00 | 100% | $5,400 |

## Issues Found
- CRITICAL: Homepage Takeover fill rate dropped from 98% to 94%
  Recommendation: Review floor price ($15 CPM) against market
- MEDIUM: Data Page CTR below benchmark (0.08% vs 0.15% target)
  Recommendation: Request updated creative from advertiser
```

## Pipeline Analysis Framework

### Standard Deal Stage Definitions

| Stage | Exit Criteria | Probability | Max Age |
|-------|--------------|-------------|---------|
| Lead | Qualified by SDR, fits ICP | 10% | 14 days |
| Qualified | Budget confirmed, decision-maker identified | 20% | 21 days |
| Discovery | Needs mapped, use case validated | 40% | 30 days |
| Proposal | Proposal delivered, pricing discussed | 60% | 21 days |
| Negotiation | Terms being finalized | 80% | 30 days |
| Verbal Close | Agreement in principle | 90% | 14 days |
| Closed Won | Contract signed | 100% | - |
| Closed Lost | - | 0% | - |

### CRM Hygiene Audit Checklist

Run these checks weekly against Salesforce/HubSpot data:

```markdown
## Data Quality Checks
- [ ] All open opportunities have an Amount > $0
- [ ] All open opportunities have a Close Date in the future
- [ ] All opportunities in Discovery+ have a Next Step populated
- [ ] No duplicate accounts (match on domain name)
- [ ] No contacts without an associated account
- [ ] All Closed Won deals have contract start date

## Stage Integrity Checks
- [ ] No deals in same stage > [Max Age] days
- [ ] Probability matches stage (no manual overrides)
- [ ] No deals jumped from Lead directly to Negotiation
- [ ] All Closed Lost have a Loss Reason selected

## Output Format
Generate a CSV with columns:
Opportunity ID, Name, Issue Type, Current Value, Days in Stage, Owner
```

### Weighted Pipeline Forecast

```typescript
interface DealStage {
  name: string;
  probability: number;  // 0-1
  historical_conversion: number;  // Actual conversion rate from last 4 quarters
}

interface ForecastConfig {
  stages: DealStage[];
  use_historical: boolean;  // Use actual conversion rates vs stated probability
  confidence_interval: number;  // 0.8 = 80% CI
}

interface ForecastResult {
  expected_revenue: number;
  best_case: number;     // Upper bound of CI
  worst_case: number;    // Lower bound of CI
  coverage_ratio: number;  // Pipeline / Quota
  at_risk_deals: Deal[];   // Stale or missing data
}

// Forecast calculation pattern
// Use historical conversion rates, not CRM probability fields
// Apply Monte Carlo simulation for confidence intervals
// Flag deals where stage age > 1.5x average for that stage
```

## AdOps Workflow Patterns

### Campaign Setup Checklist

```markdown
## Pre-Launch Checklist (Direct Sold)
- [ ] IO (Insertion Order) signed and uploaded to CRM
- [ ] Campaign dates confirmed (start/end)
- [ ] Creative assets received and spec-compliant
  - [ ] Display: 300x250, 728x90, 160x600 (+ mobile sizes)
  - [ ] Specs: <150KB file size, <15s animation, click-through URL set
- [ ] Targeting configured:
  - [ ] Geo targeting (if applicable)
  - [ ] Content targeting / section restriction
  - [ ] Frequency cap set (recommend: 3/user/day)
- [ ] Impression goal entered in ad server
- [ ] Click tracking URL tested (resolves to correct landing page)
- [ ] Revenue booked in CRM (monthly allocation if multi-month)
- [ ] Pacing type set (even / front-loaded / ASAP)

## Mid-Flight Checks (Weekly)
- [ ] Delivery pacing within 10% of target
- [ ] CTR above minimum threshold (0.05% display, 1% native)
- [ ] No creative errors or broken click-throughs
- [ ] Fill rate above 90% for guaranteed campaigns

## Post-Campaign
- [ ] Final delivery report generated
- [ ] Over/under delivery calculated
- [ ] Makegoods scheduled if under-delivered > 10%
- [ ] Revenue reconciliation completed in CRM
- [ ] Case study opportunity flagged (if strong performance)
```

### Yield Optimization Framework

| Metric | Definition | Healthy Range | Action if Below |
|--------|-----------|--------------|-----------------|
| eCPM | Effective revenue per 1000 impressions | $8-25 (display) | Review floor prices, test header bidding |
| Fill Rate | % of ad requests that serve an ad | >90% (direct), >70% (programmatic) | Lower floors, add demand partners |
| Viewability | % of served ads actually seen by user | >60% | Adjust ad placement, lazy-load below fold |
| CTR | Click-through rate | >0.08% (display), >0.5% (native) | Refresh creative, improve targeting |
| Revenue/Page | Revenue generated per page view | Varies by section | Optimize ad density, test layouts |

### Revenue Reporting Template

```markdown
# Monthly Revenue Report - [Month Year]

## Revenue Summary
| Source | Actual | Budget | Variance | YoY Change |
|--------|--------|--------|----------|------------|
| Direct Display | $[X] | $[X] | [+/-N%] | [+/-N%] |
| Programmatic | $[X] | $[X] | [+/-N%] | [+/-N%] |
| Sponsorships | $[X] | $[X] | [+/-N%] | [+/-N%] |
| Data/API | $[X] | $[X] | [+/-N%] | [+/-N%] |
| Events | $[X] | $[X] | [+/-N%] | [+/-N%] |
| **Total** | **$[X]** | **$[X]** | **[+/-N%]** | **[+/-N%]** |

## Key Metrics
- **ASP (Avg Selling Price):** $[X] CPM (vs $[X] target)
- **Win Rate:** [N]% (vs [N]% last month)
- **New Logos:** [N] (contributing $[X] in bookings)
- **Renewal Rate:** [N]% of expiring contracts renewed

## Pipeline for Next Month
- **Committed:** $[X] ([N]% of target)
- **Probable (>60%):** $[X]
- **Pipeline Total:** $[X]
- **Gap to Target:** $[X]
```

## Sub-Agent Orchestration Pattern

For complex RevOps automation, use specialized agents:

```markdown
## Agent Architecture

### PPC Auditor Agent
- **Scope:** Google Ads, Meta Ads performance analysis
- **Access:** Read-only to ad platform APIs
- **Output:** Structured audit report with severity ratings
- **Guardrail:** Never modifies bids or budgets directly

### Yield Analyst Agent
- **Scope:** eCPM trends, fill rate optimization, floor price analysis
- **Access:** Ad server reporting API
- **Output:** Yield recommendations with projected impact
- **Guardrail:** Recommendations require human approval before implementation

### CRM Hygienist Agent
- **Scope:** Salesforce/HubSpot data quality
- **Access:** Read-only to CRM
- **Output:** CSV of records needing cleanup with specific issues
- **Guardrail:** Never modifies CRM records directly
```

### Plan Mode for High-Stakes Changes

Before any AdOps change exceeding $500 impact:

```markdown
1. Agent generates change proposal with:
   - What: Specific change (e.g., "Lower floor price from $15 to $12 CPM")
   - Why: Data supporting the change (e.g., "Fill rate dropped 8% this week")
   - Impact: Projected revenue effect (e.g., "+$2K/week from volume, -$1K from price")
   - Risk: What could go wrong (e.g., "CPMs could fall further if market softens")

2. Human reviews and approves/rejects

3. Only after approval: Agent executes the change

4. Agent monitors for 48 hours and reports back
```

## Success Criteria

- [ ] Pipeline reports include coverage ratios and risk flags
- [ ] CRM hygiene checks cover data quality and stage integrity
- [ ] Campaign checklists cover pre-launch through post-campaign
- [ ] Revenue reports include actuals vs budget and YoY comparisons
- [ ] AdOps recommendations require human approval for high-impact changes
- [ ] All templates use consistent metrics definitions

## Copy/Paste Ready

```
"Generate a quarterly pipeline health report"
"Audit our ad campaign performance for this month"
"Create a CRM data hygiene checklist for Salesforce"
"Build a revenue forecast using our current pipeline"
"Write a campaign setup checklist for a new direct-sold deal"
```
