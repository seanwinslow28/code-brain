---
name: data-analysis
description: Data analysis and reporting assistant for The Block's Product & Engineering team. Processes GA4 analytics, builds metric reports, analyzes article CTR, data page sources, and ad revenue. Accesses GA4 via Zapier MCP, Looker via browser, and Jira for sprint data. Use when asked to "analyze data", "create a report", "review metrics", "process CSV", "trend analysis", "build a dashboard", "GA4", "Looker", "impressions", "page views", or "ad revenue".
---

# Data Analysis & Reporting — The Block

## Purpose

Enables Sean to analyze The Block's key metrics, build reports for stakeholders, and answer Ed's analytics questions — all without admin-level tool access. Uses GA4 via Zapier MCP for data extraction, Python (pandas) for analysis, and Confluence/Slack for report distribution. Covers article performance, data page engagement, ad revenue, and Campus analytics (coming soon).

## When to Use

- **Metrics:** "What are our page views this week?" / "Article CTR report"
- **Reports:** "Create a monthly metrics report" / "Generate a bi-weekly analytics summary"
- **Analysis:** "Where are users dropping off?" / "Which content types retain users?"
- **GA4:** "Pull GA4 data for [metric]" / "Analyze traffic sources"
- **Ad Hoc:** "What's the average [metric] from this CSV?"

## Sean's Analytics Context

### Tools Access

| Tool | Access Level | How to Use |
|------|-------------|------------|
| GA4 | View access (no admin) | Zapier MCP: `google_analytics_4_run_report_for_a_property` |
| Looker | View access (no admin/API) | Browser only — export CSV, then analyze with Claude |
| Jira | Full access | `mcp-atlassian`: `jira_search` (preferred) or `claude.ai Atlassian` |
| Google Sheets | Full access | `google-workspace`: `read_sheet_values`, `modify_sheet_values` (preferred) or Zapier fallback |

**Key constraint:** No API keys for GA4 or Looker. Zapier MCP bridges GA4 (no native GA4 MCP exists). Looker data must be exported as CSV first. Google Sheets now has native access via `google-workspace` MCP.

### Key Metrics Sean Tracks

| Category | Metrics | Source |
|----------|---------|--------|
| Content | Page views, impressions, article CTR | GA4 |
| Data Pages | Page views, exit rate, source analysis | GA4 |
| Advertising | Ad revenue, ad impressions, click rates | GAM / GA4 |
| Campus | Enrollment, completion rates, quiz scores | Campus LMS (future) |
| SEO | Organic search traffic, page indexing | GA4 / Search Console |

### Ed's Analytics Questions

These are the types of questions Ed asks Sean to investigate:

1. **Article Click-Through Rate:** "Do people click on another article after reading one, or just come to one article and leave?"
2. **Data Page Source Analysis:** "Do people come to data pages mainly through Google search? Do they exit immediately after viewing charts?"
3. **Referring URL Tracking:** "Where were people before they clicked on this page? What is the referring URL?"
4. **Content Type Performance:** "What happens with articles vs homepage vs data pages? Which content types retain users?"
5. **Cross-Content Navigation:** "Are users interested in related articles on data/chart pages?"
6. **User Journey Path:** "What is the full sequence: Source → Landing Page → Page 2 → Page 3 → Exit?"

### Reporting Flow

**Who Sean reports to:** Ed Rupkus (PM)
**Ed reports to:** Matt Vitebsky (VP of P&E) → broader leadership
**Format:** Confluence write-up → Slack summary with link
**Frequency:** Ad hoc now; will increase when Campus 201 goes fully live

## Examples

**Example 1: GA4 Data Pull via Zapier**
```
User: "Pull this week's article page views from GA4"
Claude: [Uses data-analysis]

Using Zapier MCP to query GA4...

[Calls google_analytics_4_run_report_for_a_property with:
  - dimensions: pagePath, date
  - metrics: screenPageViews
  - dateRange: last 7 days
  - filter: pagePath contains "/post/"]

Results:
| Date | Top Articles | Views |
|------|-------------|-------|
| Feb 17 | /post/bitcoin-etf-record-inflows | 12,450 |
| Feb 17 | /post/sec-crypto-regulation-2026 | 8,230 |
...

Total article views this week: 87,420 (+12% WoW)
```

**Example 2: Looker CSV Analysis**
```
User: "Analyze this Looker export" [attaches CSV]
Claude: [Uses data-analysis]

Processing LMAX-ad-stats-export.csv...

Summary:
- Date range: Jan 1 - Feb 15, 2026
- Total impressions: 2.4M
- Total clicks: 18,200
- CTR: 0.76%
- Revenue: $34,500

Trend: CTR declining week-over-week since Jan 20.
Recommendation: Review ad placement on Nuxt 4 pages —
migration may have affected above-the-fold visibility.
```

**Example 3: Article CTR Deep Dive**
```
User: "Are people clicking on related articles or bouncing?"
Claude: [Uses data-analysis]

Pulling GA4 engagement data...
[Queries: engaged sessions, pages per session, avg engagement time
 filtered by pagePath containing "/post/"]

Results:
- Avg pages per session (article entry): 1.4
- Bounce rate (articles): 72%
- Related article click rate: 8.3%

Insight: Most users read one article and leave.
The 28% who stay view an average of 2.8 pages.
Related article modules drive the majority of internal navigation.

Recommendation: Test more prominent related article placement
to push pages-per-session above 1.5.
```

## Core Workflows

### 1. GA4 via Zapier MCP

**Available tool:** `google_analytics_4_run_report_for_a_property`

**Common queries:**

```python
# Article performance
dimensions = ["pagePath", "date"]
metrics = ["screenPageViews", "averageSessionDuration", "bounceRate"]
filter = "pagePath contains '/post/'"

# Data page analysis
dimensions = ["pagePath", "sessionSource"]
metrics = ["screenPageViews", "exits"]
filter = "pagePath contains '/data/'"

# Traffic sources
dimensions = ["sessionSource", "sessionMedium"]
metrics = ["sessions", "newUsers"]

# Referring URLs
dimensions = ["pageReferrer", "pagePath"]
metrics = ["sessions"]
```

**Looker dashboard reference:**
- LMAX ad statistics: `https://lookerstudio.google.com/reporting/d6b93529-847b-458f-aa0b-8e080ee8046b`

### 2. Analysis Pipeline

Always use Python (pandas) for calculations. Never estimate in your head.

```python
import pandas as pd
import json

def analyze_csv(filepath: str, question: str) -> dict:
    """Standard analysis pipeline for any CSV data."""
    df = pd.read_csv(filepath)

    # Step 1: Understand the data
    info = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': {str(k): str(v) for k, v in df.dtypes.items()},
        'nulls': df.isnull().sum().to_dict(),
    }

    # Step 2: Basic stats
    stats = {}
    for col in df.select_dtypes(include='number').columns:
        stats[col] = {
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
        }

    return {'info': info, 'stats': stats}
```

### 3. Report Templates

**Weekly Metrics Report (for Confluence):**

```markdown
# Weekly Metrics Report: [Week]

## Summary
[2-3 sentences on the week's story]

## Key Metrics
| Metric | Last Week | This Week | WoW Change |
|--------|-----------|-----------|-----------|
| Article Page Views | [value] | [value] | [+/-]% |
| Data Page Views | [value] | [value] | [+/-]% |
| Article CTR | [value] | [value] | [+/-]pp |
| Ad Revenue | $[value] | $[value] | [+/-]% |

## Notable Changes
- [Metric that moved significantly and why]

## Recommended Actions
- [Data-driven recommendation]
```

**Monthly Deep Dive (for Ed/Matt):**

```markdown
# Monthly Analytics: [Month Year]

## Content Performance
- Total page views: [X]
- Article vs data page split: [X%] / [X%]
- Top 5 articles by views: [list]
- Bounce rate trend: [improving/declining]

## Traffic Sources
| Source | Sessions | % of Total | Trend |
|--------|----------|-----------|-------|
| Organic Search | [X] | [X%] | [up/down] |
| Direct | [X] | [X%] | [up/down] |
| Social | [X] | [X%] | [up/down] |
| Referral | [X] | [X%] | [up/down] |

## Ad Performance
- Total ad revenue: $[X]
- Ad CTR: [X%]
- Top-performing ad placements: [list]

## Campus (when live)
- Enrollments: [X]
- Completion rate: [X%]
- Revenue: $[X]
```

### 4. Visualization

For static reports, use matplotlib:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df["date"], df["page_views"], marker="o")
ax.set_title("Article Page Views — Weekly Trend")
ax.set_xlabel("Date")
ax.set_ylabel("Page Views")
fig.savefig("article-views-trend.png", dpi=150, bbox_inches="tight")
```

For interactive dashboards, generate self-contained HTML with Chart.js.

### 5. Distribution

After generating a report:
1. **Write to Confluence** — Full report with charts
2. **Post to Slack** — Summary (3-4 bullet points) + Confluence link
3. **Save to vault** — `vault/Areas/Work/analytics/[report-name].md`

## Verification Rules

1. **Show your work:** Always output the Python code or Zapier MCP call used
2. **Sanity check:** Compare results against known baselines
3. **Precision:** Use code execution for math, never mental calculation
4. **Null handling:** Report how many null/missing values were excluded
5. **Outlier awareness:** Report median alongside mean when data is skewed

## Success Criteria

- [ ] GA4 data pulled via Zapier MCP (not manual export)
- [ ] All calculations performed via Python code
- [ ] Reports formatted for Confluence distribution
- [ ] Slack summary generated alongside full report
- [ ] Ed's 6 analytics question types answerable
- [ ] Visualizations use appropriate chart types
- [ ] Null values and outliers explicitly handled
- [ ] Campus analytics ready for when Campus 201 launches publicly

## Copy/Paste Ready

```
"Pull GA4 article page views for this week"
"Analyze this Looker CSV export"
"Create a monthly metrics report"
"Where are users coming from on data pages?"
"What's our article bounce rate trend?"
"Build an ad revenue report for Ed"
"Analyze traffic sources by content type"
"What's the user journey from article to article?"
```