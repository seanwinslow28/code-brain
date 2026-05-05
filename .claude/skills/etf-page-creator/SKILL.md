---
name: etf-page-creator
description: Streamline WordPress ETF (Exchange-Traded Fund) page creation for a publishing platform. Use when user needs to create or update ETF pages with structured data including Track Insight IDs, symbols, issuers, trading data, categories, and SEO metadata. Guides data collection, validates inputs, and formats output for copy-paste into WordPress fields.
---

# ETF Page Creator

Create properly formatted WordPress ETF pages for a publishing platform with structured data collection and validation.

## Workflow Overview

1. **Determine mode**: New ETF or update existing
2. **Collect data**: Guide user through all required fields
3. **Validate & enrich**: Check data format, optionally search for missing info
4. **Format output**: Generate copy-paste ready checklist matching WordPress field order

## Step 1: Determine Mode

Ask user: "Are you creating a **new ETF page** or **updating an existing one**?"

**If updating**: Ask which fields need updating, skip straight to those fields in data collection.

**If creating new**: Proceed with full data collection workflow below.

## Step 2: Data Collection

Collect data systematically using the form below. If user doesn't have certain data, offer to search for it using web_search.

### Required Fields (always collect)

**Page Title** (ETF full name)
- Example: "Grayscale Bitcoin Trust"
- Validation: Should be the official ETF name

**Symbol** (ticker/short name)
- Example: "GBTC"
- Validation: All caps, typically 3-5 characters
- Data source hint: TwelveData API (https://api.twelvedata.com/etf)

**Type** (dropdown selection)
- Options: Spot / Futures / Other
- Default: Spot for most Bitcoin/Ethereum ETFs

**Status** (dropdown selection)
- Options: Pending / Approved / Live
- Use: "Pending" for applications, "Live" for trading ETFs

### External Integration Fields

**Track Insight ID**
- Where to find: https://cloud.datasets.sh/e/trackinsight-web/v0/shares?key=your-api-key
- Format: share_id from the API response
- Validation: Alphanumeric string
- Note: User needs Track Insight API key

**TradingView Symbol** (optional)
- Where to find: https://www.tradingview.com/widget/advanced-chart/
- Format: Exchange:SYMBOL (e.g., "NASDAQ:GBTC")
- Leave empty if: Token not available in TradingView (chart will be hidden)

### ETF Details

**Issuer** (company name)
- Example: "Grayscale", "BlackRock", "Fidelity"
- Data source hint: Track Insight API or web search

**Fee** (expense ratio or flat fee)
- Format examples: "0.25%", "$50", "1.5%"
- Validation: Must include % or $ symbol

**URL** (official ETF page)
- Format: Full URL starting with https://
- Validation: Must be valid URL to issuer's official page

**Custodian** (optional)
- Example: "Coinbase Custody", "Fidelity Digital Assets"
- Leave empty if: Not applicable or unknown

### Categories (multi-select checkboxes)

Available categories:
- Bitcoin
- Dogecoin
- Ethereum
- Litecoin
- Solana
- XRP
- Other

Ask user which categories apply. Most ETFs will have 1-2 categories.

### Content & SEO

**Main Content** (page body)
- Use rich text editor in WordPress
- Always write 3 short paragraphs:
  1. **Fund overview**: What the ETF is, issuer, what asset it holds, exchange, ticker, and structure (e.g., Delaware statutory trust). Mention staking if applicable.
  2. **Underlying asset/network**: Brief description of the blockchain or asset the ETF tracks — what it does, key stats, notable adopters or use cases.
  3. **Structure & risk**: Regulatory status (e.g., not registered under 1940 Act), fee/expense ratio, custodian(s), administrator, and risk disclaimers (volatility, staking not guaranteed, etc.).
- If user wants help: Offer to search for ETF information and draft content

**SEO Title** (optional but recommended)
- Default: Same as page title if not provided
- **The Block's Standard Format**: `[ETF Name] ([Symbol]) [Status] & Key Details | The Block`
- Status keywords: "Live Status" or "Status" (both acceptable)
- Examples:
  - "Grayscale Cardano Trust (GADA) Live Status and Key Details | The Block"
  - "Fidelity Solana Fund (FSOL) Status & Key Details | The Block"
  - "ARK 21 Shares Ethereum Futures Strategy ETF (ARKZ) Live Status and Key Details | The Block"

**Slug** (URL-friendly name, optional)
- WordPress auto-generates from title if not provided
- Format: lowercase, hyphens for spaces (e.g., "grayscale-bitcoin-trust")

**Meta Description** (optional but recommended)
- Length: 150-160 characters optimal
- **The Block's Standard Format**: 
  - `[ETF Name] ([Symbol]) is a [type] [asset] ETF [launched/proposed] by [Issuer]. See [status keyword], [statistics,] and details.`
- Use "proposed" for pending ETFs, "launched" for live/approved ETFs
- Optionally include "statistics" for live ETFs
- Examples:
  - **Pending**: "The Grayscale Cardano Trust is a potential spot Cardano (ADA) ETF proposed by Grayscale. See live status and details."
  - **Live (Spot)**: "Fidelity Solana Fund (FSOL) is a spot SOL ETF launched by Fidelity. See ETF live status, statistics, and details."
  - **Live (Futures)**: "The 21Shares 2x Long Dogecoin ETF (TXXD) is a Dogecoin ETF launched by 21Shares. See the latest status, details and statistics here."
  - **Overview style**: "An overview of the ARK 21 Shares Active Ethereum Futures Strategy ETF (ARKZ) with live chart, latest price, market info and related ETF data."

## Step 3: Validate & Enrich (Optional)

If user is missing data, offer: "I can search for [missing field] using web search. Would you like me to find this information?"

**Key data sources for web search**:
- Official issuer websites (prospectus, fact sheets)
- SEC filings for US ETFs
- TradingView for chart symbols
- Financial news (The Block, CoinDesk, Bloomberg)

## Step 4: Format Output

**Always auto-generate SEO Title and Meta Description** using The Block's standard formats (shown in Step 2). Don't ask user if they want these - just create them automatically based on the ETF data collected.

Generate a **numbered checklist** matching exact WordPress field order for easy copy-paste:

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
[instruction: "Select from dropdown after page is created"]

**Categories (check all that apply):**
- [ ] Bitcoin
- [ ] Dogecoin
- [ ] Ethereum
- [ ] Litecoin
- [ ] Other
- [ ] Solana
- [ ] XRP

**Main Content:**
[content or "Add using WordPress rich text editor"]

---

## SEO Settings

**SEO Title:**
[ETF Name] ([Symbol]) [Live Status/Status] & Key Details | The Block

**Slug:**
[auto-generated-slug or custom slug]

**Meta Description:**
[Generated using The Block's standard format based on ETF type and status]
```

## Tips for User

**After generating checklist:**
- "Open your WordPress 'Add ETF Page' in another tab"
- "Copy each value and paste into the corresponding WordPress field"
- "For dropdowns (Type, Status), select the matching option"
- "For categories, check the relevant boxes"
- "Use the rich text editor for Main Content section"

**Validation reminders:**
- URLs must start with https://
- Fees must include % or $ symbol
- Symbols are typically uppercase
- TradingView Symbol format: EXCHANGE:SYMBOL

## References

For detailed field explanations and data sources, see:
- `references/field-definitions.md` - Complete field documentation
- `references/data-sources.md` - APIs and websites for finding ETF data
- `references/seo-writing-guide.md` - Complete SEO title and meta description patterns with examples
