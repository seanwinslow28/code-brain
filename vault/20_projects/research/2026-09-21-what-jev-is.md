---
title: "What Jev is — TypeSafe AI's System One model, and where it could sit in the studios (issue #301, pass 2)"
date: 2026-09-21
project: productcraft
status: draft
ticket: https://github.com/seanwinslow28/code-brain/issues/301
tags: [research, productcraft, systemcraft, devcraft, designcraft, jev, typesafe, runtime-registry]
cost: $0 — web reads only; the product's API was not called
models: "research and synthesis: Fable 5.1"
---

# What Jev is — findings brief

**Question (pass 2 of #301):** what is "Jev", from its own docs first; what is its API surface; what has anyone measured beyond launch week; and where, honestly, could it fit in a Productcraft or Systemcraft train, in Designcraft or Devcraft, and what would a first real test be.

The docs site resolves cleanly: `docs.typesafe.ai` is the documentation of **TypeSafe AI**, whose first and only model is **Jev** (`jev-1.13.0`). Everything below is tier B unless marked.

## Findings summary

1. **Jev is a hosted, non-generative decision model, not an LLM and not a harness.** One endpoint, `POST /v1/systemone`: a `state` (text or JSON) plus a map of typed questions in, one typed answer per question out — a `choice` with a probability distribution, a `score` on a rubric, or a `noul` (a 0–1 yes/no). It does not write text, code or rationales [S3, S9]. The docs say outright it is "**not** a drop-in replacement for the LLM behind Claude Code" [S9].
2. **The company came out of stealth 2026-09-15 with a $40M seed led by DCVC**; CEO Diogo Almeida was at OpenAI on RLHF/InstructGPT [S13, S14, S15]. Access is waitlisted early access; Sean has a key.
3. **The API surface is small and well-typed**: 64K tokens per request (32K for `state`), 255 options per Choice, 2–10 levels per Score, `usage {input_tokens, output_tokens}` on every response, $0.042 per million input tokens and output free, 1,200 rpm / 250K tok/s, no streaming, no tool calling, hosted only, also reachable through OpenRouter and Vercel AI Gateway [S3, S4, S10].
4. **Independent evidence exists and is unusually good for a one-week-old product** — five reproducible GitHub evals with raw data, one pre-registered. The pattern: strong zero-shot on semantic classification (83–96%), roughly tied with a frontier LLM at 1/100–1/300 of the cost and 2–3× the speed at the client, **but calibration does not survive out-of-distribution or unanswerable questions**, and single broad questions underperform decomposed ones [S20–S25].
5. **Fit:** no seat, no gate, no co-sign. The only honest Productcraft slot is the ladder's **rung 2 judge for `overclaimed-pointer`**, which is not yet earned (1 coded fail, 8 defects, 33 labels). The strongest fit is **Devcraft**: a typed tool-call risk Noul in a PreToolUse hook, which is exactly what one independent benchmark measured [S24]. Designcraft: weak — text-only, no images.

## 1. What Jev is, in its own words

**Class.** "System One models are a class of AI models built to make fast, structured decisions that software can use directly. A System One model evaluates a state and returns typed answers and probabilities." "System One models do not write replies, produce code, or generate explanations of their reasoning." The name is Kahneman's fast/intuitive System 1 [S2]. Jev is "the first System One model"; the name is from the Jevons paradox [S18, tier C].

**"Typesafe."** The docs never define the word. The nearest primary statement is the primer's "Machine Native Intelligence: AI with software-like properties such as structure, reliability, observability, testability, speed, consistency, and low cost" [S11], and the launch post's framing: "a frontier-intelligence function call: unstructured state in, typed probabilistic decisions out," with type-safety "mathematically guaranteed" because the answer space is the schema you supplied — so "hallucination" in the structured-output sense is impossible by construction. That is a claim about *form*, not correctness; the docs are careful: "Calibration is measured across groups of predictions; it does not guarantee that an individual answer is correct" [S2, S12].

**Architecture and training.** The launch post says non-autoregressive sampling (all answers in one parallel pass) and a training method it calls **Reinforcement Learning for Calibrated Decisions (RLCD)**, described in the primer as training the model "to return decisions and calibrated probabilities instead of generated text," where "outcomes assigned a probability of 0.2 should occur about 20% of the time" [S11, S12]. No model card, no paper, no parameter count, no base-model disclosure anywhere primary. Wikipedia's "transformer-based, synthetic data only" is tier C and unverified [S18]. The GitHub org carries forks of LLaDA (a diffusion LM) and vLLM — suggestive of the inference stack, nothing more [S16].

**Who.** TypeSafe AI, San Francisco; founders Diogo Almeida (CEO; the team page says Google Brain and co-inventor of RLHF/InstructGPT, the press release says OpenAI), Sasha Sheng (COO, ex-Meta/FAIR), Erik Gafni (CTO) [S13, S14]. Founded 2024 per press and TechCrunch's "two years ago" — the company's own site does not state a founding year [S14, S17]. Forbes's $200M valuation is cited only second-hand [S18, unverified].

## 2. The API surface

| Facet | What the docs say | Source |
|---|---|---|
| Endpoint | `POST https://api.typesafe.ai/v1/systemone`, `Authorization: Bearer <key>`; body `{state, model, questions}` | [S3] |
| `state` | `string \| object \| array`; text only, "Images, audio, and video are not supported (yet)"; English best, CJK "not equally well" | [S3, S4, S7] |
| Question types | `noul` (optional `criteria.true/false`); `choice` (`criteria` map, **max 255 options**); `score` (ordered `criteria` array, **2–10 levels**). `instructions` may itself be an object holding the question plus data it references | [S3] |
| Answers | `noul: 0–1`; `choice` + `probabilities` (sum to 1) + `confidence`; `score` (probability-weighted, can land between levels) + `legend` + `probabilities` + `confidence`. "Every answer is independent." | [S3, S5] |
| `confidence` | A statistic of the distribution's peakedness, 0–1; for a Choice the docs' explorer computes `(n·peak − 1)/(n − 1)`; Noul carries none; "never locked into our definition" — raw probabilities are returned | [S6] |
| Meter | `usage: {input_tokens, output_tokens}` on every response; the SDK types both as `int \| None` "when the API did not report it" | [S3, S10] |
| Limits | `jev-1.13.0`: "64k tokens per request; 32k tokens for `state` plus the longest question"; 250,000 tokens/s and 1,200 requests/min; aliases `jev-latest` (default) and `jev-preview` (identical today) | [S4] |
| Price | "$42 per billion" = **$0.042 / MTok input; output tokens are free**; the homepage's "238× cheaper than Fable 5.1" is a vendor ratio | [S1, S4] |
| Errors / retries | 401, 422 (validation, names the field), 429, **529 Overloaded**; SDK `RetryPolicy(max_retries=2, backoff 0.5→5.0s, jitter 0.25, statuses {408, 429, 5xx}, respect_retry_after=True)` | [S3, S10] |
| Streaming / tools | **Not found in primary sources** — nothing to stream, no tool calling; it is not generative | [S3, S9] |
| SDKs | Python ≥ 3.10 (`typesafe-sdk`, pydantic since 0.7.0, `response_model=` for typed responses, first public release 0.5.7 on 2026-09-14); TypeScript (`typesafe-sdk-js`); Vercel AI SDK 7 `evaluate()` | [S10, S16, S19] |
| Gateways | OpenRouter `~typesafe/jev-latest` via `base_url="https://openrouter.ai/api"`; Vercel AI Gateway `typesafe-ai/jev` — both must follow TypeSafe's OpenAPI spec, not chat completions | [S10, S19] |
| Hosting | Hosted only; no self-host, on-prem or weights mentioned anywhere | [S1–S4] |
| Data | Privacy policy (dated 2025-11-19): "We will not train or fine tune any … models on your prompts or other Input"; inputs disclosed only to service providers; **no fixed retention period** ("as long as reasonably necessary"). The public terms are website terms; no API terms of service were found | [S8] |
| Agent skill | `claude plugin marketplace add typesafe-ai/skills` + `claude plugin install typesafe@typesafe-ai` — teaches an agent to *write code that calls Jev*, nothing else | [S9, S16] |

**Known limits the vendor publishes** ("jaggedness", reviewed 2026-09-17 [S7]): literal reading ("answers the question you wrote, not the one you meant"); no arithmetic, counting or numeric representations ("Jev is not a calculator"); dates read as text; indirection and double negatives; accuracy "falls as the state grows with content unrelated to the decision" ("context rot"); "State is data, and `jev-1.13` does not treat it as hostile by default" — adversarial content "can move the answer"; contradictory instructions vs criteria; no structural invariants (the same yes/no as a Noul and as a Choice gave 0.22 vs 0.01; a question and its negation summed to 1.19); and generation ("there are other models for that").

## 3. Independent evidence

**What the maker measured (tier C, its own workflows).** `evals.typesafe.ai` runs four TypeSafe-authored workflows (security incidents, agent-trace observability, invoice processing, customer service). Four-workflow average: **Jev 67.8% accuracy, $0.0004/case, 0.4s**, against Opus 5 (workflow) 73.1% / $0.1761 / 37.8s, Sonnet 5 67.8% / $0.1174 / 78.1s, GPT-5.6 Sol 74.1% / $0.0836 / 23.3s, Terra 67.9% / $0.0304 / 10.1s. Reference labels are "an average of the responses of GPT-6 Astra and Claude Fable 5.1" at high reasoning while "all other models are evaluated using the provider's default reasoning settings" — so the headline 193.6× / 444.6× ratios are the best case on tasks the vendor designed, with vendor-chosen comparators [S12, S26]. DataCamp's reading, not hands-on, adds that TypeSafe "can't prove the pricing isn't subsidized" [S27, tier C].

**What others measured (tier C, independent, raw data on GitHub).**

- **priorbench/jev** [S20] — 2026-09-20, via OpenRouter, **50 predictions pre-registered**, 5,721 calls, 21 experiments, $0.176. 95.9% zero-shot on a 400-item classification set vs 77.2% keyword rules and 66.0% supervised TF-IDF+LR. Latency floor ~430 ms at the gateway; 800 judgments in one call in 985 ms. Calibration: accuracy flat from 0.50 to 0.95 confidence, 100% only at 0.99 — "gate at 0.99 or not at all." The model always answers: a cake recipe was classed a technical issue at 0.94. 26/50 predictions confirmed, 21 falsified.
- **scienthoon/jev-ood-calibration** [S21] — 2026-09-19, 900 rule-generated tickets + 3 public benchmarks. Public sets 86–94% with ECE 0.024–0.032; synthetic tickets 75% with **ECE 0.107 vs a 0.024 noise floor (4.4×)**. Choice and Score overconfident (temperature refit 3.3–3.4), boolean underconfident (0.66). On labels the text cannot contain, it assigned 0.74 probability at 44.7% accuracy — "confidently wrong" off-distribution. Reproducible for ~$0.06.
- **ickma2311/jev-baselines-eval** [S22] — 2026-09-18, pre-registered. Banking77: Jev 0.832, gpt-5.4-nano 0.793, GPT-5.6 Terra 0.875, **supervised encoder 0.933**. CLINC150: Jev 0.870, nano 0.795, Terra 0.915. Verdict "AMBIGUOUS" on both; confidence-ranking AUROC mixed with CIs spanning zero; client latency 0.43s vs 0.92s for nano — "the vendor's 40–200× speed claim does not describe this comparison."
- **anisselbd/jev-phishing-bench** [S23] — 2026-09-17, 2,000 synthetic emails vs Claude Haiku 4.5. **One broad question: Jev 62.6% vs Haiku 81.3%** (p<0.0001). **Five decomposed signals + logistic regression: 95.0% vs 93.2%** (tied; Haiku higher AUROC). ECE 0.154 vs 0.097. p50 239 ms vs 687 ms; $0.038 vs $0.462 per 1,000. Label flips across two passes 2.2% vs 0.7%.
- **webofmike, agent tool-call risk** [S24] — 2026-09-20, 60 hand-labeled calls (readonly / destructive / privileged / exfiltration): 91.7% overall, 100% on clear cases, 71.4% on ambiguous; **every wrong answer carried confidence below 1.000**. No LLM baseline; n too small to separate.
- **14-TR/jev-empirical** [S25] — staged protocol, 101/101 on authored diagnostics (author calls it a ceiling effect); "a well-typed answer is not necessarily correct."

**Trade press (tier C).** The Register carries no independent verification [S17a]. TechCrunch (2026-09-18) quotes Vercel's Pranit Sharma replacing Luna 5.6 with Jev for command-safety classification at 5–18× the speed, and Armin Ronacher's caution that a 50% answer "maybe … is a coin toss"; no TechCrunch measurement [S17]. A "TypeSafe employee measured 15.9%" piece [S28, tier D, no primary link] refers to one decision step of a DSPy pipeline swapped to Jev: 1.16× end-to-end, cost per ticket −30.1% — the pipeline-level number, which is the one that matters for a train.

**The buzz, characterized.** What the videos and posts demonstrate is real-time control on structured text state: TypeSafe's own Doom demo at ~10 decisions/s and ~$7/hour; community Minecraft (~1¢ per two minutes), Subway Surfers, a drone course, a driving sim; plus browser agents, a live trading loop and email triage [S17a, S29, S30]. None of these is a reasoning task; all are "pick one of N from a fed state, fast." The two YouTube videos found could not be read (page shell only) [S31, tier D, unverified]. "Fastest-adopted model in AI Gateway history" appears only in a secondary outlet [S32, tier D, unverified]; Vercel's own changelog restates the vendor's 193.6×/444.6× and nothing about adoption [S19].

## 4. Fit

**(a) Productcraft / Systemcraft train — no seat, no gate, no co-sign, one future slot.** A seat pass reads a corpus and writes a markdown artifact; a co-sign or audit writes a check record with a verdict line, findings, "what was attacked and held" and a loopback message [S33]; a gate writes findings. All three are generative by definition, and the vendor says so [S7, S9]. The trace kit's record fields (`meter`, `wall_clock_s`, `## Corpus read`) are facts the coordinator writes, not judgments, and rung 0 is deterministic "with no model" by law [S34] — a model there would be a regression. "Co-sign transcription" is string-copying a verdict line into a field; it needs a regex, not a model.

The one honest slot is the **evals ladder's rung 2**: "a judge per recurring failure mode, validated against Sean's labels before it gates anything," earned at 30–50 labels per class [S34, S35]. Of the two coded modes, `overclaimed-pointer` — "a citation or status claim says more than its source holds" — is a one-hop, literal, source-in-state question, which is Jev's best shape and is literally the vendor's *Double-checking citations* cookbook (find the quote in the source, then a Noul on "does the source support the claim", human confirms below 0.8) [S36]. `unobservable-measure` needs the pilot's own rules as context — indirection, the vendor's mode 4 — and is a poor fit. **Today the slot is not earned**: 1 coded fail and 8 distinct defects across 33 labels [S35]. Jev changes nothing about that rule; it only changes what the judge could cost when the rule is met (cents per engagement, and a probability instead of a rationale, which is the right shape for a judge whose TPR/TNR is reported against Sean's labels).

Adjacent and already real: the fusion-discovery council's VERIFY stage, which drops any pain point "not traceable to a real fetched URL," is the same citation-check shape on existing session logs.

**(b) Designcraft and Devcraft.** Designcraft: weak. Jev is text-only [S4]; the design-team agents review layout, contrast and motion from code and screenshots. It could score text-described token compliance, but the Design System Enforcer already does that as a read-only subagent, and a Choice over token names is not the hard part of that review.

Devcraft: the strongest fit in the whole set, and it maps onto a rule already in CLAUDE.md — "Hooks enforce; subagents judge." A PreToolUse hook that must answer allow/deny in well under a second is the one place in Sean's stack where "typed decision, 100–500 ms, calibrated-ish probability, no prose" is the specification rather than a compromise. The independent tool-call risk benchmark [S24] is that use case, and the vendor's own use-case map names "detect tool-call errors," "model routing," "reasoning trace classification" and "semantic lints … in CI" [S37]. Two caveats travel with it: the vendor admits state "does not treat [content] as hostile by default" [S7], so a guard that reads attacker-influenced tool arguments is exactly where mode 6 bites; and scienthoon's finding that Jev is confident on questions the state cannot answer means a hook must gate on the vendor-recommended "act / confirm / escalate" bands with thresholds set from Sean's own labels, never from a doc example [S6, S21].

**(c) A first real test, no throwaway.** Both candidates run on inputs that already exist and leave a kept artifact.

1. **Devcraft shadow guard (recommended first).** A PreToolUse hook that sends every Bash/Edit call's command and cwd as `state` to one Choice (`readonly | destructive | privileged | exfiltration`) plus one Noul ("would a careful engineer want to be asked before this runs?"), **logs the answer and never blocks**, exit 0 always. Cost at $0.042/MTok is ~$0.00002 per call [S4, S24]. After a week the log is a labeled dataset of Sean's real tool calls against his own eventual verdicts — the first thirty labels the ladder needs, gathered on live traffic, in the Husain order (hand-read first). It is not throwaway because the log is the Devcraft guard's design input either way.
2. **Rung-2 calibration read for `overclaimed-pointer`.** Replay pc-eng-001's co-sign evidence rows (the five bounced at co-sign and the ones that passed) through the citation-check pattern against the frozen evidence files, and compare Jev's Noul to the check records' verdicts [S33, S35, S36]. Tens of calls, cents. Written up as an eval note under `evals/`, not as a trace pass — a judge that has not earned its rung never touches `labels.md`. It answers the only question that matters for the slot: does Jev's probability separate the bounced rows from the passed ones on *this* corpus.

Not a first test: any seat, any gate, and anything that needs the number Jev cannot produce (counts, dates, arithmetic — modes 2 and 3).

## What the sources cannot tell us

- What Jev *is* under the hood: no model card, paper, parameter count or base model. "Non-autoregressive" and "RLCD" are vendor descriptions; the LLaDA and vLLM forks are circumstantial.
- Whether the $0.042 price is sustainable; the vendor's own evals page does not say, and DataCamp's "subsidized" remark is a reading, not a disclosure.
- Native-API latency: every independent number came through OpenRouter or Vercel, so the ~430 ms floor cannot be attributed to the model.
- Retention period for API inputs (the policy gives none) and whether any API-specific terms exist beyond the website terms.
- Whether Vercel's free promotion and end date, and the "fastest adopted" claim, are real — both surfaced only in secondary snippets.
- Anything about seat-quality: no source tried Jev on a reasoning, drafting or critique task, because it cannot do one.

## Decisions requested (Sean)

1. Rule Jev **out of the runtime registry (#286)** as a seat runtime — it cannot carry a pass — and record that ruling on #301 so the question does not come back with the next video.
2. Approve the **Devcraft shadow guard** as the first real test (log-only PreToolUse hook, live traffic, no blocking), with the log kept as Devcraft design input.
3. Decide whether the **rung-2 calibration read** on pc-eng-001's co-sign rows is worth cents now, or waits until `overclaimed-pointer` reaches the 30-label floor per the ladder's own rule.

## Sources (tier-audited: A academic · B primary · C trade · D forum)

- [S1] B — TypeSafe AI homepage, typesafe.ai (v0.01 page; "$42 per billion input tokens"; "238× cheaper than Claude Fable 5.1").
- [S2] B — docs.typesafe.ai/concepts/system-one (System One definition; "do not write replies, produce code, or generate explanations"; calibration caveat; Kahneman note).
- [S3] B — docs.typesafe.ai/api (endpoint, request/response schema, 255-option and 2–10-level limits, `usage`, error table).
- [S4] B — docs.typesafe.ai/models (`jev-1.13.0`, aliases, 64K/32K context, 250K tok/s, 1,200 rpm, $0.042/MTok, output free, text-only, language note).
- [S5] B — docs.typesafe.ai/primitives (+ /primitives/choice, /score, /noul; "Every answer is independent").
- [S6] B — docs.typesafe.ai/confidence (derived statistic; Noul has none; three-band pattern; thresholds scale with risk).
- [S7] B — docs.typesafe.ai/model-jaggedness/jev-1.13 (nine failure modes, reviewed 2026-09-17).
- [S8] B — typesafe.ai/legal/privacy-policy (no training on Input; service-provider disclosure; no fixed retention; dated 2025-11-19); typesafe.ai/legal/terms (website terms only).
- [S9] B — docs.typesafe.ai/introduction/coding-agents ("**not** a drop-in replacement for the LLM behind Claude Code"); docs.typesafe.ai/agent-skill.
- [S10] B — docs.typesafe.ai/sdk/python/usage, /sdk/python/api/retries, /sdk/python/api/types/responses, /sdk/python/changelog, /sdk/javascript/api/interfaces/Usage (SDK shape, `RetryPolicy` defaults, gateway `base_url` examples, `Usage` typing).
- [S11] B — docs.typesafe.ai/introduction/machine-learning-primer (RLCD; calibration definition; "Machine Native Intelligence").
- [S12] B — TypeSafe AI blog, "Introducing System One Models & Jev," Diogo Almeida, 2026-09-15 (non-autoregressive; RLCD; 70–500 ms; 193.6× / 444.6×; "hallucination-free" by schema; text-only; waitlist).
- [S13] B — typesafe.ai/team (founders and prior affiliations; San Francisco; investors unnamed).
- [S14] B — Business Wire press release via Morningstar, "TypeSafe AI Emerges From Stealth With $40M in Funding," 2026-09-15; DCVC, "TypeSafe emerges from stealth," dcvc.com (lead investor's own post).
- [S15] B — GitHub org typesafe-ai: `skills` (MIT), `typesafe-sdk-python`, `typesafe-sdk-js`, `system-one-adapter-python` ("Drop-in TypeSafeClient replacement backed by LLM APIs," for comparing Jev with an LLM), forks of LLaDA and vLLM.
- [S16] B — github.com/typesafe-ai/skills README and docs quick start (plugin install commands).
- [S17] C — TechCrunch, Tim Fernholz, "A new kind of AI model from a ChatGPT inventor is thrilling developers," 2026-09-18 (Sharma/Vercel, Mudholkar/Bryo, Ronacher quotes; no TechCrunch measurement).
- [S17a] C — The Register, Thomas Claburn, "TypeSafe AI debuts model for machines that plays Doom," 2026-09-16 (demo figures 0.114 s vs 8.566 s; no independent verification).
- [S18] C — Wikipedia, "Jev (AI model)" (tertiary; founding 2024, Forbes $200M valuation, Jevons naming, "transformer-based, synthetic data" — all unverified against primary).
- [S19] B — Vercel changelog, "TypeSafe AI's Jev now available on AI Gateway," 2026-09-16 (`typesafe-ai/jev`, native `evaluate()` API, restates vendor ratios; no adoption or pricing claim on the page itself).
- [S20] C (independent, pre-registered, raw JSONL published) — github.com/priorbench/jev, 2026-09-20.
- [S21] C (independent, raw responses published) — github.com/scienthoon/jev-ood-calibration, 2026-09-19.
- [S22] C (independent, pre-registered) — github.com/ickma2311/jev-baselines-eval, 2026-09-18.
- [S23] C (independent, reproducible) — github.com/anisselbd/jev-phishing-bench, 2026-09-17; summarized by beri.net, 2026-09-20 (C).
- [S24] C — dev.to/webofmike, "I Benchmarked Jev on Agent Tool-Call Risk. Calibration Held.", Mike Moore, 2026-09-20 (n=60, no LLM baseline).
- [S25] C — github.com/14-TR/jev-empirical, TR Ingram, staged protocol (ceiling-effect diagnostics).
- [S26] C (vendor-run, vendor-authored workflows) — evals.typesafe.ai, "Workflow Evals," four-workflow table and reference-label methodology.
- [S27] C — DataCamp, Matt Crabtree, "Jev: TypeSafe's System One Model That Never Hallucinates," 2026-09-16 (not hands-on; "no large-scale independent reproduction has surfaced yet").
- [S28] D (no primary link; unverified) — The Cherry Creek News, "TypeSafe Claims Its Model Is 193.6x Faster. Its Own Employee Measured 15.9%…," 2026-09-21.
- [S29] C — MindStudio, "Jev AI Plays Minecraft, Subway Surfers, and Drives Cars: Demos Reviewed," 2026-09-18 (community demos, author did not run them).
- [S30] C — flaviocopes.com/jev (hands-on, updated 2026-09-21); dev.to/valyuai, "How to Use Jev," 2026-09-17 (hands-on guide; both restate vendor ratios as ceilings).
- [S31] D (unverified — pages returned only the YouTube shell) — youtube.com/watch?v=CcmqPS6q9Gw "I tried TypeSafe's System One Model: Jev"; youtube.com/watch?v=QKafJHkYrRE.
- [S32] D (unverified) — Startup Fortune, "Jev Becomes Vercel's Fastest Adopted Launch"; search snippet naming a Vercel free promotion ending 2026-09-25.
- [S33] B (local) — productcraft/templates/check-record.md; productcraft/trace/record-template.md.
- [S34] B (local) — productcraft/trace/README.md (rung 0 "deterministic checker with no model"; ladder order).
- [S35] B (local) — productcraft/trace/taxonomy.md (rung 1 codes and pc-eng-001 counts; "Rung 2 … No judge exists and none is earned").
- [S36] B — docs.typesafe.ai/cookbooks/citation_check ("Double-checking citations": quote-find, then a Noul on support, human confirms below 0.8).
- [S37] B — docs.typesafe.ai/concepts/use-case-map (harness use cases: routing, tool-call error detection, semantic lints in CI).
- C (not relied on) — LangChain blog "Building a harness with Jev" (conceptual, no measurement); MindStudio launch explainer; runtimewire.com on an unreleased "semantic lint" console feature (sourced to a reverse-engineer's X post, D); SiliconANGLE, HPCwire, Dealroom restating the press release.
