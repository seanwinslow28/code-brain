# Claude Code prompt — fix the SDK blocker and run the writing-voice-modes eval

> Paste everything below the line into Claude Code, run from the repo root (~/Code-Brain/code-brain).

---

# Mission

Make `python -m agents.skill_optimizer --score-only` run to completion on this Mac, then run it and
report the scores. It currently dies with a generic `exit code 1` from the Claude Agent SDK. Your job
is to diagnose the real cause, fix it, run the eval, and report. You have the machine, the CLI, the
SDK, OAuth, and Ollama right here — use them. You may research the `claude-agent-sdk` / `claude` CLI
online if needed.

## THE HARD CONSTRAINT (read twice — non-negotiable)

Generation MUST bill my Claude **subscription** via `claude login` OAuth, and must **NEVER** use an
Anthropic **API key**. I removed all `ANTHROPIC_API_KEY`s from this machine after an eval drained my
API credit. Therefore:
- Do NOT set, export, or pass `ANTHROPIC_API_KEY` anywhere. Verify none is in the environment
  (`echo $ANTHROPIC_API_KEY` should be empty) and keep it that way.
- The fix must keep billing on the subscription (Agent SDK over OAuth, or the `claude` CLI directly,
  which is also OAuth). If the ONLY way you can make it work is an API key, **STOP and ask me** — do
  not spend API money. A working run on the subscription is the entire point.
- The score-only run is ~105 generations on Opus via the subscription. That consumes subscription
  quota, not dollars. That's expected and fine. Watch for rate-limiting, not cost.

## What this eval is (background)

This is part of a long project calibrating the `writing-voice-modes` skill to my personal writing
voice. The `skill_optimizer` is an autoresearch harness (generate → judge → keep/revert). I added a
`--score-only` mode that scores the CURRENT `SKILL.md` once (no mutation, no git, no keep/revert) and
writes a `score-only-<date>` row to results.tsv. I need that number to see whether a big recent
overhaul (grit register / 90-10 rearchitecture / reference governor) helped. The prior baseline to
compare against is **train_score 0.7267** (the 2026-05-10 iteration-1 row already in results.tsv).

Pipeline for one score-only run: for the 5 training + 2 holdout prompts in
`.claude/skills/writing-voice-modes/evals.yaml`, generate 15 outputs each (Opus, via subscription),
then score each output with 3 structural checks (free, local Python) + 3 LLM-judge criteria (Qwen3-14B
local via Ollama). Aggregate, write the row.

## Current state — files and what's been tried

Key files:
- `agents-sdk/agents/skill_optimizer.py` — the harness. Relevant pieces:
  - `_SubscriptionClient` — routes generation/judge calls through `claude_agent_sdk.query()` over
    OAuth (NO api key). Exposes `.messages.create()` and `.complete()`. This is where the failure is.
  - `run_score_only(config, dry_run, debug)` — the entry point `--score-only` calls.
  - `generate_outputs()` — loops `client.messages.create(model=..., system=skill_md, messages=[...])`.
- `agents-sdk/config.toml` `[agents.skill_optimizer]` — `generator_model = "opus"`,
  `judge_model_local = "qwen3-14b-research:latest"`, `ollama_base_url = "http://localhost:5050"`.
- SDK source (read it): `agents-sdk/.venv/lib/python3.13/site-packages/claude_agent_sdk/` —
  especially `_internal/transport/subprocess_cli.py` and `_internal/query.py`.

What's already been tried (by a Cowork session that could NOT run the SDK, so these were source-read
fixes, not verified):
1. Model string was `claude-opus-4-7` (invalid ID) → changed to the alias `"opus"` (config + code).
   This did NOT fix it.
2. Removed `setting_sources=[]` and `allowed_tools=[]` from the options (they emitted empty-valued
   flags like `--setting-sources=`). Still fails.
3. Wired the SDK `stderr` callback (`opts["stderr"]`) → prints `[claude-cli] ...`. On the failing run
   it produced NO output, meaning the CLI started, accepted the query, and failed mid-run reporting a
   generic error over the control channel (`query.py` ~line 740 raises `message.get("error")`), not
   via stderr.
4. Added a `--debug` flag that sets `extra_args={"debug-to-stderr": None}` so the CLI runs verbose.

Confirmed from the SDK source: `env` is MERGED with os.environ (so `env={}` is fine, OAuth path is
intact); the CLI is found via `shutil.which("claude")` (no CLINotFoundError, so it's on PATH); `model`
is passed straight through as `--model <value>`; there is a CLI version check.

## Diagnostic ladder (start here)

1. Confirm no API key and that the bare CLI works non-interactively on the subscription:
   - `echo "key set? [$ANTHROPIC_API_KEY]"`
   - `claude --version`
   - `claude --print "say hello in five words"`
   - `claude --print --model opus "say hello in five words"`
   This isolates CLI/auth/model from the harness. (Note: you ARE a `claude` process; you'll be
   spawning a nested one. The SDK strips `CLAUDECODE` from the child env, so nesting is expected to
   work, but be aware of it.)
2. Run the harness with debug to capture the real error:
   - `cd agents-sdk && PYTHONPATH=. .venv/bin/python -m agents.skill_optimizer --score-only --debug 2>&1 | tee /tmp/voice-eval-debug.log`
   - Read the `[claude-cli]` lines and the full traceback in the log.
3. Confirm the local judge is reachable (needed for the full run, not the generation fix):
   - `curl -s http://localhost:5050/api/tags` (Ollama) and confirm `qwen3-14b-research:latest` exists
     (`ollama ls`). If Ollama is down or the model is missing, start/pull it.

Interpretation:
- `claude --print` fails → auth/CLI problem (try `claude login`) — fix that first.
- `--print` works but `--model opus` fails → Opus not available to this CLI/plan; try `--model sonnet`
  or find the correct current Opus model string and set `generator_model` in config.toml.
- both bare commands work but the harness fails → it's the harness's SDK option set; the `--debug`
  log will name it. Fix it.

## Your task

1. Run the diagnostic ladder; identify the ACTUAL root cause from real output (not a guess).
2. Fix it. You have latitude on HOW, with one constraint: stay on the subscription, never an API key.
   Acceptable approaches include:
   - Correcting the `_SubscriptionClient` options for `claude_agent_sdk.query()`.
   - If the Agent SDK path is genuinely unreliable for one-shot generation, replacing the transport
     inside `_SubscriptionClient` with a direct `claude` CLI subprocess in `--print` mode (e.g.
     `claude --print --model opus --append-system-prompt <skill> <prompt>`, capturing stdout) — this
     is ALSO OAuth/subscription-billed and may be simpler/more robust. Keep the same
     `.messages.create()` / `.complete()` interface so callers don't change.
   - Whatever else the evidence points to.
3. Run `--score-only` to completion (no `--debug` needed once it works). Confirm it wrote a
   `score-only-<date>` row to `agents-sdk/data/skill-optimizer/writing-voice-modes-results.tsv`.
4. Report: the train_score and per-criterion scores, side by side with the prior baseline (train
   0.7267; per-criterion from the 2026-05-10 row: substack_format_intro 0.36,
   anti_pattern_overreference 0.79, stylometric_distance 0.40, signature_move_present 0.81,
   sounds_like_sean 1.00, no_anti_pattern_violation 1.00). Tell me honestly whether the overhaul moved
   anything. Note: `sounds_like_sean` was already pinned at 1.00, so it can't show improvement — the
   eval is known to be blunt; flag if the result is uninformative rather than over-claiming.
5. Keep the test suite green:
   `PYTHONPATH=. .venv/bin/python -m pytest tests/test_skill_optimizer.py tests/test_stylometry.py -q`
   (was 58 passing). Update/add tests if you change the transport.

## Environment specifics

- Repo: `~/Code-Brain/code-brain`; harness under `agents-sdk/`; venv `agents-sdk/.venv` (Python 3.13).
- Always run with `PYTHONPATH=.` from inside `agents-sdk/`.
- `--score-only` skips the git-branch preflight (it never commits), but still requires the eval files
  and a calibrated stylometry threshold. The threshold is already set (`_threshold` in
  `data/skill-optimizer/stylometry_baseline.json`, ≈9.64); if it's somehow null, run
  `python scripts/calibrate_stylometry_threshold.py --reuse-existing` (key-free, no API).
- The local Qwen judge must be up at `http://localhost:5050`.

## Guardrails / stop conditions

- If the only path to a working run requires an API key, STOP and ask me. Do not spend API money.
- If Opus on the subscription is rate-limited or unavailable, tell me; don't silently fall back to a
  different model in a way that changes the measurement without flagging it.
- Don't touch the vault with git (Obsidian-Git owns it). You can edit code/config/CHANGELOG normally.

## Deliverable

A completed `--score-only` run billed to the subscription, the scores reported vs the 0.7267 baseline
with an honest read, the test suite green, and a CHANGELOG.md entry (+ a one-line note under `## Todo`
in `vault/00_inbox/tickets.md` for any follow-up). Tell me exactly what the root cause was and what you
changed.
