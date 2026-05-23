# LLM Council — Decision Table

When to convene a council vs. use a single model vs. use Gemini Deep Research.

## Quick routing

| Question shape | Tool | Cost | Why |
|---|---|---|---|
| "Help me think through this code change" | Single-model Claude (in-session) | $0 | Code work; council adds noise |
| "Is this PRD missing anything?" | **`llm-council` premium** | $0.30–1 | Four-vendor stress-test surfaces holes one model misses |
| "Draft this cover letter and critique" | **`llm-council` premium** | $0.30–1 | Different RLHF biases → diverse tone critique |
| "Which interpretation of this voice spec is correct?" | **`llm-council` variance** | $0.10–0.40 | Divergence itself is the signal — mid-tier models add variance |
| "What could go wrong with this decision?" | **`llm-council` premium** | $0.30–1 | Each model's blind spot is different; pre-mortem benefits from diversity |
| "Research the landscape for X" | `gemini-deep-research` | $1–7 | Council = peer-review, not research with citations |
| "What's hot on Reddit this week" | `last30days` | $0 | Social conversation, not synthesis |
| "Synthesize 8 papers I've already read" | Single-model Claude | $0 | One model can hold all 8; council adds latency without insight |

## Profile selection

- **premium** — four frontier models, judging flat-out.
  - High-stakes synthesis: job-hunt artifacts, decision pre-mortems, PRD reviews.
  - When you'd rather pay $1 than have the answer be subtly wrong.
  - Members: Claude Opus 4.7 + GPT-5.5 + Gemini Pro + Grok 4.20. Chairman: Opus 4.7.

- **variance** — four models with maximally different RLHF lineages (premium + mid-tier mix).
  - Stylistic/divergence questions: voice modes, prompt-clarity tests.
  - When the *spread* between models is the signal, not their consensus.
  - Cheaper, so usable more frequently.
  - Members: Claude Sonnet + GPT-5.4-mini + DeepSeek v4-pro + Qwen 3.5 Plus. Chairman: Sonnet.

## When NOT to use council

- **Coding tasks.** Claude Code is the venue; council multiplies noise.
- **Anything `skill_optimizer` handles.** That's already a council (Opus generator + Qwen judge + Sonnet sample-check) tuned for SKILL.md.
- **Anything Qwen-local can answer at $0.** Cost discipline matters — don't burn OpenRouter credits on questions a local 14B can field.
- **Daily ops.** Single Claude is fine.

## Cost gates

- Per-query hard caps live in `/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council/council/profiles.py:PROFILES[<name>].max_cost_per_query` ($1.00 premium / $0.40 variance)
- Daily / monthly governors live in `/Users/seanwinslow/Code-Brain/code-brain/tools/llm-council/council/cli.py:_DAILY_CAP_USD` ($7) and `_MONTHLY_CAP_USD` ($40)
- Spend tracked in `/Users/seanwinslow/Code-Brain/code-brain/vault/health/council-spend-{YYYY-MM-DD}.json` (single canonical location across all repos)
- Use `--force` ONLY when Sean explicitly asks (bypasses per-query cap, not daily/monthly)
