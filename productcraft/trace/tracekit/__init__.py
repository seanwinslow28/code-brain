"""tracekit — the Productcraft trace kit (build map #264, ticket #290).

Designed on #272 and #292: the pass-record template, the labels-file template,
the rung-0 checker, the viewer renderer, and the cases template the viewer's
guided reading is written to (DESIGN.md §14). Stdlib only:
the Close ritual runs on whatever python3 the session has, with nothing
installed, no model and no network. Scripts read the private ledger only at
run time; nothing here carries engagement content.

First copy. The content machine's kit (#291) shares this code rather than
forking it; `craftwork` extracts the shared home later.
"""

KIT_NAME = "productcraft/trace"
KIT_VERSION = "0.1.0"
