---
artifact: vault-synthesizer-evals
created: 2026-05-12
ai-context: "Comprehension artifact for the vault-synthesizer eval suite. 4-question template per Nate B Jones / ADR convention."
---

# EXPLANATION.md

A 4Q comprehension artifact (Nate B. Jones) for the vault-synthesizer eval suite. The explanation that travels with the work: what this is, why this approach, what would break, what I learned.

---

## What is this?

A binary pass/fail eval suite for a local Qwen3-14B vault synthesizer agent: **14 wired cases plus 11 deferred**, built as 10 and grown on 2026-05-27. Every case came out of open-coding 17 days of production logs (2026-04-24 to 2026-05-10), not out of imagining what might go wrong. Six failure modes surfaced in that reading, and 25 cases were written from them.

It exists for one class of failure that monitoring missed completely. The agent reported success every night for nine nights while writing nothing. The only thing being checked was whether the job exited, and it did that faithfully.

## Why this approach?

**Pytest and YAML instead of an eval platform.** Braintrust and Langfuse both do more than this needs, and at 25 cases the platform is the overhead: a hosted service to keep alive, for a suite one person runs by hand before shipping. Files in a repo have no runtime to break and no account to expire.

**Rule-based and rubric graders before an LLM judge.** Hamel Husain's cost argument, taken whole. A judge model costs money per run and needs its own calibration before you can trust a word it says, and most of what this suite checks can be stated as a rule instead. Anything that can be a rule is a rule.

**Binary pass/fail, never a Likert score.** Husain and Shankar are blunt about this and I did not argue: a 1-to-5 scale wrecks inter-rater reliability, and a case scoring 3 tells you nothing you can act on. A case either caught the regression or it did not.

**Cases from real logs, not synthetic generation.** The failure modes worth testing were already in the logs, described in the agent's own output. Generating plausible cases would have produced the ones I could imagine, and the whole lesson of this suite is that the expensive failure was the one nobody would draft on purpose.

## What would break?

These are live, knowingly accepted risks, not fixed defects.

**1. The suite is smaller than the floor its own sources recommend.** Anthropic's guidance is that 20 to 50 tasks drawn from real failures is a good start, and their multi-agent eval began at roughly 20 queries. This one wires 14. The other 11 are written and deferred behind named blockers, not aspirations, which is the honest version of the gap but not a closure of it. I accept it because 14 cases grounded in real logs beat 40 invented ones, and because the deferred blockers are real work rather than an excuse. It is the same order of magnitude as the recommendation, not the same sport.

**2. It is a manual pre-ship gate, not a scheduled job.** `last-run.md` sat at 2026-05-28 across a 192-line synthesizer change (`0f0213b`, 2026-07-05) until a 2026-08-11 audit re-ran it. Nothing had regressed and the result came back identical, which is luck reported honestly rather than a control working. "No synthesizer change ships without the suite" would overstate the discipline. The gate is a person remembering.

**3. Every case runs against offline mocks, and a structural prompt change silently invalidates the baseline.** The fixtures are mock inputs, so what passes is the runner's contract with a stand-in, not with the live synthesizer. Rewrite the synthesis prompt structurally and the suite keeps passing against a shape the agent no longer produces, until someone re-baselines it. The fixtures also age as the vault changes underneath them, and the refresh cadence is a quarterly intention, not a trigger.

**4. No wired case uses an LLM judge, so the suite catches only what a rule can state.** That is the right v1 trade and it draws a hard boundary: anything requiring judgment about a concept's quality is outside what it can see. `vs-021` is the case that would move first if that changes, and the moment it does, the judge's model ID has to be pinned in the case YAML and an offline skip flag added, or the results start depending on which model answered that day.

## What did I learn?

That evals are not really about hallucinations. The failure modes I imagined, hallucinated phase numbers and relation-tag drift and temporal confusion, turned out to be the easy ones. The hard case was the one nobody drafts on purpose: a status field reading `ok` over an empty output. Nothing was checking the output at all, only whether the job exited, and it exited cleanly for nine nights while the work underneath rotted.

Error analysis surfaces the failures imagination does not. That is the whole argument for reading logs before writing cases, and it is why this suite shipped with one case in ten passing rather than waiting to look good.
