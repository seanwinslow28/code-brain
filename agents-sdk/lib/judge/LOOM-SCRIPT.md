---
type: loom-script
artifact: judge-layer
created: 2026-05-31
target_length: 90s
ai-context: "90-second Loom script for the judge-layer demo (Task 12 Step 8). Two takes: the ESCALATE take (deterministic, primary) and the REVISE→retry→ALLOW take (richer arc, depends on the local model self-correcting). Lead with ESCALATE for a reliable single-pass recording."
---

# Judge Layer — 90-Second Loom Script

**Goal of the take:** show that the Substack-Drafter isn't just an agent that writes — it's an actor inside a control architecture that intercepts, judges, and quarantines before anything reaches me. Close on the boundary: agents draft, I send.

**Recording setup:** terminal + the policy YAML open in a split. `[substack_drafter].enabled = true` for the take (flip back after). Font large enough to read on LinkedIn mobile.

---

## Primary take — ESCALATE (deterministic, single pass)

**[0:00–0:12] — The contract, not the code.**
> "Before I show the agent, here's the thing a recruiter can actually read — the policy. Four rules in YAML. No fabricated quotes from named people, citations required on anything from my old employer, voice has to match the assigned mode, and the agent can never publish itself. That last one is a hard boundary."

*On screen: `policies/substack_drafter.yaml` — scroll the four rule IDs.*

**[0:12–0:30] — Rig the draft.**
> "I'm going to make the agent misbehave on purpose. This flag injects a synthetic instruction that tells the drafter to fabricate a quote from a named former colleague — no citation. The judge's response is real; only the prompt is rigged."

*On screen: type `python3 agents/substack_drafter.py --demo-injection` and hit enter.*

**[0:30–0:55] — The interception.**
> "Here's the ActionProposal — eight typed fields plus the draft body itself, which is the part that lets the rules actually read what's being proposed. The judge runs locally, on a four-billion-parameter model on a Mac Mini, zero cost per decision. And it comes back ESCALATE — rule A, unverifiable claim attributed to a named person."

*On screen: the printed `ActionProposal` + the `ESCALATE` line.*

**[0:55–1:18] — The receipt.**
> "The draft didn't go to my review queue. It went to a quarantine folder. And every decision writes a row to an append-only ledger — outcome, which model judged it, latency, and the text that produced the verdict. That's the audit trail the fleet dashboard reads."

*On screen: `ls` the quarantine folder, then `tail -1 vault/health/judge_log/$(date -u +%F).jsonl | python3 -m json.tool`.*

**[1:18–1:30] — The boundary.**
> "If the judge model is down, it falls open to me — my manual review is still the real control. The judge is defense-in-depth. Agents draft. I send. Every word."

*On screen: cut to the closing frame.*

---

## Alternate take — REVISE → retry → ALLOW (richer arc, if the local model cooperates)

Swap the command for `--demo-injection=revise_citation`. The narration for 0:30–1:18 becomes:

> "The judge comes back REVISE — rule B, a claim about my old employer with no citation. Watch what happens: the feedback goes back into the agent's prompt, it retries with the citation marker added, and the second pass is ALLOWed. The control didn't just block — it improved the output and preserved the cadence."

This take is stronger if it lands, but the retry depends on the local model self-correcting, so record the ESCALATE take first as the safe one.

---

## Don't-say list

- No "AI-powered," no "revolutionary," no "guardrails" (overused). Say "control architecture" — it's the JD's language.
- Don't oversell the model. It's a 4B local model; the point is the *architecture*, not the model.
- Don't claim it's wrapping all eight agents. It wraps one, on purpose. The schema makes the next wrap additive — say that if asked, don't claim it's done.
