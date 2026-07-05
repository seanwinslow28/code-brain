# Creative Partner Memory Layer, Spec (2026-06-30)
## Give the agent a memory so your taste sticks and compounds

**Status:** Design spec, derived from [SOUL.md](SOUL.md) (the partner-then-system arc), [SKILL-PACKAGING-PLAN.md](SKILL-PACKAGING-PLAN.md) §2-3 (the Creative Partner orchestrator), and the 2026-06-30 deep-research pass (the 6-question memory study). It specs (a) the memory layer that extends the Creative Partner, both tiers, and (b) the memory post that demonstrates it. The memory post gets its own Stage 0 pre-flight and full build sheet before it is drafted; this doc is the architecture lock and the post plan, not the capture.

**One-line thesis (Sean's, 2026-06-30):** teaching an agent your taste means nothing if it cannot remember it. Post 1 hands the agent your taste once, through the interview. Memory is what makes it *keep* that taste and get more *you* every session. This is the **partner into system** bridge made concrete: the interview builds the partner, memory is the first piece of system built on top of it.

No em dashes anywhere (folder rule). Anti-hype, demo-first, both tiers, differentiate-never-duplicate.

---

## 0. What the research settled (so we do not relitigate it)

Full readout lives in the 2026-06-30 research synthesis. The load-bearing findings:

1. **The architecture is solved and convergent.** Every serious memory system (the Anthropic memory tool, claude-mem, mem0, Letta/MemGPT, Claude Code auto-memory) is the same shape underneath: a **small durable core + session deltas + a periodic reconcile**. We are not inventing an architecture, we are pointing a proven one at creative taste.
2. **The wedge is wide open.** Style memory exists only as brand-voice SaaS (Jasper, Velocity, Blaze, Kinetik): writing-only, marketing-scale, *ingest-and-lock* (it reads your posts), vendor-owned. General AI memory is saturated and not creative. Nobody ships an **interviewed, personal, multi-craft, you-owned, portable** taste memory wired to a creative partner. That intersection is empty.
3. **Cross-vendor lock-in is the field's biggest failure, and our biggest opening.** ChatGPT memory cannot move to Claude, Claude cannot move to Gemini. So "you own the file and it travels across every model" is not a fallback, it is the selling point.
4. **Bloat is the real enemy, not capacity.** Anthropic's own rule: ruthlessly remove anything the model could reverse-engineer, because a bloated memory makes the model ignore the real instructions. A taste memory that grows without reconciling will *degrade* the output, not improve it.
5. **The moat is already running in the fleet.** code-brain's `agents-sdk/lib/fleet_memory.py` is a `BetaAbstractMemoryTool` subclass with per-agent namespacing and `promote_to_shared()`, a live production instance of Anthropic's memory-tool pattern. Sean operates the architecture, he does not theorize it.

---

## 1. The architecture (one structure, both tiers)

The whole layer is three parts. Everything else is plumbing.

```
.creative-partner/
├── taste.md            # THE DURABLE BLOCK. The 8-field taste-context from Post 1,
│                       #   kept short on purpose (the "ruthlessly remove" rule).
│                       #   This is what loads every session. It is the source of truth.
├── sessions/           # THE DELTAS. One short note per working session:
│   ├── 2026-07-02.md   #   what the partner learned about your taste today
│   └── 2026-07-09.md   #   (a new never-do, a reference you reacted to, a correction pattern).
└── references/         # optional: the 3-5 anchor images / samples the block points at.
```

**1. The durable block (`taste.md`).** Your taste-context block, the exact artifact Post 1 already produces. It is the Core Memory / the always-loaded layer. It stays short (target: fits the Claude Code MEMORY.md ~200-line budget; the shorter it is, the more the model actually obeys it). This is the thing memory is *for*: a durable, you-owned statement of your hand.

**2. The session delta.** Each working session, the partner writes a short note: what it learned about your taste that was not already in the block. A new tell you rejected, a reference that landed, a correction you made twice. Deltas are cheap and append-only. This is the "absorb what you worked on and how" that Sean asked for.

**3. The reconcile step.** Periodically (or at session end), the partner folds the deltas back into `taste.md`: add what is genuinely new, update what changed, drop what is now wrong, keep it coherent and short. This is where compounding actually happens, and it is the step that stops bloat. You stay in control: `taste.md` is a plain file you can read, edit, or delete a line from at any time.

> **The key reframe for the post:** memory is not a new artifact. It is Post 1's taste block, given a folder, a heartbeat, and a discipline. "The interview wrote it once. Memory keeps it true."

---

## 2. The skill tier (the reader leveling up)

The `.creative-partner/` folder, plus an automatic absorb loop, plus a one-command install. Three viable absorb mechanisms, in increasing order of "you own it":

| Mechanism | What it does | Best for | Source |
|---|---|---|---|
| **Claude Code native auto-memory** | `MEMORY.md` + `CLAUDE.md`; on by default; Claude writes notes to itself across sessions, top ~200 lines load | the simplest path, zero install beyond the skill | [Claude Code memory](https://code.claude.com/docs/en/memory) |
| **claude-mem** (recommended default) | SessionEnd captures + compresses the session, SessionStart injects it back; local SQLite; one-command install; runs on Claude Code, Codex, Gemini, **Hermes**, more | the cleanest cross-harness "absorb each session" with a dashboard | [claude-mem](https://github.com/thedotmack/claude-mem) |
| **Anthropic memory tool** (`/memories`) | API-level CRUD memory you back with your own storage; `BetaAbstractMemoryTool`; pairs with compaction | the reader who wants to own the whole stack (this is what the fleet runs) | [memory tool docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool) |

**The Creative Partner skill's job in all three:** at session end, write the taste delta and reconcile `taste.md`; at session start, load `taste.md`. The absorb mechanism (claude-mem or native auto-memory) handles the capture/inject plumbing; the skill owns the *taste discipline* (what is worth remembering, how to reconcile without bloat). That division is the moat: anyone can bolt on claude-mem, only our skill knows what a *taste* delta is and how to keep a taste block coherent.

**Install (Pocock-style, one command):**
```
npx skills@latest add <pencil-and-prompt-repo>/creative-partner
# then, in your agent:
/setup-creative-partner     # scaffolds .creative-partner/, seeds taste.md from your Post 1 block,
                            # wires the SessionEnd/SessionStart absorb loop (claude-mem or native)
```

**MVP for the post:** the `.creative-partner/` scaffold + `taste.md` seeded from the Post 1 interview + the SessionEnd reconcile step. claude-mem as the recommended absorb engine because it is one-command and harness-agnostic. The Anthropic-memory-tool version is the "own the whole stack" sidebar, with the fleet as the worked example, not the required path.

---

## 3. The copy-paste tier (start today, own it forever)

The same three-part structure, run by hand. This is the portable, you-owned version, and per the research it is *more* durable across vendors than any built-in memory, because nothing is locked inside one product.

**The ritual (the MVP a non-coder follows):**
1. **Keep `taste.md`** (your Post 1 block) as a plain note you own.
2. **Paste it at the top of each session** in whatever tool you use. Optional convenience: park it in ChatGPT memory, a Claude Project's knowledge, or a Gemini Gem, but the file stays the source of truth (because those do not port across vendors).
3. **End each session with the maintenance prompt** (ships as the copy-paste artifact):
   > "Based on everything we did this session, update my taste block. Add only what is genuinely new about my taste, what I kept, what I killed, and why. Tighten anything that got long. Do not pad it. Output the full updated block so I can save it back."
4. **Save the output back over `taste.md`.** That is the reconcile step, done by hand.

**Why this is a feature, not a consolation prize:** the built-in memories are opaque (ChatGPT), do not auto-learn (Claude Projects), or are persona presets that do not accumulate (Gemini Gems), and none of them move between vendors. A taste file you maintain works in all of them and survives any of them. The post says this out loud: own your taste, do not rent it.

---

## 4. Update discipline (compound, do not bloat)

The rules that keep the memory getting better instead of louder. These map the research patterns onto a taste profile.

- **Keep the durable block short.** Every line earns its place. If the model could infer it from your references, cut it. (Anthropic's bloat rule, and the MEMORY.md 200-line budget.)
- **Deltas append, the block reconciles.** Never let the block grow by accretion. New learning lands as a delta, then gets folded in deliberately, with contradictions resolved (mem0's ADD/UPDATE/DELETE, the memory tool's `str_replace`).
- **Taste evolves, so memory must support change, not just growth.** When your hand changes, the reconcile updates the rule, it does not stack a second contradictory one. The human owns "this is no longer me."
- **Human-in-control by construction.** `taste.md` is a readable file (skill tier) or a note you hold (copy-paste tier). Edit it, delete a line, forget something. No opaque store deciding for you. This is the direct answer to ChatGPT-memory's opacity.

---

## 5. Differentiation (the value gate, pre-checked)

| They have | We have |
|---|---|
| Brand-voice SaaS (Jasper, Velocity, Blaze, Kinetik): writing-only, marketing-scale, ingest-and-lock, vendor-owned | A **personal creative taste** memory, **interviewed** (not scraped from your posts), **multi-craft** (visual first), **you-owned and portable** (a file, both tiers), **wired to a partner** |
| General AI memory (ChatGPT/Claude/Gemini), opaque or non-portable; Nate's "AI Memory Wall" is org/employment, not creative | The "**own your taste, it travels across every model**" angle, a direct hit on the cross-vendor lock-in everyone else has |

**The one-sentence wedge:** everyone else either remembers your *facts* or scrapes your *posts*; we interview your *taste* and hand you a memory you own that makes any model more you, every session.

**Value gate (the memory post):** Itch is genuinely Sean's (he runs fleet-memory; he lives the "teach it once and it forgets" pain). Transfer is un-covered (nobody ships this). Solution is the captured compounding run (section 6), which clears the gate when shot.

---

## 6. The proof / value-gate capture (design the memory post around this)

The watchable, honest proof is **compounding across sessions**. Capture it as a controlled before/after:

- **Session 1 (no memory):** run a fresh creative ask cold-ish, count the **correction turns** to reach "that is mine." Save the count.
- **Session 3 (memory on):** run a *different* fresh ask. The partner should land closer with **fewer correction turns**, and ideally **volunteer a remembered rule unprompted** ("I left the construction lines in and skipped the gradient, per your taste"). Screenshot that moment, it is the hero.
- **The number:** correction turns session 1 vs session 3, on comparable asks. Fewer turns = the taste compounded. The analog from the research: Velocity's brand agent "held a recognizable voice across six channels without manual rewriting", consistency-without-resteering is the metric.
- **The honesty beat:** show a reconcile that *dropped* a stale rule, so the post proves memory is curated, not hoarded. Memory that only grows is a liability; we show the pruning.

Capture discipline (same as Post 1): save every session note and the evolving `taste.md`, one line of why per reconcile. The mess is the texture.

---

## 7. The memory post (queue + shape)

**Working title (open):** "Give Your Partner a Memory" / "The Partner That Remembers" / "Teach It Once, It Remembers." Names finalized at the post's own naming beat.

**Where it sits (open decision, recommendation):** the natural **Post 2**, and it can absorb the **Back to Basics #1 ("what is a skill, why .claude is a superpower")** job, because installing the Creative Partner memory IS the worked example that onboards the reader to the technical layer. So Post 2 = the memory post, doubling as the Back to Basics bridge: it teaches the `.claude` / skill / hook layer by giving the reader a memory they can feel. Alternative: keep them separate (memory as a Spine entry, Back to Basics #1 as a lighter standalone). Sean's call; SERIES-COMMAND-CENTER gets updated when locked.

**Format:** Spine + Back to Basics hybrid (demo-first, both tiers, the partner-into-system bridge).

**Both-tier artifacts it ships:**
1. **Copy-paste kit:** the `taste.md` template (already from Post 1) + the **end-of-session maintenance prompt** + the "park it in ChatGPT/Claude/Gemini, but the file is the source of truth" note.
2. **Skill upgrade:** the Creative Partner skill gains the `.creative-partner/` memory + the SessionEnd reconcile + SessionStart load, installed one-command, claude-mem as the default absorb engine, the Anthropic-memory-tool/fleet version as the "own the stack" sidebar.

**Pre-flight reminder:** the memory post runs its own Stage 0 (CLAUDE.md §8) before drafting, pain + competitive + craft-currency + PM lens + value gate, captured at the top of its build sheet. This spec pre-loads most of it; the build sheet confirms and captures.

---

## 8. The Post 1 teaser (the bridge line)

Post 1 stays the interview + the block. It plants exactly one forward line, at the gift or the closer, no more:

> The interview gets the agent your taste today. Next, we give it a memory, so it keeps your taste and compounds it, session after session. The partner starts becoming a system.

Placement candidate: the closer, right after the Saturday-morning callback, so the reader leaves the flagship with the next post already pulling them. It also earns the masthead's "partner, then system" in one sentence without front-loading the framework.

---

## 9. Open decisions for Sean

1. **Memory-post slot:** Post 2 as a memory + Back to Basics #1 hybrid (recommended), or keep the two separate? Drives the queue order in SERIES-COMMAND-CENTER.
2. **Default absorb engine in the post:** claude-mem (one-command, harness-agnostic, recommended) as the headline, with native auto-memory as the no-install option and the Anthropic memory tool as the own-the-stack sidebar. Confirm the headline.
3. **Where the Creative Partner skill (and its memory) actually ships:** the open question from SKILL-PACKAGING-PLAN §6.1 (a Pencil & Prompt skills repo vs Claude.ai-native vs a plugin). Memory does not change the answer, but it raises the stakes, the folder is the product.
4. **Post 1 teaser wording + placement:** the line above, at the closer, approve or tune.

---

## Sources

- [Claude Code memory](https://code.claude.com/docs/en/memory) · [Anthropic memory tool](https://docs.claude.com/en/docs/agents-and-tools/tool-use/memory-tool) · [claude-mem](https://github.com/thedotmack/claude-mem) · [Claude Agent SDK memory & context](https://github.com/bgauryy/open-docs/blob/main/docs/claude-agent-sdk/memory-and-context.md)
- [ChatGPT vs Claude Projects vs Gemini Gems memory](https://mindlock.io/blog/chatgpt-memory-vs-claude-projects-vs-gemini-gems) · [mem0 vs Letta](https://vectorize.io/articles/mem0-vs-letta) · [CLAUDE.md bloat guidance](https://medium.com/@bijit211987/the-complete-guide-to-claude-md-memory-rules-loading-and-cross-tool-compression-97cc12ed037b)
- [Pocock skills](https://github.com/mattpocock/skills) · [AI brand-voice tools (prior art)](https://noimosai.com/en/blog/top-5-ai-agents-for-brand-voice-consistency-scale-content-without-compromising-quality)
- Fleet worked example: code-brain `agents-sdk/lib/fleet_memory.py` (the `BetaAbstractMemoryTool` subclass, per-agent namespacing, `promote_to_shared()`)
