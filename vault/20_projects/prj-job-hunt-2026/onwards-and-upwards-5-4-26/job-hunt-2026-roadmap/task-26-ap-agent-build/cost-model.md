# Cost Model — AP Invoice-Approval Agent at 5,000 invoices/month

**Thesis:** at this volume the LLM bill is a rounding error next to the human labor it offsets — so the cost decision isn't "how do we shave tokens," it's "route the cheap work to the cheap tier, and don't fall into the self-host trap before you have the volume to justify it."

All figures are reproducible — run [`cost_model.py`](./cost_model.py) to regenerate the table or re-cost with different assumptions. Prices are **June 2026 published, standard rates** (no batch discount, no prompt caching applied to the headline numbers; both levers are discussed below). Re-verify prices at build time — they move.

## Assumptions

| Assumption | Value | Basis |
|---|---|---|
| Invoices / month | 5,000 | Problem statement (the Meridian scenario) |
| Input tokens / invoice | 3,000 | System policy + instructions + invoice + PO + vendor record |
| Output tokens / decision | 500 | Verdict + structured reasoning trace |
| Classifier output (Haiku first pass) | 300 | Terser routing output |
| Escalation rate (to deeper model) | 5% | The spec's 95/5 auto/escalate target |

These are the levers. They're conservative-to-typical; the calculator makes them one-line edits so the model survives a "what if invoices are bigger?" challenge.

## Pricing (June 2026, per million tokens, standard rates)

| Model | Input | Output |
|---|---|---|
| Claude Opus 4.8 | $5.00 | $25.00 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| Claude Haiku 4.5 | $1.00 | $5.00 |

Self-host reference: AWS **g5.12xlarge** (4× A10G, 96 GB GPU) on-demand **$5.672/hr** (us-east-1) ≈ **$4,140.56/mo** at 730 hr; ~40% less on a 1-year commit. Labor reference: **$5.83/invoice** fully-loaded (APQC cross-industry median).

## The three scenarios

### A) Frontier-only — Opus 4.8 on every invoice
The naive default: best model, every step. Per invoice = (3,000 × $5 + 500 × $25) / 1M = **$0.0275**. Monthly = 5,000 × $0.0275 = **$137.50/mo**.

### B) Hybrid routing — Haiku classifies all, Sonnet deep-passes the 5%
A cheap, fast model reads and triages *every* invoice; only the genuinely ambiguous ~5% get escalated to a mid-tier model for deeper judgment. This is the routing discipline from a real autonomous-agent fleet, applied to AP.
- Haiku on all 5,000: (3,000 × $1 + 300 × $5) / 1M × 5,000 = **$22.50/mo**
- Sonnet on the escalated 250: (3,000 × $3 + 500 × $15) / 1M × 250 = **$4.13/mo**
- **Total = $26.62/mo** ($0.0053/invoice)

### C) Self-host — Llama 3.1 70B on a dedicated GPU instance
No per-token fee, but you rent the GPU whether it's busy or not, plus the engineering to serve, monitor, patch, and stay on-call for it.
- On-demand: $5.672/hr × 730 = **$4,140.56/mo** ($0.8281/invoice)
- Reserved (~40% off): **≈ $2,484/mo** ($0.4969/invoice)
- Plus non-trivial ops/engineering overhead (not in the dollar figure).

## The comparison (verified by `cost_model.py`)

| Scenario | $/month | $/invoice |
|---|--:|--:|
| A) Frontier-only (Opus 4.8) | 137.50 | 0.0275 |
| B) Hybrid (Haiku all + Sonnet 5%) | **26.62** | **0.0053** |
| C) Self-host g5.12xlarge (on-demand) | 4,140.56 | 0.8281 |
| C) Self-host g5.12xlarge (reserved) | 2,484.34 | 0.4969 |
| *(ref) Manual processing @ $5.83* | *29,150.00* | *5.8300* |

## Three findings that matter

**1. Hybrid is 5.2× cheaper than frontier-only — and the multiple is not arbitrary.** It's essentially the **Opus:Haiku price ratio (5:1)**, because 95% of the work runs on the model that's 5× cheaper; the small Sonnet deep-pass softens it slightly. The multiple grows to ~10× if your frontier baseline is Opus *Fast Mode* ($10/$50). The lesson for an interview: *the savings number falls out of the price ratio between the tier you'd default to and the tier the bulk of the work actually needs* — quote it as a ratio, not a magic "10×."

**2. Self-host is a trap at this volume.** A dedicated GPU costs the same whether it processes 5,000 or 500,000 invoices, so at 5,000/mo it's **~30× more expensive than just calling the frontier API** and ~156× more than hybrid. Self-host only breaks even **above ~150,000 invoices/mo vs. frontier and ~780,000/mo vs. hybrid** — 30× and 156× the current volume. It's a high-volume play; recommending it here would be a unit-economics error.

**3. At this scale the model bill is not the decision.** Every API option lands between **$27 and $138/month — 0.1%–0.5% of the ~$29,150/month** in fully-loaded manual labor it offsets. The business case is dominated by **automation rate and avoided fraud**, not token optimization. Pick hybrid because it's good hygiene and it scales, but don't pretend the $110/mo gap between hybrid and frontier is the point. (It *becomes* the point at 100× volume — which is exactly why the routing architecture should be in place from day one.)

## Optimization levers (not applied to the headline numbers)

- **Batch processing — 50% off.** The clean ~95% auto-approvals don't need the <30s SLA (that SLA is for *escalation* routing); they can run as a batch, roughly halving the dominant all-invoice pass. Escalations stay synchronous.
- **Prompt caching — 90% off cached input.** The system policy + instructions are a stable prefix repeated on every call. With ~2,000 of the 3,000 input tokens cached, input cost on every invoice drops sharply — and since input dominates the hybrid bill, caching compounds the hybrid win. (One-line change in the calculator to model it.)
- Together these push hybrid well under $20/mo — but see finding #3: this is optimizing a number that's already negligible.

## Recommendation (full version → build-vs-buy memo, Session D)

**Ship hybrid routing.** It's 5× cheaper than the default, it's the only option whose architecture scales cleanly to 100× volume without a re-platform, and it keeps the cheap tier doing the boring bulk while reserving real judgment spend for the 5% that needs it. **Defer self-host** until sustained volume crosses ~150K/mo — and even then, weigh the ops burden the dollar figure hides. The build-vs-buy memo scores this against managed-platform options.

## Reproducibility & sources

Run `python cost_model.py` to regenerate every figure above. Edit the `ASSUMPTIONS` / `PRICES` blocks to re-cost.

- Claude API pricing (Opus 4.8 / Sonnet 4.6 / Haiku 4.5), June 2026 — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing); corroborated by [finout.io](https://www.finout.io/blog/anthropic-api-pricing) and [benchlm.ai](https://benchlm.ai/blog/posts/claude-api-pricing).
- g5.12xlarge on-demand $5.672/hr — [instances.vantage.sh/aws/ec2/g5.12xlarge](https://instances.vantage.sh/aws/ec2/g5.12xlarge); ~$4,140.56/mo corroborated by [economize.cloud](https://www.economize.cloud/resources/aws/pricing/ec2/g5.12xlarge/).
- Manual cost-per-invoice median $5.83 — APQC via [cfo.com](https://www.cfo.com/news/metric-of-the-month-accounts-payable-cost) (see research reference brief §1).

> ⏱ **Time-sensitive:** all model prices, GPU instance rates, and benchmark figures drift. Re-pull at build/publish time and re-date this section. Llama-70B-on-g5.12xlarge *throughput* (not used in the cost math, which is fixed-instance) is hardware-dependent; the self-host conclusion holds because the instance cost is fixed and volume is low, not because of a throughput estimate.
