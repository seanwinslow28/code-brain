---
name: personal-finance
description: Personal finance automation assistant. Import CSV bank exports from Chase and Bilt, categorize transactions via regex, generate monthly spending reports, track credit card debt paydown, audit subscriptions, and manage budget targets. Use this skill when the user mentions "budget", "expenses", "spending report", "categorize transactions", "credit card", "debt paydown", "subscription audit", "how much did I spend", or uploads CSV bank statements.
---

# Personal Finance Automation

## Purpose

A personal finance command center. Processes Chase and Bilt CSV exports into categorized spending reports, tracks credit card debt paydown progress, manages subscription costs, and generates actionable budget insights. Built for a first-time budgeter — the skill provides structure, gamification, and clear visual progress toward financial goals.

## When to Use

- **Processing Statements:** "Analyze my latest Chase CSV" / "Process the new Bilt export"
- **Reporting:** "Monthly spending report" / "Where did my money go?"
- **Debt Tracking:** "How's my credit card paydown going?" / "Interest charges this month?"
- **Subscriptions:** "Run a subscription audit" / "What am I paying for?"
- **Budgeting:** "Am I over budget on dining?" / "Show my budget variance"
- **Savings Goals:** "How much have I saved toward [goal]?" / "[Trip/purchase] fund status"

## Financial Profile (local-only)

The real numbers live in `references/financial-profile.md`, which is **gitignored and never committed** — it stays on local disk only. Load it at runtime for: income baseline, account list and limits, the active subscription roster with keep/cancel status, financial goals in priority order, the annual renewal calendar, and the owner-specific merchant regex map.

If the reference file is missing (fresh clone), ask the user to provide income, accounts, and subscriptions, then regenerate it from the template below.

**Profile template** (placeholder values):

### Income

- **Gross:** $X,XXX.XX/semi-monthly ($X,XXX/month)
- **Net take-home:** $X,XXX.XX/semi-monthly ($X,XXX/month)
- **Deductions:** Medical, dental, vision, life, disability, taxes

### Accounts

| Account | Bank | Limit/Type | Primary Use |
|---------|------|------------|-------------|
| Credit Card A | Chase | $XX,XXX limit | Primary spending card |
| Credit Card B | Bilt | $X,XXX limit | Rent payments (earns points on rent) |
| Checking | Chase | Checking | Primary bank account |
| Savings | Chase | Savings | Emergency fund |

### CSV Formats

**Chase Credit Card:**
```
Transaction Date,Post Date,Description,Category,Type,Amount,Memo
12/29/2025,12/30/2025,EXAMPLE *Subscription,Shopping,Sale,-19.99,
```
- Amounts are negative for charges, positive for payments/refunds
- Has a `Category` column (Chase's auto-categorization — often inaccurate)
- `Type` field: Sale, Payment, Fee, Return, Adjustment

**Bilt Credit Card:**
```
"01/30/2026","-49.99","*","","EXAMPLE MERCHANT 8005551234 CA"
```
- Quoted fields, no column headers
- Columns: date, amount, unknown, unknown, description
- Amounts negative for charges, positive for payments
- Must add headers when parsing: `date,amount,flag1,flag2,description`

### Budget Framework (Recommended: Modified 50/30/20)

| Category | % | Notes |
|----------|---|-------|
| **Needs** | 50% | Rent, insurance, groceries, health, transport |
| **Wants** | 20% | Dining out, entertainment, shopping |
| **Debt + Savings** | 30% | CC payments above minimum, savings goals |

**Why modified 50/30/20:** Standard 50/30/20 puts 20% to savings. With active CC debt accruing interest, flipping the wants/savings ratios is better — attack debt aggressively while maintaining quality of life.

## Examples

**Example 1: Monthly Import & Report**
```
User: "Process the new Chase statement and show me January spending"
Claude: [Uses personal-finance] Analyzing Chase-Credit-Card.CSV...
- Loaded 52 transactions for January.
- Categorized 48 automatically (92%).
- Flagged 4 for review.

January Spending Report:
| Category        | Actual  | Budget  | Variance | Status |
|-----------------|---------|---------|----------|--------|
| Rent            | $X,XXX  | $X,XXX  | -$XX     | OK     |
| Subscriptions   | $XXX    | $XXX    | +$XX     | WATCH  |
| Groceries       | $XXX    | $XXX    | -$XX     | OK     |
| Dining Out      | $XXX    | $XXX    | -$XX     | OK     |
| Health          | $XXX    | $XXX    | -$XX     | OK     |
| Interest Charges| $XXX    | $0      | +$XXX    | ALERT  |

Debt Status: Interest cost you $XXX this month.
If you redirect $XXX/mo from cancelled subs to extra payments,
you'll save ~$XXX in interest over the next 12 months.
```

**Example 2: Subscription Audit**
```
User: "Run a subscription audit"
Claude: [Uses personal-finance + subscription-audit]

Active Monthly Recurring: $X,XXX/mo
(That's XX% of your net income on subscriptions alone)

Top 5 by cost: [from references/financial-profile.md]

Upcoming renewals to watch: [from the renewal calendar]
```

**Example 3: Debt Paydown Tracker**
```
User: "How's my debt paydown going?"
Claude: [Uses personal-finance]

Credit Card Debt Dashboard:
Card A: [========--------] $X,XXX remaining
Card B: [============----] $X,XXX remaining

This month: $X,XXX paid | $XXX interest charged
Net debt reduction: $X,XXX

At current pace: debt-free by [month/year]
If you add $200/mo extra: debt-free by [earlier month/year]
(Saved $X,XXX in interest)
```

## Core Workflows

### 1. The Drop-and-Analyze Pipeline

**Workflow:**
1. **Ingest:** Load CSVs from the finance folder
2. **Normalize:** Map Chase and Bilt formats to standard schema
3. **Categorize:** Apply regex rules (see below)
4. **Report:** Generate markdown summary to vault

**Standard schema:**
```csv
date,description,amount,category,source,type
2026-01-15,EXAMPLE MERCHANT,49.99,Health/Supplements,Bilt,subscription
2026-01-13,CLAUDE.AI SUBSCRIPTION,XXX.XX,AI Tools,Chase,subscription
```

### 2. Bank-Specific Parsers

**Chase parser:**
```python
import pandas as pd

def parse_chase(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['Transaction Date'])
    df['amount'] = df['Amount'].abs()
    df['is_charge'] = df['Amount'] < 0
    df['source'] = 'Chase'
    return df[['date', 'Description', 'amount', 'Category', 'Type', 'source', 'is_charge']]
```

**Bilt parser:**
```python
def parse_bilt(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, header=None,
                     names=['date', 'amount', 'flag1', 'flag2', 'description'],
                     quotechar='"')
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float).abs()
    df['is_charge'] = df['amount'] < 0  # Original value
    df['source'] = 'Bilt'
    return df[['date', 'description', 'amount', 'source', 'is_charge']]
```

### 3. Categorization Rules

The full owner-specific merchant map (40+ patterns tuned to real statements) lives in `references/financial-profile.md` (local-only). Representative structure:

```python
CATEGORY_MAP = {
    # Housing
    'Rent': r'BILT RENT|BPS\*BILT',
    'Insurance': r'INSURANCE',

    # AI / Dev / Creative tooling
    'AI Tools': r'CLAUDE\.AI|OPENAI|PERPLEXITY|ELEVENLABS',
    'Creative Tools': r'ADOBE|FIGMA|SUPABASE|GOOGLE \*Google One',

    # Daily life
    'Groceries': r'WHOLE\s?F[DO]S|TRADER JO|KEY FOOD|SAFEWAY|KROGER|ALDI',
    'Dining': r'TST\*|SQ \*|RESTAURANT|CAFE|COFFEE|STARBUCKS|PIZZ|CHIPOTLE',
    'Transport': r'UBER\s+\*TRIP|LYFT|MTA\*|AMTRAK|GAS|PARKING',
    'Food Delivery': r'UBER\s+\*EATS|DOORDASH|GRUBHUB',
    'Entertainment': r'DISNEY|HBO|MAX\.COM|NETFLIX|SPOTIFY',
    'Shopping': r'AMAZON',
    'Fitness': r'YMCA|GYM',

    # Fees
    'Interest/Fees': r'INTEREST CHARGE|LATE FEE|FOREIGN TRANSACTION',

    # Payments (credits)
    'Payment': r'Payment Thank You|AUTOMATIC PAYMENT|ONLINE ACH PAYMENT',
}
```

### 4. Anomaly Detection

```python
def detect_anomalies(df: pd.DataFrame, threshold=3.0) -> pd.DataFrame:
    """Flag transactions that are statistical outliers within their category."""
    stats = df.groupby('category')['amount'].agg(['mean', 'std'])
    df = df.merge(stats, on='category', how='left')
    df['z_score'] = ((df['amount'] - df['mean']) / df['std']).abs()
    anomalies = df[df['z_score'] > threshold].copy()
    return anomalies[['date', 'description', 'amount', 'category', 'z_score']]
```

**Autonomous mode:** Do NOT ask the user to review anomalies. Instead, output all anomalies as a structured markdown table in the report with a `## Flagged Anomalies` section. Tag each anomaly with a severity (HIGH: z>5, MEDIUM: z>3) and include the category average for context. The user will review the table asynchronously.

### 5. Reporting Templates

**Monthly report** — generate to `vault/Areas/Finance/monthly/`:
```markdown
# Financial Report: [Month Year]

## Summary
- **Net Income:** $X,XXX
- **Total Spend:** $X,XXX
- **Savings Rate:** XX%
- **Debt Payment:** $X,XXX (of which $XXX was interest)

## Category Breakdown
| Category | Actual | Budget | Variance | Status |
|----------|--------|--------|----------|--------|
| Rent | $X,XXX | $X,XXX | -$XX | OK |
...

## Subscription Tracker
- Active recurring: $X,XXX/mo
- Upcoming renewals: [list]

## Debt Dashboard
- Card A balance: $XX,XXX (interest: $XXX)
- Card B balance: $X,XXX (interest: $XX)
- Months to payoff at current rate: XX

## Action Items
- [ ] Review flagged transactions
- [ ] Check upcoming renewal: [service]
```

### 6. Debt Paydown Calculator

```python
def paydown_projection(balance: float, monthly_payment: float,
                       apr: float = 0.25) -> dict:
    """Project debt payoff timeline."""
    monthly_rate = apr / 12
    months = 0
    total_interest = 0

    while balance > 0:
        interest = balance * monthly_rate
        total_interest += interest
        principal = monthly_payment - interest
        if principal <= 0:
            return {'error': 'Payment does not cover interest'}
        balance -= principal
        months += 1

    return {
        'months_to_payoff': months,
        'total_interest_paid': round(total_interest, 2),
        'payoff_date': f'{months} months from now'
    }
```

### 7. Annual Renewal Calendar

Track renewal dates in `references/financial-profile.md` — set Google Calendar reminders when connected:

| Service | Renewal Date | Cost | Action |
|---------|-------------|------|--------|
| [service] | [month year] | $XXX | Evaluate — keep? |
| [service] | [month year] | $XXX | CANCEL before renewal |

### 8. Integration Patterns

**Vault:** Monthly reports to `vault/Areas/Finance/monthly/`, debt dashboard to `vault/Areas/Finance/debt-tracker.md`

**Google Sheets (via google-workspace MCP):** Export categorized transactions to a tracking spreadsheet for visual dashboards. Use `modify_sheet_values`, `create_spreadsheet_row`, etc.

**Future: Custom Rocket Money replacement app** — local-first or Cloudflare/Netlify hosted. The personal-finance skill provides the data pipeline; the UI is a separate project.

## Success Criteria

- [ ] Chase CSV parsed correctly (7 columns, negative amounts = charges)
- [ ] Bilt CSV parsed correctly (no headers, quoted fields)
- [ ] Regex patterns match >90% of transactions from real statements
- [ ] Monthly report generated with budget variance table
- [ ] Debt paydown projection calculates correct timeline
- [ ] Subscription list matches confirmed keep/cancel status
- [ ] Annual renewal dates tracked with reminder system
- [ ] Anomaly detection flags outliers correctly
- [ ] Reports output to vault as valid Markdown

## Copy/Paste Ready

```
"Analyze my latest Chase statement"
"Process the Bilt CSV"
"Monthly spending report"
"Run a subscription audit"
"How's my debt paydown going?"
"Am I over budget this month?"
"What subscriptions am I paying for?"
"Show my interest charges"
"Compare this month vs last month"
"What's renewing soon?"
```
