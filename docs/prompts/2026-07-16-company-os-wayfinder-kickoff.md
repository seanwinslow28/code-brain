# groundwork — Session 2 kickoff: /wayfinder charting

> Continuation of the Company OS portfolio project. Session 1 (2026-07-15/16) completed the brainstorm + research + hardening: the approved design brief is the single source of truth. This session's ONE job is charting. Paste everything below into a fresh Fable 5 session in `/Users/seanwinslow/Code-Brain/code-brain`.

---

This is Session 2 of the **groundwork** Company OS project (company-agnostic, agent-installed Company OS repo — my flagship portfolio project). Session 1 produced a fully-hardened design brief; your single job this session is **/wayfinder charting**: turn the brief into a public wayfinder map + decision tickets on the NEW repo's issue tracker. Per wayfinder's one-session-per-phase rule, do NOT scaffold the product, write product code, or start working tickets — charting only.

### Step 0 — Invoke the wayfinder skill first

Invoke `/wayfinder` before anything else and run the whole session inside its charting flow.

### Step 1 — Load the source of truth (read fully before charting)

1. `docs/plans/2026-07-15-company-os-design-brief.md` — **the approved design brief.** Read all of it, including Appendices A–E (seed-thesis verdicts, three research-provenance appendices, and the fusion-discovery pain-point gate). Every design decision below is already made and evidence-backed; do not re-litigate them — chart them.
2. `vault/20_projects/research/2026-07-16-company-os-org-adoption-pm-idea-ledger.md` — the verified pain-point ledger (5 pains, evidence URLs) the design was final-checked against.
3. For history only, the original kickoff: `docs/prompts/2026-07-15-company-os-brainstorm-kickoff.md`.

Key decisions already locked (details in the brief): wedge = ontology-first generation + compiled governance + governed self-improvement; multi-harness = convention not tooling (AGENTS.md canonical, one-line CLAUDE.md import, .cursor/rules pointers, skills as work packages); git-native with one AI-Ops maintainer; 8 ontologies / 3 deep functions (CS, Product, HR-or-Finance); ~20-person B2B SaaS demo company; machinery in V1, compliance pack + truth layer in V2; org memory = typed schema + draft-PR proposal gate, zero engines; lead name **groundwork**.

### Step 2 — Create the public repo FIRST

Before drawing the map: check GitHub name availability for `groundwork` under my account (`seanwinslow28`; fallback order: `quartermaster`, `charter-os`, `keel` — brief §10). Create the **empty public repo** (README stub + license placeholder at most — no scaffolding). The wayfinder map and all decision tickets live on the NEW repo's tracker, not code-brain's — a visible public map of decisions-in-progress is itself portfolio evidence of process. Confirm the name with me before creating if `groundwork` is taken.

### Step 3 — Chart

- **Destination statement:** start from the candidate in brief §11 and refine it with me.
- **Decision tickets:** brief §11 lists **17 open decisions phrased as sharp questions** — these become the map's decision tickets on the new repo's tracker. Preserve their sharpness; add anything charting itself surfaces.
- **Not-yet-specified entries:** brief §11's foggy areas (delivery-recipe shape, drift-flow mechanics, truth-layer schema, enterprise posture, scoreboard measurement, skill auto-invocation reliability).
- Wayfinder subsumes `/grill-with-docs` — grill me against the brief wherever the map needs a decision sequenced or a dependency made explicit. Use AskUserQuestion at real forks only.

### Step 4 — Wrap

Update the Company OS ticket in `vault/00_inbox/tickets.md` (Session 2 done, map URL, first ticket to work in Session 3). Commit prompt/doc changes in code-brain on a feature branch as usual. Sessions 3+ work the map **one ticket per session**; build sessions use Fable 5 with the Codex plugin as the review gate (`/codex` review or `codex:codex-rescue`) — note it on the map, don't act on it now.

### Constraints

- Charting only. No product scaffolding beyond the empty repo + tracker + map artifacts wayfinder itself requires.
- Never re-open Session 1's locked decisions without new evidence; the brief's appendices are the evidence record.
- Honesty rules carry over: the map must reflect what research actually verified (including the prior-art concessions in brief §2).
