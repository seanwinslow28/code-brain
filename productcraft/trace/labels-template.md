# Labels file template — Sean's judgment, apart from the run's facts

The second piece of the trace kit ([#272](https://github.com/seanwinslow28/code-brain/issues/272) decision 6; [#290](https://github.com/seanwinslow28/code-brain/issues/290)). One file per engagement at `ledger/engagements/<eng-id>/trace/labels.md`, private. Rows keyed by pass id. Husain's spreadsheet floor: the run's facts stay in the records, the judgment stays here, and the two are joined by the pass id alone.

**Sean labels as he reads**, during the train (he reads every artifact before ratifying), plus a mandatory Close sweep so every pass has a row. The viewer lets him enter a verdict, a first failing stage and a critique on the page; drafts live in the browser only, and **Copy label rows** puts them on the clipboard in exactly this table's column order, for pasting here. The file is the record; the page never writes it.

```markdown
---
engagement: pc-eng-001-16bitfit-revisit
labeler: Sean
---

# Labels — pc-eng-001

| pass | verdict | first_failing_stage | critique | failure_code |
|---|---|---|---|---|
| pass-01 | pass | | Diagnosis is one sentence and names the constraint. A new hire could restate it. | |
| pass-02 | fail | 1 | Right to fail it, but the write-up buries the load-bearing finding under two notes; lead with it. | |
| pass-03 | | | | |
```

## The columns

- **`verdict`** — `pass` or `fail`, nothing between. "Mostly fine" fails. An empty cell is a row that still waits for a verdict; the checker counts it as unlabeled and the viewer's counter shows it.
- **`first_failing_stage`** — set on every fail: the stage (1–7) where the problem *entered* the train, which may be upstream of the pass being read. This single column builds the transition-failure matrix (last good stage = first failing stage − 1 in a linear train), so it is never left blank on a fail and never set on a pass.
- **`critique`** — one to three sentences a new hire could act on. Escape a pipe as `\|`; keep it on one line. Optional on a pass, expected on a fail.
- **`failure_code`** — blank until the failure taxonomy exists (rung 1, after ~30 labels). Then a code from the studio's tracked taxonomy file, never free text.

## Rules the checker enforces

The header must read exactly `| pass | verdict | first_failing_stage | critique | failure_code |`. A pass id appears once. A verdict outside `pass` / `fail` / empty is an error. A fail without its first failing stage is an error. A row for a pass that has no record is a finding on "Every pass has a record". Blind pairs (a trial and its baseline) are labeled like any other row — the viewer hides their runtime until both rows carry a verdict, and reveals it on the next render, never on the page.
