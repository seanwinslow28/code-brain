# Labels file template — Sean's judgment, apart from the run's facts

The content machine's copy of the kit's second piece ([#261](https://github.com/seanwinslow28/code-brain/issues/261), [#272](https://github.com/seanwinslow28/code-brain/issues/272) decision 6; [#291](https://github.com/seanwinslow28/code-brain/issues/291)). One file per run at `pieces/<run>/trace/labels.md`, private. Rows keyed by pass id. The run's facts stay in the records, the judgment stays here, and the two are joined by the pass id alone.

**Sean labels as he reads** — each deck read, each gate ruling — plus a sweep at deck or ship close so every pass has a row. The viewer lets him enter a verdict, a first failing stage and a critique on the page; drafts live in the browser only, and **Copy label rows** puts them on the clipboard in exactly this table's column order, for pasting here. The file is the record; the page never writes it. A [#260](https://github.com/seanwinslow28/code-brain/issues/260) deck-fault ticket is the same act at deck granularity: it carries a `first_failing_stage` too.

```markdown
---
run: 2026-10-06-x-deck
labeler: Sean
---

# Labels — 2026-10-06-x-deck

| pass | verdict | first_failing_stage | critique | failure_code |
|---|---|---|---|---|
| pass-05 | pass | | Agrees with the post and the second line is the one only he would write. | |
| pass-06 | fail | 3 | Two of three sentences restate the post; the one that is his is the second. Lead with it. | |
| pass-08 | pass | | | |
| pass-15 | | | | |
```

## The columns

- **`verdict`** — `pass` or `fail`, nothing between. "The other picks can use a little work" is a fail with a critique. An empty cell is a row still waiting; the checker counts it and the viewer's counter shows it.
- **`first_failing_stage`** — set on every fail: the stage, **0–6 in the machine's numbering**, where the problem *entered* the run, which may be upstream of the pass being read. A dunk the shaper produced by imitating a withdrawn sample broke at 3; a card the Oracle should never have decked broke at 0; a lifted run the origin gate missed broke at 4. This single column builds the transition matrix (last good stage × first failing stage), so it is never blank on a fail and never set on a pass.
- **`critique`** — one to three sentences a new hire could act on. Escape a pipe as `\|`; keep it on one line. Optional on a pass, expected on a fail. **Never his words** — the run folder is private, but the critique is the one field most likely to be pasted into a ticket.
- **`failure_code`** — blank while rung 1 is unopened, which is the state today ([taxonomy.md](taxonomy.md)). When a code exists it must be one in that file, never free text: the checker's tenth line fails on a code outside it.

## Rules the checker enforces

The header must read exactly `| pass | verdict | first_failing_stage | critique | failure_code |`. A pass id appears once. A verdict outside `pass` / `fail` / empty is an error. A fail without its first failing stage is an error; a stage outside 0–6 is an error. A row for a pass that has no record is a finding on "Every pass has a record".
