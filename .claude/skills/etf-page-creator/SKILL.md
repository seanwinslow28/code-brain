---
name: etf-page-creator
description: WordPress ETF page creation assistant for The Block. Guides data collection, validates inputs, and formats output for copy-paste into WordPress custom fields. Handles Track Insight IDs, TradingView symbols, issuers, fees, categories, and SEO metadata. Use when asked to "create an ETF page", "add a new ETF", "update ETF data", "ETF page", or any crypto ETF page workflow.
---

# ETF Page Creator — The Block

## Purpose

Streamline creation of WordPress ETF (Exchange-Traded Fund) pages for The Block's website. Guides data collection for all required fields, validates inputs, auto-generates SEO metadata, and produces a copy-paste ready checklist matching WordPress field order.

## When to Use

- **New ETF page:** "Create an ETF page for [fund name]"
- **Update existing:** "Update the GBTC ETF page fee"
- **Batch creation:** "Create pages for these 5 new Bitcoin ETFs"
- **Data enrichment:** "Find the Track Insight ID for [ETF]"

## Workflow

### Step 1: Determine Mode

Ask: "Are you creating a **new ETF page** or **updating an existing one**?"

- **New:** Full data collection workflow below
- **Update:** Ask which fields need updating, skip to those fields

### Step 2: Collect Data

Collect systematically. If user doesn't have data, offer to search for it.

#### Required Fields

| Field | Format | Example | Validation |
|-------|--------|---------|------------|
| **Page Title** | ETF full name | Grayscale Bitcoin Trust | Official ETF name |
| **Symbol** | Ticker (all caps) | GBTC | 3-5 characters, uppercase |
| **Type** | Dropdown | Spot / Futures / Other | Select one |
| **Status** | Dropdown | Pending / Approved / Live | Select one |

#### External Integration Fields

| Field | Where to Find | Format |
|-------|--------------|--------|
| **Track Insight ID** | `https://cloud.datasets.sh/e/trackinsight-web/v0/shares` | Alphanumeric `share_id` from API |
| **TradingView Symbol** | TradingView widget configurator | `EXCHANGE:SYMBOL` (e.g., `NASDAQ:GBTC`) |

TradingView Symbol is optional — leave empty if not available (chart will be hidden).

#### ETF Details

| Field | Format | Example |
|-------|--------|---------|
| **Issuer** | Company name | Grayscale, BlackRock, Fidelity |
| **Fee** | With % or $ | 0.25%, $50 |
| **URL** | Full https:// URL | Official issuer page |
| **Custodian** | Company name (optional) | Coinbase Custody, Fidelity Digital Assets |

#### Categories (multi-select)

Available: Bitcoin, Dogecoin, Ethereum, Litecoin, Solana, XRP, Other

Most ETFs have 1-2 categories.

### Step 3: Auto-Generate SEO

Always generate these automatically from collected data:

**SEO Title format:**
```
[ETF Name] ([Symbol]) [Live Status/Status] & Key Details | The Block
```

Examples:
- `Grayscale Cardano Trust (GADA) Live Status and Key Details | The Block`
- `Fidelity Solana Fund (FSOL) Status & Key Details | The Block`

**Meta Description format:**
```
[ETF Name] ([Symbol]) is a [type] [asset] ETF [launched/proposed] by [Issuer]. See [status keyword], [statistics,] and details.
```

- Use "proposed" for Pending ETFs, "launched" for Live/Approved
- Include "statistics" for Live ETFs

Examples:
- **Pending:** "The Grayscale Cardano Trust is a potential spot Cardano (ADA) ETF proposed by Grayscale. See live status and details."
- **Live (Spot):** "Fidelity Solana Fund (FSOL) is a spot SOL ETF launched by Fidelity. See ETF live status, statistics, and details."
- **Live (Futures):** "The 21Shares 2x Long Dogecoin ETF (TXXD) is a Dogecoin ETF launched by 21Shares. See the latest status, details and statistics here."

**Slug:** Auto-generate from title (lowercase, hyphens). Example: `grayscale-bitcoin-trust`

### Step 4: Format Output

Generate a copy-paste checklist matching WordPress field order:

```
## ETF Page Data - Copy-Paste Checklist

**Page Title:**
[value]

**Track Insight ID:**
[value]

**Symbol:**
[value]

**Issuer:**
[value]

**Type:**
[value] (Select from dropdown: Spot/Futures/Other)

**Fee:**
[value]

**URL:**
[value]

**Custodian:**
[value or "Leave empty"]

**TradingView Symbol:**
[value or "Leave empty - chart will be hidden"]

**Status:**
[value] (Select from dropdown: Pending/Approved/Live)

**Charts:**
[Select from dropdown after page is created]

**Categories (check all that apply):**
- [ ] Bitcoin
- [ ] Ethereum
- [ ] Solana
- [ ] XRP
- [ ] Dogecoin
- [ ] Litecoin
- [ ] Other

**Main Content:**
[content or "Add using WordPress rich text editor"]

---

## SEO Settings

**SEO Title:**
[auto-generated]

**Slug:**
[auto-generated]

**Meta Description:**
[auto-generated]
```

## Data Sources for Enrichment

If user is missing data, search these:

| Data | Source |
|------|--------|
| Track Insight ID | Track Insight API (requires API key) |
| TradingView Symbol | TradingView widget configurator |
| Issuer, Fee, Custodian | Official issuer website, SEC filings |
| General ETF info | The Block, CoinDesk, Bloomberg |

## Validation Rules

- URLs must start with `https://`
- Fees must include `%` or `$` symbol
- Symbols are uppercase, 3-5 characters
- TradingView Symbol format: `EXCHANGE:SYMBOL`
- Meta Description: 150-160 characters optimal
- SEO Title: include `| The Block` suffix

## Examples

**Example 1: New ETF page**
```
User: "Create an ETF page for the new BlackRock Solana ETF"
Claude: [Uses etf-page-creator]

I'll collect the data for this ETF page. Let me start:

1. Page Title: BlackRock Solana Trust
2. Symbol: BSOL (confirm?)
3. Type: Spot
4. Status: Pending (since it's new)

What's the Track Insight ID? I can search for it if needed.
...

[After collecting all data, generates copy-paste checklist with auto-generated SEO]
```

**Example 2: Update existing**
```
User: "Update the GBTC page - status changed to Live and fee is now 1.5%"
Claude: [Uses etf-page-creator]

Updated fields for GBTC:
- Status: Live (select from dropdown)
- Fee: 1.5%

SEO updates needed:
- Meta Description: Update "proposed" to "launched" and add "statistics"
```

## Post-Creation Instructions

After generating the checklist, remind user:
1. Open WordPress "Add ETF Page" in another tab
2. Copy each value into the corresponding field
3. For dropdowns (Type, Status), select the matching option
4. For categories, check the relevant boxes
5. Use the rich text editor for Main Content
6. Publish and verify the page renders correctly

## Success Criteria

- [ ] All required fields collected and validated
- [ ] SEO Title and Meta Description auto-generated using Block formats
- [ ] Output formatted as copy-paste checklist matching WordPress field order
- [ ] Validation rules applied (URLs, fees, symbols)
- [ ] Categories correctly identified for the asset type

## Copy/Paste Ready

```
"Create an ETF page for [fund name]"
"Add a new [asset] ETF page"
"Update the [symbol] ETF page"
"Find the Track Insight ID for [ETF]"
"Create ETF pages for these funds: [list]"
```