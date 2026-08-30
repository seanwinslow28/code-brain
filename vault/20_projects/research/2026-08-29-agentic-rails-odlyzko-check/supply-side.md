# Odlyzko check — SUPPLY SIDE: the agent-web rails buildout, as of August 29, 2026

Research-agent sweep, 2026-08-29 evening. 14 primary/secondary sources fetched and read.
Tags: [vendor-reported] = from the company building/selling the rail; [independent] =
no stake in the rail's success; [derived] = secondary aggregation or calculation.
Numbers surfaced only via search snippets are tagged [derived] and one confidence tier lower.

## 1. CAPITAL

**Startup rounds (agent commerce / payments / pay-per-crawl / AEO / observability):**

- **TollBit — $24M Series A, Oct 22, 2024** (Lightspeed, Section 32); 200+ publisher sites at raise. https://tollbit.com/blog/series-a/ [vendor-reported; round corroborated by press]. Tracxn ~$31M total over 2 rounds [derived].
- **Basis Theory — $33M Series B, Oct 2025** (Costanoa) — agentic payments/tokenization; seeded the "Agentic Commerce Consortium" (Lithic, Crossmint, Skyfire, Rye, Channel3). https://stellagent.ai/insights/agentic-commerce-infra-startups [derived — no primary fetched].
- **Skyfire — $9.5M total** (Neuberger Berman, a16z CSX, Coinbase Ventures) — agent identity/"Know Your Agent" + payments. Same Stellagent piece [derived]; backers confirmed in https://www.akamai.com/newsroom/press-release/no-free-crawls-akamai-tollbit-and-skyfire-turn-traffic-into-revenue (Sept 17, 2025).
- **Nekuda — $5M seed, May 2025** (Madrona; Amex Ventures, Visa Ventures) — agent checkout credentials [derived].
- **Profound (AEO/agent-readiness) — $96M Series C at $1B valuation, Feb 24, 2026** (Lightspeed); ladder $3.5M seed → $20M A → $35M B (Sequoia) → C; ~$155M total. https://www.tryprofound.com/blog/profound-raises-96m-series-c [vendor-reported; Fortune corroborates]. A $1B valuation for optimizing brand visibility *to AI answer engines* is itself a supply-side bet on agent-mediated demand.
- **Braintrust (AI/agent observability) — $80M Series B, Feb 17, 2026** (Iconiq) at $800M valuation; customers Notion, Replit, Cloudflare, Ramp, Dropbox. https://siliconangle.com/2026/02/17/braintrust-lands-80m-series-b-funding-round-become-observability-layer-ai/ [independent report of vendor-disclosed round].
- **Aggregate:** disclosed startup capital in agent-payments proper is small (~$50M Series A/B across Basis Theory + Skyfire + Nekuda [derived]); the buildout is overwhelmingly **corporate** capital plus adjacent categories (AEO, observability) with 3–10x larger rounds. Total disclosed across named startups ≈ **$305M+** [derived].

**Corporate programs (announced, not inferred):** Coinbase built and donated x402 to the Linux Foundation; Cloudflare shipped pay-per-crawl, x402 support, Wallets/cloudflare.pay; Stripe co-built ACP with OpenAI; Google shipped AP2 and donated it to FIDO; Visa shipped Intelligent Commerce; Mastercard shipped Agent Pay and Agent Pay for Machines. **No corporate program discloses its investment size** [finding].

## 2. PROTOCOL / STANDARD CAPACITY — with activation where it exists

**x402** — the best-instrumented rail, and the clearest Odlyzko specimen:
- Announced Sept 23, 2025 (Cloudflare: 1B+ HTTP 402 responses *already sent daily* to bots — refusals, not payments). https://blog.cloudflare.com/x402/ [vendor-reported]
- Foundation operational launch **July 14, 2026: 40 member orgs**, 17 premier incl. Visa, Mastercard, Amex, AWS, Google, Stripe, Shopify, Adyen, Fiserv. https://x402.org/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications/ [vendor-reported]. **The launch announcement contains zero usage statistics.**
- Coinbase: **169M payments, 590K buyers, 100K+ sellers in year one** (May 13, 2026). https://cointelegraph.com/news/coinbase-launches-x402-batch-settlement-ai-payments [vendor-reported]
- The independent pair: monthly settlement peaked **$5.15M Nov 2025** (x402 briefly 19% of Base activity), fell **~77% to $1.19M by May 2026**; Aug 2026 daily settlement **down 93% YTD** — 7-day avg ~$41,800/day vs Q4-2025 peaks near $800K–$1M. Average transaction **$0.52**. https://cryptopotato.com/x402-volume-plunges-93-ytd-as-agentic-ai-economy-hype-fades/ (Helios Analytics, Aug 12, 2026) [independent]. Analyst Jamie Coutts: a "reality check" for claims the agentic economy has arrived [independent].
- Read together: 169M payments ÷ volume data ⇒ payments are overwhelmingly sub-cent test/spam-scale [derived]. **Membership curve (17→40 orgs) and volume curve (-93%) move in opposite directions. Capacity compounding while activation collapses.**

**AP2 (Google):** announced **Sept 16, 2025 with 60+ partner orgs** (Mastercard, PayPal, Amex, Adyen, Coinbase, Salesforce, Worldpay, UnionPay…). https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol [vendor-reported]. v0.2 Apr 28, 2026 + FIDO donation [derived]. **No published transaction volume anywhere. 60+ orgs, 11+ months live, zero utilization data.**

**ACP / Instant Checkout (Stripe + OpenAI):** launched **Sept 29, 2025** — Etsy US sellers day one, "**over one million**" Shopify merchants "coming soon." https://stripe.com/newsroom/news/stripe-openai-instant-checkout [vendor-reported]. Protocol still beta, latest spec 2026-04-17. Enablement "in as little as one line of code" [vendor-reported]. **No party has published agent-originated GMV, order counts, or merchants-with-any-ACP-sale.** Secondary merchant guides report OpenAI deprioritizing standalone Instant Checkout toward discovery + merchant-owned checkout [derived, unverified — if true, the flagship consumer rail is being redesigned within a year of launch].

**Visa Intelligent Commerce:** announced Apr 2025; mid-2026 "Intelligent Commerce Connect" **in pilot with 7 named partners** (Aldar, AWS, Diddo, Highnote, Mesh, Payabli, Sumvin), broader rollout "planned this year" — American Banker via search [independent report]. No volumes.

**Mastercard Agent Pay:** launched Apr 2025; **first live agentic transaction announced as a milestone Sept 29, 2025** (one transaction — itself a tell); live authenticated agentic transactions for Hong Kong (Mar 27, 2026), Thailand (Apr 7, 2026) [vendor via press]. **Agent Pay for Machines launched June 10, 2026** with 30+ partners; launch release has **no transaction numbers**. https://investor.mastercard.com/investor-news/investor-news-details/2026/Mastercard-Launches-Agent-Pay-for-Machines-to-Unlock-Super-Fast-Always-On-Payments/default.aspx [vendor-reported].

**WebMCP:** Chrome 149 origin trial (through Chrome 156, mid-to-late 2026); 9 named participants (Expedia, Booking.com, Shopify, Credit Karma, TurboTax, Redfin, Etsy, Instacart, Target). Independent assessment: "WebMCP in July 2026 is a standard with everything except users… no mainstream agent client calls `modelContext` tools. Claude, ChatGPT Agent, Perplexity and Gemini all still read pages the old way"; of the 9 logos: "logos of that size signal intent. Deployment is a separate step none of them has confirmed." https://www.spronta.com/blog/state-of-webmcp-july-2026/ [independent]. Community's own label: "Shipping a 0% Adoption Standard" (freeCodeCamp).

**MCP servers:** official registry **9,652 latest server records (28,959 server/version records) as of May 24, 2026**; Glama indexes ~20,000 [derived]. On FastMCP's usage-ranked directory of 1,864 servers, the top 10 (~0.5%) dominate consumption [derived]. A "41% of MCP deployments reach production" survey claim circulates without methodology [derived, weak]. **No per-server traffic exists for the long tail; the server count is a capacity number with no utilization instrument.**

**Cloudflare pay-per-crawl → Pay Per Use:** private beta **July 1, 2025**. On the first anniversary — **July 1, 2026 — Cloudflare itself declared per-crawl payment insufficient** and pivoted to "Pay Per Use" (pay when content appears in an answer), launching with **two AI companies (Ceramic.ai, You.com)**. Cloudflare's own beta measurements: Anthropic's crawler fetched **38,000 pages per referral visit returned**; OpenAI 1,091:1; >50% of AI crawler traffic re-fetches unchanged pages. https://techcrunch.com/2026/07/01/cloudflares-new-policy-pushes-ai-companies-to-pay-for-publishers-content/ [independent report; ratios vendor-measured]. **One full year of beta: no publisher earnings figure ever published; the operator replaced the model.**

**TollBit:** 200+ publishers (Oct 2024) → **3,000+ publishers, 1.5B quarterly bot scrapes monitored, ~450M quarterly bots redirected to paywall** (Sept 17, 2025, Akamai release) [vendor-reported]; 730% growth in bot paywall adoption Q4'24→Q1'25 [vendor-reported]. **No dollar payout figure ever published** — "redirected to paywall" ≠ "paid the toll," and that conversion rate is the number TollBit has never released.

**Cloudflare Wallets / cloudflare.pay:** announced **Aug 4, 2026** — 25 days ago. Available today: *reserving a wallet handle*. Wallets, funding, issuance: "coming in the following months." https://www.cloudflare.com/press/press-releases/2026/cloudflare-gives-ai-agents-an-identity-and-a-wallet/ [vendor-reported]. Pre-capacity, announced with the cycle's fullest narrative framing.

## 3. (a) BUILDOUT INVENTORY TABLE

| Rail | Live since | Age (Aug 2026) | Capacity number | Activation number | Gap |
|---|---|---|---|---|---|
| x402 | May–Sep 2025 | ~12–15 mo | 40 foundation members incl. Visa/MC/Amex/AWS/Google/Stripe [vendor]; 100K+ sellers [vendor] | $1.19M settled/mo (May '26), −77% from peak; ~$42K/day Aug '26, −93% YTD [independent]; avg tx $0.52 | Membership up 2.4x while volume fell 93% |
| AP2 | Sep 16, 2025 | 11.5 mo | 60+ consortium orgs [vendor] | **none published** | total |
| Stripe ACP / Instant Checkout | Sep 29, 2025 | 11 mo | Etsy day-1 + "1M+" Shopify merchants promised [vendor] | **no GMV/order data**; standalone checkout reportedly deprioritized [derived, unverified] | total |
| Visa Intelligent Commerce | Apr 2025 | ~16 mo | announced platform | 7 pilot partners; no volumes | pilot-only |
| Mastercard Agent Pay / AP4M | Apr 2025 / Jun 2026 | ~16 / ~2.5 mo | 30+ AP4M partners [vendor] | 1 transaction announced as milestone (Sep '25); country launches without volumes | near-total |
| Cloudflare pay-per-crawl | Jul 1, 2025 | 13 mo (superseded) | Cloudflare-scale beta | **no payout data ever; model replaced Jul 1, 2026**; successor: 2 AI buyers | operator abandoned the model |
| TollBit | 2024 | ~2 yr | 3,000+ publishers; 450M bots/qtr paywalled [vendor] | **no publisher-earnings figure published** | total on the dollar side |
| WebMCP | ~mid-2026 OT | ~3 mo | 9 named participants; standard + browser shipped | ~0 confirmed production deployments; 1 committed agent consumer [independent] | "0% adoption standard" |
| MCP servers | Nov 2024 | ~21 mo | 9,652–20,000 registered servers [derived] | top ~0.5% carry usage; long tail unmeasured | unmeasurable by design |
| Cloudflare Wallets | Aug 4, 2026 | 25 days | handle reservation only | n/a — not shipped | pre-capacity |
| Startup capital | 2024–2026 | — | ≈ **$305M+ disclosed** [derived] | revenue undisclosed across all | — |

## 4. (b) LOAD-BEARING NARRATIVE CLAIMS (verbatim, attributed)

1. **McKinsey (Oct 2025)** — the demand forecast the buildout leans on: up to **$1T** orchestrated US retail revenue, **$3–5T globally by 2030**; "This is not just an evolution of ecommerce. It's a rethinking of shopping itself." (via https://www.digitalcommerce360.com/2025/10/20/mckinsey-forecast-5-trillion-agentic-commerce-sales-2030/) [independent *forecast*, not measurement]. Companions: Gartner 20%-of-digital-commerce-by-2030; 90%-of-B2B-buying / $15T-by-2028 [derived].
2. **Matthew Prince, Cloudflare CEO (Aug 4, 2026)**: "The Internet is shifting from human-driven browsing to agent-driven commerce, and the infrastructure needs to keep up… It's the identity and payment infrastructure the agentic web needs to function." — present-tense fact claim in the same month independent data showed x402 settlement down 93% YTD.
3. **Jorn Lambert, Mastercard CPO (Jun 10, 2026)**: "Machine payments can make it possible for services to be bought and sold among agents at fundamentally different scales than payments today — very high volumes, very small values, very fast and at extremely low latency." — the micropayments-at-machine-scale thesis Odlyzko spent the 2000s falsifying for human content.
4. **Will Gaybrick, Stripe president (Sep 29, 2025)**: "Stripe is building the economic infrastructure for AI. We're working alongside the most ambitious companies to create new AI-powered commerce experiences for billions of people."
5. **Jim Zemlin, Linux Foundation / Peyton Rice, AWS (Jul 14, 2026)**: "AI agents and automated systems are becoming active participants in the global economy, yet they have lacked a native, secure way to transact" / "AI agents are becoming first-class participants in digital commerce, and they need a payments layer as open and interoperable as the internet itself." — asserted in an announcement containing no usage data.

## 5. (c) CAPACITY NUMBERS WITH NO PUBLISHED UTILIZATION PAIR — absence as finding

- **AP2's 60+ orgs:** 11+ months live; not one volume figure from Google, FIDO, or any partner.
- **ACP's "1M+ Shopify merchants":** no agent-originated GMV, order count, or merchants-with-any-sale from Stripe, OpenAI, Shopify, or Etsy — the most conspicuous silence in the space, from companies that publish GMV constantly when it's good.
- **Visa/Mastercard:** 16 months of announcements; the only concrete unit ever published is *one* transaction (Sept 2025).
- **TollBit's 3,000 publishers / 450M redirects:** no dollar payout in two years.
- **Cloudflare pay-per-crawl:** a year of beta, zero payout disclosure, resolved by replacing the model.
- **MCP's 10–20K servers:** no long-tail traffic instrumentation; unfalsifiable as a utilization claim.
- **The only rail with a real published pair is x402 — and its pair (40 members up, 93% volume down, $0.52 avg tx) is the cycle's cleanest capacity-racing-ahead-of-demand signal.** That the best-measured rail shows collapse while every worse-measured rail publishes only capacity is itself the Odlyzko pattern: in 2000–02, carriers also published route-miles, never lit-fiber utilization.
