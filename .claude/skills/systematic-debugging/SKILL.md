---
name: systematic-debugging
description: Use when encountering bugs, test failures, or unexpected behavior, before proposing any fix — code-brain's canonical four-phase root-cause discipline. Inside this repo a bare "systematic-debugging" reference means THIS skill; superpowers:systematic-debugging is the generic edition of the same method (use it when explicitly namespaced, or outside code-brain). This edition adds hard phase-exit gates (a written Evidence Block that every later phase must cite), a Phase-1 sufficiency checklist, fleet first-checks for agents-sdk, launchd, hook, and local-model bugs, find-polluter.sh for test pollution, and this repo's verify chain (verification-loops, verification-before-completion). Stands alone when exported without the plugin.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

This edition backs the principle with structure: each phase has an **exit gate** that produces something citable, because prose discipline collapses exactly when it matters most — mid-incident, under time pressure. A gate you can't show is a gate you haven't passed.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## Which systematic-debugging? (vs. `superpowers:systematic-debugging`)

Two live skills carry this name. The division of labor is deliberate — complementary, not duplicative:

| Situation | Use |
|-----------|-----|
| Working inside code-brain — any bug, fleet or generic | **This skill.** It is the canonical debugging discipline for this repo; its gates and fleet first-checks govern all repo fix work. |
| A doc or prompt explicitly namespaces `superpowers:systematic-debugging` | The plugin — an explicit namespace always wins. |
| Another project that received this skill via `install.sh` export, plugin absent | This skill — the full method below stands alone. |

A bare `systematic-debugging` reference anywhere in this repo (`zoom-out-and-think`, agents-sdk continuation docs) means **this skill**.

Both share the same four-phase spine and Iron Law. What this edition adds that the plugin does not have: hard phase-exit gates (the Evidence Block), a Phase-1 sufficiency checklist, code-brain Fleet First-Checks, `find-polluter.sh`, and a **deliberately chosen** verification chain — Phase 4 here hands off to this repo's `verification-loops` and `verification-before-completion` (which ship in the same export group), where the plugin hands off to `superpowers:test-driven-development`. That difference is a choice, not fork drift. For the plugin's extra generic prose (human-partner signals, impact numbers), read it there — do not copy it here.

Adjacent routing: a **first-time** bug belongs here; a bug that **keeps coming back after 2+ patches** belongs in `zoom-out-and-think` (see Phase 4, step 5).

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

## The Four Phases

You MUST complete each phase before proceeding to the next. Each phase ends at a gate.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

0. **In code-brain, scan Fleet First-Checks below** — a known failure surface can collapse this phase from hours to minutes. The table accelerates evidence-gathering; it never replaces it.

1. **Read Error Messages Carefully**
   - Don't skip past errors or warnings
   - Read stack traces completely
   - Note line numbers, file paths, error codes

2. **Reproduce Consistently**
   - Can you trigger it reliably? What are the exact steps?
   - If not reproducible, gather more data — don't guess
   - Test passes alone but fails in the suite (or the reverse), or stray files/state appear? That's test pollution — bisect with `find-polluter.sh` (this directory)

3. **Check Recent Changes**
   - What changed that could cause this?
   - Git diff, recent commits
   - New dependencies, config changes

4. **Gather Evidence in Multi-Component Systems**

   **WHEN system has multiple components (CI -> build -> signing, API -> service -> database):**

   Add diagnostic instrumentation at each component boundary BEFORE proposing fixes:
   - Log what data enters and exits each component
   - Verify environment/config propagation
   - Run once to gather evidence showing WHERE it breaks
   - THEN investigate that specific component

5. **Trace Data Flow**

   See `root-cause-tracing.md` in this directory for the complete backward tracing technique.

   Quick version:
   - Where does bad value originate?
   - What called this with bad value?
   - Keep tracing up until you find the source
   - Fix at source, not at symptom

#### Phase 1 Exit Gate — the Evidence Block

<HARD-GATE>
Do not enter Phase 2, and do not utter a fix, until you have WRITTEN the
Evidence Block below with every field filled honestly. "Origin: unknown" or
"Origin: probably X" is not a filled field — it is Phase 1 telling you it
isn't done. This applies even when the bug looks trivial and even when the
fix seems obvious; obvious fixes to untraced origins are how symptom patches
are born.
</HARD-GATE>

```
EVIDENCE
- Symptom: <exact error / wrong output, verbatim — not "it's broken">
- Repro:   <command or steps, and whether it reproduces reliably;
            if not reproducible, what evidence you gathered instead>
- Origin:  <file:line or component where the bad value/behavior is BORN,
            not where it surfaced>
- Owner:   <the component that owns that origin>
- Changed: <recent commit / config / dependency that plausibly introduced
            it, or "none found">
```

Rules that make the gate real:

- Write it down — in the conversation is fine; for fleet incidents, paste it into the daily note or the ticket so it survives the session.
- The block is the Phase-1 **sufficiency checklist**: all five fields filled honestly = sufficient evidence; any field you can't fill = you are still in Phase 1.
- **Phase 3's hypothesis must name this block's Origin. Phase 4's fix must open by citing it.** A fix that can't say which traced origin it addresses is a symptom patch by definition.
- Under time pressure the block is five lines. If there's no time for five lines, there is definitely no time for a wrong fix and the new bug it ships.

Honesty about mechanism: a skill can steer, not enforce. The block's job is to make a skipped Phase 1 **visible in the transcript** — an absent or hand-waved Evidence Block is auditable proof the process was skipped.

### Phase 2: Pattern Analysis

1. **Find Working Examples** — Locate similar working code in the same codebase
2. **Compare Against References** — Read reference implementation COMPLETELY, don't skim
3. **Identify Differences** — List every difference between working and broken, however small
4. **Understand Dependencies** — What settings, config, environment does this need?

**Exit gate:** you can state the concrete difference-list between working and broken.

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** — in the shape: **"Origin `<from the Evidence Block>` produces Symptom `<from the block>` because `<mechanism>`."** A hypothesis that doesn't name the traced origin is a guess wearing a lab coat.
2. **Test Minimally** — Make the SMALLEST possible change; one variable at a time
3. **Verify Before Continuing** — Didn't work? Form NEW hypothesis. DON'T add more fixes on top.
4. **When You Don't Know** — say "I don't understand X" and go research; pretending stalls at the gates anyway, just later and more expensively.

**Exit gate:** hypothesis confirmed by the minimal test, or explicitly replaced — never quietly stacked.

### Phase 4: Implementation

1. **Create Failing Test Case** — Reproduce the bug as a failing test before fixing. Use the `verification-loops` skill — this repo's TDD/verify loop, the deliberate chain for this edition (see "Which systematic-debugging?").
2. **Implement Single Fix** — The fix's first line of explanation cites the gate: **"Fixes Origin: `<Origin from the Evidence Block>`."** ONE change at a time. No "while I'm here" improvements.
3. **Verify Fix** — Failing test now passes? No other tests broken? Symptom from the block actually gone? Before claiming done, run `verification-before-completion` — evidence before assertions.
4. **If Fix Doesn't Work** — Count attempts:
   - If < 3: Return to Phase 1 and **revise the Evidence Block** with what the failed fix taught you (usually that Origin was wrong). Don't patch on top.
   - **If >= 3: STOP and question the architecture**
5. **If 3+ Fixes Failed: Question Architecture**
   - Each fix reveals new coupling/problem in a different place
   - Fixes require "massive refactoring" to implement
   - Each fix creates new symptoms elsewhere
   - Three failed fixes means this is no longer a first-time bug — it is the entrenched, recurring case. In code-brain, escalate to `zoom-out-and-think` (system-level root cause + intent-carrying spec); where that skill isn't installed, question the architecture directly.
   - **Discuss with your human partner before attempting any Fix #4**

### When Investigation Reveals No Single Code Root Cause

Sometimes a complete investigation converges on "truly environmental, timing-dependent, or external" — in this fleet, the canonical example is an overnight agent step failing because the MBP was asleep: a reachability gap, not a code defect. Then:

1. The Evidence Block documents what you ruled out (that IS the completed investigation — Origin names the environmental condition)
2. Implement appropriate handling: retry, timeout, skip-and-continue, clear error message
3. Add monitoring/logging so the next occurrence carries its own evidence

**But:** ~95% of "no root cause" conclusions are incomplete investigation. Reread the block before accepting one.

## Fleet First-Checks (Phase-1 accelerators for code-brain)

The fastest honest Phase 1 is recognizing a known failure surface. Check the matching row FIRST — then verify with your own eyes and fill the Evidence Block from what you observe, not from this table. Outside code-brain, skip this section.

| Symptom | First check | Canonical reference |
|---------|-------------|---------------------|
| launchd agent fails; `CLIConnectionError`; `claude` CLI not found | plist `EnvironmentVariables` must set `PATH` (incl. `/opt/homebrew/bin`, `~/.local/bin`) | `agents-sdk/BUGFIX-2026-04-07-launchd-path.md` |
| Headless agent 401s while interactive sessions work | Long-lived `claude setup-token` in Keychain, injected by `resolve_oauth_token()` — the 2026-06-20 morning 401's root cause | `agents-sdk/lib/auth.py` |
| Overnight MBP-model step fails intermittently (synthesizer, lint Tier 2, flush >=100-msg) | Was the MBP awake? Reachability, not code — WOL retired; agents skip-and-continue by design | CLAUDE.md agents table |
| `RouteUnavailable` from `tier_c_batch_summarize` off-hours | Pattern-E gate behaving as designed (`fallback = "none"` — never the paid API); Alienware reachable ~7am–5pm manual-wake only | CLAUDE.md Tier C row |
| A hook "doesn't block" the operation | Hook must exit **2** to deny; exit 1 is logged-but-allowed | CLAUDE.md hook exit codes |
| Test pollution (passes alone / fails in suite; stray files or state) | Bisect: `./find-polluter.sh <artifact> <test-glob>` | this directory |

Where fleet evidence lives: launchd stdout/stderr at the per-plist `StandardOutPath` (e.g. `/var/log/<agent>.log`); nightly manifests and lint reports in `vault/health/`; flush and overnight digests in the daily note.

## Red Flags — STOP and Follow Process

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "It's probably X, let me fix that"
- "Here are the main problems:" — a fix list with no investigation behind it
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)
- **Writing Phase 4 code with no Evidence Block in the transcript**
- **A hypothesis or fix that doesn't name an Origin**

**ALL of these mean: STOP. Return to Phase 1.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first" | First fix sets the pattern. Do it right from the start. |
| "Multiple fixes saves time" | Can't isolate what worked. Causes new bugs. |
| "I see the problem" | Seeing symptoms != understanding root cause. |
| "The Evidence Block is overhead" | It is five lines. A wrong fix costs hours and ships a new bug. |
| "I'll write the test after the fix" | Untested fixes don't stick. The failing test is the proof you fixed the right thing. |

## Quick Reference

| Phase | Key Activities | Exit Gate |
|-------|---------------|-----------|
| **1. Root Cause** | Read errors, reproduce, check changes, instrument boundaries, trace to origin | Evidence Block — all five fields filled honestly |
| **2. Pattern** | Find working examples, compare completely | Difference-list between working and broken |
| **3. Hypothesis** | One theory, smallest test | Hypothesis cites the block's Origin; confirmed or replaced |
| **4. Implementation** | Failing test, single fix, verify | Fix cites its Origin; tests green; `verification-before-completion` run |

## Supporting Techniques

Available in this directory:
- **`root-cause-tracing.md`** — Trace bugs backward through call stack to find original trigger
- **`defense-in-depth.md`** — Add validation at multiple layers after finding root cause
- **`condition-based-waiting.md`** — Replace arbitrary timeouts with condition polling
- **`find-polluter.sh`** — Bisection script to find which test creates unwanted state. Reach for it when a test is order-dependent, only fails in the full suite, or leaves artifacts behind. Note: it drives `npm test` — adapt the runner line for pytest or other frameworks.

## Success Criteria

- Evidence Block written — all five fields — before any fix was proposed
- Fix explicitly cites the Origin it addresses; root cause, not symptom
- Failing test existed first and now passes; no other tests broken
- `verification-before-completion` run before claiming success
- 3+ failed fixes escalated to `zoom-out-and-think` / architecture discussion, never a silent Fix #4
