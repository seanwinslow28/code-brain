# Daily-Driver Cost Fix — Model Swap + Cap Tripwire

**Date:** 2026-06-16
**Author:** Sean (via Claude Code brainstorming)
**Status:** Approved design — ready for implementation plan
**Scope:** `agents-sdk/agents/daily_driver.py`, `agents-sdk/config.toml`

## Problem

The daily-driver morning agent has been creeping toward and tripping its budget cap:

| Date range | Cost/run | Event |
|---|---|---|
| 5/18–5/27 | ~$0.50 | baseline |
| 5/28 | $0.70 | fleet-memory MCP bridge went live |
| 5/29 | **$0.97 cap-hit** | fleet-memory doubled per-turn overhead (subsequently disabled) |
| 6/02–6/11 | $0.68 → $0.85 | steady prompt/output creep |
| 6/12, 6/15 | **$0.91 cap-hits** | tripped the $0.90 cap |
| 6/16 | $0.88 | ran under the new $1.25 cap (raised 6/15, PR #80) |

Raising the cap (0.60 → 0.90 → 1.25) chases the creep instead of removing its cause.

## Root Cause

The morning run executes a **templated note task** — read yesterday's note, fill a
template, inject a ~200-token fleet digest verbatim, write a 1-3-5 plan — on **Opus**,
in 5–7 turns. `build_options()` in `daily_driver.py` sets no `model`, so the agent
inherits the OAuth default (Opus). config.toml itself names this "the Opus daily_driver
path" ([config.toml:592](../../../agents-sdk/config.toml#L592)).

**Ruled out:**
- **MCPs are not the driver.** This is a headless SDK agent; per CLAUDE.md it cannot
  reach cloud MCPs (Slack/Calendar/Gmail need interactive OAuth). Its only MCP is the
  local `vault_inject` tool. Disabling MCPs saves ~nothing.
- **Pulled-content size is not the driver.** The injected fleet digest measures ~803
  chars (~200 tokens). The preamble is modest; the dominant cost is the model tier
  applied across 5–7 turns, not the input volume.

## Decision Summary (from brainstorming)

| Decision | Choice |
|---|---|
| Model strategy | **Swap morning to Sonnet 4.6** (~5× cheaper; task is well within Sonnet's range) |
| Budget cap | **$0.50** tripwire (~2.7× expected Sonnet cost; still below the ~$0.88 Opus floor) |
| Scope | **Model + cap only** — no preamble/skill trimming now |
| Verification | **Dry-run today + tomorrow's 08:45 scheduled run** (no extra side-effects) |

## The Fix — Two Changes

### Change 1: Per-mode model override in `build_options()`

`daily_driver.py:414-423` already resolves `max_turns` and `max_budget_usd` from the
per-mode table `[agents.daily_driver.modes.{mode}]`. Add a `model` read in the same
shape, then thread it into `ClaudeAgentOptions`:

```python
model = mode_cfg.get("model")  # None ⇒ omit ⇒ SDK uses OAuth default (Opus)
...
return ClaudeAgentOptions(
    ...
    model=model,
    ...
)
```

- When the key is **absent**, `model` is `None` and behavior is unchanged (Opus). This
  keeps evening/weekly modes untouched and makes rollback a one-line config delete.
- The `"sonnet"`/`"opus"` aliases are a proven OAuth SDK pattern in this repo
  (skill_optimizer: [config.toml:507-509](../../../agents-sdk/config.toml#L507-L509)).
- Implementation note: confirm the `ClaudeAgentOptions` kwarg is named `model` in the
  pinned SDK (`0.1.63`) before finalizing; passing `None` must mean "use default."

### Change 2: config.toml — morning mode block

In `[agents.daily_driver.modes.morning]`:
- **add** `model = "sonnet"`
- **change** `max_budget_usd = 1.25` → `0.50`
- **replace** the dated comment block with the 2026-06-16 rationale (Opus→Sonnet swap,
  cap reset to a regression tripwire). Preserve the historical context that the prior
  bumps were creep-chasing, now superseded by the model swap.

## Expected Result

- ~$0.15–0.20/run (down from $0.88).
- ~$5–6/month worst case (was ~$27–37).
- Cap-hits stop and **stay** stopped: even with continued prompt creep, Sonnet has
  ~2.7× headroom against the $0.50 cap, and an accidental Opus regression (~$0.88)
  trips the cap loudly instead of billing silently.

## Verification

1. **Dry-run** (free, zero side-effects):
   `cd agents-sdk && PYTHONPATH=. .venv/bin/python3 agents/daily_driver.py --mode morning --dry-run`
   → confirm `Max budget: $0.5` and that the resolved model is `sonnet`.
2. **Tomorrow's 08:45 scheduled run** is the real test (no manual live run today, to
   avoid a second idempotent portfolio commit). Afterward, check
   `vault/90_system/agent-logs/agent-run-history.csv` for the 6/17 morning row:
   - cost should land ~$0.15–0.20 (vs 6/16 Opus $0.8847)
   - status `success`
3. **Quality check:** eyeball tomorrow's daily note — valid 1-3-5 plan present, fleet
   digest injected verbatim at the `<!-- fleet-overnight -->` anchor.

## Rollback (instant, config-only)

- Delete `model = "sonnet"` from the morning block → reverts to Opus.
- Restore `max_budget_usd = 1.25` if $0.50 ever proves too tight.
- No code path changes when the `model` key is absent, so Change 1 is inert without
  Change 2.

## Out of Scope (deferred)

Per the "model + cap only" decision, the following are **not** done now and should be
captured as a follow-up ticket if cost is still a concern after the Sonnet baseline is
measured:
- Preamble trimming (3-domain HEARTBEATs, vault health, synth manifest, critic health,
  job-feed summary) — these *are* the morning brief's content; trimming changes what
  Sean reads.
- Dropping the redundant `vault-read-write` skill from the system prompt.
- Slimming the `claude_code` preset system prompt.
- Evening/weekly model overrides (both modes are currently unscheduled/disabled).

## Doc Updates Required

- CHANGELOG.md entry (config + agent behavior change).
- The morning-mode comment block in config.toml is the canonical changelog for the cap
  history; keep that lineage intact.
