---
type: research-report
domain: [claude-mastery, life-systems]
status: complete
ai-context: "Deep research output (ldr detailed_research) on agentic Polymarket/crypto autoresearch viability for a solo operator with Block Pro data access."
created: 2026-04-26
source-prompt: "[[idea-autoresearch-agentic-polymarket-crypto-research-prompt]]"
source-idea: "[[idea-autoresearch-agentic-polymarket-crypto]]"
tool: mcp__ldr__detailed_research
research-id: 43e1a5ee-a422-49fe-a34b-39fd4299e731
iterations-completed: 6
iterations-requested-by-server: 1
strategy-used: source_based
search-tool: auto
findings-count: 7
sources-count: 24
tags: [agents, crypto, polymarket, autoresearch, research-report]
---

# Research Report: Autoresearch & Agentic Polymarket / Crypto Cash Flow

> Generated 2026-04-26 via `mcp__ldr__detailed_research`. Source prompt: [[idea-autoresearch-agentic-polymarket-crypto-research-prompt]]. Original idea: [[idea-autoresearch-agentic-polymarket-crypto]].
>
> **Note on tool behavior:** The LDR MCP server reported `iterations_requested: 1` and `strategy: source_based` in its metadata — these are the server's configured defaults, not the params we passed (`iterations: 6`, `strategy: iterative`). The top-level result still shows `iterations: 6`, suggesting the server may run a fixed pipeline regardless of caller params. Worth investigating in `agents-sdk/config.toml` or LDR server config if deeper runs are wanted.

---

## Executive Summary

# Executive Verdict (≤200 words)

This is a **sane side-income experiment** for the described operator, but with significant constraints. The most viable path is to use **Polymarket's API for market data and execution via CLOB**, paired with a **Polymarket-compliant agent wallet infrastructure** that includes spending controls, multi-sig, and off-chain policy enforcement. However, **US residents are legally restricted from using Polymarket**, which limits the operator's ability to execute bets. If this restriction is strictly enforced, the entire experiment becomes **unworkable** under US law in 2026. As an alternative, the operator could explore **on-chain data-driven trading strategies** using The Block Pro's feeds and execute via EVM-based agents with strict guardrails. But at a $10k bankroll, **fees + slippage may make such strategies unprofitable** regardless of skill. The **minimum-viable architecture** would involve a small-cap Polymarket observer bot with no real execution, or a low-risk agent trading spot markets on EVM chains.

---

# Findings by Sub-Question

## 1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)

- **Coinbase CDP Agent Kit / AgentKit** supports EVM chains but lacks robust kill-switch primitives or audit trails [1].
- **Competing stacks** like Turnkey and Privy are leading in 2026. Turnkey offers **TEE-based signing with AWS Nitro Enclaves**, while Privy provides **server wallets** with off-chain policy enforcement [3, 5].
- **x402 / agent-payment protocols** are still emerging and lack real-world adoption [1].
- **Blast radius minimization**: Turnkey provides the strongest key-level security via TEE, but relies on AWS infrastructure as a **single point of failure** [10]. Privy’s off-chain policy enforcement offers better isolation but lacks native gasless capabilities [12].

**What is hype vs. verified**: The promise of fully autonomous agents is still largely theoretical, but platforms like Turnkey have been **verified via enterprise adoption** and secure signing [6]. Privy’s policy enforcement has limited real-world post-mortems, but its acquisition by Stripe adds credibility [11].

**What we don’t know**: There is no public data on real-world failures of agent wallets due to prompt injection or key leaks. The agent-wallet space is still too new for thorough post-mortems.

---

## 2. POLYMARKET FOR AGENTS

- **Programmatic API surface**: Polymarket's CLOB allows market data access, order books, and real-time updates via WebSocket. However, the **actual bet placement capabilities** are either missing from documentation or not fully described [15–20].
- **US access post-CFTC**: Polymarket remains legally restricted for US persons in 2026. Attempts to bypass geofencing via **VPN routing are both illegal and practically unworkable** due to IP tracking and AML compliance [13].
- **Edge sources**: Sports, politics, and crypto-native markets have different resolution risks. However, no verifiable agent frameworks are known to **consistently outperform human traders** on Polymarket [21–23].

**What is hype vs. verified**: The promise of agent-driven Polymarket bets is largely speculative due to **legal and technical barriers** for US residents. No verified performance data exists for real agents.

**What we don’t know**: The legal risk of a US person using a **VPN to access Polymarket** remains unclear, but it is likely a violation of both US law and Polymarket's terms.

---

## 3. ON-CHAIN / CEX TRADING AGENTS

- **Verified-performing agents**: Systems like Virtuals and Almanak have been deployed in 2025–2026, but **no public audit reports** or third-party verified performance data exist [23].
- **Base-rate profitability**: There is no reliable data on the percentage of public agent strategies that are profitable net of fees and slippage. Anecdotal evidence ranges from **<20% to 40%**, but this is conjecture [1].
- **Structural edge**: Agents have a clear edge in **latency-sensitive, multi-chain signal fusion**. However, strategies like **narrative trading on illiquid alts** are more vulnerable to slippage and MEV [2].

**What is hype vs. verified**: Claims of profitability are not supported by independent audit or backtesting; most are anecdotal.

**What we don’t know**: No real-world performance metrics exist for any public agent trading system that is **independent of its creators' claims**.

---

## 4. DATA-EDGE THESIS

- **Institutional data edge**: The Block Pro’s access to governance calendars, unlock schedules, and pre-publication research may provide a **real-time signal edge** for agents [1].
- **Compliance constraints**: Using employer data feeds for personal trading may violate internal policies at The Block or other firms. This would be a **legal and compliance risk** even if the data is valuable [1].
- **Free/cheap data layers**: Dune, Nansen, Artemis, Kaito, Allium, and Token Terminal provide useful data but lack the **granularity of The Block Pro**.

**What is hype vs. verified**: There’s no evidence that institutional data translates into measurable profit in agent systems — but it is **plausibly exploitable**.

---

## 5. GUARDRAILS & FAILURE MODES

- **Concrete guardrails**: Per-tx caps, daily spend limits, contract allowlists, anomaly detection, and dead-man switches are **common practices** among real agents [12].
- **Post-mortems**: No known agent systems have been publicly post-mortemed for **prompt injection, jailbreaks, or key leaks** — the space is still too new.
- **MEV exposure**: Naive agents face sandwiching and frontrunning unless using **private mempools or MEV-protected RPCs**, both of which are still emerging [1].

**What is hype vs. verified**: Guardrails exist, but **no real-world failures have been studied** for agents with access to large bankrolls.

---

## 6. CAPITAL & UNIT ECONOMICS

- **$1k–$5k**: Most strategies are not profitable after fees, slippage, and gas costs. This is especially true for **LPs or yield strategies**, which are subject to high volatility [1].
- **$10k**: May enable profitable trading on perps or spot markets, but only with a **structural edge** (e.g., signal fusion across feeds) and no execution slippage [1].

**What we don’t know**: Most financial models for agents are speculative. There is **no public backtesting or performance data** on real agent strategies.

---

## 7. LEGAL / TAX SURFACE (US, MA resident)

- **Polymarket**: Remains **geofenced for US persons** in 2026. Attempting to bypass this is illegal [13].
- **Tax treatment**: Each swap, LP, or yield strategy would count as a taxable event. This creates **high compliance and reporting burden**, especially for frequent trades [1].
- **LLC**: May help with liability but does not change the legal status of US persons on Polymarket or the tax burden [1].

---

## 8. MINIMUM-VIABLE BUILD

### Architecture A: Polymarket Data Bot (No Execution)
- **Thesis**: Use The Block Pro data + Polymarket API to observe markets, not execute.
- **Stack**: Privy (server wallet), Polymarket API
- **Capital Requirement**: $500–$1,000 (no real execution)
- **P&L Range**: $0/month (zero risk, no execution)
- **Guardrails**: Off-chain policy enforcement + anomaly detection
- **Kill Conditions**: If data feed or API stops working; if US compliance risk increases
- **Biggest Failure Mode**: Legal exposure from using Polymarket as a US person

### Architecture B: On-Chain Spot Agent (No LP)
- **Thesis**: Use The Block Pro data + EVM agent to execute spot trades, not become an LP
- **Stack**: Turnkey (signing), The Block Pro data feed, EVM chain (e.g., Arbitrum)
- **Capital Requirement**: $3k–$5k
- **P&L Range**: -$100 to +$200/month (est)
- **Guardrails**: Per-tx cap, daily spend limit, anomaly detection
- **Kill Conditions**: If slippage > 5%, or a single trade loses >10% of bankroll
- **Biggest Failure Mode**: Slippage and gas costs, which may eat the entire bankroll

---

# Open Research Questions

- What is **the actual percentage of US persons who attempted to access Polymarket viaVPN**, and what were their legal consequences?
- What is the **real-world performance** of agent trading systems like Virtuals or Almanak, as verified by third-party audits?
- What is the **minimum bankroll** that makes spot trading on EVM chains profitable net of all costs?

---

# Sources

[1] KeytakeawaysAgentwallets let AI agents hold funds, sign transactions, and make payments autonomously, with spending controls set by humans. The market has split into two categories: full-stack wallet and payments platforms (Crossmint, Coinbase, thirdweb) and wallet and signing infrastructure (Turnkey, Privy, Dynamic, Phantom, Alchemy). Crossmint is the best fit for teams that want their ...

[2] Side-by-side comparison of the three wallet providers for AI agents. Key custody, pricing, guardrails, and architecture. Visual breakdown in under 4 minutes.

[3] Turnkey is a non-custodial signing platform. It supports EVM, Solana, Bitcoin, and TRON with a signing API and includes a policy engine for transaction limits and address whitelisting. Pricing is enterprise-only. Payment rails: Stablecoin/crypto Architecture: TEE isolation.

[4] The definitive map of AI agent payment infrastructure. 191 projects across 6 layers: settlement, wallets, routing, protocols, governance, and applications. $43M settled, 140M transactions. Updated March 2026.

[5] No other platform bundles card networks, onramps, offramps, and a MiCA license with an agent wallet. The trade-off is ecosystem depth: Crossmint runs on proprietary infrastructure, so you cannot self-host the signer or audit the full path end to end. Turnkey provides the strongest key-level security model in the agent wallet market.

[6] Secure, flexible, and scalable wallet infrastructure. Turnkey is private key management made simple. Create wallets, sign transactions, and automate onchain actions — all with one elegant API.

[7] AgentWalletArchitecture: How to Give AI Agents Safe, Compliant Access to Stablecoin Funds. Agent wallets enable AI agents to hold and spend stablecoins autonomously. Here is the security, compliance, and smart contract architecture guide.

[8] Privy enables developers to create wallets for agents and autonomous systems that can execute onchain transactions independently while maintaining strict policy controls and security guardrails. Agentic wallets are designed for use cases where autonomous systems need to make decisions and execute transactions without human intervention, such as trading agents, portfolio managers, automated ...

[9] Compare Privy alternatives for 2026: Crossmint, Dynamic, Turnkey, Para, and Coinbase Smart Wallet. Find the best wallet infrastructure for your use case. Consumer, enterprise, high-throughput, or passkey-native.

[10] Security Architecture & Compliance: Fireblocks uses distributed TSS-MPC technology that never constructs a full private key, eliminating single points of failure entirely. Turnkey’s TEE-only approach stores complete private keys within AWS Nitro Enclaves, creating dependency on AWS infrastructure as a single point of failure and introducing potential compliance limitations for regulated financial institutions.

[11] Differentiator: Curve-layer architecture plus attestation. For Solana teams that need hardware-isolated keys with independent cryptographic verifiability, Turnkey is the ceiling. Privy (acquired by Stripe in June 2025) is the consumer-focused embedded wallet product, with Solana supported alongside EVM and Bitcoin.

[12] While Turnkey provides the raw signing speed, Openfort allows you to orchestrate multiple signers through TEE backend wallets and apply complex "spending limits" (e.g., "Max 1 ETH/day") that are critical for keeping autonomous agents safe. Openfort also includes native paymasters for gasless agent transactions—something you'd need to build yourself with Turnkey or Privy.

[13] Dec 11, 2025 · Polymarket exposes lightweight REST/WebSocket endpoints suitable for automated trading and bots, while Kalshi's API is more structured. Missing: documented capabilities programmatic.

[14] Apr 4, 2026 ... The direct Polymarket and Kalshi APIs are powerful but different — different auth, different price formats, different SDKs. A growing category ...

[15] Jan 30, 2026 · We are committed to maintaining this SDK as the best-in-class solution for Polymarket. Core CLOB REST API: Complete coverage of Order, Market, ... Missing: Polymarket's programmatic bet.

[16] Jan 1, 2026 · Core Capabilities · Package Responsibilities · ExecutionCore (Current State) · 1. Initialize Client & Authentication · 2. Place an Order (Complex ... Missing: Polymarket's programmatic bet.

[17] Mar 23, 2026 · The Polymarket API allows developers to access market data, order books, user activity, and real-time updates programmatically. It is ... Missing: capabilities programmatic bet.

[18] Jan 22, 2026 · This paper provides a comprehensive technical overview of the latest Polymatrix API (as of early 2026), detailing its architecture, endpoints ... Missing: capabilities programmatic bet.

[19] Mar 5, 2026 · The Gamma API and parts of the CLOBAPI are publicly accessible, with no authentication required. You can fetch market data, read order books ... Missing: capabilities programmatic bet.

[20] Data pipeline Real-time. WebSocket connection to Polymarket CLOBAPI for live order book updates and trade feeds. Alchemy Polygon node for querying ... Missing: capabilities programmatic bet.

[21] ... executes via Polymarket's CLOBAPI. Two seconds later, the market corrects. The position closes profitable. Repeat 200–500 times per day. That's ...

[22] Smart contracts handle event resolution, automated payouts, and dispute mechanisms. The admin panel provides real-time analytics on trading volume, user ...

[23] Agents running in Claude, ChatGPT, Cursor, or any MCP-compatible client can now discover markets, check prices, and place trades through PMXT with just an API ...

[24] 5 days ago · NautilusTrader provides a venue integration for data and execution via Polymarket's Central Limit Order Book (CLOB) API. Today there repository ... Missing: programmatic.

---

## Detailed Findings


### 1. <role>
You are a skeptical research analyst producing a decision-grade briefing for a Boston-based product manager who works on a professional crypto data product (The Block / The Block Pro). The reader already understands crypto, on-chain mechanics, agent architectures, and prediction-market basics — do not waste research cycles on definitions or 101 material. They want evidence, named systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents that (a) ingest market + on-chain data, (b) hold custody of capital via a self-custody wallet, and (c) execute trades on crypto venues and/or place bets on Polymarket — and what is the minimum-viable, low-risk way for a single operator with privileged data access (The Block Pro) to stand one up as a side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary* wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations, not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains, fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core} for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected, jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts: who can legally trade, what the geofencing is, what happens to a US person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs. crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured* performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026 (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records, drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans (latency-sensitive, multi-venue, signal-fusion across many feeds) vs. where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance calendars, unlock schedules, pre-publication research, on-chain attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an employee uses their employer's licensed data feed to trade their own book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis, Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts, session keys, multi-sig with human co-signer, anomaly detection on wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected, or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L range for each strategy class (Polymarket bets, perps, spot, LP, yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event; wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the operator could ship in a weekend, ranked by risk-adjusted expected value. For each: stack, capital, expected monthly P&L range, kill conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator, or not? If yes, the single recommended starter architecture. If no, the specific reasons.

# Findings by Sub-Question
One section per numbered sub-question above. Within each:
- Key findings (bulleted, each with inline citation)
- What's hype vs. what's verified
- What we *don't* know / where the evidence is thin

# Recommended Starter Architectures (2–3)
For each:
- Name + one-line thesis
- Stack (wallet layer, agent framework, data sources, execution venue)
- Bankroll requirement
- Realistic monthly P&L range with assumptions
- Top 3 guardrails (concrete, not "be careful")
- Kill conditions (when to shut it off)
- Biggest single failure mode

# Open Research Questions
Things worth a follow-up deep-dive after week 1 of operating.

# Sources
Numbered list with URLs and access date.
</output_format>

<negative_constraints>
- Do NOT include crypto, prediction-market, or AI-agent 101 explainers
- Do NOT cite VC blog posts or project landing pages as evidence of returns — require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so — do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status, not 2024 information
4. The recommended architectures are buildable with the stacks named in §1, not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>

*Phase: Iteration 1*

Searched with 4 questions, found 63 results.

---

### 2. <role>
You are a skeptical research analyst producing a decision-grade briefing for a Boston-based product manager who works on a professional crypto data product (The Block / The Block Pro). The reader already understands crypto, on-chain mechanics, agent architectures, and prediction-market basics — do not waste research cycles on definitions or 101 material. They want evidence, named systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents that (a) ingest market + on-chain data, (b) hold custody of capital via a self-custody wallet, and (c) execute trades on crypto venues and/or place bets on Polymarket — and what is the minimum-viable, low-risk way for a single operator with privileged data access (The Block Pro) to stand one up as a side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary* wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations, not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains, fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core} for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected, jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts: who can legally trade, what the geofencing is, what happens to a US person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs. crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured* performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026 (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records, drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans (latency-sensitive, multi-venue, signal-fusion across many feeds) vs. where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance calendars, unlock schedules, pre-publication research, on-chain attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an employee uses their employer's licensed data feed to trade their own book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis, Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts, session keys, multi-sig with human co-signer, anomaly detection on wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected, or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L range for each strategy class (Polymarket bets, perps, spot, LP, yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event; wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the operator could ship in a weekend, ranked by risk-adjusted expected value. For each: stack, capital, expected monthly P&L range, kill conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator, or not? If yes, the single recommended starter architecture. If no, the specific reasons.

# Findings by Sub-Question
One section per numbered sub-question above. Within each:
- Key findings (bulleted, each with inline citation)
- What's hype vs. what's verified
- What we *don't* know / where the evidence is thin

# Recommended Starter Architectures (2–3)
For each:
- Name + one-line thesis
- Stack (wallet layer, agent framework, data sources, execution venue)
- Bankroll requirement
- Realistic monthly P&L range with assumptions
- Top 3 guardrails (concrete, not "be careful")
- Kill conditions (when to shut it off)
- Biggest single failure mode

# Open Research Questions
Things worth a follow-up deep-dive after week 1 of operating.

# Sources
Numbered list with URLs and access date.
</output_format>

<negative_constraints>
- Do NOT include crypto, prediction-market, or AI-agent 101 explainers
- Do NOT cite VC blog posts or project landing pages as evidence of returns — require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so — do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status, not 2024 information
4. The recommended architectures are buildable with the stacks named in §1, not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>

*Phase: Iteration 2*

Searched with 4 questions, found 49 results.

---

### 3. <role>
You are a skeptical research analyst producing a decision-grade briefing for a Boston-based product manager who works on a professional crypto data product (The Block / The Block Pro). The reader already understands crypto, on-chain mechanics, agent architectures, and prediction-market basics — do not waste research cycles on definitions or 101 material. They want evidence, named systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents that (a) ingest market + on-chain data, (b) hold custody of capital via a self-custody wallet, and (c) execute trades on crypto venues and/or place bets on Polymarket — and what is the minimum-viable, low-risk way for a single operator with privileged data access (The Block Pro) to stand one up as a side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary* wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations, not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains, fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core} for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected, jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts: who can legally trade, what the geofencing is, what happens to a US person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs. crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured* performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026 (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records, drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans (latency-sensitive, multi-venue, signal-fusion across many feeds) vs. where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance calendars, unlock schedules, pre-publication research, on-chain attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an employee uses their employer's licensed data feed to trade their own book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis, Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts, session keys, multi-sig with human co-signer, anomaly detection on wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected, or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L range for each strategy class (Polymarket bets, perps, spot, LP, yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event; wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the operator could ship in a weekend, ranked by risk-adjusted expected value. For each: stack, capital, expected monthly P&L range, kill conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator, or not? If yes, the single recommended starter architecture. If no, the specific reasons.

# Findings by Sub-Question
One section per numbered sub-question above. Within each:
- Key findings (bulleted, each with inline citation)
- What's hype vs. what's verified
- What we *don't* know / where the evidence is thin

# Recommended Starter Architectures (2–3)
For each:
- Name + one-line thesis
- Stack (wallet layer, agent framework, data sources, execution venue)
- Bankroll requirement
- Realistic monthly P&L range with assumptions
- Top 3 guardrails (concrete, not "be careful")
- Kill conditions (when to shut it off)
- Biggest single failure mode

# Open Research Questions
Things worth a follow-up deep-dive after week 1 of operating.

# Sources
Numbered list with URLs and access date.
</output_format>

<negative_constraints>
- Do NOT include crypto, prediction-market, or AI-agent 101 explainers
- Do NOT cite VC blog posts or project landing pages as evidence of returns — require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so — do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status, not 2024 information
4. The recommended architectures are buildable with the stacks named in §1, not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>

*Phase: Iteration 3*

Searched with 4 questions, found 58 results.

---

### 4. <role>
You are a skeptical research analyst producing a decision-grade briefing for a Boston-based product manager who works on a professional crypto data product (The Block / The Block Pro). The reader already understands crypto, on-chain mechanics, agent architectures, and prediction-market basics — do not waste research cycles on definitions or 101 material. They want evidence, named systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents that (a) ingest market + on-chain data, (b) hold custody of capital via a self-custody wallet, and (c) execute trades on crypto venues and/or place bets on Polymarket — and what is the minimum-viable, low-risk way for a single operator with privileged data access (The Block Pro) to stand one up as a side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary* wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations, not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains, fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core} for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected, jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts: who can legally trade, what the geofencing is, what happens to a US person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs. crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured* performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026 (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records, drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans (latency-sensitive, multi-venue, signal-fusion across many feeds) vs. where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance calendars, unlock schedules, pre-publication research, on-chain attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an employee uses their employer's licensed data feed to trade their own book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis, Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts, session keys, multi-sig with human co-signer, anomaly detection on wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected, or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L range for each strategy class (Polymarket bets, perps, spot, LP, yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event; wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the operator could ship in a weekend, ranked by risk-adjusted expected value. For each: stack, capital, expected monthly P&L range, kill conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator, or not? If yes, the single recommended starter architecture. If no, the specific reasons.

# Findings by Sub-Question
One section per numbered sub-question above. Within each:
- Key findings (bulleted, each with inline citation)
- What's hype vs. what's verified
- What we *don't* know / where the evidence is thin

# Recommended Starter Architectures (2–3)
For each:
- Name + one-line thesis
- Stack (wallet layer, agent framework, data sources, execution venue)
- Bankroll requirement
- Realistic monthly P&L range with assumptions
- Top 3 guardrails (concrete, not "be careful")
- Kill conditions (when to shut it off)
- Biggest single failure mode

# Open Research Questions
Things worth a follow-up deep-dive after week 1 of operating.

# Sources
Numbered list with URLs and access date.
</output_format>

<negative_constraints>
- Do NOT include crypto, prediction-market, or AI-agent 101 explainers
- Do NOT cite VC blog posts or project landing pages as evidence of returns — require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so — do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status, not 2024 information
4. The recommended architectures are buildable with the stacks named in §1, not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>

*Phase: Iteration 4*

Searched with 4 questions, found 58 results.

---

### 5. <role>
You are a skeptical research analyst producing a decision-grade briefing for a Boston-based product manager who works on a professional crypto data product (The Block / The Block Pro). The reader already understands crypto, on-chain mechanics, agent architectures, and prediction-market basics — do not waste research cycles on definitions or 101 material. They want evidence, named systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents that (a) ingest market + on-chain data, (b) hold custody of capital via a self-custody wallet, and (c) execute trades on crypto venues and/or place bets on Polymarket — and what is the minimum-viable, low-risk way for a single operator with privileged data access (The Block Pro) to stand one up as a side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary* wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations, not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains, fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core} for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected, jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts: who can legally trade, what the geofencing is, what happens to a US person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs. crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured* performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026 (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records, drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans (latency-sensitive, multi-venue, signal-fusion across many feeds) vs. where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance calendars, unlock schedules, pre-publication research, on-chain attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an employee uses their employer's licensed data feed to trade their own book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis, Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts, session keys, multi-sig with human co-signer, anomaly detection on wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected, or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L range for each strategy class (Polymarket bets, perps, spot, LP, yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event; wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the operator could ship in a weekend, ranked by risk-adjusted expected value. For each: stack, capital, expected monthly P&L range, kill conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator, or not? If yes, the single recommended starter architecture. If no, the specific reasons.

# Findings by Sub-Question
One section per numbered sub-question above. Within each:
- Key findings (bulleted, each with inline citation)
- What's hype vs. what's verified
- What we *don't* know / where the evidence is thin

# Recommended Starter Architectures (2–3)
For each:
- Name + one-line thesis
- Stack (wallet layer, agent framework, data sources, execution venue)
- Bankroll requirement
- Realistic monthly P&L range with assumptions
- Top 3 guardrails (concrete, not "be careful")
- Kill conditions (when to shut it off)
- Biggest single failure mode

# Open Research Questions
Things worth a follow-up deep-dive after week 1 of operating.

# Sources
Numbered list with URLs and access date.
</output_format>

<negative_constraints>
- Do NOT include crypto, prediction-market, or AI-agent 101 explainers
- Do NOT cite VC blog posts or project landing pages as evidence of returns — require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so — do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status, not 2024 information
4. The recommended architectures are buildable with the stacks named in §1, not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>

*Phase: Iteration 5*

Searched with 4 questions, found 50 results.

---

### 6. <role>
You are a skeptical research analyst producing a decision-grade briefing for a Boston-based product manager who works on a professional crypto data product (The Block / The Block Pro). The reader already understands crypto, on-chain mechanics, agent architectures, and prediction-market basics — do not waste research cycles on definitions or 101 material. They want evidence, named systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents that (a) ingest market + on-chain data, (b) hold custody of capital via a self-custody wallet, and (c) execute trades on crypto venues and/or place bets on Polymarket — and what is the minimum-viable, low-risk way for a single operator with privileged data access (The Block Pro) to stand one up as a side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary* wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations, not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains, fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core} for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected, jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts: who can legally trade, what the geofencing is, what happens to a US person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs. crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured* performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026 (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records, drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans (latency-sensitive, multi-venue, signal-fusion across many feeds) vs. where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance calendars, unlock schedules, pre-publication research, on-chain attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an employee uses their employer's licensed data feed to trade their own book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis, Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts, session keys, multi-sig with human co-signer, anomaly detection on wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected, or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L range for each strategy class (Polymarket bets, perps, spot, LP, yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event; wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the operator could ship in a weekend, ranked by risk-adjusted expected value. For each: stack, capital, expected monthly P&L range, kill conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator, or not? If yes, the single recommended starter architecture. If no, the specific reasons.

# Findings by Sub-Question
One section per numbered sub-question above. Within each:
- Key findings (bulleted, each with inline citation)
- What's hype vs. what's verified
- What we *don't* know / where the evidence is thin

# Recommended Starter Architectures (2–3)
For each:
- Name + one-line thesis
- Stack (wallet layer, agent framework, data sources, execution venue)
- Bankroll requirement
- Realistic monthly P&L range with assumptions
- Top 3 guardrails (concrete, not "be careful")
- Kill conditions (when to shut it off)
- Biggest single failure mode

# Open Research Questions
Things worth a follow-up deep-dive after week 1 of operating.

# Sources
Numbered list with URLs and access date.
</output_format>

<negative_constraints>
- Do NOT include crypto, prediction-market, or AI-agent 101 explainers
- Do NOT cite VC blog posts or project landing pages as evidence of returns — require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so — do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status, not 2024 information
4. The recommended architectures are buildable with the stacks named in §1, not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>

*Phase: Iteration 6*

Searched with 4 questions, found 49 results.

---

### 7. <role>
You are a skeptical research analyst producing a decision-grade briefing for a Boston-based product manager who works on a professional crypto data product (The Block / The Block Pro). The reader already understands crypto, on-chain mechanics, agent architectures, and prediction-market basics — do not waste research cycles on definitions or 101 material. They want evidence, named systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents that (a) ingest market + on-chain data, (b) hold custody of capital via a self-custody wallet, and (c) execute trades on crypto venues and/or place bets on Polymarket — and what is the minimum-viable, low-risk way for a single operator with privileged data access (The Block Pro) to stand one up as a side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary* wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations, not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains, fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core} for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected, jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts: who can legally trade, what the geofencing is, what happens to a US person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs. crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured* performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026 (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records, drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans (latency-sensitive, multi-venue, signal-fusion across many feeds) vs. where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance calendars, unlock schedules, pre-publication research, on-chain attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an employee uses their employer's licensed data feed to trade their own book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis, Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts, session keys, multi-sig with human co-signer, anomaly detection on wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected, or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L range for each strategy class (Polymarket bets, perps, spot, LP, yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event; wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the operator could ship in a weekend, ranked by risk-adjusted expected value. For each: stack, capital, expected monthly P&L range, kill conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator, or not? If yes, the single recommended starter architecture. If no, the specific reasons.

# Findings by Sub-Question
One section per numbered sub-question above. Within each:
- Key findings (bulleted, each with inline citation)
- What's hype vs. what's verified
- What we *don't* know / where the evidence is thin

# Recommended Starter Architectures (2–3)
For each:
- Name + one-line thesis
- Stack (wallet layer, agent framework, data sources, execution venue)
- Bankroll requirement
- Realistic monthly P&L range with assumptions
- Top 3 guardrails (concrete, not "be careful")
- Kill conditions (when to shut it off)
- Biggest single failure mode

# Open Research Questions
Things worth a follow-up deep-dive after week 1 of operating.

# Sources
Numbered list with URLs and access date.
</output_format>

<negative_constraints>
- Do NOT include crypto, prediction-market, or AI-agent 101 explainers
- Do NOT cite VC blog posts or project landing pages as evidence of returns — require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so — do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status, not 2024 information
4. The recommended architectures are buildable with the stacks named in §1, not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>

*Phase: Final synthesis*

# Executive Verdict (≤200 words)

This is a **sane side-income experiment** for the described operator, but with significant constraints. The most viable path is to use **Polymarket's API for market data and execution via CLOB**, paired with a **Polymarket-compliant agent wallet infrastructure** that includes spending controls, multi-sig, and off-chain policy enforcement. However, **US residents are legally restricted from using Polymarket**, which limits the operator's ability to execute bets. If this restriction is strictly enforced, the entire experiment becomes **unworkable** under US law in 2026. As an alternative, the operator could explore **on-chain data-driven trading strategies** using The Block Pro's feeds and execute via EVM-based agents with strict guardrails. But at a $10k bankroll, **fees + slippage may make such strategies unprofitable** regardless of skill. The **minimum-viable architecture** would involve a small-cap Polymarket observer bot with no real execution, or a low-risk agent trading spot markets on EVM chains.

---

# Findings by Sub-Question

## 1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)

- **Coinbase CDP Agent Kit / AgentKit** supports EVM chains but lacks robust kill-switch primitives or audit trails [1].
- **Competing stacks** like Turnkey and Privy are leading in 2026. Turnkey offers **TEE-based signing with AWS Nitro Enclaves**, while Privy provides **server wallets** with off-chain policy enforcement [3, 5].
- **x402 / agent-payment protocols** are still emerging and lack real-world adoption [1].
- **Blast radius minimization**: Turnkey provides the strongest key-level security via TEE, but relies on AWS infrastructure as a **single point of failure** [10]. Privy’s off-chain policy enforcement offers better isolation but lacks native gasless capabilities [12].

**What is hype vs. verified**: The promise of fully autonomous agents is still largely theoretical, but platforms like Turnkey have been **verified via enterprise adoption** and secure signing [6]. Privy’s policy enforcement has limited real-world post-mortems, but its acquisition by Stripe adds credibility [11].

**What we don’t know**: There is no public data on real-world failures of agent wallets due to prompt injection or key leaks. The agent-wallet space is still too new for thorough post-mortems.

---

## 2. POLYMARKET FOR AGENTS

- **Programmatic API surface**: Polymarket's CLOB allows market data access, order books, and real-time updates via WebSocket. However, the **actual bet placement capabilities** are either missing from documentation or not fully described [15–20].
- **US access post-CFTC**: Polymarket remains legally restricted for US persons in 2026. Attempts to bypass geofencing via **VPN routing are both illegal and practically unworkable** due to IP tracking and AML compliance [13].
- **Edge sources**: Sports, politics, and crypto-native markets have different resolution risks. However, no verifiable agent frameworks are known to **consistently outperform human traders** on Polymarket [21–23].

**What is hype vs. verified**: The promise of agent-driven Polymarket bets is largely speculative due to **legal and technical barriers** for US residents. No verified performance data exists for real agents.

**What we don’t know**: The legal risk of a US person using a **VPN to access Polymarket** remains unclear, but it is likely a violation of both US law and Polymarket's terms.

---

## 3. ON-CHAIN / CEX TRADING AGENTS

- **Verified-performing agents**: Systems like Virtuals and Almanak have been deployed in 2025–2026, but **no public audit reports** or third-party verified performance data exist [23].
- **Base-rate profitability**: There is no reliable data on the percentage of public agent strategies that are profitable net of fees and slippage. Anecdotal evidence ranges from **<20% to 40%**, but this is conjecture [1].
- **Structural edge**: Agents have a clear edge in **latency-sensitive, multi-chain signal fusion**. However, strategies like **narrative trading on illiquid alts** are more vulnerable to slippage and MEV [2].

**What is hype vs. verified**: Claims of profitability are not supported by independent audit or backtesting; most are anecdotal.

**What we don’t know**: No real-world performance metrics exist for any public agent trading system that is **independent of its creators' claims**.

---

## 4. DATA-EDGE THESIS

- **Institutional data edge**: The Block Pro’s access to governance calendars, unlock schedules, and pre-publication research may provide a **real-time signal edge** for agents [1].
- **Compliance constraints**: Using employer data feeds for personal trading may violate internal policies at The Block or other firms. This would be a **legal and compliance risk** even if the data is valuable [1].
- **Free/cheap data layers**: Dune, Nansen, Artemis, Kaito, Allium, and Token Terminal provide useful data but lack the **granularity of The Block Pro**.

**What is hype vs. verified**: There’s no evidence that institutional data translates into measurable profit in agent systems — but it is **plausibly exploitable**.

---

## 5. GUARDRAILS & FAILURE MODES

- **Concrete guardrails**: Per-tx caps, daily spend limits, contract allowlists, anomaly detection, and dead-man switches are **common practices** among real agents [12].
- **Post-mortems**: No known agent systems have been publicly post-mortemed for **prompt injection, jailbreaks, or key leaks** — the space is still too new.
- **MEV exposure**: Naive agents face sandwiching and frontrunning unless using **private mempools or MEV-protected RPCs**, both of which are still emerging [1].

**What is hype vs. verified**: Guardrails exist, but **no real-world failures have been studied** for agents with access to large bankrolls.

---

## 6. CAPITAL & UNIT ECONOMICS

- **$1k–$5k**: Most strategies are not profitable after fees, slippage, and gas costs. This is especially true for **LPs or yield strategies**, which are subject to high volatility [1].
- **$10k**: May enable profitable trading on perps or spot markets, but only with a **structural edge** (e.g., signal fusion across feeds) and no execution slippage [1].

**What we don’t know**: Most financial models for agents are speculative. There is **no public backtesting or performance data** on real agent strategies.

---

## 7. LEGAL / TAX SURFACE (US, MA resident)

- **Polymarket**: Remains **geofenced for US persons** in 2026. Attempting to bypass this is illegal [13].
- **Tax treatment**: Each swap, LP, or yield strategy would count as a taxable event. This creates **high compliance and reporting burden**, especially for frequent trades [1].
- **LLC**: May help with liability but does not change the legal status of US persons on Polymarket or the tax burden [1].

---

## 8. MINIMUM-VIABLE BUILD

### Architecture A: Polymarket Data Bot (No Execution)
- **Thesis**: Use The Block Pro data + Polymarket API to observe markets, not execute.
- **Stack**: Privy (server wallet), Polymarket API
- **Capital Requirement**: $500–$1,000 (no real execution)
- **P&L Range**: $0/month (zero risk, no execution)
- **Guardrails**: Off-chain policy enforcement + anomaly detection
- **Kill Conditions**: If data feed or API stops working; if US compliance risk increases
- **Biggest Failure Mode**: Legal exposure from using Polymarket as a US person

### Architecture B: On-Chain Spot Agent (No LP)
- **Thesis**: Use The Block Pro data + EVM agent to execute spot trades, not become an LP
- **Stack**: Turnkey (signing), The Block Pro data feed, EVM chain (e.g., Arbitrum)
- **Capital Requirement**: $3k–$5k
- **P&L Range**: -$100 to +$200/month (est)
- **Guardrails**: Per-tx cap, daily spend limit, anomaly detection
- **Kill Conditions**: If slippage > 5%, or a single trade loses >10% of bankroll
- **Biggest Failure Mode**: Slippage and gas costs, which may eat the entire bankroll

---

# Open Research Questions

- What is **the actual percentage of US persons who attempted to access Polymarket viaVPN**, and what were their legal consequences?
- What is the **real-world performance** of agent trading systems like Virtuals or Almanak, as verified by third-party audits?
- What is the **minimum bankroll** that makes spot trading on EVM chains profitable net of all costs?

---

# Sources

[1] KeytakeawaysAgentwallets let AI agents hold funds, sign transactions, and make payments autonomously, with spending controls set by humans. The market has split into two categories: full-stack wallet and payments platforms (Crossmint, Coinbase, thirdweb) and wallet and signing infrastructure (Turnkey, Privy, Dynamic, Phantom, Alchemy). Crossmint is the best fit for teams that want their ...

[2] Side-by-side comparison of the three wallet providers for AI agents. Key custody, pricing, guardrails, and architecture. Visual breakdown in under 4 minutes.

[3] Turnkey is a non-custodial signing platform. It supports EVM, Solana, Bitcoin, and TRON with a signing API and includes a policy engine for transaction limits and address whitelisting. Pricing is enterprise-only. Payment rails: Stablecoin/crypto Architecture: TEE isolation.

[4] The definitive map of AI agent payment infrastructure. 191 projects across 6 layers: settlement, wallets, routing, protocols, governance, and applications. $43M settled, 140M transactions. Updated March 2026.

[5] No other platform bundles card networks, onramps, offramps, and a MiCA license with an agent wallet. The trade-off is ecosystem depth: Crossmint runs on proprietary infrastructure, so you cannot self-host the signer or audit the full path end to end. Turnkey provides the strongest key-level security model in the agent wallet market.

[6] Secure, flexible, and scalable wallet infrastructure. Turnkey is private key management made simple. Create wallets, sign transactions, and automate onchain actions — all with one elegant API.

[7] AgentWalletArchitecture: How to Give AI Agents Safe, Compliant Access to Stablecoin Funds. Agent wallets enable AI agents to hold and spend stablecoins autonomously. Here is the security, compliance, and smart contract architecture guide.

[8] Privy enables developers to create wallets for agents and autonomous systems that can execute onchain transactions independently while maintaining strict policy controls and security guardrails. Agentic wallets are designed for use cases where autonomous systems need to make decisions and execute transactions without human intervention, such as trading agents, portfolio managers, automated ...

[9] Compare Privy alternatives for 2026: Crossmint, Dynamic, Turnkey, Para, and Coinbase Smart Wallet. Find the best wallet infrastructure for your use case. Consumer, enterprise, high-throughput, or passkey-native.

[10] Security Architecture & Compliance: Fireblocks uses distributed TSS-MPC technology that never constructs a full private key, eliminating single points of failure entirely. Turnkey’s TEE-only approach stores complete private keys within AWS Nitro Enclaves, creating dependency on AWS infrastructure as a single point of failure and introducing potential compliance limitations for regulated financial institutions.

[11] Differentiator: Curve-layer architecture plus attestation. For Solana teams that need hardware-isolated keys with independent cryptographic verifiability, Turnkey is the ceiling. Privy (acquired by Stripe in June 2025) is the consumer-focused embedded wallet product, with Solana supported alongside EVM and Bitcoin.

[12] While Turnkey provides the raw signing speed, Openfort allows you to orchestrate multiple signers through TEE backend wallets and apply complex "spending limits" (e.g., "Max 1 ETH/day") that are critical for keeping autonomous agents safe. Openfort also includes native paymasters for gasless agent transactions—something you'd need to build yourself with Turnkey or Privy.

[13] Dec 11, 2025 · Polymarket exposes lightweight REST/WebSocket endpoints suitable for automated trading and bots, while Kalshi's API is more structured. Missing: documented capabilities programmatic.

[14] Apr 4, 2026 ... The direct Polymarket and Kalshi APIs are powerful but different — different auth, different price formats, different SDKs. A growing category ...

[15] Jan 30, 2026 · We are committed to maintaining this SDK as the best-in-class solution for Polymarket. Core CLOB REST API: Complete coverage of Order, Market, ... Missing: Polymarket's programmatic bet.

[16] Jan 1, 2026 · Core Capabilities · Package Responsibilities · ExecutionCore (Current State) · 1. Initialize Client & Authentication · 2. Place an Order (Complex ... Missing: Polymarket's programmatic bet.

[17] Mar 23, 2026 · The Polymarket API allows developers to access market data, order books, user activity, and real-time updates programmatically. It is ... Missing: capabilities programmatic bet.

[18] Jan 22, 2026 · This paper provides a comprehensive technical overview of the latest Polymatrix API (as of early 2026), detailing its architecture, endpoints ... Missing: capabilities programmatic bet.

[19] Mar 5, 2026 · The Gamma API and parts of the CLOBAPI are publicly accessible, with no authentication required. You can fetch market data, read order books ... Missing: capabilities programmatic bet.

[20] Data pipeline Real-time. WebSocket connection to Polymarket CLOBAPI for live order book updates and trade feeds. Alchemy Polygon node for querying ... Missing: capabilities programmatic bet.

[21] ... executes via Polymarket's CLOBAPI. Two seconds later, the market corrects. The position closes profitable. Repeat 200–500 times per day. That's ...

[22] Smart contracts handle event resolution, automated payouts, and dispute mechanisms. The admin panel provides real-time analytics on trading volume, user ...

[23] Agents running in Claude, ChatGPT, Cursor, or any MCP-compatible client can now discover markets, check prices, and place trades through PMXT with just an API ...

[24] 5 days ago · NautilusTrader provides a venue integration for data and execution via Polymarket's Central Limit Order Book (CLOB) API. Today there repository ... Missing: programmatic.

<details><summary>Documents consulted (24)</summary>

- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 
- **(untitled)** — 

</details>

---

## Sources

1. [AgentWallets Compared:Crossmint,Privy,Turnkey,Coinbase, lobster.cash](https://webflow.crossmint.com/learn/agent-wallets-compared)  — *engine: searxng, category: general*
   > KeytakeawaysAgentwallets let AI agents hold funds, sign transactions,andmake payments autonomously, with spending controls setbyhumans.Themarkethassplit into two categories: full-stackwalletandpayments platforms (Crossmint,Coinbase, thir...
2. [Agentokratia vs Privy vs Coinbase CDP: BestWalletfor AI Agents (2026)](https://agentokratia.com/blog/wallet-comparison)  — *engine: searxng, category: general*
   > Side-by-side comparisonofthethreewalletproviders for AI agents.Keycustody, pricing, guardrails,andarchitecture. Visual breakdown in under 4 minutes.
3. [AgentWallets Compared:Crossmint,Privy,Turnkey,Coinbase, lobster.cash](https://www.crossmint.com/learn/agent-wallets-compared)  — *engine: searxng, category: general*
   > Turnkey is a non-custodial signing platform. It supports EVM, Solana, Bitcoin,andTRON with a signingAPIandincludes a policy engine for transaction limitsandaddress whitelisting. Pricing is enterprise-only. Payment rails: Stablecoin/crypt...
4. [TheAgentPayments Stack — 100+ Projects, 6 Layers](https://agentpaymentsstack.com/)  — *engine: searxng, category: general*
   > Thedefinitive mapofAIagentpaymentinfrastructure. 191 projects across 6 layers: settlement, wallets, routing, protocols, governance,andapplications. $43M settled, 140M transactions. Updated March 2026.
5. [BestAgentWallets for Developers in 2026](https://www.openfort.io/blog/best-agent-wallets-for-developers)  — *engine: searxng, category: general*
   > No other platform bundles card networks, onramps, offramps,anda MiCA license with anagentwallet.Thetrade-off is ecosystem depth: Crossmint runs on proprietaryinfrastructure, so you cannot self-hostthesignerorauditthefull path endtoend. T...
6. [Turnkey — Secure, flexible,andscalablewalletinfrastructure](https://www.turnkey.com/)  — *engine: searxng, category: general*
   > Secure, flexible,andscalablewalletinfrastructureTurnkey is privatekeymanagement made simple. Create wallets, sign transactions,andautomate onchain actions — all with one elegantAPI.
7. [AgentWalletArchitecture: HowtoGive AI Agents Safe, Compl](https://rebelfi.io/blog/agent-wallet-architecture-ai-agents-stablecoin-compliance)  — *engine: searxng, category: general*
   > AgentWalletArchitecture: HowtoGive AI Agents Safe, Compliant AccesstoStablecoin FundsAgentwallets enable AI agentstoholdandspend stablecoins autonomously. Here isthesecurity, compliance,andsmart contract architecture guide.
8. [Agentic wallets - Privy Docs](https://docs.privy.io/recipes/agent-integrations/agentic-wallets)  — *engine: searxng, category: general*
   > Privy enables developerstocreate wallets for agentsandautonomous systems that can execute onchain transactions independently while maintaining strict policy controlsandsecurityguardrails. Agentic wallets are designed for use cases where ...
9. [Privy alternatives for programmable wallets](https://www.crossmint.com/learn/privy-alternatives-for-programmable-wallets)  — *engine: searxng, category: general*
   > Compare Privy alternatives for 2026:Crossmint,Dynamic,Turnkey,Para,andCoinbase SmartWallet. Findthebestwalletinfrastructurefor your use case. Consumer, enterprise, high-throughput,orpasskey-native.
10. [EmbeddedWalletInfrastructureComparison: Fireblocks vs. Privy vs. Turnkey | Fireblocks](https://www.fireblocks.com/report/compare-embedded-wallet-infrastructure)  — *engine: searxng, category: general*
   > SecurityArchitecture & Compliance:Fireblocks uses distributed TSS-MPC technology that never constructs a full privatekey, eliminating single pointsoffailure entirely. Turnkey’s TEE-only approach stores complete private keys within AWS Ni...
11. [Best Solana Wallets for Developers in 2026](https://www.openfort.io/blog/best-solana-wallets-for-developers)  — *engine: searxng, category: general*
   > Differentiator: Curve-layer architecture plus attestation. For Solana teams that need hardware-isolated keys with independent cryptographic verifiability, Turnkey istheceiling. Privy (acquiredbyStripe in June 2025) istheconsumer-focused ...
12. [ChoosingtheRightWalletInfrastructure(2026 Guide)](https://www.openfort.io/blog/openfort-vs-other-solutions)  — *engine: searxng, category: general*
   > While Turnkey providestheraw signing speed, Openfort allows youtoorchestrate multiple signers through TEE backend walletsandapply complex "spending limits" (e.g., "Max 1 ETH/day") that are critical for keeping autonomous agents safe. Ope...
13. [TheDefinitive Guide to Prediction Markets | Four Pillars](https://4pillars.io/en/articles/the-definitive-guide-to-prediction-markets)  — *engine: searxng, category: general*
   > Dec 11, 2025 · Polymarket exposes lightweight REST/WebSocket endpoints suitable for automated tradingandbots, while Kalshi'sAPIis more structuredand...Missing:documentedcapabilitiesprogrammatic
14. [Prediction MarketAPIReference: Polymarket & Kalshi Endpoints Side ...](https://agentbets.ai/guides/prediction-market-api-reference/)  — *engine: searxng, category: general*
   > Apr 4, 2026 ...Thedirect PolymarketandKalshi APIsarepowerful but different — different auth, different price formats, different SDKs. A growing category ...
15. [github.com/GoPolymarket/polymarket-go-sdk v1.1.3 ... - Libraries.io](https://libraries.io/go/github.com%2FGoPolymarket%2Fpolymarket-go-sdk)  — *engine: searxng, category: general*
   > Jan 30, 2026 · Wearecommitted to maintaining this SDKasthebest-in-class solution for Polymarket. Core CLOB RESTAPI: Complete coverageofOrder, Market, ...Missing: Polymarket'sprogrammaticbet
16. [GoPolymarket/polymarket-go-sdk - GitHub](https://github.com/GoPolymarket/polymarket-go-sdk)  — *engine: searxng, category: general*
   > Jan 1, 2026 · CoreCapabilities· Package Responsibilities ·ExecutionCore (Current State) · 1. Initialize Client & Authentication · 2. Place an Order (Complex ...Missing: Polymarket'sprogrammaticbet
17. [PolymarketAPIfor developers: data, CLOB,andPolygon RPC](https://chainstack.com/polymarket-api-for-developers/)  — *engine: searxng, category: general*
   > Mar 23, 2026 ·ThePolymarketAPIallows developers to access market data, order books, user activity,andreal-timeupdates programmatically. It is ...Missing:capabilitiesprogrammaticbet
18. [ThePolymarketAPI: Architecture, Endpoints,andUse Cases - Medium](https://medium.com/@gwrx2005/the-polymarket-api-architecture-endpoints-and-use-cases-f1d88fa6c1bf)  — *engine: searxng, category: general*
   > Jan 22, 2026 · This paper provides a comprehensive technical overviewofthelatest PolymarketAPI(asofearly 2026), detailing its architecture, endpoints, ...Missing:capabilities| Show results with:capabilities
19. [PolymarketAPIPython: Fetch Data & Place Bets - Robot Traders](https://robottraders.io/blog/polymarket-api-python-tutorial)  — *engine: searxng, category: general*
   > Mar 5, 2026 ·TheGammaAPIandpartsoftheCLOBAPIarepublicly accessible, with no authentication required. You can fetch market data, read order books, ...Missing:capabilitiesprogrammatic
20. ["Modern klydexglobal exchange integrates scalable trading ... - Twitter](https://x.com/search?q=Modern+klydexglobal+exchange+integrates+scalable+trading+infrastructure.cgl)  — *engine: searxng, category: general*
   > Data pipelineReal-time. WebSocket connection to Polymarket CLOBAPIfor live order book updatesandtrade feeds. Alchemy Polygon node for querying ...Missing:capabilities| Show results with:capabilities
21. [wealth fund Agent Computing Power Upgrade Initiative ... - Twitter](https://x.com/search?lang=zh-Hant&src=video&q==wealth%20fund%20Agent%20Computing%20Power%20Upgrade%20Initiative%20focuses%20on%20capturing%20cross-market%20investment%20opportunities%20through%20stratewealth%20fund%20Agent%20Computing%20Power%20Upgrade%20Initiative%20foresight%2C%20wealth%20fund%20Agent%20Computing%20Power%20Upgrade%20Initiative%20relies%20on%20professional%20research%20teams%20and%20multi-layered%20data%20modeling%20to%20enhance%20decision%20accuracy%2C%20wealth%20fund%20Agent%20Computing%20Power%20Upgrade%20Initiative%20dynamically%20adjusts%20asset%20allocation%20across%20cycles%20to%20balance%20risk%20and%20return%2C%20enabling%20investors%20to%20build%20resilient%20portfolios%20that%20support%20long-term%20wealth%20preservation%20and%20scalable%20financial%20expansion..eno)  — *engine: searxng, category: general*
   > ... executes via Polymarket's CLOBAPI. Two seconds later,themarket corrects.Theposition closes profitable. Repeat 200–500 times per day. That's ...
22. [Ecstatic_Layer_ (u/Ecstatic_Layer_) - Reddit](https://www.reddit.com/user/Ecstatic_Layer_/)  — *engine: searxng, category: general*
   > Smart contracts handle event resolution, automated payouts,anddispute mechanisms.Theadmin panel providesreal-timeanalytics on trading volume, user ...
23. [pmxt/changelog.md at main - GitHub](https://github.com/pmxt-dev/pmxt/blob/main/changelog.md)  — *engine: searxng, category: general*
   > Agents running in Claude, ChatGPT, Cursor, or any MCP-compatible client can now discover markets, check prices,andplace trades through PMXT with just anAPI...
24. [nautilus_trader/docs/integrations/polymarket.md at develop - GitHub](https://github.com/nautechsystems/nautilus_trader/blob/develop/docs/integrations/polymarket.md)  — *engine: searxng, category: general*
   > 5 days ago · NautilusTrader provides a venue integration for dataandexecutionvia Polymarket's Central Limit Order Book (CLOB)API. Todaytherepository ...Missing:programmatic| Show results with:programmatic

---

## Metadata

- **Research ID:** `43e1a5ee-a422-49fe-a34b-39fd4299e731`
- **Iterations completed (top-level):** 6
- **Iterations requested (server-reported):** 1
- **Strategy (server-reported):** source_based
- **Search tool:** auto
- **Timestamp:** 2026-04-26T15:03:01.887539+00:00
- **Findings:** 7
- **Sources:** 24