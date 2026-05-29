---
type: kickoff-prompt
project: prj-job-hunt-2026
parent_task: task-12-judge-layer
day: 5
target: cowork-fresh-session
created: 2026-05-28
ai-context: "Kickoff for the next Cowork session — Day 5 of Task 12 (Judge Layer). Builds the JSONL ledger writer at lib/judge/ledger.py plus boot-time Pushover credential check plus auto-ledger integration with judge.evaluate(). Days 1-3 already shipped + Claude Code verified PASS in the 2026-05-28 session. Day 6 (substack-drafter wire-up) waits on this + on B7 gate closure."
---

# Cowork kickoff prompt — Task 12 Day 5 (Ledger Writer)

> Copy everything between the `===` lines below into the new Cowork session. The rest of this file is meta-context for Sean (file map, pre-session checklist, why each scope choice is what it is).

---

```
===

You're picking up Day 5 of Task 12 (Judge Layer Retrofit) in my job-hunt-2026
roadmap. Earlier today (2026-05-28), in a previous Cowork session, the
infrastructure layer of the judge module shipped Days 1-3 in a single sitting
— Pydantic schema, YAML policy loader + the canonical substack_drafter.yaml,
and judge.evaluate() routing through HybridRouter's new judge_layer task
profile. Claude Code verified PASS the same day (79 judge tests, 802 in the
full suite, zero regressions, two small in-scope improvements landed).

Today's scope is Day 5 only: the JSONL ledger writer + boot-time Pushover
credential check + auto-ledger integration with evaluate(). Day 6
(substack-drafter wire-up) is the NEXT session and waits on the B7
synthesizer gate closing (target 2026-06-02).

────────────────────────────────────────────────────────────────────────────
READ THESE FIRST (in order, before touching code)
────────────────────────────────────────────────────────────────────────────

  1. vault/20_projects/prj-job-hunt-2026/onwards-and-upwards-5-4-26/
     job-hunt-2026-roadmap/2026-05-06-unified-roadmap.md
     → search for "### Task 12" — read the Status banner (2026-05-28 entry)
       AND Step 4 spec. Step 4 IS Day 5.

  2. vault/.../2026-05-28-task-12-days-1-3-handoff.md
     → file map of what shipped Days 1-3 + the three interview answers the
       artifact unlocks. Skim the "interview answers" section so Day 5 work
       extends the same narrative line.

  3. vault/.../unified-roadmap-completion-log.md
     → search for "2026-05-28 — Task 12 Days 1-3 SHIPPED + VERIFIED" — the
       canonical ship narrative + the Obsidian-Git scope surprise + Claude
       Code's two small fixes. Two minutes of context here saves 30 minutes
       of confusion later.

  4. agents-sdk/lib/judge/judge.py (lines 1-50 + 250-340 + the evaluate()
     function near line 380) — how the existing module structures fail-open
     today. The ledger writer integrates with evaluate(); you need to know
     where to slot the call.

  5. agents-sdk/lib/pushover.py — the canonical boot-time-credential pattern
     (PushoverConfigurationError + ensure_credentials_or_raise()). Day 5
     reuses this for the boot-time check. DO NOT reinvent.

  6. agents-sdk/lib/filelock.py — the atomic FileLock pattern (POSIX
     advisory lock + context manager + LockTimeout). Day 5 reuses this for
     concurrent-safe JSONL append. DO NOT reinvent.

  7. agents-sdk/lib/judge/schema.py — re-acquaint with JudgeDecision +
     ActionProposal. The ledger writer round-trips both via Pydantic
     model_dump_json().

  8. vault/health/ (just `ls`, don't read files) — observe the existing
     telemetry pattern: synth-manifest-{date}.json, gemini-spend-{month}.json,
     council-spend-*.json. Day 5 lands at vault/health/judge_log/{date}.jsonl
     to fit the same convention.

────────────────────────────────────────────────────────────────────────────
WHAT YOU'RE BUILDING (Day 5 scope, exactly)
────────────────────────────────────────────────────────────────────────────

THREE deliverables. No more, no less.

(1) agents-sdk/lib/judge/ledger.py — JSONL ledger writer.

    Public API (target shape; if you have a better idea, surface it before
    writing the code):

      write_decision(
          decision: JudgeDecision,
          proposal: ActionProposal,
          *,
          agent_name: str,
          ledger_dir: Path | None = None,
      ) -> Path

    Returns the absolute path of the JSONL file the row landed in.
    Default ledger_dir = vault/health/judge_log/ (resolve via config.toml
    or via a module constant that mirrors agents-sdk/config.toml's
    [paths].vault_root). Tests pass a tmp_path.

    Each ledger row is exactly ONE JSON object per line with the schema:
      {
        "evaluated_at":         <ISO 8601 UTC from JudgeDecision>,
        "agent_name":           "<substack_drafter | future agent name>",
        "outcome":              "<ALLOW | BLOCK | REVISE | ESCALATE | JUDGE_UNAVAILABLE>",
        "matched_rule_id":      "<rule id or null>",  // derive from authorization_basis
        "model_used":           "<gemma4:e4b | etc>",
        "latency_ms":           <int>,
        "feedback":             "<text or null>",
        "quarantine_reason":    "<text or null>",
        "proposal":             { ...full ActionProposal model_dump() }
      }

    Atomicity: wrap the append in lib.filelock.FileLock(<dir>/.lock,
    exclusive=True, timeout=5.0). Other agents writing telemetry concurrently
    must not corrupt the file. LockTimeout → raise LedgerWriteError; the
    caller (evaluate or a future wrapper) decides what to do.

    Date bucketing: {YYYY-MM-DD}.jsonl rolls at UTC midnight, NOT local time.
    Use JudgeDecision.evaluated_at (already UTC) to pick the file, not
    datetime.now() — that way a row written just after UTC midnight doesn't
    end up in yesterday's file if the caller's local time is mid-evening.

    Module-level exception classes (mirror pushover.py's shape):
      class LedgerError(Exception): "Base class for any ledger error."
      class LedgerWriteError(LedgerError): "Raised on FileLock timeout
                                            or filesystem I/O failure."

(2) Boot-time check in lib.judge — ensure the ledger directory exists +
    Pushover credentials are present, fail loud if not.

    Add a function ensure_ledger_ready(ledger_dir: Path | None = None) -> None
    to ledger.py. Behavior:

      - mkdir -p the ledger_dir (and parents).
      - Verify the dir is writable (create + delete a .write-test file).
      - Verify pushover credentials exist via lib.pushover.
        ensure_credentials_or_raise() — re-raise PushoverConfigurationError
        directly so the operator sees the same actionable message they'd
        see if they ran the synthesizer.

    Called by the Day 6 wire-up (and by a future Day 5 manual smoke-test
    CLI if you add one). The pattern mirrors the v3.33.0 Pushover boot check
    in vault_synthesizer.py — same goal: fail loud at agent startup, not
    silent later.

(3) Integrate the ledger into judge.evaluate() so every decision lands in
    JSONL automatically — AND fire a Pushover alert on JUDGE_UNAVAILABLE.

    ARCHITECTURAL CHOICE — SURFACE THIS TO SEAN BEFORE CODING:

      Option A: evaluate() itself calls ledger.write_decision() + the
                Pushover alert. Cleaner for callers (one function does it
                all). Worse for testability (eval logic now does I/O).

      Option B: evaluate() stays pure (current behavior). A new wrapper
                judge_action(proposal, policy, *, agent_name, ledger_dir=None)
                calls evaluate() + writes the ledger + fires Pushover on
                JUDGE_UNAVAILABLE. evaluate() remains the pure unit
                tested by Days 1-3 tests. Day 6 substack-drafter calls
                judge_action(), not evaluate().

      My read: Option B is structurally cleaner and matches how the rest
      of the agents-sdk handles I/O (pure logic + a wrapper for effects),
      but Option A is what the Day 5 roadmap spec literally says. ASK SEAN
      WHICH SHAPE HE WANTS BEFORE WRITING THE INTEGRATION. If he says
      "Option B," the 24 existing test_judge_evaluate.py tests stay green
      unchanged.

    Whichever option ships, the contract is:

      - On ALLOW / BLOCK / REVISE / ESCALATE → ledger row only. No Pushover.
      - On JUDGE_UNAVAILABLE → ledger row + Pushover at severity 0
        (low priority "warning"), title "Judge layer unavailable",
        message including model_used + agent_name + a tail of the error
        text from the last failure attempt (truncate to 200 chars).
      - The Pushover alert is best-effort — if Pushover send fails, log
        the failure but do NOT raise. evaluate's / judge_action's caller
        sees the JudgeDecision with outcome=JUDGE_UNAVAILABLE either way.

(4) Tests at agents-sdk/tests/test_judge_ledger.py — pytest, mirror the
    existing test_judge_*.py class-grouped pattern.

    Minimum coverage:
      - TestWriteDecision: writes a JSONL row, file is one valid JSON per
        line, all required keys present, model_dump round-trips cleanly.
      - TestWriteDecisionAppend: writing twice produces 2 lines, in order.
      - TestWriteDecisionBucketsByUtcMidnight: same calendar local-date but
        different UTC-date evaluated_at values land in different files.
      - TestWriteDecisionAtomicity: monkeypatch lib.filelock.FileLock to
        simulate LockTimeout → LedgerWriteError raised.
      - TestEnsureLedgerReady: creates missing dir, raises on read-only
        parent, raises PushoverConfigurationError when creds absent
        (use the env-var override pattern from pushover.py's test, NOT a
        Keychain probe).
      - TestEvaluateIntegration (or TestJudgeActionIntegration depending
        on Option A/B): mock the router + the ledger writer + the Pushover
        client. Verify on JUDGE_UNAVAILABLE: ledger row landed, Pushover
        called once, decision still returned. On ALLOW: ledger row landed,
        Pushover NOT called. On Pushover send failure: log but don't raise,
        decision still returned.

    DO NOT add tests that hit the real vault/health/ directory. ALL tests
    use tmp_path for ledger_dir. The TestRealSubstackDrafterPolicy pattern
    from test_judge_policy.py is the right shape if you need an integration
    test, but ledger writes are too destructive for a real-file test.

────────────────────────────────────────────────────────────────────────────
DESIGN INVARIANTS YOU MUST PRESERVE (council-locked, do not touch)
────────────────────────────────────────────────────────────────────────────

  1. JudgeDecision schema (Days 1-3) is FROZEN. If you find yourself wanting
     to add a field to make the ledger writer's life easier, STOP and ask.
     The dashboard at Task 11 keys on the current field names.

  2. Outcome enum (5 values) is FROZEN. JUDGE_UNAVAILABLE stays the load-
     bearing 5th outcome. Don't merge it into BLOCK or remove it.

  3. evaluate() never raises (Day 3 contract). If Option A is chosen, the
     ledger writer call inside evaluate() must ALSO never raise out — wrap
     in try/except and log. If Option B is chosen, evaluate() stays
     unchanged; the new judge_action() wrapper takes over the never-raises
     contract.

  4. The substack_drafter.yaml policy has exactly 4 rules with 4 canonical
     ids. Day 5 doesn't modify the policy. If something in the ledger row
     schema suggests adding a 5th rule, you're misreading the schema —
     the matched_rule_id field is just a reference to whichever existing
     rule fired, not a new rule.

  5. config.toml's judge_layer = { model = "gemma4:e4b", machine = "mac_mini" }
     in [routing.task_map] stays as-is. The ledger writer doesn't reroute.

  6. Tier-A check (preserved through Days 1-3 — preserve through Day 5):
       Walk-away $100k:            N/A (ledger is infrastructure)
       AI > Tech > Creative PM:    ✓ ledger is the artifact the Task 11
                                     dashboard's "judge-outcome distribution"
                                     panel consumes — direct FDE asset
       Agents draft / Sean sends:  ✓ EXPLICITLY PRESERVED — the ledger
                                     records what the judge said; Sean's
                                     manual gate stays canonical Tier-A
       5:30 PM hard stop:          ✓ Day 5 is a ~5-hour build
       Track-C protected:          ✓ no v0.2 work here

────────────────────────────────────────────────────────────────────────────
PRE-FLIGHT (run BEFORE writing any code)
────────────────────────────────────────────────────────────────────────────

  - cd ~/Code-Brain/code-brain/agents-sdk && source .venv/bin/activate
  - PYTHONPATH=. pytest tests/test_judge_*.py -v
    → 79 must pass. If anything is red, STOP — surface the failure to Sean
      first; do not start Day 5 on top of a broken Day 1-3 baseline.
  - git log --oneline -10
    → confirm the previous session's commits are present (5406a17 + 4dd0743
      with the judge-layer-v0.0.1-infra tag). If absent, ask Sean — the
      previous session may not have been pushed yet.
  - git status
    → confirm working tree is clean. If there are uncommitted Day 1-3
      tweaks, ask Sean before adding Day 5 work on top.

────────────────────────────────────────────────────────────────────────────
VERIFICATION GATE (must pass before commit + handoff)
────────────────────────────────────────────────────────────────────────────

  All 4 must be green:

  1. PYTHONPATH=. pytest tests/test_judge_*.py -v
     → 79 + new (somewhere in the 12-18 range for new ledger tests) all
       pass. Zero red.

  2. PYTHONPATH=. pytest tests/ -v
     → previous baseline (802 / 2 pre-existing reds) holds. Judge-induced
       regressions: zero.

  3. python3 ../scripts/validate.py (from repo root)
     → "Validation PASSED" with warnings ≤ 62 (the 5/28 baseline). Zero
       errors.

  4. Smoke import that exercises the new public surface:

        PYTHONPATH=. python3 -c "
        from lib.judge.ledger import (
            write_decision, ensure_ledger_ready,
            LedgerError, LedgerWriteError,
        )
        # If Option B was chosen, also import judge_action:
        # from lib.judge import judge_action
        print('Day 5 imports green')
        "

────────────────────────────────────────────────────────────────────────────
WHAT TO HAND OFF AT SESSION END
────────────────────────────────────────────────────────────────────────────

Same shape as the 2026-05-28-task-12-days-1-3-handoff.md doc. Write a new
file at vault/.../job-hunt-2026-roadmap/2026-05-28-task-12-day-5-handoff.md
(or whichever date the session actually lands) containing:

  - TL;DR (one paragraph)
  - File map (what shipped, line counts)
  - Verification commands run + outputs
  - Commit message (pre-written for Sean to copy verbatim)
  - Pending items (Days 6-9 status + B7 gate watch)
  - One paragraph each on what interview answer this artifact unlocks
    (the dashboard panel framing — Day 5 turns judge decisions from an
    in-memory return value into an observable telemetry stream).

DO NOT commit. Day 5 is the ledger; Sean reviews + commits. Same convention
as Days 1-3 — leave the commit to Sean so he can eyeball the diff. (The
Day 1-3 session ran into Obsidian-Git auto-committing the source tree
outside vault/; Sean is supposed to narrow the plugin scope BEFORE this
session starts. If you find an unexpected auto-commit on your work,
surface it immediately and stop.)

────────────────────────────────────────────────────────────────────────────
ALSO UPDATE THE ROADMAP CHECKBOXES AT SESSION END
────────────────────────────────────────────────────────────────────────────

vault/.../2026-05-06-unified-roadmap.md Task 12 Step 4 → flip to [x] with a
one-paragraph completion summary in the same shape as Steps 1-3 (artifact
pointers, line counts, test-class breakdown). Add a new entry to
vault/.../unified-roadmap-completion-log.md under ## Amendments Log with
header "### 2026-05-28 (later) — Task 12 Day 5 SHIPPED (ledger writer +
auto-integration)". Match the existing entry conventions.

────────────────────────────────────────────────────────────────────────────
KNOWN-UNKNOWNS WORTH SURFACING

  - Test count nomenclature: my Days 1-3 handoff said "74 tests" but
    pytest reported 79 after collection. If your Day 5 estimate count
    differs from pytest's, report pytest's count.

  - "≤60 warnings" in the handoff doc was imprecise. The real validator
    threshold is whatever the validator's PASSED gate is. Don't try to
    drive warnings below 62; that's the current baseline and none of
    them touch the judge module.

  - "ruff check" was in the Day 1-3 verification but ruff isn't a
    project dependency. Skip it for Day 5 unless Sean explicitly adds
    ruff to pyproject.toml dev deps in the meantime.

  - Day 6 (substack-drafter wire-up) needs the B7 synthesizer gate
    closed (5 consecutive nights of concepts_written > 0). As of
    2026-05-28: 4/5 green, 5/25 broke chain. Next clean window opens
    5/29. Don't start Day 6 work in this session even if Day 5 finishes
    early — let B7 close first.

START NOW with the READ THESE FIRST list. Don't ask me clarifying
questions until you've at least read items 1-4. Most likely questions
are already answered in the handoff doc + completion log.

===
```

---

## Why this prompt is shaped the way it is (for Sean — not for the new Cowork agent)

### It opens with one paragraph of context, not a wall

The new agent has zero memory of the previous Cowork session. The opener names: (a) what Day 5 is, (b) what Days 1-3 already shipped, (c) what's verified, (d) what's still pending. Four facts in three sentences. After that, the agent knows enough to read the doc list with the right framing.

### It points at canonical docs in a specific read order

The READ THESE FIRST list is ordered by leverage. The roadmap status banner gives the highest-density context per word; the handoff doc gives the interview narrative the new work has to extend; the completion log gives the Obsidian-Git + Claude Code surprises that aren't in the roadmap; the source files give the implementation patterns to mirror. If the agent reads in order, it gets context cheaper than from any other order.

### It surfaces the Option A vs Option B architectural choice

The Day 5 roadmap spec was written before the Day 3 `evaluate()` actually shipped, and the spec's literal language ("catch in the wrapper, return `decision.outcome = ALLOW` to caller") doesn't quite match the architecture that's now live. Rather than have the new session guess, the prompt names the two reasonable shapes and tells the agent to ask you which one before writing the integration. Saves a re-do.

### It pre-states the design invariants

Same pattern as the Day 1-3 verification kickoff. The numbered invariants make every council-locked decision a tripwire — the agent has to consciously override a named constraint, which forces a stop-and-ask moment.

### It includes a pre-flight check

Confirms the previous session's commits exist + the working tree is clean before any new code lands. If the previous session's auto-commit + tag aren't there, the agent flags it instead of starting Day 5 on top of a confused git state.

### It explicitly names what NOT to do

- Don't reinvent FileLock / Pushover boot check — both exist
- Don't add fields to JudgeDecision / Outcome — frozen
- Don't write tests against the real vault/health/ — use tmp_path
- Don't start Day 6 even if Day 5 finishes early — B7 isn't closed
- Don't commit — leave that to Sean

These are the five most likely paths a fresh session might wander down. Pre-banning them costs ten words each; un-doing the mistake costs a session.

### It defines a clean handoff shape

The Days 1-3 handoff doc became the canonical reference for the verification session and this kickoff prompt. Day 5's handoff doc will do the same for the Day 6 (substack-drafter) kickoff. The pattern compounds — each day's session produces a doc that bootstraps the next session's prompt cheaply.

---

## Pre-session checklist (for Sean, before pasting the prompt)

Run through these in order. They're small, but each one prevents a class of session-derailment:

1. **Narrow Obsidian-Git scope to `vault/` only.** Open Obsidian → Settings → Obsidian Git → "Files to ignore" (or equivalent for the version you're on). Add: `agents-sdk/`, `the-block/`, `creative-studio/`, `life-systems/`, `claude-mastery/`, `tools/`, `scripts/`, `shared/`, `presets/`, `plugin/`, `docs/`, `evals/`, `export-groups/`. Test by editing a file in `agents-sdk/` and confirming the plugin doesn't pick it up. ~5 minutes.

2. **Push the Day 1-3 commits.** `cd ~/Code-Brain/code-brain && git push --follow-tags origin <branch>`. If you decided to cherry-pick onto a fresh `feature/judge-layer-v0` branch, do that first; otherwise the existing `feature/fleet-memory-phase-1` push carries everything. ~2 minutes.

3. **Confirm B7 nightly synth ran clean overnight.** Tomorrow morning (5/29) check `vault/health/synth-manifest-2026-05-29.json` for `concepts_written > 0`. If green, the 5-night gate window restarts; if red, B7 stays open and Day 6 timeline slides. Doesn't affect Day 5 — but worth knowing before you open the session.

4. **Decide Option A vs Option B in advance** (optional). The prompt asks the new agent to surface this choice. If you already have a preference (my read: Option B is structurally cleaner and preserves the existing 24 evaluate tests unchanged), you can tell the agent up front by appending one line to the prompt: *"Option B (judge_action wrapper) — keep evaluate() pure."* If you're indifferent, let the agent surface and pick.

5. **Open a fresh Cowork session.** Paste everything between the `===` lines into the new session's first message.

---

## Why Day 5 is the right next step (and not something else)

Day 5 is the only Day 4-9 item that doesn't depend on B7 closing. Day 6 (substack-drafter wire-up) is the natural next step but waits on the synth-manifest gate. Day 7 (`--demo-injection` flag) waits on Day 6 to be wired. Days 8-9 (4Q EXPLANATION.md + Loom + LinkedIn) wait on the demo being runnable.

So Day 5 is the only path that keeps the artifact moving forward this week. It also unblocks two downstream pieces:

- **The Task 11 dashboard's judge-outcome distribution + judge-availability panels** start being usable as soon as JSONL rows start landing. Even without the substack-drafter wire-up, you could write a manual test that calls `judge_action()` (or `evaluate()` + `write_decision()` if Option A) and produces a row the dashboard can plot. That's a Loom-able milestone.

- **The Day 8 4Q EXPLANATION.md "What is this?" answer gets richer.** With the ledger writer shipped, you can say "every decision lands in JSONL within 5ms" — that's a sentence other PMs can't say.

So Day 5 is both the cheapest item to ship next AND the one that unlocks the most downstream story. That's the move.

---

## What the next-after-Day-5 session looks like (preview for sequencing)

Once Day 5 ships + B7 closes, Day 6 substack-drafter wire-up is the next Cowork session. The kickoff prompt for THAT session writes itself: read the Day 5 handoff + the Day 5 ledger module + `agents-sdk/agents/substack_drafter.py`'s `_route()` seam + the 4 dispatch paths spec from Task 12 Step 5 in the roadmap. Then 4-6 hours of integration work + 4 integration tests covering ALLOW / REVISE-retry / BLOCK / ESCALATE.

If you want me to draft that Day 6 kickoff prompt in advance (so it's ready to paste the moment B7 closes), say so after the Day 5 session lands and I'll write it.
