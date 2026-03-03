---
name: personal-finance
description: Personal finance automation assistant. Import CSV bank exports from Chase and Bilt, categorize transactions via regex, generate monthly spending reports, track credit card debt paydown, audit subscriptions, and manage budget targets. Use this skill when the user mentions "budget", "expenses", "spending report", "categorize transactions", "credit card", "debt paydown", "subscription audit", "how much did I spend", or uploads CSV bank statements.
---

# Personal Finance Automation

## Purpose

Sean's personal finance command center. Processes Chase and Bilt CSV exports into categorized spending reports, tracks credit card debt paydown progress, manages subscription costs, and generates actionable budget insights. First-time budgeter — the skill provides structure, gamification, and clear visual progress toward financial goals.

## When to Use

- **Processing Statements:** "Analyze my latest Chase CSV" / "Process the new Bilt export"
- **Reporting:** "Monthly spending report" / "Where did my money go?"
- **Debt Tracking:** "How's my credit card paydown going?" / "Interest charges this month?"
- **Subscriptions:** "Run a subscription audit" / "What am I paying for?"
- **Budgeting:** "Am I over budget on dining?" / "Show my budget variance"
- **Savings Goals:** "How much have I saved toward the ring?" / "Cannes trip fund status"

## Sean's Financial Profile

### Income

- **Gross:** $4,166.67/semi-monthly ($8,333.34/month, ~$100K/year)
- **Net take-home:** $2,870.63/semi-monthly (**$5,741.26/month**)
- **Employer:** The Block (paid via Rippling)
- **Deductions:** Medical, dental, vision, life, disability, taxes (NY state + NYC)
- **Note:** NY taxes will shift to MA after Boston move (March 21, 2026). Tax withholding change pending HR.

### Accounts

| Account | Bank | Limit/Type | Primary Use |
|---------|------|------------|-------------|
| Chase Credit Card | Chase | $27,000 limit | Primary spending card |
| Bilt Credit Card | Bilt | $6,000 limit | Rent payments (earns points on rent) |
| Chase Checking | Chase | Checking | Primary bank account |
| Chase Savings | Chase | Savings | Not actively used yet |

### CSV Formats

**Chase Credit Card:**
```
Transaction Date,Post Date,Description,Category,Type,Amount,Memo
12/29/2025,12/30/2025,GOOGLE *Google One,Shopping,Sale,-272.18,
```
- Amounts are negative for charges, positive for payments/refunds
- Has a `Category` column (Chase's auto-categorization — often inaccurate)
- `Type` field: Sale, Payment, Fee, Return, Adjustment

**Bilt Credit Card:**
```
"01/30/2026","-134.97","*","","SEED.COM 8446463586 CA"
```
- Quoted fields, no column headers
- Columns: date, amount, unknown, unknown, description
- Amounts negative for charges, positive for payments
- Must add headers when parsing: `date,amount,flag1,flag2,description`

### Active Subscriptions (as of Feb 2026)

**Keep:**
| Service | ~Monthly Cost | Category | Notes |
|---------|-------------|----------|-------|
| Claude.AI | $217.75 | AI Tools | Max plan |
| Perplexity AI | $200.00 | AI Tools | Max plan |
| ElevenLabs | $19.96 | AI Tools | $239.53 annual (renews May 2026) |
| Nate AI News | $20.00 | Professional | AI + PM insights |
| Adobe Creative Cloud | $32.00 | Creative | Split with friend (full price $65.31) |
| Google One | $136-272 | Cloud/AI | 30TB storage, Veo 3.1, AI Studio |
| Figma | $17.42 | Creative | $209 annual |
| Supabase | $25-35 | Dev Tools | For 16BitFit project |
| Seed.com | $134.97 | Health | Gut health supplement |
| Gray Matter Co | $45-50 | Health | Supplements |
| L Conscious | $95-211 | Health | Varies monthly |
| Medvidi | $79.50 | Health | $159 every 2 months — transitioning to Aetna in Boston |
| Rosebank Pharmacy | $6.00 | Health | $12 every 2 months — prescriptions |
| AP Vape Shop | $141-170 | Lifestyle | Keep for now, planning to quit |
| Amazon Prime | $2.99 | Shopping | Via Bilt |
| Apple.com | $2.99 | Services | Via Bilt |
| Disney+ | $15.83 | Entertainment | $189.99 annual, split with cousin |
| HBO Max | $170 | Entertainment | Annual — will split with girlfriend |
| FantasyPros | $54 | Entertainment | Seasonal (Aug-Dec football only) |

**Cancelling Soon:**
| Service | ~Monthly Cost | Action |
|---------|-------------|--------|
| Suno Inc | $10 | Cancel this month, find open-source |
| Gamma.app | $91-96 | Cancel before next renewal |
| YMCA | $50 | Cancel when switching to new gym ($100-120) |
| Lemonade Insurance | $126 | Cancel after Boston move |
| LinkedIn Premium | $261.17 | Annual — cancel next renewal (Jan 2027) |
| Meshy | $10 | Annual $120 — cancel before renewal (Aug 2026) |
| Lottiefiles | $20 | Annual $239.88 — cancel before renewal (Oct 2026) |
| Boss Foundry | $17 | Should be cancelled — Chase dispute active |

**Already Cancelled:**
Midjourney, Hailuo AI Video, Runway Pro, Codia, MagicPath AI, OpenAI ChatGPT, Cursor AI, XAI/Grok, Unicorn Studio, Carlyagar Training, Product Compass PM, Botanic Tonics, Paramount+, Codecademy, Aspireship, TealHQ, Mobbin

### Financial Goals (Priority Order)

1. **Reduce credit card debt** — interest charges averaging ~$200/mo on Chase + $50-90/mo on Bilt. This is the #1 priority.
2. **Build emergency fund** — target 3 months expenses in Chase Savings
3. **Save for engagement ring** — no timeline yet, post-debt-paydown
4. **Save for house down payment** — no timeline yet, post-ring
5. **Cannes, France trip** — September 21, 2026 (friend's wedding + Paris extension)

### Budget Framework (Recommended: Modified 50/30/20)

First-time budgeter. Based on $5,741/mo net income:

| Category | % | Monthly Target | Notes |
|----------|---|---------------|-------|
| **Needs** | 50% | $2,870 | Rent, insurance, groceries, health, transport |
| **Wants** | 20% | $1,148 | Dining out, entertainment, shopping |
| **Debt + Savings** | 30% | $1,723 | CC payments above minimum, savings goals |

**Why modified 50/30/20:** Standard 50/30/20 puts 20% to savings. But with active CC debt accruing ~$250/mo in interest, flipping the wants/savings ratios is better — attack debt aggressively while maintaining quality of life.

## Examples

**Example 1: Monthly Import & Report**
```
User: "Process the new Chase statement and show me January spending"
Claude: [Uses personal-finance] Analyzing Chase-Credit-Card-2025.CSV...
- Loaded 52 transactions for January.
- Categorized 48 automatically (92%).
- Flagged 4 for review.

January Spending Report:
| Category        | Actual  | Budget  | Variance | Status |
|-----------------|---------|---------|----------|--------|
| Rent (Bilt)     | $2,161  | $2,200  | -$39     | OK     |
| Subscriptions   | $847    | $800    | +$47     | WATCH  |
| Groceries       | $312    | $400    | -$88     | OK     |
| Dining Out      | $186    | $200    | -$14     | OK     |
| Health          | $289    | $300    | -$11     | OK     |
| Interest Charges| $159    | $0      | +$159    | ALERT  |

Debt Status: Interest cost you $159 this month.
If you redirect the $115/mo from cancelled subs to extra payments,
you'll save ~$840 in interest over the next 12 months.
```

**Example 2: Subscription Audit**
```
User: "Run a subscription audit"
Claude: [Uses personal-finance + subscription-audit]

Active Monthly Recurring: $1,143 - $1,487/mo
(That's 20-26% of your net income on subscriptions alone)

Top 5 by cost:
1. Google One: $136-272
2. Claude.AI: $217.75
3. Perplexity: $200
4. AP Vape: $141-170
5. Seed.com: $135

Upcoming renewals to watch:
- May 2026: ElevenLabs ($240 annual)
- Aug 2026: Meshy ($120 annual) — CANCEL before this
- Oct 2026: Lottiefiles ($240 annual) — CANCEL before this
- Jan 2027: LinkedIn Premium ($261) — CANCEL before this
```

**Example 3: Debt Paydown Tracker**
```
User: "How's my debt paydown going?"
Claude: [Uses personal-finance]

Credit Card Debt Dashboard:
Chase:  [========--------] $X,XXX remaining
Bilt:   [============----] $X,XXX remaining

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
2026-01-15,SEED.COM,134.97,Health/Supplements,Bilt,subscription
2026-01-13,CLAUDE.AI SUBSCRIPTION,217.75,AI Tools,Chase,subscription
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

### 3. Categorization Rules (Sean-Specific)

```python
CATEGORY_MAP = {
    # Housing
    'Rent': r'BILT RENT|BPS\*BILT',
    'Insurance': r'LEMONADE|INSURANCE',

    # AI Tools
    'AI Tools': r'CLAUDE\.AI|OPENAI|PERPLEXITY|CURSOR|MIDJOURNEY|HAILUO|SUNO|XAI LLC|ELEVENLABS|CODIA|MAGICPATH|RUNWAY',

    # Creative/Dev
    'Creative Tools': r'ADOBE|FIGMA|UNICORN\s?STUDIO|GAMMA\.APP|SUPABASE|GOOGLE \*Google One|GOOGLE \*CLOUD',

    # Health/Supplements
    'Health/Supplements': r'SEED\.COM|GRAYMATTERCO|BOTANIC TONICS|MEDVIDI|ROSEBANK PHARMACY|LCONSCIOUS|PRIMAL HARV|TRANSPARENT LABS|BUCKED UP|CALMING CO|CREATE WELLNESS|CLUB EARLYBIRD|1MD|NEUROGUM',

    # Professional
    'Professional': r'CARLYAGAR|BOSS FOUNDRY|PRODUCT\s?COMPASS|NATE AI|ASPIRESHIP|BOSS FOUNDRY|PARCHMENT|WAWALLAMA',

    # Groceries
    'Groceries': r'WESTERN BEEF|WHOLE\s?F[DO]S|TRADER JO|KEY FOOD|PALM GRILL|CONVENIENCE|SAFEWAY|KROGER|ALDI|TRIBECA FINEST|FAMILY DOLLAR',

    # Dining
    'Dining': r'TST\*|SQ \*|RESTAURANT|TAVERN|BREWERY|BAR|GRILL|CAFE|COFFEE|STARBUCKS|DINER|PIZZ|CHIPOTLE|SUSHI|DISHOOM|PRET A MANGER',

    # Transport
    'Transport': r'UBER\s+\*TRIP|LYFT|MTA\*|AMTRAK|UNITED|DELTA|CITGO|SPEEDWAY|WAWA|QUICK CHEK|GAS|PARKING',
    'Food Delivery': r'UBER\s+\*EATS|DOORDASH|GRUBHUB',

    # Entertainment
    'Entertainment': r'DISNEY|PARAMOUNT|HBO|MAX\.COM|NETFLIX|SPOTIFY|NFL\.COM|FANTASYPROS|21-DRAW|KLINGAI|MFA\s+Boston',

    # Shopping
    'Shopping': r'AMAZON|HARRODS|FAMILY DOLLAR|CITY MARKET',

    # Vape
    'Vape': r'AP VAPE',

    # Fitness
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

### 5. Reporting Templates

**Monthly report** — generate to `vault/Areas/Finance/monthly/`:
```markdown
# Financial Report: [Month Year]

## Summary
- **Net Income:** $5,741
- **Total Spend:** $X,XXX
- **Savings Rate:** XX%
- **Debt Payment:** $X,XXX (of which $XXX was interest)

## Category Breakdown
| Category | Actual | Budget | Variance | Status |
|----------|--------|--------|----------|--------|
| Rent | $2,161 | $2,200 | -$39 | OK |
...

## Subscription Tracker
- Active recurring: $X,XXX/mo
- Upcoming renewals: [list]

## Debt Dashboard
- Chase balance: $XX,XXX (interest: $XXX)
- Bilt balance: $X,XXX (interest: $XX)
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

Track these dates — set Google Calendar reminders when connected:

| Service | Renewal Date | Cost | Action |
|---------|-------------|------|--------|
| ElevenLabs | May 2026 | $240 | Evaluate — keep? |
| Meshy | Aug 2026 | $120 | CANCEL before renewal |
| FantasyPros | Aug 2026 | $54 | Re-activate for football season |
| Disney+ | Oct 2026 | $190 | Keep (split with cousin) |
| Lottiefiles | Oct 2026 | $240 | CANCEL before renewal |
| HBO Max | ~Apr 2027 | $170 | Split with girlfriend |
| LinkedIn Premium | Jan 2027 | $261 | CANCEL before renewal |
| Figma | ~Jun 2027 | $209 | Keep |

### 8. Integration Patterns

**Vault:** Monthly reports to `vault/Areas/Finance/monthly/`, debt dashboard to `vault/Areas/Finance/debt-tracker.md`

**Google Sheets (via google-workspace MCP):** Export categorized transactions to a tracking spreadsheet for visual dashboards. Use `modify_sheet_values`, `create_spreadsheet_row`, etc.

**Future: Custom Rocket Money replacement app** — local-first or Cloudflare/Netlify hosted. The personal-finance skill provides the data pipeline; the UI is a separate project.

## Success Criteria

- [ ] Chase CSV parsed correctly (7 columns, negative amounts = charges)
- [ ] Bilt CSV parsed correctly (no headers, quoted fields)
- [ ] Regex patterns match >90% of transactions from Sean's actual statements
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