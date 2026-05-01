---
title: "Stripe adds x402 integration for USDC agent payments on Base"
source: "https://www.theblock.co/post/389352/stripe-adds-x402-integration-usdc-agent-payments"
author:
  - "[[Brian Danga]]"
published: 2026-02-11
created: 2026-04-24
description: "Stripe launched x402-based USDC agent payments on Base as CoinGecko enabled $0.01 pay-per-request crypto data access."
tags:
  - "source/web-clip"
type: "source"
status: draft
domain: [product-management]
ai-context: "Stripe integrated x402 to let developers charge AI agents in USDC on Base via PaymentIntents API; CoinGecko launched $0.01-per-request x402 endpoints."
---
Stripe has unveiled a preview of machine payments on its platform, integrating the x402 protocol to enable developers to charge AI agents directly using the USDC stablecoin on the Base network.

Jeff Weinstein, product lead at Stripe, [wrote](https://x.com/jeff_weinstein/status/2021331763960873058) on X on Tuesday that the deployment would eventually expand to include additional protocols, currencies, and blockchains. The system utilizes the PaymentIntents API to allow businesses to programmatically charge AI agents for API usage, Model Context Protocol calls, and HTTP requests.

The x402 protocol, an open payment standard developed by Coinbase, repurposes the previously dormant HTTP 402 "Payment Required" status code to enable onchain payments directly within a standard web request. Weinstein noted that the current financial system is tuned for humans and is incompatible with agent needs, which include microtransactions, 24/7 global rails, and low-latency finality guarantees.

Under the preview, a developer creates a PaymentIntent, after which Stripe generates a deposit address that is passed to an agent to send funds or a payment token. Transaction status can then be tracked through an API, webhook or the Stripe dashboard before the funds settle, according to the post.

Sales tax, refunds and reporting are handled within Stripe's existing tooling, Weinstein wrote, adding that developers only need to engage with crypto components if they choose. Stripe also released an open-source command line tool called purl, plus Node and Python samples, to test machine payments.

The product launch came as Bloomberg [reported](https://www.bloomberg.com/news/articles/2026-02-09/stripe-valuation-set-to-hit-140-billion-in-new-tender-offer) Tuesday that the payments giant is exploring a higher valuation. Citing a person familiar with the matter, the report said Stripe is arranging a tender offer that would value the company at $140 billion — a 31% increase from its $107 billion valuation last year. In 2023, the company [raised $6.5 billion](https://stripe.com/en-pl/newsroom/news/stripe-series-i-employee-liquidity) in a Series I funding round led by Thrive Capital.

## CoinGecko adds x402 payments

Simultaneously, market data provider CoinGecko launched x402-powered API endpoints, according to a [statement](https://www.coinbase.com/en-gb/developer-platform/discover/launches/coingecko-x402) released Tuesday. The integration turns its API into a pay-per-use utility, letting autonomous agents fetch price and onchain data for a flat rate of $0.01 USDC per request without requiring an account or API key.

Supported endpoints include price queries and multiple onchain routes, while the statement said CoinGecko's overall coverage spans more than 18,000 cryptocurrencies and over 250 networks. Builders can use it to create autonomous arbitrage monitors or onchain risk watchdogs.

The x402 flow for CoinGecko follows a standard handshake: an agent calls an endpoint, receives a 402 response with payment details, attaches a USDC payment authorization, and retries the call to access the data.

---
*Clipped from [theblock.co](https://www.theblock.co/post/389352/stripe-adds-x402-integration-usdc-agent-payments) on 2026-04-24T10:03:15-04:00*
