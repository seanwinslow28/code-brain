# The Block — Design System Document

**Version:** 1.0
**Last Updated:** February 2026
**Product:** TheBlock.co

---

## Table of Contents

1. [Overview](#1-overview)
2. [Brand Identity](#2-brand-identity)
3. [Color System](#3-color-system)
4. [Data Visualization Palettes](#4-data-visualization-palettes)
5. [Typography](#5-typography)
6. [Iconography](#6-iconography)
7. [Logo Assets](#7-logo-assets)
8. [Navigation & Information Architecture](#8-navigation--information-architecture)
9. [Page Layouts](#9-page-layouts)
10. [Audience Context](#10-audience-context)
11. [Appendix](#11-appendix)

---

## 1. Overview

The Block is a leading digital media and research platform covering cryptocurrency, blockchain technology, and digital finance. This design system document defines the visual language, component standards, and usage guidelines that ensure consistency across TheBlock.co's web products.

### Design Principles

- **Data-first:** Prioritize clarity and readability for financial and market data.
- **Dual-theme support:** All components must function in both Light Mode and Dark Mode.
- **Professional credibility:** Visual design should reflect the institutional, research-grade nature of the content.
- **Information density:** Layouts accommodate large volumes of content (news feeds, data tables, price tickers) without feeling cluttered.

---

## 2. Brand Identity

### Primary Brand Colors

The Block's brand identity uses a bold, high-contrast palette of five core colors:

| Role | Color | Approximate Hex | Usage |
|------|-------|-----------------|-------|
| Primary Blue | Vivid blue | `#0066FF` | Primary brand accent, CTAs, links, data highlights |
| Accent Coral/Red | Warm coral-red | `#FF4D5A` | Secondary accent, alerts, negative data indicators |
| Accent Lime | Yellow-green/lime | `#D4FF00` | Tertiary accent, promotional highlights, badges |
| Light Neutral | Off-white/light gray | `#F0EDEA` | Light mode backgrounds, cards |
| Dark Neutral | Black | `#000000` | Dark mode backgrounds, primary text on light |

These five brand colors appear prominently in the brand swatch panel and are used throughout the site for advertising banners, navigation highlights, and key interactive elements.

---

## 3. Color System

The design system includes a comprehensive set of color scales, each ranging from very light tints to deep, saturated darks. Every scale contains approximately 8–10 steps.

### 3.1 Neutral / Grayscale

A full grayscale from white through mid-grays to pure black. Used for backgrounds, text, borders, and UI chrome across both themes.

| Step | Description | Typical Use |
|------|-------------|-------------|
| 1 (lightest) | White / near-white | Light mode page background |
| 2–3 | Light grays | Card backgrounds, dividers |
| 4–5 | Mid grays | Secondary text, icons, borders |
| 6–7 | Dark grays | Dark mode card backgrounds |
| 8 (darkest) | Pure black | Dark mode page background, light mode primary text |

### 3.2 Green Scale

Ranges from a pale mint green through vivid greens to a deep forest green. Stars (indicating Research/Data Color Set usage) appear on several mid-range values.

**Usage:** Positive data indicators (price up, gains), success states, and data visualization.

### 3.3 Cyan / Teal Scale

Spans from a light icy cyan to a deep dark teal. Stars mark several mid-range tones for data visualization use.

**Usage:** Secondary data series, chart accents, informational badges, link hover states.

### 3.4 Blue Scale

Ranges from a very light periwinkle/lavender to a deep navy. Stars mark several tones for data set usage.

**Usage:** Primary interactive elements, links, selected states, chart primary series, header accents.

### 3.5 Purple Scale

Light lavender through to deep plum/eggplant.

**Usage:** Tertiary data series, category tags, premium/pro feature indicators.

### 3.6 Red Scale

Pale pink through vivid red to a deep crimson/maroon. Stars mark data-set-designated tones.

**Usage:** Negative data indicators (price down, losses), error states, alerts, breaking news badges.

### 3.7 Orange Scale

Light peach through bright orange to a deep burnt orange.

**Usage:** Warning states, moderate-priority alerts, trending indicators.

### 3.8 Yellow Scale

Pale cream through bright yellow to a dark olive-gold. Stars mark data-set-designated tones.

**Usage:** Caution indicators, highlight/spotlight elements, promotional badges (when combined with the lime brand accent).

### Color Usage Rules

- **Stars** on swatches denote colors designated for the Research/Data Color Sets. These specific tones should be reserved for charts and data visualizations to maintain consistency across all research outputs.
- Always ensure sufficient contrast ratios (WCAG AA minimum) when pairing text and background colors.
- In Dark Mode, use lighter tints from each scale for text and data; in Light Mode, use darker shades.

---

## 4. Data Visualization Palettes

Two purpose-built palettes ensure that charts and graphs are visually distinct and accessible.

### 4.1 Small Data Palette (1–8 Data Points)

For charts displaying up to 8 distinct series. Colors are selected for maximum differentiation at a glance:

| Order | Color Description |
|-------|-------------------|
| 1 | Blue (primary) |
| 2 | Coral/Red |
| 3 | Cyan |
| 4 | Olive/Khaki |
| 5 | Pink/Magenta |
| 6 | Teal |
| 7 | Yellow-green |
| 8 | Warm gray |

### 4.2 Large Data Palette (9–13 Data Points)

For charts requiring more series differentiation. Extends the small palette with additional hues:

| Order | Color Description |
|-------|-------------------|
| 1 | Blue (primary) |
| 2 | Medium blue |
| 3 | Coral/Red |
| 4 | Soft red/salmon |
| 5 | Cyan |
| 6 | Pink/Magenta |
| 7 | Olive/Khaki green |
| 8 | Yellow-green |
| 9 | Dark olive |
| 10–13 | Additional muted tones for extended series |

### Data Palette Rules

- Always use the Small Data Palette when 8 or fewer series are present. Do not skip colors or reorder.
- Only switch to the Large Data Palette when 9 or more series require differentiation.
- Maintain consistent color-to-category mapping across related charts (e.g., Bitcoin should always use the same color within a single report or dashboard view).

---

## 5. Typography

Based on the homepage screenshots, The Block uses a clean, modern sans-serif type system designed for high information density and readability.

### Typographic Hierarchy (Observed)

| Level | Style | Context |
|-------|-------|---------|
| Site Logo | Custom wordmark — "THE BLOCK" | All caps, geometric sans-serif, appears in the header |
| H1 / Hero Headlines | Bold, large sans-serif | Lead story headlines |
| H2 / Section Headers | Bold, medium sans-serif, uppercase | Section titles like "LATEST CRYPTO NEWS", "PRICES", "CRYPTO INDICES" |
| H3 / Card Headlines | Semi-bold, standard size | Article card titles |
| Body Text | Regular weight, comfortable reading size | Article summaries, descriptions |
| Caption / Metadata | Small, lighter weight or muted color | Timestamps, author names, tags |
| Data / Ticker Text | Monospace or tabular figures | Price ticker, index values, percentage changes |

### Typography Rules

- Headlines should remain concise and scannable.
- Price and financial data should use tabular (monospaced) figures for alignment in tables and tickers.
- In Dark Mode, body text should be a soft white or light gray rather than pure white to reduce eye strain.

---

## 6. Iconography

The icon set uses a consistent outlined (stroke-based) style with uniform weight. All icons are rendered in a single color (dark gray or black on light backgrounds, white on dark backgrounds).

### Available Icons (Observed)

| Icon | Description | Typical Use |
|------|-------------|-------------|
| Home (outline) | House shape, unfilled | Navigation — Home link |
| Home (filled) | House shape, filled | Navigation — Active Home state |
| External Link | Arrow pointing out of a box | Open in new tab, external sources |
| Menu / Hamburger | Three horizontal lines | Mobile navigation toggle |
| Edit / Pencil | Pencil on paper | Edit content, user notes |
| Image / Gallery | Landscape photo icon | Media content, image galleries |
| Save / Bookmark | Floppy disk or bookmark shape | Save article, bookmark |
| Filter / Sort | Funnel or adjustment lines | Filter controls, data sorting |

### Icon Usage Rules

- All icons must use a consistent stroke width (approximately 1.5–2px).
- Icons should be a minimum of 24x24px at standard resolution for touch targets.
- Never mix filled and outlined icons in the same context unless indicating active vs. inactive states.
- Icons should inherit text color from their parent element to maintain theme compatibility.

---

## 7. Logo Assets

### 7.1 Cryptocurrency Logos

The design system includes a library of 60+ cryptocurrency logos, displayed as circular icons on a dark background. These are used in data tables, price tickers, token pages, and research content.

**Included tokens (partial list):**

- **Layer 1 / Major:** Bitcoin (BTC), Ethereum (ETH), Solana (SOL), Cardano (ADA), Avalanche (AVAX), Polkadot (DOT), Cosmos (ATOM)
- **DeFi:** Uniswap (UNI), Aave (AAVE), Maker (MKR), Compound (COMP), Curve (CRV)
- **Layer 2 / Scaling:** Polygon (MATIC), Arbitrum (ARB), Optimism (OP)
- **Payments / Exchange:** Litecoin (LTC), XRP, Stellar (XLM), BNB
- **Meme / Culture:** Dogecoin (DOGE), Coq Inu
- **Infrastructure:** Chainlink (LINK), Filecoin (FIL), The Graph (GRT)
- **Other Notable:** Algorand (ALGO), Tron (TRX), Tezos (XTZ), NEAR, Sui, Aptos, Hedera (HBAR), Stacks (STX), Synthetix (SNX), Decentraland (MANA), Monero (XMR), and more

### Crypto Logo Display Rules

- Logos are always displayed in circular containers.
- Standard sizes: 24px (inline/ticker), 32px (tables), 48px (detail pages).
- On dark backgrounds, logos use their native colors. On light backgrounds, ensure sufficient contrast.

### 7.2 Fiat Currency Logos

A set of fiat currency symbols displayed as white symbols inside dark circular icons:

| Symbol | Currency |
|--------|----------|
| $ | US Dollar (USD) |
| ¥ | Japanese Yen (JPY) / Chinese Yuan (CNY) |
| € | Euro (EUR) |
| £ | British Pound (GBP) |
| ₹ | Indian Rupee (INR) |
| ₱ | Philippine Peso (PHP) |
| C$ | Canadian Dollar (CAD) |
| Rp | Indonesian Rupiah (IDR) |
| A$ | Australian Dollar (AUD) |
| Rs | Pakistani/Sri Lankan Rupee |
| ₽ | Russian Ruble (RUB) |

### Fiat Logo Display Rules

- Fiat logos follow the same circular container format as crypto logos for visual consistency.
- White symbol on dark gray/black background.
- Used wherever fiat currency conversions, pricing, or cross-currency data is displayed.

---

## 8. Navigation & Information Architecture

The site follows a structured hierarchy with a primary navigation bar, search, and several content verticals.

### 8.1 Primary Navigation Bar

**Top-level items:**

| Nav Item | Description |
|----------|-------------|
| Home | Landing page / custom dashboard |
| Research | Institutional-grade research reports and analysis |
| Data | Market data, on-chain metrics, DeFi stats |
| News | Breaking news and editorial content |
| Funding | Venture capital, deal flow, and company funding data |
| More Menu | User profile, settings, additional resources |

### 8.2 Search

- **Global Indexed Results** — site-wide search across all content types.
- **Show Summary with Reference Source Links** — AI-assisted search summaries with citations.

### 8.3 Context Actions

Available alongside search results:

- Cite with Research Topic
- Cite with Direct link
- Notes with Bookmarks

### 8.4 Section Breakdown

#### Home / Custom Dashboard

- Account-specific content personalization
- User-curated feeds
- Custom Dashboard configuration

#### Research

- **Content Types:** Latest (The Firehose), Most Popular (D1, M1, M6, All-Time), Custom Views / Favorite Topics, Staff Picks
- **Filters / Tags:** The Block, Layer 1s, Ecosystem Maps, Market Recap, RapidIntelligence, DeFi, Metaverse & NFT, Enterprise Blockchain, Layer 2s / Scaling, Web3, Reports, Crypto Ecosystems, BridgeS, Currency, Markets, Staking, Company Intelligence, IT Companies, Companies, Infrastructure, More

#### Data

- **Content Types:** Custom Views / Favorites, Most Popular, Staff Picks
- **Categories:** Markets, Futures, Bitcoin ETFs, Crypto ETFs, DeFi, Crypto Indices, Options, Sports Tokens, Prices, Comparison, Exchange Token, Stablecoins, ESG Prepared, Non-Fiat Pegged, On-Chain Metrics, Bitcoin, Ethereum, Solana, Polygon, Avalanche, Comparison, Tron
- **Scaling Solutions:** Ethereum L2, Layer 1 EVM Blockchains, Layer 1 Non-EVM Blockchains, Layer 2 Optimistic Rollups, Layer 2 ZK Rollups, Data Availability
- **DeFi Sub-categories:** Risk, Stablecoins, Exchange, Borrowing, Lending, Equities, Protocol Revenue, Value Locked
- **Additional:** NFTs, Flows, Art & Collectibles, Gaming, Market Movers, Alt Metrics, Web Traffic, App Usage, Social

#### News

- **Content Types:** Latest (The Firehose), Most Popular (D1, M1, M6, All-Time), Custom Views / Favorite Topics, Staff Picks
- **Filters / Tags:** Deals, Democracy, Capital Markets, Institutional Investors, M&A, Organizations, Finance, Private Equity, Venture Capital, Policy, Central Banks, International Policy Making, Law, Lobbying, People, Regulation, U.S. Policy Making
- **Crypto Ecosystems:** Bridges, DeFi, Governance, Infrastructure, Layer 1s, Layer 2s and Scaling, People, Security, Social Platforms, Stablecoins
- **Markets:** Equities, Funds, Merits, Market Recap, Market Updates, Product, Public Equities, Token Programs, Commodities, Art, Crypto Infrastructure, Exchanges, Finance Firms, Fintech, Restructuring, Startups, Tech
- **NFT Sub-categories:** Art & Collectibles, Corporate NFTs, Fashion NFT, Gaming, Metaverse, NFT Brands, NFT Collections, NFT Infrastructure, Organizations, People

#### Funding

- Funding Landing / Summary page
- Companies and Deals database
- Boomtown (emerging companies)
- Investors directory
- **Funding Components:** Custom Table Views, Search and Filter, Company Detail, Blockchain Detail, Investor Detail

#### More Menu

- What's New / Change Log
- User Profile / Professional details
- Professional Services
- Upcoming Events
- APIs
- Stream AI (Multimodal — marked as new)
- Podcasts
- Newsletter
- Feedback
- ArchiveBot

### 8.5 User Profile & Preferences

| Setting | Description |
|---------|-------------|
| My Bookmarks | Saved articles and research |
| My Notification Settings | Email and push notification preferences |
| My Custom Search | Saved search queries |
| My APIs | API key management |
| My Downloads | Downloaded reports and data |
| Course Preferences | Learning track preferences |
| Light Mode / Dark Mode | Theme toggle |
| Font Settings | Typography customization |

---

## 9. Page Layouts

### 9.1 Homepage — Dark Mode

The dark mode homepage uses a near-black background (`~#0A0A0A`) with the following layout structure from top to bottom:

**Header Bar:**
- Left: Promotional banner area (e.g., sponsor badges)
- Center: The Block logo (white on dark)
- Right: "Compare Plans" and "Sign In" buttons, search icon, user menu

**Navigation Bar:**
- Horizontal list: LMAX Digital branding, Home, Research, Data, News, Prices, Learn Crypto dropdown
- Background: Dark, slightly lighter than the page background

**Main Content Area (Multi-column grid):**

1. **Latest Crypto News (Left column, ~60% width):**
   - Hero article card with large featured image
   - Below: Smaller article cards in a list format with thumbnails
   - Sponsored content ("Crypto IQ" widget) integrated inline

2. **Right Sidebar (~40% width):**
   - Sponsored ad unit (LMAX Digital)
   - "Most Read" list (numbered article links)
   - Additional sponsored units (ACCESS)
   - Secondary article cards

3. **"How much do you know about crypto?" — Interactive quiz/survey banner (full width)**

4. **Prices Ticker Section:**
   - Horizontal scrollable row of crypto prices (BTC, ETH, SOL, XRP, etc.)
   - Each shows: logo, ticker symbol, price, percentage change (green/red)

5. **Crypto Indices Section:**
   - Tabbed chart: "Top by Market Cap"
   - Line chart with value display (e.g., 140.26)
   - Time range selector buttons
   - Telegram channel promotion alongside

6. **Popular Crypto News Section:**
   - Full-width editorial content area
   - Featured article with large image
   - Grid of article cards (2–3 columns)
   - "52 key crypto hires, exits, and moves" type roundup articles

7. **Footer / Ad Area:**
   - Full-width sponsored banner

### 9.2 Homepage — Light Mode

Two variants are shown side-by-side. The light mode version mirrors the same layout structure as dark mode with the following theme differences:

- **Background:** White/off-white (`~#FFFFFF` / `~#F5F5F5`)
- **Text:** Dark gray to black
- **Cards:** White with subtle shadows or light gray borders
- **Navigation bar:** White background with dark text
- **Price indicators:** Green (up) and Red (down) remain consistent with dark mode
- **Charts:** Dark line on light background (inverted from dark mode)
- **Sponsored content:** Adapts to light backgrounds

### Layout Rules

- The homepage follows a **content-dense, news portal** layout pattern.
- Maximum content width should be constrained (approximately 1200–1400px) and centered.
- Sponsored/ad units have clearly defined placements and should be visually distinguishable from editorial content.
- All layout sections must adapt for both Light and Dark Mode without altering content structure.
- Price tickers use **green for positive** and **red for negative** percentage changes in both themes.

---

## 10. Audience Context

Understanding the audience is critical for design decisions. The Block's audience profile (2025):

### Scope & Reach

| Metric | Value |
|--------|-------|
| Monthly Page Views | 1.6M+ |
| Monthly Unique Users | 1M+ |
| Social Followers | 460K+ |
| Monthly Podcast Downloads | 90,000+ |

### Device Breakdown

| Device | Percentage |
|--------|------------|
| Mobile | 62% |
| Desktop | 38% |

**Design Implication:** Mobile-first responsive design is essential. All components, data tables, and charts must be optimized for smaller screens.

### Demographics

| Attribute | Value |
|-----------|-------|
| Gender — Male | 86% |
| Gender — Female | 15% |
| Age Range (Primary) | 25–54 (64%) |
| Income $100K+ | 85% |

### Industry Breakdown

| Industry | Approx. Share |
|----------|---------------|
| Media & Communications | ~33% (largest segment) |
| Technology & Innovation | ~17% |
| Crypto, Finance & Investment | ~11% |
| Research & Education | ~6% |
| Consulting & Professional Services | ~5% |
| Government, Civic & Social Services | ~2% |
| Traditional Enterprise | ~14% |
| Other | ~12% |

**Design Implications:**

- The audience is highly professional and financially sophisticated — avoid overly casual design choices.
- High income demographic expects a premium, polished visual experience.
- The dominant 25–54 age range is comfortable with data-dense interfaces.
- Given 62% mobile usage, ensure all data visualizations and tables have responsive mobile alternatives (e.g., horizontally scrollable tables, simplified chart views).

---

## 11. Appendix

### A. File Reference

| File | Contents |
|------|----------|
| `Design-Colors.png` | Full color system: scales, data palettes, brand colors |
| `Icons.png` | Core UI icon set |
| `Crypto-Logos.png` | 60+ cryptocurrency token logos |
| `Fiat-Logos.png` | 11 fiat currency symbol icons |
| `TheBlockWebsite-Navigation.png` | Complete site navigation and IA map |
| `Homepage Updates - Desktop-Darkmode.png` | Homepage layout — Dark Mode |
| `Homepage Updates - Desktop-Lightmode.png` | Homepage layout — Light Mode (two variants) |
| `TheBlock-Audience-Profile-2025.png` | Audience demographics and reach data |

### B. Glossary

| Term | Definition |
|------|------------|
| DXA | Document unit of measurement (1440 DXA = 1 inch) |
| IA | Information Architecture |
| CTA | Call to Action |
| WCAG | Web Content Accessibility Guidelines |
| ETF | Exchange-Traded Fund |
| DeFi | Decentralized Finance |
| NFT | Non-Fungible Token |
| L1 / L2 | Layer 1 / Layer 2 blockchain networks |

---

*This document was generated from visual design assets provided for The Block's design system. Hex values are approximations based on visual analysis and should be verified against the source Figma/design tool files for exact values.*
