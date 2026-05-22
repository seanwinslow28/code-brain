---
type: research-report
date: 2026-05-21
question: "Topic 18 — Pi + ChatGPT Codex subscription integration in 2026. How to plug an existing ChatGPT Plus / Codex subscription into Pi (auth, supported model IDs, hybrid workflows, subscription limits, comparison vs direct OpenAI API key)."
topic: 18
source: chatgpt-manual
tier: dr
tags: [research, deep-research, pi.dev, openai-codex, chatgpt-manual]
---

# Auth modes

Pi supports both ChatGPT subscription (Codex) login and OpenAI API keys. In interactive mode you can run `/login` and choose “ChatGPT Plus/Pro (Codex)”【4†L123-L130】. This opens a browser OAuth flow to authenticate your ChatGPT Plus/Codex account. Once logged in, Pi stores a ChatGPT (Codex) session token (via the `openai-codex` provider) and uses that for subsequent calls【16†L108-L116】. (This matches OpenAI’s guidance that Codex can “sign in with ChatGPT for subscription access”【10†L667-L675】.) Pi also accepts an OpenAI API key by setting `OPENAI_API_KEY` in the environment or in `~/.pi/agent/auth.json`【4†L169-L172】. In other words, Pi lets you use your ChatGPT Plus/Codex subscription (via OAuth login) or a standard OpenAI API key. It does *not* currently support a separate “service account” or enterprise Codex access token flow – those are only for enterprise automation【10†L716-L724】. There is no special “Codex CLI key”; you simply use the same OpenAI login or API key. 

# Supported model IDs

When using the ChatGPT/Codex login, Pi’s built‑in **openai‑codex** provider exposes the new GPT‑5 series models. As of early 2026, Pi lists these Codex models: **GPT-5.2**, **GPT-5.3-Codex** and **Codex Spark**, **GPT-5.4**, **GPT-5.4-mini**, and **GPT-5.5**【26†L558-L564】. (These correspond to the Codex-recommended models in OpenAI docs【33†L669-L678】【33†L694-L702】.) All of those models have very large context windows (roughly 272K tokens in the Pi catalog) and support Codex features. In practice, `openai-codex/gpt-5.5` is the full flagship model for heavy coding tasks; `gpt-5.4-mini` is a faster, smaller variant; and the 5.3 models are earlier generations. (Note: names like “gpt-5.5-codex” or “gpt-5.5-thinking” are not separate IDs – the model is simply `gpt-5.5` under the Codex provider.) All of these models support tool use (code editing, `bash`, etc.) and *vision* input (they accept images in prompts) just like other GPT-5 models. In short, under the Codex login Pi can use GPT-5.5, 5.4(-mini), 5.3-Codex, and 5.2, all with the full Codex capabilities【26†L558-L564】【33†L669-L678】. 

# Hybrid workflows

Yes – Pi can mix providers within one session. You can configure Pi to use one model/provider for code writing and another for higher‑level tasks. For example, Pi’s JSON config lets you specify different models for different subtasks. A common pattern (as in community recipes) is to set the main model under the `openai-codex` provider and use an Anthropic or Gemini model for planning or review. For instance, a `~/.pi/agent/config.json` might look like:

```json
{
  "model": "openai-codex/gpt-5.5",
  "thinking": "medium",
  "summary": {
    "enabled": true,
    "model": "openai/gpt-5.4-mini",
    "thinking": "low"
  }
}
```

This example (from a Pi extension) routes the main agent to GPT-5.5 via Codex and uses plain `openai` (API-key mode) for summarization【34†L140-L148】. You could analogously replace `"openai/gpt-5.4-mini"` with an Anthropic model (e.g. `"anthropic/claude-sonnet-4-0"`) or a Gemini model by prefixing with `anthropic/` or `google/`. In effect, Pi will call Codex for code generation (`openai-codex/...`) and fallback to the other provider for planning or review. The config format is just `"provider/model"` (e.g. `"anthropic/claude-3-sonnet-4"`) with an optional `"thinking"` level. If the chosen model isn’t available, Pi automatically falls back to the current model【34†L153-L161】. 

# Subscription limits inside Pi

When you sign in with ChatGPT Plus/Codex, Pi’s requests count against your Codex usage quotas. In practice, *the same limits apply as if you were using the Codex CLI or cloud*. That means your Codex tasks (via Pi) use up your ChatGPT/Codex message budget. For example, a Plus/Pro plan might allow on the order of a few dozen Codex conversations per 5-hour window (see OpenAI’s Codex usage dashboard【41†L368-L372】 for exact numbers). Pi itself does not show your remaining quota; it will simply begin returning 429 “rate limit” errors if you hit the limit (as the `pi-codex-image-gen` docs note, you’ll see a 429 and should retry later【16†L181-L184】). To check your remaining Codex allowance, you need to use OpenAI’s Codex usage dashboard (or run the Codex CLI’s `/status` command)【41†L368-L372】. In short, Pi doesn’t magically bypass the 50-per-3h or weekly caps – it *inherits* the same consumption limits of your ChatGPT plan, and you monitor them through OpenAI’s tools rather than inside Pi.

# vs. direct OpenAI API key

- **Cost:** Using ChatGPT Plus/Codex auth means you pay a fixed subscription ($20/mo for Plus, which includes Codex) with a usage cap, versus paying per token with an API key at published rates. If you have a Plus/Pro plan, you essentially pre‑pay for some amount of Codex usage each billing period, whereas an API key charges you $ (or credits) per token used【10†L701-L709】. In other words, subscription mode is effectively “bundled” usage, API mode is pay-as-you-go.  
- **Rate limits:** API access is limited by tokens/sec or QPS (e.g. ~60 requests/minute) and your account token quota, while ChatGPT/Codex auth is limited by the user-plan quotas (dozens of sessions per hour as above). Pi will hit the same ChatGPT plan limits when using subscription.  
- **Features:** Both modes support the same GPT-5.x models, with vision and tool use. Codex (subscription) mode may have slightly higher priority or “fast mode” (as OpenAI notes, some speed-optimized features like Codex’s *fast mode* are only enabled when using ChatGPT sign-in)【10†L707-L709】. In practical terms, you get identical modeling capabilities either way.  
- **What’s missing under subscription:** The subscription path can’t access the OpenAI API’s fine-tuning or new function-calling endpoints directly (those require API keys). It also can’t generate traditional API “request IDs” or receipts. Conversely, the API key route doesn’t give you the Codex app UI or fast-mode priority. Also, if you have private data compliance needs (e.g. no data retention), the subscription mode follows your ChatGPT workspace rules (per OpenAI)【10†L679-L687】. 

# Working config

In Pi you generally configure the provider/model in a JSON settings file. For example, to use ChatGPT Plus (Codex login) for code and a fallback to Anthropic for planning, your `~/.pi/agent/config.json` might look like this:

```json
{
  "model": "openai-codex/gpt-5.5",
  "thinking": "medium",
  "plan": {
    "model": "openai-codex/gpt-5.5-thinking",
    "thinking": "fast"
  },
  "fallback": {
    "model": "anthropic/claude-sonnet-4-0",
    "thinking": "low"
  }
}
```

In this snippet, the main agent uses `openai-codex/gpt-5.5` (using your ChatGPT login), and the “plan” or subtask also uses the GPT-5.5 Thinking mode. If that fails or is inappropriate, it falls back to an Anthropic Claude model via `anthropic/claude-sonnet-4-0`. (The actual Pi schema is flexible – the key idea is to use `provider/model` strings. See e.g. the [pi-subagent-review extension example](#Hybrid-workflows) where they specify `"model": "openai-codex/gpt-5.5"` and a summary model in another provider【34†L140-L148】.) 

# Sources

- Pi Coding Agent documentation (latest) – Providers and authentication methods【4†L123-L130】【2†L169-L173】  
- Pi model catalog – list of built-in models by provider【26†L558-L564】  
- Pi extensions/examples – configuration snippets for multi-provider workflows【34†L140-L148】  
- OpenAI Codex documentation – ChatGPT vs API sign-in and features【10†L667-L675】【10†L707-L709】  
- OpenAI Codex pricing/help – ChatGPT/Codex usage limits and dashboard【41†L368-L372】  
- Pi package docs (`pi-codex-image-gen`) – notes on ChatGPT login and rate-limit behavior【16†L108-L116】【16†L181-L184】 (accessed 2026-05-21)