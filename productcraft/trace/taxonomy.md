# taxonomy — rung 1 of the ladder, Productcraft

The tracked vocabulary the labels file's `failure_code` column draws from. This is Productcraft's file: the seat failure modes its own labels earned. The families every studio shares, today the **process-waste** family, live in the shared kit's [craftwork/trace/taxonomy.md](../../craftwork/trace/taxonomy.md), and `check.py` reads both ([studio.py](studio.py) names this file). Shapes of failure only — no engagement content, no private text, nothing a recruiter should not read.

**Rung 1 is open, on a thin base.** The ladder is deterministic checks first, a taxonomy after about thirty labels, a judge only for a mode that recurs with 30–50 labels per class validated on TPR/TNR ([#272](https://github.com/seanwinslow28/code-brain/issues/272)). The reading happened on 2026-09-21: pc-eng-001's 33 label rows carry verdicts, and the two seat failure modes below were grouped and counted from their critiques ([#299](https://github.com/seanwinslow28/code-brain/issues/299)). Thirty-three labels is the floor for *starting* a taxonomy, not for trusting one, and five fails is a thin base for "recurring" — so two shapes are codes, two more are sighted and kept off the table until a second engagement's labels say whether they recur.

The process-waste family landed ahead of the reading, because it was earned by an investigation rather than by labels ([#296](https://github.com/seanwinslow28/code-brain/issues/296) clause 8, landed on [#298](https://github.com/seanwinslow28/code-brain/issues/298)). It sat in this file until the kit moved to `craftwork/` on [#325](https://github.com/seanwinslow28/code-brain/issues/325). It is shared now, so its four codes, its quote rule for `manufactured` and its placement rule are in the shared file, not here.

## The codes

A `failure_code` in an engagement's `trace/labels.md` must be a seat failure mode below or a code in the [shared file](../../craftwork/trace/taxonomy.md), exactly as spelled. `check.py` reads every code table in both and enforces it: a code in neither is free text and a finding (line 10 of rung 0).

## Seat failure modes

**Opened 2026-09-21 from pc-eng-001's 33 labels — proposed by the coordinator, ratified by Sean.** The rule of this section is that modes come from one expert's reading, so the provenance travels with every count: the 33 verdicts were coordinator-drafted at Sean's request and Sean-approved (the labels file's own provenance block says so, and its critiques are worded by the coordinator, not by him), and the mode names below were proposed by that same coordinator from those critiques on [#299](https://github.com/seanwinslow28/code-brain/issues/299). A code here is a mode only once the line below carries his date.

Ratified: **Sean, 2026-09-21**, both names as proposed; pass-19's code kept as `unobservable-measure` on his ruling (its two standing-rule contradictions stay in the sighted list).

### The codes

| code | family | a label with this code says | quote |
|---|---|---|---|
| `unobservable-measure` | seat | The artifact defines a measure, kill condition, trigger or safeguard on an event the pilot's own rules cannot produce or deliver — no channel, no record field, no authorised contact or app open | — |
| `overclaimed-pointer` | seat | A citation or status claim says more than its source holds — a clause not in the cited file, an evidence rung above what the pointer supports, a ledger state the entry does not carry | — |

### The counts, pc-eng-001

Two numbers per mode, because they answer different questions. **Coded fails** is how many fail rows carry the code in `labels.md` — the column labels a pass, so this is the number rung 0 checks. **Distinct defects** is how many separate defects of that shape the critiques name across all 33 rows, including blemishes on passing rows and the check findings that caught them — the number that says whether a mode recurs. A defect is counted once however many rows mention it (a draft, its audit and its repair are three rows, one defect).

| mode | coded fails | distinct defects | drafting seats it appeared in |
|---|---|---|---|
| `unobservable-measure` | **3** — pass-01, pass-13, pass-19 | **8** — an outcome left open to a prompt channel and a bet with no liveness condition (pass-01); a kill condition naming a blinded reader the pilot does not have (pass-03); a classifier resting on an end-of-pilot reconciliation no contact rule authorised (pass-07 / pass-10, M8); a harm pause with no route to a phone before day 14 (pass-13 / pass-15, F1); a pre-registered metric on a record field that does not exist (pass-19 / pass-20); a key result whose zero-counts cannot see the failure it guards, and one that dropped the total that makes it readable (pass-25 / pass-26) | 4 of 7 — Strategist, Insights, Growth, Delivery |
| `overclaimed-pointer` | **1** — pass-28 | **8** — five evidence rows bounced at co-sign, a clause in none of the frozen files, a clause contradicted by the file it cites, three rungs above their evidence (pass-02 / pass-05); a pointer into an overwritten revision (pass-09, E19); two memos claiming a ratification their entries read `null` on, and one citing an entry for a status it does not decide (pass-28 / pass-29). Plus one record-level sighting kept apart from the artifact count: `grounding: full` declared with no corpus file opened (pass-15) | 2 of 7 — Discovery, Leadership |

**Sighted, not yet a mode.** Two more shapes recur in the critiques, and neither is coded, because the column labels what a pass *was* and no fail is led by either. They are written here so the second engagement's labels can confirm or dissolve them; a shape earns a code when it leads a fail there.

- **Invented threshold** — a number, floor or owner the seat had no upstream source or authority for: a key-result floor on a metric the Insights seat had declined to threshold, and an owner assigned to an agent seat that does not exist after Close (pass-25 / pass-26, gate M9). Two defects, one seat (Delivery), the lead shape of pass-25 — which is why pass-25's `failure_code` is blank rather than stretched onto `unobservable-measure` on the strength of two of its four bounced rows.
- **Contradicts a standing rule** — the draft contradicts a ruling ratified upstream or a rule in its own text: two roster counts against a floor ratified that same morning and a build push its own headline rule forbids (pass-19), a kill condition breaking the policy clause the same revision added (pass-03), a worst case run at eight while the scenarios ran five to six and one weekly rate against another (pass-21 / pass-23), an overbroad sentence kept in the ledger after the artifact corrected it (pass-24, gate N5). Six defects across three seats (Growth, Strategist, Business), the lead shape of no fail. The one ruling this proposal leaves to Sean: pass-19 carries two contradictions beside its one unrecordable metric, and could be coded here instead.

**The process-waste prediction, checked.** [#296](https://github.com/seanwinslow28/code-brain/issues/296)'s unlabeled classification counted 1 `kit-induced`, 1 `stale-restatement`, 1 `overstated-scope`, 0 `manufactured`. The labels agree as *findings*: the stale residual rows are named in pass-30's critique, the over-counted owner corrections in pass-29's (N2), the memo template's contribution in pass-28's (gate N8), and no row in 33 reads any finding as manufactured. As *coded rows* the count is 0 / 0 / 0 / 0, which is what this file's own rule requires — each was one NOTE-severity row inside a gate pass whose other findings were sound, so the pass stays `pass` with the waste named in its critique.

## Rung 2

No judge exists and none is earned. A judge arrives for one named mode, after it recurs across engagements, with 30–50 labels per class and a reported TPR/TNR against Sean's own labels. Until then the codes are read, not scored.
