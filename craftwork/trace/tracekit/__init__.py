"""tracekit — the shared trace kit every -craft team reads (built as Productcraft's on #290, shared on #325).

Designed on #272 and #292: the pass-record template, the labels-file template,
the rung-0 checker, the viewer renderer, and the cases template the viewer's
guided reading is written to (DESIGN.md §14). Stdlib only:
the Close ritual runs on whatever python3 the session has, with nothing
installed, no model and no network. Scripts read the private ledger only at
run time; nothing here carries engagement content.

0.2.0 closes the gaps the first engagement exposed (#297): the `open` and
`readout` record kinds, a meter that may be one total, corpus reads inherited
along an artifact's revision chain, shared repo machinery as provenance rather
than tampering, ledger entries hashed into the chain, and `nextid.py`.

0.3.0 opens rung 1's vocabulary (#298, landing #296 clause 8): `taxonomy.md`
holds the process-waste family, and a tenth rung-0 line keeps `failure_code`
inside it — a code outside the table is free text, and `manufactured` is a
finding unless the critique quotes the text it indicts.

0.4.0 opens the seat failure modes (#299): the parser reads every code table in
`taxonomy.md` rather than the first, so the seat family sits under its own heading
beside the process-waste family; the viewer's *Failure taxonomy* slot fills from
the labels file — one line per mode with its count, a row's code linking to its
mode — and stays in its empty state until a row carries a code.

0.5.0 adds the registry numbers (#286, #272 decision 9): `registry.py` derives the
runtime × seat table the runtime registry's § Numbers holds — labeled passes as
counts, the rung-0 clean count, medians over measured passes, trials and
promotions — so no number in that public file is ever typed by hand; the
meter-source vocabulary grows to one value per registry row, with a drift test.

0.6.0 makes the kit studio-agnostic (#291): a `Studio` profile (`studio.py`)
holds the one set of things the two studios disagree on — stages, kinds, the
kinds that own `## Moves`, gate seats, repo path prefixes, item-id shape, the
taxonomy file, one structure check — and the loader, checker and viewer read it
from the engagement. The content machine's profile lives beside the machine and
imports `tracekit` from here.

0.8.0 checks the runtime against the transcript (#321): the Agent tool's `opus` and
`sonnet` aliases moved to the 5.5 generation after the first train closed, and a
record written from the alias names a model that never ran. An eleventh rung-0
line reads each Claude pass's raw log for its model stamps and fails a record
whose `runtime:` disagrees; a pass with no log or no stamp is unverifiable, named.

0.8.1 follows a recorded move (#324): shared law moved into `craftwork/`, and a
closed record keeps the path its seat read. When a repo path is gone, the loader
looks it up in `craftwork/README.md` § Moved here and hashes the file where it now
lives. Same bytes still match; changed bytes are machinery that moved since the pass,
unverifiable as before; a path with no row still fails as missing. The paths
followed are named in a note.

0.9.0 moves the kit to `craftwork/trace/` (#325), the shared home every -craft
team inherits from, and takes Productcraft's shape out of it. No profile lives in
the kit any more: `resolve_studio` takes the one passed in, else the nearest
`<team>/trace/studio.py` above the engagement (Productcraft's sits at
`productcraft/trace/studio.py`, with its stage-structure check), else the file
`$TRACEKIT_STUDIO` names, and otherwise refuses. The taxonomy splits in two: the
process-waste family is the kit's `taxonomy.md`, shared by every studio unless
its profile sets `shared_taxonomy=False`; a studio's own seat modes stay in its
own file. The CLIs take `--studio <file>`. Productcraft's two engagements check
and render with the results they had at 0.8.1.

0.10.0 adds the handoff freezer (#326, ruled on #282 decision 6): `freeze.py` strips
the process parts a pair's binding names from each crossing artifact (sections by
heading, repair tags on headings, named paragraphs, frontmatter keys), hashes what
is left, and stamps the copy with that hash and the source's. Nothing is stripped
by guess: a binding with no `strip` block is refused. `verify` re-hashes a copy
without its stamps, so copies frozen verbatim before the rule still verify.

0.11.0 maps Systemcraft's five seats to families (#287): Design Strategist to framing,
Evals & Evidence Architect to evidence grading, Ops & Economics Modeler to
quantitative, and two new families, architecture and trust design, so that no model
earns one seat on another's work. A test fails when any bench seat file in either
studio would read `other`.

The content machine (#291) shares this code rather than forking it, through its
own profile.
"""

KIT_NAME = "craftwork/trace"
KIT_VERSION = "0.11.0"
