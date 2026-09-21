---
title: "Open-weight models per Productcraft seat family — independent-evidence pass (Pass 1, #300)"
date: 2026-09-21
project: productcraft
status: draft
ticket: https://github.com/seanwinslow28/code-brain/issues/300
tags: [research, productcraft, open-models, bench, model-selection]
cost: $0 (web research against primary pages and the OpenRouter /api/v1/models endpoint; no DR or council spend)
models: "research + synthesis: Fable 5.1"
---

# Open-weight models per seat family — findings brief

**Question (Pass 1):** for each Productcraft seat family, which open or open-weight models have *independent* evidence of fitness, what do they cost on OpenRouter, and could any of them run on Sean's own hardware? Trials come later; this pass only ranks who earns a trial.

**Method ($0):** first-party model cards and license files (Hugging Face, GitHub, Z.ai, Moonshot, DeepSeek, Qwen, OpenAI), the OpenRouter models API pulled 2026-09-21 (443 models), and four independent evaluators with published methodology: Artificial Analysis (AA), LMArena, Epoch AI, Aider, plus Vectara's HHEM leaderboard and one peer-reviewed independent run. Every source is tier-audited in the list at the end. Vendor benchmark tables are cited only as vendor claims.

## Findings

1. **The three names Sean hears are the top three open models on every independent board that has scored them — and none of them can run on his hardware.** GLM-5.3 (753B/40B active), Kimi K3 (2.8T/104B) and DeepSeek V4 Pro 0813 (1.6T/49B) need hundreds of gigabytes at 4-bit. They are OpenRouter seats or nothing. The local fleet can only field 27B-dense and small-MoE models, and the independent evidence for those at seat-level work is thin.
2. **GLM-5.3 is the strongest single open candidate for the knowledge-work seats (a, e) and for coding (f).** It ranks #1 open on LMArena text (1483, overall rank 19), tops open models on AA's GDPval-AA v2.1 (Elo 1646) and AA-Briefcase (1525), and beats Kimi K3 on Terminal-Bench 4.0 by 42% to 13%. Its OpenRouter price ($0.91 in / $2.86 out per M) is a third of Kimi K3's.
3. **Kimi K3 is the strongest open candidate for discovery synthesis (b) and the quantitative seat (d).** It leads GLM-5.3 on long-context reasoning (AA-LCR 89% vs 80%), Humanity's Last Exam (47 vs 42), GDP.pdf (22 vs 11) and CritPt (23 vs 19), and posts the highest open LiveBench global score on the mirror I could reach (79.2). It is the priciest open model on OpenRouter ($3 / $15).
4. **For evidence grading (c) the hallucination numbers disqualify DeepSeek V4 Pro and warn against Kimi K3.** On AA-Omniscience, the hallucination rate (wrong answers as a share of non-correct responses) is GLM-5.3 30%, Kimi K3 51%, DeepSeek V4 Pro 0813 95%. A seat whose job is to say "the evidence does not support this" cannot be the model that answers 95% of what it does not know. GLM-5.3 is the only one of the three with a defensible profile, and even it regressed from GLM-5.2's 26%.
5. **A fourth name should enter the trials: Xiaomi's MiMo-V2.6-Pro.** It is #1 open on AA's current Intelligence Index (46, ahead of GLM-5.3's 45) at $0.435 / $0.87 on OpenRouter — the cheapest of the frontier open set by a wide margin. Its model card was unreachable this session, so its parameter count (reported ~1T/42B, MIT) is **unverified** here; the AA score is independent.
6. **Local-route candidates are two: Qwen3.8-27B (dense, Apache 2.0, AA index 34) on the MacBook Pro, and gpt-oss-20b on the RTX 5080.** Neither has independent evidence at the level of the seats above; Qwen3.8-27B's claims (SWE-bench Pro 61.7, Terminal-Bench 2.1 73.0) are vendor-reported. They are candidates for cheap drafting or first-pass audits, not for holding a seat.
7. **No independent benchmark measures seat (e), delivery breakdown, directly, and independent SWE-bench Verified runs for the 2026 open models could not be located.** Both gaps are stated plainly in the section on what the evidence cannot say.

## Seat families — ranked shortlists

### (a) Framing / strategy — Product Strategist, Leadership

What was measured: GDPval-AA (blinded, expert-graded deliverables across 44 occupations including Project Management Specialists, Computer & Information Systems Managers, General & Operations Managers, Financial Managers), AA-Briefcase (four multi-week projects, 91 tasks, domains explicitly include *product management* and *corporate strategy*, rubric + pairwise grading), LMArena text (human pairwise preference, 8.1M votes).

1. **GLM-5.3** — best open on all three: GDPval-AA 1646, Briefcase 1525, LMArena open #1.
2. **Kimi K3** — GDPval-AA 1524, Briefcase 1510; not yet placed on LMArena's main board.
3. **DeepSeek V4 Pro 0813** — GDPval-AA v2 1590 (Aug article; not on the current v2.1 comparison), LMArena 1463.
4. **MiMo-V2.6-Pro** — #1 open on the composite index; no per-eval breakdown seen. Trial on price alone.
5. **Qwen3.8 2.4T-A95B** — open variant of Qwen3.8-Max; not on AA's open board at all this session; custom license. Hold.

### (b) Discovery synthesis — Discovery Lead

What was measured: AA-LCR (long-context reasoning over multi-document sets), GDP.pdf (reasoning over real documents), HLE. Summarization *faithfulness* (Vectara HHEM) exists only for older generations of each family.

1. **Kimi K3** — AA-LCR 89%, GDP.pdf 22, HLE 47; 1M native context; native vision reads interview screenshots and decks.
2. **GLM-5.3** — AA-LCR 80%, GDP.pdf 11; text-only.
3. **DeepSeek V4 Pro 0813** — 1M context; no AA-LCR figure surfaced; hallucination profile (finding 4) makes it a drafter that needs a co-signer, which the Insights seat already is.
4. **GLM-5.3-Flash** (320B/18B, MIT, $0.15 / $0.50) — AA index 42, third open; a cheap synthesis drafter if the seat's evidence is co-signed.

### (c) Evidence grading — Insights & Analytics

What was measured: AA-Omniscience (index from -100 to 100; wrong answers penalised, abstention not), its hallucination rate, and HHEM (summary faithfulness, older models only). No benchmark measures grading the *strength of someone else's evidence*.

1. **GLM-5.3** — Omniscience 14, hallucination rate 30%; the only frontier open model with a usable abstention profile.
2. **Kimi K3** — Omniscience 20 (higher accuracy) but hallucination 51%; it knows more and bluffs more. Acceptable only with a rubric that forces "insufficient evidence" as an allowed verdict.
3. **Qwen3.8-27B / Qwen3 family** — no 2026 AA hallucination figure; Qwen3-32B posted 5.9% on HHEM summarization faithfulness (2025 model). Unproven at this seat.
4. **Not shortlisted:** DeepSeek V4 Pro 0813 (95% hallucination rate), gpt-oss-120b (HHEM 14.2%, Aider 41.8%).

### (d) Structured quantitative / modeling — Business & Economics, Insights

What was measured: SciCode (scientific coding), CritPt (physics reasoning), GDP.pdf, LiveBench global (six categories including math and data analysis; per-category scores not retrievable this session), AA-Briefcase's data-science and banking-operations projects.

1. **Kimi K3** — CritPt 23, SciCode 59, LiveBench 79.2 (mirror).
2. **DeepSeek V4 Pro 0813** — LiveBench 77.4 (mirror); vendor claims LiveCodeBench 93.5, GPQA 90.1.
3. **GLM-5.3** — SciCode 59, CritPt 19, LiveBench 76.1 (mirror).
4. **MiMo-V2.6-Pro** — untested here; cheapest to trial.

No benchmark I found exercises a unit-economics or pricing model in a spreadsheet; the trial will have to.

### (e) Delivery breakdown — epics → stories → sprint plan

What was measured: nothing directly. Closest proxies: AA-Briefcase rubric checks (instruction adherence, evidence use, conflict resolution across multi-week deliverables) and AutomationBench-AA (long-horizon task automation).

1. **GLM-5.3** — Briefcase 1525, AutomationBench 62%.
2. **Kimi K3** — Briefcase 1510, AutomationBench 58% (AA's July article had it at #1 on AutomationBench at 53% before GLM-5.3 shipped).
3. **GLM-5.3-Flash** — cheap enough to draft ten story sets and let the seat audit; evidence is the composite index only.

This is the weakest-evidenced family; rank it by trial results, not this list.

### (f) Planned coding — Devcraft-style

What was measured: Terminal-Bench 4.0 (agentic terminal tasks, run by AA), Aider polyglot (225 Exercism problems in six languages, edit-loop; last updated 2025-11-20 so no 2026 model appears), one peer-reviewed independent build (Potanin, arXiv 2604.17187: five open models on a GH200 building a real React Native app), plus LMArena's Frontend Code Arena (Kimi K3 reported leading at 1,679 — trade-press relay, **unverified**).

1. **GLM-5.3** — Terminal-Bench 4.0 42%, best open by a wide margin; vendor DeepSWE 66.9.
2. **DeepSeek V4 Pro 0813** — Aider lineage is the strongest independent open record (DeepSeek-V3.2 Reasoner 74.2% at $1.30 per run, the top open entry); V4 Pro itself has no Aider run.
3. **Kimi K3** — Terminal-Bench 4.0 13% is anomalous next to its other scores and next to Kimi K2.5's win in the Potanin build (best of five at 3-bit); treat as a harness question to test, not a verdict.
4. **MiMo-V2.6-Pro** — vendor DeepSWE 72.6 (trade-press relay); AA index leader; no coding sub-score seen.
5. **Qwen3.8-27B** (local-capable) — vendor SWE-bench Pro 61.7; the only coding candidate that fits the MacBook Pro.

## Candidate table

Prices are OpenRouter's listed rate on 2026-09-21 (`/api/v1/models`); they vary by provider and the `:batch` / `:free` variants are cheaper. Local-fit assumes Q4_K_M GGUF (~0.55–0.6 GB per billion params) plus KV cache; RTX 5080 = 16 GB VRAM; MacBook Pro = M4 Max 48 GB unified (~40 GB usable); Mac Mini = M4 Pro 24 GB.

| Model | Params (total / active) | Context | License | OR $/M in / out | RTX 5080 16 GB | MBP 48 GB | Notes |
|---|---|---|---|---|---|---|---|
| GLM-5.3 | 753B / 40B MoE | 1M (OR lists 1.3M) | GLM-5.3 License: commercial OK; MaaS >$10B/yr revenue needs Z.ai security review | 0.91 / 2.86 | No (~420 GB) | No | Text only |
| GLM-5.3-Flash | 320B / 18B MoE | 1M | MIT | 0.15 / 0.50 | No (~180 GB) | No | Multimodal |
| Kimi K3 | 2.8T / 104B MoE (896 experts, 16 active) | 1M | Kimi K3 License: commercial OK; MaaS >$20M/12mo needs separate agreement; UI attribution >100M MAU or >$20M/mo | 3.00 / 15.00 | No (~1.5 TB at native MXFP4) | No | Native vision |
| DeepSeek V4 Pro 0813 | 1.6T / 49B MoE | 1M | MIT | 0.66 / 1.98 | No (~900 GB native FP4/FP8) | No | |
| DeepSeek V4.1 Flash | 552B / 8B prefill, 16B decode | 1M | MIT (per DeepSeek news page) | 0.15 / 0.60 | No (~300 GB) | No | AA index 39 |
| MiMo-V2.6-Pro | ~1T / 42B MoE (**unverified**; card 401'd) | 1M | MIT (**unverified**; V2.5-Pro card is MIT) | 0.435 / 0.87 | No | No | AA index 46, #1 open |
| Qwen3.8 2.4T-A95B | 2.4T / 95B MoE | 1M | Custom Qwen3.8-Max license (thresholds at 100M MAU / $20M-mo; MaaS $50M TTM) | 2.00 / 6.00 | No | No | Not on AA open board |
| Qwen3.8-27B | 27B dense (Gated DeltaNet hybrid) | 262K native, 1M YaRN | Apache 2.0 | 0.42 / 3.00 | Partial: Q4_K_M ~16.5 GB spills; Q3_K_M ~13 GB fits with short context | **Yes** (~17 GB + KV) | AA index 34 |
| Qwen3.6-27B | 27B dense | 262K | Apache 2.0 | 0.30 / 2.00 | Partial (as above) | **Yes** | Already benchmarked on Mini per Topic 20 |
| Qwen3.6-35B-A3B | 35B / 3B MoE | 262K | Apache 2.0 | 0.15 / 1.00 | Offload (24 GB) | **Yes** (current MBP model) | No AA seat-level evidence |
| MiniMax M3 | 428B / 23B MoE | 1M | minimax-community | 0.30 / 1.20 | No (~240 GB) | No | AA index 29; vendor SWE-V 80.5 |
| Nemotron 3 Ultra | 550B / 55B hybrid Mamba-MoE | 1M | OpenMDW-1.1 (no thresholds) | 0.60 / 2.40 (`:free` exists) | No (~300 GB NVFP4) | No | AA index 23 |
| gpt-oss-120b | 117B / 5.1B MoE | 131K | Apache 2.0 | 0.15 / 0.60 | No (~61 GB MXFP4) | No (marginal at 48 GB) | Aider 41.8%, HHEM 14.2% |
| gpt-oss-20b | 21B / 3.6B MoE | 131K | Apache 2.0 | 0.03 / 0.13 | **Yes** (~13 GB, OpenAI states 16 GB) | Yes | No seat-level evidence |
| Kimi K2.6 | 1T / 32B MoE (K2 lineage) | 262K | Modified MIT | 0.95 / 4.00 | No | No | LMArena open #7 (1460); HHEM 10.8% |

Prices for GLM-5.3 and Kimi K3 quoted by AA from first-party APIs are higher ($1.40 / $4.40 and $3 / $15); the OpenRouter figure is what Sean would pay through the fleet's route.

## What the evidence cannot tell us

- **Seat (e) has no benchmark.** Nothing independent scores turning a strategy into epics, stories and a sprint plan. AA-Briefcase's rubric checks are the nearest proxy and they grade a different deliverable.
- **Evidence grading is not factual recall.** AA-Omniscience measures whether a model bluffs on facts it does not hold. Grading the strength of interview evidence is a different skill; the hallucination rate is a necessary filter, not a proof of fitness.
- **Index versions moved under the models.** AA's v4.1 index scored GLM-5.3 and Kimi K3 at 60 and DeepSeek V4 Pro 0813 at 53; the current v4.3.2 (harder agentic evals) scores them 45, 44 and 36. Any number quoted from the summer is on a different scale from any quoted now. This note uses v4.3.2 unless stated.
- **No independent SWE-bench Verified run for any 2026 open model was found.** Epoch publishes its methodology (barebones scaffold, 484 samples, no network) but the score table did not render; swebench.com's table did not render; the SWE-bench experiments repository shows no 2026 open-model submissions. Aider's board stopped at 2025-11-20. Terminal-Bench 4.0 via AA is the only independent agentic-coding number for the current generation, and Kimi K3's 13% there may be a harness artefact.
- **LiveBench per-category scores (data analysis, instruction following) were not retrievable**; the global scores cited come from a mirror (llm-stats), which is a C-tier relay of an A-tier benchmark.
- **MiMo-V2.6-Pro's card and Nemotron 3 Ultra's NVIDIA card returned 401/403.** Their AA scores are independent; their parameter and license figures here are from secondary pages and marked unverified.
- **Vendor tables dominate the local-route story.** Qwen3.8-27B's SWE-bench Pro 61.7 and Terminal-Bench 2.1 73.0, Qwen3.6-27B's SWE-bench Verified 77.2, MiniMax M3's SWE-bench Verified 80.5, and every DeepSeek card figure are the vendor's own harness. Nothing independent places a 27B model at seat level.
- **Quantization is untested for these seats.** The local-fit column is arithmetic, not a measurement; the one peer-reviewed data point (Kimi K2.5 at 3-bit outperforming its 4-bit self on a real build) says quantization effects are not monotone, so a local trial must be run at the quant it would ship at.
- **Prices drift.** A search snippet and the API dump disagreed on gpt-oss-120b the same day; the table uses the API.

## Decisions requested (Sean)

1. Confirm the trial roster: GLM-5.3, Kimi K3, DeepSeek V4 Pro 0813 and MiMo-V2.6-Pro via OpenRouter; Qwen3.8-27B on the MacBook Pro as the sole local challenger.
2. Confirm that hallucination rate is a hard filter for the Insights seat (rules DeepSeek V4 Pro out of that seat before trials).
3. Confirm seat (e) is trialled without a benchmark prior, ranked only by the trial's own rubric.

## Sources (tier-audited)

**A — academic / peer-reviewed**
- GDPval paper, arXiv 2510.04374 (Oct 2025): 220 gold tasks, 44 occupations, blinded expert pairwise grading, 14-year average expert experience. — A
- LiveBench paper, arXiv 2406.19314 (ICLR 2025 Spotlight): six categories, monthly refresh, contamination-limited. — A
- Potanin, "React-ing to Grace Hopper 200," arXiv 2604.17187 (Apr 2026): five open coding models on a GH200, real multi-file build; Kimi K2.5 at Q3 best of five. — A
- DeepSeek-V4 technical report, arXiv 2606.19348. — A (vendor-authored; architecture only)

**B — primary (model cards, licenses, first-party pricing, independent leaderboards with published methodology)**
- OpenRouter `https://openrouter.ai/api/v1/models`, pulled 2026-09-21 (443 models; all prices and context lengths in the table). — B
- huggingface.co/zai-org/GLM-5.3 model card and LICENSE file (753B, glm_moe_dsa, $10B MaaS security-review clause). — B; its benchmark table — C
- huggingface.co/zai-org/GLM-5.3-Flash (320B/18B, MIT). — B
- github.com/MoonshotAI/Kimi-K3 and huggingface.co/moonshotai/Kimi-K3 LICENSE (2.8T/104B, MXFP4, $20M MaaS and 100M-MAU attribution clauses). — B; benchmark table — C
- huggingface.co/deepseek-ai/DeepSeek-V4-Pro (1.6T/49B, MIT, FP4/FP8). — B; benchmark table — C
- deepseek.com/en/news/deepseek-v4-1-flash (552B, 8B/16B active, MIT), via search relay. — B/C
- huggingface.co/Qwen/Qwen3.8-27B and Qwen/Qwen3.6-27B (27B dense, Apache 2.0, 262K native). — B; benchmark tables — C
- huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro (1.02T/42B, MIT) via search relay; MiMo-V2.6-Pro card unreachable. — B (V2.5), unverified (V2.6)
- huggingface.co/MiniMaxAI/MiniMax-M3 (428B/23B, minimax-community license). — B; benchmarks — C
- huggingface.co/openai/gpt-oss-120b and openai.com/index/introducing-gpt-oss (117B/5.1B and 21B/3.6B, Apache 2.0, MXFP4, 80 GB / 16 GB). — B
- docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b (550B/55B, OpenMDW-1.1) via search relay; build.nvidia.com card unreachable. — B
- artificialanalysis.ai/models/open-source (Intelligence Index v4.3.2 open ranking: MiMo-V2.6-Pro 46, GLM-5.3 45, Kimi K3 44, GLM-5.3-Flash 42, DeepSeek V4.1 Flash 39, DeepSeek V4 Pro 0813 36, Qwen3.8-27B 34, MiniMax M3 29, Nemotron 3 Ultra 23). — B
- artificialanalysis.ai/models/comparisons/glm-5-3-vs-kimi-k3 (per-eval numbers: Briefcase, GDPval-AA v2.1, AutomationBench, Terminal-Bench 4.0, SciCode, HLE, GDP.pdf, CritPt, Omniscience, AA-LCR, speed, verbosity). — B
- artificialanalysis.ai/models/glm-5-3, /kimi-k3, /deepseek-v4-pro (specs, first-party prices, release dates). — B
- artificialanalysis.ai/evaluations/omniscience and /evaluations/aa-briefcase (metric definitions; Briefcase domains include product management and corporate strategy). — B
- artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-1 (weights: GDPval-AA 20%, Terminal-Bench 16%, etc.). — B
- artificialanalysis.ai articles: Kimi K3 launch (2026-07-17: index 57 on v4.1, GDPval-AA 1668, hallucination 51%, $0.94/task); GLM-5.2 open-weights lead (2026-06-16: GLM-5.2 hallucination 28.1%); GLM-5.3 note relayed via search (2026-08-18: hallucination 30%, Omniscience 14); DeepSeek V4 Pro 0813 note relayed via search (GDPval-AA v2 1590, hallucination 95%). — B (search-relayed items B/C)
- arena.ai/leaderboard/text?license=open-source (2026-09-13, 8.1M votes: glm-5.3-max 1483 #19 overall, glm-5.3-flash 1475, deepseek-v4-pro-high 1463, kimi-k2.6 1460). — B
- aider.chat/docs/leaderboards (polyglot, last updated 2025-11-20; DeepSeek-V3.2 Reasoner 74.2% top open; gpt-oss-120b 41.8%; Llama 4 Maverick 15.6%). — B
- epoch.ai/benchmarks/swe-bench-verified and /aider-polyglot (methodology only; score tables did not render). — B
- github.com/vectara/hallucination-leaderboard (HHEM, 2026-05-11: GLM-5 10.1%, Kimi K2.6 10.8%, DeepSeek V3.2 6.3%, Qwen3-32B 5.9%, gpt-oss-120b 14.2%, Llama-3.3-70B 4.1%). — B
- github.com/SWE-bench/experiments evaluation/verified listing (no 2026 open-model submissions visible). — B
- Repo: agents-sdk/docs/plans/2026-05-21-topic-20-fleet-model-refresh-benchmarks-plan.md (MBP M4 Max 48 GB, Mac Mini M4 Pro 24 GB, local GGUF sizes). — B

**C — trade press / vendor marketing / mirrors**
- interconnects.ai "The current balance of power in open models" (2026-09-21; Nathan Lambert's reading of the AA open board; 2–5 month open-vs-closed lag). — C (informed commentary)
- llm-stats.com/benchmarks/livebench (mirror: Kimi K3 79.2, DeepSeek V4 Pro 77.4, GLM-5.3 76.1; DeepSeek-V4-Pro-Max 0.736) and llm-stats.com/blog/research/qwen3-8-max-open-weights (2.4T/95B, custom license). — C
- venturebeat.com Kimi K3 license piece; siliconangle.com DeepSeek V4.1-Flash release; orcarouter.ai MiMo-V2.6-Pro (1T/42B, MIT, DeepSWE 72.57); runaihome.com / kingy.ai GLM-5.3 GGUF and hardware notes; localaimaster.com LMArena Frontend Code Arena claim (Kimi K3 1,679). — C, all unverified where marked
- Vendor benchmark tables on every model card above (GLM-5.3 DeepSWE 66.9 / Terminal-Bench 2.1 88.2; Kimi K3 GPQA 93.5 / DeepSWE 67.5; Qwen3.8-27B SWE-bench Pro 61.7; Qwen3.6-27B SWE-bench Verified 77.2; MiniMax M3 SWE-bench Verified 80.5; DeepSeek V4 Pro LiveCodeBench 93.5). — C

**D — forum / social**
- x.com/ArtificialAnlys posts relayed in search (GLM-5.3 index 60 on v4.1; DeepSeek V4 Pro 0813 index 53) — D as posts, though they restate B-tier AA data.
