# LLM Council Model Selection — 2026-05-14

**Pricing snapshot:** [`openrouter-models-snapshot-2026-05-14.json`](openrouter-models-snapshot-2026-05-14.json) (captured 2026-05-14 from `https://openrouter.ai/api/v1/models`)

All prices in USD per token. To convert to per-1k: multiply by 1000.

## Premium profile

Frontier-only, judging flat-out. One model per major Western lab (Anthropic / OpenAI / Google / xAI). Used for high-stakes synthesis: cover letters, decision pre-mortems, PRD stress-tests, role-fit memos.

| Role | Model ID | Per-1k input | Per-1k output | Context |
|---|---|---|---|---|
| Council 1 | `anthropic/claude-opus-4.7` | $0.005 | $0.025 | 1,000,000 |
| Council 2 | `openai/gpt-5.5` | $0.005 | $0.030 | 1,050,000 |
| Council 3 | `~google/gemini-pro-latest` | $0.002 | $0.012 | 1,048,576 |
| Council 4 | `x-ai/grok-4.20` | $0.00125 | $0.0025 | 2,000,000 |
| **Chairman** | `anthropic/claude-opus-4.7` | $0.005 | $0.025 | 1,000,000 |

**Estimated per-query cost:** ~$0.29 (typical voice-mode-calibration shape: 2k input × 4 fan-out + 2.5k input × 4 cross-rank + 8k chairman; outputs 1.5k / 0.5k / 2k)

**Per-query hard cap:** **$1.00** (~3.5× typical, leaves headroom for 5k-input PRDs)

## Variance profile

Maximally different RLHF lineages — divergence between models is the point. Mix of premium + mid-tier across four distinct training organizations (Anthropic, OpenAI, DeepSeek, Mistral). Used for voice-mode calibration, prompt-clarity tests, anywhere the spread is the signal.

| Role | Model ID | Per-1k input | Per-1k output | Context |
|---|---|---|---|---|
| Council 1 | `~anthropic/claude-sonnet-latest` | $0.003 | $0.015 | 1,000,000 |
| Council 2 | `openai/gpt-5.4-mini` | $0.00075 | $0.0045 | 400,000 |
| Council 3 | `deepseek/deepseek-v4-pro` | $0.000435 | $0.00087 | 1,048,576 |
| Council 4 | `mistralai/mistral-medium-3-5` | $0.0015 | $0.0075 | 262,144 |
| **Chairman** | `~anthropic/claude-sonnet-latest` | $0.003 | $0.015 | 1,000,000 |

**Estimated per-query cost:** ~$0.14 (same shape as premium estimate; up from ~$0.12 after the Qwen → Mistral swap on 2026-05-16)

**Per-query hard cap:** **$0.40** (~2.9× typical)

## Combined gates

- **Daily circuit breaker:** **$7.00** across both profiles combined
- **Monthly governor:** **$40.00** across both profiles combined
- **Spend tracking files:** `vault/health/council-spend-{YYYY-MM-DD}.json` (daily) and `vault/health/council-spend-{YYYY-MM}.json` (monthly aggregate computed from daily files)
- **Override:** `--force` flag bypasses per-query cap only; daily and monthly caps are NEVER bypassed

## Headroom at chosen caps

At $7/day combined:
- 7 premium runs/day, OR
- 17 variance runs/day, OR
- mixed: 5 premium + 5 variance

At $40/month combined:
- ~40 premium-equivalents/month
- Aligns roughly with the gemini-deep-research $20/month observed spend pattern

## Profile-routing rule

- **premium** for stakes/synthesis (job-hunt artifacts, decision pre-mortems, PRD reviews) — pay $0.30 to ensure the answer isn't subtly wrong
- **variance** for stylistic/divergence (voice-mode calibration, prompt-clarity tests) — divergence between four lineages IS the signal

## Refresh cadence

Re-run the catalog query weekly:

```bash
curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $(grep ^OPENROUTER_API_KEY .env | cut -d= -f2)" \
  > tools/llm-council/openrouter-models-snapshot-$(date +%Y-%m-%d).json
```

If any selected model's `pricing.prompt` or `pricing.completion` changes by **>20%**, alert Sean and adjust caps. If a selected model is removed from the OpenRouter catalog (e.g., deprecated), pick a replacement from the same vendor at the same tier and re-run this decision doc.

## Lineage rationale (variance panel)

Why these four for "maximally different RLHF":

| Model | Org | Training lineage | Why included |
|---|---|---|---|
| `~anthropic/claude-sonnet-latest` | Anthropic | Constitutional AI + heavy RLHF, US | Strong synthesizer baseline; the "house" voice |
| `openai/gpt-5.4-mini` | OpenAI | RLHF-tuned for efficiency, US | Different RLHF flavor than Anthropic; OpenAI's compressed-capability tier |
| `deepseek/deepseek-v4-pro` | DeepSeek | Mixture-of-experts, Chinese lab | Different geography + architecture; trained on different post-training data |
| `mistralai/mistral-medium-3-5` | Mistral | European multilingual, dense, French lab | Third Western RLHF flavor distinct from both Anthropic and OpenAI; dense (no reasoning-trace blowout) so reliable inside the 120s client timeout; strong literary register adds creative-writing variance |

Three Western + one Chinese, three dense + one MoE. Synthesis chairman is Sonnet because (a) Sean reads Sonnet output fluently and can spot Sonnet artifacts, (b) Anthropic synthesis is the established baseline, (c) it's already on the panel so no extra wire call.

## Swap history

### 2026-05-16: Qwen 3.5 Plus → Mistral medium-3-5

**Trigger:** Two consecutive production failures of `qwen/qwen3.5-plus-20260420` on real prompts (MBP voice-mode-calibration run 2026-05-15; Mac Mini Substack-first-post run 2026-05-16). Both Stage-1 fan-outs surfaced Qwen in `dropped_models`.

**Diagnosis:** Direct probes against the OpenRouter `chat/completions` endpoint confirmed Qwen 3.5 Plus is **alive and responding** to small prompts, so the failure isn't deprecation or rate-limiting. It's a **reasoning-token timeout**: Qwen 3.5 Plus emits a multi-hundred-token internal `reasoning` trace before producing visible `content`. On a 4k-token creative prompt the reasoning trace blows past the OpenRouter+Alibaba serving latency budget and exceeds the council client's 120s timeout. Same probe behavior reproduced on `z-ai/glm-4.7` (Zhipu) and `minimax/minimax-m2` — they are also reasoning models with smaller but qualitatively-similar bloat. Production-scale probe (real Substack prompt, 4751 input tokens) showed:

- `mistralai/mistral-medium-3-5`: **14.9s wall, 0 reasoning chars, 736 output tokens** — matches the response profile of Sonnet/GPT-5.4-mini/DeepSeek (the three working panelists)
- `z-ai/glm-4.7`: 93.4s wall, 8,429 reasoning chars, 2,916 output tokens — survived this run but at 78% of the timeout boundary, structurally fragile

**Decision:** Replace Qwen with Mistral medium-3-5. Accepts a shift from the original "2 Western + 2 Chinese" geographic-balance design to "3 Western + 1 Chinese," reasoning that **structural reliability matters more than geographic balance for the variance panel's actual purpose** (producing four distinct drafts the chairman can synthesize from). A panelist that intermittently fails contributes zero variance; a reliable European panelist adds genuine third-Western-lineage spread between Anthropic's Constitutional flavor and OpenAI's efficiency-tuned RLHF.

**Cost delta:** Typical per-query estimate shifts from ~$0.12 → ~$0.14 (Mistral input is 5× Qwen's; output is 4×). Per-query hard cap unchanged at $0.40; daily $7 and monthly $40 governors unchanged.

**Open question for re-evaluation:** When Qwen 3.5 Plus or a Qwen successor stops emitting heavy reasoning traces on long prompts (e.g., a non-thinking-mode SKU), reconsider re-adding it as a 5th model or as Mistral's replacement to restore the 2W+2C balance.
