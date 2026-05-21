---
title: Multi-CLI Integration Patterns — Codex + Anti-Gravity + Claude + Local
created: 2026-05-21
status: smoke-tested-awaiting-implementation
companion_artifacts:
  - 2026-05-13-vault-synthesizer-retrofit-tiers.md
  - ../../tools/llm-council/model-selection-2026-05-14.md
related_memories:
  - feedback_synth_verify_filter_to_manifest.md
  - feedback_synth_verify_against_median_not_best.md
  - project_pr52_mbp_stale_checkout.md
---

# Multi-CLI Integration Patterns

> **Future Sean / future Claude reading this:** this doc captures a 2026-05-21 design session for moving Sean's agent fleet beyond Claude-only orchestration. Codex CLI and Anti-Gravity CLI were both smoke-tested live (see §Smoke Test Evidence) and proven to produce thinking-partner output from non-interactive headless mode at $0 incremental cost on existing personal subscriptions. Three integration patterns are described below in ROI order. Pattern 1 is the recommended first ship.

## Why this doc exists

The vault_synthesizer Tier 1.5 retrofit (shipped 2026-05-20) fixed the *shape* of synthesizer output — articles now have 3-sentence definitions, prose evidence quotes, named cross-domain tension+consequence, etc. But on 2026-05-21 Sean named the next-tier gap honestly: **the output is still descriptive, not generative**. The synthesizer can tell you what a concept means, grounded in your own vault. It cannot tell you what you are missing, because every grounding point is internal.

The fix is not a deeper depth gate (the current gate is already strict). The fix is an **external reference frame**: a critic layer that reads each concept and compares against canonical references the synthesizer can't see (literary canon for writing skills, OSS prior art for code skills, industry frameworks for PM skills, etc.).

That layer requires either (a) Claude API + WebFetch/WebSearch (~$30-60/month nightly), or (b) shelling out to a CLI that already has those capabilities on a subscription Sean already pays for. Codex CLI (ChatGPT Plus) and Anti-Gravity CLI (Google personal OAuth + Gemini 3) are exactly that — and were verified working in §Smoke Test Evidence below.

## Inventory — what's installed and tested

### Codex CLI (OpenAI)

| Field | Value |
|---|---|
| Binary | `/opt/homebrew/bin/codex` |
| Version | 0.130.0 |
| Config | `~/.codex/config.toml` |
| Active model | `gpt-5.5` with `model_reasoning_effort = "medium"` |
| Auto-migration noted in config | `gpt-5.3-codex → gpt-5.4` |
| Headless entrypoint | `codex exec [PROMPT]` |
| Auth | Signed-in (`~/.codex/auth.json` present) |
| Output format | stdout raw markdown; stderr = full session log including echo of prompt + response + `tokens used` footer |
| JSON output flag | **None** — stdout is the canonical capture; for tool integration, wrap prompts with output-fencing markers so the parser can extract a known region |
| Trust gate | `--skip-git-repo-check` OR run from a trusted dir (Sean's `/Users/seanwinslow` is trusted via `[projects]` in config.toml) |
| Sandbox modes | `--sandbox read-only` (verified); also `workspace-write`, etc. (see `codex --help`) |
| Plugins enabled | atlassian-rovo, google-calendar, gmail, figma, github, google-drive (all via OpenAI's curated registry) |
| MCP server capability | `codex mcp-server` — Codex can BE an MCP server, callable from Claude Code as a tool |
| Cost on test | $0 (ChatGPT Plus subscription absorbs gpt-5.5 calls; see rate-limit caveats §Gotchas) |

### Anti-Gravity CLI (Google, replaced legacy Gemini CLI)

| Field | Value |
|---|---|
| Binary | `/opt/homebrew/bin/gemini` (same binary name; binary contents replaced May 19, 2026) |
| Version | 0.42.0 |
| Config | `~/.gemini/settings.json` (NOT `~/.antigravity/` or `~/.antigravity-ide/` — those are legacy IDE state) |
| Active model | `auto-gemini-3` (routes to `gemini-3.1-pro-preview` in practice — confirmed in smoke test stats) |
| Headless entrypoint | `gemini -p "PROMPT"` |
| Auth | OAuth personal (`~/.gemini/oauth_creds.json`, refreshed 2026-05-21 morning) |
| Output format | `--output-format {text,json,stream-json}` — `json` returns `{session_id, response, stats}` with full token breakdown including `thoughts` tokens. **Strongly prefer JSON for tool integration.** |
| Trust gate | `--skip-trust` flag OR `GEMINI_CLI_TRUST_WORKSPACE=true` env var OR `~/.gemini/trustedFolders.json` |
| Approval modes | `--approval-mode {default,auto_edit,yolo,plan}` — `plan` is read-only and verified safe; `yolo` is unattended-auto-accept (use only inside `--sandbox`) |
| Agent primitives | `gemini mcp`, `gemini extensions`, `gemini skills`, `gemini hooks`, `gemini gemma` (local Gemma model routing), `gemini --acp` (Agent Communication Protocol) — mirror architecture of Claude Code |
| MCP servers configured | nanobanana, zapier, notebooklm-mcp, mcp-atlassian, chrome-devtools, pencil (see `~/.gemini/settings.json`) |
| Worktree support | `--worktree` flag — spawns into a new git worktree for isolation |
| Cost on test | $0 (Google personal OAuth free tier; see rate-limit caveats §Gotchas) |

## Smoke Test Evidence — 2026-05-21

**Prompt used (saved at `/tmp/critique-prompt.md`):** A targeted critique of `vault/knowledge/concepts/writing-voice-modes.md`, asking each CLI to name **3 specific things Sean is missing** from his 5-voice-mode skill, with named authors, named sentence patterns, and named genre unlocks. The prompt was identical across both CLIs for apples-to-apples comparison.

**Headline:** Both CLIs delivered thinking-partner output. Five total non-overlapping recommendations across the two runs; ONE shared recommendation (Joan Didion / *The White Album*) appeared in both — convergence on that specific mode is itself a signal that Sean genuinely needs it.

### Run 1 — Codex (`codex exec --sandbox read-only --skip-git-repo-check`)

- **Wall-clock:** 21s
- **Tokens used:** 17,182 (per Codex's `tokens used` footer in stderr; Codex doesn't break down input/output separately)
- **Workdir:** `/Users/seanwinslow` (trusted per `~/.codex/config.toml`)
- **Exit code:** 0
- **Output verbatim** (3 recommendations, all named author + work + sentence pattern + genre unlock):

```markdown
1. **Add "Forensic Moral Essayist" Mode**

Anchor it on **Joan Didion, "The White Album"**.

Sentence pattern: **reported fact + withheld judgment + destabilizing qualification
+ moral aftershock**.

What it adds: a mode for **diagnostic essays about institutions, taste, technology
culture, and personal complicity**. The current five modes can observe, intensify,
riff, deadpan, or hybridize, but they do not give Sean a cold instrument for saying:
*this is what happened, this is what everyone pretended it meant, and here is the rot
beneath the explanation*. It would unlock essays where Sean needs authority without
performance.

2. **Add "Architectural Systems Narrator" Mode**

Anchor it on **John McPhee, "The Search for Marvin Gardens"**.

Sentence pattern: **concrete scene + structural analogy + hidden system + return to
the scene with altered meaning**.

What it adds: a mode for **technical strategy essays, company operating memos,
architecture notes, and product retrospectives** where the argument needs to be felt
as a system, not stated as a thesis. Sean's current modes are voice-forward. This
would add **form-forward writing**: pieces whose organization carries the insight.

3. **Add "Intimate Intellectual Pressure" Mode**

Anchor it on **Maggie Nelson, "Bluets"**.

Sentence pattern: **numbered fragment + private confession + citation/idea shard
+ unresolved turn**.

What it adds: a mode for **personal knowledge-vault essays, grief/obsession notes,
creative research logs, and hybrid memoir-thinking pieces**. The current five modes
do not fully support vulnerability without either joking, stylizing, or accelerating
past it.
```

### Run 2 — Anti-Gravity (`GEMINI_CLI_TRUST_WORKSPACE=true gemini -p ... --output-format json --approval-mode plan`)

- **Wall-clock:** 43s
- **Tokens used:** 15,746 (input 13,183 / candidates 645 / thoughts 1,918) — full breakdown in `stats.models["gemini-3.1-pro-preview"]`
- **Workdir:** `/Users/seanwinslow` (trusted via env var)
- **Exit code:** 0
- **Model resolved:** `gemini-3.1-pro-preview` (per JSON stats; `auto-gemini-3` routed there)
- **Output shape:** Clean JSON — `{session_id, response, stats}`. Response field is markdown ready for direct write to file.
- **Output verbatim** (3 recommendations):

```markdown
### 1. Surgical Cultural Synthesis
* **Author/Work:** Joan Didion, *The White Album* (titular essay)
* **Sentence Pattern:** The Anaphoric Flattening. `[Anaphoric list of chaotic or
  highly specific details] + [em-dash or paragraph break] + [flat, monosyllabic
  declarative resolution].`
* **What it unlocks:** Systemic teardowns, tech-industry post-mortems, and cultural
  trend analysis. Your current modes default to irony (Vonnegut), chaos (Thompson),
  or provincial detachment (Sedaris). Didion unlocks the ability to write about
  systemic failure and industry decay with ruthless, chilling authority and
  atmospheric dread, treating a failed startup or a broken paradigm like a crime
  scene.

### 2. Escalating Moral Architecture
* **Author/Work:** James Baldwin, *The Fire Next Time* ("Down at the Cross")
* **Sentence Pattern:** The Periodic Logical Trap. `[Subordinate clause establishing
  historical/contextual premise] + [nested relative clauses stacking the stakes]
  + [comma] + [main subject + declarative verb delivering a devastating,
  inescapable absolute].`
* **What it unlocks:** Manifestos, core-belief essays, and calls-to-action. Your
  current skill lacks a mode for absolute, unironic conviction. When you need to
  persuade an audience of a high-stakes paradigm shift, Beat Flow is too messy and
  Absurdist undermines the stakes.

### 3. Techno-Dialectical Aphorist
* **Author/Work:** Byung-Chul Han, *The Burnout Society*
* **Sentence Pattern:** The Conceptual Inversion. `[Abstract noun phrase] +
  [negation of expected action] + [semicolon] + [paradoxical, aggressive verb].`
* **What it unlocks:** Short-form architecture memos, strategic axioms, and
  high-signal social media threads. Vonnegut's minimalism relies on folksy
  colloquialisms ("So it goes"), which can sound flippant in a technical strategy
  document. Han's mode strips out narrative entirely.
```

### Cross-CLI analysis

| Dimension | Codex | Anti-Gravity |
|---|---|---|
| Convergence | Didion / The White Album | Didion / The White Album |
| Unique adds | McPhee (form-as-argument), Maggie Nelson (fragmentary) | Baldwin (manifesto/conviction), Byung-Chul Han (aphoristic theory) |
| Sentence-pattern specificity | Named patterns in prose form | Named patterns with formal pseudo-grammar — easier to mechanize |
| Citation tightness | Names specific works, summarizes machinery | Names specific works, quotes the actual sentence pattern from Didion verbatim |
| Domain coverage | Diagnostic essays, operating memos, personal vault essays | Tech post-mortems, manifestos, strategy axioms |
| Genre-unlock specificity | "Sean's company operating memos" | "Failed startup or a broken paradigm like a crime scene" |
| Best fit for Sean's job-hunt 2026 work | McPhee mode for operating memos | Han mode for short-form strategy axioms |
| Best fit for Sean's personal writing | Maggie Nelson mode for vault essays | Baldwin mode for high-stakes conviction |

**Verdict:** the two CLIs are genuinely complementary, not redundant. Running both for ~$0 incremental cost gives 5 high-quality adds where one CLI alone gives 3. The vault_critic agent should ship using both.

---

## Pattern 1 — `vault_critic` agent (RECOMMENDED FIRST SHIP)

### Goal

Replace the next-tier complaint ("the synthesizer describes what I have, not what I should add") with a true thinking-partner layer running nightly at $0 marginal cost.

### Architecture

A new SDK agent at `agents-sdk/agents/vault_critic.py` that runs on launchd at **03:30 daily** (after vault-synthesizer 02:30 → deep-researcher 02:45). Schedule sequence:

```
02:00  vault-indexer       (Mac Mini, Ollama nomic-embed)
02:30  vault-synthesizer   (Mac Mini, Qwen3-14B on MBP — DESCRIPTIVE layer)
02:45  deep-researcher     (Mac Mini, LDR + SearXNG + Qwen3-14B — single-target research)
03:30  vault-critic   NEW  (Mac Mini, shells to Codex + Anti-Gravity — GENERATIVE layer)
08:30  daily-driver morning
08:45  meta-agent
```

### Inputs

1. **Today's Mac Mini synth-manifest** (`vault/health/synth-manifest-{today}.json`) — filter against PR contamination per `feedback_synth_verify_filter_to_manifest.md`. Only critique articles Mac Mini wrote, not files merged in from stale-checkout machines.
2. **Newly-written concept articles** from the night, capped at 3 per run to stay under rate limits.
3. **Critique prompt template** (next section).

### Critique prompt template

The smoke-tested prompt at `/tmp/critique-prompt.md` is the prototype. Generalize to:

```
You are reviewing a concept article from Sean Winslow's personal knowledge vault.
Sean's complaint about his agent fleet is that it produces descriptive summaries of
what he already has, not generative critique of what he should add.

ARTICLE UNDER REVIEW: `{slug}`

{Full article body}

CONTEXT (from `vault/knowledge/index.md`):
- This concept currently cross-references: {list of [[wikilinks]] in body}
- It originates from source file: {source path from frontmatter}
- Sean's broader vault includes (truncated to top 30 by recency):
  {recent concepts/connections list}

TASK: Give Sean 3 specific things he is MISSING from this concept — adjacent
techniques, canonical references, missing facets, contradicting frameworks. For each:
- (1) WHAT to add (named technique, idea, framework, voice, pattern, etc.),
- (2) WHO/WHAT exemplifies it — a specific author, book, paper, project, repo, talk,
       essay; cite the specific work, not the field,
- (3) WHAT this would unlock for Sean — name the genre of work, the kind of decision,
       the kind of artifact this would let him produce that the current concept
       cannot reach.

Be specific. No generic advice. If you cite an author, cite a specific work.
No "consider exploring X" — instead, name what to add and why.

Respond in plain markdown, under 600 words. Lead with the 3 recommendations.
```

### Output shape

For each critiqued article, write a sibling file at `vault/knowledge/expansions/{slug}.md`:

```markdown
---
title: "How to make `{Original Concept Title}` better"
type: expansion
parent: "[[{original-slug}]]"
sources:
  - codex (gpt-5.5)
  - anti-gravity (gemini-3.1-pro-preview)
created: 2026-MM-DD
updated: 2026-MM-DD
---

## What this is

Critiques from two external reasoners (gpt-5.5 via Codex CLI, Gemini 3 via
Anti-Gravity CLI) of [[{original-slug}]]. The synthesizer describes what the
concept is; this expansion proposes what's missing.

## From Codex (gpt-5.5)

{codex stdout, verbatim}

## From Anti-Gravity (Gemini 3)

{response field from gemini JSON, verbatim}

## Convergence

{Optional: a 3rd pass where the agent identifies shared recommendations between
the two — likely a second LLM pass at marginal cost. Skip on first iteration.}
```

### Implementation outline

```python
# agents-sdk/agents/vault_critic.py
"""
Nightly generative critique of newly-written concept articles.
Runs after vault_synthesizer (02:30) and deep_researcher (02:45) at 03:30.
Shells out to Codex CLI (gpt-5.5) and Anti-Gravity CLI (Gemini 3) in parallel.
Cost: $0 incremental on existing personal subscriptions.
"""

import asyncio
import json
import subprocess
from pathlib import Path
from datetime import date

# Path constants — anchored to repo root via lib.paths.repo_root()
VAULT = Path("vault")
KNOWLEDGE = VAULT / "knowledge"
HEALTH = VAULT / "health"
EXPANSIONS = KNOWLEDGE / "expansions"
LOGS = VAULT / "90_system" / "agent-logs"

MAX_CRITIQUES_PER_RUN = 3   # rate-limit guard
CODEX_TIMEOUT_S = 120
GEMINI_TIMEOUT_S = 120


async def run_codex(prompt: str) -> tuple[str, dict]:
    """Returns (markdown_response, meta). meta has duration_s, tokens, exit_code."""
    # codex exec runs from a trusted dir (HOME) with read-only sandbox.
    # --skip-git-repo-check bypasses the workspace-trust check.
    cmd = ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check", prompt]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=Path.home(),
    )
    stdout, stderr = await asyncio.wait_for(
        proc.communicate(), timeout=CODEX_TIMEOUT_S
    )
    # Codex stderr has the "tokens used: N" footer — parse it for meta.
    tokens = _parse_codex_tokens(stderr.decode())
    return stdout.decode(), {"tokens": tokens, "exit_code": proc.returncode}


async def run_antigravity(prompt: str) -> tuple[str, dict]:
    """Returns (markdown_response, meta)."""
    cmd = [
        "gemini", "-p", prompt,
        "--output-format", "json",
        "--approval-mode", "plan",     # read-only mode, verified safe
    ]
    env = {"GEMINI_CLI_TRUST_WORKSPACE": "true", **os.environ}
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=Path.home(),
        env=env,
    )
    stdout, stderr = await asyncio.wait_for(
        proc.communicate(), timeout=GEMINI_TIMEOUT_S
    )
    payload = json.loads(stdout)
    return payload["response"], {
        "tokens": payload["stats"]["models"]["gemini-3.1-pro-preview"]["tokens"],
        "exit_code": proc.returncode,
        "session_id": payload["session_id"],
    }


async def critique_one(article_path: Path) -> Path:
    """Fan out one article to both CLIs in parallel, write expansion file."""
    prompt = _build_critique_prompt(article_path)
    codex_task = run_codex(prompt)
    gemini_task = run_antigravity(prompt)
    (codex_resp, codex_meta), (gem_resp, gem_meta) = await asyncio.gather(
        codex_task, gemini_task, return_exceptions=False,
    )
    expansion_path = EXPANSIONS / article_path.name
    expansion_path.write_text(_format_expansion(article_path, codex_resp, gem_resp))
    return expansion_path


def select_targets(manifest: dict) -> list[Path]:
    """Pick up to MAX_CRITIQUES_PER_RUN concept articles from today's manifest.
    Filter against PR contamination per feedback_synth_verify_filter_to_manifest.md."""
    # Read the auto-commit that wrote the manifest, get its file list,
    # intersect with vault/knowledge/concepts/.
    ...


async def main():
    today_manifest = HEALTH / f"synth-manifest-{date.today()}.json"
    if not today_manifest.exists():
        # No synth ran or synth wasn't completed — exit quietly.
        return
    manifest = json.loads(today_manifest.read_text())
    targets = select_targets(manifest)
    expansions = await asyncio.gather(*(critique_one(t) for t in targets))
    _write_critic_manifest(expansions, manifest)


if __name__ == "__main__":
    asyncio.run(main())
```

### Manifest fields

`vault/health/critic-manifest-{date}.json`:

```json
{
  "run_id": "2026-MM-DDTHH:MM:SS",
  "duration_seconds": 87.3,
  "articles_critiqued": 3,
  "codex_calls": 3,
  "codex_failures": 0,
  "codex_tokens_total": 51234,
  "antigravity_calls": 3,
  "antigravity_failures": 0,
  "antigravity_tokens_total": 47891,
  "expansions_written": [
    "vault/knowledge/expansions/writing-voice-modes.md",
    "..."
  ]
}
```

`daily_driver` morning brief should surface this under Vault Health: "Critic ran on N articles last night → vault/knowledge/expansions/".

### Tests to add

- `test_vault_critic.py::test_select_targets_filters_pr_contamination` — mock a manifest with `concepts_written=1` but vault/knowledge/concepts/ has 30 fresh files; assert only 1 is selected.
- `test_vault_critic.py::test_codex_response_parsing` — mock subprocess output matching the Codex stderr/stdout shape; assert markdown extracted and token count parsed.
- `test_vault_critic.py::test_antigravity_json_parsing` — mock JSON shape from smoke test; assert `response` extracted.
- `test_vault_critic.py::test_concurrent_failure_isolation` — when one CLI fails, the other's output is still written and the failure is logged in the manifest.

### Effort estimate

~3 hours: subprocess wrappers + prompt builder + manifest schema + 4 tests + plist installer. Smoke-test data above can be replayed as test fixtures, avoiding live CLI calls in CI.

### Rollback

Disable the launchd plist via `agents-sdk/schedules/install_schedules.sh --remove vault_critic`. The expansion files at `vault/knowledge/expansions/` remain useful even if the agent is paused.

---

## Pattern 2 — Multi-vendor LLM Council via direct CLI shell-out

### Goal

Bring `tools/llm-council/` from OpenRouter-mediated calls to direct CLI shell-outs. Removes vendor-tuning loss (OpenRouter strips some provider behaviors), gives access to vendor-tuned reasoning effort settings, and drops marginal cost to ~$0 on the subscriptions Sean already pays for.

### Today's council (per CLAUDE.md v3.37.1)

| Profile | Models | Chairman | Typical cost | Mediation |
|---|---|---|---|---|
| premium | Claude Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20 | Opus 4.7 | ~$0.29 | OpenRouter |
| variance | Claude Sonnet + GPT-5.4-mini + DeepSeek v4-pro + Mistral medium-3-5 | Sonnet | ~$0.14 | OpenRouter |

### Proposed addition

Add CLI-backed adapters as alternate council members:

| Adapter | Backing | Cost on test | Tradeoff |
|---|---|---|---|
| `codex-cli` | `codex exec` → gpt-5.5 medium reasoning | $0 (ChatGPT Plus rate-cap) | Subject to ChatGPT Plus rate caps; no fine-grained reasoning_effort flag exposed to CLI |
| `antigravity-cli` | `gemini -p --output-format json` → Gemini 3.1 Pro | $0 (Google personal OAuth rate-cap) | Subject to Google personal-OAuth rate caps |

### Use cases that benefit

- **Voice-mode calibration** — exactly the smoke test we just ran. Convergence detection between two vendors signals strong "you need this" recommendations.
- **Pre-mortem decisions** — different RLHF biases produce useful spread on "what could go wrong".
- **PRD stress-test** — Codex (code-aware) catches API-design defects; Gemini (search-grounded) catches market/competitor blind spots; Claude catches scope-creep.
- **Cover-letter critique** — Codex is blunt about substance; Gemini is sensitive to tone; combine for balanced feedback.

### Implementation outline

```python
# tools/llm-council/council/adapters/codex_cli.py
class CodexCLIAdapter(CouncilMember):
    name = "codex-cli"
    backing_model = "gpt-5.5"

    async def respond(self, prompt: str) -> CouncilResponse:
        out, meta = await run_codex(prompt)  # same wrapper as vault_critic
        return CouncilResponse(text=out, tokens=meta["tokens"], cost_usd=0.0)
```

```python
# tools/llm-council/council/adapters/antigravity_cli.py
class AntigravityCLIAdapter(CouncilMember):
    name = "antigravity-cli"
    backing_model = "gemini-3.1-pro-preview"

    async def respond(self, prompt: str) -> CouncilResponse:
        text, meta = await run_antigravity(prompt)
        return CouncilResponse(text=text, tokens=meta["tokens"], cost_usd=0.0)
```

Reuse the wrappers built for Pattern 1 by hoisting them into `agents-sdk/lib/cli_runners.py` and importing from both `vault_critic.py` and the council adapter modules.

### New profile

Add a third profile alongside premium and variance:

```toml
# tools/llm-council/council/profiles/zero-cost.toml
[profile]
name = "zero-cost"
description = "Codex (gpt-5.5) + Anti-Gravity (Gemini 3 Pro) + local Qwen3-14B. $0 marginal cost on personal subscriptions."

[[members]]
adapter = "codex-cli"

[[members]]
adapter = "antigravity-cli"

[[members]]
adapter = "ollama-qwen3"   # already exists for local runs

[chairman]
adapter = "codex-cli"      # cheapest synthesizer; could also be antigravity-cli
```

### Effort estimate

~2 hours: two adapter classes (most code reusable from Pattern 1's CLI wrappers) + one profile TOML + one test pinning the adapter return shape.

---

## Pattern 3 — Job-routing in HybridRouter

### Goal

Long-term architecture: route each task type to the best backend. Today HybridRouter picks between Qwen3-14B local and Sonnet 4.6 fallback. Extend it so each task class has a primary + fallback chain across all four available backends (Claude API, Codex, Anti-Gravity, local Qwen).

### Proposed routing table

| Task class | Primary | Fallback 1 | Fallback 2 | Rationale |
|---|---|---|---|---|
| `vault_synthesis` | Qwen3-14B local | (none) | (none) | Bulk descriptive synthesis at $0; current behavior. |
| `vault_critique` (NEW) | Codex + Anti-Gravity (parallel) | Sonnet 4.6 | (none) | Two-vendor coverage at $0; Sonnet only if both CLIs rate-cap. |
| `code_review` (NEW) | Codex (gpt-5.5 is code-tuned) | Sonnet 4.6 | Qwen3-14B | Codex is the strongest code reasoner; Sonnet has the deepest context. |
| `web_grounded_research` | Anti-Gravity (native Google Search) | Gemini DR API | Local LDR | Anti-Gravity is free for simple grounded research; Gemini DR for compound; LDR for offline. |
| `daily_driver_morning` | Sonnet 4.6 | Codex | (none) | Current cost is acceptable; Codex as a fallback if Anthropic rate-caps or pricing shifts. |
| `inbox_triage` | gemma4:e4b local | Anti-Gravity | (none) | Local is fastest for routing; Anti-Gravity only for ambiguous items. |
| `meta_agent` | gemma4:e4b local | (none) | (none) | Current behavior; no need to escalate. |

### Implementation outline

Extend `agents-sdk/lib/hybrid_router.py` with new task classes and an explicit allowlist of CLI backends. The CLI runners from Pattern 1 already provide the shell-out primitives.

Add a new method `HybridRouter.route_to_cli(task_class: str, prompt: str) -> CLIResponse` that picks from the routing table, retries on rate-cap detection (e.g., 429-shaped stderr from Codex, specific text in Anti-Gravity stderr), and surfaces telemetry to the daily_driver morning brief.

### Effort estimate

~6-8 hours: routing table TOML config, retry/fallback logic, rate-cap detection heuristics per CLI, telemetry plumbing, 6-8 tests.

### When to ship

After Pattern 1 has run for ≥1 week and Pattern 2 has been used for ≥2 council sessions. Only ship Pattern 3 if there's evidence that the existing single-backend agents would benefit from routing — premature otherwise.

---

## Cross-cutting concerns

### Trust flags (mandatory for all three patterns)

| CLI | What to set | Where |
|---|---|---|
| Codex | `--skip-git-repo-check` flag OR run with `cwd=Path.home()` OR add the repo to `~/.codex/config.toml` `[projects]` with `trust_level = "trusted"` | Per-invocation flag preferred; explicit and reviewable |
| Anti-Gravity | `GEMINI_CLI_TRUST_WORKSPACE=true` env var OR `--skip-trust` flag OR add to `~/.gemini/trustedFolders.json` | Env var preferred; explicit and reviewable |

The trust gates are good safety properties — they prevent stray agent invocations in untrusted contexts. The wrappers should set them deliberately, not silently.

### Sandbox modes (mandatory for all three patterns)

| CLI | Read-only critique mode | Auto-edit mode (NOT for nightly) |
|---|---|---|
| Codex | `--sandbox read-only` (verified in smoke test) | `--sandbox workspace-write` |
| Anti-Gravity | `--approval-mode plan` (verified in smoke test) | `--approval-mode auto_edit` |

Nightly agents must use the read-only modes. Auto-edit is only appropriate for interactive sessions where Sean is at the keyboard.

### Output parsing

| CLI | Recommended parser |
|---|---|
| Codex | Capture stdout as-is. stderr has session metadata + token footer; parse `tokens used\n(\d+)` for meta. Wrap critique prompts with explicit start/end markers (e.g., "Respond in plain markdown, between `<critique>` and `</critique>` markers") if you need a guaranteed boundary. |
| Anti-Gravity | `json.loads(stdout)`, extract `payload["response"]`. Token breakdown lives at `payload["stats"]["models"][<model_name>]["tokens"]`. Model name is whichever auto-router resolved to — don't hardcode. |

### Rate limits (unverified — must test in production)

- **ChatGPT Plus / Pro** does not publish a daily quota for `codex exec`. Anecdotal reports suggest ~150 messages per 5 hours on Plus. For 3 critiques/night that's 6 messages (3 prompts × 1 response), which is ~4% of the conservative cap. Safe in expectation but worth confirming after 3 nights of live use.
- **Google personal-OAuth** rate limits for Anti-Gravity are not publicly documented. The smoke test used 15,746 tokens in one call. If the quota is daily-token-based (likely), 3 critiques/night ≈ 50K tokens/day, well under any plausible cap. Monitor `gemini-out.json` `stats` for any error-shape stderr.

If either CLI starts rate-capping mid-run, the vault_critic agent should:
1. Log the rate-cap event to `vault/90_system/agent-logs/vault-critic-stderr.log`
2. Continue with the working CLI if the other is capped
3. Mark the run `status: partial` in the manifest
4. NOT retry the same CLI within the same run (would just compound the cap)

### Secrets hygiene

`~/.gemini/settings.json` contains **live API keys** for Gemini (Nano-Banana MCP), Zapier (token in `mcpServers.zapier.args` URL), and Atlassian (JIRA + Confluence API tokens in the `mcp-atlassian` env). Any tooling that reads this file for config (including future vault_critic auth introspection) MUST NOT log the full file contents — log only the keys actually consumed. Auth state for the gemini CLI itself lives in the separate `~/.gemini/oauth_creds.json` (gitignored by Anti-Gravity's installer); read from there for auth status checks, not from `settings.json`.

### Codex's auto-migration behavior

`~/.codex/config.toml` has a `[notice.model_migrations]` block: `"gpt-5.3-codex" = "gpt-5.4"`. OpenAI auto-migrates between model versions. Don't hardcode `gpt-5.5` as the expected model in tests — parse what comes back via stderr session metadata.

### Anti-Gravity's `auto-gemini-3` routing

The settings file specifies `"model": {"name": "auto-gemini-3"}`. In the smoke test this resolved to `gemini-3.1-pro-preview`. Both the routed model and the preview status may change. Don't hardcode in tests; read from the JSON stats.

---

## Sequencing recommendation

1. **Week of 2026-05-21:** Ship Pattern 1 (vault_critic) per the implementation outline. Run for ≥3 nights to validate output shape, rate-cap tolerance, and manifest health. Read 2 expansion files per night — sample the median, not the best, per `feedback_synth_verify_against_median_not_best.md`.
2. **Week of 2026-05-28:** If Pattern 1 is healthy, ship Pattern 2 adapters (zero-cost council profile). Use it on 2-3 real decisions — calibrate vs the existing premium and variance profiles.
3. **Week of 2026-06-04+:** Decide on Pattern 3 based on usage signal from Patterns 1+2. If the single-backend agents are still routing well, defer. If you start running into rate caps or quality gaps, ship the routing layer.

## Open questions

1. **Codex output fencing:** Should the critique prompt require the model to wrap its response in `<critique>...</critique>` markers? This would harden parsing against any rogue Codex preamble/postamble. Negligible token cost; recommended.
2. **Convergence detection:** When Codex and Anti-Gravity independently suggest the same author (Didion in the smoke test), is that worth surfacing in the expansion file as a "🔁 Both reasoners agreed on" callout? Cheap to detect (string-match author names across responses) and valuable to Sean. Recommended for v1.
3. **Articles per night cap:** Set at 3 in the outline. Synthesizer wrote 1 article on 2026-05-21 → 1 critique. On busy nights (5/19 wrote 35) → 3 critiques + 32 untouched. Should the cap scale (e.g., top 3 by "newness × cross-cluster-distance"), or stay fixed? Fixed at 3 is the v1 default; revisit after 1 week.
4. **Expansion file lifecycle:** Should expansion files be regenerated when the underlying concept is rewritten by the synthesizer? Or stay frozen as snapshots in time? Snapshot is simpler; recommended for v1.
5. **Skill_optimizer relationship:** `vault_critic` is the cheap nightly tier. `skill_optimizer` (manual, $20-145/run, autoresearch convergence loop) is the deep tier. Should the vault_critic expansion file include a footer like "Run `skill_optimizer` for deep convergence on this critique" with the exact command? Cheap to add; recommended.

## Companion artifacts

- Smoke-test prompt: `/tmp/critique-prompt.md` (move to `agents-sdk/prompts/vault-critic-prompt-template.md` when Pattern 1 ships)
- Smoke-test outputs: `/tmp/codex-out.txt`, `/tmp/gemini-out.json` (move to `agents-sdk/docs/multi-cli-smoke-2026-05-21/` if useful for tests)
- Codex config: `~/.codex/config.toml`
- Anti-Gravity config: `~/.gemini/settings.json`
- Vault synthesizer retrofit plan (Pattern 1 sequel): [`2026-05-13-vault-synthesizer-retrofit-tiers.md`](../../vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/job-hunt-2026-roadmap/2026-05-13-vault-synthesizer-retrofit-tiers.md)
- LLM Council base (Pattern 2 target): [`tools/llm-council/`](../../tools/llm-council/)
- HybridRouter (Pattern 3 target): [`agents-sdk/lib/hybrid_router.py`](../lib/hybrid_router.py)
- Memory: random-sample contamination filter — [`feedback_synth_verify_filter_to_manifest.md`](../../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_filter_to_manifest.md)
- Memory: median-not-best verification rule — [`feedback_synth_verify_against_median_not_best.md`](../../../../.claude/projects/-Users-seanwinslow-Code-Brain-code-brain/memory/feedback_synth_verify_against_median_not_best.md)
