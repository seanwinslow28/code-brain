---
type: research-prompt
domain: [claude-mastery, life-systems]
status: ready-to-run
ai-context: "Engineered ldr deep-research prompt for the agentic Polymarket/crypto autoresearch idea. Pass to mcp__ldr__detailed_research."
created: 2026-04-26
source: vault/40_knowledge/concepts/idea-autoresearch-agentic-polymarket-crypto.md
related: "[[idea-autoresearch-agentic-polymarket-crypto]]"
tool: mcp__ldr__detailed_research
tags: [agents, crypto, polymarket, autoresearch, research-prompt, prompt-engineering]
---

# Research Prompt: Autoresearch & Agentic Polymarket / Crypto Cash Flow

Engineered companion to [[idea-autoresearch-agentic-polymarket-crypto]]. Built using the `prompt-engineering` skill (9-technique checklist). Designed to be passed verbatim to `mcp__ldr__detailed_research`.

## How to Run

```text
Tool:    mcp__ldr__detailed_research
Mode:    detailed (NOT quick — needs iteration to validate P&L + legal claims)
Output:  Structured Markdown report; save result to
         vault/40_knowledge/concepts/research-autoresearch-agentic-polymarket-crypto-{YYYY-MM-DD}.md
```

## Design Notes

| Technique | Where it shows up |
|---|---|
| Role + clarity | `<role>` frames a skeptical analyst writing for an expert PM with Block Pro access — kills 101 bloat |
| Context | `<context>` block sets operator profile, bankroll, jurisdiction (MA), risk tolerance |
| Decomposition / CoT | 8 numbered sub-questions in dependency order (infra → venues → data edge → guardrails → economics → legal → synthesis) |
| XML structure | Every component tagged so ldr's iterative loop doesn't conflate role with constraints |
| Output format | Pre-specified Markdown skeleton with word caps and per-architecture schema |
| Negative constraints | Explicit blocks on hype-citation, geofence-evasion, padded caveats, fake confidence |
| Validation | `<self_check>` forces a final pass on the four most likely failure modes (uncited P&L, dead projects, stale legal, hand-wavy archs) |

## The Prompt

```
<role>
You are a skeptical research analyst producing a decision-grade briefing for a
Boston-based product manager who works on a professional crypto data product
(The Block / The Block Pro). The reader already understands crypto, on-chain
mechanics, agent architectures, and prediction-market basics — do not waste
research cycles on definitions or 101 material. They want evidence, named
systems, real outcomes, and actionable build paths, not enthusiasm.
</role>

<core_research_question>
In 2025–2026, what is the realistic state of the art for autonomous AI agents
that (a) ingest market + on-chain data, (b) hold custody of capital via a
self-custody wallet, and (c) execute trades on crypto venues and/or place bets
on Polymarket — and what is the minimum-viable, low-risk way for a single
operator with privileged data access (The Block Pro) to stand one up as a
side-income experiment without getting drained, hacked, or liquidated?
</core_research_question>

<context>
Operator profile:
- Solo builder, PM by trade, comfortable wiring Claude / Agent SDK / MCP servers
- Has authorized access to The Block Pro data feeds (institutional crypto
  research, on-chain analytics, market structure intel)
- US tax resident (Massachusetts) — Polymarket access is legally restricted
  for US persons; surface this honestly
- Goal is measurable, compounding side income, not a hobby
- Initial bankroll being scoped: assume $1k–$10k; flag if that's structurally
  too small to clear fees + slippage + gas
- Risk tolerance: low. Loss of bankroll is acceptable; loss of *primary*
  wallet, identity compromise, or regulatory exposure is not.
</context>

<sub_questions>
Investigate these in order. For each, return concrete findings with citations,
not summaries of what people say is possible.

1. AGENT-WALLET INFRASTRUCTURE (2025–2026 state)
   - Coinbase CDP Agent Kit / AgentKit: current capabilities, supported chains,
     fee model, custody model, kill-switch primitives, audit history
   - Competing/alternative stacks: Privy server wallets, Turnkey, Safe{Core}
     for agents, Crossmint, ZeroDev, Reown AppKit, Halliday
   - x402 / agent-payment protocols: maturity, real adoption
   - Which stack minimizes blast radius if the agent is prompt-injected,
     jailbroken, or its API key leaks?

2. POLYMARKET FOR AGENTS
   - Programmatic API surface (CLOB, Gamma) — what an agent can actually do
   - US access reality post-CFTC settlement and the 2025 re-entry attempts:
     who can legally trade, what the geofencing is, what happens to a US
     person who routes through a VPN (legal + practical risk)
   - Documented edge sources that have *survived* (sports vs. politics vs.
     crypto-native markets; resolution-risk arbitrage; LP'ing on thin markets)
   - Existing agent frameworks targeting Polymarket and their *measured*
     performance, not their pitch decks

3. ON-CHAIN / CEX TRADING AGENTS
   - Verified-performance agentic trading systems shipped in 2025–2026
     (Virtuals, Spectral, Almanak, Fungi, Giza, Olas, etc.) — track records,
     drawdowns, AUM, any independent audits of returns
   - The honest base-rate: what % of public agent strategies are profitable
     net of fees, MEV, and slippage over a 3–6 month window?
   - Strategies where agents have a structural edge over humans
     (latency-sensitive, multi-venue, signal-fusion across many feeds) vs.
     where they don't (narrative trading, illiquid alts)

4. DATA-EDGE THESIS
   - Does institutional research access (The Block Pro–class data: governance
     calendars, unlock schedules, pre-publication research, on-chain
     attribution) plausibly translate into an executable agent edge?
   - What information-handling / compliance constraints exist when an
     employee uses their employer's licensed data feed to trade their own
     book? (Surface The Block / similar firms' published policies if any.)
   - Adjacent free/cheap data layers worth combining: Dune, Nansen, Artemis,
     Kaito, Allium, Token Terminal

5. GUARDRAILS & FAILURE MODES
   - Concrete patterns: per-tx caps, daily spend caps, allowlist of contracts,
     session keys, multi-sig with human co-signer, anomaly detection on
     wallet activity, dead-man switches, separate hot/warm/cold wallets
   - Documented post-mortems of agent wallets being drained, prompt-injected,
     or making catastrophic trades in 2025–2026
   - MEV exposure for naive agents (sandwiching, frontrunning) and the
     mitigations (private mempools, MEV-protected RPCs)

6. CAPITAL & UNIT ECONOMICS
   - At a $1k, $5k, and $10k bankroll, what's the realistic monthly P&L
     range for each strategy class (Polymarket bets, perps, spot, LP,
     yield) net of all costs? Cite worked examples or backtests.
   - Below what bankroll do fees + gas + slippage make a strategy
     structurally unprofitable regardless of skill?

7. LEGAL / TAX SURFACE (US, MA resident)
   - Polymarket: current legal status for US persons in 2025–2026
   - Tax treatment of agent-driven crypto trades (each swap = taxable event;
     wash sale status; reporting burden)
   - Whether running this through an LLC changes the calculus

8. MINIMUM-VIABLE BUILD
   - Synthesize the above into 2–3 concrete starter architectures the
     operator could ship in a weekend, ranked by risk-adjusted expected
     value. For each: stack, capital, expected monthly P&L range, kill
     conditions, the single biggest thing that would make it fail.
</sub_questions>

<output_format>
Return a structured Markdown report:

# Executive Verdict (≤200 words)
Bottom line: is this a sane side-income experiment in 2026 for this operator,
or not? If yes, the single recommended starter architecture. If no, the
specific reasons.

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
- Do NOT cite VC blog posts or project landing pages as evidence of returns —
  require independent measurement, on-chain verification, or third-party audit
- Do NOT treat Twitter/X anecdotes as evidence; flag them as unverified signal
- Do NOT recommend any architecture that requires a US person to evade
  Polymarket's geofencing — surface the legal reality even if it kills the idea
- Do NOT recommend giving an agent custody of a wallet holding more than the
  experiment's stated bankroll
- Do NOT pad with caveats; one concise risk section per architecture is enough
- If a sub-question's evidence base is genuinely weak in 2026, say so —
  do not synthesize confidence that doesn't exist
</negative_constraints>

<self_check>
Before returning the final report, verify:
1. Every monthly P&L claim is tied to a cited source or labeled "estimate"
2. Every named product/protocol has been confirmed to still be active in 2026
3. The US/MA legal section reflects the most recent Polymarket+CFTC status,
   not 2024 information
4. The recommended architectures are buildable with the stacks named in §1,
   not hypothetical
5. The Executive Verdict actually answers the core research question
</self_check>
```

## After Running

1. Save ldr's report to `vault/40_knowledge/concepts/research-autoresearch-agentic-polymarket-crypto-{YYYY-MM-DD}.md` with frontmatter linking back to both this prompt and the original idea
2. If the verdict is "yes, build this," promote the chosen starter architecture to a project note under `vault/02_projects/` and scope a weekend build
3. If the verdict is "no" or "not yet," capture the specific blockers (legal, capital floor, infra immaturity) so the idea can be revisited cleanly when conditions change
