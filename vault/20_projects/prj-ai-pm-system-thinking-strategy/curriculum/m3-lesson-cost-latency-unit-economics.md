# M3 — Cost, Latency & Unit Economics as System Variables (Lesson)

*Module 3 of 7 · Systems Thinking AI PM program · Week 2*
*Prerequisites: M1 (stocks/flows, balancing loops), M2 (drift, reward hacking).*

## Why this module exists

This module was absent from the first curriculum draft, and a four-model review called that the single biggest gap — because in 2026 this is table-stakes AI PM work. Deterministic software has near-zero marginal cost per request; AI products have a *meter running on every call*. That one difference rewires product economics: cost is now a system variable with its own loops, and quality, latency, and cost form a triangle where pushing one corner moves the others. PMs who can't reason about this triangle ship products that are either too slow, too expensive, or quietly getting worse.

## 1. The cost-quality-latency triangle

For any LLM-backed feature, three variables trade against each other:
- **Quality**: bigger/frontier models answer better — and cost more and run slower.
- **Latency**: users feel response time; every quality-improving addition (bigger model, more retrieval, more verification passes) adds milliseconds to seconds.
- **Cost**: tokens in, tokens out, per call, forever. Volume multiplies everything.

The triangle is a *constraint*, not a dial you set once: load, prompt growth, and context accumulation shift the balance continuously. The PM job is to decide, per feature, which corner is protected, which corner flexes, and what the *floor* on the flexing corners is — written down, before launch.

## 2. Cost loops: the meter as a system

Model the money in M1 terms. Spend is a flow; budget is a stock; every architectural choice adds loops:

- **Uncapped reinforcing loops are how bills explode.** An agent that retries on failure, a loop without a stop condition, a feature whose usage grows with its own success — each is a reinforcing loop on the spend flow. A loop with no cap is "a billing machine": target, budget, and stall conditions must be *written into the system*, not held in someone's head.
- **Cost caps are balancing loops — design them like products.** A good cap doesn't just stop spend; it degrades gracefully (fallback model, queued work, honest error) and *tells someone*. A cap that silently drops work converts a cost problem into a trust problem.
- **The routing trap.** Model routing — sending easy requests to cheap models, hard ones to frontier models — reliably cuts bills 40–85%. But the failure mode is systemic and delayed: "The bill goes down, the quality goes down with it, and you find out from customer tickets two or three days later." Routing without a quality-regression alarm is a fixes-that-fail archetype: the fix (cheaper model) works instantly; the side-effect (quality drain) arrives after a delay, on a different dashboard, owned by a different team.
- **Caching is a loop-breaker.** Semantic caching (returning stored answers for semantically similar queries) can absorb 60–85% of calls in repetitive workloads — it removes calls from the meter entirely rather than making them cheaper. The trade: a cache serves yesterday's answer, so cache invalidation policy is a *freshness* decision, not an infrastructure detail.

## 3. The verification tax

The seductive claim: generative AI makes output "free." The systemic reality: **every probabilistic output that matters must be verified by someone**, and that human audit labor is a real cost the "zero marginal cost" story hides. If verification costs more than doing the task by hand — and for high-stakes outputs it can — the system *destroys* value while its usage metrics look great.

Operationalize it: for any AI feature, estimate **$/verified-good-output**, not $/output. That one denominator change is the difference between a feature that scales and a feature whose hidden labor grows linearly with adoption. (This tax is also why "just add human review" isn't free — you'll design review loops properly in M6.)

## 4. Latency budgets

Latency is a stock the user experiences and a sum the architecture pays: model inference + retrieval + verification passes + routing overhead + network. The PM moves:
- **Set a per-feature latency budget** (e.g., p95 under 2s) and treat every architectural addition as spending from it. Routing adds 1–100ms depending on the router; a verification pass can double response time; streaming buys *perceived* latency without changing actual latency.
- **Watch the latency-quality death spiral**: quality complaints → add verification passes → slower responses → users abandon mid-response → less feedback data → quality stalls. That's a reinforcing loop entered through the "obvious" fix.

## 5. Unit economics: will this feature ever make money?

Tie it together with one honest per-unit model: value per successful task minus (inference cost + retrieval cost + verification tax + support cost of failures) at the *actual* mix of easy/hard requests. Then stress it: what happens at 10× volume? When the model provider reprices? When the frontier model you depend on is deprecated (monoculture risk, M5)? A feature that only works at current prices with current models is a bet, not a business — fine, as long as it's a *written* bet with a kill criterion (M5 again).

## 6. Vocabulary, compressed

**Cost-quality-latency triangle · marginal cost per call · token economics · cost cap (balancing loop) · stop condition (target/budget/stall) · model routing · semantic caching · verification tax · $/verified-good-output · latency budget · p95 · unit economics · graceful degradation.**

## Exercise (prediction-first)

**Subject: your own fleet's paid pipelines** — discovery ($30/day cap), Gemini DR ($20/month cap), council ($40/month cap), all ledgered in `vault/health/`.

1. **Predict (15 min, written):** Pick one pipeline. Before modeling, predict: which loop would blow the budget if its cap vanished, how long until you'd notice, and through which signal. Name the weakest part of the current cap design (detection? degradation? notification?). State a falsifier.
2. **Model (45 min):** Draw the stock-and-flow diagram: budget as stock, spend flows per stage, each cap as a balancing loop with its trigger condition. Then audit today's real incident: the ledger recorded *reservation* amounts ($11.19) while actual settle was $0.79 — trace what that discrepancy does to the cap loop's behavior. Is the cap now too tight, too loose, or lying?
3. **Calibrate:** Compare. Which loop or failure mode did the model reveal that your prediction missed?

Submit all three parts.
