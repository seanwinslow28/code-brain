# Odlyzko check — DEMAND SIDE: measured agent-web commerce data, as of August 2026

Research-agent sweep, 2026-08-29 evening. Every datapoint tagged [independent] /
[vendor] / [derived], with what it *actually* measures. "AI-referred traffic" (a human
clicked out of a chatbot), "AI-influenced sales" (a recommendation touched the journey),
and "agent-executed transactions" (software completed checkout) are three different
quantities separated by orders of magnitude, and most circulating numbers are the first
two dressed up as the third.

## 1. Agent commerce volume (retail)

| # | Datapoint | Date | Tag | What it measures |
|---|---|---|---|---|
| 1.1 | ChatGPT Instant Checkout GMV: **never disclosed**. Fintech Brain Food: "the quiet part out loud of agentic commerce is there's no volume yet." ~50M shopping queries/day on ChatGPT is an OpenAI-side estimate. (https://www.fintechbrainfood.com/p/agentic-checkout, https://openai.com/index/buy-it-in-chatgpt/, https://stripe.com/newsroom/news/stripe-openai-instant-checkout) | Sept 2025 launch → Aug 2026 | [vendor] / absence | Query volume ≠ purchases. No transaction or GMV figure exists publicly. |
| 1.2 | **Etsy quit Instant Checkout in March 2026** after ~6 months: "didn't see a large volume of sales from the integration." Same calls: agentic-channel traffic to Etsy grew **~15x YoY but is <1% of total traffic**; ChatGPT-originated orders skew higher AOV. (https://techcrunch.com/2026/05/05/etsy-launches-its-app-within-chatgpt-as-it-continues-its-ai-push/, https://www.fool.com/earnings/call-transcripts/2026/02/19/etsy-etsy-q4-2025-earnings-transcript/, https://finance.yahoo.com/markets/stocks/articles/etsy-inc-q1-2026-earnings-165048884.html) | Feb–May 2026 | [vendor, disclosure *against* interest — highest-trust class] | Actual revealed demand at the first large-scale agent-checkout integration: too small to keep running. The single strongest demand datapoint in the file. |
| 1.3 | Shopify Q2 2026: AI-driven traffic and **orders "tripled YoY"** but volume is "still small relative to GMV" (Q2 GMV $115.6B). AI-referred sessions land on PDPs 2.5x more often; catalog-fed AI converts 2x scraped data. (https://www.fool.com/earnings/call-transcripts/2026/08/12/shopify-shop-q2-2026-earnings-call-transcript/, https://www.digitalcommerce360.com/article/shopify-revenue-gmv/) | Aug 12, 2026 | [vendor] | AI-*referred* orders (human completes checkout), not autonomous purchases. No absolute number. |
| 1.4 | Adobe Analytics (>1T visits panel): AI-referred traffic **+4,700% YoY (Jul 2025) → +693% (Nov–Dec 2025) → +393% (Q1 2026) → +269% (Mar 2026)**. AI-referred visitors converted 31% higher holiday 2025; 42% better by Mar 2026. (https://business.adobe.com/blog/ai-driven-traffic-surges-across-industries, https://www.digitalcommerce360.com/2026/01/13/generative-ai-online-holiday-shopping-traffic-2025/, https://www.retailgentic.com/p/breakingadobe-releases-q1-ai-traffic) | Jul 2025–Mar 2026 | [independent-ish: measurement vendor, real clickstream] | **Referral traffic only.** Absolute share unpublished; third-party syntheses put AI-referred sessions at **<0.2–1% of e-commerce sessions** (https://commercetools.com/blog/agentic-commerce-stats-enterprise-guide) [derived]. |
| 1.5 | Salesforce: AI "influenced" **20% of global orders / $262B** holiday-2025; Cyber Week $336.6B total, AI-influenced ~$67–73B; 7% of shoppers *start* search in an AI assistant. (https://www.salesforce.com/news/press-releases/2025/12/05/cyber-week-ai-agents-sales/, https://www.salesforce.com/news/stories/2025-holiday-shopping-data/) | Dec 2025–Jan 2026 | [vendor] | "Influenced" = an AI recommendation appeared anywhere in the journey — mostly retailers' own on-site recommendation AI, i.e. rebranded personalization. The loosest metric in circulation. |
| 1.6 | Amazon Rufus: **~$12B annualized "incremental" sales** (Amazon's own attribution); 300M customers used it in 2025; 60K-shopper Azoma panel: Rufus users convert **2.74x**, Black Friday Rufus-assisted ~40% of sessions / ~66% of purchases. (https://finance.yahoo.com/news/amazon-says-ai-shopping-assistant-152500992.html, https://www.azoma.ai/insights/what-percentage-of-amazon-shoppers-use-rufus-2026) | Q3 2025–Q1 2026 | [vendor] for $12B; [independent] panel w/ self-flagged selection bias | Assistant-*assisted* on-platform purchases; human still checks out. High-intent shoppers self-select into Rufus. |
| 1.7 | Perplexity shopping: **~2M monthly active shoppers, ~$2B annualized GMV run rate** (≈$167M/month), 8–12% take rate — trade press only, **no primary Perplexity disclosure** (https://novadata.io/resources/news/perplexity-buy-now-agent-2m-shoppers-july-2026) | Jul 2026 | [vendor-adjacent/unverified] | Weakest sourcing of any number here — upper-bound input only. |

## 2. Machine payments (x402 and pay-per-crawl)

| # | Datapoint | Date | Tag | What it measures |
|---|---|---|---|---|
| 2.1 | Coinbase claim: **169M payments, 590K buyers, 100K+ sellers** in year one. (https://crypto.news/coinbases-x402-has-processed-over-100-million-transactions-on-base/) | ~mid-2026 | [vendor] | Raw on-chain transaction count, no value or organic filter. |
| 2.2 | Independent academic count: **~130M all-time tx as of May 2026** (Ling et al., arXiv:2605.30998, via Dune); Base 54% / Solana 35% / Polygon 10%; USDC 98.8% of EVM dollar volume; 3 facilitators = 71% of volume; 1,853 resource servers, 915 merchants. Companion USENIX 2026 measurement: **119M Base+Solana tx** (https://www.usenix.org/system/files/usenixsecurity26-wang-qinying.pdf) | May 2026 | [independent] | Confirms count order of magnitude — but counts are the wrong axis. |
| 2.3 | **Dollar value: 75M transactions moved $24M in 30 days — avg ~$0.32/tx** (CoinDesk Jul 2026). Weekly volume **collapsed 77%** from Nov 2025 peak ($5.15M/wk) to $1.19M/wk by May 2026; daily dollar volume at one point ~$28K/day. (https://www.coindesk.com/tech/2026/07/15/visa-mastercard-and-ripple-join-the-standard-letting-ai-agents-pay-in-stablecoins, https://www.coindesk.com/markets/2026/03/11/coinbase-backed-ai-payments-protocol-wants-to-fix-micropayment-but-demand-is-just-not-there-yet, https://www.mexc.com/news/901995) | Nov 2025–Jul 2026 | [independent] | Entire x402 economy ≈ **$24M/month nominal** — roughly one mid-size Shopify merchant. |
| 2.4 | Organic share: Artemis — "**roughly half** of observed x402 transactions reflect artificial activity… 'the x402 agent-payments boom is still mostly a mirage.'" Q4-2025 spike driven by PING pay-to-mint memecoin (tx +10,000% in a week); facilitator (Murr) estimate: **25–30%** leaderboard farming. Chainalysis: x402 wallets young (197 vs 423 days), hold 26 tokens vs 4 — speculator profile. (https://www.chainalysis.com/blog/x402-agentic-payments-adoption/) | Q4 2025–Mar 2026 | [independent] | Organic machine-payment demand ≈ **$10–15M/month** [derived]. |
| 2.5 | TollBit: nearly **20% of ~7,000 publisher sites** have earned, ranging "**hundreds of dollars to tens of thousands** a month" (CEO). The circulating "$500–$5,000/month" bracket is a narrowed paraphrase — the primary quote is wider on both ends. (https://digiday.com/media/the-washington-posts-arc-xp-adds-tollbit-to-help-publishers-make-money-from-ai-bot-traffic/, https://www.fastcompany.com/91403867/ai-scraping-publishers-revenue-report-tollbit) | Apr–mid 2026 | [vendor] | ~1,400 earning publishers ⇒ plausibly **$2–10M/month** network payouts [derived, wide]. |
| 2.6 | Cloudflare pay-per-crawl: **no published earnings results from the beta.** 2026: abandoned per-crawl pricing for "pay per answer" with two launch partners (Ceramic.ai, You.com), conceding crawls are a poor proxy for value. (https://ppc.land/cloudflare-stops-charging-ai-per-crawl-and-starts-paying-per-answer/, https://techcrunch.com/2026/07/01/cloudflares-new-policy-pushes-ai-companies-to-pay-for-publishers-content/) | Jul 2025–Jul 2026 | absence | A year-old monetization beta pivoting without ever publishing revenue is itself demand evidence. |

## 3. Agent traffic quality (decomposition)

- **57.5% of HTML requests automated vs 42.5% human** — Cloudflare Radar, ~20% of the web, mid-2026. Requests, not visitors, not commerce. (https://www.tomshardware.com/tech-industry/artificial-intelligence/bots-have-now-passed-human-traffic-online-cloudflare-boss-laments-says-agentic-traffic-wasnt-expected-to-eclipse-real-people-until-next-year)
- **1 AI-bot visit per 31 human visits** (Q4 2025, from 1-in-200 at start of 2025) — TollBit [vendor]. On publisher sites AI bots ≈ 3% of visits — the 57.5% figure is request-level plumbing, not audience. (https://pressgazette.co.uk/platforms/publishers-urged-to-embrace-future-where-bot-readers-provide-majority-of-revenue/, https://tollbit.com/bots/25q2/)
- **80% of AI crawling is model-training crawl generating zero referral** — Kinsta, own 10B-request infra measurement, corroborating TollBit [independent]. (https://kinsta.com/ai-bot-traffic/, https://ppc.land/ai-bots-hammered-wordpress-cart-pages-3-75m-times-in-a-day-kinsta-data-shows/)
- **Of live *agentic* (non-crawl) traffic, only 2.3–2.6% touches checkout/payment pages**; ~76% is product/search/reading — HUMAN Security State of Agentic Traffic, Apr–Jul 2026 [vendor telemetry]. Checkout-page arrival ≠ completed purchase; upper bound on transactional intent. (https://www.humansecurity.com/learn/blog/state-of-agentic-traffic-may-2026-financial-services-agentic-traffic-continues-to-climb-more-than-doubling-this-month/, https://www.humansecurity.com/learn/blog/state-of-agentic-traffic-july-2026-publishers-claim-highest-share-of-agentic-traffic/)
- Stacking [derived]: *transaction-attempting agent traffic* ≈ (small agentic slice of automated traffic) × 2.6% — a rounding error of total web traffic. The 57.5% headline and the commerce narrative share almost no members.

## 4. Human-side leading indicators (behavioral, not survey)

- **Bilal et al., arXiv:2608.02100** — 1.5M real ChatGPT/Gemini interactions, 6,304 US/India users, Aug–Oct 2025: financial chats are Inform (63.5% US) and Shape (58.6% US); **Level-3 "Act" (execution/delegation) = 0.3% of US and 0.1% of Indian FS chats**, and even those were "almost all instruction-led budgeting and tracking" — "close to no evidence of users delegating autonomous financial decisions to AI." [independent] (https://arxiv.org/html/2608.02100v1)
- Etsy's revealed-preference exit (1.2) is the commerce-side twin: when execution was one click away inside ChatGPT, users didn't take it at sustaining volume. [vendor-against-interest]
- Salesforce's own behavioral stat: **7% of shoppers start product search in an AI assistant** [vendor] — a discovery indicator; heavy Shape, negligible Act.

## 5. Growth-claim audit

| Claim | Who | Check against measured series |
|---|---|---|
| "Agentic traffic +7,851% YoY" | HUMAN Security 2026 benchmark [vendor] (https://www.globenewswire.com/news-release/2026/03/26/3263087/0/en/human-security-s-2026-state-of-ai-traffic-cyberthreat-benchmark-report-signals-a-new-internet-era-automation-growth-now-outpaces-humans.html) | Real but off a near-zero base; HUMAN's own decomposition: only ~2.3–2.6% touches checkout. Growth of a discovery channel, not a commerce channel. |
| "AI retail traffic +4,700% YoY" | Adobe, Jul 2025, endlessly recirculated | Adobe's own newer series decelerates: 4,700% → 693% → 393% → 269% by Mar 2026. The most-quoted number is the stalest, and it measures referral clicks on a <1%-of-traffic base. |
| "AI agents will handle 90% of B2B buying / $15T by 2028" | Gartner, Nov 2025 (https://www.digitalcommerce360.com/2025/11/28/gartner-ai-agents-15-trillion-in-b2b-purchases-by-2028/) | Measured machine-native payment volume today: ~$24M/month nominal, ~half artificial. Requires ~**six orders of magnitude** growth in ~2.5 years, or a definitional retreat to "an agent touched the PO workflow." |
| "AI influenced $262B / 20% of holiday sales" | Salesforce [vendor] | Definitionally engineered: includes on-site recommendation widgets. The agent-*executed* fraction is not reported by anyone; every disclosed proxy says rounding error. |
| "x402: 169M payments, the agent economy is here" | Coinbase [vendor] | Independent value data: $24M/30d, $0.32 avg, ~50% artificial, dollar volume down 77% from Nov-2025 peak. Count grew while value collapsed — the signature of farming, not demand. |

## (a) Best defensible estimate: current monthly agent-commerce volume

**Agent-executed retail commerce:** Perplexity ≤$167M/mo GMV [unverified upper bound];
ChatGPT Instant Checkout undisclosed, bounded low by the Etsy exit — $10–100M/mo
generous bracket [derived]; everything else assume ≤ ChatGPT.
**Bracket: ~$50M–$400M GMV/month globally, order 1–5M orders/month — ~0.01–0.1% of
online retail** (vs ~$500B/month global e-commerce) [derived].

**Machine-native payments:** ~$24M/month nominal, **~$10–15M/month organic** [independent-anchored]. Content licensing (TollBit): $2–10M/month [derived].

**Total genuinely agent-executed commerce: order $100M–$500M/month** — versus
$50–70B/month "AI-influenced" by Salesforce's definition. **The 100–500x gap between
those two numbers is the Odlyzko finding.**

## (b) Measured vs claimed growth

Measured: Adobe referral growth decelerating 4,700%→269% over 8 months; Shopify agentic
orders ~3x YoY (base "small"); Etsy ~15x YoY on <1% base, then exit; x402 *dollar*
volume peaked Nov 2025 and fell 77% by May 2026. Real, fast, decelerating growth in
*referral/discovery*; flat-to-negative in *machine-payment value*; one confirmed
shutdown in *agent checkout*. Claimed: 7,851%, $15T-by-2028, 20%-of-all-sales. Claimed
rates exceed measured rates on every commerce-relevant series, generally by redefining
the metric rather than by citing a different measurement.

## (c) What does not exist publicly — absence as finding

1. **No platform has ever disclosed agent-checkout GMV or transaction counts** — not
   OpenAI (11 months post-launch), not Microsoft, Google, or Amazon for agentic Rufus.
   In an industry that publicizes every favorable metric, an 11-month disclosure
   silence across all vendors is data.
2. **No independent panel measures agent purchase *completion*** — Adobe/Similarweb see
   referral clicks; HUMAN sees checkout-page *arrivals*; nobody publishes completion.
3. **No audited number anywhere**: zero agentic GMV in any GAAP filing as a quantified
   line item; closest are "small but tripling" (Shopify) and an exit (Etsy).
4. **Cloudflare pay-per-crawl produced no published revenue results in 12 months** and pivoted.
5. **No decomposition of Cloudflare's 57.5%** into training/live-agent/transactional
   from Cloudflare itself — must be stitched from TollBit + Kinsta + HUMAN.
6. **No independent verification of Perplexity's $2B GMV** or take rate.

**Bottom line:** 1845 all over again — supply-side telemetry (traffic, transaction
*counts*, protocol memberships incl. Visa/Mastercard/Ripple joining x402) is abundant
and loud; demand-side money is measurable, small (order $10⁸/month), decelerating where
measured, and the two cleanest revealed-preference tests (Etsy's exit; 0.1–0.3%
execution delegation across 1.5M real conversations) point the same direction. The
trustworthy demand data exists, and it is being ignored in favor of redefined metrics.
