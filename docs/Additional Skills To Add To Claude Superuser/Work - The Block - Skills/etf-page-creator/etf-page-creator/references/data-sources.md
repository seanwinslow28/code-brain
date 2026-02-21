# ETF Data Sources

Comprehensive guide to APIs, websites, and resources for finding ETF information.

## Primary Data APIs

### Track Insight API
**Purpose**: Official market data integration for The Block's ETF pages
**Required For**: Track Insight ID field
**Authentication**: API key required (user must have access)

**Endpoint**: `https://cloud.datasets.sh/e/trackinsight-web/v0/shares?key=your-api-key`

**Response Structure**:
```json
{
  "data": [
    {
      "share_id": "uuid-string-here",
      "isin": "US1234567890",
      "name": "ETF Full Name",
      "ticker": "SYMB",
      "currency": "USD",
      "issuer": "Issuer Name"
    }
  ]
}
```

**Fields to Extract**:
- `share_id` → Track Insight ID
- `name` → Page Title
- `ticker` → Symbol
- `issuer` → Issuer

**Search Strategy**: Use ETF name or ticker to find matching record

---

### TwelveData API
**Purpose**: ETF trading data, symbols, and market information
**Authentication**: API key required (free tier available)

**Endpoint**: `https://api.twelvedata.com/etf`

**Parameters**:
- `symbol`: ETF ticker (e.g., "GBTC")
- `apikey`: Your API key

**Response Includes**:
- Symbol
- Full name
- Exchange
- Expense ratio (fee)
- Asset class
- Inception date

**Use Cases**: Symbol validation, fee information, exchange data

**Website**: https://twelvedata.com/

---

### TradingView Chart Lookup
**Purpose**: Find TradingView symbol for chart widget integration
**Authentication**: None (public widget)

**Search URL**: `https://www.tradingview.com/widget/advanced-chart/`

**Process**:
1. Open TradingView advanced chart widget
2. Search for ETF ticker in symbol search
3. If found, format as EXCHANGE:SYMBOL
4. If not found, leave TradingView Symbol field empty

**Format Examples**:
- US ETFs on NASDAQ: "NASDAQ:GBTC"
- NYSE Arca: "NYSEARCA:IBIT"
- CBOE: "CBOE:ETHE"

**Note**: Not all ETFs are available in TradingView. New/pending ETFs won't be listed.

---

## Official & Regulatory Sources

### SEC EDGAR Database
**Purpose**: Official SEC filings, prospectuses, form S-1 applications
**URL**: https://www.sec.gov/edgar/searchedgar/companysearch.html

**Key Documents**:
- **Form S-1**: Initial ETF application (pending status)
- **Prospectus**: Official ETF details (fee, strategy, custodian)
- **Form N-1A**: Registration for investment companies
- **485BPOS**: Post-effective amendments (updates)

**Search Strategy**:
1. Search by ETF issuer name or ticker
2. Look for most recent S-1 or prospectus
3. Extract: Fee, custodian, official name, strategy

**Information Available**:
- Official ETF name
- Expense ratio (fee)
- Custodian
- Investment strategy
- Issuer details
- Approval status dates

---

### Issuer Official Websites

**Major Crypto ETF Issuers**:

**Grayscale**
- URL: https://grayscale.com/products/
- Products: GBTC, ETHE, multiple crypto trusts
- Data Available: Fees, AUM, holdings, custodian

**BlackRock**
- URL: https://www.ishares.com/us/products/etf-investments
- Products: IBIT (Bitcoin ETF)
- Data Available: Full prospectus, fact sheets, fees

**Fidelity**
- URL: https://institutional.fidelity.com/app/funds-and-products/etf/
- Products: FBTC, FETH
- Data Available: Prospectus, fund details, expense ratios

**ARK Invest**
- URL: https://ark-invest.com/our-etfs/
- Products: ARKB (Bitcoin)
- Data Available: Daily holdings, strategy, fees

**21Shares**
- URL: https://21shares.com/en-us/product-list
- Products: Multiple crypto ETPs
- Data Available: Product sheets, fees, custodian info

**Bitwise**
- URL: https://bitwiseinvestments.com/crypto-funds
- Products: BITB (Bitcoin)
- Data Available: Fund information, strategies

**VanEck**
- URL: https://www.vaneck.com/us/en/investments/
- Products: HODL (Bitcoin)
- Data Available: Prospectus, fact sheets

**Valkyrie**
- URL: https://valkyrieinvest.com/
- Products: Multiple crypto ETFs
- Data Available: Product details, filings

---

## Financial Data Websites

### ETF.com
**URL**: https://www.etf.com/
**Purpose**: ETF research and data
**Search**: https://www.etf.com/etfanalytics/etf-finder
**Data Available**:
- Expense ratios
- Holdings
- Performance data
- Issuer information
- Category classifications

**Search Strategy**: Use ETF ticker or name in finder tool

---

### ETFdb.com
**URL**: https://etfdb.com/
**Purpose**: Comprehensive ETF database
**Search**: https://etfdb.com/screener/
**Data Available**:
- Detailed ETF profiles
- Expense ratios
- Holdings breakdown
- Historical data
- Category/classification

---

### Yahoo Finance
**URL**: https://finance.yahoo.com/
**Purpose**: Real-time quotes and ETF profiles
**Search Format**: https://finance.yahoo.com/quote/[TICKER]
**Example**: https://finance.yahoo.com/quote/GBTC

**Data Available**:
- Current price and charts
- Expense ratio
- Official name
- Holdings summary
- Custodian (sometimes listed)

**Use Cases**: Quick validation, fee verification, current status

---

## Crypto & Industry News Sources

### The Block
**URL**: https://www.theblock.co/
**Purpose**: Crypto news including ETF coverage
**Search**: Site search for ETF ticker or name
**Data Available**:
- Approval announcements
- Launch dates
- Industry analysis
- Issuer statements

---

### CoinDesk
**URL**: https://www.coindesk.com/
**Purpose**: Crypto financial news
**ETF Section**: https://www.coindesk.com/tag/etf/
**Data Available**:
- Regulatory updates
- New ETF launches
- Performance analysis
- Market data

---

### Bloomberg Crypto
**URL**: https://www.bloomberg.com/crypto
**Purpose**: Financial and crypto market news
**Data Available** (may require subscription):
- Detailed ETF analysis
- Regulatory filings
- Market performance
- Institutional data

---

## Search Strategies by Field

### Finding Track Insight ID
1. **Primary**: Track Insight API with ETF name or ticker
2. **Alternative**: Contact The Block's data team if not in API

### Finding Symbol
1. **Primary**: Official issuer website
2. **Backup**: TwelveData API, Yahoo Finance
3. **Validation**: SEC EDGAR filings

### Finding Issuer
1. **Primary**: SEC EDGAR company search
2. **Backup**: Official ETF website, financial news

### Finding Fee
1. **Primary**: Official prospectus (SEC EDGAR)
2. **Backup**: Issuer website, ETF.com, Yahoo Finance
3. **Validation**: Should be in prospectus as "expense ratio"

### Finding URL
1. **Primary**: Google search "[ETF name] official page"
2. **Validation**: Should be issuer's domain (grayscale.com, ishares.com, etc.)
3. **Format**: Direct link to specific ETF product page

### Finding Custodian
1. **Primary**: Official prospectus (SEC EDGAR)
2. **Backup**: Issuer press releases, industry news
3. **Common Custodians**: Coinbase Custody, Fidelity Digital Assets, BitGo

### Finding TradingView Symbol
1. **Only Source**: TradingView widget search
2. **Format**: Must be EXCHANGE:SYMBOL
3. **Fallback**: Leave empty if not found (many new ETFs won't be available)

### Finding Status (Pending/Approved/Live)
1. **SEC Filings**: Check for S-1 (pending), approval notice (approved)
2. **News Sources**: The Block, CoinDesk for approval announcements
3. **Trading Status**: Yahoo Finance, TradingView (if trading = live)

### Finding Categories
1. **Prospectus**: "Investment Objective" section lists underlying assets
2. **Issuer Website**: Product page typically lists asset exposure
3. **ETF.com/ETFdb**: Holdings breakdown shows category

---

## Web Search Tips

### Effective Search Queries
- **For official pages**: "[ETF Name] [Issuer] official"
  - Example: "IBIT BlackRock official"
  
- **For prospectus**: "[ETF Name] prospectus SEC"
  - Example: "Grayscale Bitcoin Trust prospectus SEC"
  
- **For fees**: "[Symbol] expense ratio"
  - Example: "GBTC expense ratio"
  
- **For custodian**: "[ETF Name] custodian"
  - Example: "IBIT custodian"
  
- **For approval status**: "[ETF Name] SEC approval"
  - Example: "Fidelity Ethereum ETF SEC approval"

### Validation Strategy
When finding data via web search:
1. Cross-reference with at least 2 sources
2. Prioritize official sources (SEC, issuer website)
3. Check publication dates (use recent data)
4. Verify URLs are from legitimate domains

---

## Quick Reference: Best Source by Field

| Field | Best Source | Backup Source |
|-------|------------|---------------|
| Track Insight ID | Track Insight API | N/A (API only) |
| Symbol | Issuer website | SEC EDGAR |
| Issuer | SEC EDGAR | Issuer website |
| Type | Prospectus | ETF.com |
| Fee | Prospectus | Yahoo Finance |
| URL | Google search | Issuer homepage |
| Custodian | Prospectus | Industry news |
| TradingView | TradingView widget | N/A (leave empty) |
| Status | SEC EDGAR | News sources |
| Categories | Prospectus | ETF.com holdings |
