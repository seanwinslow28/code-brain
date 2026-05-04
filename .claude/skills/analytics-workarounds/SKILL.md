---
name: analytics-workarounds
description: Analytics data access workarounds for PMs without direct tool access. Uses Zapier MCP as a data bridge from GA4, Looker, and BigQuery to Google Sheets for analysis. Use when user says "pull analytics", "GA4 workaround", "get metrics without Looker access", "analytics pipeline", or "data bridge".
---

# Analytics Workarounds

## Purpose

Enable product managers to access, analyze, and report on analytics data even when they lack direct access to tools like GA4, Looker, or BigQuery. Uses Zapier MCP as a data bridge to extract metrics into Google Sheets, then analyzes with Claude.

## When to Use

- You need GA4 data but don't have direct console access
- Looker dashboards are admin-gated and you need metrics now
- Building a recurring analytics pipeline without engineering help
- Pulling data for a stakeholder update or sprint review
- Comparing metrics across time periods for trend analysis

## Examples

**Example 1: GA4 via Zapier MCP**
```
User: "Pull last week's page views for the courses section"
Claude: [Uses analytics-workarounds]
Using Zapier MCP → Google Analytics 4 → Run Report...

Courses pageviews (Feb 10-16, 2026):
| Page                  | Views  | Avg Time | Bounce |
|:----------------------|:-------|:---------|:-------|
| /courses              | 12,450 | 2:34     | 32%    |
| /courses/intro-101    | 8,230  | 4:12     | 18%    |
| /dashboard            | 6,890  | 1:45     | 41%    |

Week-over-week: +8% total views, -3% bounce rate.
Writing to "Analytics Exports" Google Sheet...
```

**Example 2: Subscriber Metrics**
```
User: "How are our subscriber numbers trending?"
Claude: [Uses analytics-workarounds]
Reading from "Subscriber Tracking" sheet via Zapier MCP...

| Month   | Total Subs | Net New | Churn | MRR      |
|:--------|:-----------|:--------|:------|:---------|
| Dec '25 | 14,200     | +890    | -120  | $284,000 |
| Jan '26 | 15,050     | +970    | -120  | $301,000 |
| Feb '26 | 15,800     | +850    | -100  | $316,000 |

Trend: Steady growth, churn stabilizing. Feb net adds
slightly below Jan but MRR still growing (ARPU increasing).
```

## Data Access Patterns

### Pattern 1: GA4 via Zapier MCP

Use Zapier's Google Analytics 4 tools to pull reports without needing GA4 console access.

**Available Zapier GA4 tools:**
- `google_analytics_4_run_report_for_a_property` — Primary data extraction tool
- `google_analytics_4_find_conversion` — Lookup conversion events
- `google_analytics_4_create_measurement` — Send measurement events
- `google_analytics_4_send_measurement_events_for_an_` — Batch measurement events

**Workflow:**
1. Run a GA4 report with dimensions (page path, date) and metrics (sessions, pageviews, bounce rate)
2. Parse the response into a readable table
3. Write to Google Sheets for persistent storage
4. Analyze trends and surface insights

**Budget note:** Each Zapier MCP call = 2 Zapier tasks. A GA4 report pull + Sheets write = 4 tasks. Plan accordingly for monthly task budgets.

### Pattern 2: Google Sheets as Data Hub

When data already exists in spreadsheets (exported by someone with access, or populated by Zaps):

**Available Zapier Sheets tools:**
- `google_sheets_lookup_spreadsheet_row` — Find specific data
- `google_sheets_get_many_spreadsheet_rows_advanced` — Bulk data retrieval
- `google_sheets_get_data_range` — Read a range
- `google_sheets_create_spreadsheet_row` — Write new data

**Workflow:**
1. Read existing data from the tracking sheet
2. Analyze with Claude (trends, anomalies, comparisons)
3. Write summary rows or create a new analysis sheet
4. Generate a formatted report for stakeholders

### Pattern 3: Manual Export + Claude Analysis

When automated pipelines aren't set up:

1. Ask someone with Looker/GA4 access to export a CSV
2. Import the CSV into the Claude Code session
3. Analyze: trends, anomalies, period-over-period comparison
4. Output: formatted table, chart description, stakeholder summary

### Pattern 4: BigQuery Public Datasets

For market research or benchmarking, use BigQuery public datasets:
- Google Analytics sample dataset (e-commerce)
- GitHub activity data
- Stack Overflow questions/answers
- Crypto market data (via public APIs)

Access via Zapier's `code_by_zapier_run_python` for custom queries.

## Recurring Pipeline Setup

### Weekly Metrics Pipeline

Set up a Zapier automation (outside Claude) that runs weekly:
1. **Trigger:** Schedule (every Monday at 8am)
2. **Action 1:** GA4 Run Report (last 7 days)
3. **Action 2:** Write results to Google Sheet (append row)
4. **Action 3:** Slack notification with summary

Then in Claude Code, read the sheet on demand:
> "Read the Weekly Metrics sheet and compare the last 4 weeks"

### Monthly Dashboard Refresh

> "Pull this month's GA4 data, compare to last month, and draft a metrics section for the stakeholder update"

This chains analytics-workarounds with stakeholder-update for end-to-end reporting.

## Fallback Patterns (When Zapier Is Unavailable)

### Pattern 5: Looker Browser Export

When Zapier MCP is down or you've hit your task budget:

1. Open Looker dashboard in Chrome (use `chrome-workflows` skill if available)
2. Apply filters (date range, dimensions) in the Looker UI
3. Download as CSV via Looker's "Download" button
4. Import CSV into Claude Code session for analysis
5. Write results to Google Sheets manually or via Sheets API

**Best for:** One-off pulls when you have Looker browser access but not API access.

### Pattern 6: BigQuery CLI

If you have `bq` CLI installed and authenticated:

```bash
bq query --use_legacy_sql=false --format=csv \
  'SELECT page_path, COUNT(*) as views
   FROM `project.dataset.ga_sessions_*`
   WHERE _TABLE_SUFFIX BETWEEN "20260201" AND "20260215"
   GROUP BY page_path ORDER BY views DESC LIMIT 50'
```

Pipe results into Claude Code for analysis. Useful for custom queries that Zapier's GA4 connector can't express.

### Pattern 7: Google Sheets API (Direct)

When data already lives in Sheets but Zapier isn't available:

1. Use the Google Sheets MCP server if configured, OR
2. Export the sheet as CSV (`File → Download → CSV`) and import into Claude Code
3. For recurring needs, set up a Google Apps Script to auto-export to a known location

**Choosing the right fallback:**

| Situation | Use |
|:----------|:----|
| Zapier available, task budget OK | Pattern 1 (GA4 via Zapier) |
| Zapier down, have Looker access | Pattern 5 (Looker browser export) |
| Need custom SQL, have BQ access | Pattern 6 (BigQuery CLI) |
| Data already in Sheets | Pattern 7 (Sheets direct) |
| No tool access at all | Pattern 3 (ask someone to export CSV) |

## Common Metrics to Track

| Metric | Source | Frequency | Why |
|:-------|:-------|:----------|:----|
| Page views by section | GA4 | Weekly | Content performance |
| Subscriber count | Internal sheet | Monthly | Growth tracking |
| API usage | Internal dashboard | Weekly | Product adoption |
| Course enrollment | LMS DB | Weekly | Education engagement |
| Bounce rate by page | GA4 | Monthly | UX quality signal |
| Conversion rate | GA4 | Monthly | Funnel health |

## Success Criteria

- [ ] Can pull GA4 data without direct console access
- [ ] Data lands in Google Sheets for persistence and sharing
- [ ] Trend analysis includes period-over-period comparison
- [ ] Output is formatted for direct use in stakeholder updates
- [ ] Zapier task budget is respected (each call = 2 tasks)

## Copy/Paste Ready

```
"Pull last week's GA4 data for the main site"
"Compare this month's subscribers to last month"
"Set up a weekly metrics pipeline using Zapier"
"Analyze this CSV export and find anomalies"
"Draft the metrics section for this week's stakeholder update"
```