# Lane manifests

One file per lane, seven lanes, one seat each. A lane manifest is the first thing its
seat reads on every invocation, and it is two documents in one file.

The upper half is **shelf labels** for the seat: a title, a pointer into the private
corpus, and a one-line note saying when the pointer is worth following. Never the books
themselves — the content lives in `../corpus/`, which is gitignored, so on a machine
without it the pointers do not resolve and the seat declares `manifest-only` grounding
instead of pretending otherwise. The lower half, from `## Reading path` down, is Sean's:
an ordered table of what to read and in what situation, plus a `### Next` shelf of titles
the lane holds in reserve. Seats stop at that heading; the reading path is the owner's.

Two rules keep the halves from drifting. A book's format, audio and corpus facts are
stated on exactly one lane — its primary — and any other lane that needs its chapters
carries a pointer row instead. And listen-only titles appear only in a reading path,
never as a shelf label, so no seat can name a book it cannot read. Schema ratified on
[the lane manifest schema ticket](https://github.com/seanwinslow28/code-brain/issues/270),
2026-09-11. Toolbelts live in the seat file, not here.

## Studio reading order

Before any lane: **Cagan, *INSPIRED* (2nd ed.)** — the reference map of the whole craft,
and the studio's first listen. It is listen-only; no seat reads it.

Then the lanes, in pipeline order — the order the seats run in an engagement, and the
order to read them in:

| # | Lane | Seat | Manifest |
|---|---|---|---|
| 1 | Strategy | [Product Strategist](../bench/product-strategist.md) | [strategy.md](strategy.md) |
| 2 | Discovery | [Discovery Lead](../bench/discovery-lead.md) | [discovery.md](discovery.md) |
| 3 | Insights | [Insights & Analytics](../bench/insights-analytics.md) | [insights.md](insights.md) |
| 4 | Growth | [Growth & Distribution](../bench/growth-distribution.md) | [growth.md](growth.md) |
| 5 | Business | [Business & Economics](../bench/business-economics.md) | [business.md](business.md) |
| 6 | Delivery | [Delivery & Execution](../bench/delivery-execution.md) | [delivery.md](delivery.md) |
| 7 | Leadership | [Product Leadership](../bench/product-leadership.md) | [leadership.md](leadership.md) |

Pipeline order lives in the seat number, never the filename, so reordering the train
never renames a manifest. See [../CLAUDE.md](../CLAUDE.md).
