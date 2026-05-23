---
name: llm-council
description: Convene a multi-vendor LLM council (4 models cross-ranking + chairman synthesis) for high-variance, high-stakes critique tasks via OpenRouter. Use when Sean says "convene council", "council critique", "variance check", "premium council", "four-model review", "calibrate voice modes", "stress-test this spec", "council pre-mortem", or surfaces a question where (a) different RLHF biases would produce useful spread, OR (b) different frontier-model blind spots would catch what one model misses. Two profiles available — premium (4 frontier models, ~$0.30–1/query, for stakes/synthesis) and variance (4 mixed-lineage models, ~$0.10–0.40/query, for stylistic/divergence questions). Skip for coding tasks (use Claude Code directly), for research with citations (use gemini-deep-research), for anything skill-optimizer already handles, or for daily ops where single-model Claude is fine. Inspired by Andrej Karpathy's llm-council.
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# LLM Council

Multi-vendor LLM critique via OpenRouter, invocable from inside Claude Code sessions. Inspired by [Andrej Karpathy's llm-council](https://github.com/karpathy/llm-council).

See [`decision-table.md`](decision-table.md) for the full routing reference.

---

## 0. Path resolution (read first)

This skill is also symlinked from `~/.claude/skills/llm-council/` so it's invocable from any Claude Code session on Sean's machine. The backing CLI, profiles, budget guardrails, and spend tracking are canonical here in code-brain — don't duplicate them.

| Resource | Canonical absolute path |
|---|---|
| CLI working dir | `/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council` |
| Spend tracking | `/Users/seanwinslow/Code-Brain/code-brain/vault/health/council-spend-{YYYY-MM-DD}.json` |
| Session JSON archive | `/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council/data/sessions/<session-id>.json` |
| writing-voice-modes spec | `.claude/skills/writing-voice-modes/SKILL.md` in the **current** repo (most repos carry a local copy) — fall back to `/Users/seanwinslow/Code-Brain/code-brain/.claude/skills/writing-voice-modes/SKILL.md` if not present locally. |

**Output routing rule:** Always pass `--output` explicitly as an absolute path. The transcript should land next to the artifact being critiqued — in whatever repo the session is running from — not in code-brain's vault by default. Examples:
- Portfolio writing surfaces → `/Users/seanwinslow/Code-Brain/sw-ai-pm-portfolio/docs/critiques/<surface>-council-<YYYY-MM-DD>.md`
- Job-hunt artifacts → `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/...`

`mkdir -p` the parent directory first.

---

## 1. When to convene a council

| Question shape | Profile | Why |
|---|---|---|
| Voice spec calibration ("how differently do models read this?") | **variance** | Divergence = signal |
| Cover letter / role-fit memo critique | **premium** | Different vendors, different tone biases |
| Decision pre-mortem ("strongest objection?") | **premium** | Each model has different blind spots |
| PRD / tech-spec stress test | **premium** | Multi-vendor catches holes single-vendor misses |
| Prompt clarity test ("is my SKILL.md unambiguous?") | **variance** | Spread reveals ambiguous instructions |

**Skip council when:**
- Writing or refactoring code (single-model Claude is faster)
- Researching the landscape for X (use `gemini-deep-research`)
- Anything `skill_optimizer` already does (it's structurally a council)
- Daily ops (overkill)

---

## 2. Workflow templates

### 2.1 Voice-mode calibration (variance profile)

Use when Sean wants to check whether the `writing-voice-modes` SKILL.md spec is unambiguous enough that four different frontier models would read it the same way.

**Steps:**

1. Ask Sean for (a) the topic (one sentence) and (b) optionally his own draft (to compare against, not to share with the council).

2. Read the relevant voice-mode spec section from `.claude/skills/writing-voice-modes/SKILL.md` (typically "Sean Mode" unless Sean specifies a different mode).

3. Build the prompt file at `/tmp/llm-council/voice-mode-calibration-<timestamp>.md`:

   ```
   You are critiquing a writing sample written in "<mode name>" — a calibrated voice
   defined in writing-voice-modes SKILL.md.

   [paste the relevant voice-mode spec section verbatim]

   The author wants to know whether the spec is unambiguous enough that four different
   frontier models would read it the same way.

   YOUR TASK: Write a 150-word paragraph on [TOPIC] in <mode name>, following the spec
   exactly. Do not reference any existing sample — write blind from the spec only.
   ```

4. Invoke the CLI (absolute paths so this works from any repo):

   ```bash
   cd /Users/seanwinslow/Code-Brain/code-brain/tools/llm-council && uv run python -m council \
       --profile variance \
       --prompt-file /tmp/llm-council/voice-mode-calibration-<ts>.md \
       --output <ABSOLUTE-PATH-TO-OUTPUT-FILE> \
       --tag voice-mode-calibration
   ```

   Create parent directories first if they don't exist (`mkdir -p ...`). For `--output`, pick a path inside the repo whose surface you're calibrating — see §0 path resolution.

5. Read the chairman synthesis from the output file. Report back to Sean: where did the four interpretations converge, where did they diverge, what does the chairman think the spec is missing.

6. (Optional, on Sean's request) Draft a diff to `.claude/skills/writing-voice-modes/SKILL.md` based on the divergence findings.

### 2.2 Cover letter / role-fit memo critique (premium profile)

1. Ask Sean for the role context (company, role title, what he's submitting).

2. Write the prompt file:

   ```
   The author is applying for [ROLE TITLE] at [COMPANY], coming from [BACKGROUND].

   Below is their draft. Critique it on:
   1. Specificity (claims that are too generic / could apply to any candidate)
   2. Differentiators that are buried or missing
   3. Tone (confident vs. arrogant vs. hedging)
   4. Concrete edits that would improve it

   Be direct. The author wants the strongest critique, not flattery.

   === DRAFT ===

   [paste full draft]
   ```

3. Invoke the CLI with `--profile premium --tag cover-letter-<company-slug>` (use the absolute `cd` path from §2.1 step 4).

4. Output to `/Users/seanwinslow/Code-Brain/code-brain/vault/20_projects/prj-job-hunt-2026/applications/<company>/<YYYY-MM-DD>-council-critique.md`.

### 2.3 Decision pre-mortem (premium profile)

1. Ask Sean to share the decision doc or spec (read it via `Read`).

2. Write the prompt file:

   ```
   The author is about to commit to the following decision/design. Before they pull
   the trigger, surface the strongest objections.

   Each model should independently surface:
   1. The single strongest reason this could fail in production
   2. The most likely "this is fine for v0.1 but will hurt at v1.0" debt
   3. The assumption the author is making that they shouldn't be

   Be ruthless. The author wants pre-mortem, not validation.

   === DECISION/DESIGN ===

   [paste full doc]
   ```

3. Invoke the CLI with `--profile premium --tag premortem-<topic-slug>` (use the absolute `cd` path from §2.1 step 4).

4. Output to the same directory as the decision doc with `-council-premortem.md` suffix (absolute path).

### 2.4 PRD / spec stress-test (premium profile)

1. Read the PRD or spec via `Read`.

2. Write the prompt file:

   ```
   Stress-test the following PRD/spec. Each council member should independently surface:
   1. Acceptance criteria that are ambiguous or unmeasurable
   2. Missing edge cases (what happens when X is empty / large / concurrent)
   3. Hidden dependencies (this requires Y to exist first; Y isn't mentioned)
   4. Vocabulary mismatches (the term "user" is used 3 different ways)

   Quote specific lines/sections when possible.

   === PRD/SPEC ===

   [paste full doc]
   ```

3. Invoke the CLI with `--profile premium --tag spec-stress-<topic-slug>` (use the absolute `cd` path from §2.1 step 4).

4. Output next to the source doc (absolute path).

---

## 3. Cost discipline

- Every CLI invocation does a pre-flight cap check. If estimated cost > per-query cap, the CLI refuses with a clear error.
- Daily and monthly caps are enforced across BOTH profiles combined.
- The CLI never uses `--force` unless Sean has explicitly authorized it for this query.
- After a successful run, the CLI records actual spend to `/Users/seanwinslow/Code-Brain/code-brain/vault/health/council-spend-{YYYY-MM-DD}.json` (canonical — same file across all repos, so daily/monthly caps stay coherent).

If the CLI rejects a query on budget, surface the error verbatim and ask Sean whether to:
1. Wait until tomorrow (daily reset)
2. Use `--force` (per-query bypass, daily/monthly still enforced)
3. Switch to single-model Claude review

---

## 4. Failure modes

- **One model fails in Stage 1** — CLI continues with N-1 survivors; output names the missing model in the cost summary. Surface the partial output to Sean.
- **Two+ models fail in Stage 1** — CLI exits with code 3 and "Council unavailable" message. Recommend falling back to single-model Claude review.
- **Chairman synthesis fails** — CLI exits with partial transcript; Sean still has the four raw drafts + cross-rankings.

---

## 5. Output handling

Council output files are full markdown transcripts: original prompt, four named responses, cross-rank table with reasoning, chairman synthesis, cost summary. They live next to the artifact being critiqued (see §0 + workflow templates) for permanent record. Session JSON is always written to `/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council/data/sessions/<session-id>.json` (canonical archive across all repos) for machine-readable replay.

For voice-mode-calibration specifically, the run-trail is portfolio-worthy: the diff between Sean's draft and the four blind drafts is the calibration signal, accumulating over time.
