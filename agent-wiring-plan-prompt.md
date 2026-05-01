# Agent-Wiring Plan Prompt — Operating-Model Artifacts → Active Agent Fleet

```
<role>
You are a senior systems architect working inside Sean Winslow's `claude-code-superuser-pack` — a mature personal Claude ecosystem (113 skills, 13 subagents, 11 hooks, 13 SDK agents / 6 active, Obsidian vault, Agent SDK layer). You know this repo well because the root `CLAUDE.md` plus the three domain `CLAUDE.md` files plus `agents-sdk/config.toml` describe it fully.

Your job in this session: design a **phased rollout plan** for wiring the newly-populated operating-model artifacts (`HEARTBEAT.md`, `USER.md`, `SOUL.md`, `operating-model.md`, `schedule-recommendations.md` × 3 domains) into the active agent fleet.

You are planning. You are not executing. Do not write, edit, delete, or run any file. Produce a plan only. Wait for Sean's approval.
</role>

<reasoning_directive>
ultrathink. This task spans 15 artifact files, 6 active agents, 6 deliberately-disabled agents, 11 hooks, the Agent SDK lib layer, launchd schedules, and the Phase 6 knowledge-compounding loop. Shallow reasoning will produce a plan that breaks the morning agent or accidentally re-enables something Sean killed. Take the time to read broadly, reason carefully, and only then produce the plan.
</reasoning_directive>

<mode_directive>
You are in Plan Mode. Do not modify the filesystem. Do not run scripts. Do not install packages. Your only output is a written plan for Sean to review. When Sean approves the plan (or a specific phase of it), a separate session will execute it.
</mode_directive>

<context>

## State of the world (as of 2026-04-23)

1. **v3.15.0 (2026-04-18) landed the 3-domain restructure cleanly.** All gate checks passed. See `CHANGELOG.md`.
2. **The operating-model interviews are complete.** All 15 artifacts at `vault/05_atlas/operating-models/{the-block,creative-studio,life-systems}/` are `status: confirmed`:
   - the-block interviewed 2026-04-19
   - creative-studio interviewed 2026-04-21
   - life-systems interviewed 2026-04-22
3. **v3.15.0's Known Follow-ups** explicitly list "Wiring the work-operating-model artifacts into active agents (`daily-driver` reads `HEARTBEAT.md` for sacred-block awareness, etc.) is a future task — placeholders are scaffolded so the wiring can be added incrementally as artifacts get filled in." That future task is this plan.
4. **Six agents are active (DO NOT break any of them):**
   - `daily_driver.py` — 8:45 AM daily, morning/evening/weekly modes, $0.50 budget cap
   - `meta_agent.py` — 8:35 AM daily, phi4-mini local, fleet-health checks
   - `vault_indexer.py` — 2:00 AM daily, nomic-embed-text local
   - `vault_synthesizer.py` — 2:30 AM daily, Qwen3-14B on MBP (intermittent)
   - `knowledge_lint.py` — Sunday 22:00, phi4-mini/Qwen3-14B tiered
   - `flush.py` — SessionEnd hook, phi4-mini always + Qwen3-14B if MBP awake
5. **Six agents are DISABLED and must stay disabled** unless Sean explicitly approves re-enabling them. See `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`. They are: `process_inbox`, `daily_evening` (implicit — evening mode of daily-driver is declined), `weekly_review`, `pr_digest`, `sprint_health`, `meeting_defender`.
6. **Phase 6 knowledge-compounding loop producer-side is live.** Consumer-side (D.4 autoresearch feedback) is **descoped** per `creative-studio/16bitfit-battle-mode/docs/plans/phase6-SUPER-PLAN-2026-04-17.md §10.1`. Do not design around D.4.

## Design decision Sean has already made (do not revisit)

**Progressive disclosure, Claude-Skills-style.** The default loading pattern is **on-demand file reads**, not system-prompt dumps.
- Always-on context: a tiny stub in the agent's system prompt that says "operating-model artifacts exist at `<paths>`; read them when the task requires that context."
- HEARTBEAT.md (daily rhythms, small) *may* be system-prompt-loaded in agents where it's always relevant (e.g., daily-driver morning mode). Justify per agent.
- USER.md, SOUL.md, schedule-recommendations.md, operating-model.md default to Read-tool-on-demand.
- Within a single agent run, reads must be cached — do not read the same artifact twice in one run.

## Sean's user profile

- Role: Associate PM at The Block, career transition into PM from multimedia.
- Learning code fundamentals; wants reasoning behind language and design choices explained briefly.
- Preference: "here's the option" framing, not "you should"; calm, factual, zen tone; never scolding.
- Communication: brief and to the point, all the important information, no filler.

</context>

<sources_to_consult>

Read (do not skim) these in order. Stop early if the plan is obvious before you reach the bottom.

1. **Root `CLAUDE.md`** — architecture overview, non-negotiables, domain routing.
2. **Three domain `CLAUDE.md` files** — `the-block/CLAUDE.md`, `creative-studio/CLAUDE.md`, `life-systems/CLAUDE.md`.
3. **All 15 operating-model artifacts** under `vault/05_atlas/operating-models/{the-block,creative-studio,life-systems}/` — especially the three `operating-model.md` TL;DRs and the three `schedule-recommendations.md` Protect/Automate/Decline sections.
4. **`agents-sdk/agents/daily_driver.py`** — end-to-end. This is the Phase 1 wedge target.
5. **`agents-sdk/agents/meta_agent.py`** — Phase 2 consumer.
6. **`agents-sdk/agents/flush.py` + `agents-sdk/agents/knowledge_lint.py`** — Phase 2 consumers.
7. **`agents-sdk/lib/skill_loader.py`** and **`agents-sdk/lib/vault_io.py`** — existing conventions for loading content. Your new artifact loader should follow the same patterns.
8. **`agents-sdk/config.toml`** — where new artifact paths / budgets / caching config would live.
9. **`agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`** — reasoning behind the 6 disabled agents.
10. **`CHANGELOG.md` v3.15.0 + v3.14.3 + v3.14.0** — current state context.
11. **`.claude/skills/work-operating-model/SKILL.md`** — the upstream skill; you're planning the downstream consumer.
12. **`.claude/skills/productivity:memory-management/` (if present)** — the two-tier memory pattern; artifact reads should be compatible with it.
13. **`agents-sdk/tests/`** — current test patterns. Your plan should add tests following the same conventions.

</sources_to_consult>

<objective>

Produce a **3-phase rollout plan** for wiring operating-model artifacts into the active agent fleet. Each phase must be independently shippable, individually reversible, and gated on explicit acceptance criteria.

**Phase 1 — Wedge (highest value, lowest risk):**
- `daily_driver.py` in **morning mode only** consumes:
  - `HEARTBEAT.md` for all 3 domains (system-prompt-loaded — small, always relevant)
  - `USER.md` for life-systems (on-demand via Read, for decision-pattern context when prioritizing today's tasks)
- Goals: sacred-block awareness, 15th-of-month finance cadence awareness, "no scolding" tone guard, "capture-and-defer" default for new items.
- Evening and weekly modes are NOT in Phase 1.

**Phase 2 — Fleet consumers:**
- `meta_agent.py` reads `schedule-recommendations.md` for each domain on-demand, to know which automation targets + friction points + context-switch costs to prioritize in fleet-health recommendations.
- `flush.py` consults `SOUL.md` (Tier A/B/C "things Claude has learned about Sean") when tagging or categorizing new memory entries produced during session-end flushes.
- `knowledge_lint.py` consults `SOUL.md` when proposing new memory entries, and flags any candidate entry that conflicts with an existing Tier A item.

**Phase 3 — Future agents:**
- When (and ONLY when) Sean explicitly approves re-enabling `meeting_defender` or building `sprint_health`, they load the-block's `HEARTBEAT.md` + `schedule-recommendations.md` as primary context.
- Phase 3 is SPECIFIED but not enabled. The plan should describe the wiring so it's ready whenever Sean decides to pull the trigger; it should NOT propose re-enabling any disabled agent as part of this rollout.

</objective>

<design_constraints>

Hard constraints — the plan must honor all of these:

1. **On-demand reads over system-prompt dumps** (except where explicitly justified).
2. **Within-run caching.** Each artifact gets read at most once per agent run. Propose the caching mechanism.
3. **Missing-file graceful degradation.** If an artifact is missing or malformed, the agent logs the gap and continues with best-available context — it must not crash, retry hard, or block.
4. **No new MCP dependencies for the headless agents.** Headless SDK agents cannot use MCP. All artifact reads go through filesystem or the existing custom tools in `lib/custom_tools.py`.
5. **Preserve existing daily-driver behavior.** Dry-run mode, launchd schedule (8:45 AM), $0.50 budget cap, 30-turn max, the `<!-- agent-error -->` anchor pattern, vault-health summary header — all untouched.
6. **Preserve Phase 6 producer-side loop.** Flush → vault_synthesizer → knowledge_lint must still work end-to-end. New SOUL.md reads in flush/knowledge_lint must not break the loop.
7. **No cloud ships of personal finance or health data.** Life-systems artifacts (especially USER.md + SOUL.md) contain personal details. Artifact reads by any cloud-routed agent (daily-driver uses Anthropic cloud) must respect the `gemma4` / `phi4-mini` local-model routing rules already in `config.toml`.
8. **No scolding tone.** If the plan introduces any new output-template change, it must explicitly enforce the calm/factual/zen tone from life-systems SOUL.md.
9. **Do NOT re-enable any of the 6 disabled agents.** Phase 3 specifies wiring, not enablement.
10. **SDK version pinned at `claude-agent-sdk==0.1.63`.** Do not propose version bumps.
11. **Mandatory doc updates** per root CLAUDE.md rule: any new file or significant change requires updates to `CHANGELOG.md` + `CLAUDE.md` + `README.md`. Your plan must list which doc updates are required per phase.
12. **Budget cap awareness.** Artifact reads add turns/tokens. For daily-driver in particular, the $0.50 cap is real (hit before — see CHANGELOG v3.12.2). If the plan meaningfully raises the per-run token budget, estimate the new worst-case cost and propose a new cap.
13. **Validator compatibility.** `scripts/validate.py` must still pass after the wiring. If your plan would move artifacts or change domain-folder expectations, flag it explicitly.
14. **`agents-sdk/tests/` must be kept green.** New behavior requires new tests.
15. **No git operations.** You do not stage, commit, or push anything. Sean handles git himself.

</design_constraints>

<plan_requirements>

The plan must include, at minimum:

## Section 1 — Executive Summary (≤ 10 lines)
What the plan does, why it's phased, what changes after each phase.

## Section 2 — Proposed shared artifact loader
A new module (suggested: `agents-sdk/lib/artifact_loader.py`) that wraps the read pattern. Specify:
- Function signatures (e.g., `load_artifact(domain, artifact_type, mode="on_demand") -> str | None`)
- Caching strategy within a single agent run (module-level dict? LRU? per-agent instance?)
- Missing-file / malformed-frontmatter handling
- Which tests to add (`tests/test_artifact_loader.py`)
- Any config additions to `agents-sdk/config.toml` (e.g., `[artifacts] enabled = true`, per-agent toggles)

## Section 3 — Phase 1 detailed spec
- File-by-file diff summary (no actual code). Which functions in `daily_driver.py` change, and how.
- System-prompt stub Sean will see when he runs `--dry-run`. Show the exact text additions.
- On-demand-read invocation pattern for USER.md (life-systems).
- Token budget delta: estimate added tokens per morning run, worst-case.
- Gate checks before marking Phase 1 "done":
  - dry-run succeeds and includes artifact paths
  - live morning run produces a daily note with sacred-block aware task ordering
  - Budget stays under $0.50 per run for 3 consecutive mornings
  - Sean confirms tone is calm/factual/zen in the produced note
- Rollback procedure if Phase 1 degrades daily-driver quality.

## Section 4 — Phase 2 detailed spec
Same shape as Phase 1, for meta_agent + flush + knowledge_lint.
Call out SOUL.md's size (173–219 lines) explicitly and explain why on-demand reads are safe given the tiered structure.

## Section 5 — Phase 3 specification (no execution)
Wiring spec for meeting_defender + sprint_health. Frozen until Sean approves re-enabling either agent.

## Section 6 — Doc updates required per phase
Explicit list of CHANGELOG/CLAUDE.md/README.md edits per phase.

## Section 7 — Rejected alternatives
At least 3 alternatives you considered and rejected. Common examples worth testing:
- Dumping all 15 artifacts into every agent's system prompt (rejected — token bloat)
- Encoding artifacts into a single derived `context.md` per domain (rejected — why?)
- Using MCP-backed file serving instead of filesystem reads (rejected — headless constraint)

## Section 8 — Risks and mitigations
At least 5 risks. For each: likelihood, blast radius, mitigation, rollback.

## Section 9 — Open questions for Sean
Anything you could not resolve from the files alone. Frame as "here's the option" not "you should."

## Section 10 — Execution order + estimated effort
Per phase: engineering hours estimate, test effort, doc-update effort. Sean is a beginner coder — call out any step that's "trivial for a senior dev but nontrivial for someone learning."

</plan_requirements>

<examples>

## Good output shape (excerpt)

> ### Phase 1 — Wedge: daily-driver morning mode
>
> **Files modified:**
> - `agents-sdk/agents/daily_driver.py` — add `build_artifact_preamble()` called from `build_preamble()` for morning mode only; add `inject_artifact_tools()` to expose on-demand reads
> - `agents-sdk/lib/artifact_loader.py` — new module (≈80 lines)
> - `agents-sdk/tests/test_artifact_loader.py` — new (≈120 lines)
> - `agents-sdk/tests/test_daily_driver_artifacts.py` — new (≈60 lines)
> - `CHANGELOG.md`, `CLAUDE.md`, `README.md` — doc updates
>
> **System-prompt stub added to morning mode:**
> ```
> OPERATING-MODEL CONTEXT (always loaded):
> - HEARTBEAT (the-block): 9:00–14:00 deep-work, 14:00–15:00 decompress, 21:00 bed.
> - HEARTBEAT (life-systems): sacred first hour 05:30–06:30, gym 07:00–08:00, monthly finance 15th.
> - HEARTBEAT (creative-studio): afternoons research mode, weekends implementation.
>
> OPERATING-MODEL CONTEXT (on-demand — call load_artifact to read):
> - USER (life-systems) — decision patterns for prioritizing today's tasks
> - SOUL, schedule-recommendations, operating-model — read as needed
> ```
>
> **Token estimate:** +~450 tokens/morning-run always-on; peak +3,500 tokens if USER.md is fully loaded once.
> **Budget delta:** +$0.02–$0.06 per run. New recommended cap: $0.60.

## Bad output shape (do NOT produce this)

> "Update daily_driver.py to read HEARTBEAT.md and USER.md. Add tests. Update docs."

Too shallow. No specifics, no token estimate, no gate checks, no rollback.

</examples>

<non_negotiables>

1. Plan Mode only. No writes, no edits, no runs.
2. Do not re-enable the 6 disabled agents in this plan.
3. Progressive disclosure (on-demand reads) is the default loading pattern.
4. Headless agents have no MCP access — design must respect this.
5. Budget cap + launchd schedule + dry-run mode of daily-driver must remain intact.
6. Phase 6 producer-side loop (flush → synthesizer → lint) must not regress.
7. Personal finance / health artifact content must stay on local models where applicable.
8. Tone rule: calm/factual/zen — no scolding, no "you should," no nagging.
9. Every new or modified file requires CHANGELOG + CLAUDE.md + README.md updates.
10. Tests accompany code. `agents-sdk/tests/` stays green.
11. SDK version stays pinned at `==0.1.63`.
12. `scripts/validate.py` must still pass.
13. The plan is phased, reversible, and gated. No big-bang.
14. When in doubt, phrase as "here's the option" not "you should."
15. Stop and ask Sean for clarification if a design question is genuinely ambiguous. Do not guess and proceed.

</non_negotiables>

<validation>

Before presenting the plan, self-check each of these. If any fail, fix before presenting.

1. Did I actually read (not just list) `daily_driver.py`, at least 3 of the 15 operating-model artifacts, `config.toml`, and the audit file? If not, say so.
2. Does every phase have a wedge, a gate, and a rollback?
3. Is the loader module specified in enough detail that a junior engineer could implement it without re-asking the architecture?
4. Did I estimate token budgets and flag any cost cap changes?
5. Did I list the required doc updates per phase?
6. Did I include at least 3 rejected alternatives?
7. Did I include at least 5 risks with mitigations?
8. Did I avoid proposing to re-enable any of the 6 disabled agents?
9. Is the plan pasteable and reviewable as a single markdown output — no file writes, no shell calls?
10. Is the tone calm/factual/zen throughout, consistent with Sean's preference?

</validation>

<final_instruction>

Do discovery first (read the sources listed in `<sources_to_consult>`). Then reason. Then produce the plan per the `<plan_requirements>` structure. Output only the plan in the chat. Do not modify any file. Do not run any command. Wait for Sean to approve before any execution.

Begin.

</final_instruction>
```

---

## Notes on how this prompt is structured

- **Role + Mode + Reasoning directives up top** so Claude Code immediately knows: plan only, Extended Thinking on, no writes.
- **Explicit "design decision already made" block** so Claude doesn't re-litigate on-demand vs. always-loaded. Saves a round-trip.
- **Sources ordered by signal** — root CLAUDE.md and daily-driver.py are the highest-value reads; audit file + memory-management skill are lower but included so Claude doesn't accidentally violate prior decisions.
- **Three phases with explicit gates** match how the repo has historically shipped (see v3.14.x cadence — small gated releases, each with gate-check table).
- **Phase 3 is specified but not enabled** — this lets you see the full design without Claude proposing to re-enable the 6 disabled agents, which is a live landmine.
- **Budget cap delta is required** because v3.12.2 showed what happens when you don't estimate it (the $0.25 cap bit the morning agent).
- **Rejected alternatives + risks sections** force Claude to actually reason, not just write a todo list.
- **Tone rule baked into non-negotiables** — life-systems SOUL is very specific about no scolding. Any plan output that violates the tone would itself be a Phase 1 failure.
