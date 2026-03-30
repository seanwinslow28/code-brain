---
granola_id: 41bba522-9201-4d22-995e-eb34f02d2106
title: "Data (Pro Future) discussion"
type: note
created: 2026-03-30T14:00:25.219Z
updated: 2026-03-30T14:33:27.458Z
attendees: 
  - erupkus@theblock.co
  - scousaert@theblock.co
transcript: "[[30_domains/product-management/the-block-meetings-granola-notes/Data (Pro Future) discussion-transcript.md]]"
---
### Current Pro Platform Issues

- Searchability problems with charts dashboard
	- Users must scroll through multiple pages to find relevant data
	- No way to know what data is available without extensive exploration
	- Poor onboarding experience for new clients
- Underutilized granular data
	- Market charts show monthly aggregations while hourly data exists
	- Spot market volume displayed monthly but collected hourly by exchange
	- Significant data not visible on any frontend

### Data Ownership & Partnerships

- Current data breakdown: ~60-65% proprietary/sellable
	- Markets data: Collected via exchange APIs (considered owned)
	- On-chain analytics: Fully proprietary in-house scripts
	- Third-party data: DeFi Llama, CoinGecko (cannot sell)
- Key dependencies for complete coverage:
- Multi-chain complexity forcing reliance on third parties
	- In-house parsing would cost ~$500k/year for full coverage
	- Current free API usage limiting data quality

### Product Strategy Considerations

- Chart creation tool concept
	- Allow users to build custom visualizations from datasets
	- Simon skeptical about revenue potential based on market history
	- Would require significant development investment without proven demand
- Simon AI current limitations
	- Too much conflicting information (articles from 2020+)
	- General crypto questions better served by public LLMs
	- Value proposition: linking live data queries to AI responses
	- Needs focus on data integration rather than general knowledge
- Client demand patterns follow 80/20 rule
	- Most requests: stablecoins, market data, treasuries
	- Minimal demand for DeFi analytics
- Institutional focus emerging
	- TradFi companies building crypto teams
	- Interest in payments, stablecoins, RWA tokenization
- Business model tension: consulting vs. scalable SaaS product
	- Current success through niche, hands-on client work
	- Clients unaware of Block’s full capabilities
	- No systematic communication of case studies/expertise

Chat with meeting transcript: https://notes.granola.ai/t/74cef385-194b-4c1f-b6a5-ba7e45ea47db
