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

- **`verdict`** — `pass` or `fail`, nothing between; or `defer` (since kit 0.7.0, DESIGN.md §15), a recorded "come back to this" that is not a verdict: the row still waits, never reveals a blind pair, and is never counted as labeled. "Mostly fine" fails. An empty cell is a row that still waits for a verdict; the checker counts it as unlabeled and the viewer's counter shows it.
- **`first_failing_stage`** — set on every fail: the stage (1–7) where the problem *entered* the train, which may be upstream of the pass being read. This single column builds the transition-failure matrix (last good stage = first failing stage − 1 in a linear train), so it is never left blank on a fail and never set on a pass.
- **`critique`** — one to three sentences a new hire could act on. Escape a pipe as `\|`; keep it on one line. Optional on a pass, expected on a fail.
- **`failure_code`** — blank while rung 1 is unopened, which is the normal state. A code must be one in [taxonomy.md](taxonomy.md), never free text: `check.py`'s tenth line fails on a code outside it. Two families exist: **process-waste** (`manufactured`, `stale-restatement`, `overstated-scope`, `kit-induced`) and the **seat failure modes** opened from the first engagement's labels (`unobservable-measure`, `overclaimed-pointer`, #299). The column codes what a pass *was* — a fail whose lead shape is not yet a mode stays blank, and the shape is noted in the taxonomy's sighted list instead. `manufactured` is a finding unless the critique quotes the text it indicts, so the claim is checkable by someone other than its author.

## Rules the checker enforces

The header must read exactly `| pass | verdict | first_failing_stage | critique | failure_code |`. A pass id appears once. A verdict outside `pass` / `fail` / empty is an error. A fail without its first failing stage is an error. A row for a pass that has no record is a finding on "Every pass has a record". Blind pairs (a trial and its baseline) are labeled like any other row — the viewer hides their runtime until both rows carry a verdict, and reveals it on the next render, never on the page.
