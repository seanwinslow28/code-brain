---
type: operating-model
artifact: SOUL
domain: [life-systems]
status: draft
last_interviewed: 2026-04-22
created: 2026-04-18
review-date: null
ai-context: "People, tools, and tacit/tribal knowledge for personal systems. Part A (dependencies) populated by Layer 3 interview; Part B (institutional knowledge) populated by Layer 4. Consumed by sprint-health, process-inbox, and as a context layer for all life-systems agents."
---

# SOUL — Life Systems

## Part A — Dependencies (Layer 3)

### Critical-Path Collaborators

Life-systems has no human collaborators in the classical sense — this is a solo domain. Loved ones interact with it as context and pivots, not partners.

| Relationship | Role in life-systems | What happens if unavailable |
|---|---|---|
| **Claude + Anthropic** | **True collaborator.** Second-brain, personal assistant, creative partner, financial partner. Everything in this domain is being built on top of Claude's capability stack. | Life-systems agents halt. Manual mode until restored. |
| Girlfriend | Daily context — evening plans, weekend, shared life, future shared finances | Not a blocker for life-systems tasks; she influences rhythm, not execution |
| Parents | Occasional pivots (travel, holidays, family events). Both ~70 — future dependency likely. | Not a blocker today; plan to revisit as they age |
| Cousins + friends | Social pivots — events, plans that break a ritual | Not a blocker; just a schedule perturbation |

**Key framing:** Sean is an only child. People aren't blocking life-systems execution — they're changing *when and whether* rituals happen. A pivot that happens rarely is fine. A pattern of pivots would become a nuisance worth addressing.

### Load-Bearing Tools (non-AI)
- **Obsidian vault** — canonical note + task store; knowledge graph
- **Apple Notes** — habitual quick-capture (goal: promote to vault via MCP/plugin)
- **Chase app** — credit + bank access
- **Bilt app** — rent payment + Bilt credit + points
- **Apple Health / Apple Fitness / Apple Workouts** — fitness tracking (iPhone + Watch)
- **Gmail (personal)** — subscription + notification inbox; life-systems comms
- **Calendar (personal Gmail)** — currently sparse; will grow as life-systems UI matures
- **[life-systems-hub](../../../../../life-systems-hub/) (in build)** — React + Vite + Tailwind v4 UI for habit/finance/research dashboard; future consumer of the vault

Exploratory: additional finance-focused apps on the radar; actively looking.

### Load-Bearing External APIs / Models

**Today (running):**
- Local models on Mac Mini: `gemma4`, `phi4-mini` — used for finance categorization to keep personal data local
- NotebookLM + NotebookLM MCP — research organization, queryable from Claude Code

**Inbound (near-term):**
- The Block's API key — crypto research/investment data (Sean's day-job company; API access pending)

**Target (the build-out):**
- Perplexity API — research agent backbone
- Gemini Deep Research MCP — second-opinion research channel
- Coinbase [agentkit](https://github.com/coinbase/agentkit.git) — agents with their own wallets for small financial moves
- Open-source deep-research models (TBD, under evaluation)

**Open workstream:** full audit of free/paid APIs + free/paid MCPs to maximize research firepower. Sean has flagged this as a "help me figure this out" item.

### Three-Machine Topology (life-systems lens — minimal coupling)
- **Mac Mini**: Agents SDK hub. Life-systems agents run here (vault synthesizer, knowledge lint, daily-driver autonomous runs, session-end flush). **Pivotable** — if it halts, Sean can relocate orchestration to another machine; nothing is strictly pinned to Mac Mini hardware.
- **MacBook Pro**: work machine. No life-systems load.
- **Alienware**: creative-studio generation node. No life-systems load.
- **iPhone + Apple Watch**: **only life-systems hard dependency** is fitness tracking (Apple Health/Workouts). If both are lost for a day, fitness logging halts — everything else (finance apps, Claude Code, vault) is reachable from another machine.

### Single Source of Truth

| Sub-area | Canonical SOT (target state) |
|---|---|
| **Finance** | Single aggregated CSV / Excel sheet combining Chase bank, Chase credit, Bilt credit, Rippling biweekly pay stubs. Not yet built — target state. Claude needs direct read access to this file for the 15th-of-the-month check. |
| **Fitness** | Apple Fitness / Apple Health. **Gap:** no MCP or CLI connection exists today — this is a build target. |
| **Tasks / notes** | Obsidian vault (canonical). Apple Notes is habitual quick-capture — wants Apple Notes ↔ Obsidian MCP or community plugin so nothing gets stranded there. |
| **Research captures** | Raw: `vault/00_inbox/` (Obsidian webclipper + quick thoughts). Indexed: `vault/40_knowledge/concepts/` with YAML frontmatter. Mature topics: promoted into their own sub-folder so research + execution plans stay bundled per topic rather than spread across the concepts folder. |

### Who Depends On Me

- **No one today.** Sean is not currently the keystone for anyone else's life-systems.
- **Future — girlfriend**: shared finances (she earns independently, so not an income dependency — it's shared-visibility and joint-planning).
- **Future — parents**: both close to 70; a dependency Sean expects but hasn't architected yet ("cross that bridge when we get to it").

### Self-Blocking Decisions (pile-ups)

Life-systems decisions only Sean can make that tend to **pile up**:

1. **Investment / savings decisions** — biggest pile-up. This is precisely what the agent-research fleet is being built to de-risk: if an agent produces a researched brief + recommended action + path to execution, Sean's cost to decide drops from "research from scratch" to "read the brief and pull the trigger."
2. **Learning decisions** — Sean hops between AI learning threads (tools / workflows / courses). Starts classes, struggles to finish because something new catches his attention or work gets busy. Structural tension with how fast the AI space moves, not a discipline problem.

---

## Part B — Institutional Knowledge (Layer 4)

_To be filled by Layer 4 interview._

### Internal Vocabulary
_Pending Layer 4._

### Sacred Cows
_Pending Layer 4._

### Unwritten Communication Rules
_Pending Layer 4._

### Ask X About Y
_Pending Layer 4._

### Past Landmines
_Pending Layer 4._

### Week-One Tacit Knowledge
_Pending Layer 4._

### Things Collaborators Have Learned About Sean
_Pending Layer 4._
