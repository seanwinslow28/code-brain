# ETF Field Definitions

Complete reference for all WordPress ETF page fields with validation rules and examples.

## Core Identification Fields

### Page Title
**Purpose**: Official full name of the ETF
**Required**: Yes
**Format**: Proper case, full legal name
**Examples**:
- "Grayscale Bitcoin Trust"
- "iShares Bitcoin Trust ETF"
- "Fidelity Ethereum Fund"
**Validation**: Should match official SEC filings or issuer documentation

### Symbol
**Purpose**: Ticker symbol for trading and identification
**Required**: Yes
**Format**: Uppercase letters, typically 3-5 characters
**Examples**: "GBTC", "IBIT", "FETH", "ETHE"
**Data Sources**:
- TwelveData API: https://api.twelvedata.com/etf
- Official issuer website
- Financial news sites
**Validation**: All caps, no special characters or spaces

### Issuer
**Purpose**: Financial institution managing the ETF
**Required**: Yes
**Format**: Company name as commonly known
**Examples**:
- "Grayscale"
- "BlackRock"
- "Fidelity"
- "ARK Invest"
- "21Shares"
**Data Sources**: Track Insight API, SEC filings, official ETF documentation

## Trading & Market Data Fields

### Type
**Purpose**: Classification of ETF by underlying asset type
**Required**: Yes
**Format**: Dropdown selection
**Options**:
- **Spot**: Direct ownership of underlying crypto assets
- **Futures**: Exposure through futures contracts
- **Other**: Hybrid or alternative structures
**Default**: Spot (most common for Bitcoin/Ethereum ETFs)

### Status
**Purpose**: Current regulatory and trading status
**Required**: Yes
**Format**: Dropdown selection
**Options**:
- **Pending**: Application filed, awaiting SEC approval
- **Approved**: SEC approved but not yet trading
- **Live**: Actively trading on exchanges
**Usage Notes**: Update status as ETF progresses through approval process

### Fee
**Purpose**: Annual expense ratio or management fee
**Required**: Yes
**Format**: Percentage or flat dollar amount
**Examples**: "0.25%", "1.5%", "$50"
**Validation**: Must include either "%" or "$" symbol
**Typical Range**: 0.15% - 2.5% for crypto ETFs
**Data Sources**: Official prospectus, issuer fact sheets, SEC filings

### URL
**Purpose**: Official ETF landing page from issuer
**Required**: Yes
**Format**: Full URL with https://
**Examples**:
- "https://grayscale.com/products/grayscale-bitcoin-trust/"
- "https://www.ishares.com/us/products/333011/"
**Validation**: Must be valid URL starting with https://
**Data Sources**: Google search "[ETF Name] official page"

### Custodian
**Purpose**: Entity holding the underlying crypto assets
**Required**: No (optional)
**Format**: Company name
**Examples**:
- "Coinbase Custody"
- "Fidelity Digital Assets"
- "BitGo Trust Company"
**When to Leave Empty**: Not applicable for futures-based ETFs or when custodian is not publicly disclosed

## External Integration Fields

### Track Insight ID
**Purpose**: Unique identifier for Track Insight market data integration
**Required**: Yes (for live ETFs)
**Format**: Alphanumeric string (typically UUID format)
**Data Source**: Track Insight API
**API Endpoint**: https://cloud.datasets.sh/e/trackinsight-web/v0/shares?key=your-api-key
**Field to Use**: `share_id` from API response
**Authentication**: Requires Track Insight API key
**Usage**: Powers price charts and market data on ETF page

### TradingView Symbol
**Purpose**: Symbol for TradingView chart widget integration
**Required**: No (optional)
**Format**: EXCHANGE:SYMBOL
**Examples**:
- "NASDAQ:GBTC"
- "NYSEARCA:IBIT"
- "CBOE:ETHE"
**When to Leave Empty**: Token not available in TradingView (chart will be hidden on site)
**Data Source**: Search on https://www.tradingview.com/widget/advanced-chart/
**Validation**: Format must be EXCHANGE:SYMBOL with colon separator

### Charts
**Purpose**: WordPress dropdown for chart configuration
**Required**: Field exists but selection made after page creation
**Format**: Dropdown selection in WordPress admin
**Usage**: Select appropriate chart type after creating page
**Note**: This is configured in WordPress admin, not during initial data entry

## Categorization & Organization

### ETF Categories
**Purpose**: Tag ETF by underlying cryptocurrency assets
**Required**: At least one category
**Format**: Multi-select checkboxes
**Available Options**:
- Bitcoin
- Dogecoin
- Ethereum
- Litecoin
- Solana
- XRP
- Other

**Selection Guidelines**:
- Select all cryptocurrencies that represent >10% of ETF holdings
- Single-asset ETFs: Select one primary category
- Multi-asset ETFs: Select multiple categories
- Novel assets: Use "Other" category

**Examples**:
- Pure Bitcoin ETF: [Bitcoin]
- 70/30 Bitcoin/Ethereum fund: [Bitcoin, Ethereum]
- Diversified crypto basket: [Bitcoin, Ethereum, Other]

## Content & SEO Fields

### Main Content
**Purpose**: Page body with ETF description and details
**Required**: Yes (though can be minimal)
**Format**: Rich text (HTML) via WordPress editor
**Suggested Content**:
- Brief ETF overview (2-3 sentences)
- Investment strategy
- Key features or differentiators
- Links to prospectus or issuer resources
**Word Count**: 100-300 words typical
**Data Sources**: Official prospectus, issuer website, financial news coverage

### SEO Title
**Purpose**: Override default page title for search results
**Required**: No (optional)
**Format**: Text string, WordPress auto-formats as "Title | Separator | Site title"
**Default Behavior**: If empty, WordPress uses Page Title
**Best Practice**: Only customize if significantly different from Page Title
**Max Length**: 60 characters (Google truncates longer titles)

### Slug
**Purpose**: URL-friendly version of page title
**Required**: No (optional)
**Format**: lowercase, hyphens for spaces, no special characters
**Default Behavior**: WordPress auto-generates from Page Title
**Examples**:
- Page Title: "Grayscale Bitcoin Trust" → Auto-slug: "grayscale-bitcoin-trust"
- Custom slug: "gbtc" or "grayscale-btc-etf"
**Best Practice**: Leave empty unless you need specific URL structure

### Meta Description
**Purpose**: Search result snippet text
**Required**: No (optional but strongly recommended)
**Format**: Plain text, no HTML
**Optimal Length**: 150-160 characters
**Purpose**: Summarize ETF for search results and social sharing
**Best Practice**: Include ETF name, type, issuer, and key differentiator
**Example**: "Grayscale Bitcoin Trust (GBTC) is a spot Bitcoin ETF managed by Grayscale, offering institutional access to BTC with 1.5% annual fee."

## Field Validation Quick Reference

| Field | Required | Format | Typical Value |
|-------|----------|--------|---------------|
| Page Title | Yes | Text | "Grayscale Bitcoin Trust" |
| Symbol | Yes | UPPERCASE | "GBTC" |
| Track Insight ID | Yes* | Alphanumeric | UUID from API |
| Issuer | Yes | Text | "Grayscale" |
| Type | Yes | Dropdown | "Spot" |
| Fee | Yes | Number + % or $ | "1.5%" |
| URL | Yes | URL | https://... |
| Status | Yes | Dropdown | "Live" |
| Categories | Yes | Checkboxes | [Bitcoin] |
| Custodian | No | Text | "Coinbase Custody" |
| TradingView | No | EXCHANGE:SYMBOL | "NASDAQ:GBTC" |
| Main Content | Yes** | Rich text | 100-300 words |
| SEO Title | No | Text | Auto-generated |
| Slug | No | URL-safe | Auto-generated |
| Meta Desc | No*** | Text | 150-160 chars |

\* Required for live ETFs with market data  
\*\* Can be minimal but should exist  
\*\*\* Optional but strongly recommended for SEO
