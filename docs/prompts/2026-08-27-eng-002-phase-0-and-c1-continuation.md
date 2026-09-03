# Continuation — eng-002: start Phase 0, close RT-G2R6-C1, and decide whether 1A should be observational

*Written 2026-08-27 at the end of a long session. Paste into a fresh session.*

---

Invoke `/systemcraft`. This continues **eng-002-fleet-to-workforce-redesign**. Read `systemcraft/ledger/engagements/eng-002-fleet-to-workforce-redesign/RESUME.md` first — it is the state handoff — then `systemcraft/ledger/index.md` and the entries you need.

**Where it stands:** Gate 1 (PRD sign-off) closed **PASS WITH ACCEPTANCES** after six rounds; I signed all four acceptances. Gate 2 (pre-launch) has run **six rounds** and stands at **FAIL — 1 CRITICAL / 0 MATERIAL / 1 NOTE**. The record is **143 ledger entries, 18 artifacts, 6 runnable proofs**, nothing committed, private layer intact.

**I am changing posture, and this prompt is that change.** Six gate rounds have produced real findings and one thing they have not produced is anything built. Meanwhile eng-001's four P0 fixes have sat unshipped since that engagement closed — which is the studio's own d03 and d40 pointed back at itself. **The gate blocks 1A launch. It does not block building. I have been treating it as a blocker for all work and I am stopping that.**

Three things, and I want **1 and 2 running in parallel, not in sequence**.

## 1 — Phase 0. Start it.

Nothing in Phase 0 depends on the open CRITICAL. Scope it, sequence it, tell me what you need from me, and let's move:

- The **four eng-001 P0 fixes** — Pushover alert delivery (d40), the crying-wolf one-liner (d21), the index-truncation decision (deferred at eng-002.d05 — honour that deferral or re-justify it), the daily-driver note assertion.
- **B8 deploy-path reconciliation.** Production is on side branch `vault/process-inbox-2026-07-14`, ~26 commits ahead / 94 behind `origin/main`, one stash, and on 2026-08-26 its vault auto-commit swept my three hand-edited code files — including the d10 mDNS fix — into mixed commit `7d7c9db` titled "vault: auto-commit". ADR-03 designed the fix: one clone, three-class file classification, forward-only flow, revert-based rollback, a deploy→verify→rollback drill, a daily drift tripwire. **Nothing touches that machine without my explicit approval, per change.**
- **B11 Tailscale** — my install, on the Mini and my iPhone. Tell me when.
- **The critic schedule** — disabled at Phase 0 per d15, manual mode preserved; the installer converges to config-declared state per ADR-04.

Phase 0's exit evidence is already specified across the B-checklist. **Use it; don't redesign it.**

## 2 — RT-G2R6-C1, one bounded pass

**The defect:** the manual 1A bridge has no single lawful population. My producer content-scores eight rows; Claude verifies locations and six pass; six delivered, five acknowledged, four disposed. Three current artifacts support three different values of `n`:

```
eligible-only reading      n = 6  ->  PASS
every-candidate reading    n = 8  ->  DELIVERY-FAIL
literal frozen-rule read   n = 0  ->  INCONCLUSIVE
```

Same event history, opposite launch decisions. `v5-projection-replay.py` cannot decide it because `project()` receives `n_items` from its caller — the actor fixture tests what happens *after* `n` is supplied, not how manual 1A constructs it.

**Cause, on the record:** the frozen rule was written for the steady state where ADR-11 exists and `geo_status` is a scoring-time field. The steel-man bridge I ratified (d131) removes ADR-11 from 1A, so "qualifying" has no referent in the phase we'd run first. My ratification created this; don't treat it as a seat's error.

**The gate's two options — pick one, implement one, record the loser:** (a) every existing-schema content-scored candidate enters `n`, with a missing or non-eligible B16 record explicitly zeroing the item; or (b) a separate immutable manual-condition qualification event created from a complete eligible B16 record, with an exact cutoff, order and ID join, stating plainly that 1A's `n` begins there. **Bind the choice into the executable projection and replay the eight-row trace.** Full detail in `artifacts/red-team-gate2-round6-findings.md`.

## 3 — Then put this question to me: should 1A be observational?

Before another verdict-rule repair, I want the option on the table that was never considered.

The population rule has now forked **five times** — clock, population, cardinality, vocabulary, phase order. Each fix was correct and each created the next. That suggests the verdict apparatus is carrying more weight than a two-week, eight-item test can bear: we have built a machine precise enough to need five rounds of definition, to grade a sample its own PRD says can only establish "the funnel is usable."

**The alternative: run 1A observationally.** Collect the events, retain everything, and read the data afterward — rather than pre-committing to a verdict function that keeps forking. Design it honestly, price it, name what it costs (repeatability, a crisp 1B trigger) and what it buys, and **give me a recommendation with the loser on record.** If the answer is that the verdict rule is worth keeping, say that plainly — I'd rather hear a defended "no" than a polite pivot.

## Binding constraints

- **Model routing:** heavy delegated work goes to **Codex `gpt-5.6-sol` at High**. **Do not escalate a seat to Fable without naming the trigger and asking me first** — the ladder's per-invocation rule has no aggregate budget and it exhausted my quota mid-engagement.
- **Codex launches need `< /dev/null`** or they hang silently while looking busy. **Never run two instances of one seat concurrently** — they share the ledger index.
- **Verify, don't assert.** Run all six proofs and report actual output: `v3-enumeration.py` (5,400 / 0 ambiguous / 399 / 236) · `v5-projection-replay.py` (**22**) · `g2c1-gate-replay.py` (24) · `tco-line-sum.py` (8) · `check-version-drift.py` (**exit 0**, `--selftest` **23**) · `geo-label-replay.py` (35). Leave no `__pycache__`.
- **Nothing committed** without draft-then-ratify; push is my call. `git status --porcelain systemcraft/` must be empty at every stop. Private layer never reaches git.
- **Every live count carries its exact SQL, database path and capture instant** — that standard exists because the coordinator broke it twice, both times a loose query reported as a precise one. Corrected forms only: **105** roll-ups (not 107) · **54** strong fits / 16 at score 5 / 503 scored / 16,460 total (53 = the dated 2026-08-24 baseline) · exact `Remote, US` = **60** · exact `100% Remote (US)` = **2** · the 443 "US-remote-pattern" figure is **withdrawn** · the notification era = **31 role IDs in ~20 API-accepted batched messages, receipt and attention unmeasured**.
- **Ratified, do not reopen:** the disposed-decision unit of value · the job-hunt beachhead · two-week clean-room 1A · the frozen risk dial (never apply, email or contact anyone) · rule v5 · the nine claims · the sourcing sentinel · the no-quota principle · the eight April-2026-disabled agents · d02 (stands, precision premise withdrawn) · d131 (the steel-man bridge) · my rulings: four Gate-1 acceptances · Tailscale/B11 · escalation one push that week and none during 1A · **3 interrupts/day** · **2 applications/week, calibration only, never a target** · geo **remote (preferred) or Boston, MA**.
- I'm a PM, not a dev — plain language, one question at a time, a recommendation with every question.

## What done looks like for this session

Phase 0 sequenced and started, with the first thing I need to do named. C1 closed by one bounded pass with the eight-row replay green. The observational-1A question put to me with a recommendation. Ledger accreting; RESUME.md reconciled. **No more gate rounds until 1 and 2 are done** — the re-gate comes after, and it should be scoped to what changed.

## One live thing, unrelated to the design

There is an **OpenAI Product Manager, Learning** role (score 5, scored 2026-08-26) and two **Fireworks** score-5 roles sitting at `status = new` in the feed. All three are San Francisco or multi-city hybrid and **fail my geo constraint** — that is what surfaced CF-01. If anything genuinely eligible is sitting untriaged, tell me; otherwise leave them.
