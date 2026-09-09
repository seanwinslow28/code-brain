# CLAUDE.md — Productcraft

**Productcraft — a product leadership studio.**

The second studio built by the Systemcraft method: a seven-seat specialist bench for product leadership work — strategy, discovery, evidence, growth, business economics, delivery, and the leadership decisions that hold them together. It plans, executes, and audits, and explains every material choice (why A over B, briefly, and what it leaned on from the canon) so the work doubles as demonstration. The machinery is public; the brain is private.

## Status

Scaffold only. The studio is being built along the [Productcraft build map](https://github.com/seanwinslow28/code-brain/issues/264) — the wayfinder map holds the ratified decisions and the open design tickets. Nothing in this folder is final until its owning ticket closes.

## Layout

| Path | Lane | What lives here |
|---|---|---|
| `bench/` | public | Seven specialist seat definitions: Product Strategist, Discovery Lead, Insights & Analytics, Growth & Distribution Architect, Business & Economics Modeler, Delivery & Execution Lead, Product Leadership & Org Designer |
| `templates/` | public | Artifact templates, one per seat-owned artifact — including the leadership seat's hard contracts (stakeholder map, decision memo, operating-model doc) — plus the Systemcraft handoff contract and ratified law surfaces |
| `lanes/` | public | Seven lane manifests — topic-organized tables of contents (title + pointer + one-line when-to-read) into the private corpus, doubling as reading paths for listen-only titles. Shelf labels, never the books: an entry that paraphrases a source's substance belongs in the private lane |
| `corpus/` | **private — gitignored** | Two-layer reference corpus: free-canon distillates + book-to-skill ingests |
| `ledger/` | **private — gitignored** | The decision ledger — every design the studio produces, accreting per engagement, each entry carrying its "from the canon" line |
| `books/` | **private — gitignored** | Guard directory only: purchased ebooks live at `~/Books/productcraft/`, outside the repo. Nothing should ever sit here |
| master skill | public | Lives in `.claude/skills/` per the house rule; its design is owned by the map's Master skill design ticket |

`bench/`, `templates/`, and `lanes/` hold only a placeholder README each; their contents are created by their own map tickets.

## Non-negotiable rules

1. **Public machinery, private brain.** `corpus/`, `ledger/`, and `books/` are local-only via the PRIVATE LAYER block in the root `.gitignore`. Never `git add` them, never weaken those rules, and never let book-derived text land in a tracked file or a GitHub issue. Assume every tracked file in this folder is read by a recruiter.
2. **Graceful degradation.** On a machine where the private lanes are absent (fresh clone, employer machine), seats say so plainly and continue on tracked knowledge — they never fabricate citations into a corpus they cannot read.
3. **Explain why, and name the canon.** Every material choice ships with a one-breath why-A-over-B and names what it leaned on from the canon — a title and the idea, never the book's text. That behavior is the studio's teaching surface.
4. **Insights measures, never decides.** The Insights & Analytics seat designs metrics, grades evidence strength, and reads experiments. It co-signs the Discovery Lead's evidence and audits the Growth seat's experiments. It never makes a product decision — the Strategist, Growth, and Business seats decide on its measurements, and Sean decides above them (Cagan's enablement rule; Systemcraft's "the seat that designs a test never grades it").
5. **Full artifacts forward, never summaries.** The seven seats run as a sequential pipeline; each seat receives the complete artifacts of the seats before it.
6. **Audits run fresh, in two closed cycles.** An audit is a fresh-context invocation that never sees the drafting conversation. Strategist → Leadership → Discovery → Strategist; Insights → Growth → Business → Delivery → Insights. Every seat audits exactly one artifact and is audited by exactly one peer. The red-team gate is a Codex-run protocol, not a seat.
7. **One invocation, one seat** *(inherited from Systemcraft eng-003.d30)*. An invocation carries exactly one seat identity, its seat contract, one lane manifest, and its declared target. Provider outages never merge lanes; a planned provider that is unavailable gets a dated, owner-approved substitution or a dated deferral — never a silent swap and never an escalation to Fable without asking.
8. **Systemcraft owns the AI-system layer.** Platform, technical, and AI-fluency questions route to Systemcraft through the handoff contract; Productcraft crosses typed artifacts and references, never its reasoning.
