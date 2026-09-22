"""tracekit — the Productcraft trace kit (build map #264, ticket #290).

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
from the engagement. `PRODUCTCRAFT` is the default profile, so nothing that
called the kit before changes meaning; the content machine's profile lives
beside the machine and imports `tracekit` from here.

First copy. The content machine's kit (#291) shares this code rather than
forking it; `craftwork` extracts the shared home later.
"""

KIT_NAME = "productcraft/trace"
KIT_VERSION = "0.6.0"
