# trace — the shared trace kit

The evals-and-trace kit every -craft team reads, in [craftwork/](../README.md)'s shared home since kit 0.9.0 ([#325](https://github.com/seanwinslow28/code-brain/issues/325), 2026-10-01). It was built as Productcraft's, the public pieces that studio's evals-and-trace design needed before its first engagement opened. It was designed on [#272](https://github.com/seanwinslow28/code-brain/issues/272) (record, labels, ladder, blind trials) and [#292](https://github.com/seanwinslow28/code-brain/issues/292) (the viewer's [DESIGN.md](DESIGN.md)), built on [#290](https://github.com/seanwinslow28/code-brain/issues/290) (2026-09-13). Husain's order, local by law: log full traces → one expert reads them in a purpose-built viewer → binary pass/fail with a written critique → taxonomy → code checks → judges only for persistent failure modes. Nothing here ships a payload anywhere.

| Piece | File | Who uses it |
|---|---|---|
| Record template | [record-template.md](record-template.md) | the coordinator, one file per invocation |
| Labels-file template | [labels-template.md](labels-template.md) | Sean, one file per engagement |
| Rung-0 checker | [check.py](check.py) | Close, and any time between |
| Viewer renderer | [render.py](render.py) → `trace/eval.html`, to [DESIGN.md](DESIGN.md) | Sean, reading and labeling |
| Cases template | [cases-template.md](cases-template.md) → an engagement's `trace/cases.md` | the writer pass, once a train has run |
| Entry-id helper | [nextid.py](nextid.py) | the coordinator, before writing a ledger entry |
| Handoff freezer | [freeze.py](freeze.py): strips the process parts a pair's binding names from each crossing artifact, then hashes the copy ([handoff contract § 6](../handoff-contract.md)) | the sending seat at a handoff or return; the receiving seat's intake check runs `verify` |
| Shared failure codes | [taxonomy.md](taxonomy.md) — the process-waste family; each studio's own modes are in its own file | Sean, when a label carries a code; `check.py` reads every code table in both files; the viewer counts rows per mode |
| Registry numbers | [registry.py](registry.py) → the runtime × seat tables pasted into [craftwork/templates/runtime-registry.md](../../craftwork/templates/runtime-registry.md) § Numbers | the coordinator at Close, and #287's trials; counts only, never a percentage |

Everything runs on the system `python3` with nothing installed: no model, no network, no third-party import. Templates hold no private content; the scripts read the private ledger only at run time and write only `eval.html`.

## Whose engagement: studio profiles

The kit holds no studio. A studio's shape lives with the studio, in one **profile** file: the numbered stages, the record kinds, which kinds own `## Moves`, the gate seats, the repo path prefixes, the item-id shape, its taxonomy file, and its own rung-0 line 8 ([tracekit/studio.py](tracekit/studio.py) is the `Studio` shape). A -craft team writes `<team>/trace/studio.py` defining `STUDIO`. Productcraft's is [productcraft/trace/studio.py](../../productcraft/trace/studio.py), beside its seat failure modes and its samples.

Every command finds an engagement's profile in this order:

1. the file passed with `--studio <file>`;
2. the nearest `trace/studio.py` walking up from the engagement folder. A team's ledger sits inside the team's folder, so `productcraft/ledger/engagements/<eng-id>/` finds Productcraft's with no flag;
3. the file `$TRACEKIT_STUDIO` names;
4. otherwise the command refuses with exit 2. It never guesses a studio.

The content machine keeps its profile beside the machine (`machine.py`, in its own repo) and passes it explicitly. Systemcraft's is [systemcraft/trace/studio.py](../../systemcraft/trace/studio.py), written with its adoption of the shared law ([craftwork build 4](https://github.com/seanwinslow28/code-brain/issues/327)); it reads the brief header from `open-brief.md` and finds check records in `artifacts/`, and Systemcraft traces from eng-005 on.

## Where things live

Inside each engagement folder of a studio's private ledger (Productcraft's is `productcraft/ledger/engagements/<eng-id>/`, layout per #268), the kit owns one subfolder:

```
<eng-id>/
├── brief.md                        # Open: the header below, then the one-paragraph brief
├── artifacts/  audits/  dNN-*.md   # what the seats wrote — record paths are relative to this folder
├── readout/                        # the human versions of final, past-gate artifacts — never a pass input
└── trace/
    ├── pass-NN-<seat>-<kind>.md    # one immutable record per invocation
    ├── labels.md                   # Sean's verdicts, apart from the facts
    ├── cases.md                     # the guided-reading content, apart from the records
    ├── notes.md                    # process notes; the viewer's third growth slot
    ├── logs/                       # raw transcripts the records index (subagent JSONL, codex logs)
    ├── trials/                     # a trial's artifact, beside the train, never in artifacts/
    └── eval.html                   # the rendered viewer — local file, never hosted
```

The `trace/` subfolder is a #290 call: #272 said "in the engagement folder", and twenty-six pass files at the ledger root would bury the decision entries the ledger exists for. Both commands accept the engagement folder or its `trace/` subfolder.

**The brief header the kit reads.** `brief.md` (the profile names the file) opens with frontmatter the coordinator writes at Open: `id` (`pc-eng-NNN` in Productcraft), `name`, `type` (`full-train` | `audit` | `execution-breakdown` | `one-off` | `role-support`), `opened`, `closed` (null until Close), `pass_budget`, and `synthetic: true` only on invented engagements (the viewer shows a badge; a real engagement shows nothing, never "REAL"). The stage-structure check asserts the full train's shape only when `type` says full train.

## The Close ritual — three lines, adopted verbatim by both studios' master skills

```bash
python3 craftwork/trace/check.py productcraft/ledger/engagements/<eng-id>
```

```bash
python3 craftwork/trace/render.py productcraft/ledger/engagements/<eng-id>
```

Then confirm every pass has a row with a verdict in `trace/labels.md`. The checker exits 0 when every line passes, 1 when any fails (each finding names the pass and the thing), 2 when the path is not an engagement. `--json` emits the same checks as data. The renderer never refuses to render on a failing check: the page is how the failure gets seen.

## Rung 0 — what the checker asserts, and what it cannot see

Ten deterministic lines, in this order:

1. **Records parse and carry every required field** — the YAML subset parses; every field in the template is present; `kind` and `stage` are in range; `withheld` names the drafting conversation.
2. **Every pass has a record** — the numbering has no gap; every id referenced by `checks`, `triggered_by`, `shadow_of` or the labels file has a record; each filename matches its record.
3. **Every pass has a label row** — and every row names a real pass. Rows still waiting for a verdict are counted in a note.
4. **Input hashes match disk or a recorded prior revision** — each input's sha256 matches the file now, or matches a hash an earlier pass recorded as its output for that path *and* the disk holds the latest recorded revision. Outputs are checked the same way. A file edited outside a pass fails here — with one carve-out, below.
5. **Cited corpus files appear in the transcript's file reads** — every `corpus/…` path an output artifact or ledger entry cites is in the record's `## Corpus read`, **or in that of an earlier pass which wrote the same artifact**: a repair inherits the citations of the revision it overwrote, and charging it with those reads would be a false finding. Reads travel along one artifact's revision chain, never sideways. `grounding: full` with no corpus read, or `grounding: none` with one of this pass's own, is a finding.
6. **Every move names an existing upstream item; splits are subsets** — each `kept` / `split` / `merged` / `dropped` item is found in an input readable at its recorded hash (ids like `O2`, `OC-1a`, `KR-2`; ranges like `E1–E5` expand; prose items are phrase-matched); a split's children are new and appear in the artifact. Malformed lines and unknown ops are findings. `added` lines are new by definition.
7. **Meter present or UNMEASURED** — `meter_source` is one value of the [runtime registry](../../craftwork/templates/runtime-registry.md)'s vocabulary (one per registry row, mirrored as `METER_SOURCES` and held equal by a test); a measured meter carries whole token counts in one of two forms, the split `input` + `output` pair or a single `total` (which is what the Agent tool's usage field and the Codex footer each actually report; every other row reports the pair); `UNMEASURED` is honest and listed, and so is a total that was never split.
8. **The studio's own structure line** — the one check a profile writes for itself and registers when it loads. Productcraft's is *each drafting stage has one draft, an audit, and its required co-signs*: per stage reached, exactly one `draft` by the stage's seat, at least one `audit` by the fixed auditor, a `co-sign` by the co-signing seat at stages 2 and 6, on full trains only. A profile that registers none gets an honest note on this line, never a pass it did not earn.
9. **Trials blind-labeled before their runtime is shown** — a trial's inputs are hash-identical to its baseline's; while either lacks a verdict, the rendered page's rows for both hide runtime, launch form and log path (the check reads the pair's own rows in `eval.html`, since gates may share a runtime).
10. **Every `failure_code` is in the taxonomy; a quote-required code quotes its text** — a code in `labels.md` must appear in the shared [taxonomy.md](taxonomy.md) or the studio's own file (a profile with `shared_taxonomy=False` reads its own alone), so the column can never be free text, and `manufactured` is a finding unless the row's critique quotes the text it indicts. A blank column is the normal state and passes with a note (#296 clause 8, landed #298).
11. **Recorded runtime matches the raw log's model stamps** — a Claude pass's `runtime:` must equal the model every assistant message in its own JSONL raw log is stamped with; a different or second model is a finding naming both. An alias is not a pin: the Agent tool's `opus` / `sonnet` moved to the 5.5 generation after the first train closed, and a record written from the alias would name a model that never ran (#321). `<synthetic>` stamps are ignored; a pass with no JSONL log or no stamp is unverifiable, named; Codex and the other rows are out of scope until their logs are read the same way, and so are the coordinator's own passes with no log.

**Shared machinery is provenance, not a chain link.** A seat's inputs include the studio's own files — its seat contract, a lane manifest, an artifact template — which live in the repo, outside the engagement, and keep improving after a train closes. The ticket that fixes a template is doing its job, not tampering with a record, so a repo-path input (`productcraft/…`, `systemcraft/…`, `craftwork/…`, `.claude/…`) that **no pass in this engagement wrote** is counted *unverifiable* and named in a note when its hash has moved, exactly as an overwritten revision's Moves are. The recorded hash is never rewritten to match. Everything the engagement itself wrote — including a repo path some pass recorded as an output — stays strict, which is where the guarantee matters. The limit, stated plainly: this cannot tell a template edited *between* two passes of a live train from one edited a month after Close; mid-train, that belongs in the engagement's `## Notes`. **A file that moved** (kit 0.8.1, #324) is followed through [craftwork/README.md](../../craftwork/README.md) § Moved here: the record keeps the old path, the loader hashes the file where it now lives, and the paths followed are named in a note. A moved path with no row in that table still fails as missing.

**Ledger entries ride the chain.** A drafting pass lists each entry it wrote as a `- path:` block with its hash, with the `- id:` beside it — an entry with no hash is outside the chain, so an edit to it is invisible. When the coordinator marks an older entry `status: superseded`, that edit is an **output of the superseding pass**, recorded there with the new hash; otherwise the entry reads as edited outside any pass and fails line 4, correctly.

**What rung 0 cannot see.** Artifacts are redrafted in place (#274), so a superseded revision is no longer on disk. The checker names this honestly rather than passing or failing it: a pass whose artifact was later overwritten has its Moves reported as no longer on disk; a move whose only possible home is an unreadable revision is counted *unverifiable*, never verified. A replay over the raw transcript is a later rung (#272 decision 4), not day one. Apart from line 11's model stamps, the checker does not read transcripts: `## Corpus read` is written by the coordinator from the transcript's file reads, and the checker trusts the record.

## The next entry id

Ids are permanent and bare (#268), so a gap in the `dNN` numbering is harmless — but reserving a block ahead of writing it is how two passes end up claiming one id, which is what the first engagement did. The helper hands out the next free one and shows its working:

```bash
python3 craftwork/trace/nextid.py productcraft/ledger/engagements/<eng-id>
```

An id is **claimed** by a file on disk *or* by a pass record naming it among its outputs, so a reserved-but-unwritten id is never handed out twice. The report names the gaps (left alone, never reused) and separately the ids a record reserved but no file fills — at Close, each of those is either a gap or an entry someone forgot to write. `--bare` prints the id alone, for a shell variable. Read-only: it writes nothing.

## The viewer

One self-contained HTML per engagement, to [DESIGN.md](DESIGN.md) (APPROVED 2026-09-11, the renderer's authority — if the two disagree, DESIGN.md is the intent and the renderer is the bug). Masthead → prose reading line → labeling counter → the first-failing-stage matrix beside the fails with their critiques and the rung-0 checks → the train → one folded row per pass → three growth slots → footer. Fonts embedded from [fonts/](fonts/); every string from a record, label or artifact is escaped; no `<link>`, no `<script src>`, no URLs. Labels drafted on the page live in the browser and leave through **Copy label rows**; the file is the record. **The blind rule:** a shadow pair's runtime, launch form, meter source and log path are not in the HTML at all until both rows carry a verdict in the labels file — the reveal happens on the next render, never on the page.

## Guided reading

The page teaches as it is read, to phase 3 of the eval learning plan (adopted 2026-09-20, recorded in [DESIGN.md §14](DESIGN.md)). Above the counts it states the four things a reader is judging, kept apart — record checks, the seats' findings, your own labels, the owner decisions that are yours alone — with the versioned review prompt for each kind of run. Below them sits **guided reading**: one chapter per case, with decreasing help, each leading with a plain `Run NN · <Seat> <kind>` line, quoting its source with the line it sits on, and offering a question, a note and a bookmark.

That teaching content is **not** in the renderer. It lives in `trace/cases.md` beside the records, written by hand in a **writer pass** after a train has run, to [cases-template.md](cases-template.md): one case per pass and finding, each source pinned to the sha256 it carried at writing time. The renderer reads, checks and qualifies it, and composes nothing. No file renders an honest empty section; a source whose hash has moved renders "the source changed since this story was written" instead of a stale quote; an excerpt that is not in its file is printed as an error. Practice answers live in the browser under a key of their own and never touch `labels.md` — the page records which help was opened before each answer, so an assisted answer is never mistaken for a blind one.

## Tests and the synthetic sample

Everything is tested on an invented engagement, never on ledger content. `pc-eng-000` "Callboard" (a fictional casting tool for community theatre, the same invention #292's sample used) is built by [tests/synth.py](tests/synth.py), which *simulates* the train — it hashes each pass's inputs from the folder as it stands and lets repairs overwrite artifacts in place — so the records' hash chain is real and the checker is exercised on superseded revisions, bounce loops and a blind pair. It refuses to write under any `ledger/` path.

```bash
cd /Users/seanwinslow/Code-Brain/code-brain && agents-sdk/.venv/bin/python3 -m pytest craftwork/trace/tests -q
```

```bash
python3 craftwork/trace/tests/synth.py productcraft/trace/samples/synthetic-engagement && python3 craftwork/trace/check.py productcraft/trace/samples/synthetic-engagement && python3 craftwork/trace/render.py productcraft/trace/samples/synthetic-engagement
```

The kit's tests run through **Productcraft's profile**, the first studio the kit served, because the simulated train is Productcraft-shaped. [tests/reference.py](tests/reference.py) loads it from where it lives, never a copy, and names it in `$TRACEKIT_STUDIO` for engagements built under a temp folder. A toy profile in `test_studio.py` keeps the kit honest about any other shape. [productcraft/trace/samples/synthetic-engagement/](../../productcraft/trace/samples/synthetic-engagement/) is the folder `synth.py` builds, committed with its rendered `trace/eval.html` so the page can be opened from a fresh clone. It is Productcraft's sample, so it lives there. The #292 prototype render Sean ratified stays untouched at [productcraft/trace/samples/pc-eng-000-callboard/](../../productcraft/trace/samples/pc-eng-000-callboard/).

## Registry numbers

What each runtime has done on real work lives in the registry's § Numbers as **counts** — labeled passes as "3 of 4", the rung-0 clean count, medians over measured passes, trials and promotions — and never as a number typed by hand: `python3 craftwork/trace/registry.py productcraft/ledger/engagements/pc-eng-*` regenerates both tables (per runtime, per runtime × seat with its family) and the coordinator replaces the section at Close. The generator runs rung 0 in memory to learn which passes a finding names, counts a meter as measured only from a registered source, and reads a promotion from one `promoted:` line in the trial record's `## Notes` (#272 decision 9, built on [#286](https://github.com/seanwinslow28/code-brain/issues/286)). No percentage at any count. Every seat file on either studio's bench maps to a family in `SEAT_FAMILIES` (`tracekit/registry.py`); a test fails when one would read `other` (#287).

## Freezing a handoff copy

A handoff crosses artifacts, never reasoning, so the copies leave their process parts at home ([the handoff contract](../handoff-contract.md) § 6, built on [#326](https://github.com/seanwinslow28/code-brain/issues/326)). The pair's binding names those parts in a fenced `strip` block; `freeze.py` removes exactly what it names and refuses a binding without one. `show` lists what a copy would lose and writes nothing. `copy` writes `<source-id>--<slug>.md`, stamped with the stripped copy's hash and the source's, and prints the manifest. `verify` re-hashes a copy without its stamp lines, and with `<copy>=<artifact>` also reports a source that has moved since the freeze. Copies frozen verbatim before the rule (three stamps) verify unchanged. The library is `tracekit/freeze.py`; the tests are `tests/test_freeze.py`.

## Shared home

This kit was the **first copy** (#272 decision 8), built inside Productcraft on #290. Since kit **0.6.0** (#291, 2026-09-22) it has been **studio-agnostic**, and since **0.9.0** (#325, 2026-10-01) it lives in [craftwork/](../README.md) and holds no studio at all: every profile lives with its studio, as above. The content machine imports `tracekit` from here through its own profile (`machine.py`: stages 0 Oracle → 6 Lessons, kinds `sweep` … `lesson`, rep ids like `Rep 7e`, line 8 *each shape ran in the clean context, was gated, and reached the pick*) and forks nothing. Its `$TRACEKIT_DIR` defaults to this folder.

**Rung 1 is two files.** This folder's [taxonomy.md](taxonomy.md) holds the families every studio shares. Today that is the **process-waste** family, earned by [#296](https://github.com/seanwinslow28/code-brain/issues/296)'s investigation of the checks rather than by labels. A studio's own file holds its **seat failure modes**. Productcraft's opened on [#299](https://github.com/seanwinslow28/code-brain/issues/299) from the first engagement's 33 labels, with two modes coded, two shapes sighted and held off the table, and every count carrying the labels' assisted provenance. Those modes stayed in [productcraft/trace/taxonomy.md](../../productcraft/trace/taxonomy.md) when the kit moved. The viewer's *Failure taxonomy* slot fills from the labels file, one line per mode with its count. Rung 2 (a judge per failure mode, validated on TPR/TNR) lands beside the studio's taxonomy when it is earned, not here.
