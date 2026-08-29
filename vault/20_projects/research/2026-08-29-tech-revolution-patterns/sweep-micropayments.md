# Sweep — why human micropayments failed, and whether agents escape the mechanism (2026-08-29)

Stage-0 research-agent sweep, 12 sources (10 read directly; Flooz and Blendle rest on
search-result summaries of named articles — flagged inline, re-verify before publication).
Question 1 of the historical-patterns funnel. Quotes verbatim as extracted; agent
inference explicitly labeled.

## PER-SOURCE FINDINGS

### 1. Nick Szabo, "Micropayments and Mental Transaction Costs" (May 1999)
**URL:** https://nakamotoinstitute.org/library/micropayments-and-mental-transaction-costs/ · **Classification:** Primary/scholarly essay (the canonical theoretical source) · Read in full.

- "Mental accounting costs... set the main lower bound on price granularity." Technology cost reduction is aimed at the wrong constraint.
- "Cognitive costs usually well outweigh technological costs" — his core empirical assertion.
- Three sources of mental cost: uncertain cashflows, incomplete observation of product attributes, incomplete decision-making.
- Flat fees work because "a flat fee constitutes an embedded, implicit insurance contract" against spend uncertainty.
- **Critically: Szabo considered software agents in 1999 and rejected them:** "Since these agents are programmed remotely, not by the consumer, it is difficult for the consumer to determine whether the agent is acting in the consumer's best interests." His objection is a *principal-agent trust* problem, not a capability problem.
- **Mechanism attributed:** mental transaction costs, with preference-elicitation cost as the reason agents don't trivially fix it.

### 2. Clay Shirky, "The Case Against Micropayments" (O'Reilly OpenP2P, Dec 19, 2000)
**URL (mirror read):** http://mx.thirdvisit.co.uk/2002/10/04/theacaseaagainstamicropayments/ (original openp2p.com dead; canonical cite: oreillynet.com/pub/a/p2p/2000/12/19/micropayments.html) · **Classification:** serious contemporaneous commentary · Read in full via mirror.

- "A transaction can't be worth so much as to require a decision but worth so little that that decision is automatic." — the impossibility at the heart of human micropayments.
- "The only transaction a user will be willing to approve with no thought will be one that costs them nothing."
- The "double-standard of value": "One cannot tell users that they need to place a monetary value on something while also suggesting that the fee charged is functionally zero."
- Body count as of 2000: "FirstVirtual, Cybercoin, Millicent, Digicash, Internet Dollar, Pay2See, MicroMint, Cybercent" — none achieved user adoption.
- Predicts winners: aggregation, subscription, subsidy. (iTunes 2003 and the ad-funded web validated all three.)

### 3. Andrew Odlyzko, "The Case Against Micropayments" (Financial Cryptography 2003, LNCS)
**URL:** https://www-users.cse.umn.edu/~odlyzko/doc/case.against.micropayments.pdf · **Classification:** scholarly (peer venue) · Read in full (7 pp). The densest source; enumerates FIVE mechanisms:

- "The obstacles to micropayment adoption have very little to do with technology, and are rooted in economics, sociology, and psychology... What is missing are convincing business cases."
- **(a) Competitive squeeze:** "The same advances... are also enabling competing payment systems (especially credit and debit cards) to economically handle decreasingly small transactions."
- **(b) Payment systems move on non-internet time:** "Changes in payment systems tend to be even slower" than decade-scale tech diffusion; "it took credit cards several decades to achieve their high penetration."
- **(c) Bundling beats itemization for sellers:** "It is to the sellers' advantage to sell bundles of goods, as that maximizes their profits."
- **(d) Flat-rate behavioral preference:** "Consumers are willing to pay more for flat-rate plans than for metered ones" — telephone pricing ~1900, rediscovered by Bell System in the 1970s. The AOL anecdote: told she'd pay *less* at flat rate: "'I don't care'... 'I am being cheated by you.'"
- **(e) Sellers want to maximize usage:** "Any kind of barrier to usage, such as explicit payment, serves to discourage usage." Elsevier PEAK: "as soon as the usage is metered on a per-article basis, there is an inhibition on use." Flat-rate switch increases usage "by 50 to 200 percent"; AOL usage tripled.
- Anonymity — sold as a feature — is *opposed by both governments and sellers* (price-discrimination incentive).
- Escape hatch: micropayments "are most likely to succeed if they piggyback on top of something that is already widely used" (cell phones, transit cards) — exactly what later semi-worked (carrier billing).

### 4. Andrew Odlyzko, "Internet Pricing and the History of Communications" (Computer Networks 36, 2001)
**URL:** https://www-users.cse.umn.edu/~odlyzko/doc/history.communications1b.pdf · **Classification:** scholarly journal article · Read partially (lossy PDF extraction; paraphrase-level, cross-confirmed by the FC2003 paper's citations).

- A century of pricing history (mail, telegraph, telephone): quality up, prices down, usage up, and **pricing simplifies** toward flat/uniform tariffs.
- Users prefer flat rates strongly enough to pay more in total; itemized billing generates dissatisfaction and admin overhead exceeding revenue-allocation gains.
- Fine-grained Internet pricing fights a 150-year historical current. Flat-rate preference is a *durable behavioral regularity across technologies*, not a 1990s UX artifact.

### 5. "How DigiCash Blew Everything" (Next! Magazine, Jan 1999; English trans. Feb 1999)
**URL:** https://cryptome.org/jya/digicrash.htm · **Classification:** primary journalistic post-mortem (ex-DigiCash insiders) · Read in full.

- Chaum's deal paranoia killed the distribution that would have solved cold start: Microsoft (~$100M offer; Chaum wanted $1–2 per Windows 95 copy), Visa ($40M offered, Chaum moved to $75M), ING ("The day we were all set to sign, David didn't want to").
- Banks had no urgency: card rails were profitable; eCash lived in innovation-department quarantine.
- Consumers didn't want the flagship feature: no fraud fear (issuers absorbed losses), no revealed demand for anonymity.
- Two-sided cold start: content providers "couldn't do anything but wait."
- **Mechanism:** two-sided cold start + execution/distribution failure + a value proposition nobody demanded. Notably *not* mental transaction costs — DigiCash never got far enough for that to bind.

### 6. Ali, Clarke & McCorry, "The Nuts and Bolts of Micropayments: A Survey" (arXiv:1710.02964, Oct 2017)
**URL:** https://arxiv.org/abs/1710.02964 · **Classification:** scholarly survey · Read pp. 2–7.

- "the vast majority of micropayments solutions have failed, in large part due to neglect of critical non-technical concerns such as usability issues, ethical and legal concerns, poor business cases, and ineffective deployment strategies."
- Endorses Szabo: micropayments "involve what economists describe as cognitive or **mental transaction costs**, i.e. the 'hassle-factor'... Szabo has argued persuasively that researchers often overlook the fact that these mental costs outweigh the technological."
- First generation (mid-1990s: CyberCoin, Mini-Pay, NetBill, Millicent, PayWord, MicroMint): "poor usability... high latency. CyberCash, for example, typically took 15-20 seconds to finalize a transaction... poor interoperability, and consequently there was low penetration among merchants."
- Second generation (~2000: PayPal, ClickandBuy, prepaid, carrier-validated like Zong) partially survived — "good usability, intuitive design, and low latency" plus "the cultural shift... Brand association also played a critical role" (iTunes, PayPal–eBay).
- Millicent: DEC, 1995, sub-cent fees via merchant-specific vouchers; "briefly trialled in the United States in 1997"; merchant lock-in + secret-sharing overhead structural.
- Berners-Lee and Andreessen "considered incorporating micropayments directly into the Web at the protocol level but were discouraged by conservative banking regulations."

### 7. Matthew Guay, "First, add no friction: How micropayments lost and subscriptions won" (Buttondown, May 2026)
**URL:** https://buttondown.com/blog/why-micropayments-do-not-work · **Classification:** serious practitioner commentary (vendor-adjacent) · Read in full.

- Fee-floor arithmetic: "Credit card fees eat up a third of a $1 transaction; PayPal's lower fees work out to 55% on 10¢."
- Blendle's revealed demand: "Of its 1 million-plus registered users, only 150,000 had actually made any micropayments" — most only spent free credits.
- "A newspaper becomes impossible to value" per-article; articles lack music's re-play value (why iTunes' unit sale worked where per-article didn't).
- Flattr lasted 14 years before folding; Gratipay ~5.

### 8. Flooz/Beenz fraud collapse (Aug 2001)
**Sources (search summaries + Wikipedia excerpt; NOT directly fetched — re-verify):** https://en.wikipedia.org/wiki/Flooz.com ; https://www.deseret.com/2001/8/27/19603623/flooz-com-shuts-down-perhaps-a-victim-of-fraud/ · **Classification:** secondary/reference.

- FBI notified Flooz that a crime syndicate used ~$300K of Flooz bought with stolen cards for laundering; fraudulent purchases reached ~19% of consumer credit-card transactions by mid-2001; Flooz guaranteed redemptions while its processor withheld funds → Chapter 7. Beenz died the same month.
- **Mechanism:** chargeback/fraud economics — a *closed-loop scrip funded by an open-loop card rail* inherits the card rail's fraud without its scale to absorb it.

### 9. Blendle pivot (2019, 2023)
**Sources:** Nieman Lab pieces (both 403'd on fetch; claims from search summaries + Guay + Pugpig coverage — lower quote confidence) · **Classification:** trade journalism.

- Blendle (2013, "iTunes for newspapers," ~$0.20/article) never turned a profit on micropayments; premium subscribers "turn out to be much more active"; micropayment service shut 2019; fully exited by 2023.

### 10. Coinbase Developer Platform, "x402: An open standard for internet-native payments" (whitepaper, May 6, 2025)
**URL:** https://www.x402.org/x402-whitepaper.pdf · **Classification:** vendor primary · Read pp. 1–8.

- "one of the major roadblocks to achieving fully autonomous AI systems is the lack of a payment system that empowers AI Agents to function without human intervention."
- Targets the legacy-rail mechanism: services "stuck using inefficient business models like subscriptions, and hindered by... delayed settlement times, high transaction fees, manual invoicing, and susceptibility to fraud and chargebacks."
- Comparison table: credit card "$0.30 + 2.9%," chargebacks "up to 120d," vs x402 on Base: "nominal gas <$0.0001," settlement "200 ms," chargeback "No - not reversible."
- "x402 removes the need for API keys, accounts, and subscriptions." "x402 eliminates friction, allowing AI agents to pay per use with zero manual steps."
- **What it does NOT address (agent's observation from the full read):** never cites Szabo, Shirky, or Odlyzko; never engages flat-rate preference, bundling economics, or seller usage-maximization incentives — it answers the 1990s *technological* failure story, which every scholarly source above says was not the binding constraint for humans.

### 11. Ling et al., "Free-Riding the Agentic Web: A Systematic Security Analysis of x402 Payments" (arXiv:2605.30998, May 2026, rev. June 2026)
**URL:** https://arxiv.org/abs/2605.30998 · **Classification:** scholarly (recent, pre-peer-review) · Abstract + key results read.

- x402 "has crossed from prototype to infrastructure for the agentic web, driving 130 million all-time transactions."
- "Four flaw classes: cross-resource substitution, duplicate-settlement race, allowance overdraft, and denial of settlement"; against official SDKs and a production deployment, "resource-leakage ratios up to 100%."
- Attacker leverage "8.7×" without mitigations; a proved limit that "no output-only pricing can be both fair to honest users and bounded against inflation."
- **Relevance:** removing chargebacks doesn't remove adversarial economics — fraud reappears as protocol-level free-riding and settlement races on the *merchant's* side.

### 12. Cloudflare, "Introducing pay per crawl" (blog, July 1, 2025)
**URL:** https://blog.cloudflare.com/introducing-pay-per-crawl/ · **Classification:** vendor primary · Read.

- Revives HTTP 402 for AI crawlers; publishers "define a flat, per-request price across their entire site"; per-crawler Allow/Charge/Block.
- "Cloudflare acts as the Merchant of Record" — even in the machine era, an *aggregator* sits in the middle handling identity (Ed25519 Web Bot Auth), billing, settlement.
- "an agentic paywall could operate entirely programmatically," agents given "a budget to spend to acquire the best and most relevant content."
- Still "in private beta" — no adoption data.
- **Relevance:** the strongest real-world design implicitly concedes two historical lessons: bot *identity/anti-fraud* must be solved first, and aggregation (one merchant of record, flat per-request pricing) does the mental-cost-reduction work, not the payment rail.

## CROSS-SOURCE SYNTHESIS

### (1) Failure-mechanism inventory with kill attribution

| # | Mechanism | Core sources | Systems it (primarily) killed |
|---|---|---|---|
| M1 | **Mental transaction costs** — per-purchase decision cost has a floor independent of fee size | Szabo 1999; Shirky 2000; Ali et al. | Every *consumer-facing* per-item system that reached users: CyberCoin, Millicent trials, Pay2See; Blendle and Flattr in the 2010s |
| M2 | **Flat-rate/insurance preference + metering chills usage** (binds even with zero decision friction, via budget anxiety and seller usage-maximization) | Odlyzko 2001 & 2003 (AOL, Bell System, PEAK/Elsevier) | Per-article news generally; explains why sellers *chose* subscriptions (Blendle pivot) |
| M3 | **Two-sided cold start / merchant integration burden** — special wallets, merchant-specific scrip, no interoperability | DigiCash post-mortem; Ali et al.; Odlyzko §3 (payment adoption takes decades, VC timelines don't) | DigiCash/eCash, Millicent, First Virtual, MiniPay |
| M4 | **Fixed per-transaction fee floors on incumbent rails** — $0.30+2.9% makes sub-dollar prices arithmetically impossible | Guay; x402 whitepaper; Ali et al. | Anything routing tiny sums over card rails |
| M5 | **Fraud/chargeback economics** — small payments can't amortize dispute costs; scrip funded by cards inherits card fraud | Flooz record; x402 whitepaper | Flooz outright; Beenz by contagion |
| M6 | **Competitive squeeze + bundling economics** — cards/PayPal ate down-market while sellers preferred bundles | Odlyzko 2003 §2,§4; Ali et al. | Peppercoin (aggregation replicated by processors; acquired 2007 with "modest adoption" — secondary); most 2nd-gen startups |
| M7 | **Anonymity as anti-feature** — governments and price-discriminating sellers both resist; consumers don't demand it | Odlyzko 2003 §5; DigiCash post-mortem | DigiCash specifically |

Why iTunes/app stores/carrier billing succeeded where these failed (sourced): brand + usability + cultural shift (Ali et al.); piggyback "on top of something that is already widely used" (Odlyzko's exact prediction); durable-good value + friction removal (Guay). All are aggregation-with-stored-credentials — they *reduced the number of payment decisions*; they did not make tiny decisions cheap.

### (2) Per mechanism: does removing the human remove it, keep it, or transform it?

- **M1 — REMOVED at transaction time, TRANSFORMED into a policy-setting cost.** Sourced core: Szabo/Shirky locate the cost in a human's per-event decision; an agent evaluating a $0.001 call against a utility function does not incur it; Shirky's impossibility dissolves when the approver is code. Sourced counterweight: Szabo's 1999 agent paragraph — the cost migrates to whether the human can trust the agent's spending policy. Inference: the human now makes one meta-decision (budget + policy), which is exactly the flat-fee/insurance structure Szabo said humans want — the mechanism is relocated to a layer where it's payable once. **The strongest genuine escape in the record.**
- **M2 — PARTIALLY KEPT.** Inference anchored in Odlyzko: the psychological half disappears (no AOL indignation), but the seller-side half survives: sellers still profit from bundling and usage maximization, and humans funding agents still prefer capped predictable spend — today's dominant AI pricing (subscriptions, committed tiers) is already flat-rate-shaped; Cloudflare prices "flat, per-request... across their entire site" — flattening *inside* the metered model. Budget-capped agents recreate PEAK's budget-anxiety inhibition in literal code.
- **M3 — KEPT.** Sourced: payment adoption is glacial independent of technology; pay-per-crawl still "in private beta"; x402's 130M transactions real but tiny and heavily crypto-internal. Inference: agents shrink the *merchant integration* cost, but sellers won't price per-request until paying agents exist and vice versa. The historical escape route (piggyback on what everyone has) maps to Cloudflare / Coinbase wallets / the model providers. The aggregator re-forms ("Merchant of Record").
- **M4 — REMOVED, conditionally.** Sourced: <$0.0001 gas at 200ms removes the arithmetic impossibility — a genuine technological change since Shirky/Odlyzko. Caveat (inference): the floor was never the binding constraint for humans; removing it is necessary for machine micropayments, not sufficient for anything.
- **M5 — TRANSFORMED, not removed.** Sourced: irreversibility kills the Flooz failure mode, but Ling et al. show adversarial economics reappearing: settlement races, allowance overdraft, 100% resource leakage, 8.7× attacker leverage, an impossibility result on fair output-based pricing. Irreversibility shifts fraud risk onto the *payer* — inverting, not eliminating, the trust problem. Cloudflare's Ed25519 bot identity confirms fraud/identity is first-order in the machine era too.
- **M6 — KEPT, arguably strengthened.** Inference: the incumbents this time are the AI platforms; a lab bundling search/browsing/tools into a flat subscription is Microsoft-Office-bundling with better margins. Per-request wins only in the long tail platforms don't bundle — matching Odlyzko's "(very likely small) niche" prediction.
- **M7 — KEPT in mutated form.** KYC/AML pressure on stablecoin rails; sellers want to identify and price-discriminate between crawlers — Cloudflare's design is *de*-anonymizing bots. Anonymous machine cash faces the same institutional headwinds eCash did.

**Net answer (agent synthesis, labeled):** The record identifies ~seven mechanisms; the famous one (mental costs) is the one agents most plausibly remove, and the fee floor genuinely falls. But the actual 1990s corporate deaths trace mostly to M3/M5/M6/M7 — cold start, fraud, competition, distribution — and those survive or transform. "Removing the human removes the binding constraint" is true only if mental cost was the binding constraint — and the record suggests it bound *whether demand existed at all*, while the others bound *any given system's survival*. Agents relieve the demand-side constraint while leaving the supply-side/institutional ones live — predicting machine micropayments become *possible* but consolidate around a few aggregator/merchant-of-record chokepoints, not a frictionless open mesh.

### (3) What the record does NOT settle — open questions for a paid deep-research run

1. **Whether the mental-cost relocation is stable:** no empirical study on how humans set/adjust agent spending policies, tolerate spend variance, or demand flat-rate agent products (Szabo's 1999 trust objection, untested at scale).
2. **Real x402/pay-per-crawl adoption quality:** 130M transactions — how much is organic paid demand vs airdrop farming/self-dealing inside crypto? No independent decomposition found. Cloudflare beta results unpublished.
3. **Peppercoin's precise cause of death:** the strongest natural experiment (Rivest/Micali aggregation cryptography — M1+M4 addressed by design, still failed) — no serious post-mortem found, only acquisition notices.
4. **Carrier billing economics:** the predicted escape route partially worked — no scholarly quantification found of its fee structure (30–40%?) and why it stayed niche.
5. **Seller-side bundling equilibrium for machine buyers:** does bundling math change when the buyer is an agent with uncorrelated spiky demand across thousands of sellers? Nothing models this; it may be the actual crux.
6. **Whether irreversibility is regulatorily survivable:** consumer-protection and AML treatment of irreversible autonomous stablecoin payments — no serious legal analysis surfaced.
7. **The Odlyzko test applied forward:** payment regimes take decades even with forcing agents; who is the forcing agent for x402-style rails (Coinbase? Cloudflare? model providers?), and does their incentive point at open protocols or proprietary bundles?

**Source-quality note:** 10 of 12 read directly. Flooz and Blendle claims rest on search summaries of named articles — re-verify before publication. Odlyzko 2001 extraction lossy — paraphrase-level. No fabricated URLs or quotes.
