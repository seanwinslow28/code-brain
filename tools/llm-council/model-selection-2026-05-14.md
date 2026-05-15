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

Maximally different RLHF lineages — divergence between models is the point. Mix of premium + mid-tier across four distinct training organizations (Anthropic, OpenAI, DeepSeek, Alibaba). Used for voice-mode calibration, prompt-clarity tests, anywhere the spread is the signal.

| Role | Model ID | Per-1k input | Per-1k output | Context |
|---|---|---|---|---|
| Council 1 | `~anthropic/claude-sonnet-latest` | $0.003 | $0.015 | 1,000,000 |
| Council 2 | `openai/gpt-5.4-mini` | $0.00075 | $0.0045 | 400,000 |
| Council 3 | `deepseek/deepseek-v4-pro` | $0.000435 | $0.00087 | 1,048,576 |
| Council 4 | `qwen/qwen3.5-plus-20260420` | $0.0003 | $0.0018 | 1,000,000 |
| **Chairman** | `~anthropic/claude-sonnet-latest` | $0.003 | $0.015 | 1,000,000 |

**Estimated per-query cost:** ~$0.12 (same shape as premium estimate)

**Per-query hard cap:** **$0.40** (~3.3× typical)

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
| `qwen/qwen3.5-plus-20260420` | Alibaba | Western-influenced multilingual, Chinese lab | Second Chinese lineage but distinct from DeepSeek; high context, different long-context behavior |

Two Western + two Chinese, two dense + one MoE + one MoE-equivalent. Synthesis chairman is Sonnet because (a) Sean reads Sonnet output fluently and can spot Sonnet artifacts, (b) Anthropic synthesis is the established baseline, (c) it's already on the panel so no extra wire call.
