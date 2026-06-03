---
type: chain-verification
date: 2026-06-02
purpose: "Phase 4 end-to-end proof of the four-skill chain on a real solved problem (the vault-critic Anti-Gravity nightly failure). storytelling-architecture -> substack-value-engine -> writing-voice-modes -> writing-humanity-pass."
source_facts: "CHANGELOG.md [Unreleased] > Fixed: vault_critic Anti-Gravity CLI nightly 100% failure"
---

# THE POST (final, post-chain)

## The night watchman who wasn't there

For six nights, half of my nightly critic was dead, and every morning I glanced at it and decided everything was fine.

Here's the setup. At 3:30am a little agent I built wakes up and runs two other AIs against my notes, Codex and Anti-Gravity, two independent critics from two different companies, picked specifically so they'll disagree with each other and catch what one alone would miss. Variance is the whole point. Two sets of eyes that don't share a blind spot. I pay for both through subscriptions I already had, so it costs me nothing and makes me feel like a man who has his life together.

Then I actually opened the manifest. Anti-Gravity: five of five failed. Zero tokens. And the date on the rot went back a week.

The part that was supposed to catch this is the part that hid it. When one critic fails and the other survives, the run logs itself as "partial." Partial is yellow. Partial is fine. Partial is the status I built so a single bad night wouldn't nuke the whole job, and partial is exactly why I scrolled past six mornings of a dead robot without blinking. The resilience was the camouflage.

I assumed rate limits. A bad night, a tired API, the usual weather. But when I went digging, the thing that stopped me cold was the absence: there were no session files at all. Not failed sessions. None. Anti-Gravity wasn't dying in the middle of the critique. It was never waking up.

What was actually happening is dumber than a rate limit. The Gemini CLI, before it does anything, reads a settings file and dutifully boots up six MCP servers it thinks it might need. One of them wants to talk to a Chrome browser on a specific port. At 3:30am, in an empty house, Chrome is closed and the port is dark, so the CLI stands there politely waiting for a browser that is never coming, waits past its 120-second timeout, and dies on the doorstep having never said a word. Run it at noon with Chrome open and it takes fifteen seconds and you'd never know. Run it alone at night and it hangs until the watchdog shoots it.

The fix is one flag. `--allowed-mcp-server-names __none__`. The critic only ever needed to read text and hand me an opinion. It never needed a browser, or Zapier, or any of the other six. So I told it to load none of them. It now finishes in 6.4 seconds on twelve thousand tokens, wide awake.

But the flag is the small fix. The real bug wasn't the hang. The real bug was that I couldn't see the hang, because I'd taught the system to report a number (five failures) instead of a reason (none of them ever started). So the second change matters more than the first: every failure now writes down what actually killed it, not just that it died. A tolerated state with no diagnostic isn't resilience. It's a blind spot you put on a schedule.

If you run a fleet of your own, this is the part worth stealing. Go find your "partial is fine" state, the yellow you've quietly trained yourself to walk past, and ask what it's allowed to hide. Then make it say why, out loud, every time. (I currently have an unreasonable amount of time for 3am archaeology.)

The watchman is awake again. Both of them, now. I still don't fully trust the one that slept through a week, which is, I think, the correct amount to trust a watchman.

---

# CHAIN TRACE (verification record)

## Stage 1: storytelling-architecture (beat map, Problem-Struggle-Fix)

1. COLD OPEN [L1 opens]: half the nightly critic dead for six nights, greeted like it was fine. Q: how do you not notice half a system dying for a week?
2. THEREFORE (stakes): the critic exists to catch MY blind spots via two independent eyes; one eye was blind, so the variance it was built for was gone.
3. BUT (the trap): no alert, because "partial" is tolerated. The resilience state became the camouflage. [L1 open: why partial hid it]
4. THEREFORE (false lead -> diagnosis): assumed rate limits; but zero session files ever existed. Not failing mid-critique. Never starting.
5. THE TURN [L1 closes]: Gemini CLI boots 6 MCP servers on every invocation; chrome-devtools waits for a closed Chrome at 3:30am; hangs past the 120s timeout. Never thinks.
6. PAYOFF: one flag, `--allowed-mcp-server-names __none__`. 6.4s, 12K tokens, green.
7. PIVOT/SECOND PAYOFF: the flag fixed the symptom; the real bug was invisibility. Persist the error (reason), not the count. "A tolerated state with no diagnostic is a blind spot on a schedule."
8. SO-CAN-YOU: find your own "partial is fine" state; make it say why. Sideways job-hunt clause lands once, mid-late.

Gates: but/therefore holds on every seam; cold open raises one question; L1 opens beat 1, closes beat 5; rescue withheld (fix not revealed early); each section ends forward-pulling; specificity high; template bent (false-lead beat 4 breaks the canonical shape) so it is not nameable. PASS.

## Stage 2: substack-value-engine (gate verdict)

- **Itch** (real, first-person, checkable): half my nightly dual-CLI critic silently failed for a week; I missed it because "partial" is tolerated. PASS.
- **Solution** (with artifact): root-caused to gemini-CLI MCP startup hanging past the 120s timeout; fixed with `--allowed-mcp-server-names __none__` (verified 6.4s / 12K tokens); plus persist per-CLI error reason to the manifest. Artifact = the flag + the numbers. PASS.
- **Transfer** (one concrete capability): after reading, the reader can spot a tolerated "partial/degraded" state hiding a real failure in their own fleet, and add the one diagnostic (persist the reason, not the count) that surfaces it. PASS.
- **VERDICT: PASS.** Seam marked at beat 7 (pivot line names the lesson; the how-to fulfills the "how did I not notice" hook, not an appendix). Rule of One holds (one idea: a tolerated degraded state hides real failures). Over-deliver: exact flag + the persist-the-reason pattern, usable in 10 min. Hiring signal shown (self-post-mortem + numbers), ask sideways (one mid-body clause, ends on the lesson).

## Stage 3: writing-voice-modes (Sean Mode ~85%)

Cold open; domestic defamiliarizer ("dies on the doorstep having never said a word"); self-implication ("I scrolled past six mornings"); sensory-before-numbers (the absence, then 120s, then 6.4s/12K); hard-cut deflation ("a man who has his life together"; closer); rule-of-three + pivot ("a bad night, a tired API, the usual weather"); callback closer (the watchman, transformed); sideways job-hunt fact as one parenthetical, never the closer. Beats not reordered.

## Stage 4: writing-humanity-pass

Em/en dash scan on THE POST: ZERO (verified by grep). No generic AI tells ("Here's the setup" is specific connective, not slop "Here's the thing"); varied the two "Here's" openers (second became "What was actually happening is dumber than a rate limit"). Rule-of-three preserved as a signature move. Paragraph count preserved. Meaning intact.

## Stage 5: independent cold critique (llm-council variance stand-in)

A blind senior-engineer/AI-PM critic read the post with no prior context. Verdict: bookmark = YES (the "partial/yellow tolerated state camouflaging a total subsystem death" is a transferable, non-obvious trap); value = clear (audit your own "partial is fine" states; log the reason not the count); credibility = competent and senior (peak line: "report a number instead of a reason"). Two flags, both fixed:

1. The job-hunt parenthetical read as "an unforced flare... fishing for sympathy" (it named the layoff + "learn this one properly"). Fixed: dried to "(I currently have an unreasonable amount of time for 3am archaeology.)", a fact in passing, no sympathy, recruiter still infers availability. This is exactly the value-engine sideways-ask rule self-correcting.
2. The opening "walked past the body and said good morning" corpse metaphor was "overworked." Fixed: "every morning I glanced at it and decided everything was fine", which drops the strained image and seeds the "partial is fine" beat better.

Production note: the live `llm-council` variance profile (Sonnet + GPT-5.4-mini + DeepSeek + Mistral, ~$0.14/run) is the real blind-spot pass; this single-critic subagent is the credential-free stand-in.

## Eval scorecard (against evals.yaml across both skills)

| Check | Result |
|---|---|
| Addictive open (cold open + closeable gap) | PASS: opens on the dead half of the critic, one concrete question |
| Value Gate (Itch/Solution/Transfer all concrete) | PASS |
| Seam marked, value fulfills the hook (not appendix) | PASS: pivot at beat 7 answers "how did I not notice" |
| Voice intact under structure (not flattened, seams invisible) | PASS: Sean signature moves present; template bent |
| Funny-not-cheesy (specific, self-implicating, punch-word-last, no signposting) | PASS: deflation closers, no winking |
| Recruiter signal without desperation (artifact + self-post-mortem; ask sideways) | PASS after fix: dried the parenthetical; ends on the lesson |
| Zero em dashes (THE POST) | PASS |
| Independent bookmark test (stranger stuck on same problem) | PASS: would bookmark + share |
