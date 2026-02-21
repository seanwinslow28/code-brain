---
name: personal-finance
description: Personal finance automation assistant. Import CSV bank exports, categorize transactions via regex, generate monthly spending reports (markdown/HTML), and track budget variance. Use this skill when the user mentions "budget", "expenses", "spending report", "categorize transactions", or uploads CSV bank statements.
---

# Personal Finance Automation

## Purpose

Automate personal financial tracking by processing raw CSV bank exports into structured reports. This skill eliminates manual data entry, ensures consistent categorization via regex rules, and produces action-oriented spending analysis (Variance Reports, Anomaly Detection).

## When to Use

- **Processing Statements:** When you drop a new CSV export (bank/credit card) into the `/data` folder.
- **Reporting:** When you need a "Monthly Variance Report" or "Year-to-Date Summary."
- **Analysis:** When you ask "Where did my money go?" or "Am I over budget on dining?"
- **Categorization:** When you need to classify a list of raw transaction descriptions.

## Examples

**Example 1: Monthly Import & Report**
```
User: "Process the new Chase statement in /data/inbox and show me the April spending report."
Claude: [Uses personal-finance] I've analyzed `Chase_Apr.csv`.
- Loaded 45 transactions.
- Categorized 42 transactions automatically (93%).
- Flagged 3 uncategorized items for review.

Here is your **April Variance Report**:

| Category | Actual | Budget | Variance | Status |
| :--- | :--- | :--- | :--- | :--- |
| Housing | $2,500 | $2,500 | $0 | ✅ |
| Dining | $850 | $500 | +$350 | 🚨 |
...
```

**Example 2: Anomaly Check**
```
User: "Check my credit card csv for any weird charges."
Claude: [Uses personal-finance] Running anomaly detection (Z-score analysis) on `transactions.csv`...

🚨 **Found 2 Potential Anomalies:**
1. **$1,200.00 at Apple** (May 12) - This is 4σ above your average "Shopping" transaction ($85).
2. **$14.99 at Unidentified_Sub** (May 14) - New recurring merchant detected.
```

## Finance Automation Workflow

### 1. The "Drop-and-Analyze" Pipeline

Do not manually edit CSVs. Use the `analyze_spending.py` script to standardize, categorize, and report on raw data.

**Workflow:**
1.  **Ingest:** Load all CSVs from `data/inbox/`.
2.  **Normalize:** distinct bank formats -> standard `date`, `amount`, `description` columns.
3.  **Categorize:** Apply regex rules from `references/category_patterns.md`.
4.  **Report:** Generate markdown summary.

To run the full analysis:
```bash
python3 scripts/analyze_spending.py --input data/inbox --output reports/april_summary.md
```

### 2. Categorization Logic (Regex Map)

Use strictly defined regex patterns to map merchant strings to categories.
For the complete list of 50+ common merchant patterns, see `references/category_patterns.md`.

```typescript
// Example Typings for Categorization
interface Transaction {
  date: Date;
  amount: number;
  description: string;
  category?: string;
}

const CATEGORY_MAP: Record<string, RegExp> = {
  'Housing': /rent|mortgage|hoa|con\s?ed|utilities/i,
  'Transport': /uber|lyft|mta|parking|gas|shell|citibike/i,
  'Groceries': /whole\s?fds|trader\s?joes|safeway|kroger|aldi/i,
  'Dining': /doordash|ubereats|starbucks|chipotle|cafe|restaurant/i,
  'Subscriptions': /netflix|spotify|aws|github|digitalocean|apple\s?serv/i
};
```

### 3. Anomaly Detection (Z-Score)

Use this pattern to find outliers in a DataFrame without manual review.

```python
import pandas as pd

def detect_anomalies(df: pd.DataFrame, threshold=3.0) -> pd.DataFrame:
    """
    Identifies transactions that are statistical outliers within their category.
    """
    if 'category' not in df.columns:
        return pd.DataFrame()

    # Calculate mean and std deviation per category
    stats = df.groupby('category')['amount'].agg(['mean', 'std'])
    df = df.merge(stats, on='category', how='left')
    
    # Calculate Z-score: (x - mean) / std
    df['z_score'] = ((df['amount'] - df['mean']) / df['std']).abs()
    
    # Filter
    anomalies = df[df['z_score'] > threshold].copy()
    return anomalies[['date', 'description', 'amount', 'category', 'z_score']]
```

### 4. Reporting Template (Markdown)

Generate reports using this strict format to ensuring readability.

```markdown
## 💸 Financial Report: [Date Range]

**Total Spend:** $[Total]
**Savings Rate:** [Rate]%

### Category Breakdown
| Category | Amount | % of Total | Trend |
| :--- | :--- | :--- | :--- |
| **Housing** | $[Amt] | [XX]% | ➖ |
| **Dining** | $[Amt] | [XX]% | ⬆️ |

### 🚨 Anomalies & Review
- [ ] [Date]: [Merchant] ($[Amount]) - Verify this charge.
- [ ] [Date]: [Merchant] ($[Amount]) - Uncategorized.
```

## Success Criteria

- [ ] Script successfully normalizes columns (Date -> date, etc.) from at least 2 different bank formats.
- [ ] Regex patterns match >90% of a standard test dataset.
- [ ] Anomaly detection correctly identifies large outliers.
- [ ] Reports generated are valid Markdown tables.

## Copy/Paste Ready

```
"Analyze the new statement in /inbox and flag any anomalies."
"Update my spending report for this month."
"Categorize these transactions and show me the breakdown."
```
