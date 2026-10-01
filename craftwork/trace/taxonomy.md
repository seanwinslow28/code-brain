# taxonomy — the shared families of rung 1

The tracked vocabulary every studio's labels file draws on before it has codes of its own. Shapes of failure only — no engagement content, no private text, nothing a recruiter should not read.

**Two files make a studio's vocabulary** (kit 0.9.0, [#325](https://github.com/seanwinslow28/code-brain/issues/325)). This file holds the families every studio shares. Each studio's own file holds the failure modes its own labels earned, and its profile names it. Productcraft's is [productcraft/trace/taxonomy.md](../../productcraft/trace/taxonomy.md). `check.py` reads both, this one first, so a studio row that repeats a code here wins. A profile with `shared_taxonomy=False` reads its own file alone. The content machine's profile does that, because its taxonomy has not adopted this family.

**Why a shared family exists at all.** The ladder is deterministic checks first, a taxonomy after about thirty labels, and a judge only for a mode that recurs with 30–50 labels per class, validated on TPR/TNR ([#272](https://github.com/seanwinslow28/code-brain/issues/272)). Seat failure modes come from one studio's labels, so they live with the studio. The **process-waste** family is different. An investigation of the studio's own checks earned it, not any one studio's labels: ratified on [#296](https://github.com/seanwinslow28/code-brain/issues/296) clause 8, landed on [#298](https://github.com/seanwinslow28/code-brain/issues/298), moved here from Productcraft's file on #325. It names how *checking* goes wrong, which is the same question in every studio that runs an adversarial check. It exists because a lone `manufactured` code with zero instances invites every unwelcome finding to be filed under it.

## The codes

A `failure_code` in an engagement's `trace/labels.md` must be one of these or one of the studio's own modes, exactly as spelled. `check.py` reads every code table in both files and enforces it: a code in neither is free text and a finding (line 10 of rung 0). A code marked **quote required** is a finding unless the row's critique quotes the text it indicts, so someone other than its author can check the claim.

| code | family | a label with this code says | quote |
|---|---|---|---|
| `manufactured` | process-waste | The finding's own named evidence does not support it — the check produced a defect rather than found one | **required** |
| `stale-restatement` | process-waste | The finding restates something already repaired, or reads a superseded state as current | — |
| `overstated-scope` | process-waste | The finding is real but describes more of the artifact than it actually reaches | — |
| `kit-induced` | process-waste | The seat did not err: a template, a checklist line or a kit rule made correct work read as a defect | — |

**`manufactured` is the serious one and the rare one.** Productcraft's first engagement had zero instances across 20 material findings, both gates and two re-checks ([#296](https://github.com/seanwinslow28/code-brain/issues/296) (a)). A row carrying it is a claim that a check invented a defect, which is why it must quote the unsupported text and why it can never be a bare code. A finding you merely disagree with is not manufactured. A finding whose severity you would grade lower is not manufactured either; that is the severity grading's business.

## Where a process-waste code goes, and where it does not

The column labels **a pass**, not a finding. A check pass whose material findings were overwhelmingly process waste is a failing pass, coded here. A pass with one waste row among sound findings is a `pass` with the waste named in the critique. The code marks what the pass *was*, not every row inside it.

Process waste is a finding against the studio, never against the seat that wrote the artifact. `kit-induced` in particular is a ticket on the studio's templates or on this kit. Two of Productcraft's first-train check findings were the kit's fault and closed as kit 0.2.0 ([#297](https://github.com/seanwinslow28/code-brain/issues/297)).

## Rung 2

No judge exists in this kit. A judge arrives for one named mode in one studio, after it recurs across that studio's engagements, with 30–50 labels per class and a reported TPR/TNR against Sean's own labels. It lands beside that studio's taxonomy, not here.
