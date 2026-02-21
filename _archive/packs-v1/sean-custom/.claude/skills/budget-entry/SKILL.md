---
name: budget-entry
description: Quick expense categorization and budget tracking. Paste receipts or transactions, get categorized entries.
---

# Budget Entry Skill

## Purpose

Turn messy transaction data into categorized budget entries. Supports bank exports, receipt text, or manual entry. Zero friction.

## Clarifying Interview (First Use Only)

```
Budget Setup (one-time):

1. **Categories you use:**
   [ ] Housing | Utilities | Groceries | Dining | Transport
   [ ] Entertainment | Shopping | Health | Subscriptions | Savings
   [ ] Custom: ___

2. **Budget tracking method:**
   [ ] Spreadsheet (Google Sheets / Excel)
   [ ] App (YNAB / Mint / Copilot)
   [ ] Plain text / Markdown
   [ ] Notion database

3. **Currency:** USD | EUR | Other: ___

4. **Include tax separately?** Y/N
```

## Input Formats Accepted

### Bank Statement Paste
```
01/15 UBER EATS           -$24.50
01/15 SPOTIFY             -$10.99
01/16 AMAZON.COM          -$47.82
01/16 TRANSFER TO SAVINGS -$500.00
```

### Receipt Text
```
Trader Joe's
01/16/2024

Bananas         $0.79
Eggs            $4.99
Chicken breast  $8.99
Olive oil       $6.49
-----------------
Subtotal:      $21.26
Tax:            $0.64
Total:         $21.90
Paid: VISA ****1234
```

### Voice/Quick Entry
```
"Coffee at Blue Bottle $6"
"Uber to airport $45"
"Monthly gym $50"
```

## Output Format

### Categorized Table
```markdown
| Date | Description | Category | Amount | Notes |
|------|-------------|----------|--------|-------|
| 01/15 | Uber Eats | Dining | $24.50 | Delivery fee included |
| 01/15 | Spotify | Subscriptions | $10.99 | Monthly |
| 01/16 | Amazon | Shopping | $47.82 | Review for category |
| 01/16 | Savings | Savings | $500.00 | Auto-transfer |
```

### For Spreadsheet (CSV-Ready)
```csv
Date,Description,Category,Amount,Notes
2024-01-15,Uber Eats,Dining,24.50,
2024-01-15,Spotify,Subscriptions,10.99,Monthly
2024-01-16,Amazon,Shopping,47.82,Review
2024-01-16,Savings Transfer,Savings,500.00,
```

### Summary View
```markdown
## Week of Jan 15-21

**Total Spent:** $583.31

| Category | Amount | % of Total | vs Budget |
|----------|--------|------------|-----------|
| Dining | $124.50 | 21% | ⚠️ 80% used |
| Groceries | $89.00 | 15% | ✅ On track |
| Subscriptions | $45.99 | 8% | ✅ Expected |
| Shopping | $123.82 | 21% | ⚠️ Review items |
| Savings | $200.00 | 34% | ✅ Goal met |

**Flagged for Review:**
- Amazon $47.82 - Unclear category
- Target $76.00 - Mixed purchase
```

## Category Rules (Customizable)

```yaml
# Auto-categorization rules
rules:
  dining:
    - contains: [uber eats, doordash, grubhub, restaurant, cafe, coffee]
  groceries:
    - contains: [trader joe, whole foods, safeway, grocery, market]
  subscriptions:
    - contains: [spotify, netflix, hulu, disney+, youtube, adobe]
  transport:
    - contains: [uber, lyft, gas, parking, transit]
  utilities:
    - contains: [pg&e, electric, water, internet, phone]
```

## Success Criteria

- [ ] Every transaction has a category
- [ ] Amounts match source (bank/receipt)
- [ ] Ambiguous items flagged for review
- [ ] Running totals are accurate
- [ ] Output format matches your tracking system

## Verification Steps

1. **Sum Check:** Do categorized amounts match bank total?
2. **Category Check:** Any miscategorized items?
3. **Duplicate Check:** Any transactions entered twice?
4. **Date Check:** All dates in correct format for your system?

## Quick Commands

```
/budget-entry [paste bank statement]
/budget-entry receipt: [paste receipt text]
/budget-entry quick: coffee $5, lunch $15, uber $22
/budget-entry summarize January
/budget-entry compare Jan vs Dec
```

## Integration Patterns

### For Google Sheets
```
After categorizing, paste into your Budget sheet:
1. Copy the CSV output
2. Paste into column A
3. Data → Split text to columns

Or use this formula for auto-import:
=IMPORTDATA("your-csv-url")
```

### For Notion
```markdown
Create database entries:
- Date: [date property]
- Description: [title]
- Category: [select]
- Amount: [number]
- Notes: [text]
```

## Monthly Review Template

```markdown
# [Month] Budget Review

## Summary
- **Total Income:** $X,XXX
- **Total Expenses:** $X,XXX
- **Savings Rate:** XX%

## By Category
| Category | Budgeted | Actual | Variance |
|----------|----------|--------|----------|
| Housing | $X,XXX | $X,XXX | ✅/⚠️/🔴 |
| ... | ... | ... | ... |

## Insights
- Largest unexpected expense:
- Category most over budget:
- Wins this month:

## Next Month Adjustments
- [ ] Adjustment 1
- [ ] Adjustment 2
```
