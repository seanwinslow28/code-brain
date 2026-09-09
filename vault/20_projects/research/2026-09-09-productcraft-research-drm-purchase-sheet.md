---
title: "Productcraft map research — DRM-free availability per tier-1 title, purchase sheet (#283)"
date: 2026-09-09
project: productcraft
status: filed — resolves Productcraft map ticket #283
tags: [research, productcraft, wayfinder]
cost: $0 (web research by a subagent; no paid research)
---

# R1 — DRM-free availability per tier-1 title (purchase sheet)

Research note. Facts and expectations only, with the confidence of each row stated. Automated verification of retail listings was **blocked** this session: ebooks.com's search API returns 403 to non-browser clients and its search page is a JavaScript app; two subagents stalled on retail domains without writing. What follows was verified by direct fetch where a site allowed it, and otherwise inferred from publisher policy, which is stated per row. **The purchase task verifies every "expected" row at checkout before paying.**

## How to read DRM status

- **DRM-free** — the seller states no DRM (ebooks.com marks each format "DRM Free"; author stores usually say so outright). book-to-skill can ingest it.
- **Watermark** — social DRM (buyer's name stamped in the file); ingestible.
- **Adobe DRM** — locked; book-to-skill cannot read it, and this project does not strip DRM. The lane manifest then carries a "read by Sean, not ingested" row.
- **Expected** — inferred from the publisher's standing practice, not seen on a listing this session.

## Purchase sheet

| # | Title | Publisher | DRM status | Where to buy first | Fallback | Verified this session |
|---|---|---|---|---|---|---|
| 1 | Rumelt, *Good Strategy Bad Strategy* | Crown Currency (PRH) | **Adobe DRM expected** — PRH trade titles carry DRM on every retailer | ebooks.com (check the format badge) | Kindle for reading only; treat as not ingested | No (retail blocked) |
| 2 | Dunford, *Obviously Awesome* (2026 updated ed.) | Ambient Press (self-published) | **DRM-free expected** — self-published on KDP/Kobo; Kobo lists many self-published titles DRM-free | aprildunford.com book page → retailer links (page reachable, 200) | Kobo, filter "DRM-free" | Page reachable; DRM field not shown |
| 3 | Torres, *Continuous Discovery Habits* | Product Talk LLC (self-published) | **DRM-free expected** — self-published; Torres sells direct and via Amazon/Kobo | producttalk.org/continuous-discovery-habits (reachable, 200) → retailer links | Kobo DRM-free filter | Page reachable; DRM field not shown |
| 4 | Fitzpatrick, *The Mom Test* (current ed.) | Self-published (author store) | **DRM-free expected** — the author sells the ebook bundle directly at momtestbook.com; author direct sales are conventionally DRM-free | momtestbook.com (curl was blocked; open in a browser) | Kobo | No (site blocked curl) |
| 5 | Bland & Osterwalder, *Testing Business Ideas* | Wiley | **Expected DRM-free or watermark on ebooks.com** — Wiley sells many business titles DRM-free there; must confirm the badge | ebooks.com, then wiley.com | Kobo | No (retail blocked) |
| 6 | Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* | Cambridge University Press | **Watermark/DRM-free expected** — Cambridge Core sells chapter and book PDFs without Adobe DRM; ebooks.com badge to confirm | cambridge.org/core book page (curl timed out; open in a browser) | ebooks.com | No (site timed out) |
| 7 | Ellis & Brown, *Hacking Growth* | Crown Currency (PRH) | **Adobe DRM expected** | ebooks.com (check badge) | Kindle, not ingested | No |
| 8 | Ramanujam & Tacke, *Monetizing Innovation* | Wiley | **Expected DRM-free or watermark on ebooks.com** | ebooks.com, then wiley.com | Kobo | No |
| 9 | Bryar & Carr, *Working Backwards* | St. Martin's Press (Macmillan) | **Adobe DRM expected** — Macmillan trade titles carry DRM | ebooks.com (check badge) | Kindle, not ingested | No |
| 10 | Patton, *User Story Mapping* | O'Reilly | **DRM-free** — O'Reilly titles on ebooks.com are sold DRM-free (Systemcraft bought five this way, 2026-08) | ebooks.com | — | Precedent, not re-checked |
| 11 | Lombardo et al., *Product Roadmaps Relaunched* | O'Reilly | **DRM-free** — same as above | ebooks.com | — | Precedent, not re-checked |
| 12 | Grove, *High Output Management* | Vintage (PRH) | **Adobe DRM expected** | ebooks.com (check badge) | Kindle, not ingested | No |
| 13 | Cagan & Jones, *EMPOWERED* | Wiley | **Expected DRM-free or watermark on ebooks.com** | ebooks.com, then wiley.com | Kobo | No |
| 14 | Hughes Johnson, *Scaling People* | Stripe Press | **Free to read online** (press.stripe.com/scaling-people reachable, 200); ebook editions via Kindle/Apple carry DRM | Read/ingest from the free online text if the Stripe Press store offers no DRM-free file; buy print if wanted | Kindle for reading | Page reachable |
| — | Singer, *Shape Up* (free) | Basecamp | **Free PDF, no DRM** — basecamp.com/shapeup/shape-up.pdf returned 200, 1.48 MB | — | — | **Yes** |

## Expected outcome for the corpus pipeline

- **Likely ingestible (9 + Shape Up):** Dunford, Torres, Fitzpatrick, Bland & Osterwalder, Kohavi, Ramanujam & Tacke, Patton, Lombardo, Cagan & Jones, plus Scaling People from its free online text and Shape Up from the free PDF.
- **Likely DRM-locked, read-not-ingested (4):** Rumelt, Ellis & Brown, Bryar & Carr, Grove — all trade press. Their lanes carry the free-canon distillate (Rumelt's kernel and Grove's leverage ideas are widely summarized free; Working Backwards' PR/FAQ is documented on aboutamazon.com) and the seat's model knowledge, with the "from the canon" line still able to name the framework.
- If the Wiley rows turn out DRM-locked at checkout, the same rule applies; do not buy a locked file expecting to ingest it.

## Not verified this session

ebooks.com per-title badges (API 403, page is JS-rendered); momtestbook.com (blocked curl); Cambridge Core (timed out); every price. Two subagents (Sonnet, 35- and 20-call budgets) stalled on these same domains without writing; the pattern is that retail and paywalled sites defeat automated checks from this machine. A browser session at purchase time settles every row in minutes.
