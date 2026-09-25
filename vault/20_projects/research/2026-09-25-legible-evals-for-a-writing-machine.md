---
title: "Legible evals for a writing machine: what the page shows and names"
date: 2026-09-25
type: research
status: draft
issue: 305
tags:
  - evals
  - error-analysis
  - content-machine
  - trace-kit
  - husain
  - research
---

# Legible evals for a writing machine: what the page shows and names

**Question.** How do you make an eval of a writing machine easy for its owner to read at a glance? The owner is a product manager, not a developer, learning evals by doing them. The trace kit built on [#291](https://github.com/seanwinslow28/code-brain/issues/291) records the right facts but presents them in the kit's vocabulary, and he cannot follow it. This note is for [#305](https://github.com/seanwinslow28/code-brain/issues/305); its test bed is [#302](https://github.com/seanwinslow28/code-brain/issues/302).

**Source tiers:** A academic · B primary (the author's own post, repo or paper) · C trade press · D forum or personal post. Every claim below is B or A, cited to the author's own page. The vault's earlier primer on Husain was not used.

**Privacy.** The kit was exercised only on its own synthetic run (an invented three-card deck of invented posts, `tests/deck_synth.py`). Nothing from a real run, the corpus, the samples or a draft appears here.

---

## 1 · Recommendation: the page, in under 300 words

**Unit.** One row per **card** (a draft), not one per stage invocation. The three-card synthetic deck renders as fifteen rows today; twelve are scripts and gates needing no human verdict. Sean judges outcomes: the page asks about the draft and shows what ran on it.

**Layout.** A counter ("Card 2 of 8"), one card open at a time. Left: the post it answers, then the draft. Right: verdict, critique, and the checks in plain words ("Origin check: nothing lifted", "Coined-lines: one phrase flagged, quoted"). Above the cards, one sentence: cards, judged, failed, where fails most often entered.

**Columns** (closed-card list): Card · Answers (the post's first line) · Verdict · Where it went wrong · Why.

**Label set, the smallest useful.** Three fields. **Verdict:** pass or fail. **Where it went wrong** (fail only): five plain phrases, not numbers — *the Oracle picked it* · *the post it answers* · *the draft* · *a check missed it* · *the pick*. **Why:** one to three sentences, caption "What went wrong, and what would fix it?" No failure code or tags until thirty labels exist.

**Verdict form.** The word and the glyph, keys `1` / `2`, revisable until copied out. The critique sits beside the verdict on the closed row, never folded.

**Deliberately off the surface** (one "Under the hood" fold per card): pass ids, seat and kind names, hashes, meters, wall-clock, launch forms, timestamps, `## Moves` lines, the ten record checks (one line replaces them: "Records check out" or "2 records don't; open to see"), the train, the transition matrix until ten fails exist, and every Productcraft-only block that renders empty here.

**Names.** Rename on the page, never in the files. "Pass" is the verdict word only; the unit is a *step*. Stages read as phrases, not `3 Shape`.

---

## 2 · What Husain actually says, point by point

Each point is cited to the post and the section heading where it appears.

1. **Remove all friction; render the trace in domain terms; everything on one screen.** "You must remove all friction from the process of looking at data. This means rendering your traces in domain-specific ways. I've often found that it's better to build my own data viewing & labeling tool so I can gather all the information I need onto one screen." — *Your AI Product Needs Evals*, § Level 2: Human & Model Eval → Looking At Your Traces ([B](https://hamel.dev/blog/posts/evals/)).

2. **Start with good/bad, not scores.** "I often start by labeling examples as good or bad. I've found that assigning scores or more granular ratings is more onerous to manage than binary ratings." — same post, same section. Expanded in the FAQ: "Binary evaluations force clearer thinking and more consistent labeling … annotators often default to middle values to avoid making hard decisions." And: "Start with binary labels to understand what 'bad' looks like. Numeric labels are advanced and usually not necessary." — *AI Evals FAQ*, Q: Why do you recommend binary (pass/fail) evaluations instead of 1-5 ratings ([B](https://hamel.dev/blog/posts/evals-faq/why-do-you-recommend-binary-passfail-evaluations-instead-of-1-5-ratings-likert-scales.html)).

3. **The nuance goes in the critique, not the scale.** "Nuance isn't lost – it's just moved to the qualitative critique that accompanies the judgment." — *Field Guide*, § 5 → Favor Binary Decisions Over Arbitrary Scales ([B](https://hamel.dev/blog/posts/field-guide/)). His model critique names the pass, then the flaw, in one paragraph: the market analysis was delivered (PASS) but carried irrelevant demographic detail — § 5 → Enhance Binary Judgments With Detailed Critiques.

4. **A critique is written for a new employee.** "It should be detailed enough that a new employee could understand it. Being too terse is a common mistake." — *LLM-as-a-Judge*, Step 3 → Examples of Good Critiques ([B](https://hamel.dev/blog/posts/llm-judge/)). The kit's labels caption already says this ("one to three sentences a new hire could act on"); keep it.

5. **Do not root-cause while labeling.** "At this point, you don't need to perform a root cause analysis into the technical reasons behind why the AI failed. Many times, it's useful to get a sense of overall behavior before diving into the weeds." — *LLM-as-a-Judge*, Step 3, the note after the critique examples. This bounds the "where it went wrong" field: it records the first place the reader *saw* the problem enter, not an investigation.

6. **Note the first failure; upstream errors cause downstream ones.** "It is recommended to focus on noting the first failure observed in a trace, as upstream errors can cause downstream issues, though you can also tag all independent failures if feasible." — *FAQ*, Q: Why is "error analysis" so important → 2. Open Coding ([B](https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html)). Repeated for large traces: "A useful heuristic is to focus on the first upstream failure. Errors tend to compound." — *FAQ*, Q: How do you review a trace that is really large? ([B](https://hamel.dev/blog/posts/evals-faq/)). This is the primary-source warrant for the kit's `first_failing_stage`; the field is right, only its presentation (a number 0–6) is not.

7. **One domain expert, the "benevolent dictator".** "For most small to medium-sized companies, appointing a single domain expert as a 'benevolent dictator' is the most effective approach." — *FAQ*, Q: How many people should annotate my LLM outputs? ([B](https://hamel.dev/blog/posts/evals-faq/how-many-people-should-annotate-my-llm-outputs.html)). Sean is the one labeler; the page needs no agreement machinery.

8. **The expert judges outcomes, not mechanics.** "Ask 'Has an appointment been made?' not 'Did the tool call succeed?' … Keep all context on one screen so non-technical reviewers focus on results." — *FAQ*, Q: Should product managers and engineers collaborate on error analysis? ([B](https://hamel.dev/blog/posts/evals-faq/should-product-managers-and-engineers-collaborate-on-error-analysis-how.html)). For this machine the outcome is the card; the gate runs, hashes and meters are the tool calls.

9. **Hand-read first: 30 yourself, ~100 to saturation, taxonomy after.** "Start with 100 diverse traces and annotate at least the first 30 yourself." "Keep this first pass manual. If the agent starts suggesting problems too early, its guesses can bias your judgment." "Continue until new traces stop revealing failure modes … theoretical saturation." — *FAQ*, Q: How many examples do I need for an eval? → Stage 1 ([B](https://hamel.dev/blog/posts/evals-faq/how-many-examples-do-i-need-for-an-eval.html)).

10. **Judges are earned, per failure mode, at 30–50 labels per class.** "Plan to label 100 to 200 examples for each failure mode … When possible, include 30 to 50 Pass examples and 30 to 50 Fail examples in both the dev and test sets." — same Q, Stage 2 → LLM judges need labeled examples. Validation is TPR and TNR, not agreement: "if an error occurs in 5% of examples, a judge that always predicts Pass still has 95% agreement while detecting none of the errors." — *LLM-as-a-Judge*, FAQ → How do you validate an LLM judge against human labels?

11. **Taxonomy after open notes; count them; three modes usually dominate.** At NurtureBoss the team "wrote open-ended notes on any undesired behavior. Then we used an LLM to build a taxonomy … mapped each row to specific failure mode labels and counted the frequency," and "just three issues accounted for over 60% of all problems." — *Field Guide*, § 1 → Bottom-Up vs. Top-Down Analysis ([B](https://hamel.dev/blog/posts/field-guide/)). The kit's empty `taxonomy.md` is faithful to this.

12. **Build a custom tool; the checklist for a good one.** "Build a custom annotation tool. This is the single most impactful investment you can make." — *FAQ*, Q: Should I build a custom annotation tool or use something off-the-shelf? ([B](https://hamel.dev/blog/posts/evals-faq/should-i-build-a-custom-annotation-tool-or-use-something-off-the-shelf.html)). What makes it good: "Present the trace in a way that's intuitive for the domain … keep less important details in collapsed sections"; "progress indicators (e.g., 'Trace 45 of 100')"; "hotkeys for navigating between traces"; and the closing rule, "Keep your annotation interface minimal." — *FAQ*, Q: What makes a good custom interface for reviewing LLM outputs? → 1, 2 and General Principle ([B](https://hamel.dev/blog/posts/evals-faq/what-makes-a-good-custom-interface-for-reviewing-llm-outputs.html)). The Field Guide's five-line version: "Show all context in one place … Make feedback trivial to capture. One-click correct/incorrect buttons beat lengthy forms … Capture open-ended feedback … Enable quick filtering and sorting … Have hotkeys" — § 2 → Here's what makes a good data annotation tool.

13. **Dashboards and generic metrics are the trap.** "The kind of dashboard that foreshadows failure." "Too many metrics fragment your attention … When everything is important, nothing is." — *Field Guide*, § 1. "If your evaluations consist of a bunch of metrics that LLMs score on a 1-5 scale … you're doing it wrong." — *LLM-as-a-Judge*, Step 3 → Don't stray from binary pass/fail judgments. A page that leads with ten record checks, four counters and a matrix is a dashboard by another name.

14. **No hosted tool first; a spreadsheet beats nothing.** "Start with error analysis, not infrastructure." — *FAQ*, Q: What's a minimum viable evaluation setup? "I have no favorite vendor … I often build custom tools on top of them to fit my needs." — *FAQ*, Q: What's your favorite eval vendor? ([B](https://hamel.dev/blog/posts/evals-faq/whats-your-favorite-eval-vendor.html)). "If you're just beginning, a spreadsheet is better than nothing." — *Field Guide*, § 2.

15. **Criteria drift is normal; labels may be revised.** Quoting Shankar et al.: "the process of grading outputs helps them to define that very criteria," and his own gloss, "it is impossible to completely determine evaluation criteria prior to human judging." — *Field Guide*, § 5 → Understanding Criteria Drift. The kit's revisable in-page draft is right.

16. **For a solo expert with cheap data, skip the judge.** "You are an independent developer who is also a domain expert … Looking at data is not costly … it's probably fine to just do error analysis without a judge (at least initially)." And: "creating a LLM judge is a nice 'hack' I use to trick people into carefully looking at their data!" — *LLM-as-a-Judge*, Recap → Do You Really Need This? / It's Not The Judge That Created Value. This is Sean's case exactly: the page's job is to make him read cards, not to prepare a judge.

---

## 3 · What other primary sources add or contradict

**Shankar et al., "Who Validates the Validators?" (EvalGen), CHI/UIST 2024 ([A](https://arxiv.org/abs/2404.12272)).** Adds the interface evidence behind Husain's point 15: "Since it may be time-consuming to ask the developer to grade on a per-criterion basis, for the grader interface we decided on the simplicity of thumbs-up/down scoring" (§ 3.1), with "the context of the prompt and any input variables" shown beside the output. "We dub this phenomenon criteria drift, and it implies that it is impossible to completely determine evaluation criteria prior to human judging of LLM outputs" (§ 1). Implication for the page: the post must sit beside the draft, and the stage phrases will be re-worded after the first deck is read.

**Eugene Yan, AlignEval ([B](https://eugeneyan.com/writing/aligneval/); code [B](https://github.com/eugeneyan/align-app)).** "In labeling mode, our only job is to look at the data … for each sample, we only have to make a binary decision—pass or fail." "We should also resist the urge to prematurely define criteria." Gating: "After labeling 20 rows, we unlock evaluation mode," with his own caveat to aim for 50–100 first, and "Evaluate on a single dimension and return either 0 (pass) or 1 (fail)" — § Labeling mode / § Evaluation mode. Adds: the page can hide the taxonomy and judge slots entirely until the threshold, rather than rendering them empty.

**Eugene Yan, "Evaluating the Effectiveness of LLM-Evaluators" ([B](https://eugeneyan.com/writing/llm-evaluators/)).** A nuance Husain does not make: "Pairwise comparison … is typically used—and more reliable—for subjective evals such as persuasiveness, tone, coherence." Voice is subjective. When the machine one day judges two drafts of the same card, a side-by-side "which is more his" may label better than pass/fail on each. Not adopted now; noted for the judge rung.

**Husain & Shankar, `evals-skills` → `build-review-interface` ([B](https://github.com/ai-evals-course/evals-skills/blob/main/skills/build-review-interface/SKILL.md)).** Their own agent-facing spec for the viewer, and the closest thing to a reference implementation: "displays one trace at a time with Pass/Fail buttons, a free-text notes field, and Next/Previous navigation"; "Annotate at the trace level. The reviewer judges the whole trace, not individual spans"; "Defer button for uncertain cases"; "Once you have established failure categories from error analysis, you can later add predefined failure mode tags … But don't add these in the initial build"; "Collapse what doesn't help judgment"; "Same layout, controls, and terminology on every trace". Two points cut against the kit as ratified: the checklist wants "Pass and Fail buttons are visually distinct (color, size)", where DESIGN.md § 3 and § 13.1 ratified ink-only verdicts; and it wants a Defer key, which the kit has no state for (an empty verdict is "waiting", not "deferred"). Both are Sean's calls, flagged, not decided here.

**Husain & Shankar, `evals-skills` → `error-discovery` ([B](https://github.com/ai-evals-course/evals-skills/blob/main/skills/error-discovery/SKILL.md)).** Stricter still for the first pass: "No quality labels, no dropdowns, no structured forms. Free-text notes only," with notes as "side notes in a right margin column, aligned vertically with their corresponding highlighted text," and the header "title + label + topic. Keep it minimal." This contradicts the kit's stage picker on a fail. Reconciled by Husain's own point 6: the first failure observed is worth one field, so the recommendation keeps it, as five phrases rather than a numbered select, and keeps everything else free text.

---

## 4 · What in the current kit gets in the way

Named against the synthetic render (`render.py` on `tests/deck_synth.py`), the templates, and `machine.py`. None of these is a wrong fact; each is a right fact in the wrong words or the wrong place for a first-time reader.

1. **"Pass" is both the unit and the verdict.** Records are `pass-05`, rows read `pass-05 … pass`, the counter says "Labeled 14 of 15" and the checker says "Every pass has a label row." A reader learning the word *pass* meets it two ways in one line. Files: `labels-template.md` (`| pass | verdict |`), `record-template.md` (`pass: pass-05`), the row summaries in `tracekit/viewer.py`.

2. **Fifteen rows for three cards.** Twelve of the synthetic run's fifteen steps are the sweep, three stimulus blocks, six gates, the pick and the lesson: scripts and people, each shown with `UNMEASURED`, "No moves: this kind hands no artifact forward" and a full verdict form. Husain's unit is the trace, here the card; the page's unit is the invocation.

3. **Seat · kind pairs as names.** `x-sweep sweep`, `stimulus stimulus`, `shaper shape`, `origin-gate gate`, `orchestrator lesson` in filenames (`pass-NN-<seat>-<kind>.md`) and row headers. "Stimulus stimulus" says nothing to anyone who did not write `machine.py`.

4. **Stages as numbers.** The fail picker "Where did the problem first enter the workflow?" offers `0 Oracle … 6 Lessons`. The question is plain; the answers are the kit's numbering. Stage 6 cannot be where a card fails and should not be offered.

5. **Rung vocabulary and the ten check names.** "Rung 0 is clean on 10 of 10 checks", "rung 1 is unopened", and check titles such as "Meter present or UNMEASURED", "Trials blind-labeled before their runtime is shown", "Cited corpus files appear in the transcript's file reads 0 of 0", "Every failure_code is in the taxonomy; a quote-required code quotes its text". Right for the checker's stdout (`check.py`), wrong as page copy (`CHECK_IMPLICATIONS` in `machine.py` is already the plain-language version; the page shows both).

6. **Productcraft-shaped sections that are empty here.** "Reviewer findings 0 material · 1 note", "Owner decisions 0 pending · 0 accepted", "Guided reading — No cases have been written", three "What comes later" slots, and a train legend for `repair · audit · co-sign · trial · triggered by (a bounce loop)`, none of which are kinds the machine has. Inherited through DESIGN.md § 14 and `Studio`; they teach Productcraft's world on the machine's page.

7. **The transition matrix at one fail.** "last good ↓ · first failing →" with hatched impossible cells, captioned "1 fails so far, which is too few for a heat." DESIGN.md § 7 already says counts below ten are not a chart; the matrix is drawn anyway.

8. **`## Moves` vocabulary collides with the voice-move roster.** `kept / added / split / merged / dropped` naming `Rep 7e`; `record-template.md` itself notes the collision ("nobody reads `kept` as a licensed move"). Belongs under the hood.

9. **Raw record fields on the surface.** `shadow_of`, `triggered_by`, `meter_source: Agent-tool usage`, ISO instants, sha256 prefixes, verbatim launch command lines. One rendering bug worth a line of its own: a script's `withheld` block renders as a Python dict, `{'nothing': 'a script, no context'}`, on the page.

10. **`failure_code` shown while empty.** Every row ends "failure_code stays blank until a taxonomy exists" — Husain's own skill says not to add the tag field in the initial build.

Kept as is, because they already read plainly: the four review prompts in `machine.py` (`REVIEW_PROMPTS`), the section names "What you are judging" / "Where it broke", the critique caption, the `1` / `2` / `j` / `k` keys, the ink-only verdict and the one-file, no-network rule.

---

## 5 · Sources

Primary (B) unless marked.

- Hamel Husain, *Your AI Product Needs Evals* — https://hamel.dev/blog/posts/evals/ (§ Level 2: Human & Model Eval → Looking At Your Traces; § Automated Evaluation w/ LLMs)
- Hamel Husain (with Shreya Shankar), *AI Evals: Everything You Need to Know* (the FAQ) — https://hamel.dev/blog/posts/evals-faq/ ; per-question pages cited above:
  - Why binary — https://hamel.dev/blog/posts/evals-faq/why-do-you-recommend-binary-passfail-evaluations-instead-of-1-5-ratings-likert-scales.html
  - Error analysis — https://hamel.dev/blog/posts/evals-faq/why-is-error-analysis-so-important-in-llm-evals-and-how-is-it-performed.html
  - How many examples — https://hamel.dev/blog/posts/evals-faq/how-many-examples-do-i-need-for-an-eval.html
  - How many people — https://hamel.dev/blog/posts/evals-faq/how-many-people-should-annotate-my-llm-outputs.html
  - PMs and engineers — https://hamel.dev/blog/posts/evals-faq/should-product-managers-and-engineers-collaborate-on-error-analysis-how.html
  - Custom tool — https://hamel.dev/blog/posts/evals-faq/should-i-build-a-custom-annotation-tool-or-use-something-off-the-shelf.html
  - Good interface — https://hamel.dev/blog/posts/evals-faq/what-makes-a-good-custom-interface-for-reviewing-llm-outputs.html
  - Favorite vendor — https://hamel.dev/blog/posts/evals-faq/whats-your-favorite-eval-vendor.html
- Hamel Husain, *A Field Guide to Rapidly Improving AI Products* — https://hamel.dev/blog/posts/field-guide/ (§ 1, § 2, § 5)
- Hamel Husain, *Creating a LLM-as-a-Judge That Drives Business Results* — https://hamel.dev/blog/posts/llm-judge/ (Step 3, Recap, FAQ)
- Shreya Shankar, J.D. Zamfirescu-Pereira, Björn Hartmann, Aditya Parameswaran, Ian Arawjo, *Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences* (A) — https://arxiv.org/abs/2404.12272 (§ 1, § 3.1, § 7.3.1)
- Eugene Yan, *AlignEval: Building an App to Make Evals Easy, Fun, and Automated* — https://eugeneyan.com/writing/aligneval/ ; code https://github.com/eugeneyan/align-app
- Eugene Yan, *Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)* — https://eugeneyan.com/writing/llm-evaluators/
- Husain & Shankar, `ai-evals-course/evals-skills` — https://github.com/ai-evals-course/evals-skills ; `skills/build-review-interface/SKILL.md` and `skills/error-discovery/SKILL.md`

Kit files read (main checkout, read-only): `.claude/skills/content-machine/trace/{README.md, check.py, render.py, machine.py, labels-template.md, record-template.md, taxonomy.md, tests/deck_synth.py}`; `productcraft/trace/DESIGN.md`; `productcraft/trace/tracekit/viewer.py`; issues #261, #272, #291, #305.

**Unverified or weak points.** Isaac Flath's Anki annotation app and the "Building Eval Tools with FastHTML" video are named in the FAQ but were not watched. The EvalGen quotes come from the arXiv HTML render, not the CHI proceedings version. The `evals-skills` skills are agent instructions, not a running viewer; they were read as the authors' spec, not tested.
