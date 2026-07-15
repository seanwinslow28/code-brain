# groundwork — Company OS Design Brief

**Date:** 2026-07-15
**Session:** Brainstorm + research (Session 1 of the Company OS portfolio project; kickoff prompt at `docs/prompts/2026-07-15-company-os-brainstorm-kickoff.md`)
**Status:** Approved design brief. No code or scaffolding exists yet — next session is `/wayfinder` charting.

---

## 1. Product thesis (one sentence)

An open-source, harness-agnostic repo that interviews your company about the work each function actually does — what should get **more** human time, what should get **automated away** — and generates your operating system from that map: folder-per-function structure, skill files, governance, and a provisioning path, adoptable in an afternoon with zero credentials.

Working name: **groundwork** ("the groundwork your company runs on"). Runner-up candidates in §9.

---

## 2. White-space statement & differentiation

### The honest headline

The agent-led-interview mechanic is **already shipped, at small scale**. This brief does not claim it as virgin territory:

- [dswh/company-os](https://github.com/dswh/company-os) (~24 stars, last push 2026-06-19) describes itself verbatim as a *"self-installing AI-native company operating system seed repo"* — the agent reads `INSTALL_FOR_AGENTS.md`, interviews the adopter, and generates a company brain + department loops. Thin function coverage, governance mostly punted, no traction.
- [Workflowsio/company-os-starter-kit](https://github.com/Workflowsio/company-os-starter-kit) (~74 stars, Dan Rosenthal/workflows.io, MIT) documents "Option B: *Interview me about my business and help me fill everything in*" — but as a suggested prompt over `{{placeholder}}` fill-in of a fixed CLAUDE.md, GTM-skills-only, Claude-Code-only.
- [garrytan/gbrain](https://github.com/garrytan/gbrain) (~26.3K stars) proved agent-driven install at scale — for a knowledge/retrieval brain, not an operating system of functions, skills, and governance.
- Anthropic's own `/init` (with `CLAUDE_CODE_NEW_INIT=1`) is normalizing interview-then-generate natively — but codebase-scoped, not company-scoped ([memory docs](https://code.claude.com/docs/en/memory)).

### The verified open lane

Nobody with traction combines the four things groundwork leads with:

1. **Ontology-first generation.** Every existing repo is template fill-in or a static skill library ([w95/awesome-claude-corporate-skills](https://github.com/w95/awesome-claude-corporate-skills) 166 skills, [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) 345, [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills) 343 — the content layer is commoditized). Nobody implements JZ's actual Layer 1: map each function's work into up/down columns (more human time vs automate away) and **derive** the folder structure and skills from that map. The ontology is the unclaimed part of the architecture, and it is the PM-judgment part.
2. **Governance and adoption as first-class content.** Governance was the least-covered criterion across all seven direct-hit prior-art repos. Meanwhile the live pain is exactly here: r/cscareerquestions, 811 pts / 157 comments — *"My company have tried giving Claude code to non technical people and things already broke"*; MindStudio: non-technical teams get "setups built by engineers, with zero documentation… skills go unused… people fall back on chat." groundwork ships the captain model, two-track review, 4-level maturity self-assessment, AI-Ops role definition, and (V2) hackathon playbook as content, not afterthoughts.
3. **Multi-harness by convention** (§5). Only [getnao/sylph](https://github.com/getnao/sylph) (165 stars, YC-backed nao Labs) claims multi-harness today, and its setup is per-skill configuration, not an ontology interview.
4. **Structural enforcement.** No prior-art repo ships a validator or a synthetic demo company. groundwork ships both.

### Named competitors and how groundwork differs

| Against | What they are | groundwork's difference |
|---|---|---|
| Aakash Gupta's PM OS / Team OS ([pm-os](https://www.news.aakashg.com/p/pm-os), [team-os-cc](https://www.news.aakashg.com/p/team-os-cc)) | Paid, closed, copy-paste kits: PM OS $49 one-time / $250 founders (41 skills, 7 sub-agents, manual checklist setup); Team OS paywalled with a "1-command conversion" skill | Open source and free; interview → generation instead of manual copy; company-scale from the start |
| JZ's Laurel Company OS ([company-os-jz](https://www.news.aakashg.com/p/company-os-jz) — free editorial, **no downloadable product**) | One company's real, working OS, described but not shipped | groundwork generalizes the architecture Laurel proved (ontology → skills → delivery, captain model, two-track review, maturity levels) into something any company can install. Laurel needed a dedicated human (Sasha, AI Ops) to build theirs; groundwork's interview is that consultant, packaged |
| GitHub prior art (dswh, Workflowsio, Sylph, [clawcompany](https://github.com/Claw-Company/clawcompany) 580★, [beevibe](https://github.com/beevibe-ai/beevibe) 381★) | Seed repos, template kits, agent-role infra | Interview depth + ontology derivation + governance content + validator + demo company; positioning risk: Sylph and clawcompany are active — differentiation must never rest on "company OS repo" or "agent sets it up" alone |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (~22.8K stars, 11 function plugins) | Generic per-function content, manually customized | Company-specific generation; ontology and governance layers Anthropic's plugins don't attempt; groundwork's generated skills can *coexist* with these plugins |
| Dust ($30–150/seat/mo credit-metered) / Glean (sales-led, ~$60K/yr floor) | Hosted per-seat agent platforms | groundwork ships only files into the company's own repo; execution rides whatever harness the company already pays for; git is the source of truth; $0 incremental |

### Delivery mechanism is real and documented

Org owners upload zipped SKILL.md folders → provisioned **default-on to every employee** in Claude chat/Desktop/Cowork (Team & Enterprise plans; [help center](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization), [Anthropic blog 2025-12-18](https://claude.com/blog/organization-skills-and-directory)). groundwork's generated output is SKILL.md-conformant, so it is directly zip-and-provision compatible — the delivery layer without building delivery software.

---

## 3. Target adopter & adoption story (the first hour)

**Adopter:** the "Sasha" — a founder, COO, CPO, or designated AI-Ops person at a ~10–200 person company. Possibly non-technical. They heard the Company OS idea (the JZ episode has 36.6K views in 3 weeks; copycat content is spawning weekly) and want it without a paid kit or a platform contract.

**First hour:**

1. Open the repo folder in whichever harness they use (Claude Code, Cowork, Codex, Cursor). README's first section is the RevCoach move: **"Not technical? Point your agent at this repo"** — the agent reads the canonical instructions automatically.
2. The agent offers the **demo walkthrough** first: a synthetic ~20-person B2B SaaS company ships pre-installed in `demo/`, so the adopter watches the whole OS work end-to-end — morning-briefing skill, CS renewal prep, PM feature-request triage — with zero credentials and zero real data.
3. The adopter starts the **interview**: structured, resumable (state saved to a file so it survives sessions and harness switches), organized as ontology-first — *What functions exist? What does each do repeatedly? What should humans do MORE of? What should stop being manual?* The interview's skeleton is an adaptation of the intent-engineering 9-section spec (objective, outcomes, health metrics, constraints, autonomy, edge cases, stop rules) applied to an organization instead of an agent.
4. The generator writes `your-company/`: folder-per-function structure, per-function ontology files (up/down columns), starter skills instantiated from the schema, a constitution-style root instruction file with routing tables, and the multi-harness file set (§5).
5. `validate` passes (structure, referential integrity, no secrets, no drift between harness files).
6. The adopter zips the generated skills and uploads to Claude org settings → every employee has them by default. Done in an afternoon.

`demo/` and `your-company/` stay strictly separated, and committed content is synthetic-only — both conventions inherited from RevCoach.

---

## 4. Scope ladder (each version earns its complexity)

**V1 — adoptable in an afternoon:**
- The interview (agent instructions, resumable state file) + generator templates
- Starter ontologies for **8 functions** (sales, CS, marketing, product, engineering, finance, legal, people/HR), each with up/down columns — breadth is cheap and differentiating at the ontology layer
- **3 deep functions** with fully-worked exemplar skills wired through the demo company: **Customer Success** (renewals, session prep, handoffs — the strongest narrative link to the Laurel source), **Product/PM** (feature-request triage, PRD drafting — Sean's earned judgment), and **People/HR or Finance** (least-served functions in all prior art; final pick is a wayfinder decision ticket, leaning People/HR for its resonance with onboarding/adoption content)
- A **skill-file schema/spec** + the authoring standard (progressive disclosure, description-as-selection-surface) so generated skills are well-formed — not 200 half-baked ones
- **Governance docs:** captain model, two-track review, 4-level maturity self-assessment, AI-Ops role definition
- **Multi-harness file set** (§5) and the **validator**
- Synthetic demo company, honest Known Limitations, security/privacy section, versioned roadmap — the full RevCoach finished-artifact bar

**V2 — earns its complexity if adopters finish V1's interview:**
- Delivery layer as *recipes*: org-skills provisioning walkthrough (zip → org settings), morning-Slack-briefing pattern (calendar item → the right skill next to it)
- Hackathon playbook; maturity assessment as a runnable skill
- Second demo company (services agency) to prove company-agnosticism

**V3 — earns its complexity if the OS survives contact with month two:**
- Re-interview / drift flow (the org changed; regenerate without clobbering local edits)
- Per-function deepening passes; scoreboard/metrics for adoption

Deliberately **not** on the ladder: hosted anything, dashboards, per-seat features, an agent runtime. groundwork is files.

---

## 5. Multi-harness strategy: convention, not tooling

Verified mechanics (primary docs):

- **Codex and Cursor read `AGENTS.md` natively** ([agents.md](https://agents.md/) — Linux Foundation-stewarded, 60K+ projects; Cursor also supports nested AGENTS.md).
- **Claude Code does *not*** — docs verbatim: *"Claude Code reads CLAUDE.md, not AGENTS.md"* — but sanctions a one-line `@AGENTS.md` import ([memory docs](https://code.claude.com/docs/en/memory)).
- **Cursor scoped rules** require `.mdc` files in `.cursor/rules/` (plain `.md` there is ignored).
- **Cowork** reads CLAUDE.md-style folder instructions (help-center documented at lower confidence — a verification ticket).

**The convention:** `AGENTS.md` is the single canonical instruction source, committed alongside a permanent one-line `CLAUDE.md` that imports it, plus a small `.cursor/rules/` set pointing back. The interview writes all of them once; there is **no compile script and no build step**. Drift between the files is a **validator check**, not a build problem. Skills ship in SKILL.md format (Anthropic frames it as an open standard; ecosystem cross-installation into Codex/Cursor/Gemini is reported but needs first-party verification — decision ticket).

---

## 6. What ports from code-brain (and what deliberately does not)

From the machinery audit of this repo:

| Ports | As what |
|---|---|
| `intent-engineering` 9-section template + retrofit levels | The interview's skeleton — the questions to ask an org about any function it wants to encode; Objective/Outcomes/Health-Metrics is the anti-Goodhart spine of the ontology |
| `scripts/validate.py` architecture (per-concern checks → errors/warnings gate; referential integrity; secret scan) | Rewritten config-driven: expected domains/functions come from the generated org config, not hardcoded constants, so one validator validates any company |
| `skill-system-mastery` authoring standard (progressive disclosure, description = selection surface, negative triggers) | The skill-file schema/spec governing every generated skill |
| Root `CLAUDE.md` skeleton (constitution of non-negotiable rules + routing tables + live-count inventories + tickets protocol) | The generation target — what the root instruction file of a generated OS looks like |
| Security-hook profile + "hooks enforce; subagents judge" doctrine | Optional Claude-Code-only extra profile; the doctrine ships as governance content, with cross-harness enforcement honestly listed under Known Limitations |
| `install.sh` preset→export-group→canonical-store pattern | As a *design pattern* for generation (selection separated from content; prose fragments assembled into the root file) — not the bash implementation |

**Deliberately not ported:** the agents-sdk autonomous layer, Obsidian vault, launchd scheduling, LLM council / research APIs, personal domain content, and the export-groups/presets machinery itself (a single-product repo doesn't need preset selection).

---

## 7. Portfolio surfaces

1. **The GitHub repo** — public from day one. **Create the empty repo early** (next session), because the wayfinder map of decision tickets lives on the *new repo's* issue tracker, and a visible map of decisions-in-progress is itself portfolio evidence of process.
2. **Website walkthrough** à la RevCoach (later; after V1 is real).
3. **Substack post candidate:** "I read how Laurel runs on a Company OS, then built the version any company can install" — feeds the substack-value-engine pipeline.
4. The hiring-CPO signal throughout: ontology + governance + honest limitations + versioned roadmap where each version earns its complexity — the things that read as "this person gets it" rather than "template dump."

## 8. Process (build sessions)

- Session 2: `/wayfinder` charting only — brief → map + decision tickets on the new repo's tracker (subsumes `/grill-with-docs`). Sessions 3+: work the map one ticket per session, then scaffold/build under `/Users/seanwinslow/Code-Brain/`.
- Build phases use **Fable 5 with the Codex plugin as the review gate** (`/codex` review or `codex:codex-rescue`) — noted here per kickoff; not exercised this session.

## 9. Name candidates & new-project layout

**Lead: `groundwork`** — "the groundwork your company runs on"; evocative of the ontology-first layer, no AI-hype odor. Runners-up: `quartermaster` (the officer who provisions the ship), `charter` / `charter-os` (constitution language matching the governance wedge; crowded word), `keel` (the spine a ship is built on; needs a tagline). GitHub availability check is a wayfinder ticket.

**Location:** `/Users/seanwinslow/Code-Brain/groundwork/` (sibling to `code-brain/` and `CB-RevCoach-Brief/`).

**Proposed top-level layout:**

```
groundwork/
├── README.md              # positioning + "Not technical? Point your agent at this repo"
├── AGENTS.md              # canonical agent instructions (navigation + interview entry)
├── CLAUDE.md              # one line: @AGENTS.md import
├── .cursor/rules/         # .mdc pointers back to AGENTS.md
├── interview/             # interview flow, question banks, resumable state conventions
├── ontologies/            # 8 starter function ontologies (up/down columns)
├── skills/                # skill-file schema/spec + worked exemplar skills (SKILL.md format)
├── governance/            # captain-model, two-track-review, maturity-model, ai-ops-role
├── delivery/              # org-skills provisioning guide; (V2) morning-briefing recipes
├── demo/                  # synthetic ~20-person B2B SaaS company, OS pre-installed
├── your-company/          # empty target the generator fills (gitignored content?  → ticket)
├── scripts/validate.py    # config-driven structure/integrity/secrets/drift gate
└── docs/                  # known limitations, security/privacy, roadmap, decision records
```

---

## 10. Wayfinder handoff

**The wayfinder map lives on the NEW repo's issue tracker** — create the empty `groundwork` repo at the start of Session 2 so the map is public from day one.

### Candidate Destination statement

> Any company can point its coding agent at this repo and, within an afternoon, get a governed, multi-harness Company OS derived from its own work ontology — judgment built in, not bolted on.

### Open decisions (future decision tickets, phrased sharp)

1. **Third deep function:** People/HR or Finance — which one, and why does the demo narrative need it?
2. **Name & availability:** is `groundwork` free on GitHub (org or user namespace)? Fallback order among quartermaster/charter/keel?
3. **License:** MIT (RevCoach precedent) or Apache-2.0 (knowledge-work-plugins precedent)?
4. **Interview state format:** one resumable state file vs per-phase artifacts — what survives a harness switch mid-interview?
5. **SKILL.md portability:** verify first-party how Codex/Cursor/Gemini actually load SKILL.md-format skills today — what degrades, and what does the README promise?
6. **Cowork behavior:** confirm folder-instruction + skills loading in Cowork against current docs (documented at low confidence today).
7. **Governance docs: generated or worksheet?** Does the interview customize the captain model / two-track review per company, or do they ship static with fill-in worksheets?
8. **Hooks profile scope:** does V1 ship the optional Claude-Code security-hook profile, or does that wait for V2?
9. **`your-company/` git semantics:** committed to the adopter's fork? gitignored? Template-branch pattern?
10. **Attribution framing:** how prominently to credit JZ/Laurel and Aakash's episode as inspiration, and whether to acknowledge dswh/company-os as prior art in the README (recommended: yes — honesty is the brand).
11. **Sylph positioning:** what does the README's comparison section say about Sylph and clawcompany without punching down?
12. **Validator language:** Python stdlib (code-brain precedent) vs Node (RevCoach stack) — which does a non-technical adopter more likely have?

### Not yet specified (foggy areas)

- Delivery-layer V2 shape: Slack morning briefing as recipes/docs only, or a reference implementation? (JZ's warning about scheduled-task overload applies.)
- Re-interview / drift flow (V3): how regeneration merges with local edits.
- Metrics/scoreboard: what "adoption is working" looks like in files.
- Enterprise security profile and data-boundary guidance beyond the RevCoach-style privacy conventions.
- Whether the demo company's synthetic data needs a verifiable "all-fake" convention like RevCoach's `samples/` rule (likely yes).
- How groundwork coexists with anthropics/knowledge-work-plugins in the same org (complement, not compete — mechanics unspecified).

---

## Appendix A: seed-thesis verdicts (pressure-tested against research)

1. **"The wedge is the installer, not the template" — partially overturned.** The installer mechanic is already claimed (dswh/company-os verbatim; gbrain at 26K★; Anthropic's `/init` normalizing it natively). The wedge moved one layer up: the **ontology interview + governance content** are the product; the installer is the delivery vehicle. Competing on interview UX alone is the lane where groundwork gets out-shipped fastest.
2. **"Generator + exemplars, not filled-in content" — confirmed, sharpened.** Static skill content is commoditized (166–345-skill libraries exist). Sharpened to: 8 ontologies broad, 3 functions deep.
3. **"Synthetic demo company" — confirmed.** No prior-art repo ships one; the RevCoach move transfers directly. ~20-person B2B SaaS.
4. **"Multi-harness by design" — confirmed, but as convention, not tooling.** Research killed the compile-script version: the sanctioned `@AGENTS.md` import + native AGENTS.md reading in Codex/Cursor means the whole story is three committed files plus a validator drift-check. Only Sylph competes here.
5. **"Governance and adoption are content" — strongly confirmed.** The least-covered criterion in every prior-art repo and the loudest practitioner pain. Elevated from "content, not afterthought" to co-headline of the wedge.
6. **"Maturity path for the repo itself" — confirmed.** Delivery-layer integrations are V2+; JZ's own scheduled-task-overload warning reinforces not shipping automation in V1.

**What the theses missed (found in brainstorm):** the org-skills provisioning path (zip → default-on org-wide) makes the delivery layer nearly free; the intent-engineering 9-section spec is a ready-made interview skeleton; and `awesome-claude-code` (~50K★) has no company-OS category — a listing there is a cheap, high-visibility distribution move.

## Appendix B: research provenance (this session)

- **last30days** (2 passes, 2026-06-15→07-15): Company OS content wave 3 weeks old, epicentered on the JZ episode (36.6K views); "interview me" pattern in the air (Chase AI, 83K views); governance failure is the loudest practitioner pain (r/cscareerquestions 811 pts); raw data at `~/Documents/Last30Days/company-os-team-os-claude-code-raw.md` and `claude-code-skills-for-non-engineering-teams-raw.md`.
- **Prior-art agent A** (Aakash products, Anthropic org skills, Dust/Glean): PM OS $49/$250 paywalled copy-paste kit; Team OS paywalled; company-os-jz free editorial, no product; org-skill provisioning documented (owners upload SKILL.md zips, default-on org-wide); knowledge-work-plugins ~22.8K stars, no interview/ontology/governance.
- **Prior-art agent B** (GitHub landscape, multi-harness conventions): dswh/company-os is the verbatim prior claim (24★); Sylph (165★, YC) the strongest complete competitor; clawcompany 580★ template-selection; AGENTS.md Linux-Foundation-stewarded, 60K+ projects, **not** read natively by Claude Code (`@AGENTS.md` import sanctioned); Cursor reads AGENTS.md natively + `.mdc` scoped rules; awesome-claude-code (~50K★) has no company-OS category — a visibility gap.
- **Machinery audit** (this repo): installer pattern, validator architecture, skill-authoring standard, intent-engineering template, hook doctrine, CLAUDE.md skeleton — portability judgments in §6.
