---
name: work-operating-model
description: Run a structured 5-layer interview to produce operating-model artifacts (HEARTBEAT, USER, SOUL, operating-model, schedule-recommendations) for a named domain. Use when the user says "run the work operating model interview", "profile my work", "build my operating model", "interview me about [domain]", "update my operating model", or "run the-block interview". Takes a required `domain` argument: one of "the-block", "creative-studio", "life-systems".
---

# Work Operating Model

## Purpose

Interview Sean about how he actually works in a specific domain and produce the five artifact files that downstream agents and skills (daily-driver, sprint-health, process-inbox, pr-digest, meta-agent, flush, knowledge-lint) need to act with real context. Ported from Nate B. Jones's five-layer elicitation pattern — see the full source clip at [vault/40_knowledge/references/ref-agent-soul-md-prompt.md](../../../vault/40_knowledge/references/ref-agent-soul-md-prompt.md).

The interview runs once per domain. The three domains are The Block (day job), Creative Studio (16BitFit + Remotion + art + writing), and Life Systems (finance + health + learning + tasks + time + career). Each domain has its own artifact bundle under `vault/05_atlas/operating-models/{domain}/`.

## When to Use

- Sean says "run the work operating model interview", "interview me about the-block", "profile my creative-studio work", "build my operating model", "update my life-systems profile"
- An agent's output is generic or misaligned because it lacks operating context — the interview fills that gap
- Sean has gone through a major shift in work (new role, new rhythm, new stakeholders) and the existing operating model is stale
- Sean explicitly asks for a delta update ("my sprint cadence changed, update the-block HEARTBEAT")

## Before Starting (required)

1. Confirm the `domain` argument is one of `the-block`, `creative-studio`, `life-systems`. If not provided, ask Sean which domain this interview is for.
2. Read the five target files under `vault/05_atlas/operating-models/{domain}/`:
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
| `the-block` | `vault/05_atlas/operating-models/the-block/` | Sean as PM at The Block — crypto/ETF company, Boston, `swinslow@theblock.co` |
| `creative-studio` | `vault/05_atlas/operating-models/creative-studio/` | Sean as creative — 16BitFit founder, filmmaker, pixel artist, writer |
| `life-systems` | `vault/05_atlas/operating-models/life-systems/` | Sean as a person — finance, health, learning, relationship, move to Boston |

If Sean says "the Block" or "Block" → `the-block`. If "creative" or "16bit" alone → `creative-studio`. If "life" or "personal" → `life-systems`. If ambiguous, ask.

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

### The Block
- Layer 1, Q2: Sprint ceremonies + bi-weekly P&E update cadence. Ask about ETF compliance windows and crypto market-open implications.
- Layer 1, Q5: Email split — `swinslow@theblock.co` is work, `sean.winslow28@gmail.com` is personal. Calendar queries MUST hit both.
- Layer 3, Q5: Granola-synced meetings at `vault/30_domains/product-management/the-block-meetings-granola-notes/` are the internal source of truth.
- Layer 5: Be especially sharp on "decisions I delay because they're annoying" — these are prime candidates for Jira automation.

### Creative Studio
- Layer 1, Q2: 16BitFit has its own project rhythm (phases, gate checks). Ask about deep-work blocks vs render-waiting time.
- Layer 3, Q4: Three-machine topology is load-bearing here — Mac Mini, MacBook Pro, Alienware. Ask what specifically halts if each goes down.
- Layer 3, Q6: Sean is also pursuing an animation producer career transition — ask about festival/application cadences.

### Life Systems
- Layer 1, Q5: Most calendar items are personal Gmail. Ask about Bilt/Chase financial cycles.
- Layer 1, Q6: Boston move (from NYC) has specific seasonal friction — capture it.
- Layer 2, Q1: Includes habits and streak tracking — health-habits skill consumes this.

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
