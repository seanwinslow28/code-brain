---
title: "Eval trace viewer design prior art"
date: 2026-09-11
project: productcraft
status: draft
ticket: "#292"
tags: [research, productcraft, evals, viewer]
---

# Eval trace viewer design prior art

Prior art for a local, self-contained, one-expert HTML viewer that shows a train of 20-30 seat passes over numbered stages, pass/fail + first_failing_stage + critique per pass, a transition failure matrix (counts), per-stage pass counts, tokens and wall-clock, bounce loops, and blind shadow passes. Each exhibit records the source, the concrete UI facts, and what transfers. Fetched 2026-09-11; several vendor UI pages 404'd and are listed under Gaps.

## Exhibit 1: Hamel Husain's annotation viewers (tier B)

### 1a. Rechat "Lucy" viewer — hamel.dev/blog/posts/evals/

- One screen shows the trace log next to the CRM record it came from, plus deep links to the CRM and to the trace-logging platform for that record.
- The final output is an editable field, so a human-corrected answer can be saved for fine-tuning.
- Navigation: pick the tool/feature under test, filter by scenario combination, and a flag distinguishes synthetic inputs from real user traces.
- Labeling is binary good/bad; finer scales were "more onerous to manage than binary ratings."
- Stated goal: "Remove all friction from the process of looking at data." Built in Shiny for Python in under a day.

### 1b. Field guide (NurtureBoss) — hamel.dev/blog/posts/field-guide/

- Search/filter to jump to an error type; one-click correct/incorrect buttons; a free-text field for notes outside the taxonomy; hotkeys to move between examples and label "without clicking"; a pivot table for counts.
- Rejects 1-5 scales because "a 3 and a 4" cannot be told apart; the format is binary plus a written critique that says what passed and what was wrong.
- Open coding (free notes on ~100 traces) then axial coding into under ten failure modes; three modes covered over 60% of failures.

### 1c. Evals FAQ entries

- *What makes a good custom interface* — render per domain ("render them to look like emails," syntax highlighting for code); "keep less important details in collapsed sections"; show user input, tool calls, and reasoning; progress text of the form "Trace 45 of 100"; hotkeys such as "N for next" plus quick-apply labels; filter by metadata, keyword search, clustering; surface traces flagged by guardrails or automated evaluators; show pipeline version and eval scores in place. Four screenshots described: a domain-rendered email, an annotation screen with progress bar and hotkey guide, a cluster view, a trace view with the auto-evaluator verdict and dataset buttons.
- *Custom vs off-the-shelf* — custom "show all your context from multiple systems in one place," render product-specifically, and are "designed for your specific workflow"; Isaac Flath's Anki tool handles "400+ results per query with keyboard navigation." Off-the-shelf only earns its keep for "dozens of distributed annotators."
- *Agentic workflows* — a transition failure matrix: rows = last successful state, columns = where the first failure occurred; example GenSQL → ExecSQL 12 vs DecideTool → PlanCal 2. Two levels: end-to-end task success plus step-level diagnostics; "Record the first upstream failure during error analysis." Credits Bryan Bischof's text-to-SQL work for showing "variation in transition matrices across experiments."
- *Multi-step workflows* — log the whole chain from trigger to business outcome; segment error analysis by early/middle/late stage; fix early-stage failures first because "errors cascade in LLM chains."
- *How many / who* — ~100 diverse traces reach saturation; a single domain expert as "benevolent dictator."

### 1d. Lenny's Newsletter, "Building eval systems that improve your AI product" (tier C, authored by Husain/Shankar)

- Screenshot: Arize Phoenix showing a leasing-assistant conversation, a free-form critique field, and a binary pass/fail toggle.
- Critiques should be "detailed enough for a brand-new employee"; the matrix "Rows represent the last successful step."

**Transfers:** binary + critique, first-failing-stage label, collapsed non-critical detail, "n of N" counter, single-key next/label, keyword filter, matrix as counts. **Does not transfer:** clustering/semantic search (needs embeddings, no network), multi-annotator tooling, dataset/bug-filing action buttons.

## Exhibit 2: EvalGen, Shankar et al. arXiv 2404.12272 (tier A)

- Grading screen: one LLM output centred, the input variables and context on the left, the prompt on the right, "Good and Bad grade buttons"; graders can move back through outputs and revise earlier grades.
- Sampling is active-learning driven (selectivity estimates and confidence of poor outputs pick the next item).
- Report card: per-criterion and aggregate alignment; hovering a criterion shows "a confusion matrix," with coverage and false-failure-rate columns.
- Criteria drift: "it's hard to know until you see it"; participants "went back and change[d] previous grades." All but one participant found grading while waiting a good use of time; the one wanted the tool to show what it was doing with grades.

**Transfers:** input visible beside output at all times; revisable labels; a per-criterion confusion-matrix view. **Does not transfer:** active-learning sampling (the train is fixed and short).

## Exhibit 3: Observability trace views (tier B, vendor docs)

### Langfuse

- Trace view has a tree/timeline toggle "fully on par," view settings to "show/hide scores, comments, metrics," and search of observations "by type, ID, or name" (changelog 2025-03-19).
- Table peek panel: `J` next trace, `K` previous, `Esc` closes, table stays in view (changelog 2025-03-21).
- Annotation queues: one item at a time; score configs are categorical, boolean, or numeric, each with a comment; `→`/`←` between items, `1`-`9` pick an option, `Cmd/Ctrl+Enter` completes; "Press ? in the queue to open the in-app cheatsheet."

### Braintrust

- Experiment rows are traces; the trace pane shows "Input, output, and expected values," all spans, "scores and their explanations," timing and tokens; spans expand/collapse.
- Comparison: "Order by regressions" sorts score columns by change against a comparison experiment; in diff mode "Timeline, Thread, and custom views are disabled"; Grid layout puts outputs side by side.
- Human review: categorical, continuous (slider), and free-form scores; "a reviewer can't see peer scores, comments, or aggregate results" until they score, and blind mode hides them throughout.

### Arize Phoenix

- Retriever spans carry DOCUMENT_ID, DOCUMENT_SCORE, DOCUMENT_CONTENT, DOCUMENT_METADATA, so retrieved documents render as first-class items with scores and order; annotations carry label, score, and explanation; the same filter expressions work in the UI filter bar.

**Transfers:** J/K/Esc peek, `1`-`9` label keys, `?` cheatsheet, comment attached to every score, show/hide toggles for metrics, hide the other label until the reader has committed (the shadow-pass rule), retrieved/attached artefacts as first-class rows. **Does not transfer / is noise:** span waterfalls with nested chain/LLM/tool spans and per-span attribute tabs — for one reader of 20-30 passes the unit is the pass, not the span; timeline charts; SQL filters; assignment and review-status columns.

## Exhibit 4: Error-analysis viewers

### Inspect AI log viewer (tier B, inspect.aisi.org.uk/log-viewer.html + CHANGELOG)

- Top: task summary with metrics (accuracy, bootstrap std dev). Below: a samples table with input, target, extracted Answer, and score; "Use the Scores picker to filter" (e.g. Incorrect); Sort by epoch sequence, by score, or by sample so all epochs of one sample sit together.
- Sample view tabs: Messages (history incl. tool calls), Scoring ("the full input and full model explanation"), Metadata, Transcript; Info tab holds dataset, solver, scorer, git revision, token usage.
- Tool calls with long arguments sit in an "expandable input zone"; "more..." toggles on heavy events; Messages paginates on scroll (0.3.259). Transcript event navigation is "keyboard-driven turn and agent navigation" with a focus view for agent subtrees (0.3.251). Transcript markdown escapes HTML outside code blocks (0.3.252).
- `inspect view` binds 127.0.0.1:7575; `inspect view bundle` emits a static directory with the root viewer HTML, assets and logs, servable from GitHub Pages/S3. Husain's note: it gives "a clear way to inspect individual successes and failures."

**Transfers:** summary-above-table-above-detail; filter by verdict; sort so re-runs of one input group together (maps to shadow pairs and bounce loops); score explanation on its own tab; long arguments collapsed by default; escape HTML in rendered output; static bundle. **Does not transfer:** bundle needs HTTP range requests, so it is not a single file.

### Bryan Bischof, "Failure is a Funnel" (tier C; Heavybit write-up, Humanloop transcript, Husain FAQ)

- SQL agent failures split into stages (retrieve tables, select valid tables/columns, execute, correct result) and counted as a funnel; "Evaluation is a multi-step procedure"; "you will answer most of the hard product questions by looking at the data"; a weekly "evals party." The primary talk video was not extractable (see Gaps).

### AlignEval, Eugene Yan (tier B)

- Labeling: input and output side by side, only "pass or fail," a progress bar, evaluate mode unlocks "After labeling 20 rows," 50-100 recommended before writing criteria; look "with an open mind" before writing criteria.
- Evaluate: sample size, recall, precision, F1, Cohen's κ, TP/FP/TN/FN counts in the top-right.

### Chrestotes "Where did it break?" (tier D, practitioner post citing Husain)

- One matrix entry per failing trace: "the handoff from the last successful state to the first failed state"; rows and columns use the same state vocabulary; example 18 at troubleshoot/knowledge → troubleshoot/reasoning. The matrix locates the break, not the cause.

## Exhibit 5: Blind paired comparison, Chatbot Arena arXiv 2403.04132 (tier A)

- Two anonymous responses side by side; "Models' identities revealed only after voting"; votes are A, B, tie, or both bad; the user can keep chatting before voting.
- Leakage control: conversations naming a model or company (GPT, Claude, OpenAI, Anthropic) are filtered by keyword.
- Expert re-rating of 160 battles agreed with the crowd 72-83%.

**Transfers to the shadow rule:** hide the runtime label until both verdicts exist; scrub runtime-identifying strings (model names, tool banners, runtime version lines) from the displayed pass text or the blind is void; show the reveal only after commit.

## Exhibit 6: Single-file and printable HTML (tier B/D)

- pytest-html: `--self-contained-html` inlines CSS and images "which can be more convenient when sharing"; "all rows...will be expanded except those that have Passed"; `?sort=`, `?visible=`, `?collapsed=` query parameters set initial state; outcome checkboxes show/hide passed/failed/skipped.
- Allure: `allure generate --single-file` (2.30+) produces one HTML that opens from the file system; issue #755 records that a browser "save page" of the served report broke (loaders, 404s). Third-party allure-combine predates it.
- Inspect bundle: static but multi-file, needs range requests.
- MDN print guide: `@media print` hides nav/buttons; `break-inside: avoid` on rows and matrices; `orphans`/`widows: 3`; `@page { margin }`; `print-color-adjust: exact` if verdict colours must survive; `a::after { content: attr(href) }`; force collapsed sections open in print.

## Principles that recur across sources

1. Binary verdict plus a written critique; no Likert (Husain field guide, evals FAQ, AlignEval, EvalGen's Good/Bad).
2. Input and output visible together, never output alone (EvalGen, AlignEval, Rechat CRM-beside-trace).
3. Label the first failing step and aggregate as last-good × first-fail counts (Husain agentic FAQ, Bischof, chrestotes).
4. Collapse what is not needed for the verdict; long tool arguments and metadata folded by default (Husain FAQ, Inspect 0.3.259, Braintrust spans).
5. Keyboard-only labeling loop: next/prev, numbered labels, commit, `?` cheatsheet (Langfuse queues and peek J/K, Husain "N for next", Flath's tool).
6. Bounded session with an explicit "n of N" counter (Husain "Trace 45 of 100", AlignEval progress bar).
7. Filter by verdict and group re-runs of the same input together (Inspect Scores picker and sort-by-sample, pytest-html outcome filters).
8. Labels are revisable; graders go back and change grades as criteria drift (EvalGen).
9. Hide anything that would bias the judgement until the judgement is committed: peer scores, model identity (Braintrust blind review, Chatbot Arena).
10. One reader, one file: custom over generic, self-contained over served (Husain custom-tool FAQ, pytest-html self-contained, Allure single-file).
11. Escape rendered model text; render by domain only where safe (Inspect 0.3.252, Husain rendering advice).
12. Summary strip above the table above the detail pane (Inspect, Braintrust experiment table, AlignEval metrics corner).

## Sources (tier-audited)

| # | Source | Tier |
|---|--------|------|
| 1 | hamel.dev/blog/posts/evals/ | B (author's post) |
| 2 | hamel.dev/blog/posts/field-guide/ | B |
| 3 | hamel.dev/blog/posts/evals-faq/what-makes-a-good-custom-interface-for-reviewing-llm-outputs.html | B |
| 4 | hamel.dev/blog/posts/evals-faq/should-i-build-a-custom-annotation-tool-or-use-something-off-the-shelf.html | B |
| 5 | hamel.dev/blog/posts/evals-faq/how-do-i-evaluate-agentic-workflows.html | B |
| 6 | hamel.dev/blog/posts/evals-faq/how-do-i-evaluate-complex-multi-step-workflows.html | B |
| 7 | hamel.dev/blog/posts/evals-faq/ (index) | B |
| 8 | hamel.dev/notes/llm/evals/inspect.html | B |
| 9 | lennysnewsletter.com/p/building-eval-systems-that-improve | C (trade newsletter; authored by Husain and Shankar) |
| 10 | arxiv.org/abs/2404.12272 and /html/2404.12272 (EvalGen) | A |
| 11 | arxiv.org/html/2403.04132 (Chatbot Arena) | A |
| 12 | inspect.aisi.org.uk/log-viewer.html | B |
| 13 | github.com/UKGovernmentBEIS/inspect_ai CHANGELOG.md | B |
| 14 | langfuse.com/docs/evaluation/evaluation-methods/annotation-queues | B |
| 15 | langfuse.com/changelog/2025-03-19-new-trace-view; /2025-03-21-table-peek-view | B |
| 16 | braintrust.dev/docs/guides/evals/interpret; /docs/guides/human-review | B |
| 17 | arize.com/docs/ax/observe/tracing/how-to-tracing-manual/instrumenting-span-types (retriever attributes) | B |
| 18 | eugeneyan.com/writing/aligneval/ | B |
| 19 | humanloop.com/blog/LLM-eval-done-right (Bischof interview transcript) | C |
| 20 | heavybit.com Data Council 2025 foundation-models track write-up | C |
| 21 | manisnesan.github.io/chrestotes/posts/2026-06-04-where-did-it-break.html | D |
| 22 | pytest-html.readthedocs.io/en/latest/user_guide.html | B |
| 23 | github.com/allure-framework/allure2/issues/755; orgs/allure-framework discussions (single-file flag) | D (issue tracker, first-party maintainers) |
| 24 | developer.mozilla.org CSS printing guide | B |

## Gaps / unverified

- Arize Phoenix trace-view and annotation-UI doc pages 404'd (three URLs tried); Phoenix facts here come from the Arize span-attribute reference and the Lenny screenshot description, not Phoenix's own UI docs.
- Langfuse `docs/observability/features/trace-ui` 404'd; trace-view facts rest on two changelog entries.
- Bischof's "Failure is a Funnel" talk video could not be extracted; the stage list (retrieve, select, execute, correct) comes from a search snippet and is unconfirmed against the talk.
- Braintrust human-review keyboard shortcuts are not documented on the fetched page.
- Inspect keyboard bindings are named in the changelog but the specific keys are not published on the log-viewer page.
- No source found on Anthropic-published evaluation viewer notes; Jason Liu searches surfaced only his RAG-eval framing, not a viewer.
- Allure `--single-file` minimum version (2.30.0) comes from a discussion thread, not release notes.
- Whether `print-color-adjust: exact` is honoured by Safari's PDF export was not checked.
