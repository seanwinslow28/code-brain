---
type: handoff
parent: 2026-05-06-unified-roadmap.md
task: Task 12 — Judge Layer Retrofit (Council Gap-Fill 1)
project: prj-job-hunt-2026
created: 2026-05-31
status: handoff
ai-context: "Day-6 wire-up handoff. Cowork session built Steps 5-7 (substack-drafter judge wire-up + --demo-injection + EXPLANATION.md) against the mounted source under a sandbox Python. The Mac .venv can't run in the Linux sandbox, so the full-suite regression, validate.py, the live --demo-injection take, and the commit/tag are Sean's host moves. Steps 8-9 (Loom + LinkedIn) follow."
---

# Task 12 Day 6 — Judge Layer wire-up handoff

B7 gate closed the morning of 2026-05-31 (synth `concepts_written` ran 2 → 13 → 57 → 8 → 1 → 28 over the prior six nights — six consecutive positive nights, well past the strict 5). Day 6 was unblocked, so this Cowork session shipped **Steps 5, 6, and 7**. Steps 8-9 (Loom + LinkedIn + commit/tag) are yours on the Mac host.

## What shipped this session

**Step 5 — judge wired into the substack-drafter.**
- `lib/judge/schema.py` — added one field to `ActionProposal`: `content_preview: Optional[str] = None`. This closes a real Day-1-3 gap: the eight original fields are all metadata, none carried the draft text the policy rules ("the draft attributes a quote…") actually read. Without it the judge sees only metadata and always falls through to `ALLOW`. The Day-3 unit tests hid this by mocking the model response. **This is the load-bearing fix** — it's also the best line in the EXPLANATION and a strong interview beat.
- `lib/judge/judge.py` — `_build_user_prompt` now renders `content_preview` in a fenced `--- BEGIN/END DRAFT UNDER REVIEW ---` block after the metadata, so the local model knows which text the rules apply to.
- `agents/substack_drafter.py` — split persistence out of `write_draft` into `_persist_draft` (behavior-preserving), added `_build_action_proposal`, `route_with_judge` (the 5-outcome dispatcher with a bounded REVISE→retry→ESCALATE loop), and `_notify_judge_outcome` (best-effort Pushover for BLOCK/ESCALATE). Threaded `judge_enabled` through `main()` and `_cli()`.
- `config.toml` — added `[substack_drafter].judge_enabled = false` and a new `[judge_layer]` table (`enabled = false`, `max_retries_on_revise = 2`, `quarantine_subdir = "quarantine"`). **The judge engages only when BOTH `[judge_layer].enabled` AND `[substack_drafter].judge_enabled` are true.** Both default false → today's behavior is byte-for-byte unchanged.

**Step 6 — `--demo-injection` flag.**
- `agents/substack_drafter.py` — `--demo-injection [FRAGMENT]` on the CLI (mutually exclusive with `--voice`). It loads a synthetic rule-tripping fragment, appends it to the user prompt via `compose_prompt`, and forces the judge on for that run (so you don't have to edit config before recording). Fragment text lives in data, not source.
- `policies/demo_injection_fragments.yaml` — two fragments: `default` (fabricated quote from a named figure → `ESCALATE` via rule_a) and `revise_citation` (uncited Block metric → `REVISE` via rule_b). Production never loads this file.

**Step 7 — 4Q EXPLANATION.**
- `lib/judge/EXPLANATION.md` — recruiter-readable, leads on the actor-judge separation, names fail-open as a deliberate Tier-A-preserving choice, and tells the `content_preview` discovery story under "What would break?".

## Sandbox verification (already done here)

The Mac `.venv` symlinks to macOS Python and can't execute under the Linux sandbox, so a sandbox Python 3.10 (pydantic / pyyaml / httpx / pytest) ran against the mounted source:

- `python3 -m py_compile` clean on all four modified modules; `config.toml` parses.
- **145 passed** across `test_judge_schema / test_judge_policy / test_judge_evaluate / test_judge_ledger / test_substack_drafter / test_substack_drafter_judge_integration` (15 new integration tests).
- Import + wire smoke: policy loads (4 rules), proposal carries `content_preview`, demo fragment loads.

## Your host moves (do these on the Mac)

```bash
cd ~/Code-Brain/agents-sdk

# 1. Full-suite regression (expect the 2 known pre-existing fleet-memory reds only)
PYTHONPATH=. .venv/bin/pytest tests/ -q

# 2. Repo validator (expect PASSED / 0 errors; warnings are pre-existing)
cd ~/Code-Brain && python3 scripts/validate.py && cd agents-sdk

# 3. Live judge demo (real gemma4:e4b on Mac Mini Ollama — this is the Loom take).
#    --demo-injection forces the judge on; no config edit needed.
PYTHONPATH=. .venv/bin/python3 agents/substack_drafter.py --demo-injection
#    → ESCALATE expected: draft lands in <output_dir>/quarantine/, urgent Pushover.
#    For the REVISE→retry→ALLOW take instead:
PYTHONPATH=. .venv/bin/python3 agents/substack_drafter.py --demo-injection=revise_citation
#    Inspect the ledger row the demo wrote:
tail -1 vault/health/judge_log/$(date -u +%F).jsonl | python3 -m json.tool
```

Note: the live demo needs `enabled = true` in `[substack_drafter]` only if you run it *without* `--demo-injection`. With the flag, the judge is forced on regardless — but the agent's own top-level `enabled` kill-switch in `_cli()` still applies, so flip `[substack_drafter].enabled = true` for the recorded take, then flip it back.

## Steps 8-9 — still yours

- **90-sec Loom** (Step 8). Suggested beat sheet: (1) show `policies/substack_drafter.yaml` — "these four rules are the contract, a recruiter reads YAML not Python"; (2) run `--demo-injection`; (3) show the `ActionProposal` with `content_preview`; (4) judge returns `ESCALATE`/`REVISE`; (5) `tail` the JSONL ledger row; (6) note the draft went to quarantine, never published. Close: **"Agents draft. I send. Every word."**
- **LinkedIn post** (Step 8) — ~120 words, your hand on every word, tag Anthropic + the FDE-Boston JD URL from `target-companies.md`, link `seanwinslow.com/transactions/judge-layer/` (after the Gap-Fill 3 deploy + ledger row land).
- **Commit + tag** (Step 9). Paste-ready CHANGELOG block:

```
## [judge-layer-v0.1.0] - 2026-06-04
### Added
- Judge layer wired into Substack-Drafter (Council Gap-Fill 1 / Task 12 Step 5-7).
  ActionProposal gains a content_preview channel so policy rules evaluate the
  draft body, not just metadata. route_with_judge() dispatches the 5 outcomes
  (ALLOW/JUDGE_UNAVAILABLE fall open → persist; REVISE → bounded retry → ESCALATE;
  ESCALATE → quarantine; BLOCK → no write). --demo-injection flag + data-only
  demo_injection_fragments.yaml for the reproducible Loom take. New [judge_layer]
  config table + [substack_drafter].judge_enabled; judge engages only when both true.
- lib/judge/EXPLANATION.md (4Q).
```

Suggested commit message: `feat(judge): wire judge layer into substack-drafter — content_preview + 5-outcome dispatch + --demo-injection (Task 12 Steps 5-7)`. Tag `judge-layer-v0.1.0`.

## Two notes for the record

- **CLAUDE.md / README count bump:** the judge module already existed (Days 1-5), so this is a wire-up, not a new top-level surface. If you want the module reflected in the CLAUDE.md architecture table, add a row under the agents-sdk subsystem table — your call; not strictly required by the doc rule since no new skill/agent/hook/script was added.
- **Tickets filed** in `vault/00_inbox/tickets.md`: Steps 8-9 host moves, and the gated `/transactions/judge-layer` ledger row (blocked on the Gap-Fill 3 personal-site deploy).
