# Agent-company BUILD — ticket #7: onboarding extraction (continuation)

**Where we are:** ticket #6 CLOSED 2026-08-10. The canon ledger is built,
audited, corrected, and signed. Three commits — `eb25832` (build), `05f2d77`
(external-audit fold-in), `1395b4e` (Sean's sign-off). CI green, validator 0
errors stateless and `--diff a632f31`, **185 tests**. Map #1's Decisions-so-far
carries the resolution pointer. #7 and #8 are both unblocked; **#7 comes first
in map order.** This session picks up the build frontier.

**Read this before anything else:** #6's proposal claimed more than the code
delivered in five places, and it took an outside model to catch it. That is now
the house expectation, not an incident — see "Before you propose anything"
below.

## The company repo (all company work happens THERE, not in code-brain)

`seanwinslow28/driftgate` — private; name is a provisional codename; local clone
at `/Users/seanwinslow/Code-Brain/driftgate`.

- Wayfinder map: issue **#1**; frontier = first open child in map order with no
  open blocker and no assignee. **Verify with `gh` before claiming** (native
  sub-issue blocking relations are the truth; pass `-R seanwinslow28/driftgate`
  or you will read code-brain's issues by mistake) — expected frontier:
  **#7 Onboarding extraction on Sean's slice series**, size **M**. Its blocker
  #6 is closed.
- Claim = `--add-assignee seanwinslow28`; resolve = comment answer → close →
  pointer appended to map #1's Decisions-so-far.
- **#2 (naming) stays PARKED** — final lock happens in the design/logo phase.
  Do NOT reopen.

## What the repo now contains (read before building)

1. `AGENTS.md` — the routing file. Read it first; it inherits every agent into
   the standing rules and carries the role table, the `docs/schemas/` entry, and
   the **two proposal routes**.
2. `interview/` — 8 frozen layers, never edited; corrections are new layers.
   Layer 2 carries the master governance artifacts verbatim: the **45-item
   forbidden list**, the **two-scope pause condition**, the **three-tier
   retirement condition** (Sean is sole confirmation authority).
3. `ontologies/` + `skills/` + `governance/` + `memory/` — the generated
   instance. 4 skill work packages, all `provisioned: no`. 5 founding rules.
4. `roles/` — six seats, all `provisioned: no`. **The librarian's card governs
   this ticket too** — its `evidence_required`, `sources_must_not_use`, and
   `review_sample` lines are about to be exercised for real.
5. `src/driftgate/` — `roles.py`, `killswitch.py`, `task_result.py`,
   `escalation.py`, `permissions.py`, `frontmatter.py`, and **#6's four:
   `ids.py`, `canon.py`, `snapshot.py`, `ledger.py`**. Zero third-party
   dependencies — keep it that way unless there is a real reason not to.
6. **`docs/schemas/canon-ledger-v1.md`** — the contract you are about to write
   against. Read its "Five properties, and exactly how far each one holds" and
   "What is stubbed, and what is merely labelled" sections; they are deliberately
   narrow and you should not widen them in prose without widening the code.
7. **`governance/enforcement-gaps.md`** — R5's register, now **24 rows across
   three dated passes**. Six rows supersede earlier ones that overclaimed.
   Append-and-supersede: a row's strength changes by a **new dated row**, never
   an edit.
8. **`docs/reviews/2026-08-10-codex-audit-canon-ledger-store.md`** — the external
   audit, kept in full. Worth reading for the shape of what got missed.
9. `docs/adr/ADR-001-system-of-record.md` — §4 tenancy and §5 export/delete are
   binding spec; §5 is unbuilt (G41) and this ticket does not build it.

## Governing record (the record governs; cite, don't restate)

- Ratification package (D1-D13) + second opinion (A1-A6, binding):
  `code-brain vault/20_projects/research/2026-08-08-architecture-*`
- **The extraction protocol this ticket productizes:**
  `2026-08-08-canon-extraction-test.md` — and its full corpus, proposed bibles,
  change reports, and blind maps in `2026-08-08-canon-extraction-test/`. The
  method is already validated; #7 is running it *into the ledger*, not
  redesigning it.
- Cost ceiling source: second-opinion addition 2. First datapoint ~47K tokens per
  6-page episode → ~$1.20 (flash-class) to ~$12 (Sonnet-class) per 50
  installments, projected not billed.
- Groundwork engine (validator + schemas):
  `/Users/seanwinslow/Code-Brain/groundwork` — pull-only; friction goes upstream
  as issues, never patches from here. Seven filed so far (#24–#30).

## THE TASK — ticket #7 (after verifying it is the frontier)

Read the ticket body first; it is specific. In summary — run the productized
onboarding pass over Sean's slice series, writing into the canon ledger:

- Sequential era-by-era extraction, exactly as the product would: bible v1 from
  era 1, each later era judged against the prior bible, producing typed
  evolution events.
- Agent-proposes / creator-confirms for fine attributes. Both spikes reached the
  same boundary: **models own structure and judgement; stated canon facts own
  fine attributes.**
- **Measure onboarding cost** against the ≤~$20/50-installment ceiling. If blown,
  tiered onboarding (recent-N first, backfill lazily) is the **pre-approved**
  fallback — take it, don't re-litigate it.

**Acceptance (from the ticket):** confirmed canon bible in the ledger for the
slice series · cost datapoint recorded on the ticket · confirmation flow
exercised at least once for real.

### What makes this ticket different from every one before it

**Real creator content enters the system for the first time.** Everything so far
has been config and code. From this ticket on there is material on disk that
belongs to a person.

- Everything file-shaped lives under `~/.driftgate/data/tenants/<creator-id>/`,
  **outside the repo by construction**. `tenants/` and `.driftgate/` are
  gitignored. **Never `git add` creator content, never paste an extracted fact
  into a tracked file, never put a page image in the repo to "test something."**
- G20 (development environments where creator-data mounts do not exist) is
  tracked to this ticket and is currently `instruction-strength`. If you cannot
  build the environment, say so in the register rather than claiming it.
- The Pepper&Carrot corpus is CC-BY, external, analysis-only, no redistribution.
  Sean's own material is his.

**This is where the machinery gets its first caller.** Roughly ten register rows
are `enforced-unreached` precisely because nothing opens a ledger. #7 is the
first thing that does. Expect to update — with new dated rows, honestly — at
least: **G22, G26, G27, G29, G30, G33, G40, G42** (all `enforced-unreached`,
tracked to #7), plus **G34** (the current-installment input, which onboarding is
supposed to supply and nothing does yet) and **G38** (extractor pin, currently
validated for shape and not for truth). `enforced-unreached` becoming `enforced`
requires a production path that actually ran — not a test.

**Two decisions belong to Sean, early, before you burn tokens:**

1. **Which series.** The ticket says Sean picks: Pencil Test (14 sequential
   production frames, ratified `character.yaml` as ground truth) or a P&P-style
   serial. Ask; don't assume.
2. **Spend.** A real extraction pass costs real money on a frontier model. Sean
   owns every above-cap spend (forbidden 37 — the fleet buys nothing). Estimate
   before running, and if the estimate is uncertain, **fail closed** rather than
   proceeding (forbidden 36).

**The confirmation flow must be exercised for real**, which means Sean has to sit
down and confirm at least one proposed fact. Plan the session so that step is a
short, well-prepared ask with the proposals already queued — not a surprise at
the end. The librarian card's `review_sample` says he reads *every* proposed
canon event awaiting confirmation on his own series during the dogfood slice.

## Before you propose anything

#6's proposal claimed "no code path reaches `confirmed` without a
`CreatorAction`" (only the ledger append path does), that a caller ignoring
`state` "still cannot" read a proposal as canon (it can), that evidence was
"immutable by construction" (it is non-mutable through one API), that a rewritten
or removed line "fails at load" (a suffix rewrite does not), and that a
`CanonStore` was tenant-bound (a `CanonLedger` is). Every one erred toward
sounding better. An external `gpt-5.6-sol` review caught all five plus seven code
defects and one D4 requirement that had been declared in a schema table and never
built.

So, standing practice for this ticket:

- **Write the claim, then try to break it before Sean reads it.** An honest gap
  beats a clean-looking claim, every time.
- Prefer an external red-team on anything governed before sign-off. Codex trips a
  content filter on "attack / red-team the implementation" phrasing — frame it as
  a correctness and accuracy audit and it runs fine.
- Verify another agent's findings yourself before acting on them. Most of the
  audit was right; the severity ratings needed tempering.
- **Check claims before making them.** #5's closing comment called branch
  protection a two-minute setting without testing it, and was wrong twice over.

## How governed changes land here

Two routes, and the split matters:

- `proposals/` — the groundwork engine's route. A proposal's `target` MUST be a
  `skills/` path or `governance/constitution/`; anything else is a validator
  ERROR.
- `governance/change-proposals/` — driftgate's own route for role cards,
  permission profiles, the enforcement-gap register, and the schemas. Same
  contract (diff, reason, evidence, blast radius, Sean's sign-off), append-only
  rather than pending-only.

Nothing enforces either for those paths (register row G25; upstream groundwork
#30). Follow it anyway.

Validate with `python3 /Users/seanwinslow/Code-Brain/groundwork/scripts/validate.py .`
and `--diff a632f31` after any governed change. **CI diff bases must be
`a632f31` or later** — a diff spanning the generation commit false-fires the
proposal tripwire (groundwork #28). Keep CI green: `uv run ruff check .` and
`uv run pytest` (currently 185 passing).

**Open process question Sean flagged and has not settled:** governed files
currently land on `main` *before* his signature, because that is what #5 and #6
both did. `AGENTS.md` says to wait for sign-off. It works only because he is the
only identity touching the repo. Raise it if it comes up; don't change the
practice unilaterally.

## Standing constraints

[L2] fleet builds and operates; build-in-public wraps it. [L6] month-6 compound
bar, autonomy-proof primary. [L7] ~25 hrs/week co-primary with the job hunt,
≤$250/mo opex, quality over speed. Slice scope ratified — one creator (Sean), one
series, stills + text, advisory drift report with receipts, Phoenix-traced —
**do not widen.** Meta-tooling ≤20% of build hours. STOP ADDING DECISIONS
(addition 6): remaining unknowns are measured during the slice.

## Sean-confirmed decisions this build must honor (do not reopen)

- All 8 interview checkpoints (2026-08-09/10) — the layers are the record.
- Skills and roles stay `provisioned: no` until each actually runs under the
  executor/CI; flipping one is a governed change with evidence.
- Backup owner is "no one — work pauses" until a trusted human joins (then: a NEW
  layer, never an edit).
- Only Sean confirms retirement triggers; only Sean resolves pause packets; Sean
  owns every merge, publication, production action, and above-cap spend.
- Shadow rate $100/hr; baselines in `memory/` are the comparison floor.
- **Ticket #5's five implementation calls**, signed 2026-08-10.
- **Ticket #6's three, signed 2026-08-10:** decay `N = 12` provisional and still
  proposal-only for the librarian; the resolution policy as built (like-with-like
  gating, and a corroborating run must reach the observation being judged); and
  **a corroborated evolution never displaces a creator-`confirmed` or `declared`
  value — it becomes a `needs_creator_decision` contender (G42)**. That third one
  is load-bearing for #7: the dogfood run will produce evolutions over Sean's own
  confirmed facts, and they are advisory by design.
- **G18 (branch protection) is closed as blocked, not deferred.** Private repo on
  a Free GitHub plan; protection and rulesets both 403. Revisit only when the
  fleet holds its own credential. Do not re-litigate, and do not purchase
  anything (forbidden 37).

## Known open, not this ticket

- **G17** (mediated tool layer) and **G19** (secret broker) are unbuilt,
  buildable, and have no child on the map.
- **G28** — a `CreatorAction` is mandatory but unauthenticated. #15.
- **G36** — `awaiting_confirmation` is a label, not a barrier; blocking a
  proposal from reaching a verdict is verdict-side. #13/#18.
- **G41** — ADR-001 §5 export/delete primitives are binding spec and unbuilt.
- **G33** — a fact id survives everything except an attribute rename; the rename
  or alias event is unbuilt.
- Interview second pass (parked, in the manifest): corpus & ground-truth
  stewardship deep record · review-inbox deep record · the channel question
  (P&P vs a dedicated driftgate channel).
- **#8** (D2 pipeline state machine, size L) is also unblocked. If #7 stalls on a
  Sean-owned decision, #8 is the honest place to move rather than idling — but
  say so explicitly rather than switching quietly.

## Conventions

Company work tracks in driftgate issues; research artifacts →
`vault/20_projects/research/` (commit vault yourself on the MBP); deferred
code-brain work → one-line ticket under `## Todo` in `vault/00_inbox/tickets.md`.
Sean ratifies anything that changes a ratified decision; everything else, proceed
autonomously and report with receipts. Sean is a PM, not a dev — explain jargon
and trade-offs in plain language before asking him to decide.
