# samples — synthetic renders for the viewer design

Everything here is invented. `pc-eng-000` "Callboard" is a fictional casting tool for community theatre; no seat wrote any of it, no book was read for it, no ledger entry exists. It exists so the eval viewer's `DESIGN.md` (#292) had a page to react to.

- `render_sample.py` — the hand-built prototype that emits the sample. It is **not** the trace kit's renderer; #290 builds that, to `../DESIGN.md`, and may lift what it wants from here. Run from `productcraft/trace/`: `python3 samples/render_sample.py`.
- `pc-eng-000-callboard/eval.html` — the rendered page. Open it from disk; it needs no network.
- `pc-eng-000-callboard/synthetic-data.json` — the same invented records and labels as data, for #290's tests.

Never point this script at the real ledger.
