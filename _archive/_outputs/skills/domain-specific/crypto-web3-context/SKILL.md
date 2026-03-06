---
name: crypto-web3-context
description: Crypto and Web3 product context for a PM at The Block. Provides blockchain terminology (DeFi, L1/L2, TVL, MEV, staking), market data concepts (price feeds, order books, on-chain metrics), crypto-specific PRD vocabulary (tokenomics, governance, liquidity), and regulatory awareness. Use when working on crypto products, blockchain features, The Block data products, DeFi analysis, token specifications, or Web3 product requirements.
---

# Crypto and Web3 Product Context

## Purpose

Provide accurate crypto and Web3 domain knowledge for product management at The Block. Encode blockchain terminology, market data concepts, and crypto-specific PM patterns so Claude produces specifications, analyses, and documentation with correct industry vocabulary. Frame everything from a PM perspective, not an engineering perspective.

## When to Use

- Writing PRDs or specs for crypto data products
- Analyzing on-chain metrics or market data features
- Creating requirements for DeFi, NFT, or token-related features
- Discussing The Block's products (news, data dashboards, Campus, Simon)
- Reviewing or generating content involving blockchain terminology
- Drafting regulatory-aware product documentation

## Examples

**Example 1: Crypto data dashboard PRD**
```
User: "Write a PRD for a new TVL tracking dashboard on The Block Data"
Claude: [Uses crypto-web3-context]

# TVL Tracking Dashboard PRD

## TL;DR
Add a Total Value Locked (TVL) dashboard to The Block Data that tracks
aggregate and per-protocol TVL across L1 and L2 chains with historical trends.

## Problem
- Users currently rely on third-party tools (DefiLlama) for TVL data
- No integrated view alongside The Block's existing market data
- Missing chain-level breakdowns (Ethereum L1 vs Arbitrum/Optimism L2)

## Solution
- Real-time TVL aggregation across top 50 DeFi protocols
- Chain filter: L1 (Ethereum, Solana, Avalanche) and L2 (Arbitrum, Optimism, Base)
- Protocol category breakdown: Lending, DEX, Derivatives, Yield, Bridge
- Historical charts with 7d/30d/90d/1y views

## Success Metrics
| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| Data page views | 0 | 5k/week | 90 days |
| API endpoint usage | 0 | 200 calls/day | 60 days |
```

**Example 2: Regulatory flag in a spec**
```
User: "Add a token price alerts feature to the mobile app"
Claude: [Uses crypto-web3-context]

## Regulatory Considerations
> IMPORTANT: Price alerts for tokens classified as securities under the
> Howey Test may create liability. Consult legal before including:
> - Tokens flagged by SEC enforcement actions
> - Tokens with active regulatory proceedings
> - Any "buy/sell signal" language in alert copy
>
> Recommended: Use neutral language ("Price crossed $X") rather than
> directional language ("Token is up 50%").
```

## Blockchain Terminology Reference

### Network Architecture

| Term | Definition (PM Context) |
|------|------------------------|
| L1 (Layer 1) | Base blockchain (Ethereum, Solana, Bitcoin). Handles consensus and settlement. Product impact: data latency, finality time. |
| L2 (Layer 2) | Scaling solution built on L1 (Arbitrum, Optimism, Base, zkSync). Product impact: lower fees, faster confirmation, separate data indexing. |
| Rollup | L2 type that bundles transactions and posts proofs to L1. Optimistic (fraud proofs, 7-day withdrawal) vs ZK (validity proofs, instant finality). |
| Sidechain | Independent chain with own consensus bridged to a main chain (Polygon PoS). Not a true L2. |
| RPC Node | API endpoint for reading/writing blockchain data. Product impact: uptime, rate limits, provider selection (Alchemy, Infura, QuickNode). |

### DeFi Concepts

| Term | Definition (PM Context) |
|------|------------------------|
| TVL (Total Value Locked) | USD value of assets deposited in a protocol. Primary health metric for DeFi products. |
| DEX (Decentralized Exchange) | On-chain trading venue using AMMs (Uniswap, Curve) or order books (dYdX). |
| AMM (Automated Market Maker) | Algorithm-based liquidity instead of order books. Key params: pool depth, slippage, impermanent loss. |
| Impermanent Loss | Loss from providing liquidity when token prices diverge. Only realized on withdrawal. |
| Yield Farming | Depositing tokens to earn rewards (fees + token emissions). Key metric: APY vs APR. |
| Lending Protocol | Borrow/lend markets (Aave, Compound). Key metrics: utilization rate, liquidation threshold. |
| Staking | Locking tokens to validate transactions (PoS). Key metrics: staking ratio, reward rate, unbonding period. |
| MEV (Maximal Extractable Value) | Profit from reordering transactions in a block. Product impact: transaction ordering, user-facing slippage. |
| Gas Fees | Transaction cost on EVM chains. Measured in gwei. Product impact: UX friction, batching strategies. |

### Market Data Concepts

| Term | Definition (PM Context) |
|------|------------------------|
| Market Cap | Price x Circulating Supply. Fully Diluted = Price x Max Supply. |
| Volume | Trading volume across exchanges. Distinguish: spot vs derivatives, CEX vs DEX. |
| Price Feed | Real-time token price data. Sources: CEX APIs, DEX on-chain, oracles (Chainlink). |
| Order Book | Bid/ask depth on centralized exchanges. Measures liquidity and spread. |
| OHLCV | Open/High/Low/Close/Volume candlestick data. Standard for charting APIs. |
| On-Chain Metrics | Data derived from blockchain transactions: active addresses, transaction count, whale movements, exchange flows. |
| Oracle | Service providing off-chain data on-chain (Chainlink, Pyth). Critical for DeFi price accuracy. |

### PM Vocabulary

| Term | Definition (PM Context) |
|------|------------------------|
| Tokenomics | Token supply, distribution, utility, and emission schedule. Analyze for: inflation rate, vesting cliffs, unlock schedules. |
| Governance | Protocol decision-making via token voting. Analyze for: proposal frequency, voter participation, quorum requirements. |
| Airdrop | Free token distribution to users. Product impact: engagement spikes, data requirements (eligibility snapshots). |
| Token Gating | Restricting access based on token ownership. Product impact: wallet verification, NFT-based access control. |
| DAO (Decentralized Autonomous Organization) | Organization governed by smart contracts and token holders. Product impact: decision velocity, treasury management. |

## Crypto PRD Patterns

### Standard Sections for Crypto PRDs

Add these sections to any crypto product PRD:

```markdown
## Chain Support
- Supported chains: [List specific L1s and L2s]
- Data source: [On-chain indexer / API provider / Oracle]
- Refresh rate: [Block-level / 15s / 1min / hourly]

## Data Accuracy
- Price source: [Aggregated from N exchanges / single source]
- Staleness threshold: [Max age before data is flagged stale]
- Discrepancy handling: [Median of 3 sources / weighted average]

## Regulatory Considerations
- [ ] Legal review required for [jurisdiction/feature]
- [ ] No investment advice language in copy
- [ ] Compliance with [relevant regulation]
```

### Crypto-Specific Acceptance Criteria Patterns

```markdown
- [ ] TVL data refreshes within 60 seconds of on-chain state change
- [ ] Price feeds show source attribution (exchange name)
- [ ] All monetary values display USD and native token denomination
- [ ] Chain selector defaults to Ethereum, remembers user preference
- [ ] Historical data available from protocol launch date
- [ ] Stale data (>5 min old) displays warning indicator
```

## Regulatory Awareness Framework

### When to Flag for Legal Review

Flag any feature that:
- Displays price predictions or directional signals
- Enables token purchases or swaps (even via redirect)
- Uses language implying investment returns
- Involves user-submitted financial data
- Targets specific jurisdictions (US, EU, Singapore, Hong Kong)

### Key Regulatory Bodies

| Body | Jurisdiction | Relevance |
|------|-------------|-----------|
| SEC | United States | Securities classification, enforcement actions |
| CFTC | United States | Derivatives, futures markets |
| MiCA | European Union | Comprehensive crypto asset regulation |
| MAS | Singapore | Digital payment token licensing |
| SFC | Hong Kong | Virtual asset trading platforms |
| FinCEN | United States | AML/KYC requirements |

### Safe Language Patterns

| Instead of | Use |
|-----------|-----|
| "Buy now before it goes up" | "Current price: $X" |
| "This token will moon" | "Price has increased X% over 30 days" |
| "Investment opportunity" | "Market data overview" |
| "Guaranteed returns" | Never use this. Flag any instance. |

## Data Integrity Patterns

For crypto data products, implement verification layers:

```typescript
interface DataFeedConfig {
  sources: string[];          // Minimum 3 independent sources
  staleness_threshold_ms: number;  // Max age before warning
  discrepancy_threshold_pct: number; // Max variance between sources
  fallback_strategy: "median" | "weighted" | "halt";
}

const defaultConfig: DataFeedConfig = {
  sources: ["binance", "coinbase", "kraken"],
  staleness_threshold_ms: 300000,    // 5 minutes
  discrepancy_threshold_pct: 2.0,    // 2% max variance
  fallback_strategy: "median",
};
```

## Success Criteria

- [ ] All crypto terminology used correctly (L1 vs L2, AMM vs order book, APY vs APR)
- [ ] PRDs include Chain Support, Data Accuracy, and Regulatory sections
- [ ] No investment advice language in any user-facing copy
- [ ] Data sources are attributed and staleness is handled
- [ ] Specifications are PM-focused (requirements, not implementation)

## Copy/Paste Ready

```
"Write a PRD for a new crypto data feature on The Block"
"Help me spec out a DeFi dashboard with TVL tracking"
"Review this crypto product spec for regulatory issues"
"What on-chain metrics should we track for this L2 feature?"
"Draft acceptance criteria for a token analytics page"
```
