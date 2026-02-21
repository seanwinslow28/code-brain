---
name: subscription-audit
description: Subscription and recurring expense auditor. Analyzes bank/credit card exports to identify subscriptions, finds free alternatives, and outputs a keep/replace/cancel decision matrix. Use when user says "audit my subscriptions", "find recurring charges", "cut expenses", or "subscription review".
---

# Subscription Audit

## Purpose

Identify all recurring charges from bank or credit card statements, evaluate each subscription against usage and free alternatives, and produce an actionable keep/replace/cancel matrix. Directly supports debt reduction by surfacing hidden recurring costs.

## When to Use

- Reviewing bank/credit card CSV exports for recurring charges
- Annual subscription audit (recommended quarterly)
- After receiving a "your price is going up" notification
- When actively cutting expenses or paying down debt

## Examples

**Example 1: CSV Import Audit**
```
User: "Audit my subscriptions from this Chase export"
Claude: [Uses subscription-audit] Parsing chase_statement_jan.csv...

Found 14 recurring charges totaling $487/month:

| Service        | Amount  | Frequency | Category     | Action   |
|:---------------|:--------|:----------|:-------------|:---------|
| Netflix        | $22.99  | Monthly   | Entertainment| Keep     |
| Adobe CC       | $59.99  | Monthly   | Creative     | Review   |
| Grammarly      | $12.00  | Monthly   | Productivity | Replace  |
| Headspace      | $12.99  | Monthly   | Wellness     | Cancel   |

Potential monthly savings: $142/month ($1,704/year)
```

**Example 2: Quick Review**
```
User: "Is Notion worth keeping vs free alternatives?"
Claude: [Uses subscription-audit]
Notion ($10/mo) vs Free alternatives:
- Obsidian (free, local-first, you already use it)
- Logseq (free, open-source)
Recommendation: CANCEL — migrate remaining content to Obsidian vault.
```

## Audit Workflow

### 1. Import & Parse

Accept data in any of these formats:
- **CSV export** from bank/credit card (Chase, Amex, etc.)
- **Pasted text** from a statement
- **Manual list** of subscriptions the user types out

Parse each transaction and identify recurring charges by:
- Matching merchant names across multiple months
- Flagging common subscription merchant patterns (Netflix, Spotify, Adobe, AWS, etc.)
- Grouping by billing frequency (monthly, annual, weekly)

### 2. Categorize

Assign each subscription to a category:

| Category | Examples |
|:---------|:---------|
| Creative Tools | Adobe CC, Figma, Canva |
| Productivity | Notion, Todoist, Grammarly |
| Entertainment | Netflix, Spotify, YouTube Premium |
| Developer Tools | GitHub Pro, Vercel, Railway |
| Cloud/Storage | iCloud, Google One, Dropbox |
| Wellness | Headspace, gym memberships |
| News/Learning | Substack, Medium, Coursera |
| AI Tools | ChatGPT Plus, Midjourney, Claude Pro |
| Other | Miscellaneous recurring charges |

### 3. Evaluate

For each subscription, assess:

- **Usage frequency:** Daily / Weekly / Rarely / Never
- **Free alternative exists?** Name the specific alternative
- **Overlap:** Does another paid tool cover this? (e.g., Obsidian replaces Notion)
- **ROI justification:** Does this directly support income or a priority goal?

### 4. Decision Matrix

Output a decision matrix with one of four actions:

| Action | Criteria |
|:-------|:---------|
| **Keep** | High usage + no free alternative + supports goals |
| **Downgrade** | Useful but on a plan tier higher than needed |
| **Replace** | Free or cheaper alternative covers the use case |
| **Cancel** | Low usage, redundant, or no longer relevant |

### 5. Savings Summary

Always end with:
- Total current monthly spend
- Projected monthly spend after changes
- Annual savings
- Suggested reallocation (e.g., "redirect $142/mo to credit card paydown")

## Negotiation Tips

When the decision is "Keep" but the price is high:
- Call and ask for retention offers (works for streaming, internet, phone)
- Check for annual billing discounts (typically 15-20% savings)
- Look for student/education discounts
- Stack with cashback credit card categories

## Success Criteria

- [ ] All recurring charges identified from the provided data
- [ ] Each subscription categorized and evaluated
- [ ] Free alternatives named (not generic "there are alternatives")
- [ ] Decision matrix includes dollar amounts and frequencies
- [ ] Savings summary with monthly and annual projections

## Copy/Paste Ready

```
"Audit my subscriptions from this bank export"
"Find all recurring charges over the last 3 months"
"Compare my current tools against free alternatives"
"How much can I save by cutting unused subscriptions?"
```