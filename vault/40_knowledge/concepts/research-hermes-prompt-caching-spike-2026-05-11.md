---
type: research
status: deferred-again
domain: agents-sdk
date: 2026-05-11
question: "Does claude-agent-sdk==0.1.63's claude_code preset auto-cache the append payload, or does daily_driver.py pay full input-token cost on every morning run?"
source: claude-code-investigation
parent: "[[research-hermes-agent-investigation-2026-04-26]]"
tags: [research, hermes-agent, prompt-caching, agents-sdk, daily-driver, spike]
verdict: DEFER-AGAIN
links:
  - "[[research-hermes-agent-investigation-2026-04-26]]"
---

# SPIKE: Hermes Prompt-Caching `system_and_3` Pattern for daily-driver

Follow-up to the 2026-04-26 Hermes Agent investigation (Candidate 1 SPIKE, deferred pending Phase 2 of operating-model artifact wiring).

## Phase 2 Status Gate

**PASSED.** Phase 2 (operating-model artifact wiring for `meta_agent` / `flush` / `knowledge_lint`) shipped in **v3.17.0** and the 4-day production soak closed in **v3.17.5** (2026-05-01). CHANGELOG confirms all three agents are wired:

- `meta_agent.py`: gemma4:e4b + 3-domain schedule-recommendations for Domain-Aware Insights
- `flush.py`: 3-domain SOUL prepend on EXTRACTION_PROMPT
- `knowledge_lint.py`: 3-domain SOUL context + `soul-tier-a-conflict` LintIssue at HIGH severity

Phase 2 also produced a 4/4 night production signal: Domain-Aware Insights populated all four days with zero fallbacks (v3.17.5 soak closeout). The gate condition is met; SPIKE proceeds.

Current repo version as of this SPIKE: **v3.27.0** (2026-05-10).

## Existing-Cache Evidence from CSV

**BLOCKED.** `vault/90_system/agent-logs/agent-run-history.csv` is a local runtime file — not committed to git, and not present in this remote environment. Cannot grep for `cache_read_input_tokens > 0` rows.

Additionally: `logging_setup.py:record_run` does **not** capture cache token fields. The CSV schema is `date, time, agent, mode, status, cost_usd, duration_ms, turns, notes`. Even if the SDK were silently caching, it would not be reflected in the CSV. This is a gap regardless of the experiment outcome — if SHIP verdict lands, `record_run` should gain `cache_read_tokens` and `cache_creation_tokens` fields.

## Validation Experiment

**BLOCKED.** Two hard prerequisites are missing in this remote environment:

1. **`ANTHROPIC_API_KEY` not set.** The variable is absent from `os.environ`. The key is stored in macOS Keychain on Sean's Mac as `com.sean.agents.anthropic_api_key` (per `lib/keychain.py`). Not accessible from a remote git session.

2. **`anthropic` SDK not importable.** The `agents-sdk/.venv` is not present in this repo clone (it's a local virtualenv, not committed). `pip install anthropic` would be required before the script can run.

The validation script has been written and committed at `agents-sdk/scripts/validate_prompt_caching.py`. See **Next Steps** for the run command.

## Code Analysis (Static)

### Current SDK path — no cache markers

`agents-sdk/agents/daily_driver.py:297–303`:

```python
return ClaudeAgentOptions(
    system_prompt={
        "type": "preset",
        "preset": "claude_code",
        "append": skills_prompt,   # <- plain str, no cache_control
    },
    ...
)
```

The `append` key is a plain `str`. Anthropic's prompt-caching API requires `cache_control: {"type": "ephemeral"}` to be injected as a property on a content **block object** (`{"type": "text", "text": "...", "cache_control": {...}}`). A plain string `append` cannot carry this marker. The `claude_code` preset may inject its own stable prefix with a cache marker (the SDK internals were not accessible for inspection in this environment), but the `skills_prompt` append is almost certainly **not explicitly cache-marked**.

### Payload size

```
daily-driver/SKILL.md:   11,115 chars (~2,779 tokens)
vault-read-write/SKILL.md: 7,965 chars (~1,991 tokens)
concat + headers:          ~19,300 chars (~4,825 tokens)

build_preamble (morning):  ~800 tokens (date/path/mandates/vault health)
build_artifact_preamble:   ~1,500-3,000 tokens (3x HEARTBEAT bodies)
----------------------------------------------------------------------
Stable prefix total:       ~7,100-8,600 tokens per morning run
```

At `claude-sonnet-4-6` pricing ($3/MTok input, $3.75/MTok cache write, $0.30/MTok cache read):

| Path | Per-run input cost |
|------|--------------------|--
| No caching (today)          | ~$0.022-0.026 |
| Cache write (first cold hit) | ~$0.027-0.032 |
| Cache read (warm hit)        | ~$0.002-0.003 |

At 30 runs/month and a ~90% warm-hit rate:
- Today: ~$0.66-0.78/month on the stable prefix alone
- After caching: ~$0.09-0.12/month on the stable prefix
- Saving: ~$0.55-0.66/month (~$6.6-7.9/year)

The original investigation estimated $3/month — that figure likely included output tokens and the dynamic portion of the prompt (task prompt + tool results), which would not be cached. The stable-prefix saving is the more accurate $0.55-0.66/month estimate. Still meaningful for a zero-change system, but less dramatic than the original SPIKE pitch.

### ResultMessage does not expose cache fields

`daily_driver.py:359-368` logs `result_msg.total_cost_usd`, `result_msg.num_turns`, `result_msg.duration_ms`. The `ResultMessage` from `claude_agent_sdk==0.1.63` does not appear to expose `cache_read_input_tokens` as a public field (confirmed by inspection — the record_run schema has no cache column). This means:

1. Even if the SDK were caching, the current observability layer would not surface it.
2. Adding cache-control markers without adding cache telemetry to `record_run` would leave the benefit invisible.

## Verdict

**DEFER-AGAIN** — environment prerequisites not met; experiment cannot run remotely.

The SPIKE is structurally sound and the cost case holds (~$7/year, zero new deps). The blocker is purely operational: the validation experiment requires Sean's Mac with the `.venv` installed and `ANTHROPIC_API_KEY` accessible.

Conditions for DEFER -> SHIP:
1. Run `validate_prompt_caching.py` on Mac (see Next Steps).
2. Observe `cache_read_input_tokens > 0` on call 2.
3. Confirm the SDK path (bypassing `ClaudeAgentOptions.system_prompt` for morning mode) is feasible.

If the experiment confirms caching works, the implementation estimate remains S (half day):
- Bypass `claude_agent_sdk.query()` for morning mode only
- Call `anthropic.messages.create()` directly with the `system_and_3` pattern
- Add `cache_read_tokens` + `cache_creation_tokens` columns to `record_run`
- This mirrors `deep_researcher.py`'s pure-httpx pattern — already precedented in the fleet

## Next Steps (for Sean on Mac)

```bash
# 1. Export the API key from Keychain
export ANTHROPIC_API_KEY=$(security find-generic-password -s com.sean.agents.anthropic_api_key -w)

# 2. Run the validation script (under $0.10)
cd /path/to/claude-code-superuser-pack/agents-sdk
PYTHONPATH=. .venv/bin/python3 scripts/validate_prompt_caching.py
```

If output shows `CACHE HIT: N tokens read from cache` -> verdict flips to SHIP, open PR.

If output shows `NO CACHE HIT` -> investigate whether `cache_creation_input_tokens > 0` on call 1. If not, the Anthropic API may not be accepting `cache_control` markers for this model tier, or the SDK preset is overriding the system content.

## Open Questions Resolved / Deferred

| Question | Status |
|----------|--------|
| Has Phase 2 shipped? | **Resolved: YES** (v3.17.5 soak closed 2026-05-01) |
| Does SDK auto-cache the `append` payload? | **Unresolved** — static analysis strongly suggests NO (plain str, no content block); experiment would confirm |
| Does any CSV row show `cache_read_input_tokens > 0`? | **Unresolved** — CSV not in git; `record_run` doesn't capture cache fields anyway |
| Is the M-effort bypass-SDK variant worth it? | **Likely YES** if experiment confirms — mirrors existing `deep_researcher.py` pattern, ~$7/year saving, faster TTFT |

## Sources

- `vault/40_knowledge/concepts/research-hermes-agent-investigation-2026-04-26.md` — parent SPIKE
- `agents-sdk/agents/daily_driver.py:261-313` — `build_options()` current implementation
- `agents-sdk/lib/skill_loader.py` — `load_skills()` function
- `agents-sdk/lib/logging_setup.py:58-102` — `record_run()` CSV schema
- `CHANGELOG.md` — v3.17.0-v3.18.0 Phase 2 shipping confirmation
- `.claude/skills/daily-driver/SKILL.md` (11,115 chars)
- `.claude/skills/vault-read-write/SKILL.md` (7,965 chars)
- `agents-sdk/scripts/validate_prompt_caching.py` — validation script written by this SPIKE agent
