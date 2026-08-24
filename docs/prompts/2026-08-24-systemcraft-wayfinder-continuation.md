# Systemcraft continuation — work the build map, next ticket: Artifact templates

Copy everything below the line into a fresh Claude Code session at the Code-Brain repo root.

---

/wayfinder 142 — artifact templates

Context for this session (the map is canonical — load it first, per the wayfinder skill):

We are mid-way through the **Systemcraft build map** (GitHub issue #142) — the wayfinder map for Systemcraft, the AI PM system design studio at root workspace `systemcraft/`. **Every decision ticket on the map is closed and ratified**; only build work remains. Read the map's Decisions-so-far index and zoom into closed tickets as needed — do not re-litigate anything there.

**This session's ticket: Artifact templates (#152, prototype, HITL).** Draft the five artifact templates for me to react to, one per seat contract (ratified in Seat artifact contracts, #144):

1. **PRD** (Design Strategist) — must carry the required **"Evaluable success criteria"** section that the Evals & Evidence Architect co-signs at framing time (the dual-touch amendment).
2. **ADR** (Architecture Advisor) — options with rough cost implications per the contract.
3. **Failure-UX spec + model card** (Interaction & Trust Designer).
4. **Eval plan** (Evals & Evidence Architect) — golden datasets, metrics, LLM-judge design, holdout hygiene, plus the measurements launch gates read (thresholds belong to Ops).
5. **Ops/economics model + incident runbook** (Ops & Economics Modeler) — unit economics, rollout, launch criteria, kill switches, drift.

House rules for the templates: they land in `systemcraft/templates/` as **public machinery** — recruiter-readable, zero private content; siblings `ledger-entry.md` and `red-team-protocol.md` are already there (match their tone: brief, to the point — I ratified a "brevity law" for the ledger and I like that register everywhere). Draft as DRAFT-marked files, present the shape to me compactly for reaction, commit only after I ratify, then resolve/close the ticket and update the map per the wayfinder skill (resolution comment → close → Decisions-so-far line). Run `python3 scripts/validate.py` after structural changes. One ticket per session.

**Board state after this ticket:** remaining build tasks are Author the five-seat bench (#153), Free-canon layer build (#154), Book ingestion (#155 — EPUBs ready at `~/Books/systemcraft/`, slug-named), README as portfolio surface (#156), then the closing milestone First engagement: fleet knowledge-loop audit (#157, waits on #152 + #153 + #154).

Standing constraints: public repo — never `git add` corpus/ledger/book content (guard rules exist: `systemcraft/{corpus,ledger,books}/`, `*.epub`); I'm a PM, not a dev — plain language, recommendations with every question, one question at a time; local commits on main may be unpushed — push is my call.
