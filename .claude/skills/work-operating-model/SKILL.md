---
name: work-operating-model
description: Run a structured 5-layer interview to produce operating-model artifacts (HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations) for a named domain. Use when the user says "run the work operating model interview", "profile my work", "build my operating model", "interview me about [domain]", "update my operating model", "run the job-hunt-2026 interview", or "run the-block interview". Takes a required `domain` argument: one of "the-block" (archived 2026-05), "creative-studio", "life-systems", "job-hunt-2026".
---

# Work Operating Model

## Purpose

Interview Sean about how he actually works in a specific domain and produce the five artifact files that downstream agents and skills (daily-driver, sprint-health, process-inbox, pr-digest, meta-agent, flush, knowledge-lint) need to act with real context. Ported from Nate B. Jones's five-layer elicitation pattern — see the full source clip at [vault/40_knowledge/references/ref-agent-soul-md-prompt.md](../../../vault/40_knowledge/references/ref-agent-soul-md-prompt.md).

The interview runs once per domain. The four domains are The Block (archived 2026-05 — prior PM role; bundle moved to `vault/40_archive/operating-models-the-block-2026-05/` but the domain remains selectable so historical interviews can be re-run if needed), Creative Studio (16BitFit + Remotion + art + writing), Life Systems (finance + health + learning + tasks + time + career), and Job Hunt 2026 (Sean's 8-week post-Block search for AI/Tech/Creative PM roles, Boston metro or remote). Each domain has its own artifact bundle under `vault/05_atlas/operating-models/{domain}/` (or `vault/40_archive/...` for the-block).

## When to Use

- Sean says "run the work operating model interview", "interview me about the-block", "profile my creative-studio work", "build my operating model", "update my life-systems profile"
- An agent's output is generic or misaligned because it lacks operating context — the interview fills that gap
- Sean has gone through a major shift in work (new role, new rhythm, new stakeholders) and the existing operating model is stale
- Sean explicitly asks for a delta update ("my sprint cadence changed, update the-block HEARTBEAT")

## Before Starting (required)

1. Confirm the `domain` argument is one of `the-block` (archived 2026-05; bundle now under `vault/40_archive/operating-models-the-block-2026-05/`), `creative-studio`, `life-systems`, or `job-hunt-2026`. If not provided, ask Sean which domain this interview is for.
2. Read the five target files under `vault/05_atlas/operating-models/{domain}/` (or `vault/40_archive/operating-models-the-block-2026-05/` for the-block):
   - `HEARTBEAT.md`
   - `USER.md`
   - `SOUL.md`
   - `operating-model.md`
   - `schedule-recommendations.md`
3. Check the `status:` field in each file's frontmatter:
   - If all five are `status: awaiting-interview` → this is a **fresh interview**. Proceed through all five layers.
   - If some or all are `status: draft` or `status: confirmed` → ask Sean: "These files already have content. Is this a **fresh re-interview** (I'll overwrite), a **delta update** (pick specific layers to re-run), or a **confirmation pass** (read current answers back and ask what changed)?"
4. Remind Sean the interview takes ~45 minutes for a fresh run, ~15 for a delta. Ask if he wants to block the time now or schedule.

## Domain Argument Handling

| Argument | Target folder | Identity lens |
|---|---|---|
| `the-block` (archived 2026-05) | `vault/40_archive/operating-models-the-block-2026-05/` | Sean as PM at The Block — crypto/ETF company, Boston (Nov 2025 – May 2026; role eliminated in cost-cutting layoff). Selectable so historical interviews can be re-run; not active. |
| `creative-studio` | `vault/05_atlas/operating-models/creative-studio/` | Sean as creative — 16BitFit founder, filmmaker, pixel artist, writer |
| `life-systems` | `vault/05_atlas/operating-models/life-systems/` | Sean as a person — finance, health, learning, relationship, Boston life |
| `job-hunt-2026` | `vault/05_atlas/operating-models/job-hunt-2026/` | Sean executing his 8-week post-Block job hunt — AI PM > Tech PM > Creative PM, Boston metro or remote. See `vault/20_projects/prj-job-hunt-2026/` |

If Sean says "the Block" or "Block" → `the-block` (archived). If "creative" or "16bit" alone → `creative-studio`. If "life" or "personal" → `life-systems`. If "job hunt", "hunt", "search", or "onwards" → `job-hunt-2026`. If ambiguous, ask.

## The Five-Layer Interview

The full question set lives in [interview-questions.md](interview-questions.md) — read it in and work through the layers in order. Each layer feeds specific artifact files:

| Layer | Feeds | Consumed by |
|---|---|---|
| 1. Operating Rhythms | `HEARTBEAT.md` | daily-driver |
| 2. Recurring Decisions | `USER.md` | daily-driver, process-inbox, sprint-health |
| 3. Dependencies | `SOUL.md` (people/tools section) | sprint-health, pr-digest, process-inbox |
| 4. Institutional Knowledge | `SOUL.md` (tacit/tribal section) | all agents — context layer |
| 5. Friction | `schedule-recommendations.md` | daily-driver, meta-agent, future calendar agents |

The cross-layer `operating-model.md` file is a structured profile synthesized from all five layers — write it last.

## Checkpointing Behavior (non-negotiable)

After each layer:
1. Summarize back what Sean said in 5-8 bullet points
2. Show the proposed artifact updates (diff-style if the file already had content)
3. Ask: "Confirm this captures layer N accurately?" — wait for explicit confirm
4. Only then write to disk
5. Update the target file's frontmatter: `status: awaiting-interview` → `status: draft`; after the final layer and a full read-through, `status: draft` → `status: confirmed`

Never batch-save all five files at the end. Confirm-then-save each layer.

## Output Artifact Format

Read [artifact-templates.md](artifact-templates.md) for the exact structure of each of the five files. Key rules:

- Preserve existing frontmatter fields (`type`, `domain`, `created`) — only update `status` and `last_interviewed`
- Use markdown headings that match the template
- Write in Sean's voice (first person, present tense) unless he explicitly asks for a different register
- For `SOUL.md`: name real people. If Sean gives first names only, ask for enough context to disambiguate later ("Sarah from product" vs "Sarah from the ETF team")
- For `HEARTBEAT.md`: use 24-hour clock; call out which events are on calendar vs off
- For `schedule-recommendations.md`: each recommendation should be in the form "When X, then Y" (actionable for a calendar agent)

## Domain-Specific Tuning Notes

### The Block (archived 2026-05)
> Role ended 2026-05-04 (cost-cutting layoff delivered by Larry Cermak + Vicky Lu). Bundle preserved at `vault/40_archive/operating-models-the-block-2026-05/`. Tuning notes below preserved for re-running historical interviews; not for active use.

- Layer 1, Q2: Sprint ceremonies + bi-weekly P&E update cadence. ETF compliance windows and crypto market-open implications.
- Layer 1, Q5: Email split — `swinslow@theblock.co` was work (now archived), `sean.winslow28@gmail.com` is personal. Calendar queries no longer hit the Block account.
- Layer 3, Q5: Granola-synced meetings at `vault/30_domains/product-management/the-block-meetings-granola-notes/` are the historical record of meetings during the Block tenure.
- Layer 5: Decisions delayed because they're annoying were prime Jira-automation candidates while the role was active.

### Creative Studio
- Layer 1, Q2: 16BitFit has its own project rhythm (phases, gate checks). Ask about deep-work blocks vs render-waiting time.
- Layer 3, Q4: Three-machine topology is load-bearing here — Mac Mini, MacBook Pro, Alienware. Ask what specifically halts if each goes down.
- Layer 3, Q6: Sean is also pursuing an animation producer career transition — ask about festival/application cadences.

### Life Systems
- Layer 1, Q5: Most calendar items are personal Gmail. Ask about Bilt/Chase financial cycles.
- Layer 1, Q6: Boston move (from NYC) has specific seasonal friction — capture it.
- Layer 2, Q1: Includes habits and streak tracking — health-habits skill consumes this.

### Job Hunt 2026
> Active during Sean's 8-week post-Block search (started 2026-05-04). Once an offer is signed, retire this domain or evolve into a new role-specific bundle.

- Layer 1, Q2: Weekly application + outreach batches (5 quality applications/week, Tue + Thu mornings); interview-cycle scheduling; Friday weekly retro per `vault/20_projects/prj-job-hunt-2026/README.md`.
- Layer 1, Q5: Most flow through `sean.winslow28@gmail.com` (the-block address being archived 2026-05). Track recruiter / interview emails separately or via Gmail labels.
- Layer 2: Auto-yes for warm-intro outreach; auto-no for cold-recruiter spam below walk-away salary or outside Boston-metro / remote. Target archetype priority: AI PM > Tech PM > Creative PM.
- Layer 3, Q1: Larry Cermak (primary reference, ex-President of The Block), Matt Vitebsky (peer, contacted personally), 9 P&E peers per `vault/20_projects/prj-job-hunt-2026/The-Block-Contacts-After-Layoff.md`.
- Layer 3, Q3: Track-C work — the intent-engineering MCP server is the differentiator artifact. Ask what specifically blocks shipping v0.
- Layer 5: Application fatigue, interview prep collisions, offer-decision paralysis are the prime friction points. Look for automations that turn 20+ min admin tasks into 2 min.

## Success Criteria

At the end of an interview, the agent should be able to verify:
1. All five target files have `status: confirmed` or `status: draft` (not `awaiting-interview`)
2. Each file has real content — not template placeholders
3. Cross-references are consistent (e.g., a person named in `SOUL.md` also shows up in `HEARTBEAT.md` if they're on a recurring meeting)
4. `operating-model.md` synthesizes the other four without contradicting them
5. Sean has explicitly confirmed each layer

## Copy/Paste Ready

Sean can invoke this skill with any of:

```
Run the work-operating-model interview for the-block
Interview me about creative-studio
Profile my life-systems work
Update my the-block operating model — just layer 5
Delta update: my sprint cadence changed, update HEARTBEAT
```
