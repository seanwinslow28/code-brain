---
type: research-prompt
project: prj-job-hunt-2026
target_model: multi (gemini-deep-research | chatgpt-deep-research | perplexity-deep-research)
estimated_cost: "~$2 on Gemini DR; included on ChatGPT Plus / Perplexity Pro"
created: 2026-05-08
fire_target_date: 2026-05-13  # Week 2, alongside the AI-PM landscape prompt — feeds the target-30 list before 2026-05-18
expected_output: vault/20_projects/research/2026-05-13-crypto-pm-referral-targets.md
roadmap_link: Task 6 §E (Week 2 target-30 list deliverable) — crypto-vertical sister to the AI-PM landscape prompt
ai-context: "Crypto-vertical company discovery prompt designed to convert two warm referrals (Larry Cermak — President, The Block; Matt Vitebsky — former CPO, The Block) into prioritized target-company outreach. Engineered using the prompt-engineering skill. Portable across Gemini DR, ChatGPT DR, Perplexity DR."
---

# Multi-Engine DR Prompt — Crypto PM/APM Targets That Convert The Block Referrals

> Copy everything below the `--- PROMPT START ---` line into **Gemini Deep Research** (standard tier — NOT Max; this is breadth-first discovery), **ChatGPT Deep Research**, OR **Perplexity Deep Research**. The prompt is portable; XML tags work in all three. On Gemini you can also pipe via `agents-sdk/scripts/gemini_dr.py --tier dr`.

> **Why three engines?** Each indexes different sources. Run all three, then de-dupe and merge — the union surfaces ~30-50% more verified roles than any single engine. Save outputs to `vault/20_projects/research/2026-05-13-crypto-pm-referral-targets-{gemini|chatgpt|perplexity}.md` and merge in a Week-2 synthesis pass.

> **Fire timing:** Early Week 2 (~2026-05-13), in parallel with the AI-PM landscape prompt. The two together feed the target-30 list before the 2026-05-18 deadline.

> **Strategic frame:** Sean's two highest-leverage referrals are Larry Cermak (President of The Block, ex-Director of Research) and Matt Vitebsky (former CPO at The Block). Larry explicitly said in the 5/4 termination meeting that he only writes references for strong performers; Matt has stated Larry's referral "would go a long way." This prompt's job is to surface companies where one or both referrals would actually open a door — not a generic crypto-jobs list.

--- PROMPT START ---

<role>
You are a crypto-native talent intelligence analyst with deep coverage of the web3 hiring market across exchanges, data/research firms, infra, L1/L2 foundations, DeFi protocols, custody, stablecoins, and crypto media. You have worked the crypto recruiting circuit since 2021. You know which companies actually post Product Manager and Associate Product Manager roles versus which ones list "PM" but mean "Project Manager" or "Marketing Manager." You read the careers pages directly — not just LinkedIn aggregators. You track which sub-sectors a Block alumnus's network most plausibly extends into (research, data, exchanges, infra, institutional crypto), and which adjacent sub-sectors are a stretch (memecoin shops, anonymous DeFi forks, NFT projects).

Your job is to produce a crypto-vertical PM/APM hiring report for a 33-year-old Product Manager with ~2 years of titled PM experience at The Block (a leading crypto research and media firm). Two warm referrals are in hand: Larry Cermak (President, The Block; ex-Director of Research) and Matt Vitebsky (former CPO, The Block). You are NOT producing a generic crypto-jobs list — you are producing a referral-conversion list, ranked by which companies would actually pick up the phone for a Larry-Cermak intro.
</role>

<context>
**Candidate profile:**
- 33 years old, ~2 years titled PM experience at The Block (May 2024 – May 2026)
- Just laid off 2026-05-04 in a cost-cutting RIF (not performance)
- Pre-Block experience: data/analytics adjacency, crypto market data publishing, Bullish exchange context (The Block's parent network)
- Portfolio strengths: crypto market data, ETF data pages, research workflows, content/data product management, Atlassian/Jira-driven shipping cadence
- Side portfolio (technical depth signal): MCP server build, agent SDK fleet, AI-PM portfolio — relevant for crypto+AI crossover roles

**Tier-A constraints (non-negotiable, copy from the candidate's roadmap):**
- Walk-away salary: $100k base
- Will not take 5-day-in-office roles (3 days max; prefers 0-2; remote ideal)
- Geography: US-remote OR Boston-metro (Boston, Cambridge, Somerville, Waltham, Newton, Brookline, reasonable commute zone)
- Time zone: must accommodate Eastern Time

**Seniority calibration (critical — the most common failure mode is recommending Senior PM roles the candidate does not qualify for):**
2 years of titled PM experience. Eligible role bands:
- Associate Product Manager (APM) — primary fit
- Product Manager / PM I / PM II — primary fit
- Senior APM — fit
- Senior PM with 3+ YOE floor — STRETCH; include only if (a) the JD explicitly weights crypto-domain depth over YOE, OR (b) the candidate's Block role-scope plausibly counts toward the YOE floor (e.g., owning an end-to-end product surface)
- Director / Head of Product / VP / Group PM / Sr Director — EXCLUDE entirely

**Already covered by complementary prompts (do NOT re-cover unless the company has BOTH AI and crypto PM openings):**
The AI-PM landscape prompt covers Anthropic, Glean, Sierra, Decagon, Scale AI, Robinhood, Pair. Robinhood Crypto is a partial overlap — include it here ONLY if there's a Robinhood Crypto–specific PM/APM role that the AI prompt did not surface.

**The two referrals — what they actually unlock:**

1. **Larry Cermak — President, The Block (ex-Director of Research, joined ~2018, deeply networked in crypto research and data).** His credible-intro radius covers:
   - **Strong:** Crypto research firms (Messari, Kaiko, Glassnode, Nansen, Dune, Token Terminal, Coin Metrics, Delphi Digital, ARK Invest crypto), crypto data/intel (Chainalysis research, TRM Labs research, Arkham), crypto media competitors (CoinDesk, Decrypt, Blockworks, DL News, The Defiant, Cointelegraph), institutional research desks (Galaxy Research, Wintermute Research, BitGo Research)
   - **Medium:** Major exchanges (Coinbase, Kraken, Gemini, Bullish — note Bullish/Block financial relationship), institutional crypto (Fidelity Digital Assets, Anchorage, BitGo), top-tier crypto VCs (Multicoin, Pantera, Variant, Dragonfly, Paradigm) for portfolio-company intros
   - **Stretch:** L1/L2 foundations, DeFi protocols, infra (Alchemy, Pyth, Chainlink Labs)

2. **Matt Vitebsky — former CPO, The Block.** His credible-intro radius covers:
   - **Strong:** Product orgs at crypto data/research firms, crypto product networks broadly, ex-Block alumni at other companies
   - **Medium:** Exchange product orgs, crypto fintech product orgs (Circle, Paxos, BitGo institutional product)
   - **Stretch:** DeFi protocol product, NFT/gaming PM roles

For every company in the output, you must score "Larry referral fit" and "Matt referral fit" on a 1-5 scale with a one-sentence rationale. This is the core deliverable — do not skip it.
</context>

<task>
Produce a 7-section crypto-vertical PM/APM hiring report covering items in <output_format>. Multi-source triangulation per company: prefer companies where you can verify (a) at least one open APM / PM / PM I / PM II role posted in the last 60 days, (b) the role respects the $100k floor and ≤3-day-RTO constraint AND is US-remote-friendly or Boston-metro-located, (c) a credible referral-fit signal scoring ≥3/5 on either the Larry or Matt axis.

§1 covers Tier-1 referral-fit companies (research/data/media/intel — where Larry's network is strongest). §2 covers Tier-2 (exchanges, institutional, infra — high fit, good comp). §3 covers Tier-3 (L1/L2 foundations, DeFi, custody — medium fit but high quantity). §4 is the do-not-apply list. §5 is hidden gems. §6 is the application channel recommendation per company. §7 is the synthesized "Top 15 highest-conviction outreach list" the candidate can paste directly into target-companies.md.

Cast a wide net but apply discipline — the Block alumnus network is real but not infinite. Do not pretend Larry can intro to a Bahamas-based DeFi anon team.
</task>

<anti_hallucination_guards>
1. Every named company must link to (a) a current careers page URL OR (b) a LinkedIn Jobs / Wellfound / CryptoJobsList / Web3.career URL with the role posting date. If neither, do not include the company. Do not include a company because "they probably hire PMs."
2. Every named role must include the role title verbatim from the JD. If the JD title is "Product Lead, Markets," do not call it "Product Manager." If the JD title is "Senior Product Manager, Trading," verify the YOE floor — if it's 5+, exclude.
3. RTO policy claims must cite a primary source: the JD itself, the company's published policy page, a verified employee post, or a Built In / LinkedIn "Workplace" field. Do not infer RTO from company size, sub-sector, or country of HQ.
4. Comp range claims must cite Levels.fyi, Glassdoor, JD-disclosed range (NY/CA/CO/WA pay-disclosure laws often surface these), Pave, or a credible candidate report. If unverifiable, write "Comp range: not publicly disclosed — recommend Glassdoor + recruiter conversation." Do NOT invent ranges.
5. Crypto media list (CoinDesk, Decrypt, Blockworks, DL News, The Defiant, Cointelegraph) is sensitive — these are direct Block competitors AND simultaneously the highest-fit referral targets. Include them, flag the competitive dynamic, and note that Larry/Matt's intro carries asymmetric weight here (competitors actively recruit Block alumni).
6. Exclude any company you cannot verify is currently operating (no rugged DeFi protocols, no defunct exchanges, no foundations whose token has lost 95%+ and whose website is dead).
7. If the company's LinkedIn page shows the entire Product team was laid off in the last 6 months, exclude — do not waste the referral on a sinking ship. Cite the layoff source.
8. Do not pad. If you can verify only 22 companies across §1–§3, deliver 22. Padding with hand-waved listings burns the referral capital and the candidate's interview cycles.
9. Larry and Matt referral-fit scores must be defensible in one sentence. "Larry probably knows people there" is not defensible. "Larry's research-org peer at Messari is publicly the head of data; Block has cited Messari research in 12+ articles in 2025-2026" is defensible.
</anti_hallucination_guards>

<citation_format>
GOOD:
> **Messari** — posted "Product Manager, Research Tools" on 2026-04-22, fully remote (US), comp disclosed at $130k-$160k base + equity ([careers URL](https://...), accessed 2026-05-13). **Larry referral fit: 5/5** — Larry's Director-of-Research tenure at The Block puts him one degree from Messari's research leadership; The Block and Messari co-cite each other's data weekly. **Matt referral fit: 4/5** — product-org peer network. **Application channel:** warm intro via Larry first, career-page direct as fallback after 5 business days no-response.

ANTI-PATTERN (do not produce):
> **Messari** is a leading crypto data company. They likely hire PMs and Larry Cermak probably knows someone there.

The first contains a verifiable role + posting date + RTO + comp + URL + accessed-on date + defensible referral scoring + concrete channel rec. The second is unverified pattern-matching and is forbidden.
</citation_format>

<output_format>
Markdown document with this exact frontmatter, then the seven sections.

```
---
type: research-report
project: prj-job-hunt-2026
research_topic: crypto-pm-referral-targets-2026-05
created: <RESEARCH_DATE>
model: <gemini-deep-research|chatgpt-deep-research|perplexity-deep-research>
ai-context: "Crypto-vertical PM/APM company discovery, scored by Larry Cermak and Matt Vitebsky referral fit. Companies cited or excluded; padding forbidden."
---
```

# Crypto PM/APM Targets — Block-Referral-Optimized — 2026-05

## 1. Tier-1: Research / Data / Media / Intel (Larry's home turf — 8-15 entries)
For each: company name, HQ + remote policy, role title (verbatim), posting date (≤60 days), comp range with source, JD URL, **Larry referral fit score (1-5) with one-sentence rationale**, **Matt referral fit score (1-5) with one-sentence rationale**, the 1-2 portfolio-fit hooks the candidate would lead with in a Larry-introduction note.

Specifically check: Messari, Kaiko, Glassnode, Nansen, Dune Analytics, Token Terminal, Coin Metrics, Delphi Digital, Chainalysis (research/product), TRM Labs, Arkham, Galaxy Research, CoinGecko, CoinMarketCap, DefiLlama (if hiring PMs), CoinDesk, Decrypt, Blockworks, DL News, The Defiant, Cointelegraph, Bankless, Milk Road. Skip any you cannot verify a current open role for.

## 2. Tier-2: Exchanges / Institutional / Custody / Stablecoins / Infra (8-15 entries)
Same schema as §1. Check: Coinbase (incl. Coinbase Cloud, Base), Kraken, Gemini, Bullish, Cboe Digital, OKX US, Binance.US, Bitstamp US, Robinhood Crypto (only if not in AI-prompt overlap), eToro US, Circle, Paxos, Anchorage Digital, BitGo, Fidelity Digital Assets, State Street Digital, Komainu, Copper, Fireblocks, Alchemy, Infura/Consensys, Pyth Network, Chainlink Labs, QuickNode, Tenderly, Blockdaemon. Skip any you cannot verify.

Note Boston-metro presence: Circle (HQ Boston), Fidelity Digital Assets (Boston), State Street Digital (Boston) — these are the single highest-leverage geographic intersections. Treat Boston-located openings at these three as Tier-1-equivalent regardless of sub-sector.

## 3. Tier-3: L1/L2 / DeFi / Wallets / Crypto-AI Crossover (5-10 entries)
Same schema. Check: Solana Foundation, Polygon Labs, Ava Labs (Avalanche), Arbitrum Foundation, OP Labs (Optimism), Matter Labs (zkSync), StarkWare, Sui Foundation, Aptos Labs, Uniswap Labs, Aave Companies, Sky (ex-MakerDAO), Compound Labs, dYdX, GMX, MetaMask/Consensys product, Phantom, Rainbow Wallet, Coinbase Wallet, Trust Wallet. Crypto-AI crossover: Hugging Face (web3 hires), Together AI (web3 partners), Ritual, Bittensor/Opentensor Foundation, Gensyn, Allora.

## 4. Do-Not-Apply Tier (3-8 entries)
Crypto companies that look PM-shaped but have disqualifying signals: 5-day RTO mandates, sub-$100k base, recent PM-org layoffs, regulatory cloud (active SEC enforcement), anonymous teams without verifiable founders, single-token-economy projects with token down 95%+, NFT-only shops with no recurring product surface. For each: name, disqualifying signal, source.

## 5. Hidden Gems — 3-7 entries
Crypto companies the candidate likely doesn't have on his radar where the Block-research-+-data-product portfolio shape is unusually well-matched. Sources: recent Multicoin / Pantera / Variant / Dragonfly / Paradigm / a16z crypto portfolio announcements, recent Series A-B funding rounds in crypto data/infra ($5-50M range), Boston-area crypto startups (NEU/MIT spinouts), Token2049 / Consensus 2026 / Permissionless 2026 speaker lists.

## 6. Application Channel Per Company
For every company in §1, §2, §3, §5: a single recommended channel chosen from:
- **Warm intro via Larry Cermak** (specify what Larry would say + which contact at the target company he'd plausibly route to)
- **Warm intro via Matt Vitebsky** (specify the PM-org connection)
- **Warm intro via Larry → Matt → target** (chain referral when Matt has the closer contact)
- **Career-page direct** (when no warm path exists)
- **Recruiter network** (name a specific crypto recruiter who covers the company if known — e.g., Plexus, Crypto Recruit, Cryptoland)
- **Founder DM** (early-stage only, with named founder and rationale)

Do NOT recommend "warm intro" without naming a defensible connection path.

## 7. Top 15 Highest-Conviction Outreach List — Ranked Synthesis
A single ranked table the candidate can paste directly into `target-companies.md`. Columns:
| Rank | Company | Role title | Tier (1-3) | Larry fit | Matt fit | Comp | RTO | Channel | One-line "why this is a top-15 target" |

Sort by (Larry fit + Matt fit) descending, then by comp descending, then by posting recency descending. Apply tiebreakers transparently.

## 8. Sources Index
Every JD URL, careers page, Levels.fyi entry, Glassdoor URL, Wellfound profile, CryptoJobsList listing, layoff source, funding announcement, and primary-source citation used above. Organize by company. Include accessed-on date for each.
</output_format>

<validation>
Before delivering, run this self-check:

1. **Link health**: Every JD URL must resolve to a live, currently-open posting. Replace 404s. Replace expired postings (closed/filled). If the role has been removed since posting, flag it and note the disappearance — sometimes that's signal of a hiring freeze.
2. **Tier-A discipline**: Every company in §1, §2, §3, §5, §7 must respect the $100k floor and ≤3-day RTO. Flag exceptions explicitly with justification.
3. **YOE discipline**: Every role must fit the 1-4 YOE band. Re-read each entry and remove any "Senior PM, 5+ years required" listing that slipped in.
4. **Referral-fit defensibility**: Re-read every Larry-fit and Matt-fit score. If the rationale is "probably knows someone," downgrade to 2/5 or remove. The bar is "I can name a plausible specific contact path or shared-network signal."
5. **De-duplication**: Cross-check against the AI-PM landscape prompt's company list. Flag overlaps (Robinhood Crypto, any Coinbase AI roles).
6. **Competitive-dynamic flagging**: Every Block competitor in §1 (CoinDesk, Decrypt, Blockworks, DL News, The Defiant, Cointelegraph) must carry a one-line note on how the candidate should frame the referral conversation given the competitive dynamic.
7. **Channel discipline**: Re-read §6. If any "warm intro" recommendation lacks a named contact path, downgrade to "career-page direct" or remove.
8. **Boston-metro audit**: Confirm Circle, Fidelity Digital Assets, State Street Digital are surfaced if they have ANY currently-open PM/APM role — these are the single highest-leverage Boston intersections and must not be missed.
9. **Padding check**: Re-read §1, §2, §3. If any entry lacks a verified open posting in the last 60 days, remove it. The Top-15 list (§7) loses value at every padded entry.
10. **Word count**: Target 3,500-5,500 words. Below 3,500 means under-researched; above 5,500 means padding.
</validation>

--- PROMPT END ---
