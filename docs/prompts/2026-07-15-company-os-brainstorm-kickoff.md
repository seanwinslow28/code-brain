# Company OS — Brainstorm + Research Kickoff (Session 1 of N)

> Paste-ready kickoff for a fresh Fable 5 session in `/Users/seanwinslow/Code-Brain/code-brain`.
> Session 1 goal: turn a seed idea into a locked design brief. No code, no repo scaffold yet.
> Session 2 (separate, after this): `/wayfinder` charting — the brief's Destination + open questions become
> the map and its decision tickets (wayfinder's charting/resolution already runs `/grilling` +
> `/domain-modeling`, so a separate `/grill-with-docs` session is subsumed). Sessions 3+: work the map,
> one decision ticket per session, until the way is clear — then scaffold + build.

---

## PASTE EVERYTHING BELOW THIS LINE

I want to design a new portfolio project: a **company-agnostic Company OS** — an open-source GitHub repo any company can adopt, where an AI harness (Claude Code, Claude Cowork, Codex, Cursor — whichever they use) reads the repo, interviews the adopter about their organization, and generates their company's operating system: folder-per-function structure, ontology, skill files, delivery layer, and governance. This session is brainstorm + research only. The output is a design brief, not code.

### Step 0 — Invoke the brainstorming skill first

Invoke `superpowers:brainstorming` before anything else, and run this whole session inside it. Weave the research (Step 2) into the brainstorm wherever the skill's flow allows — don't treat them as strictly serial phases.

### Step 1 — Read these before forming opinions

1. `vault/00_inbox/How-to-Build-a-Company-OS-in-Claude-Code-with-Jiaona-Zhang.md` — the inspiration. Aakash Gupta's article + full YouTube transcript: Jiaona Zhang (CPO, Laurel) walks through the Company OS Laurel actually runs. Extract the load-bearing architecture: (a) one GitHub repo, folder per function, activity folders, skill file per activity, skills uploaded to Claude org settings; (b) the three build layers — ontology first (map every function's work; what goes UP in human time vs what gets automated), then skill files, then the delivery layer (morning Slack briefing that surfaces the right skill next to each calendar item); (c) governance — the captain model + two-track review (fast track vs product-strategy/architecture review); (d) adoption — dedicated AI Ops person, companywide hackathon, culture-as-workflow ("unreasonable hospitality" codified); (e) the 4-level AI-maturity framework (chat → workflow automation → apps → shared apps/shipping) and the screen-share test.
2. `/Users/seanwinslow/Code-Brain/CB-RevCoach-Brief/README.md` and its `CLAUDE.md` — my finished-artifact bar for portfolio repos. Note the pattern I want to reuse: "Not technical? Point Claude at this repo" agent-guided walkthrough, synthetic demo data so it runs with zero credentials, mock-first adapters with real connectors behind interfaces, honest Known Limitations, security/privacy section, versioned roadmap where each version must earn its complexity.
3. This repo's own machinery, as prior art to potentially port: `scripts/install.sh` + `export-groups/` + `presets/` (skill-export model), `scripts/validate.py` (structure enforcement), `.claude/skills/skill-system-mastery/SKILL.md` and `.claude/skills/intent-engineering/SKILL.md` (how I author skills), `.claude/hooks/` (enforcement patterns), and `CLAUDE.md` (this repo IS a personal OS — the Company OS is its org-scale sibling).

### Step 2 — Research the landscape before locking anything

Per my standing rule: research before locking design decisions. Run these, in parallel where possible:

- **`last30days`** on: Company OS / Team OS / PM OS in Claude Code; Claude Code skills for non-engineering teams; org-wide agent adoption playbooks. I want to know what practitioners are building, complaining about, and asking for RIGHT NOW.
- **`deep-research`** (or WebSearch fan-out) on prior art, minimum targets: Aakash Gupta's PM OS and Team OS articles (news.aakashg.com/p/pm-os, /p/team-os-cc, /p/company-os-jz) — his are paid subscriber products, mine must be open and differentiated; existing "company OS" / "team OS" / CLAUDE.md-template repos on GitHub (search: company-os, team-os, claude-code template, awesome-claude-code); the AGENTS.md convention and how Cursor rules / Codex / Cowork each load instructions (the multi-harness compile target); Anthropic's org-level skills in Claude settings (what JZ uses as the delivery mechanism); adjacent commercial tools (Dust, Glean) to define what this deliberately is NOT.
- Synthesize into a **white-space statement**: what exists, what's missing, and why "an OS that installs itself through an agent-led interview" is (or isn't) the gap. If research shows someone already shipped exactly this, say so plainly — we pivot the differentiator rather than pretend.

### Step 3 — Brainstorm: pressure-test these seed theses (disagree where warranted)

1. **The wedge is the installer, not the template.** JZ's repo is the artifact; the hard part for any company is the setup — ontology mapping, skill authoring, delivery wiring. Laurel needed a dedicated human (AI Ops, "Sasha") to build theirs. Thesis: this project's core product is the **agent-led interview that generates the OS** — the repo is the consultant. `SETUP.md`/agent instructions walk any harness through interviewing the adopter (What functions exist? What does each do repeatedly? What should humans do MORE of?) and then generating the folder structure, starter ontology, and skill files from templates.
2. **Company-agnostic = generator + exemplars, not filled-in content.** Per-function starter ontologies (sales, CS, marketing, product, engineering, finance, legal, people/HR) with the up/down (more-human-time vs automate-away) columns, a skill-file schema/spec, and a small number of fully-worked exemplar skills — not 200 half-baked ones.
3. **A synthetic demo company** (the RevCoach move): the repo ships with a fictional ~20-person company pre-installed so the walkthrough runs end-to-end with zero real data, and `demo/` vs `your-company/` stay cleanly separated.
4. **Multi-harness by design:** one canonical instruction source compiled/mirrored to CLAUDE.md, AGENTS.md, and Cursor rules, so the walkthrough genuinely works in Claude Code, Cowork, Codex, and Cursor — this is a headline differentiator, decide how it works early.
5. **Governance and adoption are content, not afterthoughts:** captain model, two-track review, the 4-level maturity model as a self-assessment, hackathon playbook, AI-Ops role definition — the stuff a real company needs to actually adopt, and the stuff that shows PM judgment (my hiring signal) rather than just scaffolding skill.
6. **Maturity path for the repo itself:** versioned roadmap where V1 must be adoptable in an afternoon and each later version earns its complexity (delivery-layer integrations like the Slack morning briefing are probably V2+, not V1).

Also brainstorm beyond these: what am I not seeing? What would make a hiring CPO like JZ say "this person gets it" vs "this is a template dump"? Where does my code-brain experience (hooks enforce/subagents judge, intent-engineering, validate.py, export presets) give this project an edge nobody else's template has?

### Step 4 — Converge and write the design brief

Write the brief to `docs/plans/2026-07-15-company-os-design-brief.md` (or today's date). It must contain: the one-sentence product thesis; the differentiation vs Aakash's paid OSes, JZ's Laurel-specific OS, and whatever GitHub prior art research surfaced; target adopter + adoption story (who opens the repo, what happens in the first hour); scope ladder (V1 → Vn, each version earning its complexity); the multi-harness strategy; what ports over from code-brain (and what deliberately does not); portfolio surfaces (GitHub repo, website walkthrough à la RevCoach, possible Substack post); proposed new-repo name candidates and a proposed top-level layout for the new project folder under `/Users/seanwinslow/Code-Brain/`; and **wayfinder handoff material** for the session that follows: a candidate one-or-two-line Destination statement, the open decisions phrased as sharp questions (future decision tickets), and the still-foggy areas (future "Not yet specified" entries). Note in the brief that the wayfinder map should live on the NEW project repo's issue tracker — create the empty repo early so the map is public from day one; a visible map of decision tickets is itself portfolio evidence of process.

### Constraints

- **Do not scaffold the new repo or write any product code this session.** Brief only. (Do not run `/wayfinder` this session either — charting is the next session's single job, per wayfinder's own one-session-per-phase rule.)
- Interview me at decision points — this is a brainstorm, not a solo run. Use AskUserQuestion for real forks.
- Quote or cite what research actually found; never invent prior art or claim white space you didn't verify.
- Build phases (later sessions) will use Fable 5 + the Codex plugin (`/codex` review or `codex:codex-rescue`) as the review gate — note this in the brief's process section, don't act on it now.
- Before wrapping up, run the validation pass: does the brief answer every item in Step 4? Is the differentiation claim backed by actual research findings? If not, close the gap before ending the session.
