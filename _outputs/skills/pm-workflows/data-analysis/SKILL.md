---
name: data-analysis
description: Data analysis and reporting assistant for product managers. Processes CSV and JSON files, generates metrics reports, identifies trends, creates visualizations, and integrates with analytics tools. Use when asked to analyze data, create a report, review metrics, process CSV files, do trend analysis, or build a dashboard.
---

# Data Analysis and Reporting

## Purpose

Enable non-data-scientists to perform meaningful data analysis using Claude Code. Process CSV/JSON files, generate metric reports, identify trends, create visualizations, and automate recurring reporting workflows. Execute analysis through Python scripts for mathematical precision rather than approximation.

## When to Use

- User asks to analyze a CSV, JSON, or data file
- User needs a metrics report (weekly, monthly, quarterly)
- User wants to identify trends in data
- User asks to create charts or visualizations
- User wants to integrate with analytics tools (GA4, Looker)
- User needs help interpreting experiment results or funnel data

## Examples

**Example 1: CSV funnel analysis**
```
User: "Analyze activation-funnel-q4.csv and tell me where users are dropping off"
Claude: [Uses data-analysis] I'll write a Python script to process the funnel data:

Funnel Analysis Results:
| Step | Users | Drop-off | Rate |
|------|-------|----------|------|
| Signup | 10,000 | - | 100% |
| Onboarding | 6,200 | 3,800 | 62% |
| First Action | 2,480 | 3,720 | 40% |
| Activation | 1,240 | 1,240 | 50% |

Biggest drop: Signup -> Onboarding (38% loss)
Recommendation: Investigate onboarding UX. Segment by company_size for deeper insight.
```

**Example 2: Trend report**
```
User: "Create a monthly metrics report from this data"
Claude: [Uses data-analysis]

# Monthly Metrics Report: January 2026

## Key Metrics
| Metric | Dec | Jan | MoM Change |
|--------|-----|-----|-----------|
| MAU | 45,200 | 48,100 | +6.4% |
| Avg Session | 4.2m | 4.8m | +14.3% |
| Churn Rate | 3.1% | 2.8% | -0.3pp |

## Trends
- User growth accelerating (was +3.2% in Dec)
- Session duration correlates with new dashboard feature launch
- Churn improving since support chat integration

[Saves report.md and generates charts as chart.html]
```

**Example 3: Quick data question**
```
User: "What's the average order value from this sales CSV?"
Claude: [Uses data-analysis] Processing sales-data.csv...

Average Order Value: $127.45
Median: $89.00 (skewed by 3 enterprise orders >$1000)
Range: $12.00 - $4,500.00
Total Orders: 1,847
```

## Analysis Workflow

### Step 1: Understand the Data

Before analyzing, inspect the file:

```python
import pandas as pd

df = pd.read_csv("data.csv")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(df.dtypes)
print(df.describe())
print(df.head())
```

Ask the user what question they want answered. Do not assume the analysis goal.

### Step 2: Choose the Right Approach

| Data Size | Approach |
|-----------|----------|
| <100 rows | Read directly, analyze in context |
| 100-10,000 rows | Write Python script with Pandas, return summary |
| >10,000 rows | Write Python script, return only aggregated results |

For large files, never load the full dataset into the chat context. Write a script that processes the data and outputs only the relevant summary.

### Step 3: Execute Analysis

Write and run a Python script. Always use Pandas for data manipulation:

```python
import pandas as pd
import json

# Load data
df = pd.read_csv("input.csv")

# Clean
df["date"] = pd.to_datetime(df["date"])
df = df.dropna(subset=["revenue"])

# Analyze
summary = {
    "total_revenue": float(df["revenue"].sum()),
    "avg_revenue": float(df["revenue"].mean()),
    "median_revenue": float(df["revenue"].median()),
    "count": len(df),
    "date_range": f"{df['date'].min()} to {df['date'].max()}"
}

# Output
print(json.dumps(summary, indent=2))
```

### Step 4: Visualize (When Requested)

Choose the right chart type:

| Data Pattern | Chart Type | Tool |
|-------------|-----------|------|
| Trend over time | Line chart | matplotlib or Chart.js |
| Category comparison | Bar chart | matplotlib or Chart.js |
| Proportions | Pie/donut chart | Chart.js |
| Correlation | Scatter plot | matplotlib |
| Funnel stages | Funnel chart | Custom HTML |
| Distribution | Histogram | matplotlib |
| Cohort retention | Heatmap | seaborn |

For static reports, use matplotlib:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df["date"], df["revenue"], marker="o")
ax.set_title("Revenue Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Revenue ($)")
fig.savefig("revenue-trend.png", dpi=150, bbox_inches="tight")
```

For interactive dashboards, generate self-contained HTML with Chart.js:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <canvas id="chart"></canvas>
  <script>
    const ctx = document.getElementById("chart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: [/* dates */],
        datasets: [{
          label: "Revenue",
          data: [/* values */],
          borderColor: "#1A1A2E",
          tension: 0.1
        }]
      }
    });
  </script>
</body>
</html>
```

## Report Templates

### Weekly Metrics Report

```markdown
# Weekly Metrics Report: [Week]

## Summary
[2-3 sentences on the week's story]

## Key Metrics
| Metric | Last Week | This Week | WoW Change |
|--------|-----------|-----------|-----------|
| [KPI 1] | [Value] | [Value] | [+/-] |

## Notable Changes
- [Metric that moved significantly and why]

## Recommended Actions
- [Data-driven recommendation]
```

### Experiment Analysis (A/B Test)

```markdown
# Experiment Report: [Test Name]

## Setup
- **Hypothesis:** [What we expected]
- **Control:** [Description]
- **Variant:** [Description]
- **Duration:** [Days] | **Sample:** [Users per group]

## Results
| Metric | Control | Variant | Lift | p-value |
|--------|---------|---------|------|---------|
| [Primary] | [Value] | [Value] | [%] | [Value] |

## Statistical Significance
[Significant / Not significant at 95% confidence]

## Recommendation
[Ship / Iterate / Kill]
```

## Analytics Integration

### Looker via MCP

Create a skill that maps natural language to LookML:

1. Define business terms in the skill (e.g., "Revenue = recognized_revenue, not invoiced")
2. Map questions to specific Explores and dimensions
3. Execute queries and format results

### GA4 via Python Script

```python
# Write a script to hit the GA4 API
# Save results as CSV for local analysis
# Example: traffic sources by week
```

### Database via MCP

Connect to Postgres/Supabase via MCP. Claude can:
1. Inspect schema (`list_tables`)
2. Write SQL queries
3. Execute and interpret results

## Verification Rules

For any numerical analysis:

1. **Show your work:** Always output the Python code used
2. **Sanity check:** Compare results against known baselines
3. **Precision:** Use code execution for math, never mental calculation
4. **Null handling:** Report how many null/missing values were excluded
5. **Outlier awareness:** Report median alongside mean when data is skewed

## Success Criteria

- [ ] Analysis answers the user's specific question
- [ ] All calculations performed via code (not approximated)
- [ ] Null values and outliers explicitly handled and reported
- [ ] Visualizations use appropriate chart types for the data
- [ ] Reports include actionable recommendations, not just numbers
- [ ] Data sources and methodology are documented
- [ ] Output saved to files (markdown report, charts, processed data)

## Copy/Paste Ready

```
"Analyze this CSV and show me the key trends"
"Create a weekly metrics report from this data"
"What's the conversion rate from this funnel data?"
"Build an interactive dashboard from these numbers"
"Run an A/B test analysis on experiment-results.csv"
"Generate a quarterly business review from our metrics"
```
