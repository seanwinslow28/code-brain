---
title: "Claude Opus 4.8: The Complete Prompting Playbook for 2026 🧠"
source: "https://substack.com/home/post/p-199701577"
author:
  - "[[Linas Beliūnas]]"
published: 2026-05-28
created: 2026-06-03
description: "How to get the best results from Anthropic's most powerful model every single time, including the new Dynamic Workflows feature."
tags:
  - "source/web-clip"
type: "reference"
status: "draft"
domain: [claude-mastery]
ai-context: "Linas Beliūnas's prompting playbook for Claude Opus 4.8, covering how to get best results from the model including the new Dynamic Workflows feature."
---
👋 *Hey, Linas here! Every day, I break down 3 stories shaping the future of FinTech & Artificial Intelligence - plus the money movements and trends worth tracking. First time here? 387k+ FinTech and AI leaders get this daily. Join them:*

On May 28, **Anthropic** announced a $65 billion Series H round at a whopping $965 billion post-money valuation, making it ***the most valuable private (AI) company on Earth***. The same day, it released **Claude Opus 4.8**.

That timing is definitely *intentional* here. Opus 4.8 is the model Anthropic is betting its near-trillion-dollar story on.

Anthropic describes it as an upgrade on [Opus 4.7](https://linas.substack.com/p/claude-opus-4-7-prompting-guide) “with improvements across benchmarks” and “a more effective collaborator,” available at the same price ($5/$25 per million input/output tokens). The framing is clear as Opus 4.8 ***builds on*** 4.7’s foundation rather than *breaking* from it.

![](https://substackcdn.com/image/fetch/$s_!FcU-!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F785c7a23-8136-46e4-b367-21368af874e0_2600x1392.webp)

Anthropic’s Claude Opus 4.8 vs. other AI models

[The prompting instincts you developed with 4.7](https://linas.substack.com/p/claude-opus-4-7-prompting-guide) **still apply**. But there are meaningful **new capabilities**, and one genuinely **new paradigm**, that change what’s achievable if you know how to use them.

The biggest one is undoubtedly **Dynamic Workflows in Claude Code**: the ability for Claude to write its own orchestration scripts, spin up parallel subagents, and scale test-time compute trivially. Anthropic engineers have been using this as a daily driver for months. The rest of the world found out yesterday.

<video src="blob:https://substack.com/1ea7a9ec-a206-48cc-9dc5-43de8b9d1b77" controls=""></video>

To make this as easy and seamless as possible, we’re also sharing Opus 4.8 Prompt Optimizer, a custom [Claude skill](https://linas.substack.com/p/claudeskills) that rewrites any prompt using the framework below automatically. Step-by-step setup instructions are at the end.

If you’ve read the [Claude Opus 4.7 Prompting Playbook](https://linas.substack.com/p/claude-opus-4-7-prompting-guide), the good news is that your existing prompts ***still work***. But the new capabilities reward **a specific set of upgrades**, particularly around **the effort stack**, **honesty directives**, and **Dynamic Workflows**. This guide covers all of it.

Below is everything you need to get the best output this model can produce, every single time.

## Step 0 - Choose the Right Model

Before writing a single word of your prompt, choose the right model. Anthropic’s current lineup includes **Claude Opus 4.8**, **Claude Sonnet 4.6**, and **Claude Haiku 4.5**, each optimized for different workloads.

→ **Claude Opus 4.8 is now the flagship**. It scores 69.2% on SWE-bench Pro, 88.6% on SWE-bench Verified, and 1890 Elo on GDPval-AA (121 Elo points ahead of GPT-5.5 on economically valuable professional tasks). It excels at long-horizon autonomous tasks, complex reasoning, and knowledge work. It costs more and runs slower via the API ($5/MTok input, $25/MTok output), but when the task demands genuine thinking - strategic analysis, multi-step research, complex autonomous execution - nothing else in the generally available lineup comes close.

→ **Claude Sonnet 4.6 is still the balanced workhorse**: strong reasoning at faster speed and lower cost. For most everyday tasks, Sonnet covers roughly 80% of use cases well.

→ **Claude Haiku 4.5 remains the speed specialist**: fastest, cheapest, ideal for high-volume, straightforward tasks like classification, extraction, and summarization.

**💡 The rule of thumb:** Start with Sonnet. Move to Opus when you need genuine cognitive depth, or when you’re running a Dynamic Workflow that demands long-horizon coherence. Drop to Haiku when speed matters more than intelligence.

## The Framework

Anthropic’s 31-page+ documentation describes a hierarchy of techniques ordered by impact. Most people jump straight to advanced techniques and skip the fundamentals. That’s backwards.

Here’s the framework **in the order that matters**, updated for the specific behaviors of Opus 4.8.

### 1\. Set the Effort Level (Most Important)

**This is the single most important variable in your prompt, and most people never set it at all.**

The effort parameter controls how much intelligence the model applies to a task. Like Opus 4.7, Opus 4.8 respects effort levels strictly, especially at the low end. The system remains: `low`, `medium`, `high` (default), `xhigh`, and `max`.

**One change from 4.7**: Opus 4.8 defaults to `high` effort (4.7 defaulted to `xhigh`), which Anthropic says spends similar tokens on coding tasks while performing better. Adaptive thinking is off by default and must be explicitly enabled.

**The Effort Level System for Opus 4.8:**

![](https://substackcdn.com/image/fetch/$s_!M6rk!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F398a9b35-8659-41aa-919f-4f897de89f8e_1390x508.png)

**In the API:**

```markup
client.messages.create(
    model="claude-opus-4-8",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "xhigh"},
    messages=[{"role": "user", "content": "..."}],
)
```

When running at `max` or `xhigh`, set your `max_tokens` to at least 64k - the model needs room to think, reason, and execute across tool calls and subagents.

**Key Opus 4.8 update from the System Card:** At minimum effort, Opus 4.8 matches the peak performance of Opus 4.7 at maximum effort on SWE-bench Pro. The floor has risen. But the ceiling has expanded too - `xhigh` and `max` now unlock capabilities (particularly in long-horizon agentic work) that Opus 4.7 couldn’t reach at any effort level.

![](https://substackcdn.com/image/fetch/$s_!Q0YM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffca3f8c6-28e9-4048-b007-fb9af2f52722_1782x1050.png)

For Dynamic Workflows specifically, enable `ultracode` mode: this uses workflows aggressively without requiring you to ask for them every time.

<video src="blob:https://substack.com/b757f7a7-0330-493e-a396-15b0d7a2fa26" controls=""></video>

**💡 Practical rule:** If you see shallow reasoning on a complex task, raise the effort level before changing your prompt. That’s almost always the correct fix.

### 2\. Be Specific - More Than You Think

The single highest-leverage prompting move is **specificity**. Opus 4.8, like 4.7 before it, is ***extremely literal***. Vague prompts get scoped, not generalized. If you want an instruction applied across all sections, not just the first, you have to say so. If you want exceptional output, you have to request it explicitly.

Anthropic’s own recommendation still holds: think of your prompt as instructions to a brilliant but literal new hire on their first day. They’ll do exactly what you say, so say exactly what you mean.

**❌ Weak prompt:**

```markup
Write about market positioning.
```

**✅ Strong prompt:**

```markup
Analyze the 3 most effective market positioning strategies for B2B fintech companies targeting mid-market in a crowded category. For each strategy, explain what's driving its effectiveness, provide one specific company example, and assess whether it's likely to strengthen or weaken over the next 18 months. Apply this framework to all three strategies, not just the first.
```

The difference isn’t more words. It’s **more specificity**, **explicit scope**, and a format directive at the end.

### 3\. Use XML Tags for Structure

This is Claude’s structural superpower, and still almost nobody uses it correctly.

Claude was specifically trained to recognize XML tags as structural markers. When your prompt has multiple components - context, instructions, data, constraints, output format - XML tags prevent Claude from mixing them up. Here’s what that looks like for a strategic decision:

```markup
<context>
You are helping me evaluate a potential Series A investment.
The company is a vertical fintech targeting logistics operators,
currently at $2.4M ARR growing 15% MoM.
</context>

<instructions>
Analyze the three key risks that most commonly derail vertical fintech companies
at this stage.
For each risk, explain the warning signs and what a founder should be doing
to mitigate them.
Apply this analysis to all three risks, not just the most obvious one.
</instructions>

<constraints>
- Be direct. Give me your honest assessment, not a balanced "it depends."
- Use specific examples from real companies where possible.
- Flag any assumptions you're making.
- Maximum 600 words.
</constraints>
```

Claude sees the tags and immediately understands that `<context>` is background (not a task to respond to), `<instructions>` is the actual task, and `<constraints>` are the guardrails.

Tag names are flexible - there’s no magic set of “correct” tags. Use whatever makes semantic sense: `<background>`, `<rules>`, `<examples>`, `<output_format>`. Consistency across your prompts matters more than the specific names you choose.

### 4\. Show Claude What Good Looks Like

If one technique consistently separates good outputs from great ones, it’s this: **show Claude what good looks like**.

Instead of describing the tone, format, or style you want in abstract terms, provide two to three concrete examples. Claude will pattern-match against these far more reliably than it will follow descriptive instructions alone. Wrap examples in `<example>` tags (multiple examples in `<examples>` tags) so Claude distinguishes them from instructions.

```markup
<examples>
  <example>
    Input: "We need to cut 20% of the engineering budget"
    Output: "Reducing engineering spend by 20% requires prioritization
    across three areas: contractor headcount, infrastructure costs, and
    tooling licenses. Here's a phased approach that preserves our two
    highest-impact product initiatives..."
  </example>
</examples>

Now analyze this situation using the same approach:
"We need to extend our runway by 6 months without reducing headcount"
```

Anthropic recommends 3–5 examples for best results. You can also ask Claude to evaluate your examples for relevance and diversity, or to generate additional ones based on your initial set.

### 5\. Prompt for Visible Reasoning (Chain-of-Thought)

For complex problems requiring analysis, multi-step reasoning, or strategic judgment, telling Claude to work through its reasoning before producing a final answer dramatically improves accuracy.

The simplest version: add *“Think through this step by step before giving your final answer”* to your prompt.

The more structured version uses tags to separate reasoning from output:

```markup
<instructions>
Evaluate whether we should expand into the Southeast Asian market this year.
Before giving your recommendation, work through the analysis inside
<analysis> tags.
Consider: market size and growth trajectory, regulatory requirements by
country, competitive landscape, our current operational capacity,
and capital requirements vs. expected payback period.
Then provide your final recommendation with a clear resource allocation
suggestion.
</instructions>
```

Forcing visible reasoning prevents Claude from pattern-matching to the most likely answer and back-filling justification after the fact.

**Adaptive thinking in Opus 4.8:** Claude dynamically decides when and how to think based on the effort setting and task complexity. At `high` and `xhigh` effort, deep reasoning is largely automatic for demanding tasks. Extended thinking with a fixed `budget_tokens` is no longer supported - adaptive thinking is the only thinking-on mode, and Anthropic’s evaluations show it reliably outperforms the old fixed-budget approach.

To guide reasoning explicitly, add this to your system prompt:

✅ *“After receiving results, carefully reflect on their quality and determine optimal next steps before proceeding. Use your thinking to plan and iterate based on this new information, then take the best next action.”*

### 6\. Load Rich Context

Claude can only work with what you give it. **The more relevant context you include, the more tailored and accurate the output becomes**.

Upload documents. Paste data. Provide company background. Share your goals. Explain your audience. Don’t make Claude guess what you already know.

```markup
<background>
Our company builds financial infrastructure for neobanks in emerging markets.
We're Series B, $12M ARR, primarily serving West Africa and Southeast Asia.
Our main competitors are Banking-as-a-Service players like Railsbank, Synapse,
and local incumbents.
We differentiate on compliance coverage and local payment rail integrations.
</background>

<data>
[Paste your Q1 metrics, customer feedback, churn data, or whatever's relevant]
</data>

<task>
Based on this context, identify our three biggest growth opportunities
for the next quarter.
</task>
```

For long documents (20k+ tokens), put the documents at the top of your prompt, above your instructions and query. Queries at the end can improve response quality by up to 30% on complex, multi-document inputs.

### 7\. Specify the Output Format

Don’t leave the structure of Claude’s response to chance. If you want a table, ask for a table. If you want a specific word count, state it. If you want an executive brief with defined sections, describe each section.

```markup
<output_format>
Respond with:
1. A one-paragraph executive summary (3-4 sentences max)
2. A comparison table with columns: Factor | Current State | Target State | Gap
3. A "Recommended Actions" section with 3 specific next steps, ranked by impact
</output_format>
```

Explicit format specs eliminate the most common frustration people have with AI: getting a 2,000-word essay when you wanted a concise brief, or getting bullet points when you needed flowing analysis.

### 8\. Define Constraints - Especially “Don’ts”

**Telling Claude what not to do is just as important as telling it what to do**. Without constraints, Claude defaults to its training patterns, which can mean hedge-heavy output that sounds like a committee wrote it.

```markup
<constraints>
- Do NOT open with "In today's rapidly evolving landscape" or any variant
- Skip the preamble. Start with the most important insight.
- No bullet points — write in prose paragraphs
- If you're uncertain about a claim, flag it explicitly rather than hedging
  everything
- Maximum 500 words
- Be direct. I want your honest assessment, not a balanced "it depends."
</constraints>
```

**One note specific to Opus 4.8 from the System Card:** The model has a tendency toward over-elaborate refusals on certain categories of requests. If you’re getting unnecessary hedging or qualification on legitimate business tasks, add a clear statement of legitimate purpose to your prompt - e.g., *“This analysis is for an internal investment committee memo. Please provide a direct, unqualified assessment.”*

### 9\. Control Verbosity

Opus 4.8 calibrates response length to how complex it judges the task to be - short on simple lookups, much longer on open-ended analysis. If your use case requires specific verbosity, tune it explicitly.

**To decrease verbosity:**

*“Provide concise, focused responses. Skip non-essential context and keep examples minimal.”*

**To increase depth:**

*“This is for board-level review. Go deep on every dimension - don’t compress the analysis.”*

Key insight from Anthropic itself: positive examples showing appropriate concision work better than negative instructions like “don’t be verbose.” Show Claude a response at the length and depth you want, and it will match that pattern far more reliably than it will follow abstract length instructions.

### 10\. Use Dynamic Workflows (The New Paradigm)

This is new to the Opus 4.8 era, and it’s **the most powerful capability** yet.

**What it is:** Dynamic Workflows in Claude Code allow Claude to write its own orchestration scripts that spin up tens to hundreds of parallel subagents, instead of making tool calls one at a time. The control flow is code, which means Claude won’t drift or forget halfway through thousands of files. The harness is *encoded*.

![](https://substackcdn.com/image/fetch/$s_!YqhJ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcd9f266c-8daa-46db-9d25-c48e65a63fa3_1642x1018.jpeg)

Claude Code’s newest feature with Opus 4.8: Dynamic Workflows.

**How it works:** Mention the word “workflow” in any Claude Code prompt, and Claude will spin one up automatically. For aggressive workflow use without prompting, enable `effort ultracode` in your settings.

![](https://substackcdn.com/image/fetch/$s_!ItxK!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F43deeac1-719b-4f0e-b0ba-944677c7cd3a_3840x2160.png)

How to activate Dynamic Workflow request

**What it unlocks:**

- **Massively parallel execution**: A five-agent team can handle BrowseComp tasks using just 20% of the latency of a single agent with a 10M-token limit, while scoring higher. The Orchestrator with Blocking Subagents configuration reached the highest scores overall.
- **Adversarial verification**: Route critical work through adversarial judges that each attack the output from a different lens. You can go as far as a tournament-style bracket, scoring competing plans against each other.
- **Scalable test-time compute**: Workflows let you scale test-time compute trivially. There has never been an easier way to do this in Claude Code.
- **Reusable automation**: Because workflows are scripts under the hood, you can save them, commit them to your repo, share them with your team, and turn them into skills.

**The flagship real-world example:** Jarred Sumner (creator of Bun) used Dynamic Workflows to rewrite the entire Bun runtime from Zig to Rust, roughly 750,000 lines of code, eleven days from first commit to merge, 99.8% of the existing test suite passing. The workflow mapped Rust lifetimes for every struct field in the Zig codebase, then wrote every `.rs` file as a behavior-identical port of its `.zig` counterpart, hundreds of agents working in parallel with two reviewers on each file. A fix loop then drove the build and test suite until both ran clean.

**When to reach for a workflow:**

→ The task is too big for a normal session (codebase-wide bug hunt, large refactor, multi-source research).

→ You need higher confidence that something is right (critical features, financial models, security reviews).

→ You want to parallelize work across many files or domains simultaneously.

**🔥 Cost warning:** Workflows can get expensive due to all the parallel agents. Get a feel for token usage on smaller tasks before unleashing them on larger ones. You can disable them with config or enterprise settings if needed.

**Best practices for Dynamic Workflows:**

1. Trigger intentionally. Say “workflow” explicitly for important tasks. For routine work, keep workflows off to manage costs.
2. Enable ultracode for coding sprints. When you’re in a focused engineering session, `effort ultracode` removes the friction of triggering workflows manually.
3. Use adversarial judges for critical outputs. Don’t just generate - verify. Route the output through a judge agent with explicit attack criteria.
4. Save your best workflows as skills. If a workflow solves a recurring problem well, commit it. This is institutional knowledge that compounds.
5. Set a token budget before large tasks. Ask Claude to estimate token usage before running a large workflow, then decide if the cost is justified.
6. Use blocking subagents for accuracy-critical tasks. Async subagents reduce latency but the Orchestrator with Blocking Subagents configuration scores highest when accuracy matters more than speed.
7. Let Claude choose the architecture. Don’t over-specify the workflow structure. Claude knows when to parallelize, when to serialize, and when to use a tournament bracket.
8. Test on a sample first. On large codebases or research tasks, run the workflow on a representative 10% before committing to the full task.

## Putting It All Together

Here’s what a properly structured Claude Opus 4.8 prompt looks like when you combine all the techniques covered above:

```markup
<context>
I'm the CEO of a B2B fintech startup ($8M ARR, 45 employees).
We're deciding whether to raise a Series B now or extend runway and raise
in 18 months.
Current runway: 14 months. Revenue growth: 12% MoM. CAC payback: 8 months.
</context>

<instructions>
Analyze both timing options. Before giving your recommendation, work through
the trade-offs in <analysis> tags, considering:
- Current market conditions for fintech Series B rounds
- Our specific metrics relative to typical Series B benchmarks
- The risk/reward of raising now vs. in 18 months at potentially better metrics
- What we should use the 18 months to optimize if we extend
Then provide a clear recommendation with a specific action plan.
Apply your analysis to both options equally — don't weight one by default.
</instructions>

<constraints>
- Be direct. Give me your honest read, not a balanced "it depends."
- Use specific benchmarks from comparable fintech Series B raises where possible.
- Flag any assumptions you're making about market conditions.
- Keep the total response under 700 words.
</constraints>

<output_format>
1. Analysis (in <analysis> tags)
2. Recommendation (2-3 sentences, clear and direct)
3. 90-day action plan (5 specific actions, whether we raise now or extend)
</output_format>
```

This prompt is clear, structured, specific, and constrained. It tells Claude exactly what to do, how to think about it, what to avoid, and how to format the response. The output from this kind of prompt is categorically different from *“Should I raise a Series B now or wait?”*

## 10 Mega Prompts Engineered for Claude Opus 4.8

As always, understanding the principles is one thing. Having them already engineered into prompts you can use today is another.

Below are 10 Mega Prompts, each structured using every technique above and calibrated for Claude Opus 4.8’s specific behaviors. Each covers a high-leverage task for founders, operators, and investors.

**How to use these prompts:**

- Fill in every `[PLACEHOLDER]` before submitting. Blank placeholders produce generic output.
- Enable web search for prompts that reference real-time data: Research (#1), Competitor Analysis (#8), Stock/Deal Analysis (#9), and Reverse-Engineering (#10). Without it, Claude will rely on training data and flag confidence gaps.
- Use `xhigh` or `high` effort for all 10 prompts. For #9 and #10, start at `xhigh` or `max`.
- Mix and match: you can add chain-of-thought `<analysis>` tags, output constraints, or anti-patterns from one prompt into any other.
- Alternatively, you can use **Opus 4.8 Prompt Optimizer skill** that rewrites any prompt using this framework automatically. Step-by-step setup instructions are at the end.

---
*Clipped from [substack.com](https://substack.com/home/post/p-199701577) on 2026-06-03T17:00:20-04:00*
