# DESIGN.md — the eval viewer

**Status:** APPROVED 2026-09-11 (Sean ratified all five §13 choices on #292 after reacting to the sample render). This is the renderer's design authority. Two facts were confirmed the same day before the write: labels are entered on the page and exported, and the page is one scrolling document.
**Scope:** every HTML file the trace kit's renderer (#290) emits — one per engagement, into that engagement's folder in the private ledger. The renderer follows this document; if the two disagree, this document is the intent and the renderer is the bug.
**Sample to react to:** [`samples/pc-eng-000-callboard/eval.html`](samples/pc-eng-000-callboard/eval.html), rendered from an invented engagement by [`samples/render_sample.py`](samples/render_sample.py). Product truth for this family of pages: [`PRODUCT.md`](PRODUCT.md).
**Provenance:** the #272 resolution (record, labels, ladder, blind trials); Husain's viewer rules (`vault/20_projects/research/2026-09-11-husain-evals-method-for-seat-pipelines.md` §2, §5); the tier-audited viewer prior art (`vault/20_projects/research/2026-09-11-eval-viewer-design-prior-art.md`, twelve recurring principles); the portfolio's design authority (`/Users/seanwinslow/Code-Brain/seanwinslow.com/DESIGN.md` §2, §2.1, §4, §9).

---

## 1 · What this page is

One reader, one file. Sean opens it after a train has run, or while it runs, and does three things: sees where the run broke, walks every pass with its context on one screen, and labels as he reads. The page is the studio's version of Husain's custom annotation tool. It is an **Operate** surface with a **Read** spine: a desk sheet, not a dashboard and not a span waterfall.

The units are the studio's own: **passes** (one per invocation), **stages** (the fixed train numbering 1–7, plus close), **verdicts** (pass | fail, nothing between), the **first failing stage**, **critiques**, **moves**, **checks**. Spans, tool calls and tokens-per-second are not units here; a raw log is one pointer away and stays there.

Three rules govern everything below:

1. **Legibility over completeness.** The surface shows what a verdict needs. Paths, hashes, launch forms and log pointers exist, one click down, never on the surface.
2. **The why sits beside the verdict.** No verdict appears without its critique, its failing stage, or the check that failed. A label a new hire cannot act on is not a label.
3. **The records are the truth; the page is a view.** The footer says so on every render. The page never writes the ledger.

## 2 · Inherited from the portfolio, verbatim

The viewer wears the portfolio's world. Nothing here is a new identity.

| Token | "Dailies desk" light | "Night studio" dark |
|---|---|---|
| `--ground` | cream `#FBF6EC` | warm charcoal `#191714` |
| `--ink` | graphite `#2A2622` | cream `#F2EBDD` |
| `--sub` | `#6E655B` | `#8F867A` |
| `--accent` | drafting ink `#2F5D7C` | lifted ink `#6BA3C9` |

Derived, never hand-picked: `--ink-hairline` (ink at 14%), and four **ink washes** at 6 / 16 / 30 / 48% (`--ink-wash-1..4`). No pure black or white anywhere; every neutral carries hue.

**What transfers:** the palette (§2), the accent's exhaustive mark grammar (§2.1), the type pair (§4), the keyboard-focus mark (§9), system preference as the default with a toggle that overrides in both directions.

**What does not transfer:** §5 motion, entirely. No intro, no loader, no hover clips, no draw-ins that animate over time, no tick that fades. The only "motion" is a state change that happens at once. Also not transferred: the proportional `vw` root (a layout trick for a full-viewport hero; this page uses a fixed 16px root, per Operate practice), the media system, the character placements, the hero-and-statement stack.

**Fonts travel with the file.** The page opens from disk, offline, on any machine, so the two Latin subsets are embedded as base64 `@font-face` data (`fonts/anybody-latin-wdth-normal.woff2`, 57 KB; `fonts/schibsted-grotesk-latin-wght-normal.woff2`, 47 KB; both OFL-1.1, licenses alongside). The fallback stack is `system-ui, sans-serif` and the page must read correctly in it: no layout depends on a glyph width.

## 3 · Color: ink carries magnitude, glyphs carry verdicts

The portfolio's rule is that the accent appears only in interaction marks, and this page adds **no new accent uses**. So neither the verdict nor the matrix may use hue. Two consequences, both deliberate:

- **Magnitude is ink.** The matrix and the stage strip use the ink washes as a single sequential ramp: nothing → wash-2 → wash-3. Darker means more. A count of three or more also gets a 1px ink ring and bold; there is no fourth step, because with counts below ten there is nothing a fourth step would say.
- **Verdicts are glyph + word + weight, never color.** Pass is a drawn check and the word "pass" in ink at 600. Fail is a drawn cross and the word "fail" in ink at 600, and the row's critique is set in ink where a pass row's is set in sub. Unlabeled is a dashed hollow circle and the word "unlabeled" in sub at 400. On the train, a labeled fail carries an ink ring around its mark. Print and forced-colors get the same page for free.

**Where the accent appears on this page, exhaustively:** the keyboard-focus mark (a 2px underline under the focused control), the current-row settled mark (a 2px underline inside the row the keyboard is on), the link hover draw-in (an underline that appears; it does not animate), and the text-selection tint. Nowhere else: not on buttons, not on the matrix, not on the verdict, not on the track. A selected verdict button is ink on ground inverted, not accent.

**Status colors are not introduced.** If a future reader needs red for fail, that is a ratified change to this section, not a per-render choice. The ink-only encoding is one of the choices put to Sean on #292.

Contrast, measured for the ratification record: ink on ground 13.9:1 light / 15.1:1 dark; sub on ground 5.3:1 / 5.0:1; ink on wash-3 7.6:1 / 6.1:1; sub on wash-1 4.8:1 / 4.3:1, which is why an opened row's sub text switches to ink.

## 4 · Type

- **Display:** Anybody, weight 900, width 95, uppercase, letter-spacing −0.01em, line-height 1. Used for the engagement title (`--fs-5`, 2.375rem) and the four section headings (`--fs-4`, 1.625rem). Nowhere else. Never in a row, a label, a button or a number.
- **Body:** Schibsted Grotesk for everything else, 400 for text, 600 for the pass id and the verdict word, 700 for a matrix count of three or more. Sub-headings inside a folded row are Schibsted 600 uppercase at `--fs-0` with 0.06em tracking, in sub.
- **Scale, fixed rem:** `--fs-0` 0.8125rem (row text, meta, captions), `--fs-1` 0.9375rem (body, critiques), `--fs-2` 1.0625rem (row-section titles), `--fs-3` 1.25rem (the reading line), `--fs-4`, `--fs-5`. Six sizes, no fluid type.
- **Tabular figures only where figures align:** the matrix, the stage counts, the counter, the meta line, the wall-clock and token cells, the pass id, record values, the train's SVG text. Never on body text: Schibsted's `tnum` also widens its comma, period and colon, and the first render put a space before every comma on the page.
- **Measure:** prose ≤ 68ch; the reading line ≤ 60ch; rows may run the full 1180px content width.

## 5 · Anatomy, in fixed order

Every render has these parts, in this order, under these headings. Nothing else appears between them.

1. **Masthead.** `pc-eng-NNN · Name` in display type, a `SYNTHETIC` badge when the data is invented (the badge is absent on a real engagement, never "REAL"). One meta line in sub: kind · opened · closed · passes of budget · rendered from N records, M label rows. On the right, three buttons: **Copy label rows** (with the draft count), **Keys ?**, and the **Night / Day** toggle. A 1px ink rule closes the masthead.
2. **The reading line.** One paragraph at `--fs-3`, plain prose with the counts in bold: how many passes, how many labeled, pass and fail counts, how many wait for a verdict, where the train broke first and which break cost downstream work, the rung-0 clean count. It is a sentence, not a KPI row: the renderer composes it from the data with a fixed sentence template, and it must still read when every count is zero.
3. **The counter.** `Labeled N of M`, a thin ink track (drafted-here labels shade it lighter), and `Next unlabeled: pass-NN` as a link.
4. **Where it broke.** Two columns at laptop width, one on narrow screens. Left: the **transition-failure matrix** and the **passes-per-stage** strip. Right: **the N fails, first failure named**, then **rung 0 checks**. Details in §6 and §7.
5. **The train.** Every pass in order, on its stage column, as an SVG: pass id and seat down the left, the seven stages plus close across the top, a faint lane joining consecutive passes, a mark per pass (filled square draft, washed square repair, hollow circle audit, hollow diamond co-sign, hollow triangle gate, dashed square trial, small dot close), an ink ring on a labeled fail, a curved arrow back to the pass that triggered a repair or re-gate, and a dashed tie from a trial to its baseline. A legend follows in sub. The train is order, not time; wall-clock lives in the rows.
6. **Passes.** A filter row (all · fails · unlabeled · shadow pairs, as toggle buttons with counts, plus a one-line column key and the two navigation keys), then one folded row per pass. Details in §8.
7. **What comes later.** Three growth slots, always rendered, each teaching what will fill it and when. Details in §10.
8. **Footer.** "Rendered <date> from N records and M label rows. The records are the truth; this page is a view of them." and the kit's name and version.

**Visible at the top** without scrolling at 1280×900: masthead, reading line, counter, the matrix and the first two fails. **Visible per row**: pass id, seat with its loop or shadow tag, kind, stage, runtime, wall-clock, tokens in+out, verdict, critique (one line, clipped). **Folded** (one click, or Enter): the record's launch instant, launch form, effort, meter with its source, raw log pointer, inputs with hashes, withheld, outputs, checks on this pass, corpus read, moves, notes, and the label form.

## 6 · Explainability

- **The fails list** is the page's argument. Each entry: the pass id as a jump link, seat and kind, `broke at <stage n> <stage name>`, the full critique in `--fs-1`, and one of two sub-lines: *upstream of the pass read* or *at the pass read*. A fail whose first failing stage is earlier than the pass's own stage is the most valuable line on the page; it says the fix is somewhere else.
- **Checks on this pass** is the inverse view: for a draft, every audit, co-sign and gate that touched it, with its verdict, so a reader sees a draft's whole trial without leaving the row.
- **Moves** appear as five counts in one line (`13 kept · 5 added · 1 split · 1 merged · 2 dropped`) followed by the non-kept lines only, each `op · what · from <sources>`. Kept items are never listed; the artifact's own `## Moves` section holds them. A split shows both children and its sources. An origin draft says "origin draft, no upstream" and lists what it leaned on. A kind that hands no artifact forward says so.
- **Corpus read** is labeled "from the transcript" so the reader knows it is a fact recovered from file reads, not the seat's claim.
- **The rung-0 list** shows every deterministic check with a drawn check or cross and its count (`21 of 24`), two columns, no percentages.

## 7 · Charts: which earn a place

Three do. Everything else is a number in a row.

| Chart | Job | Form | Color |
|---|---|---|---|
| **Transition-failure matrix** | locate the break | HTML table; rows = last good stage (start, 1–6), columns = first failing stage (1–7); cells are counts; impossible cells (column ≤ row in a linear train) hatched; empty cells show a dot | ink-wash ramp, three steps |
| **Passes per stage** | see the shape of the train and where labels are missing | one line per stage: a strip of 14px squares (wash-3 pass, ink fail, dashed outline unlabeled) and the counts in words | ink |
| **The train** | see order, loops and pairs | SVG, described in §5.5 | ink |

**Rules that bind all three.** Counts, never percentages, below ten of anything; the matrix caption says so when it applies ("4 fails so far, which is too few for a heat: read the numbers"). One hue, ink, light-to-dark. Recessive grid: hairlines only, no dashes. Every chart has a text equivalent on the page (the matrix is a table; the strip prints its counts; the train lists pass and seat). Hover tooltips are not required, because every value is already printed.

**Charts that do not earn a place, and why:** tokens or wall-clock per pass as bars (a column of numbers in the rows says it; a bar would make the reader compare passes of different kinds); token totals as a hero figure (the meter line is a subtotal plus an unmeasured count, never a precise figure); anything as a percentage before ten; a pie or donut of pass/fail; sparklines; a per-seat leaderboard (the registry, not this page); a duration timeline (the train is order, and wall-clock is in the row). The shadow-pass comparison is not a chart either: it is the pair filter plus two rows.

**Matrix derivation.** In the studio's linear train, last good stage = first failing stage − 1, so the matrix is derived from the label file alone. The renderer must not invent a `last_good` field; if the train ever branches, that is a schema change on #272's labels file first.

## 8 · The rows and labeling in place

**Row summary columns** (fixed widths, in order): pass id · seat with tags · kind · stage · runtime · wall-clock · tokens in+out · verdict · critique. Tags are small hairline-bordered chips after the seat name: a loop glyph and the triggering pass id for a repair or re-gate; `shadow of pass-NN` on a trial; `baseline of pass-NN` on its baseline. Under 900px the runtime, wall-clock, token and critique cells hide; the verdict never does.

**Labeling** (confirmed by Sean, 2026-09-11): the folded row ends with a label form: two toggle buttons **pass** `1` / **fail** `2`, a **first failing stage** select `f` (enabled only on fail), a **critique** textarea `c` with the caption "one to three sentences a new hire could act on", and a state line. Labels drafted on the page live in the browser only (`localStorage`, keyed by engagement id) and never touch the ledger. **Copy label rows** puts every drafted row on the clipboard as a markdown table in the labels file's column order (`pass | verdict | first_failing_stage | critique | failure_code`), critique pipes escaped, for Sean to paste. `failure_code` is always blank until a taxonomy exists, and the state line says so.

**Three label states, always visible in the state line:** *No label row yet.* · *Drafted here, not yet in the labels file.* · *In the labels file.* The counter distinguishes them: `Labeled 21 of 24 in the file, 2 drafted here`. A draft can be revised or cleared (pressing the selected verdict again clears it) because criteria drift as a reader reads; the file is the commit.

**The blind rule** (#272 decision 9). A shadow pair is a trial and its baseline. Until both carry a verdict, the runtime and launch form of both rows read *hidden* with an eye-off glyph, and the row carries the note "Blind pair with pass-NN: the runtime and launch form stay hidden until both passes carry a verdict." **The renderer must not embed a hidden runtime anywhere in the HTML**, not in a data attribute, not in a script constant; view-source would break the blind. The reveal therefore happens on the next render, after both labels are in the file. A drafted verdict on the page does not reveal; the sample's "revealed on commit" placeholder stands for exactly that re-render.

**Filters** are one row above the rows, never inside a chart, and never repaint anything: a filtered row hides, nothing else changes.

## 9 · Keyboard

The labeling loop must complete without a pointer. Keys are single letters, shown in the `?` sheet and in the filter row's key hint.

| Key | Does |
|---|---|
| `j` `k` (or ↓ ↑) | next / previous pass; the current row carries the accent underline mark |
| `enter` | open or fold the current pass |
| `1` `2` | label the current pass pass / fail |
| `f` | open the row and focus first failing stage |
| `c` | open the row and focus the critique |
| `u` | jump to the next unlabeled pass |
| `esc` | leave a field, focus returns to the row |
| `?` | the key sheet (a `<dialog>`) |

Keys are ignored while a field has focus, and with any modifier held.

## 10 · Growth slots

Rendered on every page, empty or not, under "What comes later", so the layout never changes when they fill:

- **Failure taxonomy** — after about thirty labels. Empty state names the threshold. When it fills: one line per failure mode with its count; each row's `failure_code` becomes a link to its mode.
- **Judge results** — per failure mode, after thirty to fifty labeled examples per class and validation on a held-out split. Empty state names the floor. When it fills: a second verdict column in each row, marked *judge*, beside the human one; never in place of it; the matrix stays human-labeled.
- **Process notes** — Sean's own notes for the engagement, read from the engagement's notes file when it exists, rendered as pre-wrapped prose at `--fs-1`. Empty state: "No notes file yet."

## 11 · States

Every state below has a designed rendering; none is an error message.

- **Unlabeled row** — dashed hollow circle, "unlabeled" in sub; the critique cell shows nothing, or `broke at n` if a first failing stage exists.
- **Drafted here** — the state line in ink, the counter's draft note, the track's lighter segment, the Copy button's count.
- **Blind pair** — §8.
- **Bounce loop** — the loop chip on the row and the curved arrow on the train.
- **Unmeasured meter** — the token cell shows an em dash and the meter line reads `UNMEASURED`, never zero.
- **No moves** — the row says which of the three reasons applies (origin draft · kind hands nothing forward · not recorded).
- **Filtered to nothing** — the rows section shows "No passes match" in sub; the counter does not change.
- **Zero fails** — the fails list reads "No fails labeled yet" and the matrix renders empty with its caption; the reading line still parses.
- **Dark** — the same page in the night tokens; drawn glyphs and washes follow the ink token, so nothing is re-specified. Never invert; never define a color only inside a media query.
- **Print** — folded rows open (`beforeprint`), the tools, filters and forms hide, rows and charts refuse to break across pages, colors print exactly, the light tokens always print. The page must survive as a stack of paper.
- **Narrow** — two-column sections fall to one; the row summary drops to id · seat · kind · verdict. The page is designed for a laptop; a phone is tolerated, not designed for.

## 12 · Self-contained, local, honest

- One file, no network. No `<link>`, no `<script src>`, no image URLs, no font URLs. Fonts and icons are inline. A renderer that needs a CDN has failed this document.
- Every string from a record, label or artifact is HTML-escaped before it lands in the page. Nothing from a seat is rendered as markup.
- Icons are authored SVG symbols in one stroke weight (check, cross, hollow circle, eye-off, loop, arrowhead). No emoji, no icon font, no Unicode dingbats.
- Size: the empty page is roughly 150 KB (fonts) plus data. An engagement of thirty passes renders under 400 KB. If a render passes 1 MB, something is being embedded that belongs one pointer away.
- The page says what it was rendered from and when, and that the records are the truth.

## 13 · Ratified choices (Sean, 2026-09-11, #292)

1. Ink-only verdicts (no red for fail) — §3.
2. The reading line as prose rather than a KPI row — §5.2.
3. The train as order rather than time — §5.5, §7.
4. Reveal-on-re-render for blind pairs, never on the page — §8.
5. The fixed 16px root instead of the portfolio's proportional root — §2.
