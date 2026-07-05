# WWF5D Round 2 — Task Battery (Fable-vs-Opus diff)

> Each task pins matched, reproducible inputs so the Fable blind run and the Opus baseline
> get **identical** context. Per F1, the only admissible evidence is a behavioral delta on the
> *identical* task — if the two runs don't see the same inputs, any output difference is input
> drift, not a signal. So nothing here is left to the runner's judgment.

**Mechanism (Round 2):** each task is dispatched **twice from one orchestrator** — a
`model:"opus"` subagent (baseline) and a `model:"fable"` subagent (blind), with the **identical
run prompt**, in parallel over the same working-tree snapshot. This is the proven Phase-B
subagent pattern (kills pin-drift; no `/clear` needed — subagent isolation holds blindness).
Both subagents **return their complete output as their final message**; the orchestrator writes
each to disk (capture-first) before diffing. See [`round2-session-driver.md`](round2-session-driver.md).

**Repo pins (working tree; the Cowork sandbox cannot commit, so subagents read the working tree as-is at these SHAs):**

| Repo | Path (Read/Grep/Glob) · (Bash mount) | Branch | SHA |
|---|---|---|---|
| `code-brain` | `/Users/seanwinslow/Code-Brain/code-brain` · `/sessions/gallant-amazing-ptolemy/mnt/code-brain` | `feat/fable5-phase-b` | `9dca7ab` |
| `sw-ai-pm-portfolio` | `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio` · `/sessions/gallant-amazing-ptolemy/mnt/sw-ai-pm-portfolio` | `main` | `001d54d` |

**Index:**

| Task | Title | Premium axis | Harness | Raw outputs |
|---|---|---|---|---|
| RT1 | preserve-session fix-spec | spec-decidedness + intent (§6) | `intent-engineering` | `rt1-opus.md` / `rt1-fable.md` |
| RT2 | ceiling-probe: skill-audit on `hooks-configuration` | existence-check / false-safety (§2.4) | `skill-audit` | `rt2-opus.md` / `rt2-fable.md` |
| RT3 | portfolio explainer-graphics enhancement spec | proactive-research + shape-grounding | intent-engineering scaffold + research | `rt3-opus.md` / `rt3-fable.md` |

**Shared blind-run guard (in every run prompt):** the subagent must NOT read any `bt*` or `rt*`
file under `docs/plans/wwf5d/` (prior audits, baselines, blind runs, or diffs) except the one
input file each task explicitly pins — those carry prior conclusions and would break the
independent-evidence condition.

---

## RT1 — preserve-session fix-spec

1. **Harness:** `.claude/skills/intent-engineering/SKILL.md` (code-brain working tree @ `9dca7ab`).

2. **Pinned inputs:**
   - `.claude/skills/preserve-session/SKILL.md` (the skill to fix)
   - `.claude/skills/resume-session/SKILL.md` (its consumer — the read half)
   - `docs/plans/wwf5d/round2/rt1-preserve-session-findings.md` (the shared, neutral consolidated findings — the ONLY `docs/plans/wwf5d/` file this task reads)

3. **Pinned grounding** (pre-answered; the runner restates then proceeds — do not re-derive):
   - **(a) For:** Sean runs `preserve-session` at the end of a work session (most often in code-brain, any project with a CLAUDE.md) to hand off session state with zero loss to a future session — possibly a cheaper model, possibly himself after a break. It is the WRITE half; `resume-session` is the READ half.
   - **(b) Feeds:** `resume-session` (reads what preserve wrote); a human reading CLAUDE.md; three destinations — the project CLAUDE.md `## Session Log`, the vault project note under `vault/20_projects/` (`ai-context`, `<!-- status-update -->`, decisions table, blockers), and today's daily note `<!-- claude-sessions -->`. The repo also has SessionStart inject hooks + a SessionEnd flush hook in the same area.
   - **(c) Disappoints:** resume next session misses captured items; Sean can't tell whether the vault/daily writes landed or silently did nothing; it always reports "saved" but the hand-off is lossy.
   - **(d) Wow:** a future session (or resume-session) reconstructs exactly where he was with zero loss, in the shape the reader reads, with per-destination confirmation that each write truly landed or was skipped-with-a-reason.

4. **Run prompt** (self-contained; dispatched verbatim to one `model:"opus"` and one `model:"fable"` subagent):

   > You are a fresh subagent with no prior context. Work only from this prompt and the `code-brain` repo (Read/Grep/Glob root `/Users/seanwinslow/Code-Brain/code-brain`; Bash mount `/sessions/gallant-amazing-ptolemy/mnt/code-brain`; if a path doesn't resolve with one tool, try the other). Do NOT ask questions — grounding is pre-supplied. Do NOT read any `bt*` or `rt*` file under `docs/plans/wwf5d/` **except** the one findings file named below (blind-run isolation).
   >
   > Task: author the **definitive intent-carrying fix spec** for the `preserve-session` skill. Use `.claude/skills/intent-engineering/SKILL.md` as your spec scaffold (its scaffolding, sized to a contained fix — the four-element floor plus done-criteria; scale up only if warranted). You are NOT re-auditing: the findings are given.
   >
   > Read: `.claude/skills/preserve-session/SKILL.md` (the skill to fix), `.claude/skills/resume-session/SKILL.md` (its consumer), and `docs/plans/wwf5d/round2/rt1-preserve-session-findings.md` (a neutral consolidated list of findings from two prior audits — treat every finding as given). You may read anything else in the repo the findings reference (the real hooks in `.claude/hooks/`, `.claude/settings.json`, `vault/20_projects/` structure, the daily-note template) to make the spec concrete.
   >
   > Grounding for the skill (restate your understanding of each in your output, then proceed): (a) For — Sean runs preserve-session at session end to hand off state with zero loss to a future session; it is the WRITE half, resume-session is the READ half. (b) Feeds — resume-session + a human reading CLAUDE.md; three destinations (project CLAUDE.md `## Session Log`; the vault project note's `ai-context`/`<!-- status-update -->`/decisions table/blockers; today's daily note `<!-- claude-sessions -->`); SessionStart inject hooks + a SessionEnd flush hook operate nearby. (c) Disappoints — resume misses captured items; can't tell if vault/daily writes landed; always reports "saved" but the hand-off is lossy. (d) Wow — zero-loss reconstruction in the reader's shape, with per-destination confirmation that each write landed or was skipped-with-a-reason.
   >
   > Emit ONE intent-carrying fix spec with, at minimum: **Objective** (the problem + why it matters, from the grounding); **Desired outcome** (owner-observable before→after); **The change, per finding** (for each dangerously-wrong/structural finding: the specific change PLUS the reasoning a weaker implementing model needs to make the same call on an edge case the spec didn't enumerate; minor findings may be brief); **Done looks like** (checkable statements — greps/tests/exact behaviors); **What NOT to change** (confirmed-correct, with why). The findings file names two genuine owner-forks (missing-vault-note handling; flush-hook coexistence) — handle each explicitly: pre-make it only if the record already decides it, otherwise surface it with a recommendation and its contingency, never a bare menu and never a silent pick. Return your complete output — restated grounding + the full spec — as your final message. Do not write any file.

5. **Raw outputs:** `docs/plans/wwf5d/round2/rt1-opus.md` (baseline), `docs/plans/wwf5d/round2/rt1-fable.md` (blind). **Diff:** `rt1-diff.md`.

---

## RT2 — ceiling-probe: skill-audit on `hooks-configuration`

1. **Harness:** `.claude/skills/skill-audit/SKILL.md` (code-brain working tree @ `9dca7ab`).

2. **Pinned inputs:**
   - Target: `.claude/skills/hooks-configuration/SKILL.md`
   - The audit may (and should) existence-check the skill's claims against the real surface: `.claude/hooks/` (15 scripts) and `.claude/settings.json` (which hooks are actually registered, on which matchers).

3. **Pinned grounding** (skill-audit's Step-1 hard gate (a)–(d); pre-answered — restate then proceed):
   - **(a) For:** creating, configuring, and debugging Claude Code hooks that enforce security policy and automate quality checks across Sean's fleet — the deterministic enforcement layer (15 hooks live in `.claude/hooks/`, registered in `.claude/settings.json`).
   - **(b) Feeds:** a weaker model following this skill writes real enforcement hooks the fleet depends on — actual `.claude/hooks/*.{py,sh}` scripts and their `.claude/settings.json` registrations; the exit-code contract other tools trust.
   - **(c) Disappoints:** a hook that looks configured but doesn't actually block what you think — a bypassable firewall, a hook that isn't registered, a hook type/matcher that doesn't fire the way the doc claims. You trust "enforced" and it isn't.
   - **(d) Wow:** every enforcement claim in the skill is verifiably true against this repo's real hooks + settings.json; following it produces a hook that provably blocks (proven, not asserted); and it flags the false-sense-of-safety patterns instead of teaching them.

4. **Run prompt** (self-contained; dispatched verbatim to one `model:"opus"` and one `model:"fable"` subagent):

   > You are a fresh subagent with no prior context. Work only from this prompt and the `code-brain` repo (Read/Grep/Glob root `/Users/seanwinslow/Code-Brain/code-brain`; Bash mount `/sessions/gallant-amazing-ptolemy/mnt/code-brain`; if a path doesn't resolve with one tool, try the other). Do NOT ask questions — grounding is pre-supplied. Do NOT read any `bt*` or `rt*` file under `docs/plans/wwf5d/` (blind-run isolation).
   >
   > Read and follow `.claude/skills/skill-audit/SKILL.md`. Its audit target is `.claude/skills/hooks-configuration/SKILL.md`. Audit the skill's design the way its most demanding consumer would; you are NOT rewriting it.
   >
   > Skill-audit's Step 1 is a hard gate that normally asks four grounding questions; for this run they are pre-pinned — restate your understanding of each in your output, then proceed directly to the scans without asking anything: (a) For — creating/configuring/debugging Claude Code hooks that enforce security + automate quality across the fleet's deterministic enforcement layer (15 hooks in `.claude/hooks/`, registered in `.claude/settings.json`). (b) Feeds — a weaker model following this skill writes real enforcement hooks the fleet depends on (actual `.claude/hooks/*` scripts + their `.claude/settings.json` registrations + the exit-code contract). (c) Disappoints — a hook that looks configured but doesn't actually block what you think (bypassable firewall, unregistered hook, a hook type/matcher that doesn't fire as claimed); you trust "enforced" and it isn't. (d) Wow — every enforcement claim is verifiably true against this repo's real hooks + settings.json, following it provably blocks, and it flags false-sense-of-safety patterns instead of teaching them.
   >
   > You have full read access to the repo — use it: existence-check the skill's claims against the actual `.claude/hooks/` scripts and `.claude/settings.json` registrations before believing them (does a taught mechanism actually block? is a claimed hook type/matcher real and wired? does an "enforced" pattern hold, or is it bypassable?).
   >
   > Produce both of skill-audit's Step-5 artifacts in full: the severity-tagged Seam Report (every finding tagged exactly one of `dangerously-wrong` / `structural` / `minor`, naming section/step + the seam/adapter/gap + the concrete failure the owner would observe) and the Intent-Carrying Improvement Spec (Objective, Desired Outcome, per-finding fix-with-reasoning, What NOT to Change). Return your complete output — restated grounding + both artifacts — as your final message. Do not write any file.

5. **Raw outputs:** `docs/plans/wwf5d/round2/rt2-opus.md` (baseline), `docs/plans/wwf5d/round2/rt2-fable.md` (blind). **Diff:** `rt2-diff.md`.
   **Ceiling watch-for (orchestrator, in the diff):** did the Fable arm catch the existence-check / false-sense-of-safety class of finding (the unverified "enforced" claim), or did its BT1 blind spot recur? This task is also handed to Step 4's validation battery (Opus-with-WWF5D vs without on this same prompt) to measure whether §2.4 closes the gap for the deployment models.

---

## RT3 — portfolio explainer-graphics enhancement spec

1. **Harness:** the `intent-engineering` scaffold (for the spec shape) applied to a research-and-ground procedure defined in the run prompt. (Both harness skills live in `code-brain`; the substrate is the portfolio repo.)

2. **Pinned inputs** (`sw-ai-pm-portfolio` working tree @ `001d54d`):
   - `src/components/case-study/ExplainerGraphic.astro` (the registry that swaps a static `<img>` for a per-project interactive component) + `src/scripts/interactive-explainer.ts` (the shared client script)
   - The five existing interactive explainers in `src/components/case-study/`: `AnimationPipelineExplainer.astro`, `IntentExplainer.astro`, `CodeBrainExplainer.astro`, `TheBlockExplainer.astro`, `SixteenBitFitExplainer.astro`
   - The five project case studies they explain: `src/content/work/{animation-pipeline,intent-engineering-mcp,code-brain,the-block,16bitfit}.mdx`
   - **Two pinned exemplars** both arms must work through in depth: **`animation-pipeline`** and **`intent-engineering-mcp`** (the spec gives a system-level elevation pattern + these two worked, so the pattern generalizes to the other three).
   - Available capability (neutral — stated so both arms know the tools exist, not as an instruction to use them): web research via `WebSearch`/`WebFetch` (load via ToolSearch if deferred), and the local animation reference skills (`gsap-scrolltrigger`, `animation-components`, `lottie-animations`, `react-spring-physics`, `animejs`, `locomotive-scroll`).

3. **Pinned grounding** (pre-answered; restate then proceed):
   - **(a) For:** each explainer is the "what this does at a glance" figure between the 4Q and Methods bands on a `/work/<slug>` case study (16:9), aimed at **recruiters** (fast, legible) **and creative technologists** (technically impressive). Sean feels the current ones are sub-par/basic and wants them meaningfully more creative, technical, and attention-grabbing.
   - **(b) Feeds:** the live portfolio (Astro; each renders inside its case study). The enhancement is what a future build implements.
   - **(c) Disappoints:** the current graphics under-sell genuinely strong projects — they read as basic and don't grab the target audience.
   - **(d) Wow:** each graphic makes a recruiter stop AND makes a creative technologist think "how did they do that" — while still clearly communicating what its project actually does.
   - **⚠️ Constraint lifted (Sean, 2026-07-05):** do NOT treat the portfolio's prior "no GSAP / Framer / Lenis" stack note as binding — Sean has reopened it. Any technique or library is on the table (WebGL/shaders, Rive, Three.js, scroll-driven, generative/interactive, Lottie, canvas islands, …). Recommending the right harness + tools is PART of the spec. Ground in the medium (web / Astro / recruiter-facing) and each graphic's communicative intent — not in the retired lock.

4. **Run prompt** (self-contained; dispatched verbatim to one `model:"opus"` and one `model:"fable"` subagent):

   > You are a fresh subagent with no prior context. Work only from this prompt and the `sw-ai-pm-portfolio` repo (Read/Grep/Glob root `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio`; Bash mount `/sessions/gallant-amazing-ptolemy/mnt/sw-ai-pm-portfolio`) plus the code-brain harness skill named below. Do NOT ask questions — grounding is pre-supplied. Do NOT read any `bt*` or `rt*` file under code-brain's `docs/plans/wwf5d/` (blind-run isolation).
   >
   > Task: author an **intent-carrying enhancement spec** for the portfolio's explainer graphics — the "what this does at a glance" figures on the `/work/<slug>` case studies. Sean finds the current ones sub-par/basic and wants them meaningfully more creative, technical, and attention-grabbing, for an audience of **recruiters** (fast, legible) **and creative technologists** (technically impressive). Use `code-brain`'s `.claude/skills/intent-engineering/SKILL.md` as your spec scaffold.
   >
   > Ground first, then propose: read `src/components/case-study/ExplainerGraphic.astro` (the registry), `src/scripts/interactive-explainer.ts`, the five existing `*Explainer.astro` components, and the five `src/content/work/*.mdx` case studies they explain. For EACH graphic, name what it is trying to communicate about its project and to whom — the enhancement must serve that intent, not just add dazzle.
   >
   > Constraint (explicit): you are NOT bound by the portfolio's prior "no GSAP / Framer / Lenis" stack note — Sean has lifted it for this. Any technique or library is on the table (WebGL/shaders, Rive, Three.js, scroll-driven, generative/interactive, Lottie, canvas islands, and beyond); recommending the right harness + tools is part of your job. You have web research available (`WebSearch`/`WebFetch` — load via ToolSearch if they aren't already active) and local animation reference skills (`gsap-scrolltrigger`, `animation-components`, `lottie-animations`, `react-spring-physics`, `animejs`, `locomotive-scroll`) you may consult. Ground your technique choices in the medium (web / Astro / recruiter-facing) and each graphic's intent.
   >
   > Deliverable — one enhancement spec: (1) a **system-level elevation pattern** (the approach, the recommended harness/tooling with reasoning, how it fits the Astro explainer registry, the fallback/perf/accessibility posture, the shared client-script shape); (2) **two worked exemplars in depth** — `animation-pipeline` and `intent-engineering-mcp` — each: its communicative intent, the specific creative-technical realization proposed, the technique/library and WHY it fits, and the concrete before→after a recruiter and a creative technologist would each notice; (3) an intent-carrying spec body (Objective, Desired outcome, the change with reasoning-to-carry per exemplar, What NOT to change, Done-looks-like). Return your complete output as your final message. Do not write any file.

5. **Raw outputs:** `docs/plans/wwf5d/round2/rt3-opus.md` (baseline), `docs/plans/wwf5d/round2/rt3-fable.md` (blind). **Diff:** `rt3-diff.md`. **Extracted deliverable (post-diff):** the winning enhancement spec → `docs/plans/wwf5d/round2/portfolio-explainer-enhancement-spec.md`.

---

## Diff prompt (used per task, after both raw outputs are captured)

For each task, the orchestrator (Opus) compares the two raw outputs against the run's yardstick.
Tag each real quality delta `dangerously-wrong` / `structural` / `minor`, direction **FABLE+**
(admissible WWF5D evidence per F1) or **OPUS+** (ceiling evidence per F3); ignore pure style.
The premium lenses to score against: **spec-decidedness** (pre-made decisions, edge guidance,
done-criteria, pre-make-vs-surface owner-forks), **breadth past the named seams**,
**contract-contradiction** detection, **evidence-discipline / verify-the-world** (incl. RT3's
proactive current-best-practice research + intent-grounding, and RT2's existence-check). Write
each to `rt{n}-diff.md`; jot standouts into [`../fable-learnings-log.md`](../fable-learnings-log.md).

---

**Next (outside this doc):** run per [`round2-session-driver.md`](round2-session-driver.md). Capture beats distill — save every raw output before folding anything into WWF5D.
