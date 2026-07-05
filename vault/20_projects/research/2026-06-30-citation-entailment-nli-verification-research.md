---
title: "Citation verification via NLI entailment — local-model cost model & mechanism for the E1 VERIFY gate"
date: 2026-06-30
project: fusion-discovery-council
feature: E1 (entailment gate v2 for the core VERIFY stage)
status: complete
tags: [research, nli, entailment, citation-verification, fusion-discovery-council, discovery-step-d]
method: deep-research skill ($0, Anthropic subscription) — 5 angles, ~30 sources fetched, per-finding confidence + sources below
---

# E1 research — entailment-based citation verification & the local-NLI cost model

**Decision this informs:** today `verify.py::quote_supported_at_url(cited_quote, fetched_text) -> bool`
is **substring containment**. E1 upgrades it in place to **atomic-claim decomposition + NLI
entailment** (does the source *entail* the claim, not merely contain a substring?) and reports
**citation precision + recall**. The open fork (left for Sean to confirm): the entailment-scorer
cost model — **(a) local NLI** (DeBERTa/MiniCheck/AlignScore/HHEM — $0 recurring, fleet's local
spine) · **(b) OpenRouter LLM-judge per claim** (recurring API $ — the cost trap) · **(c) subscription
agent** (interactive-only).

**Recommendation the evidence supports: (a) local NLI, run IN-PROCESS (no Ollama server).** The
decisive finding (Angle 5): a pre-built **173 MB int8 ONNX** for `cross-encoder/nli-deberta-v3-small`
runs in the calling Python process via onnxruntime — **no model host to be asleep/unreachable**, which
eliminates the fleet's documented intermittent-local-host failure mode *and* costs $0 recurring.
Option (b) is the cost trap and is rejected; (c) can't gate a headless pipeline. The only sub-choice
left is *which* local model — see "How this should shape the build."

---

## Findings (per-finding confidence + sources)

### Angle 1 — Local NLI / fact-consistency models that can run on Apple Silicon

- **`cross-encoder/nli-deberta-v3-small` — 100M params, Apache-2.0, ships a 173 MB int8 ONNX
  (`onnx/model_qint8_avx512_vnni.onnx`) runnable in-process on CPU via onnxruntime; MNLI-mm 87.55.**
  No server, no asleep-host risk. (HIGH) — https://huggingface.co/cross-encoder/nli-deberta-v3-small/tree/main
- **Vectara `HHEM-2.1-Open` — flan-t5-base (~110M), Apache-2.0, <600 MB RAM on CPU, ~1.5 s for a
  2k-token input; purpose-built for RAG faithfulness (premise/hypothesis → 0–1).** (HIGH) —
  https://huggingface.co/vectara/hallucination_evaluation_model
- **MiniCheck family (EMNLP 2024) — Flan-T5-Large 770M (MIT), plus sub-1B RoBERTa/DeBERTa variants;
  GPT-4-level fact-checking at ~400× lower cost; available via Ollama.** Bespoke-MiniCheck-7B is
  commercial/non-open. (HIGH) — https://github.com/Liyan06/MiniCheck , https://arxiv.org/abs/2404.10774
- **AlignScore (ACL 2023) — RoBERTa base 125M / large 355M; standard transformers checkpoint.** Older,
  beaten by MiniCheck. (HIGH) — https://github.com/yuh-zha/AlignScore
- **Not locally viable: Bespoke-MiniCheck-7B (commercial), Patronus Lynx-70B (70B), Luna (Galileo
  proprietary, no open weights).** (HIGH / MEDIUM on Luna's closed status) — https://arxiv.org/abs/2407.08488

### Angle 2 — Atomic-claim decomposition: cheapest reliable path

- **For a *cited-passage* entailment task (source in hand), naive sentence-splitting is the documented,
  GPT-4-competitive decomposition** — MiniCheck and Bespoke both operate at `(document, sentence)→[0,1]`
  and explicitly recommend "break the claim into sentences" as the decomposition step. $0, no LLM per
  claim. (HIGH) — https://github.com/Liyan06/MiniCheck , https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B
- **The expensive ceiling is LLM-based decomposition** — FactScore uses a paid LLM (InstructGPT,
  ~$1/100 sentences) and human experts still re-split 18% / merge 34% of its atomic facts; Claimify
  (Microsoft 2025) is multi-LLM-call-per-sentence. Decomposition method *measurably shifts* scores
  (Wanner, StarSEM 2024), so it isn't neutral — but that risk is documented mainly for *source-free*
  long-form factuality, not grounded cited-passage entailment. (HIGH) — https://arxiv.org/abs/2305.14251 ,
  https://arxiv.org/abs/2403.11903
- **If call-count must drop without a paid LLM-per-claim, chunk-level extraction (FaStfact 2025) is
  O(N/w) — but still uses an LLM. Pure $0 decomposition = sentence-splitting.** (HIGH) — https://arxiv.org/html/2510.12839

### Angle 3 — Citation precision/recall: the ALCE definitions + a realistic accuracy target

- **ALCE (EMNLP 2023) is the canonical "citation precision/recall" framing, computed reference-free by
  an NLI model φ:** *recall* = 1 iff concat(cited passages) entails the statement; *precision* uses the
  remove-one-citation test (a citation is "irrelevant" iff it alone doesn't support AND the remaining
  citations still entail). Drop-in local φ replaces ALCE's T5-11B. (HIGH) — https://arxiv.org/abs/2305.14627
- **Realistic local-φ accuracy: ~72–75% balanced accuracy on LLM-AggreFact — within ~0.6 pts of GPT-4.**
  MiniCheck-FT5 74.7, MiniCheck-DeBERTa 72.6, AlignScore 70.4, GPT-4 75.3. (HIGH) — https://arxiv.org/html/2404.10774
- **HHEM-2.1-Open (110M) beats GPT-4 on the specific consistency benchmarks: AggreFact 76.55,
  RAGTruth-QA 74.28.** Small-model factual-consistency checking is genuinely viable, not a compromise.
  (HIGH) — https://huggingface.co/vectara/hallucination_evaluation_model
- **LettuceDetect-large (396M ModernBERT) hits ~79% response-F1 / ~59% span-F1 on RAGTruth, beating a
  finetuned Llama-2-13B at ~30× smaller** — a defensible ceiling reference. (HIGH) — https://arxiv.org/html/2502.17125v1
- **Eval-harness shape:** a set of labeled `(claim, source-context, supported?)` triples scored as
  binary classification; report **balanced accuracy** (class-imbalanced) or ALCE-style reference-free
  precision/recall. (HIGH)

### Angle 4 — Substring as a cheap pre-filter (the load-bearing architecture constraint)

- **"verbatim substring ⇒ ACCEPT; else ⇒ NLI" is recall-preserving ONLY IF every substring-miss falls
  through to NLI and substring NEVER triggers a reject.** Substring is high-precision / low-recall:
  exact verbatim ≈ near-certain accept, but absence of substring ≠ unsupported (real citations
  frequently paraphrase). (HIGH) — https://arxiv.org/abs/2304.09848
- **Lexical/token-overlap trails NLI by ~18 ROC-AUC points on factual consistency (TRUE: token-match
  ~63.8 vs ANLI-NLI ~81.5)** — substring-ALONE would systematically false-negative paraphrased support.
  (HIGH; exact decimals MEDIUM — verify against TRUE Table 3 if cited in the spec) — https://arxiv.org/abs/2204.04991
- **Cheap-filter→expensive-NLI cascades are a validated production pattern** (FEVER's TF-IDF→NLI;
  HaluGate's token-detector→NLI-on-residual). Note the direction: here substring is the *precision/fast-accept*
  stage and NLI is the *recall* stage — the opposite of HaluGate — so the recall guarantee comes
  entirely from "100% of substring-misses go to NLI." (HIGH) — https://arxiv.org/pdf/1811.10971 , https://vllm.ai/blog/2025-12-14-halugate

### Angle 5 — In-process vs Ollama-server (the actual integration decision)

- **In-process ONNX/transformers eliminates the asleep-host failure mode.** onnxruntime/transformers
  load the model into the *calling* process — no daemon to be unreachable. Cost: ~173 MB int8 (or
  ~568 MB fp32) into the process's RAM + a one-time cold-start load per fresh process. (HIGH, architectural)
- **Smallest viable in-process verifier: `nli-deberta-v3-small` via its pre-built 173 MB int8 ONNX on
  onnxruntime, CPU-only.** Even smaller if needed: `nli-MiniLM2-L6-H768` (82M) or `nli-deberta-v3-xsmall`
  (70.8M) — but you'd export/quantize those yourself. (HIGH) — https://huggingface.co/cross-encoder/nli-deberta-v3-small
- **Latency (indicative, MEDIUM — search-aggregated, not card-verified): ~241 pairs/sec / ~4 ms per pair
  on CPU; int8 ONNX ≈ 3× faster than PyTorch CPU.** Sub-second for typical claim batches. Cold-start =
  one model load per process (no verified exact number — LOW). — https://sbert.net/docs/cross_encoder/usage/efficiency.html
- **Do NOT rely on Apple MPS for these encoders — unimplemented-op errors are documented; CPU (PyTorch
  or int8 ONNX) is the reliable path.** For a ~100M model CPU is plenty fast. (HIGH) — https://github.com/huggingface/sentence-transformers/issues/1564

---

## How this should shape the E1 build

1. **Cost model = (a) local NLI, in-process.** $0 recurring, consistent with the fleet's local spine,
   and — uniquely — the in-process ONNX path removes the asleep-host failure mode that an Ollama-served
   model (or the existing Tier-C pattern) would reintroduce. (b) per-claim LLM-judge rejected (cost
   trap); (c) subscription rejected (can't gate a headless pipeline).
2. **Model — Sean's sub-choice (recommend the first):**
   - **`cross-encoder/nli-deberta-v3-small` int8 ONNX, in-process (RECOMMEND).** 173 MB, Apache-2.0,
     no server, ~4 ms/pair CPU. Strongest "no new failure mode" story.
   - **Vectara `HHEM-2.1-Open` (alt).** Purpose-built RAG-faithfulness scorer, beats GPT-4 on the exact
     consistency benchmarks, <600 MB CPU — pick this if we want a faithfulness-native 0–1 score over a
     generic 3-label NLI head.
   - MiniCheck-Flan-T5-Large (770M, MIT) if we want max open accuracy and can absorb ~1.5 GB fp16.
3. **Decomposition = naive sentence-splitting ($0).** Adequate and GPT-4-competitive for grounded
   cited-passage entailment; avoid LLM-per-claim decomposition (the cost trap in disguise).
4. **Architecture = substring pre-filter → NLI cascade, with a hard invariant:** substring may only
   *add* fast accepts; **every substring-miss must go to NLI; substring must never reject.** This keeps
   the cheap fast-path while NLI owns recall on paraphrased support. Keep substring exactly as the
   current cheap containment check.
5. **Report ALCE-style citation precision + recall**, computed by the local φ (reference-free). Realistic
   accuracy of the local φ itself ≈ 72–75% balanced accuracy (≈ GPT-4 on this task); set the eval target
   there, not at 100%.
6. **Build discipline:** hermetic unit tests mock the NLI scorer (no live model in the unit suite — or a
   tiny fixture); gate the real model behind a lazy in-process loader so cold-start is paid once.

### Lower-confidence / verify-before-citing
- Exact CPU latency (~241 pairs/sec) and cold-start time are indicative, not card-verified.
- TRUE token-match vs NLI decimals (63.8 / 81.5 / 86.4) are directionally robust across two retrievals;
  eyeball TRUE Table 3 before quoting exact numbers in the spec.
- MiniCheck per-variant param counts and exact on-disk sizes not individually card-verified.
