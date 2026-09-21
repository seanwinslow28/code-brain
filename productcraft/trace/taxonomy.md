# taxonomy — rung 1 of the ladder

The tracked vocabulary the labels file's `failure_code` column draws from. One file per studio ([README](README.md), *Shared home*); this is Productcraft's. Shapes of failure only — no engagement content, no private text, nothing a recruiter should not read.

**Rung 1 is not open yet.** The ladder is deterministic checks first, a taxonomy after about thirty labels, a judge only for a mode that recurs with 30–50 labels per class validated on TPR/TNR ([#272](https://github.com/seanwinslow28/code-brain/issues/272)). The substantive families — the ways a *seat* fails — are earned by reading, and the reading has not happened: pc-eng-001's 33 label rows are still open. That section below is honestly empty.

One family lands ahead of the reading, because it was earned by an investigation rather than by labels: the **process-waste** family, ratified on [#296](https://github.com/seanwinslow28/code-brain/issues/296) clause 8 and landed on [#298](https://github.com/seanwinslow28/code-brain/issues/298). It exists because a lone `manufactured` code with zero instances invites every unwelcome finding to be filed under it; the failure modes the first train actually produced are the other three.

## The codes

A `failure_code` in an engagement's `trace/labels.md` must be one of these, exactly as spelled. `check.py` enforces it — a code not in this table is free text and a finding (line 10 of rung 0). A code marked **quote required** is a finding unless the row's critique quotes the text it indicts, so the claim can be checked by someone other than its author.

| code | family | a label with this code says | quote |
|---|---|---|---|
| `manufactured` | process-waste | The finding's own named evidence does not support it — the check produced a defect rather than found one | **required** |
| `stale-restatement` | process-waste | The finding restates something already repaired, or reads a superseded state as current | — |
| `overstated-scope` | process-waste | The finding is real but describes more of the artifact than it actually reaches | — |
| `kit-induced` | process-waste | The seat did not err: a template, a checklist line or a kit rule made correct work read as a defect | — |

**`manufactured` is the serious one and the rare one.** Zero instances in pc-eng-001 across 20 material findings, both gates and two re-checks ([#296](https://github.com/seanwinslow28/code-brain/issues/296) (a)). A row carrying it is a claim that a check invented a defect, which is why it must quote the unsupported text and why it can never be a bare code. A finding you merely disagree with is not manufactured; a finding whose severity you would grade lower is not manufactured either — that is the severity grading, which held.

## Where a process-waste code goes, and where it does not

The column labels **a pass**, not a finding. A check pass whose material findings were overwhelmingly process waste is a failing pass, coded here. A pass with one waste row among sound findings is a `pass` with the waste named in the critique — the code marks what the pass *was*, not every row inside it.

Process waste is a finding against the studio, never against the seat that wrote the artifact. `kit-induced` in particular is a ticket on `productcraft/templates/` or on this kit; two of the first train's check findings were the kit's fault and closed as kit 0.2.0 ([#297](https://github.com/seanwinslow28/code-brain/issues/297)).

## Seat failure modes

Empty until the reading. Nothing goes here from an agent's own classification of its own train — the point of rung 1 is that one expert read the traces and named what he saw. When pc-eng-001's 33 labels land, the recurring critiques get grouped, counted, and written here as named modes with their codes; only then does the viewer's *Failure taxonomy* slot fill.

**The first candidate, on the record but unlabeled:** #296's unlabeled classification of pc-eng-001 counted 1 `kit-induced`, 1 `stale-restatement`, 1 `overstated-scope`, 0 `manufactured`. Those are an agent's reading of its own engagement, not labels, and they are written here as a prediction to be checked — not as the taxonomy's first row.

## Rung 2

No judge exists and none is earned. A judge arrives for one named mode, after it recurs across engagements, with 30–50 labels per class and a reported TPR/TNR against Sean's own labels. Until then the codes are read, not scored.
