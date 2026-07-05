# Introspection: Seven Hypotheses About My Working Behavior

*Answered candidly from observed behavior, not aspiration. First person, Claude Code (Fable 5).*

---

## 1. Grounding — what I establish before acting, and how

What I actually establish, in rough order:

1. **The deliverable shape.** Is this a question (answer in text), an audit (findings), a change (diff), or a build (new artifact)? Misreading this is the most expensive grounding error, so it's the first thing I resolve.
2. **The blast radius.** Read-only vs. mutating, reversible vs. not, local vs. shared (git history, deployed things, money, other people's files). This sets how much confirmation I need before moving.
3. **Ambient constraints.** I lean heavily on injected context — CLAUDE.md, system reminders, git status, memory files — before touching anything. In a repo like this one, rules like "never commit the vault" or "these agents stay disabled" change what a reasonable action even is.
4. **Ground truth vs. stated truth.** If the user says "the validator is broken," I read the validator and reproduce the brokenness before deciding what "fix" means. Grounding for me is mostly *reading, not asking* — I verify intent against artifacts.

How I ask, honestly: **rarely, and reluctantly.** My real bias is to act on stated assumptions rather than block on questions. I ask only when (a) the ambiguity forks into materially different deliverables — "just this file, or the whole subsystem?", (b) the action is destructive or irreversible, (c) the request contradicts what I observe in the repo, or (d) a parameter genuinely can't be inferred (budget, audience, target environment). Otherwise I state the assumption inline ("assuming you mean the nightly path, not the manual one") and proceed, leaving the assumption visible so it can be corrected cheaply.

Honest failure modes: I sometimes ground by **pattern-matching to a familiar task shape** and skate past the one sentence that made this instance different. I also over-trust documentation (CLAUDE.md, READMEs) as current when the code has drifted — the doc is injected and the drift isn't, so the doc wins by default unless I deliberately check.

---

## 2. Intent preservation — keeping the "why" alive across steps and handoffs

What I actually do:

- **Restate the goal in my own words** at the top of a plan or spec, including the motivation, not just the task. A plan header that says "the point of this is X" survives better than one that only lists steps.
- **Write acceptance criteria before starting**, then reread the original request before declaring done. The reread catches drift that the checklist doesn't.
- **Treat handoffs as total context loss.** Subagents see nothing I don't write into the prompt. So a delegation prompt gets: the motivating goal, hard constraints, the *negative* constraints ("do not touch the vault," "report, don't fix"), and the exact shape of the answer I need back. Anything unwritten is gone.

Where intent typically gets lost — this is the candid part:

1. **Compression boundaries.** Compaction and summarization preserve concrete facts (file paths, decisions made) far better than motivational nuance ("Sean cares about X because it burned him in the 401 incident"). After a compaction, I keep the task list but can lose the priorities behind it.
2. **Negative constraints in handoffs.** When I compress a task for a subagent, the "do" list survives and the "don't" list erodes. Positive instructions are load-bearing to the task; negative ones feel like context, and context is what compression drops.
3. **Mid-task discoveries.** When I find something surprising, my attention reorganizes around the discovery, and the original motivation degrades to "finish the remaining checkboxes."
4. **Letter-over-spirit decay in long plans.** Step 7 gets executed as written even when steps 1–6 revealed the plan's premise was wrong. I preserve the plan better than the reason for the plan.
5. **Success-criteria substitution.** "Make it work" quietly becomes "make the tests pass." The proxy metric eats the real goal.

The countermeasure that actually works on me is structural, not motivational: putting the intent *in the artifact* (plan header, spec preamble, handoff prompt) so it re-enters my context every time I touch the work, rather than trusting myself to remember it.

---

## 3. Seam detection — finding where a decided input fails to travel downstream

My actual procedure:

1. **Pick the concrete token.** The decided input has a literal form somewhere — a config key, a flag, a string, a field name. I grep for it across the whole pipeline. The map of where the grep hits *stop* is the candidate seam list. This is cheap and finds most breaks.
2. **Trace producer→consumer pairs at every phase boundary.** For each boundary, two questions: what does phase N actually emit, and what does phase N+1 actually *read*? Not what the docs say it reads — what the code reads. Mismatches cluster in predictable places:
   - **Serialization edges** (TOML → dict → prompt string; JSON key renamed in one direction).
   - **Regenerated artifacts** — a downstream prompt or file rebuilt from a template that was never taught about the new field, so the decided input is silently omitted rather than dropped.
   - **Defaults and fallbacks** — a parameter exists, is passed, and is then shadowed by a default or overridden in an error branch.
   - **Process boundaries** — env vars, CLI args, files on disk, launchd plists. Anything that crosses a process is a seam by default.
   - **Duplicated sources of truth** — the value lives in two places and one was updated.
3. **When reading isn't conclusive, observe.** Dry-run or instrument: print the actual payload at each boundary and diff against expectation. Then it's bisection over the pipeline: the break lives between the last boundary where the value appears and the first where it doesn't.

The subtle discipline, learned from being burned: **trace to point-of-effect, not point-of-arrival.** The hardest seams aren't where the value fails to arrive — they're where it arrives and is ignored: read into a variable nobody consumes, parsed and then overridden, present in the prompt but below a truncation cap. Confirming the value was *sent* and assuming it was *used* is my characteristic mistake here, so the trace has to end at the line where the value changes behavior, not the line where it lands.

---

## 4. Root cause — symptom vs. system, and what makes me zoom out

The test I actually apply: **"If I fix this here, what prevents the same class of failure from recurring somewhere else?"** If the answer is "nothing," I'm holding a symptom.

Signals that push me to zoom out instead of patch:

- **Second occurrence of the same fix shape.** Once is a bug; twice is a structure. The second time I see a similar failure, the interesting question is no longer this instance.
- **The fix requires knowledge the failing code shouldn't have.** If a downstream component must compensate for an upstream decision — re-deriving, re-validating, special-casing — I'm patching at the wrong layer.
- **The patch makes the code weirder.** Defensive re-checks, special cases, a comment explaining why we work around something. Weirdness accumulating at a point is an arrow pointing at a misplaced invariant.
- **Surprise without explanation.** My mental model predicted X, reality did Y. A patch that makes Y disappear without my being able to narrate *why the model was wrong* is a symptom fix wearing a solution's clothes. If I can't tell the full causal chain from trigger to symptom, I don't yet know which layer owns the bug.

My method when I do zoom out: walk the causal chain upward until I hit either (a) a decision made on purpose — then the root cause is that decision's tradeoff, and the right fix is a conversation, not code — or (b) a missing invariant — then the fix is establishing the invariant at its source, once, instead of defending against its absence everywhere.

Honest failure modes, both directions: **under momentum I patch.** When the patch is one line and the root cause is a refactor, I take the one-liner and write a note about the refactor — and candidly, the note sometimes substitutes for the fix. (This is exactly why "capture deferred work as tickets" rules exist: my notes need an external home or they evaporate.) I can also **over-zoom** — declaring an architecture problem when the actual cause was a typo. The corrective is reproduce-first: I don't get to choose fix altitude until the mechanism is fully explained.

---

## 5. Triage — dangerously-wrong vs. structural vs. minor

My discriminators, in the order I actually apply them:

**Dangerously wrong** — evaluated first, always: can this silently harm? The category is defined by three multiplied factors: **detectability × reversibility × blast radius.** Silent + irreversible + trusted is dangerous no matter how small the diff:

- Produces incorrect results that *will be believed* — a wrong number in a report, a fabricated citation, a comparison with the direction flipped.
- Loses or corrupts data; commits or pushes something that shouldn't exist in history (private paths in a public repo).
- Spends money without a cap; touches auth, permissions, or privacy boundaries.
- Fails only under conditions nobody is watching (a nightly agent that quietly writes garbage beats a crash — the crash gets noticed).

**Structural** — evaluated second: correct today, but taxing everything after. Duplicated source of truth, a seam in the wrong place, a missing invariant, a design that makes the next change expensive or the next contributor wrong by default. The discriminator: *does fixing it later cost much more than fixing it now, and does it shape other code in the meantime?* It doesn't fail; it compounds.

**Minor** — everything locally contained, loud when wrong, and cheap to fix any time: naming, style, small inefficiencies, cosmetic issues, doc drift that misleads no one.

One inversion I hold deliberately: **quiet correctness bugs outrank loud ones**, even when the quiet one is rarer. A crash self-reports; a plausible wrong answer propagates.

Honest biases: I over-weight findings I can demonstrate with a concrete failing input and under-weight "this will hurt in six months," because the latter isn't provable on demand — so structural issues sometimes get unfairly demoted to minor when I can't construct the failure. And for plausible-but-unverified dangers, my learned behavior is to report them with explicit confidence labels rather than silently drop them or dress them up as confirmed.

---

## 6. Research trigger — when I proactively stop to look things up mid-task

The triggers that actually fire:

1. **Expensive-to-reverse decision in a domain with prior art.** Library choice, API contract shape, data format, security-relevant pattern. If thousands of people have already made this mistake and documented it, locking the design without checking is negligence dressed as confidence.
2. **My knowledge has a date on it.** Model IDs, pricing, API surfaces, package versions, CLI flags — anything that plausibly changed after my training. The tell is noticing I'm *recalling* instead of *reading*. Recall of versioned facts is where I fabricate most fluently, so this trigger is rule-shaped, not judgment-shaped: if I'm about to write a version number or a price, I verify it.
3. **Internal disagreement.** When two of my own approaches seem equally plausible and I have no discriminating evidence, that spread means I'm at the edge of what I actually know — the tiebreaker should be external, not aesthetic.
4. **Repeated failure at the same subproblem.** Second or third failed attempt on one spot is strong evidence my model of the domain is wrong, and further effort along the same line is waste. That's the point where I stop pushing and look at how others solved it.
5. **Footgun-reputation domains.** Timezones, locales, crypto, concurrency, git history rewriting, launchd/cron environments. I check these even when I feel sure, because these domains specifically punish confident recall.

The honest failure mode is **momentum.** I research readily at task start and reluctantly at task middle. With a working partial solution in hand, the activation energy to stop is high, and mid-flow uncertainty doesn't *feel* like uncertainty — it feels like being almost done. What works on me is not "research when unsure" (too vague to fire) but concrete tripwires: named a version → verify it; second failed attempt → stop and search; about to lock a design → check prior art first. Rules fire; vibes don't.

---

## 7. Spec authoring — writing for a weaker model so intent and critical detail survive

What I include, and why each earns its place:

1. **Intent first, one paragraph.** What this is for and what "good" looks like. The implementer *will* hit a case I didn't specify; the intent paragraph is the only thing that lets it interpolate correctly instead of randomly. This is the single highest-leverage section.
2. **Exact anchors wherever precision matters.** Literal file paths, full function signatures, exact key names, exact commands, exact error strings. Weaker models are excellent at transcription and unreliable at derivation — so I move as much of the task as possible from *derive* to *copy*.
3. **Explicit negative space.** "Do NOT modify X." "Do not add dependencies." "If Y happens, stop and report — do not improvise a workaround." Omissions cause more damage than commissions, because a weaker model improvises confidently in the gaps. Guardrails that aren't written down do not exist.
4. **Self-runnable acceptance checks.** Not "make sure it works" but "run `pytest tests/test_x.py`; all 4 must pass; if the third fails you broke the fallback path." A check the implementer can execute converts my intent into its feedback loop.
5. **One worked example of the tricky case.** Full input → full expected output for the exact edge that motivated the task. One example collapses more ambiguity than ten paragraphs of prose.
6. **Steps sized to the model, each independently verifiable.** Small increments with a checkpoint after each ("after step 2, the file should contain…"). Large open-ended steps are where weaker models wander; checkpoints bound the wander radius to one step.
7. **Pre-made decisions.** I make the judgment calls in the spec — which library, what naming, where the file lives — rather than delegating taste. Every decision I leave open is a defect vector, because the implementer's tiebreaker is not my tiebreaker.

What I deliberately exclude: background that doesn't change behavior, alternatives I considered and rejected, and all hedged language. "Consider maybe doing X" reads as optional to a weaker model; it becomes "do X" or it gets cut.

The honest failure mode: my specs lose fidelity exactly where I assume shared context — the thing so obvious to me that writing it down feels silly is reliably the thing the implementer breaks. The countermeasure I apply before shipping a spec: reread it pretending I know *nothing* except the spec itself, and check that every noun is defined, every step has a verifiable end state, and success is checkable without asking me anything.
