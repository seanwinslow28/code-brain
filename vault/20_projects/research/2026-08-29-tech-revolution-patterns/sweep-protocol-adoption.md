# Sweep — why open protocols win or lose, mapped to the agent web (2026-08-29)

Stage-0 research-agent sweep, 12 sources read (not just searched). Question 3 of the
historical-patterns funnel: what made winning open protocols win, and what does that
predict for x402 / WebMCP / MCP / A2A / AP2 / ACP? Quotes verbatim as extracted;
classification per source; agent's own inference marked as inference.

## PART A — SOURCES READ

### Historical episodes

**1. "OSI: The Internet That Wasn't"** — Andrew L. Russell, IEEE Spectrum, July 29, 2013 — https://spectrum.ieee.org/osi-the-internet-that-wasnt
**Classification: scholarly historian** (Russell later expanded this into *Open Standards and the Digital Age*, Cambridge UP).
Key claims:
- Committee gridlock was structural: "Everything was up for debate—even trivial nuances of language, like the difference between 'you will comply' and 'you should comply.'"
- Charles Bachman (1978): "The organizational problem alone is incredible... trying to get representatives from ten major and competing computer corporations... to come to any agreement."
- Price/availability asymmetry decided it — an IBM France engineer: "On one side you have something that's free, available, you just have to load it. And on the other side... expensive."
- ARPA subsidized TCP/IP implementations in Berkeley Unix, then forced the tip: "On 1 January 1983, ARPA stopped supporting the ARPANET host protocol, thus forcing its contractors to adopt TCP/IP."
- Incumbent vendors gamed the committee — John Day: "IBM played them like a violin. It was truly magical to watch."
- Louis Pouzin (1991): "It is easier and quicker to... interconnect heterogenous systems with TCP-based products."
- The IETF's credo — David Clark's 1992 "We reject: kings, presidents and voting. We believe in: rough consensus and running code" — quoted there as the cultural counter-model to OSI's committee process.

**2. "Where Have all the Gophers Gone? Why the Web beat Gopher in the Battle for Protocol Mind Share"** — Christopher (Cal) Lee, April 1999 — https://ils.unc.edu/callee/gopherpaper.htm
**Classification: scholarly** (graduate research paper, interview-based).
Key claims:
- Architecture: HTML let "document creators place links within documents, whereas Gopher provided pointers to documents through menu files, which existed separate from the documents themselves."
- The 1993 UMinn licensing move destroyed trust: "Rumors of the technology being licensable provoked a general re-evaluation" among developers steeped in open-access norms.
- Mosaic's UX mattered: "a cleaner GUI, viewing images within the text of documents, a back button."
- Governance centralization hurt: the Gopher team "put too much burden on themselves for providing innovations."
- Institutional credibility: "The Web had the advantage of coming out of CERN."
- Corroborating detail: MinnPost 2016 history — the licensing announcement "socially killed Gopher" per its own developers; 1993 Gopher traffic grew 997% vs. the Web's 341,634% — https://www.minnpost.com/business/2016/08/rise-and-fall-gopher-protocol/

**3. "The Rise and Demise of RSS"** — Two-Bit History (Sinclair Target), December 18, 2018 — https://twobithistory.org/2018/12/18/rss.html
**Classification: practitioner-historian.**
Key claims:
- Governance fork wars: by 2003 there were "three competing versions of RSS: Winer's RSS 0.92... the RSS-DEV Working Group's RSS 1.0, and Atom"; Winer felt it "unfair" that RSS-DEV "arrogated the 'RSS 1.0' name."
- The substitute was better for users: "Twitter was basically a better RSS feed, since it could show you what people thought about an article in addition to the article itself."
- Business-model misalignment killed corporate support: "Google might have been able to monetize Google+ in a way that it could never have monetized Google Reader."
- End-user friction: sites "linked to their RSS feeds using little orange boxes labeled 'XML'" — an open format too geeky to cross the chasm.

**4. Secure Electronic Transaction (SET)** — Wikipedia — https://en.wikipedia.org/wiki/Secure_Electronic_Transaction
**Classification: tertiary reference** (factual skeleton; corroborated by TechTarget/GeeksforGeeks).
Key claims:
- SET Consortium "established in 1996 by Visa and Mastercard," backed by "GTE, IBM, Microsoft, Netscape, SAIC, Terisa Systems, RSA, and VeriSign" — the heavyweight-consortium play.
- Died on friction: "The implementation by each of the primary stakeholders was either expensive or cumbersome"; consumers needed digital-wallet software and client certificates; speculation that Microsoft "sought transaction fees from SET-compliant components."
- TechTarget corroboration: SET "never succeeded in the marketplace because of its high overhead and additional requirement of public key infrastructure (PKI)" — https://www.techtarget.com/searchsecurity/definition/Secure-Electronic-Transaction-SET. Deployed 1997, decommissioned 2002. SSL — already in every browser — carried e-commerce instead; Visa retreated to 3-D Secure.
- Shapiro & Varian (1999), writing while SET looked alive, cited it as a model of cooperative standard-setting. The consortium was flawless; the adoption physics weren't.

### Economics / theory

**5. "The Art of Standards Wars"** — Carl Shapiro & Hal R. Varian, California Management Review 41(2), Winter 1999 (adapted from *Information Rules*) — http://sjbae.pbworks.com/f/shapiro_varian_1999.pdf (read in full)
**Classification: scholarly** (the canonical treatment).
Key claims:
- "Network markets tend to tip towards the leading player, unless the other players coordinate to act quickly and decisively."
- "A large buyer (in this case the U.S. government) can have more influence than suppliers in tipping the balance." (railroad gauges; ARPA 1983 is the networking rhyme)
- Seven key assets decide wars: "control over an installed base of users; intellectual property rights; ability to innovate; first-mover advantages; manufacturing capabilities; strength in complements; and brand name and reputation." And: "No one asset is decisive."
- Evolution vs. Revolution: "Evolutionary strategies are based on offering superior performance with minimal consumer switching or adoption costs"; revolutionary tech must offer "such compelling performance that consumers are willing to incur significant switching or adoption costs." (NTSC color TV won *because* black-and-white sets could still receive it.)
- "Adoption of a new technology can be painfully slow if the price/performance ratio is unattractive and if it requires adoption by a number of different players."
- "First-mover advantages need not be decisive, even in markets strongly subject to tipping" and "Victory in a standards war often requires building an alliance."

**6. "The Rise of Worse is Better"** — Richard P. Gabriel — https://www.dreamsongs.com/RiseOfWorseIsBetter.html
**Classification: practitioner** (Lisp implementer analyzing his own side's loss).
Key claims:
- "It is more important for the implementation to be simple than the interface. Simplicity is the most important consideration."
- "Unix and C are the ultimate computer viruses" — 50–80% solutions that port everywhere spread virally.
- Worse-is-better software "first will gain acceptance, second will condition its users to expect less, third will be improved."
- The Right Thing "takes a long time to get out, and it only runs satisfactorily on the most sophisticated hardware." (OSI, SET, and Xanadu in one sentence. Gary Wolf's "The Curse of Xanadu" not separately fetched — covered by this + Gopher/OSI material.)

### The 2024–2026 agent-protocol landscape

**7. "A Survey of AI Agent Protocols"** — Yingxuan Yang et al. (Shanghai Jiao Tong University), arXiv:2504.16736, April 2025 (rev. June 2025) — https://arxiv.org/abs/2504.16736
**Classification: scholarly.**
Key claims: "There is no standard way for these agents to communicate with external tools or data sources"; fragmentation "makes it difficult for agents to work together or scale effectively"; proposes "a systematic two-dimensional classification that differentiates context-oriented versus inter-agent protocols" — academia treats MCP (context-oriented) and A2A (inter-agent) as different layers, not competitors.

**8. "MCP joins the Agentic AI Foundation"** — David Soria Parra (lead maintainer), MCP blog, December 9, 2025 — https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/
**Classification: vendor.**
Key claims: "Anthropic is donating MCP to the Agentic AI Foundation, a directed fund under the Linux Foundation," "co-founded by Anthropic, Block and OpenAI, with support from Google, Microsoft, AWS, Cloudflare and Bloomberg"; "over 97 million monthly SDK downloads"; "10,000 active servers and first-class client support across major AI platforms"; the Linux Foundation "will not dictate the technical direction of MCP." (Adoption figures vendor-reported.)

**9. "The State of WebMCP: July 2026"** — Sean Ryan, Spronta, July 23, 2026 — https://www.spronta.com/blog/state-of-webmcp-july-2026/
**Classification: practitioner** (independent; corroborated by Chrome's vendor post, https://developer.chrome.com/blog/ai-webmcp-origin-trial — Chrome 149–156 origin trial, announced at I/O May 2026).
Key claims: WebMCP is "a Draft Community Group Report" — not on the W3C standards track; "Chrome is running a public origin trial from Chrome 149 through 156"; Edge behind a flag, "Firefox and Safari observe discussions without commitments"; "No mainstream agent calls WebMCP tools yet" — "a 0% adoption standard" where checker tools outnumber implementations; if Gemini-in-Chrome slips to 2027, WebMCP risks joining "Web Intents in the museum of browser APIs"; prompt-injection/confused-deputy questions "remain largely unaddressed."

**10. "Cloudflare and AWS Embed x402 Agent Payments at the Edge"** — Steef-Jan Wiggers, InfoQ, July 6, 2026 — https://www.infoq.com/news/2026/07/cloudflare-aws-x402-micropayment/
**Classification: practitioner press.**
Key claims: x402 "revives HTTP's long-dormant 402 'Payment Required' status code"; Cloudflare's Monetization Gateway "lets any Cloudflare customer charge for web pages, APIs, datasets, or MCP tools"; AWS "shipped the same capability in CloudFront and AWS WAF as a generally available feature" within weeks; Coinbase reports "over 169 million payments across 590,000 buyers and 100,000 sellers in its first year" (vendor-reported, relayed by press); the x402 Foundation "launched under the Linux Foundation in April 2026" with AWS, Cloudflare, Anthropic, Circle and 20+ members; skeptics ask whether "bots choose to pay rather than just use the public endpoints"; "anonymous stablecoin micropayments create an accounting problem that the protocol does not solve" (VAT/invoicing).

**11. "Announcing Agent Payments Protocol (AP2)"** — Stavan Parikh & Rao Surapaneni, Google Cloud Blog, September 16, 2025 — https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
**Classification: vendor.**
Key claims: AP2 is "an open protocol developed with leading payments and technology companies to securely initiate and transact agent-led payments"; built on "Mandates—tamper-proof, cryptographically-signed digital contracts that serve as verifiable proof of a user's instructions"; solves "proving that a user gave an agent the specific authority to make a particular purchase"; "more than 60 organizations" including Amex, Mastercard, PayPal, Adyen, Coinbase; "can be used as an extension of the Agent2Agent (A2A) protocol and Model Context Protocol (MCP)," with an A2A x402 extension for crypto settlement. Updates: A2A donated to the Linux Foundation, "150+ supporting organizations," production use in Azure AI Foundry, Bedrock AgentCore, Agentforce (https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year — foundation/vendor); Google donating AP2 to the FIDO Alliance (https://blog.google/products-and-platforms/platforms/google-pay/agent-payments-protocol-fido-alliance/ — vendor).

**12. "Developing an open standard for agentic commerce" (ACP)** — Jeff Weinstein & Steve Kaliski, Stripe, September 29, 2025 — https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce
**Classification: vendor.**
Key claims: ACP "enables programmatic commerce flows between buyers, AI agents, and businesses"; codeveloped with OpenAI to power "Instant Checkout in ChatGPT"; "ACP is open source, Apache 2.0 licensed, and community-designed"; merchants "maintain your customer relationships as the merchant of record, retaining control"; "ACP can connect with any commerce backend and payments infrastructure"; launch merchants: Etsy sellers plus Shopify brands "Glossier, Vuori, Spanx, and SKIMS." (OpenAI's companion post 403'd; Salesforce independently announced ACP support, October 2025.)

## PART B — RECURRING WIN/LOSE FACTORS (evidenced across multiple episodes)

**F1. Running code with zero-cost distribution beats specified perfection.** TCP/IP free in BSD vs expensive/late OSI stacks (Russell); SSL in every browser vs SET's wallets and certificates; Gabriel's thesis; Mosaic shipped image support while Gopher debated (Lee). *Four episodes.*

**F2. Evolution beats revolution: ride the installed base, don't replace it.** Shapiro & Varian's central law (NTSC vs CBS color); SSL rode existing cards and browsers while SET demanded new PKI from every party; TCP/IP interconnected existing heterogeneous networks (Pouzin). *Three episodes plus theory.*

**F3. Per-adopter friction is fatal even when the design is "better."** SET's "expensive or cumbersome" implementation for every stakeholder; RSS's orange XML boxes vs Twitter's follow button; OSI's seven-layer conformance burden; Gabriel's 50%-solution virality. *Four episodes.*

**F4. Governance credibility — cheap, open, non-rent-seeking, fork-resistant — is a survival condition.** Gopher "socially killed" by one licensing announcement while CERN released the Web royalty-free; RSS bled out through fork wars; OSI's committee captured ("IBM played them like a violin"). Neutral-home donation is now table stakes. *Three episodes.*

**F5. A large sponsor/buyer can tip the market — and single-sponsor dependence is a single point of failure.** ARPA's 1983 mandate; the U.S. government on railroad gauges; Google Reader's shutdown as RSS's demise-accelerant — the sponsor that tips you up can tip you over. *Three episodes.*

**F6. Business-model alignment of the parties who must do the work.** RSS died because an open format "didn't give technology companies the control over data and eyeballs that they needed to sell ads"; SET wobbled partly on Microsoft's rumored transaction fees; color TV stalled until RCA bought the killer-app content. *Three episodes.*

**F7. Consortium size ≠ victory; friction and demand decide.** SET had Visa, Mastercard, Microsoft, Netscape, IBM — and died in five years. OSI had every government and vendor on Earth. Alliances often *necessary*, never *sufficient*; "first-mover advantages need not be decisive." *Three episodes.*

## PART C — FACTOR-BY-FACTOR READ OF THE CURRENT CONTENDERS

**MCP** — *The TCP/IP of this cycle, on the evidence so far.* F1: overwhelming — 97M monthly SDK downloads, 10K servers, every major client (sourced, vendor-reported). F2: evolutionary — wraps existing APIs. F4: donated to a Linux Foundation fund co-founded by its chief rival OpenAI (sourced) — the anti-Gopher move, executed before any licensing scare. F5: multi-sponsor. Fragility (inference): security story still maturing; F3 cuts both ways — MCP won on low friction, which historically means the hard problems (auth, trust) were deferred TCP/IP-style, to be retrofitted for decades.

**WebMCP** — *Highest structural risk in the field.* F5: single-sponsor dependence on Chrome shipping Gemini consumption — sourced ("if delayed into 2027... museum of browser APIs"), the pattern that killed Web Intents and wounded RSS-after-Reader. F1: fails today — "no mainstream agent calls WebMCP tools yet," "a 0% adoption standard" (sourced, practitioner). F4: not on the W3C standards track (sourced). F2: genuinely evolutionary (three JS methods on existing sites — inference from Chrome docs), its best asset. Verdict (inference): the design honors worse-is-better, but supply-side tooling without a demand-side client is CBS color television — a standard with no receivers.

**x402** — *Evolutionary envelope, revolutionary payload.* F2 split (inference, the most interesting call in the field): reviving HTTP 402 is a maximal installed-base move at the protocol layer, but stablecoin settlement is a *revolution* at the money layer — exactly where SET taught that revolutions die. Mitigating difference (inference): SET's friction fell on human consumers; x402's falls on software agents, which don't experience friction, so the SET precedent may not bind. F1: real running code at Cloudflare and AWS edges (sourced); 169M payments in year one (vendor-reported via press). F4: Linux Foundation home (sourced). F6: unresolved — bot-pays-vs-scrapes and the VAT/accounting gap are sourced skepticism, and they are precisely RSS-style monetization-alignment problems.

**A2A** — *The consortium-shaped one.* F7 is the warning: 150+ organizations, Linux Foundation home, big-cloud deployments (sourced, foundation/vendor) — but SET and OSI prove roster size is the weakest predictor on the board. F1: harder to verify than MCP's; "production use" claims come from the foundation's own press release; the scholarly survey treats A2A as a distinct layer (inter-agent vs context-oriented — sourced) rather than winning one. Inference: A2A's fate resembles OSI's question — whether a spec written ahead of organic demand finds running code before the simpler thing (agents just calling each other's MCP tools or plain HTTP) absorbs the use case.

**AP2** — *The closest structural rhyme to SET in the entire landscape* (inference; the sweep's sharpest historical echo): a purpose-built, cryptographically rigorous payment-authorization protocol, launched by a consortium of 60+ payment incumbents including the same card networks, solving trust "the right thing" way with mandates and verifiable credentials (sourced). Every SET failure factor is present in form: multi-party PKI-ish burden, consortium-first adoption, clean-slate trust chain. Differences (inference): agents, not consumers, bear the friction; and the FIDO Alliance donation (sourced) puts it under a body that shipped WebAuthn into every browser — evidence that consortium + installed-base-riding *can* work when platforms absorb the friction.

**OpenAI/Stripe ACP** — *The SSL of the payments fight — with an asterisk.* F2: maximal — rides existing card rails, merchant systems, Stripe integrations ("as little as one line of code," sourced), as SSL rode existing cards. F5: distribution through the single largest consumer agent surface (ChatGPT + Etsy + Shopify merchants, sourced). F4 is the asterisk (inference): "open source, Apache 2.0, community-designed" is a vendor claim; effective control sits with two firms — survivable (SSL was Netscape's) *if* the steward doesn't rent-seek; the Gopher/Minnesota trap is one bad monetization announcement away. On pure historical form, ACP's incremental-hack profile is the winning pattern, and AP2-vs-ACP re-runs SET-vs-SSL almost beat for beat — with the open question whether the card networks learned to put their rigor *underneath* the low-friction path (AP2 claims composability with other stacks) rather than in place of it.

## PART D — WHERE THE DATA IS THINNEST (target for the paid deep-research run)

**F6 — business-model alignment and non-vendor adoption measurement.** Every load-bearing adoption number in the current landscape (MCP's 97M downloads and 10K servers, x402's 169M payments, A2A's "production use," ACP's merchant counts) is vendor- or foundation-reported; no independent instrumentation-based measurement found in this sweep. No source answers the RSS question for the agent web: *do the parties who must do the ongoing work — merchants serving agent traffic, sites exposing WebMCP tools, publishers behind x402 paywalls — actually make money doing it, and who captures the take-rate?* RSS proves an open protocol can achieve full technical adoption and still rot because the economics never worked for the servers. A paid DR run should hunt: independent traffic/settlement measurements (payment-processor filings, chain analytics for x402, crawl-based WebMCP/ACP endpoint counts), disclosed fee structures on Instant Checkout, and early merchant P&L evidence from agent-mediated commerce. Per the repo's DR guidance this is a market-shaped question — expect vendor SEO contamination, so frame it as falsification of named claims (e.g., "find independent corroboration or refutation of Coinbase's 169M-payment figure"), not an open survey.
