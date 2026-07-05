# WWF5D — Task Battery (Fable-vs-Opus diff)

> Each task lists matched, reproducible inputs so Fable and Opus get identical context.

WWF5D ("What Would Fable 5 Do") reverse-engineers Fable 5's cognition into a
portable recipe set Opus and Sonnet can inherit after Fable's context window
closes. Per constraint F1 (`docs/plans/2026-07-04-fable5-audit-campaign.md`),
a model's self-report of its own reasoning is unreliable — Fable's
introspection answers (`docs/plans/wwf5d/introspection-protocol.md`) are
hypotheses, not evidence. The **only** admissible evidence is a behavioral
delta: Fable's output vs. the Opus baseline on the *identical* task. That
makes this doc's job load-bearing, not clerical — if the two runs don't see
the same inputs, any difference in output is confounded by input drift, not a
signal about how the two models actually reason.

So every task entry below pins everything a fresh session needs to reproduce
the run byte-for-byte: the exact harness skill file, exact input file paths,
exact git SHAs, the grounding answers each harness's own hard gate demands
(these are part of the matched input — a harness that free-associates its own
answers to "For/Feeds/Disappoints/Wow" or "recurring/tried/coherent" is no
longer running the same task on the second pass), and the exact run prompt a
fresh session executes. Pin drift between the Opus run (now) and the Fable
run (Phase B) is noise the validation step can't distinguish from real
capability difference — so nothing here is left to the runner's judgment.

**Repo pins used throughout:**

| Repo | Branch/path | SHA |
|---|---|---|
| `code-brain` | branch `feat/fable5-campaign` | `93e5725` (`93e57258347a063e4a819f2ded95c884918013b2`) |
| `anima` | local path `/Users/seanwinslow/Code-Brain/anima` | `aa2007c` (`aa2007c1b7dbfbb058fa7580f8cab3ef705ad8df`) |

**Index:**

| Task | Title | Tier | Baseline |
|---|---|---|---|
| BT1 | skill-audit on `intent-engineering` | CORE | `baselines/bt1-opus.md` |
| BT2 | zoom-out-and-think on anima's register-transport seam | CORE | `baselines/bt2-opus.md` |
| BT3 | creative-chain seam audit (double duty) | CORE | `baselines/bt3-opus.md` |
| BT4 | PRD/tech-spec via `prd-generator` | OPTIONAL | none this window |
| BT5 | systematic-debugging root-cause | OPTIONAL | none this window |

---

## CORE — run all three; a baseline is generated for each

## BT1 — skill-audit on `intent-engineering`

1. **Harness:** `.claude/skills/skill-audit/SKILL.md` @ `93e5725`.

2. **Pinned inputs:**
   - Target: `.claude/skills/intent-engineering/SKILL.md` @ `93e5725`.

3. **Pinned grounding answers** (skill-audit's Step 1 hard gate, (a)–(d) — use verbatim, do not re-derive):
   - **(a) For:** design/review/retrofit intent specs for agents and skills; the "carry the why" backbone of Sean's whole agent fleet.
   - **(b) Feeds:** skill-audit's Step-5 spec output and zoom-out-and-think's spec output (both reference it by name), every agent build, the local intent-engineering MCP tools.
   - **(c) Disappoints:** the 9-section template is heavyweight for small retrofits; retrofit levels are fuzzy in practice (when is Level 1 enough?); the validation checklist exists but nothing forces it to run.
   - **(d) Wow:** specs that survive three handoffs (Fable→Opus→subagent) with zero intent drift, right-sized per retrofit level, validation actually gating.

   **Note:** `docs/plans/wwf5d/tier1-specs/intent-engineering.md` is a separate artifact — the Task 4 elevation DRAFT (different purpose: a strong draft spec for Fable to elevate in Phase B). BT1's baseline must be a fresh diff-evidence run using only this doc's pinned context. Runners must not read the `tier1-specs/` directory — doing so would let the audit see (and anchor on) a prior audit's conclusions instead of producing independent evidence.

4. **Run prompt** (self-contained; copy verbatim into a fresh session — code-brain checked out at `93e5725`, branch `feat/fable5-campaign`; use `git show 93e5725:<path>` for either file if the working tree has moved past this commit):

   > Read and follow `.claude/skills/skill-audit/SKILL.md` at git SHA `93e5725` in the `code-brain` repo (branch `feat/fable5-campaign`). Its audit target is `.claude/skills/intent-engineering/SKILL.md`, same SHA. Do not read `docs/plans/wwf5d/tier1-specs/intent-engineering.md` or any other prior audit or improvement spec for this skill — this must be an independent, fresh diff-evidence run.
   >
   > Skill-audit's Step 1 is a hard gate that normally requires asking the user four grounding questions — (a) For, (b) Feeds, (c) Disappoints, (d) Wow — before scanning anything. For this run, the answers are pre-pinned: read `docs/plans/wwf5d/task-battery.md`, section "BT1 — Pinned grounding answers," restate your understanding of each answer back in your output (per the skill's own restate-and-confirm instruction), then proceed directly to Step 2 (Seam Scan) without asking the user anything.
   >
   > Produce both of skill-audit's Step-5 artifacts in full: the severity-tagged Seam Report (every finding tagged exactly one of `dangerously-wrong` / `structural` / `minor`) and the Intent-Carrying Improvement Spec (Objective, Desired Outcome, per-finding fix-with-reasoning, What NOT to Change). Write your complete output — restated grounding answers plus both artifacts — to a single markdown file.

5. **Baseline:** `docs/plans/wwf5d/baselines/bt1-opus.md`.

## BT2 — zoom-out-and-think on anima's register-transport / per-register model-routing seam

1. **Harness:** `.claude/skills/zoom-out-and-think/SKILL.md` @ `93e5725`.

2. **Pinned inputs** (`anima` repo @ `aa2007c`, local path `/Users/seanwinslow/Code-Brain/anima`):
   - `docs/active/2026-07-04-register-backlog-and-transport-findings.md` (the field report)
   - `registers/90s-nicktoon-grossout/` (register doc + refs)
   - `registers/primal-sketch-grit/` (register doc + refs)
   - `pipeline/registers.py` (routing code as-built)

3. **Pinned grounding answers** (zoom-out-and-think's Step 1 hard gate, (a)–(c) — use verbatim, do not re-derive). These were tightened against the field report; see this doc's companion report for the verbatim before/after and why:
   - **(a) Recurring:** register transport gets decided per-register by ad hoc spike rather than through one routing seam — `pipeline/registers.py` currently hardcodes `generation_model=NB2_FLASH` for every one of its seven registers; the pipeline's universal default (NB2) fails to render `primal-sketch-grit`'s Tartakovsky-*Primal* grit and specifically cannot edit a frame into it (a four-engine test confirmed this is a model limit, not a style limit); and for any register whose transport escalates away from NB2 (e.g., to gpt-image), that model's ability to hold identity across the edit-pipeline's handoffs (anchor→turnarounds→expressions) is unvalidated — a real open risk the field report flags, not yet a confirmed failure.
   - **(b) Tried:** universal NB2 as the hardcoded default for every register (confirmed in `pipeline/registers.py`); per-register prompt nudges (e.g., `90s-nicktoon-grossout`'s gross-up-ratio correction after Sean rejected the first draft's constantly-grotesque output); per-register look-spikes ratified case-by-case (the `primal-sketch-grit` go/no-go spike, the `90s-nicktoon-grossout` cross-engine spike — see field report §1, §4, §6).
   - **(c) Coherent/correct end-to-end:** per-register model routing — each register rendered by the model that can actually hold its look, with `RegisterSpec.generation_model` / `final_model` populated as a first-class architectural decision ("the deliverable, not a comment," per the field report) rather than a default nobody revisits — and identity validated across every edit-pipeline handoff before a register's first costed Bible pass, so the routing decision lives in one place (`pipeline/registers.py`) instead of scattered per-register patches.

   **Note:** the baseline runner reads ONLY the four pinned anima paths above plus this doc — nothing else in anima. This is diagnosis and spec only; implementation is out of scope (Opus implements in Phase C). The anima repo is read-only for this task — never modify it.

4. **Run prompt** (self-contained; copy verbatim into a fresh session — code-brain checked out at `93e5725` for the harness; anima checked out at `aa2007c`, local path `/Users/seanwinslow/Code-Brain/anima`, read-only, for the subsystem):

   > Read and follow `.claude/skills/zoom-out-and-think/SKILL.md` at git SHA `93e5725` in the `code-brain` repo (branch `feat/fable5-campaign`). The subsystem under diagnosis is anima's register-transport / per-register model-routing seam, in the `anima` repo at git SHA `aa2007c` (local path `/Users/seanwinslow/Code-Brain/anima` in this environment). Read exactly these four anima paths at that SHA — nothing else in anima:
   > - `docs/active/2026-07-04-register-backlog-and-transport-findings.md`
   > - `registers/90s-nicktoon-grossout/` (research.md + refs)
   > - `registers/primal-sketch-grit/` (research.md + refs)
   > - `pipeline/registers.py`
   >
   > anima is read-only for this task: do not edit, stage, or commit anything in it.
   >
   > Zoom-out-and-think's Step 1 is a hard gate that normally requires asking the user three grounding questions — (a) What keeps recurring, (b) What's been tried, (c) What "coherent/correct" looks like end-to-end — before reading the subsystem. For this run, the answers are pre-pinned: read `docs/plans/wwf5d/task-battery.md`, section "BT2 — Pinned grounding answers," restate your understanding of each back in your output, then proceed directly to Step 2 (Read the Whole System) without asking the user anything.
   >
   > This is diagnosis and spec only. Produce: the Step 2 system map (state / control flow / orchestration, plus the `intended-vs-implemented` comparison — the field report's documented intent vs. what `pipeline/registers.py` actually does today), the Step 3 best-practice research citation(s) for per-content-type generative-model routing (a real web search, not a skipped step), the Step 4 single-sentence root cause, and the Step 5 Intent-Carrying Spec (Real ask, Root cause, Change, What NOT to change). Write your complete output to a single markdown file.

5. **Baseline:** `docs/plans/wwf5d/baselines/bt2-opus.md`.

## BT3 — creative-chain seam audit (double duty)

1. **Harness:** `.claude/skills/skill-audit/SKILL.md` @ `93e5725`, applied CHAIN-LEVEL — the audit target is the whole five-stage Substack writing chain, not any single skill.

2. **Pinned inputs** @ `93e5725` (retrieve via `git show 93e5725:<path>` if the working tree has moved past this commit):
   - `.claude/skills/storytelling-architecture/SKILL.md`
   - `.claude/skills/substack-value-engine/SKILL.md`
   - `.claude/skills/writing-voice-modes/SKILL.md`
   - `.claude/skills/writing-critique/SKILL.md`
   - `.claude/skills/writing-humanity-pass/SKILL.md`

3. **Pinned grounding answers** (skill-audit's Step 1 hard gate, (a)–(d), reframed chain-level — use verbatim, do not re-derive):
   - **(a) For:** the writing chain turns an idea into a published Substack post through five stages; taste/intent decided early (beat map, value verdict, voice choices) must survive to the end.
   - **(b) Feeds:** the published post + Sean's portfolio; each stage feeds the next.
   - **(c) Disappoints:** stages re-derive earlier decisions instead of consuming them; the 2026-07-04 Opus first-pass added named handoff artifacts (open-loop ledger, Handoff Block, locked takeaway, Value Gate verdict, critique fix list) — the open question is what STILL leaks, especially across the locked voice stage (`writing-voice-modes` is Tier-1: proposals may target the chain around it, never its voice content).
   - **(d) Wow:** a single thread of intent from beat map to published post with zero re-derivation and zero silent drops.

4. **Run prompt** (self-contained; copy verbatim into a fresh session — code-brain checked out at `93e5725`, branch `feat/fable5-campaign`):

   > Read and follow `.claude/skills/skill-audit/SKILL.md` at git SHA `93e5725` in the `code-brain` repo (branch `feat/fable5-campaign`). Apply it CHAIN-LEVEL: the audit target is the whole five-stage Substack writing chain, not any single skill. Read these five files at the same SHA (`git show 93e5725:<path>` if your working tree has moved past this commit):
   > - `.claude/skills/storytelling-architecture/SKILL.md`
   > - `.claude/skills/substack-value-engine/SKILL.md`
   > - `.claude/skills/writing-voice-modes/SKILL.md`
   > - `.claude/skills/writing-critique/SKILL.md`
   > - `.claude/skills/writing-humanity-pass/SKILL.md`
   >
   > Skill-audit's Step 1 is a hard gate that normally requires asking the user four grounding questions — (a) For, (b) Feeds, (c) Disappoints, (d) Wow — before scanning anything. For this run, the answers are pre-pinned: read `docs/plans/wwf5d/task-battery.md`, section "BT3 — Pinned grounding answers," restate your understanding of each back in your output, then proceed directly to the chain-level Seam Scan without asking the user anything.
   >
   > Hard constraint: `writing-voice-modes` is Tier-1. Your findings and spec may target how the chain hands work TO or FROM it (the seam on either side), but must never propose changing its locked voice content (Sean Mode or the four borrowed-author techniques) itself.
   >
   > Walk the chain in order — storytelling-architecture → substack-value-engine → writing-voice-modes → writing-critique → writing-humanity-pass — and find every handoff where a decision made early (beat map, Value Gate verdict, voice choice, critique fix list) could be silently re-derived or dropped by a later stage instead of consumed. Produce: a chain-level Seam Report (one bulleted finding per handoff, each tagged exactly one of `dangerously-wrong` / `structural` / `minor`, naming the specific stage-pair and the concrete failure a reader would observe) and one Intent-Carrying Improvement Spec for chain-level fixes (Objective, Desired Outcome, per-finding fix-with-reasoning, What NOT to Change). Write your complete output to a single markdown file.

5. **Baseline:** `docs/plans/wwf5d/baselines/bt3-opus.md`.

---

## OPTIONAL — candidate pinned only; no baseline generated this window

## BT4 — PRD/tech-spec via `prd-generator`

Harness: `prd-generator` skill (interview-driven — its own interview is the grounding step; no Q&A is pre-pinned here). Candidate: fusion-discovery-council PM3 t1 re-run + trend-compare feature — re-run the standard-tier "AI coding assistants" topic and compare verified-pain frequency/intensity against the persisted t0 bundle `vault/20_projects/research/.discovery-sessions/pm3-t0-ai-coding-assistants-2026-06-30.json` (t0: 2026-06-30, 93 evidence records, 8 verified, 2 dropped, $1.85; re-run due ~2026-07-21 per `vault/00_inbox/tickets.md`). No Opus baseline generated this window — the candidate is pinned so Phase B can run it if the window holds.

## BT5 — systematic-debugging root-cause

Harness: `systematic-debugging` skill (its own investigation loop is the grounding step; no Q&A is pre-pinned here). Candidate: Vault Synthesizer / knowledge-lint Tier-2 intermittency when the MBP is asleep — Wake-on-LAN was retired as a fix path, and per-agent skip-and-continue logic (`agents-sdk/agents/vault_synthesizer.py`, `agents-sdk/agents/knowledge_lint.py`) has papered over the underlying reachability gap rather than resolving it. No Opus baseline generated this window.

---

**Next steps (outside this doc's scope).** Step 2 (baseline generation): for BT1–BT3, run each task's exact Run Prompt now, in a fresh session per task, and save the full output to the Baseline path listed. Step 3 (verify) and the validation harness / Phase-B Fable runbook are separate WWF5D artifacts (Task 7).
