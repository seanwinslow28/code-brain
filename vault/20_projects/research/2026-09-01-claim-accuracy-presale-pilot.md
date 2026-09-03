---
title: "Claim-level accuracy pre-sale pilot — 4 businesses, 25 answers, 2 assistants"
date: 2026-09-01
project: agentic-web-startup
type: research-pilot
status: final
tags: [agentic-web, presale-test, claim-accuracy, misrepresentation-seam, wtp]
---

# Claim-level AI accuracy report — pre-sale pilot (run 2026-09-01, ~06:00)

The screenshot pre-sale test, reshaped per the seam recon: the artifact to pre-sell
is the **claim-level accuracy report** ("here are the untrue things assistants tell
your buyers"), not the journey grade. This pilot built the harness, ran it against 4
real businesses, and produced the owner-facing exemplar artifact. **What it proves:**
the artifact is producible in ~2 hours at $0 and the errors it finds are real,
receipted, and buyer-harming. **What it can't prove:** whether an owner pays —
that requires Sean putting the exemplar in front of real owners (next step, his).

## Method

- **Targets:** 4 real SMBs selected for a *recently changed fact documented on their
  own website* (the site is both ground truth and the delta assistants should be
  stale on). Selected + ground-truthed by a research agent (all sites fetched
  2026-09-01): Your Brother's Bookstore (Evansville IN, moved ~Apr 2026 + hours
  changed), Kohler's Bakery (Avalon NJ, seasonal wind-down schedule), Ugly Baby
  (Brooklyn NY, reopened at a new address 2026-08-27 after 2024 closure), KMP
  Plumbing Heating & Air (Fort Worth TX, June-2026 rebrand kmpcorp.com→callkmp.com,
  verified 301 + specials expired 2026-08-26).
- **Probes:** buyer-shaped questions asked blind on two assistant surfaces:
  **Perplexity** (free plan, Sean's account, fresh thread per question, via browser;
  9 questions) and **Claude-with-web-search** (subagents instructed to answer as a
  consumer assistant, not audit; blind to ground truth; 16 questions).
- **Verification:** every assistant claim graded against the business's own site
  (fetched same day). Stale third-party sources feeding errors identified where
  findable. Triage lens: "would a buyer acting on this walk away / waste a trip?"

## Scorecard — 25 answers

| # | Business | Question | Perplexity | Claude |
|---|---|---|---|---|
| 1 | Bookstore | Where located? | ✅ new address | ✅ new address (+ flags old one) |
| 2 | Bookstore | Open Mondays? | ❌ **"Yes, Mon 10–7"** — store is CLOSED Mondays; dismissed the site's correct hours as "conflicting older text" | ✅ closed Mondays |
| 3 | Bookstore | Order online? | — | ✅ bookshop.org path |
| 4 | Bookstore | Manga + used books? | — | ✅ (adds unverified "board games" ⚠) |
| 5 | Bakery | Open this Friday (Sep 4)? | ❌ **"Yes… should be open"** — site says CLOSED | ✅ closed, offers Sat/Sun |
| 6 | Bakery | Labor Day hours? | ✅ 8–10am, final day | ✅ 8–10am + sell-out warning |
| 7 | Bakery | Donut price? | — | ✅ $3.25 / $3.50 |
| 8 | Bakery | Still pre-order for weekend? | ❌ **"Yes — still taking pre-orders"** (+ invents 8–10:30 Monday hours) | ❌ **"Yes"** — every item shows SOLD OUT |
| 9 | Restaurant | Permanently closed? | ✅ reopened 8/27, new address | ✅ reopened, warns off old address |
| 10 | Restaurant | Address? | — | ✅ 364 Grand St |
| 11 | Restaurant | Open for lunch? | ✅ dinner-only from 5pm | ✅ dinner-only |
| 12 | Restaurant | Reservations? | — | ✅ Resy + walk-ins |
| 13 | Plumber | Specials right now? | ✅ *model answer:* lists them but flags all expired Aug 2026 | ⚠ leads "Yes" on expired specials, hedges late; adds unverified $317 offer |
| 14 | Plumber | Website + phone? | ✅ callkmp.com + correct phone | ✅ (but offers stale info@kmpcorp.com email ⚠) |
| 15 | Plumber | Comfort Club price? | — | ✅ $24.99/mo |
| 16 | Plumber | 24/7 emergency? | — | ✅ |

**Tally: 18/25 right · 4/25 confidently wrong · 3/25 shaky (unverified embellishment
or misleading lead).** Every one of the 4 clear errors misdirects a real buyer: two
wasted trips (Monday bookstore, Friday bakery), two phantom-inventory purchases
(sold-out pre-orders, twice — the one error BOTH surfaces made).

## Findings that matter for the product

1. **The killer specimen exists and we captured it:** Perplexity read the
   bookstore's *current, correct* hours and **discarded them as "conflicting older
   text"** in favor of pre-move directory hours. Fixing your website is provably not
   sufficient — the exact claim the r/DigitalMarketing thread hand-wrings about,
   reproduced on demand.
2. **Press coverage is the strongest correction signal found.** Ugly Baby (fresh
   reopening covered by Eater/TimeOut/Greenpointers) scored 6/6 across both
   surfaces. The bookstore's un-newsworthy hours change is where the error lives.
   Sellable implication: the correction workflow's "publish a crawlable
   contradiction" move has evidence behind it.
3. **Commerce availability is a blind spot on both surfaces** (sold-out ≠ absent:
   both assistants confidently sold unavailable products). Distinct error class from
   stale facts; worth its own claim category in the report format.
4. **Capability ≠ consistency.** Perplexity handled KMP's expired coupons perfectly
   (finding 13) and flubbed the bakery's posted Friday closure two questions
   earlier while citing the same domain. Per-question variance IS the monitoring
   pitch — a one-time audit undersells it.
5. **Stale-source chains are findable and nameable:** old bookstore address still
   live on bookishthingstodo.com and i-70corridor.com (with a wrong phone);
   whereyoueat.com still lists the restaurant's dead address + invented 11am–9pm
   hours; bestplumbers.com still points at kmpcorp.com with a different phone. These
   are the "here's where the rot lives" receipts in the owner artifact.

## The owner-facing exemplar

Built for Your Brother's Bookstore (cleanest single high-impact error + named
stale-source chain): "The Monday Problem" — the one-page claim-level accuracy
report, published as a private artifact for Sean's pre-sale use:
https://claude.ai/code/artifact/3f69e846-91b9-43e3-9566-d57306f2e1b3
(prototype label included, no commissioned-audit framing; share menu controls
distribution — it stays private until Sean shares it).

## Honest limits

Two surfaces only (no ChatGPT/Gemini/Google-AI-Overviews probes — ChatGPT needs
Sean's logged session and consent to consume quota; Google AI Overviews didn't get
probed this run); n=4 businesses selected FOR staleness likelihood (error rates here
are not population estimates — 3 of 4 clear errors landed on the two businesses
whose changes got no press, which is the selection working as designed); "Claude
answering as an assistant" is a simulation of assistant behavior on one vendor's
stack, honestly labeled; Perplexity answers came from Sean's logged-in free-plan
account (personalization effects unknown). The WTP question remains open until an
owner sees the report.

## Provenance

- Ordered by Sean 2026-09-01 ("Run the screenshot pre-sale test with the
  claim-level accuracy report").
- Ground-truth + staleness evidence: selection-agent fetch ledger (14 fetched URLs)
  preserved in session transcript; key ones inline above.
- Probe transcripts: Perplexity thread URLs in session record; Claude probe agents'
  full answers in session record.
- Feeds: [Sept-1 sitting kickoff](../../docs/prompts/2026-09-01-agentic-web-sept-1-sitting-kickoff.md)
  (context file 4) · [sitting-inputs brief](2026-08-30-sept-1-sitting-inputs-indicator-read.md)
  · [seam recon](2026-08-30-seam-recon-last30days-falsification.md).
