# groundwork — Company OS Design Brief

**Date:** 2026-07-15 · **Hardened:** 2026-07-16 (vault + Executive Circle mining pass — provenance in Appendix C)
**Session:** Brainstorm + research (Session 1 of the Company OS portfolio project; kickoff prompt at `docs/prompts/2026-07-15-company-os-brainstorm-kickoff.md`)
**Status:** Approved design brief, hardened. No code or scaffolding exists yet — next session is `/wayfinder` charting.

---

## 1. Product thesis (one sentence)

An open-source, harness-agnostic repo that interviews your company about the work each function actually does — what should get **more** human time, what should get **automated away**, and under **what rules** — and generates your operating system from that map: folder-per-function structure, skill files with named owners, a compiled constitution, and a provisioning path, adoptable in an afternoon with zero credentials.

**The sharpened claim:** groundwork is the only Company OS that **compiles governance** — typed rules with triggers, evidence, owners, and appeals, derived from an ontology interview — instead of shipping templates. And it is the only one whose **self-improvement is governed**: agents propose rule and skill changes through the company's own constitution; nothing rewrites itself silently.

Working name: **groundwork** ("the groundwork your company runs on"). Runner-up candidates in §10.

---

## 2. White-space statement & differentiation

### The honest headline

The agent-led-interview mechanic is **already shipped, at small scale**. This brief does not claim it as virgin territory:

- [dswh/company-os](https://github.com/dswh/company-os) (~24 stars, last push 2026-06-19) describes itself verbatim as a *"self-installing AI-native company operating system seed repo"* — the agent reads `INSTALL_FOR_AGENTS.md`, interviews the adopter, and generates a company brain + department loops. Thin function coverage, governance mostly punted, no traction.
- [Workflowsio/company-os-starter-kit](https://github.com/Workflowsio/company-os-starter-kit) (~74 stars, Dan Rosenthal/workflows.io, MIT) documents "Option B: *Interview me about my business and help me fill everything in*" — but as a suggested prompt over `{{placeholder}}` fill-in of a fixed CLAUDE.md, GTM-skills-only, Claude-Code-only.
- [garrytan/gbrain](https://github.com/garrytan/gbrain) (~26.3K stars) proved agent-driven install at scale — for a knowledge/retrieval brain, not an operating system of functions, skills, and governance.
- Anthropic's own `/init` (with `CLAUDE_CODE_NEW_INIT=1`) is normalizing interview-then-generate natively — but codebase-scoped, not company-scoped ([memory docs](https://code.claude.com/docs/en/memory)).
- Nate B. Jones's [SOUL.md elicitation workflow](https://natesnewsletter.substack.com/p/your-agent-needs-a-soulmd-you-cant) is the strongest *individual-level* prior art: a 5-layer resumable interview that generates operating artifacts (SOUL.md, USER.md, HEARTBEAT.md) for one person's agent. It also supplies the thesis-grade argument for why the interview IS the product: **expertise compiles into tacit judgment its owner can't articulate** — "the people with the most to gain from delegation are exactly the people whose work is hardest to delegate." groundwork is this argument applied at company scale.

### The verified open lane

Nobody with traction combines the four things groundwork leads with:

1. **Ontology-first generation with a real work schema** (§3). Every existing repo is template fill-in or a static skill library ([w95/awesome-claude-corporate-skills](https://github.com/w95/awesome-claude-corporate-skills) 166 skills, [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) 345, [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills) 343 — the content layer is commoditized). Nobody derives the structure from a scored map of the work. External practitioner validation: Hannah Stulberg's Team OS lesson is explicitly *"design the architecture deliberately, then fill it in"* — against start-small-and-iterate (ref-aakash-team-os-hannah-stulberg).
2. **Governance as compiled machinery, not prose** (§5). Governance was the least-covered criterion across all seven direct-hit repos, and the live pain is exactly here (r/cscareerquestions, 811 pts: *"gave Claude code to non technical people and things already broke"*; Nate: *"a written instruction is not enforcement"* — CLAUDE.md is context, not control). groundwork compiles constitutions: typed rules with owners and appeals on an enforcement ladder.
3. **Multi-harness via work packages, honestly** (§6). Only Sylph (165 stars, YC-backed) claims multi-harness, and its setup is per-skill configuration. groundwork adopts the harder standard: skills ship as *work packages* with explicit harness requirements and compatibility notes, because copying a SKILL.md alone demonstrably fails across harnesses.
4. **Structural enforcement.** No prior-art repo ships a validator, a context-budget check, or a synthetic demo company. groundwork ships all three.
5. **Governed organizational memory + self-improvement** (§5.4 — added 2026-07-16 after a dedicated research pass). Verified plainly: nobody ships git-native org memory with provenance, governance, and an observation→policy path. The pieces exist separately — Zep has bi-temporal provenance (an engine), Sentra has an org-memory schema (hosted SaaS), Nate's OB1 has a governance sidecar (personal memory), ADRs have the practice (engineering-only) — but no one has composed them as files a company owns. The harness vendors have explicitly declined this layer: the canonical Claude Code memory-governance request (provenance tags, review dates, `/memory-audit` — [issue #34776](https://github.com/anthropics/claude-code/issues/34776), five documented failure modes after 30 days of auto-memory) was **closed "not planned."** Both vendors' own communities route authority back to checked-in files (Codex best practice, verbatim: *"Do not rely on memories for required team/project behavior"*). Sylph claims self-improving skills, but its rewrite fires on approval of the *output* with no documented review of the *rule change itself* — the gap groundwork's proposal gate beats.

### Named competitors and how groundwork differs

| Against | What they are | groundwork's difference |
|---|---|---|
| Aakash Gupta's PM OS / Team OS ([pm-os](https://www.news.aakashg.com/p/pm-os), [team-os-cc](https://www.news.aakashg.com/p/team-os-cc)) | Paid, closed kits: PM OS $49–250 copy-paste (41 skills, 7 sub-agents, manual checklist); Team OS paid (3 context layers, 6 downloadables incl. an upgrade skill, starter repo, adoption playbook, sensitive-data checklist) | Open source and free; interview → generation instead of manual copy; company-scale and cross-function from the start; compiled governance machinery vs. checklists. Where Team OS content is genuinely strong (Shared Discipline, Classify→Consent→Enforce, adoption models) groundwork builds open equivalents and says so |
| JZ's Laurel Company OS ([company-os-jz](https://www.news.aakashg.com/p/company-os-jz) — free editorial, **no downloadable product**) | One company's real, working OS, described but not shipped | groundwork generalizes the architecture Laurel proved (ontology → skills → delivery, captain model, two-track review, maturity levels). Laurel needed a dedicated human (Sasha, AI Ops) to build theirs; groundwork's interview is that consultant, packaged — and the AI-Ops role gets a real job description (§4) |
| GitHub prior art (dswh, Workflowsio, Sylph, [clawcompany](https://github.com/Claw-Company/clawcompany) 580★, [beevibe](https://github.com/beevibe-ai/beevibe) 381★) | Seed repos, template kits, agent-role infra | Ontology schema + constitution compiler + owner cards + validator + demo company; positioning risk: Sylph and clawcompany are active — differentiation must never rest on "company OS repo" or "agent sets it up" alone |
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (~22.8K stars) + Cowork's built-in plugin library | Generic per-function content, manually customized | Company-specific generation. Coexistence stated concretely: **buy the primitives, own the company-specific workflow** — groundwork's plugins complement/override the generic ones in the same Cowork org |
| Dust ($30–150/seat/mo) / Glean (~$60K/yr floor) | Hosted per-seat agent platforms | groundwork ships only files into the company's own repo; execution rides the harness the company already pays for; git is the substrate; $0 incremental |
| Nate's Open Skills library (31 skills, 7 runbooks) | Portable *personal/team* skill library + the work-package concept | groundwork adopts the work-package standard and applies it to *generated, company-specific* skills — the library is a complement, not a competitor |

### Delivery mechanism (verified, upgraded 2026-07-16)

Two documented, real provisioning paths — no delivery software required:

1. **Org-level skills:** owners upload zipped SKILL.md folders → provisioned to employees in Claude chat/Desktop/Cowork (Team & Enterprise; [help center](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization)).
2. **Cowork plugin marketplaces (the better fit):** Cowork consumes **plugins** (skills + connectors + sub-agents) distributed via marketplaces, with a **GitHub-sync path — connect a private repo as a marketplace and every PR-merge auto-provisions org-wide** (ref-claude-cowork-manage-org-plugins). This makes "git is the source of truth" the literal provisioning mechanism.

**Boot-tax correction:** the naive "default-on for every employee" model is wrong — org-wide default-on plugins are a permanent context tax (documented case: 66K tokens loaded before typing; ref-66000-tokens). groundwork provisions a curated core as default-on and everything else as "available," using Cowork's four graded install preferences (installed-by-default / available / not-available / required, with group-level overrides).

---

## 3. The work ontology schema (Layer 1, and the primary artifact)

JZ's up/down map stays as the **executive view** — legible, color-codable, presentable to leadership. Beneath it, each activity in a function's ontology carries a deeper record. This schema is what makes "ontology-first" more than a slogan, and it is deliberately progressive: the deep fields are filled only for activities the company acts on, not all of them.

Per activity:

| Field | Values / shape | Source of the idea |
|---|---|---|
| **Direction** | up (more human time) / down (stop doing manually) | JZ/Laurel |
| **Motion** | automate / build / buy / **hire** / **wait** — scored on repetition, risk, judgment, company-specificity, market maturity | ref-exec-briefing-shape-of-the-work (up/down quietly collapses buy, wait, and hire into one bucket) |
| **Work type** | routing / sensemaking / accountability — routing automates now; sensemaking is speculative; accountability stays human permanently | ref-exec-briefing-valve-zappos (guard against automating the feedback function) |
| **Shape** | chat / single agent / agent team / don't-bother — via size, independence, separation, checkability | Nate's agent-shaped-work test |
| **Substrate** | where the work's state actually lives (CRM, tracker, ERP, spreadsheets-in-Slack). "State lives in Slack threads" = not automatable yet | ref-nate-agent-infrastructure (5 structural tests) |
| **Describability Gate** | required before anything routes to *automate*: inputs, output, standard, source of truth, exception path, error cost, owner, review gate. A skill generated for an un-describable workflow fails validation | ref-exec-briefing-shape-of-the-work: "do not automate what you cannot describe" |
| **Accountability** | which business process runs differently, and **who is accountable for proving it improved** ("employees save time" is disqualified) | ref-nate-implementation-architecture |

V1 ships starter ontologies for **8 functions** (sales, CS, marketing, product, engineering, finance, legal, people/HR) with the executive view populated and the deep schema as worksheets; the interview fills deep records for the activities the adopter chooses to act on first.

---

## 4. Target adopter & adoption story (the first hour)

**Adopter:** the "Sasha" — a founder, COO, CPO, or designated AI-Ops person at a ~10–200 person company. **Git posture (decided 2026-07-16):** groundwork is git-native and states the honest requirement plainly — **one git-capable maintainer**. That maintainer is the AI-Ops role, which groundwork gives a real job description (curate the diet, run the review loops, own the roster, merge proposals). Employees never touch git: they receive skills via org provisioning and propose changes in Slack; the maintainer commits. Git is kept not out of developer habit but because it is the one substrate with the five properties agent coordination needs — persistent state, defined verbs, ownership, permissions, audit history (ref-nate-agent-infrastructure) — and because Dropbox can't run a constitution.

**First hour:**

1. Open the repo folder in any of the four harnesses → README's first section is the RevCoach move: **"Not technical? Point your agent at this repo."**
2. **Demo walkthrough first:** a synthetic ~20-person B2B SaaS company ships pre-installed in `demo/` — the adopter watches the OS work end-to-end (CS renewal prep, PM feature-request triage, a constitution rule firing) with zero credentials. The demo script is a fixed **15-minute, 3-query sequence** (a decision lookup → a cross-function synthesis → a skill invocation) per the Team OS demo pattern.
3. **The interview** — a consultant protocol, not a form (mechanics hardened from Gabor Meyer's system-analyst pattern + Nate's elicitation workflow):
   - **Define the role first** ("what does a good vs bad organizational analyst do?"), then act as one
   - **One question at a time; no generation until understanding is complete**
   - **Evidence-based option:** with permission, the agent reads what exists — handbook, calendar export, repo, meeting notes — and reflects back *the rules the company is actually running*, because people report the rules they wish they had (Nate: "the agent version does not ask you what your rules are, because you would tell it what you wish they were")
   - **Checkpoint approvals** after each layer; **confirmed vs. provisional** facts distinguished; **resumable** state file that survives sessions and harness switches
   - The question skeleton adapts the intent-engineering 9-section spec (objective, outcomes, health metrics, constraints, autonomy, edge cases, stop rules) to an organization
4. The generator writes `your-company/`: folder-per-function structure with ontology records (§3), skills as work packages (§6) each with an Owner's Card (§5), the compiled constitution (§5), a root instruction file with routing tables, and the multi-harness file set.
5. `validate` passes — structure, referential integrity, secrets, harness-file drift, **context budget**, **description overlap**.
6. Provision: zip → org skills, or connect the repo as a Cowork plugin marketplace (curated core default-on, rest "available").

`demo/` and `your-company/` stay strictly separated; committed content is synthetic-only (RevCoach conventions).

---

## 5. Governance: the constitution compiler (Layer 2, co-headline)

groundwork's governance layer generates **machinery, not documents** (primary sources: Nate's 15 Commandments / five-question worksheet / enforcement ladder; the Agent Owner's Card; the paid Team OS's Shared Discipline layer):

1. **The constitution compiler.** The interview runs Nate's **five-question worksheet** on the adopter's existing rituals — name the ritual → name the scarcity it protected → is that scarcity still real, and what job survives → rewrite as a rule a person can verify → decide the machinery (trigger, evidence, action, owner, appeal) — starting with the rule everybody resents. Every kept rule is typed as one of **four objects with four owners** (value / rule / runtime check / human appeal) and placed on the **five-rung enforcement ladder** (value → instruction → reminder → hard block → human-owned decision; *there is no rung six* — consequential actions never terminate in automation). Every rule gets a **sunset date**. Orphan-prohibition check: a repealed ritual's surviving job must be reassigned before the repeal ships.
2. **Agent Owner's Card + roster.** Every generated skill ships with an Owner's Card (owner, backup owner, job-in-one-sentence, source of truth, allowed / proposed-only / forbidden actions, evidence required, review cadence, known failure modes, **pause and retirement conditions**), rolling up into a per-function **roster**. Doctrine: "shared use is fine; shared responsibility is often no responsibility," and **some agents should die**.
3. **Action-classification taxonomy** in every skill's frontmatter: read-only / reversible-write / external-side-effect / high-risk (spend, delete, external send). This generalizes code-brain's "hooks enforce; subagents judge" doctrine across harnesses: the taxonomy is declared everywhere, enforced by hooks where the harness supports them, by review gates where it doesn't.
4. **Organizational memory & the governed learning loop** (expanded 2026-07-16 after a dedicated research pass — provenance in Appendix D). Still **zero engines** — session recall and retrieval belong to the harness and the crowded infra field (Mem0, claude-mem 87K★, Letta, Zep, gbrain); groundwork owns the layer the vendors declined: *what an organization should remember, with what provenance, owned by whom, and how an observation becomes policy.* All of it files + validator checks:
   - **Typed org-memory schema (V1).** Records carry provenance labels (**observed / inferred / confirmed / superseded** — pulled forward from V3 into V1 frontmatter, matching the interview's confirmed-vs-provisional distinction); facts are never edited, they're **superseded** with `valid_at`/`invalid_at` windows (Zep's bi-temporal pattern — the `## Hindsight` blocks already implied this; now it's typed); each record has an owner and review status (OB1's governance-sidecar pattern); the memory folder is index-plus-topic-files under the same 200-line/25KB load discipline Claude Code's own auto-memory uses, enforced by the context-budget check.
   - **Shared Discipline (anti-rot).** The launch gate — *"the feature is not rolled out until the repository is updated"* — freshness checks (>90 days), Hindsight blocks, and the correction habit (Anthropic's own CLAUDE.md practice per Boris Cherny). Sunset dates on rules extend to expiry/review dates on every memory record — the exact mechanism the closed #34776 asked for.
   - **The promotion path.** Observation → working note → decision → rule/skill change, stage-gated by the restraint test ("recurring and non-obvious? — usually the honest answer is no," Nate's session-to-skill discipline) and a four-verb reconciliation checklist the maintainer runs at PR time: add / update / supersede / discard (Mem0's vocabulary, as review practice rather than an LLM pipeline).
   - **Governed self-improvement.** Agents may *propose* skill and rule rewrites; applying requires explicit human consent and lands as a **draft PR** (the BerriAI schema-gated pattern) — rule changes are rung-5 on the enforcement ladder *by construction*. Proposals route through three buckets mapped onto the ladder: auto-apply-with-changelog (low-risk) / needs-sign-off (review file) / needs-more-context. Ungated iterative rewriting is banned with cause: it produces context collapse and brevity bias (ACE, arXiv 2510.04618), and promote-everything becomes "the prompt pile it was supposed to replace."
   - **Engine posture.** The README points to gbrain/Open Brain/harness-native memory as complementary retrieval layers. Org memory is checked-in files — the place both vendors' communities already say authority must live.
5. **Two-axis maturity model.** Org-level (JZ's 4 levels: chat → workflow automation → apps → shared apps/shipping, with the screen-share test) × per-person fluency (the Zapier/Shopify-validated Unacceptable → Capable → Adoptive → Transformative rubric). Each level ships with signals + "one change to make this week."
6. **Adoption ladder.** Hub-and-Spoke / Full Adoption / Agent-Delegation with the decision rule ("<half the team uses AI → Hub-and-Spoke; more → Full; 10+ with eng → add Agent-Delegation"), the 4-week rollout (seed rough → one person → two habits → open with the 3-query demo), the captain model, and two-track review made concrete by the action taxonomy (track 1 = read-only/reversible; track 2 = external-side-effect/high-risk + product-strategy/architecture review).
7. **V2 — Classify → Consent → Enforce compliance pack:** `permissions.yaml` consent registry (approved_uses / do_not_use / expiration), CODEOWNERS on sensitive generated folders, a Gitleaks profile, a GDPR Art-17 `git filter-repo` erasure runbook, and a DPIA template — the auditor binder no prior-art repo has.

---

## 6. Multi-harness strategy: convention + work packages

**The convention (unchanged):** `AGENTS.md` is the single canonical instruction source; a permanent one-line `CLAUDE.md` imports it (`@AGENTS.md` — Claude Code does **not** read AGENTS.md natively, [docs verbatim](https://code.claude.com/docs/en/memory)); generated `.cursor/rules/*.mdc` point back; Codex and Cursor read AGENTS.md natively ([agents.md](https://agents.md/) — Linux Foundation, 60K+ projects). No compile script; drift between the files is a validator check.

**Hardened with the work-package standard** (Nate's Open Skills): copying a SKILL.md alone fails across harnesses — loading rules differ, hooks become prose, subagents don't exist, MCP configs vanish. So every generated skill is a **work package**: the SKILL.md *plus* explicit harness requirements (tools, permissions, scripts, connectors), **compatibility notes** ("tested in X; here is what breaks in Y" — honesty as a feature), a sync story, a **Memory row** (what the skill may read from org memory, write back, or keep run-only — required now that both harnesses write memory by default, so the constitution must say what agents may persist), and the owner (already on its card). The one-question test ships in the docs: *"if I had to move this skill tomorrow, what would break?"*

**AGENTS.md authoring standard** baked into the generator (GitHub's empirical analysis of 2,500+ AGENTS.md files, ref-pm-guide-agent-distribution): executable commands early, code not prose, explicit "never do" boundaries, pinned versions.

**Skill-count bound:** agents mis-select at 30+ tools with overlapping descriptions and are near-guaranteed wrong at 100+. Consequences: the validator enforces **non-overlapping, outcome-oriented skill descriptions** (description = selection surface, reviewed like landing-page copy), and provisioning defaults to a curated core (§2 boot-tax correction).

**Cowork:** consumes plugins via marketplaces (manual ZIP or GitHub-sync); groundwork's output is packaged as a Cowork plugin (structure + marketplace.json) in the V2 delivery recipes. Real constraints to document: reserved names, 50MB/100-plugin limits, connectors reach via Anthropic's cloud.

---

## 7. Scope ladder (each version earns its complexity)

**V1 — adoptable in an afternoon** (the constraint binds the adopter's *required path* — interview → generate → validate → provision — not repo size):
- The interview (consultant protocol, §4) + generator templates
- 8 starter ontologies with the §3 schema (executive view + progressive deep worksheets); **3 deep functions** with worked exemplar skills through the demo company: **Customer Success**, **Product/PM**, and **People/HR or Finance** (wayfinder ticket, leaning People/HR)
- Skills as **work packages** with **Owner's Cards**, action taxonomy, and the authoring standard (progressive disclosure, description-as-selection-surface)
- **The constitution compiler** + enforcement ladder + adoption ladder + two-axis maturity (§5.1–5.3, 5.5–5.6)
- **Org-memory schema + governed learning-loop rules** (§5.4): typed records with provenance/supersession frontmatter, promotion-path rules, the Memory row in every work package, and the draft-PR proposal gate — all conventions + validator checks, no engines
- Multi-harness file set (§6) and the **validator** (structure, referential integrity, secrets, drift, context budget, description overlap)
- Synthetic demo company with the 15-minute 3-query script; Known Limitations; security/privacy section; versioned roadmap — the RevCoach finished-artifact bar

**V2 — earns its complexity if adopters finish V1's interview:**
- **Classify → Consent → Enforce compliance pack** (§5.7)
- Delivery recipes: Cowork plugin packaging + GitHub-synced marketplace walkthrough; org-skills zip path; morning-Slack-briefing pattern
- The **agent-readable "truth layer"** — the company's canonical claims/proof/constraints file, legible to its own agents and external ones (ref-what-chatgpt-sees; also the strongest Substack angle)
- Hackathon playbook; maturity assessment as a runnable skill; second demo company (services agency)
- **Runnable learning-loop skills**: session-to-skill extraction (with the restraint gate) and the improvement-proposal skill (three-bucket routing → draft PR) — shipped once V1's schema has been exercised

**V3 — earns its complexity if the OS survives contact with month two:**
- Re-interview / drift flow (regeneration merging with local edits, riding the V1 provenance/supersession schema)
- Per-function deepening; adoption scoreboard measured as **coordination tax removed** (not skill-install counts) with the over-automation reversion watchlist (attrition of mid-tenure people = feedback vacuum)
- Optional evals/traces recipe for generated skills (the self-improving-agent pattern; human-in-the-loop mandatory at any change)

Deliberately **not** on the ladder: hosted anything, dashboards, per-seat features, an agent runtime, a memory system (conventions only). groundwork is files.

---

## 8. What ports from code-brain (and what deliberately does not)

| Ports | As what |
|---|---|
| `intent-engineering` 9-section template + retrofit levels | The interview's question skeleton (objective/outcomes/health-metrics is the anti-Goodhart spine of the ontology) |
| `work-operating-model` skill (itself adapted from Nate's elicitation workflow) | The interview's *session mechanics*: layered elicitation, checkpoint approvals, resumable state |
| `scripts/validate.py` architecture (per-concern checks → errors/warnings gate; referential integrity; secret scan) | Rewritten config-driven, extended with context-budget and description-overlap checks |
| `skill-system-mastery` authoring standard | The work-package schema's skill-file core |
| Root `CLAUDE.md` skeleton (constitution + routing tables + live-count inventories + tickets protocol) | The generation target for the root instruction file |
| Security-hook profile + "hooks enforce; subagents judge" doctrine | The action taxonomy's Claude-Code enforcement tier; doctrine generalized cross-harness via review gates |
| `install.sh` preset→export-group→canonical-store pattern | Design pattern for generation (selection separated from content) — not the bash implementation |

**Deliberately not ported:** the agents-sdk autonomous layer, Obsidian vault, launchd scheduling, LLM council / research APIs, personal domain content, export-groups/presets machinery, and any runtime memory system.

## 9. Portfolio surfaces & process

1. **The GitHub repo** — public from day one. **Create the empty repo early** (next session): the wayfinder decision-ticket map lives on the *new repo's* tracker, and a visible map of decisions-in-progress is itself portfolio evidence of process.
2. **Website walkthrough** à la RevCoach (post-V1). A ready-made ROI hook from the research: ~5 min/session × 3 sessions/day × 100 people ≈ 6,000 hrs/yr of context re-explanation (ref-one-file).
3. **Substack candidates:** "I read how Laurel runs on a Company OS, then built the version any company can install"; V2's truth layer ("what agents see when they look at your company") is a second angle.
4. Hiring-CPO signal throughout: ontology schema + compiled governance + honest limitations + versioned roadmap. Anti-AI-washing rule applies to groundwork's own README — describe honestly; overclaiming is trust debt (ref-what-chatgpt-sees).

**Process:** Session 2 = `/wayfinder` charting only (brief → map + decision tickets on the new repo's tracker). Sessions 3+ work the map one ticket per session. Build sessions use **Fable 5 with the Codex plugin as the review gate** (`/codex` review or `codex:codex-rescue`).

## 10. Name candidates & new-project layout

**Lead: `groundwork`** — "the groundwork your company runs on." Runners-up: `quartermaster`, `charter` / `charter-os`, `keel`. GitHub availability check is a wayfinder ticket.

**Location:** `/Users/seanwinslow/Code-Brain/groundwork/` (sibling to `code-brain/` and `CB-RevCoach-Brief/`).

```
groundwork/
├── README.md              # positioning + "Not technical? Point your agent at this repo"
├── AGENTS.md              # canonical agent instructions (navigation + interview entry; GitHub authoring standard)
├── CLAUDE.md              # one line: @AGENTS.md import
├── .cursor/rules/         # .mdc pointers back to AGENTS.md
├── interview/             # consultant protocol, question banks, layer checkpoints, resumable state conventions
├── ontologies/            # 8 starter function ontologies (executive view + deep-schema worksheets, §3)
├── skills/                # work-package schema/spec + worked exemplar skills (SKILL.md core + harness requirements + Owner's Card)
├── governance/            # constitution compiler, enforcement ladder, owner-card + roster templates,
│                          #   adoption ladder, two-axis maturity, shared-discipline conventions
├── delivery/              # provisioning guides (org skills zip; V2: Cowork plugin marketplace + GitHub sync)
├── demo/                  # synthetic ~20-person B2B SaaS, OS pre-installed, 15-min 3-query script
├── your-company/          # target the generator fills (git semantics → ticket)
├── scripts/validate.py    # config-driven: structure/integrity/secrets/drift/context-budget/description-overlap
└── docs/                  # known limitations, security/privacy, roadmap, decision records
```

---

## 11. Wayfinder handoff

**The wayfinder map lives on the NEW repo's issue tracker** — create the empty `groundwork` repo at the start of Session 2.

### Candidate Destination statement

> Any company can point its coding agent at this repo and, within an afternoon, get a governed, multi-harness Company OS compiled from its own work ontology — typed rules with owners and appeals, skills with named owners and honest compatibility notes, and a memory that learns under governance instead of rewriting itself — judgment built in, not bolted on.

### Open decisions (future decision tickets, phrased sharp)

1. **Third deep function:** People/HR or Finance — which one, and why does the demo narrative need it?
2. **Name & availability:** is `groundwork` free on GitHub? Fallback order among quartermaster/charter/keel?
3. **License:** MIT (RevCoach precedent) or Apache-2.0 (knowledge-work-plugins precedent)?
4. **Interview state format:** one resumable state file vs per-phase checkpoint artifacts — what survives a harness switch mid-interview, and how are confirmed-vs-provisional facts encoded?
5. **Ontology schema curation:** which §3 fields are V1-required vs optional worksheet — where is the line between "richest work ontology anywhere" and "form nobody finishes"?
6. **SKILL.md portability:** verify first-party how Codex/Cursor/Gemini load SKILL.md-format skills today; define the compatibility-notes testing matrix (which harnesses get "tested-in" status for V1?).
7. **Owner's Card field subset:** all 19 fields, or a V1 core (owner, job, sources, action classes, review cadence, pause/retire) with the rest optional?
8. **Constitution compiler depth in V1:** worksheet + typing + ladder as guided content, or does the interview also generate runnable rung-3 reminders (e.g., the meeting-challenger pattern) for Claude-Code orgs?
9. **Context-budget thresholds:** what boot-token estimate triggers the validator warning, and how is it measured per harness?
10. **`your-company/` git semantics:** adopter's fork? template-repo pattern? private-marketplace repo separate from the groundwork clone?
11. **Attribution framing:** how prominently to credit JZ/Laurel, Aakash, Nate B. Jones (constitution machinery, owner card, work packages), and dswh/company-os as prior art in the README (recommended: prominently — honesty is the brand).
12. **Sylph/clawcompany positioning:** what the README comparison says without punching down.
13. **Validator language:** Python stdlib (code-brain precedent) vs Node (RevCoach stack) — which does the git-capable maintainer more likely have?
14. **Demo-company data conventions:** RevCoach-style "all committed content synthetic" rule — how is it made verifiable?
15. **Org-memory schema field set:** which frontmatter fields are V1-required (provenance label, owner, valid_at/invalid_at, review_by) vs optional — and what does the validator reject vs warn on?
16. **Three-bucket thresholds:** what makes an improvement proposal "low-risk auto-apply" vs "needs sign-off" — is the boundary the action-classification taxonomy, and where does the changelog live?
17. **Draft-PR proposal mechanics per harness:** the BerriAI pattern assumes GitHub PRs — what is the equivalent gate for a Cowork-only or Cursor-only adopter?

### Not yet specified (foggy areas)

- Delivery-layer V2 recipes' exact shape (Slack morning briefing: docs only vs reference implementation — JZ's scheduled-task-overload warning applies)
- Re-interview / drift flow mechanics (V3): how regeneration merges with local edits; provenance-label lifecycle
- The truth layer's schema (V2): claims / proof / constraints — one file or per-audience?
- Enterprise security posture beyond the V2 compliance pack (SSO-gated repos? Cowork "connectors via Anthropic's cloud" caveat)
- How the adoption scoreboard's "coordination tax removed" is actually measured in files
- Skill auto-invocation reliability (~70% per Hannah Stulberg) — how generated routing tables compensate; belongs in Known Limitations

---

## Appendix A: seed-thesis verdicts (pressure-tested against research)

1. **"The wedge is the installer, not the template" — partially overturned.** The installer mechanic is already claimed (dswh verbatim; gbrain at 26K★; Anthropic's `/init`; Nate's SOUL.md workflow at the individual level). The wedge moved one layer up: the **ontology schema + compiled governance** are the product; the installer is the delivery vehicle.
2. **"Generator + exemplars, not filled-in content" — confirmed, sharpened.** Static skill content is commoditized (166–345-skill libraries). Sharpened to: 8 ontologies broad, 3 functions deep — and bounded by the empirical 30+-skill mis-selection ceiling.
3. **"Synthetic demo company" — confirmed.** No prior-art repo ships one. ~20-person B2B SaaS, with the 15-minute 3-query demo script.
4. **"Multi-harness by design" — confirmed, twice hardened.** First to convention-not-tooling; then (hardening pass) to **work packages with compatibility notes**, because SKILL.md-copying demonstrably fails across harnesses.
5. **"Governance and adoption are content" — strongly confirmed, then upgraded.** Least-covered criterion in every prior-art repo, loudest practitioner pain — and the hardening pass turned it from content into **compiled machinery** (worksheet → typed objects → enforcement ladder → owner cards).
6. **"Maturity path for the repo itself" — confirmed.** Delivery integrations are V2+; JZ's scheduled-task-overload warning and the boot-tax finding both reinforce V1 shipping no automation.

**What the theses missed (found in brainstorm + hardening):** the Cowork GitHub-sync marketplace makes git the literal delivery mechanism; the intent-engineering spec + work-operating-model skill are ready-made interview skeletons; `awesome-claude-code` (~50K★) has no company-OS category — a cheap distribution move; the boot tax and skill-count ceiling impose real, citable bounds the naive "provision everything" story ignores; and the anti-rot/discipline layer is what separates an OS that survives month two from a template dump.

## Appendix B: research provenance (session 1, 2026-07-15)

- **last30days** (2 passes, 2026-06-15→07-15): Company OS content wave 3 weeks old, epicentered on the JZ episode (36.6K views); "interview me" pattern in the air (Chase AI, 83K views); governance failure the loudest pain (r/cscareerquestions 811 pts); raw data in `~/Documents/Last30Days/`.
- **Prior-art agent A** (Aakash products, Anthropic org skills, Dust/Glean): PM OS $49/$250 paywalled kit; Team OS paywalled; company-os-jz free editorial, no product; org-skill provisioning documented; knowledge-work-plugins ~22.8K stars, no interview/ontology/governance.
- **Prior-art agent B** (GitHub landscape, multi-harness): dswh/company-os the verbatim prior claim (24★); Sylph (165★, YC) strongest complete competitor; clawcompany 580★; AGENTS.md Linux-Foundation-stewarded, not read natively by Claude Code; Cursor reads AGENTS.md + `.mdc` rules; awesome-claude-code has no company-OS category.
- **Machinery audit** (code-brain): installer pattern, validator architecture, skill-authoring standard, intent-engineering template, hook doctrine, CLAUDE.md skeleton.

## Appendix C: hardening-pass provenance (2026-07-16)

Sources mined: `vault/40_knowledge/references/` (Aakash paid-article clips + Nate corpus), `vault/00_inbox/` (15 Commandments, Hermes memory plan), and the Executive Circle MCP (full posts: "Every Agent Needs an Owner," "Open Skills"; web: agent-shaped-work).

| Adopted idea | Source | Landed in |
|---|---|---|
| Five-motion routing + six-dimension scoring; Describability Gate | ref-exec-briefing-shape-of-the-work | §3 |
| Routing/sensemaking/accountability work-type tags; over-automation watchlist | ref-exec-briefing-valve-zappos | §3, §7 V3 |
| Agent-shaped test (chat/agent/team/none) | natesnewsletter agent-shaped-work | §3 |
| Substrate column; git's five agent-substrate properties | ref-nate-agent-infrastructure-5-structural-tests | §3, §4 |
| "Who proves it improved" accountability field | ref-nate-implementation-architecture-six-components | §3 |
| Constitution compiler: five-question worksheet, four objects/four owners, enforcement ladder, sunsets, orphan-prohibition check, "instruction ≠ enforcement" | Nate 15 Commandments (inbox + MCP) | §5.1, §1 |
| Agent Owner's Card (19 fields) + roster + retirement doctrine | MCP: "Every Agent Needs an Owner" | §5.2 |
| Action-classification taxonomy; judge outcomes → two-track mapping | ref-nate-agent-judge-layer | §5.3 |
| Shared Discipline anti-rot layer; launch gate; freshness; Hindsight blocks | ref-aakash-team-os (paid, Layer 3) | §5.4 |
| Two-axis maturity (org × person fluency) | ref-zapier-measure-ai-fluency + ref-aakash-ai-fluency | §5.5 |
| Adoption ladder (3 models + decision rule), 4-week rollout, 3-query demo | ref-aakash-team-os | §5.6, §4 |
| Classify→Consent→Enforce compliance pack (V2) | ref-aakash-team-os (downloadable #5) | §5.7, §7 V2 |
| Interview protocol: one-question-at-a-time, define-role-first, no-generation-until-understood | ref-aakash-full-ai-dev-team (Gabor Meyer) | §4 |
| 5-layer elicitation, checkpoints, confirmed-vs-provisional, resumable; tacit-knowledge thesis | Nate SOUL.md (ref-agent-soul-md-prompt) | §4, §2 |
| Evidence-based interview ("rules you're actually running") | Nate 15 Commandments companion guide | §4 |
| Work-package standard; "what breaks if it moves" test | MCP: "Open Skills" | §6 |
| AGENTS.md empirical authoring standard; 30+/100+ skill mis-selection bound | ref-pm-guide-agent-distribution | §6 |
| Boot-tax correction; graded install preferences; context-budget validator check | ref-66000-tokens + ref-claude-cowork-manage/use-plugins | §2, §6, §7 |
| Cowork plugin marketplace + GitHub-sync delivery (resolves old ticket #6) | ref-claude-cowork-manage-org-plugins | §2, §7 V2 |
| Truth layer (V2) + anti-AI-washing rule | ref-what-chatgpt-sees | §7 V2, §9 |
| Memory: conventions only; store/inject/recall framing acknowledged, system deliberately excluded | Claude-Hermes-Inspired-Memory-Plan (inbox) | §5.4, §7 |
| Ontology-first practitioner validation; ~70% skill auto-invocation caveat | ref-aakash-team-os-hannah-stulberg | §2, §11 foggy |
| ROI hook (6,000 hrs/yr); git-vs-cloud contradiction (resolved: git-native, one maintainer) | ref-one-file-saves-team-thousands-hours | §9, §4 |

**Considered and not adopted:** full Hermes memory system (vector DB, capture hooks) — drifts into agents-sdk territory; dual-mode Dropbox path — guts the enforcement story; scout-mission onboarding — folded conceptually into the adoption ladder rather than a separate pattern; evals/traces loop — deferred to V3 as an optional recipe.

## Appendix D: organizational-memory & self-improvement research pass (2026-07-16)

Prompted by Sean's challenge to the "conventions only" memory decision. Method: last30days pass + deep web-research agent (harness-native memory state + flaws, memory-infra projects, self-improvement mechanics, org-memory products). Verdict: hypothesis supported with a nuance — engines are a losing race (claude-mem 87K★ silently disables native auto-memory; "fix Codex memory" tools obsoleted by native launch), but conventions-only was **under-specified about schema**. Result: §5.4 expanded into the Organizational Memory & Governed Learning Loop; provenance labels pulled from V3 to V1.

| Adopted mechanism | Source | Landed in |
|---|---|---|
| Bi-temporal supersession (valid_at/invalid_at; supersede, never edit) | Zep/Graphiti temporal knowledge graph | §5.4 schema |
| Provenance + review-status + owner sidecar | Nate's OB1 "Agent Memory" schema | §5.4 schema |
| Promotion-with-restraint gate + four-verb reconciliation (add/update/supersede/discard) | Nate session-to-skill discipline + Mem0 | §5.4 promotion path |
| Proposal → schema-gated consent → draft PR | BerriAI/self-improving-agent | §5.4 governed self-improvement |
| Three-bucket improvement routing (auto-apply / sign-off / more-context) | Austin Marchese self-improving-system framework (47K views) | §5.4, ticket #16 |
| Index + topic files under a hard load budget; progressive disclosure | Claude Code auto-memory docs + claude-mem | §5.4 schema, validator |
| Memory row (may read / may write / run-only) in every work package | Nate Open Skills work package | §6 |
| Anti-patterns cited: ungated self-rewrite → context collapse/brevity bias; promote-everything → prompt pile | ACE (arXiv 2510.04618); Nate Open Skills; Sylph's undocumented rewrite gate | §5.4, §2.5 |

Key evidence for the white-space claim: Anthropic closed the memory-governance feature request ([claude-code #34776](https://github.com/anthropics/claude-code/issues/34776) — provenance tags, review dates, /memory-audit) as **"not planned"**; Codex community best practice routes authority to checked-in files; r/ClaudeCode practitioner evaluated **21+ memory systems** just to get three agents to talk (fragmentation, not a solved layer). Unverified items flagged in the research: Codex EEA restriction, Anthropic consumer-memory caps, Sylph's diff internals, MemOS details.
