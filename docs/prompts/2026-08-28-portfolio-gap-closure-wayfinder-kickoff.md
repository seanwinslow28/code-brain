# Kickoff — portfolio gap closure build map (wayfinder)

Paste-ready prompt for a fresh Fable 5 session. Written 2026-08-28 at the close of the
panel-numbers content session, after the 25 ruled panels landed and the Nate B. Jones
cross-check surfaced two structural gaps.

**Sequencing note for Sean, not part of the prompt:** panel art is deliberately out of
scope below. Whether art runs before or after this map is a separate call you said you'd
make after reading this.

---

/wayfinder

Chart a build map for **closing the gaps in my portfolio's five project pages** — the work
that makes each page's claims true, reproducible, and legible to a recruiter who will not
dig. Repo for the map: `seanwinslow28/code-brain` (per CLAUDE.md, all wayfinder maps live
there even when the work lands in other repos).

**Override the plan-only default in the map's Notes: this map carries execution.** The
gaps are already diagnosed and mostly decided; what I need is them planned into sessions
and *done*, not a second round of deliberation. Where a ticket genuinely holds an open
decision I'll flag it below — everything else is execution.

## Source of truth — read these first, in this order

1. `~/Code-Brain/seanwinslow.com/docs/plans/2026-08-28-4q-risk-slot-and-explanation-artifacts.md`
   — the Nate B. Jones cross-check. Contains the 4Q template, the Situation/Decision/Risk/Change
   mapping, the five costed options for the missing Risk slot, the EXPLANATION.md link table,
   and the measured byte-headroom constraint. **The five options are tabled, not decided.**
2. The "Project-tile panel art direction" ticket in `vault/00_inbox/tickets.md` — the running
   log for this whole effort, including the 2026-08-28 correction entry at the end.
3. `~/Code-Brain/seanwinslow.com/src/data/projects.ts` — the 25 ruled panels as they now stand,
   and the six `descriptionStatus: 'approved'` strings this map re-opens.
4. `~/Code-Brain/seanwinslow.com/tests/beats.test.ts` — the `RULED` enumeration guard. Any new
   project content must keep it green.

## Destination

Every claim on the five project pages is reproducible by a stranger in one command or one
click, every page states what would break as well as what worked, and no page under-sells
the system behind it. Driftgate stays frozen.

## Standing constraints every ticket inherits

- **Provenance or it doesn't ship.** Every figure carries the file, command, or commit that
  proves it, recorded in the ticket. A countable and an assessment are different things and
  never get dressed as each other.
- **Byte grant.** The five real pages sit at ~3.75 KB of a 4096-byte route grant, ~300 bytes
  headroom each. `node scripts/build-byte-manifest.mjs` after any markup or copy change.
- **Gates on every commit to the site:** `npm run check` clean · `npm test` (265 baseline;
  document any change) · `npm run floors` GREEN · byte manifest ok.
- **Driftgate is frozen.** No digging, no page changes, no panels. The systemcraft
  swap-or-add call is mine and is not part of this map.
- **Public-repo privacy rules** (CLAUDE.md rule 9) apply to anything moved into `code-brain`
  or `groundwork`.
- Panel **art** is out of scope for this map entirely.

## Ticket inventory the map must cover

Wayfinder decides final decomposition, sizing, and blocking edges, but nothing here may be
dropped. Rough priority order given; challenge it if the dependency graph disagrees.

### Tier 1 — live liabilities, unblocked, do first

- **Agent Dash is not building.** Last snapshot commit 2026-08-11. `fleet.seanwinslow.com`
  is linked from the site as "Live" and is serving 17-day-old data, on a board whose entire
  argument is dated evidence. Its `3 nights` panel describes a hero counter that is currently
  frozen. Restart the nightly cron, verify a fresh snapshot lands, confirm the hero counter
  moves. Repo `~/Code-Brain/agent-fleet-observability`.
- **Agent Dash README is stale in two measurable places.** It claims `55 tests` (the suite
  collects **167**; 164 pass, 3 fail) and `~1,200 lines including tests` (actually **5,192**).
  The site links this README. Also decide what to do about the 3 failures — they look like
  hardcoded-date drift in `test_aggregations.py` and `test_kanban.py`, not real regressions;
  fix or document, don't leave them ambiguous.
- **Intent MCP: verify the rest of the README's numbers.** The dogfood claim was corrected
  2026-08-28 (`sw-mcp-intent-engineering` `d8ed73c`) after it turned out to be a paginated
  chunk score published as a whole-file score. **The same paragraph still claims the 118-skill
  batch ran with "zero parse errors" "in under a second", neither re-measured**, and
  `assess_retrofit_level` may paginate exactly the way `audit_intent_spec` does. Re-measure or
  re-word. Treat every remaining number in that README as unverified until it is re-run.

### Tier 2 — the two structural gaps from the Nate cross-check

- **DECISION TICKET: how the "what would break" line reaches the page.** Nate's third
  judgement slot — *"the blast radius question, and it's the one that separates people who
  understand their systems from people who happen to have working systems"* — has no home in
  our grammar. All 25 catch panels are backward-looking found-and-fixed defects; none states a
  live, knowingly accepted risk. Five options are costed in the plan doc (§5): re-aim catch
  supports · fold into the system panel · a sixth `risk` panel (spec change, and it touches
  Code Brain's ruled page) · one line under the band · link-only. **My ruling is that
  link-only is insufficient** — see the next ticket — so the answer is one of the first four
  or a fifth idea. This one is genuinely open; resolve it as a decision before executing.
- **DECISION TICKET: how EXPLANATION.md files get surfaced without a dig.** My constraint,
  verbatim: *"a lot of recruiters don't want to constantly dig to find something that could be
  right in front of them."* A link to a markdown file in a GitHub repo is a dig. Decide the
  surfacing mechanism — a `live`-style meta row, an on-page section, an /info entry, something
  else — then execute it. Depends on the previous ticket's answer.
- **Write the three missing EXPLANATION.md files:** `agent-fleet-observability`, `anima`,
  `groundwork`. Each answers the 4Q — what is this / why this approach and what did you choose
  not to build / **what would break** / what did you learn. Note the leverage: answering Q3 for
  these three is the exercise that *produces* the accepted-risk sentences the panels need, so
  sequence these before or alongside the Risk-slot execution, not after.
- **Link the two that already exist:** `sw-mcp-intent-engineering/docs/EXPLANATION.md` and
  `code-brain/evals/vault-synthesizer/EXPLANATION.md`. Both cite the 4Q framework by name and
  neither is reachable from its project page.

### Tier 3 — make the pages stop under-selling

- **Re-open all six `descriptionStatus: 'approved'` descriptions.** They predate the panels and
  several now say less than the panels do. **Groundwork is the worst case:** its description
  never says it is an OS *for a company's agents*, nor that it was tested against agent personas
  on six models with a nine-item answer key. Per-project: decide the new sentence, write it, and
  set `descriptionStatus` honestly. Driftgate's description is not re-opened.
- **Groundwork: make the persona-company evidence visible.** The `1 of 9` catch panel points at
  `github.com/seanwinslow28/groundwork`, which does not contain the run. The apparatus lives in
  a separate repo `~/Code-Brain/persona-company` (7 personas, 9 plants, frozen answer key,
  mode-444 frozen session log, scorecard, findings, audit). Decide what gets published — the
  whole apparatus, a sanitized run report, or a summary — respecting the privacy rules, then do
  it so the panel has somewhere to land.
- **Anima has no animation on it.** Best evidence base of the five projects and the page shows
  none of its output. The `7 frames, 0 retries` panel describes a loop that exists in the repo's
  `renders/`. Get something moving onto the page within the byte grant.

### Tier 4 — make the numbers better rather than just true

- **Groundwork run 2. Highest-value item on this map.** Run 1 (2026-07-31) scored `1 of 9` and
  the findings were routed back as design changes — the evidence-floor spec through four Codex
  rounds is that work. There is no *after*. A second run against the persona company, measured
  the same way, turns the catch panel from "found a flaw" into found → redesigned → re-measured,
  which is the complete judgement loop and would make Groundwork the strongest page on the site.
  Sized as its own multi-session sub-effort if needed. Whatever it scores is the number we
  publish, including if it does not move.
- **Vault Evals: the documented two-line fix.** `vs-016`/`vs-017` are red because the empty mock
  retriever in `runner.py`'s `_invoke_synthesizer` collides with the Tier 1.5 thin-source gate
  (`_MIN_SIMILAR_FOR_LLM=2`), so the gate skips the LLM call and `STATUS_ERROR` never reaches the
  assertion. The fix is named in the suite's own README. Moves `10 of 14` honestly. Update the
  panel's number and date if it lands.
- **Intent MCP: `--whole-file` audit aggregation.** Named as a known gap in the 2026-08-28
  CHANGELOG entry rather than quietly shipped. Grading a document longer than `max_length`
  currently means walking every chunk by hand, and a chunk that omits a section is not evidence
  the section is absent. This is the feature whose absence caused the bad claim.

### Housekeeping

- **Correct the record in git.** `seanwinslow.com` commit `e3e2bb3`'s message asserts the
  SKILL.md "scores 1/25 because its nine section headings sit inside code fences." Both the
  number and the cause are wrong — it was my own `max_length` misuse against a 32k file. The
  tickets file already carries the correction; decide whether the site repo needs a follow-up
  note commit and add one if so. `projects.ts` itself needs no change: `118 skills` remains
  correct for that panel because `23 of 25` still does not reproduce.

## What "done" looks like

The map is complete when every ticket above is closed, the five pages' claims each have a
one-command or one-click reproduction, the Risk slot has a decided and executed home, and the
site gates are green. Print the frontier and give me the one-line kickoff for the first
frontier ticket.
