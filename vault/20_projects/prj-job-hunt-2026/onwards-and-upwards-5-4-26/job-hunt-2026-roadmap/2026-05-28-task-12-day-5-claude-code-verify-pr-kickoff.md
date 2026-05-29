---
type: kickoff
project: prj-job-hunt-2026
parent_task: task-12-judge-layer
created: 2026-05-28
target: claude-code
ai-context: "Claude Code kickoff — verify Task 12 Day 5 (judge-layer ledger + judge_action wrapper) end-to-end on the Mac host, then open a PR with the verbatim commit message. Paste the block below into Claude Code from inside ~/Code-Brain/code-brain."
---

# Claude Code Kickoff — Verify Task 12 Day 5 + Open PR

Paste everything inside the fenced block into Claude Code, running from
`~/Code-Brain/code-brain`.

```
You are verifying Task 12 Day 5 of the judge-layer retrofit (Council Gap-Fill 1)
in the Code-Brain repo, then opening a PR. The Day 5 work was authored in a
prior Cowork session and is sitting UNCOMMITTED in the working tree. Your job:
prove it's correct, then commit + open a PR. Do NOT change the implementation to
make a test pass without surfacing it to me first.

────────────────────────────────────────────────────────────────────────────
WHAT DAY 5 SHIPPED (the diff you're verifying)
────────────────────────────────────────────────────────────────────────────
Four files under agents-sdk/, all uncommitted:
  - agents-sdk/lib/judge/ledger.py        (NEW, ~258 lines) — JSONL ledger
        writer. write_decision(decision, proposal, *, agent_name,
        ledger_dir=None) -> Path; atomic append under lib.filelock.FileLock
        (exclusive, timeout=5.0) → LedgerWriteError on LockTimeout/OSError;
        UTC-midnight date bucketing off JudgeDecision.evaluated_at;
        matched_rule_id derived from proposal.authorization_basis; full
        ActionProposal model_dump in the row. ensure_ledger_ready() boot check
        (mkdir + writable-probe + pushover.ensure_credentials_or_raise()).
        LedgerError / LedgerWriteError mirror pushover.py's exception shape.
  - agents-sdk/lib/judge/action.py        (NEW, ~112 lines) — judge_action(
        proposal, policy, *, agent_name, ledger_dir=None) -> JudgeDecision.
        Option-B wrapper: calls the PURE evaluate(), writes the ledger, fires a
        best-effort severity-0 Pushover ping on JUDGE_UNAVAILABLE. Never raises.
  - agents-sdk/lib/judge/__init__.py       (MODIFIED, +15) — exports
        judge_action, write_decision, ensure_ledger_ready, LedgerError,
        LedgerWriteError.
  - agents-sdk/tests/test_judge_ledger.py  (NEW, ~436 lines) — 19 tests / 7
        classes (write/append/UTC-bucket/atomicity/boot-check/rule-id/
        judge_action integration). All use tmp_path; none touch real vault/.

Full session narrative + rationale:
  vault/.../job-hunt-2026-roadmap/2026-05-28-task-12-day-5-handoff.md

DESIGN INVARIANTS — these are council-locked, DO NOT touch them to fix a test:
  1. JudgeDecision + ActionProposal schema (lib/judge/schema.py) is FROZEN.
  2. Outcome enum (5 values incl. JUDGE_UNAVAILABLE) is FROZEN.
  3. evaluate() never raises and stays PURE (Option B was chosen specifically
     so evaluate() is untouched — confirm git diff shows NO change to
     lib/judge/judge.py or lib/judge/schema.py or lib/judge/policy.py).
  4. policies/substack_drafter.yaml stays at exactly 4 rules. matched_rule_id
     is a reference to an existing rule, never a 5th.
  5. config.toml [routing.task_map] judge_layer entry stays as-is.

────────────────────────────────────────────────────────────────────────────
STEP 1 — PRE-FLIGHT (read state before doing anything)
────────────────────────────────────────────────────────────────────────────
  cd ~/Code-Brain/code-brain
  git status                  # confirm the 4 Day-5 files are untracked/modified
  git log --oneline -8        # note HEAD; confirm tag 4dd0743 judge-layer-v0.0.1-infra is in history
  git branch --show-current   # expected: feature/fleet-memory-phase-1
  git diff --stat -- agents-sdk/lib/judge/judge.py agents-sdk/lib/judge/schema.py agents-sdk/lib/judge/policy.py agents-sdk/policies/substack_drafter.yaml agents-sdk/config.toml
      # MUST be empty — Option B means none of these changed. If any show a
      # diff, STOP and tell me; an invariant may have been violated.

If the 4 Day-5 files are NOT present as uncommitted changes, STOP — either the
session didn't save or Obsidian-Git already swept them. Report what you see.

────────────────────────────────────────────────────────────────────────────
STEP 2 — VERIFICATION GATE (all four must be green)
────────────────────────────────────────────────────────────────────────────
  cd ~/Code-Brain/code-brain/agents-sdk
  source .venv/bin/activate

  # 2a. New ledger tests in isolation (fastest signal)
  PYTHONPATH=. pytest tests/test_judge_ledger.py -v
      # Expected: 19 passed.

  # 2b. All judge tests
  PYTHONPATH=. pytest tests/test_judge_*.py -v
      # Expected: prior judge baseline (79 on this host) + 19 new, all green.
      # Report the exact collected count — don't assume; counts drift by env.

  # 2c. FULL SUITE — the regression gate the Cowork sandbox could not run
  PYTHONPATH=. pytest tests/ -v
      # Expected: 802-passed / 2-failed baseline (the 2 are PRE-EXISTING
      # fleet-memory reds, NOT judge-induced) + 19 new = ~821 passed / 2 failed.
      # If you see ANY red beyond those 2 known fleet-memory failures, STOP and
      # show me the failure — do not proceed to the PR.

  # 2d. Repo validator (from repo root)
  cd ~/Code-Brain/code-brain && python3 scripts/validate.py
      # Expected: Validation PASSED, warnings <= 62, 0 errors. Note: ruff is
      # NOT a project dep — skip any ruff step.

  # 2e. Smoke import of the new public surface
  cd ~/Code-Brain/code-brain/agents-sdk
  PYTHONPATH=. python3 -c "
from lib.judge.ledger import write_decision, ensure_ledger_ready, LedgerError, LedgerWriteError
from lib.judge import judge_action
print('Day 5 imports green')
"

────────────────────────────────────────────────────────────────────────────
STEP 3 — LIVE LEDGER ROUND-TRIP SMOKE (prove it actually writes + round-trips)
────────────────────────────────────────────────────────────────────────────
Write to a TEMP dir, never the real vault/health/judge_log. This exercises the
real FileLock + JSONL append + UTC bucketing + proposal round-trip end to end:

  cd ~/Code-Brain/code-brain/agents-sdk
  PYTHONPATH=. python3 -c "
import json, tempfile
from pathlib import Path
from datetime import datetime, timezone
from lib.judge.ledger import write_decision
from lib.judge.schema import ActionProposal, JudgeDecision, Outcome

tmp = Path(tempfile.mkdtemp())
proposal = ActionProposal(
    intended_action='write_substack_draft',
    target_surface='vault/.../substack-drafts/smoke.md',
    evidence_used=['chunk_id:abc'],
    authorization_basis='substack_drafter.yaml#rule_d_publish_verb_at_top_level',
    expected_consequence='A local markdown draft lands.',
    rollback_path='rm smoke.md',
    exposure_level='local-only',
    human_review_required=True,
)
decision = JudgeDecision(
    outcome=Outcome.ALLOW, model_used='gemma4:e4b', latency_ms=412,
    evaluated_at=datetime(2026,5,28,12,0,0,tzinfo=timezone.utc),
)
path = write_decision(decision, proposal, agent_name='substack_drafter', ledger_dir=tmp)
print('wrote:', path, '(expect filename 2026-05-28.jsonl)')
row = json.loads(path.read_text().splitlines()[0])
print('keys:', sorted(row))
print('matched_rule_id:', row['matched_rule_id'])   # expect rule_d_publish_verb_at_top_level
rebuilt = ActionProposal.model_validate(row['proposal'])
print('proposal round-trips:', rebuilt == proposal)  # expect True
"
      # Expect: filename 2026-05-28.jsonl, all 9 keys present, rule_d derived,
      # proposal round-trips True.

OPTIONAL (only if you want to exercise the boot check too): run
  PYTHONPATH=. PUSHOVER_USER_KEY=x PUSHOVER_API_TOKEN=y python3 -c "
from pathlib import Path; import tempfile
from lib.judge.ledger import ensure_ledger_ready
ensure_ledger_ready(ledger_dir=Path(tempfile.mkdtemp())/'judge_log'); print('boot check OK')
"
Do NOT run ensure_ledger_ready against the real vault path, and do NOT send a
real Pushover notification.

If anything in Steps 2-3 is unexpected, STOP and report before touching git.

────────────────────────────────────────────────────────────────────────────
STEP 4 — COMMIT + OPEN PR
────────────────────────────────────────────────────────────────────────────
Branch hygiene first. The Day-5 changes are uncommitted on
feature/fleet-memory-phase-1. Create a dedicated branch so the PR is a clean
Day-5 increment:

  cd ~/Code-Brain/code-brain
  git switch -c feature/judge-layer-day5      # carries the uncommitted changes onto the new branch

Stage ONLY the four Day-5 files by explicit path — do NOT use `git add -A` or
`git commit -am` (that would sweep vault docs, the kickoff files, and anything
Obsidian-Git is mid-writing):

  git add agents-sdk/lib/judge/ledger.py \
          agents-sdk/lib/judge/action.py \
          agents-sdk/lib/judge/__init__.py \
          agents-sdk/tests/test_judge_ledger.py
  git status                                  # confirm ONLY those 4 are staged

The vault/ docs (the Day-5 handoff, the roadmap checkbox flip, the completion-
log entry) are owned by the Obsidian-Git plugin and must NOT be in this PR —
leave them unstaged.

Commit with this message VERBATIM:

  git commit -m "feat(judge): ship Task 12 Day 5 — JSONL ledger writer + boot check + judge_action wrapper (Council Gap-Fill 1)" -m "Day 5 makes judge decisions observable. Adds the JSONL ledger writer, the boot-time readiness check, and the Option-B effects wrapper that records every decision and alerts on JUDGE_UNAVAILABLE — without touching the pure evaluate().

OPTION B (locked by Sean): evaluate() stays pure and unchanged; the new judge_action() wrapper does the I/O. All 24 Day-3 evaluate tests stay green untouched.

WHAT SHIPPED
  lib/judge/ledger.py    write_decision() atomic-FileLock JSONL append (LedgerWriteError on LockTimeout/OSError), UTC-midnight date bucketing off JudgeDecision.evaluated_at, 9-key row schema incl. matched_rule_id derived from authorization_basis + full ActionProposal model_dump. ensure_ledger_ready() mkdir+writable-probe+pushover.ensure_credentials_or_raise(). LedgerError/LedgerWriteError mirror pushover.py.
  lib/judge/action.py    judge_action() — evaluate() + ledger write (LedgerError caught+logged) + best-effort severity-0 Pushover on JUDGE_UNAVAILABLE (PushoverError caught+logged). Never raises.
  lib/judge/__init__.py  exports judge_action, write_decision, ensure_ledger_ready, LedgerError, LedgerWriteError.
  tests/test_judge_ledger.py  19 tests / 7 classes; all tmp_path, never touches real vault/health/.

DESIGN INVARIANTS PRESERVED
  JudgeDecision schema FROZEN; 5-value Outcome enum FROZEN; evaluate() never-raises + pure (untouched); substack_drafter.yaml stays at 4 rules; judge_layer routing unchanged.

Closes Task 12 Step 4 (Day 5) of unified-roadmap §Task 12."

Push and open the PR:

  git push -u origin feature/judge-layer-day5

Determine the PR base before creating it:
  - Check whether the Days 1-3 judge commits (4dd0743) are already in `main`:
        git merge-base --is-ancestor 4dd0743 origin/main && echo "in main" || echo "NOT in main"
  - If the judge Days 1-3 work is NOT yet in main, the cleanest base for a
    Day-5-only diff is feature/fleet-memory-phase-1 (the branch you forked
    from) — that makes the PR show EXACTLY the 4 Day-5 files. If you'd rather
    target main, the diff will also include whatever else is on
    feature/fleet-memory-phase-1 that isn't in main; note that in the PR body.
  - If unsure which base I want, STOP and ask me before creating the PR.

Create the PR with `gh` (set --base per the decision above; default to
feature/fleet-memory-phase-1 for a clean Day-5-only diff):

  gh pr create \
    --base feature/fleet-memory-phase-1 \
    --head feature/judge-layer-day5 \
    --title "feat(judge): Task 12 Day 5 — JSONL ledger writer + judge_action wrapper" \
    --body "$(cat <<'PRBODY'
## Task 12 Day 5 — Judge Layer ledger + Option-B wrapper

Makes judge decisions observable: every JudgeDecision lands one JSON line at
vault/health/judge_log/<YYYY-MM-DD>.jsonl, the surface the Task 11 dashboard
reads. evaluate() stays pure (Option B) — a new judge_action() wrapper does the
I/O and fires a severity-0 Pushover ping on JUDGE_UNAVAILABLE.

### Files
- `agents-sdk/lib/judge/ledger.py` (NEW) — write_decision() atomic-FileLock JSONL append, UTC-midnight bucketing, matched_rule_id derivation, ensure_ledger_ready() boot check, LedgerError/LedgerWriteError.
- `agents-sdk/lib/judge/action.py` (NEW) — judge_action() Option-B wrapper; never raises.
- `agents-sdk/lib/judge/__init__.py` (MODIFIED) — exports the new surface.
- `agents-sdk/tests/test_judge_ledger.py` (NEW) — 19 tests / 7 classes, all tmp_path.

### Verification
- `pytest tests/test_judge_ledger.py` → 19 passed
- `pytest tests/test_judge_*.py` → all judge tests green (report count)
- `pytest tests/` → full-suite baseline holds (802 passed / 2 pre-existing fleet-memory reds) + 19 new; zero judge-induced regressions
- `python3 scripts/validate.py` → PASSED, 0 errors
- Live ledger round-trip smoke (tmp dir): row writes, 9 keys present, proposal round-trips

### Design invariants preserved
JudgeDecision schema frozen · 5-value Outcome enum frozen · evaluate() pure + never-raises (untouched) · substack_drafter.yaml stays at 4 rules · judge_layer routing unchanged.

Closes Task 12 Step 4 (Day 5). Day 6 (substack-drafter wire-up) is gated on the B7 synthesizer gate closing — not in this PR.
PRBODY
)"

────────────────────────────────────────────────────────────────────────────
HAND BACK
────────────────────────────────────────────────────────────────────────────
Report: the exact test counts from 2b + 2c, the validate.py result, the live
smoke output, the PR URL, and which --base you used. If you stopped at any gate,
report the gate + the failure verbatim and DO NOT open the PR.
```
