# Life-Systems Operating Model — Layer 4, Question 7 Prompt

**How to use:** Open Claude Code inside your `claude-code-superuser-pack` directory. Paste everything between the triple backticks into a single message. No Plan Mode required — this is a read-only introspection task. Extended Thinking (single Tab) is recommended.

---

```
<role>
You are a reflective archivist. Your job is to survey a mature Claude Code ecosystem and surface the tacit, accumulated knowledge that has been codified about Sean Winslow — specifically in the life-systems domain. You are not generating new advice; you are curating what's already latent in the files, agent logs, skills, and memory entries.

Treat this as forensic discovery: the "memory" lives across many files, and your job is to find it and present it cleanly.
</role>

<reasoning_directive>
ultrathink. This task reads across potentially hundreds of files. Shallow search will miss the good stuff. Take the time to search broadly, then curate tightly.
</reasoning_directive>

<task_summary>
Sean is populating the Layer 4 (Institutional Knowledge) section of his life-systems operating model. Specifically, he needs to answer:

> "Things Claude / agents have learned about me over time — patterns you've trained agents into (or out of), memory entries that keep rescuing the conversation."

He gave two examples of the kind of thing he's looking for:
- `Alienware ICMP blocked — use HTTP not ping` (an operational fact that keeps rescuing agent runs)
- `Sean prefers a 'here's the option' framing, not 'you should'` (a communication preference)
- `When Sean says 'maybe later', treat it as a defer-to-vault capture` (a linguistic decode)

Your job: produce a curated list of these for the **life-systems domain only**. Scope is: personal finance, health, learning, tasks/time, career transition.

The output will be pasted into `vault/05_atlas/operating-models/life-systems/SOUL.md` as a subsection. It is read by agents at runtime to avoid re-learning the same lessons.
</task_summary>

<scope>

**In scope (life-systems):**
- Personal finance: spending, budgeting, investments, net worth tracking
- Health: exercise, sleep, nutrition, mental health, recovery
- Learning: courses, books, skills being developed, practice routines
- Tasks / time: TASKS.md, calendars, daily routines, time protection
- Career: career-transition planning, resume work, interview prep

**Out of scope (do NOT include):**
- The Block PM work (company-specific — different domain)
- Creative Studio (16BitFit, animation, Remotion, pixel art — different domain)
- Agent SDK infrastructure tuning (cross-cutting, not life-systems)
- Claude Code / CLI / MCP configuration (tooling, not life-systems behavior)
- Generic LLM best practices Sean never specifically affirmed

If a pattern crosses domains (e.g., "Sean prefers terse responses" applies everywhere), include it only if the source evidence is anchored in life-systems interactions. Otherwise leave it for the cross-cutting review.

</scope>

<sources_to_consult>

Search all of the following. The list is ordered from highest-signal to lower-signal:

1. **`life-systems/CLAUDE.md`** (if it exists yet — may be missing per the pending restructure). Any memory/notes/preferences section.
2. **`Sean-Winslow-Full-Personal-Context-v1.1.md`** at the repo root. Scan for any life-systems-flavored preferences, constraints, or personal facts.
3. **`vault/` entire tree** with particular attention to:
   - `02_Areas/` (life domain areas)
   - `05_atlas/moc-life-systems.md`
   - `20_projects/` for any life-systems projects
   - `30_domains/` for life-systems domain notes
   - `40_knowledge/` for captured learnings
   - `90_system/templates/` for any life-systems template defaults
4. **`.claude/skills/`** — specifically the skills Sean's used for life-systems:
   - `personal-finance` (if present)
   - `career-transition`
   - `health-*` / `fitness-*` / `learning-*` (whatever exists)
   - `productivity:task-management` / `productivity:memory-management`
   - `daily-driver` skill
   - Any skill with trigger phrases or hard-won rules Sean has clearly tuned
5. **`agents-sdk/agents/`** source files for agents that touch life-systems:
   - `daily_driver.py`
   - Any disabled agent that previously handled personal-finance / spending-analysis
6. **`vault/90_system/agent-logs/`** and `agent-run-history.csv` — scan recent logs for errors that taught the system something (the "Alienware ICMP" pattern is this flavor)
7. **`CHANGELOG.md`** — look for any `### Fixed` or `### Changed` entries that codified a life-systems behavior (e.g., budget caps on spending analysis, daily driver schedule changes)
8. **`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`** — contains reasons for disabling agents; some reasons are latent preferences
9. **Any `memory/` directory** per the `productivity:memory-management` skill's two-tier memory pattern (CLAUDE.md working memory + memory/ knowledge base)
10. **Root `CLAUDE.md` "Non-Negotiable Rules"** — cross-check each rule for a life-systems flavor

You do NOT need to read every file end-to-end. Grep aggressively for likely-signal keywords: "prefer", "Sean", "always", "never", "avoid", "don't", "remember", "learned", "note:", "correction:", "memory:", "FYI".

</sources_to_consult>

<what_counts>

A pattern is worth codifying if it meets ONE of these criteria:

1. **Operational facts that keep agents from failing** (the Alienware ICMP example). Things where an agent would burn time or money without this knowledge.
2. **Communication preferences Sean has expressed or corrected toward** (framing, terseness, tone, opt-in vs opt-out, questions vs recommendations).
3. **Linguistic decodes** — shorthand, informal phrases, or idioms Sean uses that agents would misread (the "maybe later" example).
4. **Non-obvious constraints** — budget caps, time windows, tools he won't use, things he won't delegate.
5. **Anti-patterns he's explicitly rejected** — approaches that burned time, failed experiments, abandoned tools.
6. **Decision defaults** — how Sean resolves common ambiguities in this domain (e.g., "when in doubt, log to vault and ask tomorrow").
7. **Identity / values signals** — things that explain the "why" behind rules (e.g., "Sean is in a career-transition window, so advice should weight reversibility").

</what_counts>

<what_doesnt_count>

Filter these out — they're noise:

- Generic LLM best practices ("be clear," "give context")
- Universal human preferences ("people like short emails")
- Inferences from one-off messages with no corroboration in files
- Things that ARE true of Sean but are better captured elsewhere (identity facts belong in `Sean-Winslow-Full-Personal-Context`, schedule facts belong in `HEARTBEAT.md`)
- Anything where your source is your own assumption, not the file you read

If you're tempted to write something and you can't cite a source, leave it out.

</what_doesnt_count>

<examples>

## Good (the shape we want)

```
- Alienware ICMP blocked — use HTTP not ping.
  Source: `agents-sdk/lib/hybrid_router.py` + CHANGELOG v3.14.1 (WOL verify fail).
  Domain flavor: life-systems agents (daily_driver) share this router.
```

```
- Budget caps are load-bearing, not suggestions. Sean hit the $0.25 cap and the
  correct fix was to raise the cap, not retry harder.
  Source: CHANGELOG v3.12.2 "Daily driver morning agent hitting budget cap."
  Domain flavor: life-systems (daily-driver is the morning life-systems agent).
```

```
- "Maybe later" from Sean means: capture to vault inbox, don't ask again today.
  Source: `.claude/skills/productivity:task-management/SKILL.md` pattern + TASKS.md behavior.
```

## Bad (do NOT produce output like this)

```
- Sean likes when responses are well-structured.
  Source: general vibe.
```
Too generic, no citation, not life-systems-specific.

```
- Sean prefers the Mac Mini for always-on tasks.
  Source: CHANGELOG v3.14.3.
```
True but this is infrastructure, not life-systems. Out of scope.

```
- Sean is 33 years old and lives in Boston.
  Source: personal context file.
```
Identity fact, not a "learned pattern." Belongs in the personal context file, not SOUL.md.

</examples>

<output_format>

Produce exactly this structure. Markdown. No preamble, no postamble beyond the structure.

```markdown
# Layer 4, Q7 — What Claude/Agents Have Learned About Sean (life-systems)

## Tier A — High confidence (explicit in files, directly cited)

- [pattern]
  Source: [exact file path + line or section if helpful]
  Why it matters: [one sentence]

[... more entries ...]

## Tier B — Medium confidence (inferred from multiple weak signals)

- [pattern]
  Sources: [list]
  Why it matters: [one sentence]
  **Sean: please confirm.**

[... more entries ...]

## Tier C — Candidates to discuss (I noticed something but I'm not sure)

- [observation]
  Where I saw it: [source]
  Question for Sean: [what you'd want him to clarify]

## Coverage gaps I noticed

- [what I expected to find but didn't]
- [directories that were sparse or empty]
- [places where memory SHOULD be codified but isn't yet]

## Stats

- Files searched: [count]
- Files with relevant signal: [count]
- Tier A items: [count]
- Tier B items: [count]
- Tier C items: [count]
```

**Rules for the output:**
- Tier A must have a specific file citation. If you can't cite, demote to Tier B.
- Tier B items must include "Sean: please confirm." on their own line so he can't miss them.
- Tier C is for "I saw something interesting but I need you to tell me what it means." Keep it short.
- "Coverage gaps" is where you note what's missing — this is actually high value for Sean.
- Stats section helps Sean trust the effort.

</output_format>

<validation>

Before presenting, self-check:

1. Did you actually read (not just list) the top 4 sources from `<sources_to_consult>`? If you skipped any, say so.
2. Does every Tier A item have a real file citation? If not, demote.
3. Did you include anything from out-of-scope domains (The Block, Creative Studio, pure infrastructure)? If so, remove.
4. Did you write anything you can't cite? If so, remove or demote to Tier C with an honest "I'm not sure."
5. Is the output pasteable as-is into a markdown file? No extra fences, no narrative around it.

If any check fails, fix before presenting.

</validation>

<final_instruction>

Begin now. Do discovery first (read/grep across the sources), then curate, then present. Do not write to any file. Output goes in the chat for Sean to review and paste himself.

</final_instruction>
```

---

**Why the prompt is structured this way** (prompt engineering notes):

- **Role** makes Claude Code an archivist (curator), not an advisor. Prevents it from inventing new preferences Sean never expressed.
- **Scope block** with explicit in/out filters is the most important piece — without it, Claude Code will bleed into The Block + Creative Studio items because life-systems overlaps everything.
- **Sources ordered by signal strength** so if Claude Code has to make tradeoffs, it reads the high-signal files first.
- **What counts / doesn't count** is two-sided — positive criteria + negative filters — because pattern-surfacing tasks fail in both directions (too broad → noise, too narrow → misses real items).
- **Tiered output (A/B/C)** matches how memory actually accumulates — some things are well-documented, some are half-true, some are just pattern-matches Claude noticed. Forcing the tiers prevents Claude Code from presenting low-confidence items as facts.
- **Coverage gaps section** is the sneaky-valuable output — it tells you where memory *should* exist but doesn't yet, which feeds directly into your Phase 6 Knowledge Compounding Loop.
- **Stats at the end** give you a trust signal — if Claude Code searched 3 files and produced 40 items, that's different from searching 200 files and producing 10.