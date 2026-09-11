# Product

<!-- impeccable:product-schema 1 -->

Scope: the eval viewer that `productcraft/trace/` renders, one self-contained HTML file per engagement. This record covers that family of pages only, not the studio. Facts marked *(inferred)* were taken from the #292 brief and the #272 resolution rather than confirmed in an interview; the two labeling and page-shape facts were confirmed by Sean on 2026-09-11.

## Platform

web

## Stack

Static HTML, CSS and vanilla JS emitted by a Python renderer (#290). No framework, no build step for the page itself, no network at open time. *(inferred from #272 decision 3 and #290)*

## Users

One reader: Sean, the studio owner, a product manager and not a developer. He opens the file after a train has run, or during it, on a laptop, to read every pass, decide pass or fail with a critique, and see where the run went wrong. He may reopen it weeks later to add process notes or to compare engagements. Nobody else reads it; the ledger is private.

## Product Purpose

Remove the friction from looking at the run. The page is the studio's version of the custom annotation tool Husain calls the single most impactful eval investment: all context for a pass on one screen, one-click verdicts, a written critique, a counter, keyboard navigation. Success is a labeled engagement (every pass has a verdict row) and a reader who can point at the stage where the run broke without opening a single record file.

## Positioning

A purpose-built viewer over the studio's own immutable markdown records and labels file. It is not a span waterfall: passes, stages, verdicts and moves are the units, and the first-failing-stage matrix is the centrepiece. It stays local and self-contained by law; hosted trace tools would ship payloads.

## Operating Context

- Inputs on disk per engagement: `pass-NN-<seat>-<kind>.md` records (#272 decision 2), a labels file keyed by pass id (decision 6), the seats' artifacts with their `## Moves` sections (decision 4), and later a `notes.md` of Sean's process notes.
- Close ritual: run the rung-0 checker, render the viewer, confirm every pass is labeled (decision 8).
- Labels are written as Sean reads, during the train, plus a Close sweep. **Confirmed 2026-09-11:** the page lets him enter verdict, first failing stage and critique in the row, holds drafts in the browser, and exports rows for the labels file. The labels file remains the record; the page never writes it.
- **Confirmed 2026-09-11:** one scrolling document, not a two-pane console.
- Shadow passes (trials) are labeled blind: the runtime column hides until both the baseline and the trial carry a verdict (decision 9).
- Stage numbering is fixed by the train: 1 Strategist, 2 Discovery, 3 Insights, 4 Growth, 5 Business, 6 Delivery, 7 Leadership; gates and audits sit at the stage of their anchor artifact. *(inferred from #266)*

## Capabilities and Constraints

- Self-contained: fonts, styles, data and script inside one file; opens from disk offline; readable at laptop width; printable; light and dark both rendered.
- Reads by domain: stages, verdicts, matrix, counts, critiques on the surface; paths, hashes and raw-log pointers folded one click away.
- Charts: counts, never percentages, below ten. A chart earns its place only when a count list would fail.
- No motion (the portfolio's motion section does not transfer). Only state changes.
- Growth slots named in advance: judge results (rung 2), failure taxonomy (rung 1), process notes.
- Out of scope: hosting, the renderer's implementation (#290), any write to the ledger.

## Brand Commitments

The portfolio's visual world, verbatim: "Dailies desk" light and "Night studio" dark palettes (ground, ink, sub, drafting-ink accent), the "Squared character" type pair (Anybody display, Schibsted Grotesk body). The accent's mark grammar is exhaustive and gains no new uses. Source: `/Users/seanwinslow/Code-Brain/seanwinslow.com/DESIGN.md` §2, §2.1, §4, §9.

## Evidence on Hand

- Husain primary-source read: `vault/20_projects/research/2026-09-11-husain-evals-method-for-seat-pipelines.md`
- Viewer prior art, tier-audited: `vault/20_projects/research/2026-09-11-eval-viewer-design-prior-art.md`
- Torres × Husain note: `vault/20_projects/research/2026-09-09-torres-husain-evals-in-discovery-findings.md`
- Record and label schemas: #272 resolution comment.
- No real engagement data exists yet; every sample is synthetic and says so on the page.

## Product Principles

1. Legibility over completeness: the surface shows what a verdict needs; everything else folds.
2. Every verdict shows its why beside it: the critique, the failing stage, the check.
3. Counts, not percentages, until there are ten of a thing.
4. The record is the truth; the page is a view and says so.
5. Blind where bias could enter: runtime identity hides until both labels land.

## Accessibility & Inclusion

Keyboard-complete labeling loop; visible focus marks; verdicts never carried by color alone; body contrast at or above 4.5:1 on both grounds; print stylesheet that expands folded detail.
