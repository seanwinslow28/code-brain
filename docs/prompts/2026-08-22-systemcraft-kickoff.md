# Systemcraft kickoff — research passes, then Wayfinder

Copy everything below the line into a fresh Claude Code session at the Code-Brain repo root.

---

We're building **Systemcraft** — an AI PM system design studio, ratified in a creative-partner session on 2026-08-22. Nothing has been built yet. Your job this session: run the two research passes that gate the build, get my ratification on the findings, then open the `/wayfinder` session that charts the build map. Do not scaffold any folders, agents, or skills before the Wayfinder map exists.

## Read first (in this order)

1. The Systemcraft ticket in `vault/00_inbox/tickets.md` (auto-injected at session start — find the bullet starting "**Systemcraft (AI PM system design studio) — RATIFIED 2026-08-22**").
2. The partner-session sidecar at `~/.creative-harness/partner-sessions/2026-08-22-ai-pm-system-design-superpowers.md` — the full decision record with all ten locks and the proposals that lost. It is local-only and must never be committed or quoted into tracked files.

## Ratified decisions (binding — do not re-litigate; new ideas may extend them)

- **L2 — Mandate:** full practitioner, not reviewer. The studio strategically plans, executes, and builds AI PM system design work, and explains each choice briefly (why A over B) so Sean learns by demonstration. Sean's separate NotebookLM curriculum is out of scope for this build.
- **L3 — Form:** a full studio workspace — corpus library + master skill (portable interface) + specialist agent bench + artifact templates + an accreting decision ledger.
- **L4 — Scope:** real-work-primary, dual-surface. Four engagement types: design new projects, audit/improve existing ones, support landing a new role, serve future employer work. Job-hunt artifacts are cut from real ledger entries, never hypotheticals.
- **L5 — Bench (baseline hypothesis):** five lifecycle seats — Design Strategist (framing, PRDs), Architecture Advisor (model/pipeline choices, ADRs), Interaction & Trust Designer (failure UX, trust, control), Evals & Evidence Architect (golden datasets, metrics, LLM-judge design), Ops & Economics Modeler (unit economics, rollout, kill switches, drift, runbooks). Each seat drafts AND audits in its lane. A sixth Red-Team seat is an open question.
- **L6 — Corpus:** two-layer (free canon + purchased books via book-to-skill, https://github.com/virgiliojr94/book-to-skill.git), **both layers private** — the entire corpus lives gitignored/local-only. Seed from research on hand, then the best-books pass, then ongoing discoveries.
- **L7 — Bench validation gate:** the five-seat roster is ratified, grown, or shrunk against a research pass on how others compose agent teams — before build.
- **L8 — Boundary:** public machinery, private brain. Agent definitions, skill scaffold, templates, README are tracked publicly as portfolio evidence; corpus AND decision ledger are gitignored local-only (extend the PRIVATE LAYER block in `.gitignore`); seats must degrade gracefully when the private lane is absent.
- **L9 — Name/location:** root workspace `systemcraft/`, sibling to `agent-fleet-observability/`, own CLAUDE.md, wired into `scripts/validate.py`. Public subtitle: "an AI PM system design studio."
- **L10 — First engagement:** five-seat audit of the agents-sdk fleet's knowledge loop (flush → synthesizer → critic → lint → consumer hooks). The-oracle full-lifecycle design pass is the natural second engagement.

## This session's work

**Phase 1 — two research passes ($0 lanes first; paid research only with my explicit cost confirmation):**

1. **Bench composition** — how do practitioners compose and optimize multi-agent specialist teams (roster size, role boundaries, orchestrator patterns, red-team seats, common failure modes)? Fresh field practice matters here, so `last30days` is a good fit alongside web research. Deliverable: a findings brief with a concrete recommendation — confirm the five seats, add, or cut — with evidence per change.
2. **Best books** — which books earn purchase for the private corpus, in what order? Candidates already on the table: Chip Huyen's *AI Engineering*, Marily Nika's *Building AI-Powered Products*, Aminian & Xu's *Machine Learning System Design Interview*. Validate or beat these; also flag the strongest free canon (PAIR Guidebook, Amershi guidelines, Hamel Husain and Eugene Yan on evals, applied-llms.org) for the free layer. Deliverable: a ranked purchase list with a one-line case per book.

Research reports land in `vault/20_projects/research/` per house convention (findings are fine to track; book *content* later is not). Present both briefs to me in plain language and wait for my ratification of the final roster and book list — I'm the decider on both.

**Phase 2 — Wayfinder:**

After ratification, start `/wayfinder` to chart the Systemcraft build map. The map should cover at minimum: workspace scaffold + validate.py blessing + .gitignore PRIVATE LAYER extension; the master skill; the ratified bench (agent definitions with explain-why behavior baked in); artifact templates; decision-ledger schema (private lane); corpus pipeline (free layer + book-to-skill private layer, graceful degradation when absent); README as portfolio surface; and the first engagement (the fleet knowledge-loop audit) as the closing milestone.

## Standing constraints

- Never `git add` corpus or ledger content; book-derived text never lands in tracked files. Public repo — assume every tracked file is read by a recruiter.
- Run `python3 scripts/validate.py` after structural changes; new skills/agents get CHANGELOG.md entries and count-table updates per CLAUDE.md.
- I'm a PM, not a dev — define terms and trade-offs in plain language before asking me to decide, and give me a recommendation with every question, one question at a time.
