# Hermes Agent Investigation — Claude Code Prompt

> **How to use:** Open Claude Code in the `claude-code-superuser-pack/` repo root.
> Enable Plan Mode (`Shift+Tab` twice) and Extended Thinking (single `Tab`).
> Paste everything inside the fenced block below as a single message.
> Do not pre-attach files — the prompt instructs Claude Code to read what it needs.

---

```xml
<role>
You are a senior AI infrastructure architect with deep expertise in agentic systems, the Claude Agent SDK, local-first AI tooling (Ollama, MLX, LM Studio), MCP servers, and macOS launchd-scheduled autonomous workers. You read open-source codebases the way a security researcher reads them: cite file paths and line numbers, name concrete classes/functions, and never paraphrase architecture you have not actually seen. You are constitutionally allergic to hype — when something looks impressive on a README but thin in source, you say so.
</role>

<mission>
Investigate the Hermes Agent project at https://github.com/NousResearch/hermes-agent.git and decide — with evidence — which (if any) of its design patterns, components, or techniques are worth porting into Sean's existing `agents-sdk/` implementation in this repo (`/Users/seanwinslow/Code-Brain/claude-code-superuser-pack/`). Output an actionable integration plan, NOT a generic comparison essay.
</mission>

<existing_system_context>
Before investigating Hermes, ground yourself in what already exists. Read these files in this order:

1. `CLAUDE.md` — root router and non-negotiables
2. `CHANGELOG.md` — versions 3.12.0 through 3.17.0 (the agents-sdk evolution)
3. `agents-sdk/config.toml` — agent fleet, routing, budgets, artifacts wiring
4. `agents-sdk/agents/daily_driver.py` — the most-developed agent
5. `agents-sdk/agents/deep_researcher.py` — the newest agent (v3.17.0, pure-Python, no SDK in the loop)
6. `agents-sdk/lib/skill_loader.py` — how skills become system prompts
7. `agents-sdk/lib/artifact_loader.py` — operating-model artifact wiring (v3.16.0)
8. `agents-sdk/lib/vault_io.py` and `agents-sdk/lib/logging_setup.py`
9. `agents-sdk/schedules/install_schedules.sh` and one `.plist` to understand launchd shape
10. `docs/agents-sdk.md` if it exists

Then summarize, in a `<current_state>` block, the agents-sdk's:
- Architecture pattern (SDK-loop agents vs pure-Python REST agents like deep_researcher)
- Skill-as-system-prompt loading mechanism
- Routing model (`[routing.task_map]`, local vs cloud, Mac Mini vs MBP vs Anthropic API)
- Safety rails (max_turns, per-run USD caps, `--dry-run`, kill switches)
- Knowledge compounding loop (SessionEnd flush → vault-synthesizer → knowledge-lint, v3.14.3)
- Operating-model artifact injection (v3.16.0 Phase 1, daily-driver only, Phases 2-3 deferred)
- The 6 disabled agents (per `agents-sdk/AUDIT-2026-04-09-agent-downsizing.md`) — what tripped them
- Phase 6 LDR/SearXNG deep-research stack (v3.17.0) — local-only, $0/run

Do not skip this step. The integration plan is worthless if it duplicates something already shipped.
</existing_system_context>

<investigation_tasks>
Execute these as discrete passes. Use WebFetch for the GitHub repo and any docs/blog posts the README links to. If WebFetch is blocked for a domain, say so and fall back to whatever is reachable — do NOT fabricate.

<task index="1" name="identify_and_orient">
- Confirm the canonical repo URL (the user wrote `NousResearch/hermes-agent.git`; verify the org and repo name are correct — Nous Research has multiple projects, do not confuse with `Hermes` model series, `Hermes Function Calling`, or `Forge`).
- Capture: latest commit SHA + date, primary language(s), license, star/fork count, top-level folder layout, declared dependencies (`pyproject.toml` / `package.json` / `Cargo.toml` — whichever applies).
- Read the README and any `ARCHITECTURE.md` / `docs/` / blog posts. Quote 1–3 sentences that capture the project's actual thesis.
- Classify what Hermes IS: framework? runtime? model wrapper? orchestrator? agent harness? CLI? all of the above? Be precise.
</task>

<task index="2" name="map_the_internals">
For each of the following dimensions, cite specific files/functions and quote ≤5-line code excerpts where they meaningfully prove the point:

- **Agent loop / control flow** — how does Hermes decide what to do next? ReAct? Plan-and-execute? Custom? Where is the loop implemented?
- **Tool interface** — how are tools registered, called, validated? Does it use MCP? OpenAI function-calling JSON? a bespoke schema?
- **Model abstraction** — how does it talk to LLMs? Vendor-locked to a Hermes/Nous model? OpenAI-compatible? Local-friendly (Ollama, vLLM, MLX)?
- **Memory / state** — short-term scratchpad, long-term store, vector DB, none?
- **Scheduling / autonomy** — does it have a built-in scheduler, daemon mode, headless runner?
- **Safety / guardrails** — token budgets, turn caps, sandboxing, allowlists?
- **Observability** — logs, traces, run history, replay?
- **Skills / prompts / personas** — does it ship a skill or persona system? How does it differ from Claude's skills?
- **Multi-agent coordination** — does it support sub-agents / agent fleets / orchestration patterns?
- **Constitution / values / refusals** — any built-in alignment scaffolding worth comparing to Anthropic's?

For each dimension, end with a one-line verdict: `NOVEL`, `CONVERGENT_WITH_OURS`, `INFERIOR_TO_OURS`, or `NOT_PRESENT`.
</task>

<task index="3" name="diff_against_our_stack">
Build a side-by-side table:

| Dimension | Hermes approach | agents-sdk approach | Gap / Overlap |

Be specific in cells — file paths on both sides, not adjectives. If a cell would read "they have it, we don't" or vice versa, say what porting would actually require (lines of code, new dependencies, compatibility hazards).
</task>

<task index="4" name="port_candidates">
From the diff, propose AT MOST 5 concrete port candidates. For each, fill out the schema below. Be ruthless: if nothing meets the bar, return fewer than 5 (or zero) and say why. Do NOT pad.

<candidate_template>
- **Name:** <short_handle>
- **What it is:** 2 sentences max
- **Source (Hermes):** file path(s) + commit SHA
- **Target (ours):** which agent / lib file / config block it would land in
- **Estimated effort:** XS (< 1hr) / S (half day) / M (1-2 days) / L (week+)
- **Net new dependencies:** list, with PyPI/NPM names
- **Compatibility hazards:** Python 3.13, claude-agent-sdk==0.1.63, macOS launchd, the 100%-local invariant for the autonomous fleet, the no-cloud-egress rule for life-systems data
- **Why it's worth it:** quantified expected gain (cost/run, latency, reliability, capability) — no vague "better DX"
- **Why it might NOT be worth it:** strongest counter-argument
- **Validation experiment:** the smallest test (≤2 hours of work) that would prove or disprove the hypothesis before a full port
- **Verdict:** SHIP / SPIKE / WATCH / SKIP
</candidate_template>
</task>

<task index="5" name="anti_patterns">
List any patterns in Hermes that we should NOT adopt, with reasons. Examples to look for: heavy framework lock-in, model-specific assumptions, non-local dependencies, license incompatibilities, security smells (eval, shell-out without allowlists), abandonware signals (stale commits, open critical issues).
</task>

<task index="6" name="strategic_take">
In ≤200 words, answer Sean's actual question: "Should I integrate aspects of Hermes Agent into my agents-sdk?" Your answer must include:
- A one-sentence verdict (YES, YES-with-conditions, NO, NOT-YET)
- The single highest-leverage thing to port, OR the single best reason to walk away
- What this implies for the agents-sdk roadmap over the next 1-2 versions (3.18 / 3.19)
</task>
</investigation_tasks>

<reasoning_instructions>
Think step-by-step at every stage. Do NOT skip task 1 (existing system grounding) — duplicating shipped work is the biggest failure mode here. Quote source before drawing conclusions; if you cannot quote, mark the claim as "speculative" and lower confidence accordingly. When you encounter conflicting signals (README claim vs actual code), trust the code.

If WebFetch for the Hermes repo or its docs returns 403/404/blocked, say exactly which URL failed, suggest two alternative ways Sean could fetch it (gh CLI, git clone), and continue with whatever you CAN reach. Do not invent file contents.

Stay calibrated. Honest "I could not access X" beats fabricated detail. This output is going into a Plan Mode review where Sean will critique it before any code lands.
</reasoning_instructions>

<output_format>
Produce a single markdown document with these sections in this exact order:

1. `# Hermes Agent — Integration Investigation`
2. `## TL;DR` (≤5 bullets, the strategic take front-loaded)
3. `## Current agents-sdk State (verified)` — the `<current_state>` summary
4. `## Hermes Agent Identification` — task 1 output
5. `## Internals Map` — task 2 output, dimension by dimension
6. `## Side-by-Side Diff` — task 3 table
7. `## Port Candidates` — task 4, structured per the template, ranked by SHIP > SPIKE > WATCH > SKIP
8. `## Anti-patterns to Avoid` — task 5
9. `## Strategic Take` — task 6, ≤200 words
10. `## Open Questions for Sean` — anything that genuinely requires his input before a decision
11. `## Sources` — every URL fetched, every local file read, with line ranges

No filler, no executive-summary throat-clearing beyond the TL;DR, no apologies. If a section would be empty, write `(none)` rather than padding.
</output_format>

<validation>
Before finalizing the answer, run this checklist on yourself:

1. Did I read at least 8 of the 10 grounding files in `<existing_system_context>`?
2. Did I cite specific Hermes file paths + a commit SHA, or did I describe a README in vague terms?
3. Is every port candidate accompanied by a ≤2-hour validation experiment?
4. Did I distinguish between "Hermes has X" vs "Hermes claims X"?
5. Are my verdicts (NOVEL / SHIP / etc.) defensible from the evidence I cited, or are they vibes?
6. Have I respected the 100%-local invariant of the autonomous fleet (any cloud-API port candidate must explicitly justify breaking it)?
7. Have I respected the no-cloud-egress rule for life-systems personal data?
8. Is my Strategic Take actually decisive, or am I hedging?

Revise any section that fails a check. Then output the final document.
</validation>

<begin>
Start now. Begin by reading the grounding files. Use Plan Mode to lay out your investigation steps, then execute.
</begin>
```

---

## Why this prompt is shaped the way it is

A few of the prompt-engineering choices, briefly, since you mentioned wanting to learn the *why*:

- **Role first, mission second.** The `<role>` block primes Claude's tone (skeptical, code-grounded, citation-heavy) before it sees the task. Without that, you tend to get hype-mirroring summaries of any GitHub repo you point it at.
- **Forced grounding pass before investigation.** The `<existing_system_context>` block exists because the #1 failure mode here is recommending you "add" something you already shipped (e.g., skill-as-system-prompt, local-only routing, deep research). Reading your CHANGELOG/config first is non-negotiable.
- **Decomposed tasks with index numbers.** Six discrete passes (`identify → map → diff → candidates → anti-patterns → strategic take`) instead of one giant ask. This is "chain complex prompts" applied inside a single message — each task validates the previous.
- **Strict candidate template + hard ceiling of 5.** This is the negative constraint that forces ruthlessness. Without "AT MOST 5" + the "be ruthless, do NOT pad" instruction, you get a list of 12 mediocre candidates instead of 2 good ones.
- **Verdict tags (`NOVEL/CONVERGENT_WITH_OURS/INFERIOR/NOT_PRESENT`, then `SHIP/SPIKE/WATCH/SKIP`).** Forcing a categorical label per dimension keeps the analysis decision-shaped instead of essay-shaped.
- **Validation block at the end.** Self-check against 8 specific failure modes — including "did I respect the 100%-local invariant" and "am I hedging" — before final output.
- **XML tags throughout.** Claude is trained on XML-structured prompts; tags like `<role>`, `<mission>`, `<task index="1">` are more reliable separators than markdown headers when the prompt gets long.
- **Explicit fallback for blocked WebFetch.** Saves you a wasted run if the GitHub URL bounces — the prompt tells Claude what to do instead of giving up.

[View the prompt file](computer:///Users/seanwinslow/Code-Brain/claude-code-superuser-pack/vault/00_inbox/hermes-agent-investigation-prompt.md)

One thing worth flagging: the URL you gave (`NousResearch/hermes-agent.git`) — I haven't verified the repo exists at that exact path. Nous Research has several agent-related projects (the Hermes model series, Hermes Function Calling, Forge), and the prompt explicitly tells Claude Code to confirm the canonical URL in task 1 rather than assume.