---
title: "The One Skill Every AI PM Needs (That Nobody Taught You)"
source: "https://www.news.aakashg.com/p/ai-evals"
author:
  - "[[Aakash Gupta]]"
published: 2025-06-06
created: 2026-05-12
description: "The complete framework for AI evals with Hamel Husain - how to analyze failures, measure them, and improve your LLM pipeline systematically."
tags:
  - "source/web-clip"
type: "source"
status: "draft"
domain: [product-management]
ai-context: "Aakash Gupta's AI-evals primer with Hamel Husain — the complete framework for analyzing LLM-pipeline failures, measuring them, and improving systematically; the skill Aakash argues every AI PM needs."
---
### The complete framework for AI evals with Hamel Husain - how to analyze failures, measure them, and improve your LLM pipeline systematically.

![](https://substackcdn.com/image/fetch/$s_!L0FX!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdd50ac89-a12b-4f6d-9cb9-3edf7f8e7eae_3600x4500.png)

###### This article was updated on April 21, 2026

**An LLM evaluation (eval) is the systematic measurement of LLM pipeline quality. It goes beyond a single number and produces results that can be interpreted clearly and unambiguously.**

Just like you can't be a [Product Manager](https://www.news.aakashg.com/p/roadmap-to-pm-and-ai-mastery-free?utm_source=publication-search) without using analytics, you can't be a Product Manager on AI products without evals.

If you're still breaking into AI Product Management, start with [How to Become an AI Product Manager](https://www.news.aakashg.com/p/how-to-become-an-ai-pm).

Unlike traditional software, [LLM pipelines](https://www.news.aakashg.com/p/hamel-shreya-podcast-2?utm_source=publication-search) do not produce deterministic outputs.

- [A response may be factually accurate but inappropriate (](https://www.news.aakashg.com/p/hamel-shreya-podcast?utm_source=publication-search)i.e., the “vibes are off”).
- They may sound persuasive while conveying incorrect information.

The core challenge is: **How do we assess whether an [LLM pipeline](https://www.news.aakashg.com/p/hamel-shreya-podcast-2?utm_source=publication-search) is performing adequately?** *And how do we diagnose where it is failing?*

To give you the absolute expert POV on this, I’ve teamed up with [Hamel Husain](https://www.linkedin.com/in/hamelhusain/), one of the most recognized names in [AI Evals industry-wide](https://www.news.aakashg.com/p/ai-pm-llm-judge?utm_source=publication-search).

---

*Before we continue, I highly recommend his course, [AI Evals for Engineers & PMs course](https://maven.com/parlance-labs/evals?promoCode=ag-product-growth).*

![](https://substackcdn.com/image/fetch/$s_!013C!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb3c17cb4-7d70-4c72-ace9-93cf2e6127d6_1536x863.png)

*I have been participating in the first cohort alongside 700 other students and got all the knowledge for this deep dive. The practical homework assignments really are taking my learning to the next level.*

*The next and last live cohort starts July 21st. Here’s a special $800 discount for my community:*

---

## Defining Evals

What is an LLM evaluation (eval)?

> *It’s the **systematic measurement** of LLM pipeline quality. A good evaluation produces results that can be easily and unambiguously interpreted. It goes beyond a single number.*

Evals can be operationalized in many different ways.

Three common ways are:

1. **Background Monitoring** - passively, without interrupting the core workflow, these evals detect drift or degradation.
2. **[Guardrails](https://www.news.aakashg.com/p/mahesh-yadav-podcast?utm_source=publication-search)** - in the critical path of the pipeline, these evals run can block the output, force a retry, or result in the fall back to a safer alternative.
3. **To Improve a pipeline -** these evals can label data for fine-tuning LLMs, select high-quality few-shot examples for prompts, or identify failure cases that motivate architectural changes.

---

## What Could Go Wrong? The Three Gulfs

Let’s take the example of an *email processing [AI product](https://www.news.aakashg.com/p/ai-product-sense?utm_source=publication-search)*.

The goal is to: **extract the sender’s name**, **summarize the key requests**, and **categorize the emails**.

This might seem simple. But we actually encounter [three gulfs](https://arxiv.org/abs/2404.12272), as the famous paper *Who Validates the Validators?* explains:

![](https://substackcdn.com/image/fetch/$s_!_4gj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbda80a17-b62e-48ff-86d7-924092984366_3600x4500.png)

#### Gulf 1 - Comprehension (Developer → Data)

Thousands of inputs might arrive daily, with diverse formats and varying levels of clarity.

At scale, it is difficult to know the characteristics of this input data distribution, detect errors within it, or identify unusual patterns.

Just as we cannot read every input, we also cannot manually inspect every output trace generated by the pipeline to grasp all the subtle ways it might succeed or fail across the input space.

So the dual challenge is: *how can we understand the important properties of our input data, and the spectrum of our pipeline’s behaviors and failures on that data, without examining every single example?*

#### Gulf 2 - Specification (Developer → LLM Pipeline)

Our intent—the task we want the [LLM](https://www.news.aakashg.com/p/ai-pm-llm-judge?utm_source=publication-search) to perform—is often only loosely captured by the prompts you write.

For example, we might write:

> *Extract the sender’s name and summarize the key requests in this email*

At first glance, this sounds specific.

But important questions are left unanswered:

1. [How concise or detailed should the summary be?](https://www.news.aakashg.com/p/practical-ai-agents-pms?utm_source=publication-search)
2. Should the summary be a paragraph or a bulleted list?
3. Should the summary include implicit requests, or only explicit ones?
4. Should the sender be the display name, the full email address, or both?

The LLM cannot infer these decisions unless we explicitly specify them.

#### Gulf 3 - Generalization (Data → LLM Pipeline)

Imagine an email that mentions a public figure, like [Elon Musk](https://www.news.aakashg.com/p/eren-bali-the-next-musk-or-dorsey?utm_source=publication-search) or Donald Trump, within the body text.

The model might mistakenly extract these names as the sender, even though they are unrelated to the actual [email](https://www.news.aakashg.com/p/writing-cold-emails-to-get-referrals?utm_source=publication-search) metadata.

This is a generalization failure: *the model applies the instructions incorrectly because it has not generalized properly across diverse data*.

Even when prompts are clear and well-scoped, and even as models get better, this gulf will always exist to some degree, because no model will ever be perfectly accurate on all inputs.

---

## Why Evals are Challenging

Developing effective evaluations for LLM pipelines is hard.

There are at least 4 reasons for this:

![](https://substackcdn.com/image/fetch/$s_!Oywj!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3dd4eeda-d739-488a-9437-6842fa75fce5_3600x4500.png)

1. **Each application requires bridging the Three Gulfs anew**. There are *no universal evaluation recipes*.
2. **Requirements often emerge only after interacting with early outputs**. We might initially expect summaries to be written in prose, but later realize that bulleted lists are easier for users to scan. Evaluation *criteria must evolve alongside system development*.
3. **Appropriate metrics are rarely obvious at the outset**. Unlike traditional software, where correctness is well-defined, *LLM pipelines involve tradeoffs*: factual accuracy, completeness, conciseness, style, and more.
4. **There is no substitute for examining real outputs on real data**. Generic benchmarks *cannot capture the specific failure modes* of our pipeline. Systematic evaluation requires careful, hands-on analysis of representative examples.

---

## The Solution: The LLM Evaluation Lifecycle

Evaluation provides the systematic means to understand and address these challenges. This is done to through 3 steps:

![](https://substackcdn.com/image/fetch/$s_!VLNi!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5f625e39-71c5-410f-9345-e9183e305032_3600x4500.png)

### Step 1 - Analyze

Inspect the pipeline’s behavior on representative data to qualitatively identify failure modes.

This critical first step illuminates why the pipeline might be struggling. Failures uncovered often point clearly to:

- **Ambiguous instructions** (*Specification issues*), or
- **Inconsistent performance across inputs** (*Generalization issues*)

Understanding their true frequency, impact, and root causes demands quantitative data, hence Step 2…

### Step 2 - Measure

Develop and deploy specific evaluators (evals) to quantitatively assess the failure modes.

This data is crucial for prioritizing which problems to fix first and for diagnosing the underlying causes of tricky generalization failures.

### Step 3 - Improve

Make targeted interventions.

This includes direct fixes to prompts and instructions addressing Specification issues identified during Analyze.

It also involves data-driven efforts: such as, engineering better examples, refining retrieval strategies, adjusting architectures, or fine-tuning models to enhance generalization.

Cycling through Analyze, Measure, and Improve (and then back to Analyze) uses structured evaluation to systematically navigate the complexities posed by the Three Gulfs, leading to more reliable and effective LLM applications.

For a simpler take on evals without the full lifecycle, see [AI Evals Explained Simply](https://www.news.aakashg.com/p/ai-evals-explained-simply).

*We will cover each phase in greater depth in the upcoming sections.*

---

## Where We Go From Here

*So, that’s your introduction. Now, let’s go a layer deeper…*

- Eval Basics
- 🔒 Step 1: Analyze
- 🔒 Step 2: Measure
- 🔒 Step 3: Improve

---

## 1\. The Layer Deeper: Eval Basics

Before we dive further into the practical evaluation lifecycle, let’s understand:

- What [LLMs](https://www.news.aakashg.com/p/ai-pm-llm-judge?utm_source=publication-search) can and can't do
- How to communicate with them effectively
- And the basic types of evaluation metrics out there

### LLM Strengths and Weaknesses

We all have experienced LLM’s strengths: they can produce fluent text and generalize to new tasks easily.

But, despite their strengths, LLMs face *4 key limitations* that stem from their architecture, training objective, and probabilistic nature:

1. **Algorithmic tasks**. They can't reliably execute loops or recursion. A model trained on 3-digit addition often fails on 5-digit sums.
2. **Reliability**. Outputs are probabilistic, not deterministic. The same prompt can yield different results.
3. **Prompt sensitivity**. Small wording changes can dramatically alter outputs.
4. **Factuality**. LLMs optimize for statistical likelihood, not truth. They can confidently assert false information.

Given these strengths and weaknesses, *how do we effectively interact with LLMs?* **The primary method is prompting.**

I went deeper on prompting for PMs in [Prompt Engineering for Product Managers](https://www.news.aakashg.com/p/prompt-engineering).

### Prompting Fundamentals

What seems obvious to us might be unclear to the LLM.

**Precision in our prompt is key**.

A well-structured prompt contains 7 key components:

![](https://substackcdn.com/image/fetch/$s_!w24X!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4e953688-4fac-45a4-a064-5a682ebbf6e9_3600x4500.png)

**Component 1 - Role and Objective**

Clearly define the persona or role the LLM should adopt and its overall goal. This helps set the stage for the desired behavior.

*Example*:

```markup
You are an expert technical writer tasked with explaining complex AI concepts to a non-technical audience.
```

**Component 2 - Instructions/Response Rules**

- Be specific and unambiguous
- Use bullet points for multiple instructions
- Define what NOT to do

*Example*:

```markup
- Summarize the following research paper abstract.
- The summary must be exactly three sentences long.
- Avoid using technical jargon above a high-school reading level.
- Do not include any personal opinions or interpretations.
```

**Component 3 - Context**

The relevant background information, data, or text the LLM needs to perform the task.

**Component 4 - Examples (Few-Shot Prompting)**

One or more examples of desired input-output pairs. Highly effective for guiding format, style, and detail level.

**Component 5 - Reasoning Steps (Chain-of-Thought)**

For complex problems, instruct the model to "think step by step" or outline a specific reasoning process.

**Component 6 - Output Formatting Constraints**

Explicitly define the desired structure, format, or constraints for the LLM’s response. This is critical for programmatic use of the output.

*Example:*

```markup
Respond using only JSON format with the following keys: sender_name (string), main_issue (string), and suggested_action_items (array of strings).
```

**Component 7 - Delimiters and Structure**

Use clear separators (### Instructions ###, triple backticks, XML tags) to distinguish different prompt components.

For a full set of ready-to-use PM prompts, see [The PM Prompt Library](https://www.news.aakashg.com/p/pm-prompt-library).

**Precision in prompting is key to bridging the Gulf of Specification**.

However, finding the perfect prompt is *rarely immediate*.

It’s an *iterative* process.

We’ll write a prompt, test it on various inputs, analyze the outputs (using evaluation techniques we’ll discuss in future sections), identify failure modes, and refine the prompt accordingly.

#### Note on Outsourcing Prompting

There are many tools that will write prompts for you and optimize them.

**It’s important that you avoid these** in the beginning stages of development, as *writing the prompt forces you to externalize your specification and clarify your thinking*.

People who delegate prompt writing to a black box too aggressively struggle to fully understand their failure modes.

After you have some reps with looking at your data, you can introduce these tools (but do so carefully).

*An iterative refinement process hinges on having clear ways to judge whether the output is good or bad. This brings us to the concept of evaluation metrics.*

### Types of Evaluation Metrics

Evaluation metrics provide systematic measurements of LLM pipeline quality. They fall into [two categories](https://eugeneyan.com/writing/abstractive/):

![](https://substackcdn.com/image/fetch/$s_!Xaz3!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F86bc71a9-ef12-4a19-ada1-4a8a3ff43e0f_3600x4500.png)

#### Reference-Based Metrics

These evals compare the LLM’s output against a known, ground-truth answer.

This is much like having an official answer key to grade a multiple-choice test.

Reference-based metrics are often valuable during the development cycle, e.g., as unit tests. Think:

- Keyword presence verification
- Exact string matching for short-answer extraction

Beyond simple string comparisons, reference-based checks can become more complex.

Sometimes, this involves executing the result and comparing the result with a reference output. For example:

- Running generated code against unit tests
- Executing generated SQL and checking if the output result or table matches a known correct result or table.

#### Reference-Free Metrics

Alternatively, reference-free metrics evaluate an LLM’s output based on its inherent properties or whether it follows certain rules, operating without a specific “golden” answer.

This approach becomes crucial when dealing with output that is subjective, creative, or where multiple valid responses can exist.

For example:

- Verifying a chatbot doesn't offer medical advice
- Ensuring generated code includes explanatory comments
- Validating that generated SQL executes without syntax errors
- Checking if a summary introduces speculation not in the source

These examples illustrate how reference-free qualities are highly application-specific.

Reference-free checks focus on validity rather than comparing results.

#### The distinction matters

Reference-based metrics are preferred when feasible because they're much cheaper to maintain and verify.

Simple assertions and reference-based checks require minimal overhead, while LLM-as-Judge evaluators need 100+ labeled examples and ongoing maintenance.

**Focus automated evaluators on failures that persist after fixing your prompts**.

Many teams build complex evaluation infrastructure for preferences they never actually specified, like wanting short responses or specific formatting. Fix these obvious specification gaps first.

**Consider the cost hierarchy**:

- Start with cheap code-based checks (regex, structural validation, execution tests)
- Reserve expensive LLM-as-Judge evaluators for persistent generalization failures that can't be captured by simple rules.

*The way we evaluate depends heavily on what we are evaluating—and the cost of maintaining that evaluation over time.*

### Foundation Models vs Application-Centric Evals

**Foundation Model Evals** (like MMLU, HELM, GSM8k) assess general capabilities and knowledge of base LLMs. Think of them as "standardized tests"—useful for initial model selection but insufficient for your specific application.

**Application Evals** assess whether your specific pipeline performs successfully on your specific task using your realistic data. These are your primary focus because:

- Foundation models undergo opaque alignment processes
- General post-training may not match your application's requirements
- You need metrics capturing your specific quality criteria

**Be extremely skeptical of generic metrics for your application.**

In most cases, they're a *distraction*.

The quickest smell that an evaluation has gone off the rails is seeing a dashboard packed with generic metrics like "hallucination\_score," "helpfulness\_score," "conciseness\_score."

*Since application-specific evaluations often involve criteria beyond simple right/wrong answers, we need methods to systematically capture these judgments. How do we actually generate these evaluation signals?*

## Eliciting Labels for Metric Computation

How do we actually generate the scores or labels needed to compute our metrics?

This question is especially pertinent for reference-free metrics, where there is no golden answer key. How can we systematically judge qualities defined by our application, like "helpfulness" or "appropriateness"?

**We recommend starting with binary Pass/Fail evaluations in most cases**, as we'll explore in detail later. Binary evaluations force clearer thinking and more consistent labeling, while Likert scales introduce significant challenges: the difference between adjacent points (like 3 vs 4) is subjective and inconsistent across annotators, and annotators often default to middle values to avoid making hard decisions.

*With this preference for binary judgments in mind, three general approaches are used:*

![](https://substackcdn.com/image/fetch/$s_!sdY_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F255d8556-4220-454e-912d-2798771a7d9c_3600x4500.png)

#### Approach 1 - Direct Grading or Scoring

The most common method of evaluations for AI applications is Direct Grading or Scoring. Here, an evaluator assesses a single output against a predefined rubric.

This rubric might use a scale (e.g., 1-5 helpfulness) or categorical labels (e.g., Pass/Fail, Tone: Formal/Informal/Casual).

Evaluators can be human annotators, domain experts, or a well-prompted "LLM-as-judge," or an LLM that has been prompted to assess outputs according to the rubric.

Obtaining reliable direct grades demands extremely clear, unambiguous definitions for every possible score or label. Defining distinct, objective criteria for each point on a 1-5 scale can be surprisingly difficult.

For this reason, **simpler binary judgments** (like Yes/No for "Is this summary faithful to the source?") **are often easier to define consistently and are our recommended starting point**.

Binary decisions are also faster to make during error analysis—you don't waste time debating whether something is a 3 or 4.

Direct grading is most useful when our primary goal is assessing the absolute quality of a single pipeline's output against our specific, predefined standards.

#### Approach 2 - Pairwise Comparison

Pairwise comparison presents an evaluator with two outputs (A and B) generated for the same input prompt. The evaluator must then choose which output is better based on a specific, clearly defined criterion or rubric.

While this still requires unambiguous comparison criteria, making this relative choice between two options is frequently cognitively easier for evaluators than assigning a precise score from a multi-level scale.

#### Approach 3 - Ranking

Evaluators order three or more outputs generated for the same input from best to worst, according to the same clearly defined quality dimension specified in the comparison rubric.

Ranking provides more granular relative information than pairwise comparison, though it typically requires more evaluator effort.

These relative judgment methods are particularly useful when our main goal is to compare different systems or outputs directly. We might use them for A/B testing different prompts, comparing candidate models, or selecting the best response when our pipeline generates multiple options for a single input.

**For tracking gradual improvements, consider measuring specific sub-components with their own binary checks rather than using scales**.

For example, instead of rating factual accuracy 1-5, track "4 out of 5 expected facts included" as separate binary checks. This preserves the ability to measure progress while maintaining clear, objective criteria.

---

## The Layer Deeper - Step 1: Analyze

The process of developing robust evaluations for LLM applications is inherently iterative.

This section provides a detailed methodology for the Analyze portion—specifically focusing on how we systematically surface failure modes.

Let’s ground our discussion in a running example: a real estate CRM assistant.

The assistant powers real estate agents' workflows. Given natural language queries, it can generate SQL queries to retrieve listing data, summarize trends, draft emails to clients, and read calendars.

Typical user queries might include: "Find me 3-bedroom homes under $600k near downtown. Email the top 2 matches to my client. Figure out if there are showings available for this weekend."

If you want to build something like this yourself, [here's the full guide on AI prototyping for PMs](https://www.news.aakashg.com/p/ai-prototyping-for-pms).

The pipeline is agentic. An LLM call interprets the user's request and returns structured actions. Each action invokes a downstream tool.

Outputs are fed back to the LLM, which may issue further actions based on new information.

![](https://substackcdn.com/image/fetch/$s_!JeGV!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3e18b44d-8ff2-401a-8862-c1fad2185649_990x750.png)

### 1\. Bootstrap a Starting Dataset

Every error analysis starts with traces: the full sequence of inputs, outputs, and actions taken by the pipeline for a given input.

Ideally, we want to start with around 100 traces.

This gives enough coverage to surface a wide range of failure modes and push toward theoretical saturation—the point at which analyzing additional traces is unlikely to reveal sufficiently new categories or types of errors.

If 100 real user queries already exist, we sample them directly.

Diversity matters: traces should stress different parts of the system, not just repeat the same feature path.

### Systematic Synthetic Data Generation

In early-stage pipelines, real user traces are often sparse.

In those cases, we generate synthetic data—but carefully. We should not simply prompt an LLM to "give us user queries."

Naively generated queries tend to be generic, repetitive, and fail to capture real usage patterns.

For many applications, the variety of fundamental user intents is often surprisingly limited—perhaps on the order of 10 to 20 core types.

This ties directly into product strategy — we broke it down in [AI Product Strategy in 2026](https://www.news.aakashg.com/p/ai-product-strategy-2026).

First, we define key dimensions of the query space.

Choose the dimensions that describe where your AI application is likely to fail.

**Dimension**

A dimension is a way to categorize different parts of a user query. Each dimension represents one axis of variation.

For example, in a real estate assistant, useful dimensions might include:

- Feature: what task the user wants to perform (e.g., property search, scheduling)
- Client Persona: the type of client being served (e.g., first-time buyer, investor)
- Scenario Type: how clearly the user expresses their intent (e.g., well-specified, ambiguous)

Do not choose these dimensions arbitrarily! Instead, choose the dimensions that describe where your AI application is likely to fail.

Once we've defined our dimensions, we create structured combinations called tuples.

**Tuple**

A tuple is a specific combination of values—one from each dimension—that defines a particular use case.

For example:

- Feature: Property Search
- Client Persona: Investor
- Scenario Type: Ambiguous

This tuple describes a case where an investor is searching for properties, but the request may be underspecified or vague.

Here are two example queries sketched from different tuples:

- Tuple: (Feature: 'Property Search', Persona: 'First Time Buyer', Scenario: 'Specific Query') Query: Find 3-bedroom homes under $600k near downtown that allow pets.
- Tuple: (Feature: 'Property Search', Persona: 'Investor', Scenario: 'Vague Query') Query: Look up showings for good properties in San Mateo County.

Once we have a small set of example tuples and queries, we use an LLM to scale up to 100 or more.

But instead of having the LLM generate full queries directly—which often leads to repetitive phrasing—we break the process into two steps.

First, we sample structured tuples: feature, persona, and scenario. Then, for each tuple, we generate a natural-language query using a second prompt.

![](https://substackcdn.com/image/fetch/$s_!28CG!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20448f46-6b8d-49df-b15e-240b21368c6e_434x552.png)

In the first step, we prompt the LLM like this:

**Sample Prompt**

```markup
Generate 10 random combinations of (feature, client persona, scenario) for a real estate CRM assistant.

The dimensions are:
Feature: what task the agent wants to perform. Possible values: property search, market analysis, scheduling, email drafting.

Client persona: the type of client the agent is working with. Possible values: first-time homebuyer, investor, luxury buyer.

Scenario: how well-formed or challenging the query is. Possible values:
- exact match (clearly specified and feasible),
- ambiguous request (unclear or underspecified),
- shouldn't be handled (invalid or out-of-scope).

Output each tuple in the format: (feature, client persona, scenario)

Avoid duplicates. Vary values across dimensions. The goal is to create a diverse set of queries for our assistant.
```

For each LLM-generated tuple, we then generate a full query in natural language:

**Sample Prompt**

```markup
We are generating synthetic user queries for a real estate CRM assistant. The assistant helps agents manage client requests by searching listings, analyzing markets, drafting emails, and reading calendars.

Given:
Feature: Scheduling Client Persona: First-time homebuyer
Scenario: Ambiguous request

Write a realistic query that an agent might enter into the system to fulfill this client's request. The query should reflect the client's needs and the ambiguity of the scenario.

Example:
"Find showings for affordable homes with short notice availability."

Now generate a new query.
```

We continue sampling, generating, and filtering until we reach 100 high-quality, diverse examples.

When phrasing is awkward or content is off-target, we discard and regenerate.

It is better to be aggressive in quality control here: downstream evaluation is entirely based on the representativeness and realism of these traces.

### 2\. Open Coding: Read and Label Traces

With a data set of queries in hand, the next step is to run the assistant on all queries and collect complete traces.

A trace records the entire sequence of steps taken by the pipeline: the initial user query, every LLM output, each downstream tool invocation, and the final user-facing results.

We collect all intermediate and final steps, not just the surface output. Failures often arise inside the chain, not only at the end.

This process is adapted from grounded theory, a methodology from qualitative research that builds theories and taxonomies directly from data.

Rather than starting with a fixed list of error types, we observe how the system behaves, label interesting or problematic patterns, and let the structure of failures emerge naturally.

In grounded theory, coding refers to assigning short descriptive labels to parts of the data that seem important.

For each trace, we read carefully and write brief notes about what we observe: where outputs are incorrect, where actions are surprising, or where the behavior feels wrong or unexpected.

When beginning, we recommend examining the entire trace as a whole and noting the first (most upstream) failure observed.

We record each trace and its corresponding open-coded notes into a simple table or spreadsheet:

![](https://substackcdn.com/image/fetch/$s_!QvQZ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4223d5f-693c-4f68-bb35-4b6d2be0efd6_848x732.png)

At this stage, we do not attempt to group or formalize errors. We simply collect a rich set of raw observations.

Sometimes, when starting with initial labeling, it can be challenging to articulate precisely what feels "off" about a trace.

If we find ourselves stuck, a helpful strategy is to switch temporarily to a more "top-down" approach.

Consider a list of common LLM failure categories and actively look for their manifestations: hallucination, structured output issues, adherence to constraints, stylistic consistency.

Continue this initial annotation until we have surfaced a sufficiently broad set of failures.

As a rule of thumb, we proceed until at least 20 bad traces are labeled and no fundamentally new failure modes are appearing.

This point is known as theoretical saturation: when additional traces reveal few or no new kinds of errors.

### 3\. Axial Coding: Structuring and Merging Failure Modes

Open labeling produces a valuable but chaotic collection of observations.

Without further organization, we cannot meaningfully quantify failures.

Axial coding means reading through the body of open-coded traces and clustering similar failure notes together.

Some patterns are obvious. Traces where the assistant proposes showings for weekends when the real estate agent is marked unavailable cluster naturally into a broader failure mode: violation of user constraints.

Other failures reveal deeper distinctions only after reading several traces.

Hallucinations of property features—claiming a home has solar panels when it does not—and hallucinations of client activity—scheduling a tour that the user never requested—were initially grouped together.

But over time, it becomes clear they differ meaningfully: one misleads about external facts; the other fabricates user intent.

The goal is to define a small, coherent, non-overlapping set of binary failure types, each easy to recognize and apply consistently during trace annotation.

You can use a language model to assist the process. After open coding 30–50 traces, we can paste the raw failure notes into our favorite LLM (e.g., [ChatGPT](https://chat.openai.com/), [Claude](https://claude.ai/new)) and ask it to propose preliminary groupings:

**Sample Prompt**

```markup
Below is a list of open-ended annotations describing failures in an LLM-driven real estate CRM assistant. Please group them into a small set of coherent failure categories, where each category captures similar types of mistakes. Each group should have a short descriptive title and a brief one-line definition. Do not invent new failure types; only cluster based on what is present in the notes.
```

LLM-generated groupings can help organize initial ideas, but they should not be accepted blindly.

Proposed clusters often require manual review and adjustment to accurately reflect the system's behavior and the application's specific requirements.

### 4\. Labeling Traces with Structured Failure Modes

At this stage, we have two artifacts:

1. A collection of traces, each with its initial, freeform "first-pass annotations."
2. A defined list of structured, binary failure modes (from axial coding)

Our next goal is to systematically apply these structured failure modes to each trace.

For every trace, and for each defined failure mode, we determine if that specific failure is present (1) or absent (0).

**Review and Map Open Codes to Structured Failures**: We revisit our initial spreadsheet of traces and their first-pass annotations.

For each trace, we compare its freeform annotation against our defined list of structured failure modes.

**Populating the Structured Data Table**: We augment our spreadsheet by adding new columns, one for each structured failure mode.

For each trace, we then populate these columns with a 1 if the failure mode is present for that trace and a 0 if it's absent.

For example, if a first-pass annotation for a trace was "SQL query missed the budget constraint and also used an aggressive tone in the generated email," and our structured failure modes include "Missing SQL Constraint" and "Inappropriate Tone," this trace would get a 1 in both those columns and 0s in others.

During this process, it is common to discover inconsistencies or edge cases that force a reevaluation.

We allow ourselves to adjust annotations or revise failure mode definitions as needed.

Once labeling is complete, we can quantify the prevalence of each failure mode—which is critical for prioritization in the Improve phase.

### Common Pitfalls

The most common mistake in early error analysis is failing to test on representative data.

If the initial query set does not reflect the diversity and difficulty of real user behavior, the traces produced are uninformative.

A second common failure is skipping open coding altogether.

Instead of reading real traces and observing how the system actually fails, teams often default to generic categories pulled from LLM research: "hallucination," "staying on task," "verbosity."

The abuse of generic metrics is endemic in the industry as many eval vendors promote off the shelf metrics, which ensnare unsuspecting engineers into superfluous metrics and tasks.

This is also why we think most teams are [building AI products the wrong way](https://www.news.aakashg.com/p/how-to-build-ai-products).

Another frequent pitfall is the inappropriate use of Likert scales during early annotation.

In contrast, forcing binary decisions about specific failure modes—whether a problem occurred or not—produces more reproducible annotations.

Finally, treating initial annotations and failure modes as fixed is a critical error.

It is normal for annotation schemas to evolve after reviewing more data. Freezing the schema too early locks evaluation infrastructure around an incomplete understanding of system behavior.

The Analyze phase is the cornerstone of effective LLM evaluation, providing the deep, qualitative understanding necessary before any meaningful measurement or improvement can occur.

Its critical output is a well-understood, application-specific vocabulary of failure: a clear, consistent set of defined failure modes that allows us to precisely describe, and subsequently measure, how and why our LLM pipeline isn't meeting expectations.

This foundation is essential before proceeding to measure these failures at scale.

*Next up: Step 2: Measure - implementing automated evaluators to translate qualitative insights into quantitative metrics.*

---

## The Layer Deeper: Step 2 - Measure

In Section 3, we presented a framework to identify failures as part of the "Analyze" phase of our evaluation lifecycle.

Here, we present how to approach the Measure phase.

Measurement is about estimating the prevalence of our application's failure modes.

The ability to quickly and reliably measure changes in success or failure rates is fundamental to an effective development loop.

When we modify a prompt, adjust a retrieval strategy, or swap a model, we need to see concrete evidence of whether that change helped, harmed, or had no effect on specific issues.

Manually re-evaluating a large set of traces after every pipeline change is slow and prone to inconsistency.

Therefore, this section focuses on building automated evaluators.

Automated evaluators can compute various types of metrics.

- Some metrics will be reference-free, assessing inherent qualities of an output or its adherence to certain rules without needing a "golden" or ground-truth answer.
- Others will be reference-based, comparing the pipeline's output to a known correct or ideal response.

For many failure modes, it is beneficial to conceptualize and, where feasible, implement both reference-free and reference-based checks.

We continue with the same running example from Section 3: a real estate chat-based CRM assistant that interprets natural language queries from real estate agents, issues SQL, drafts client emails, reads calendars, and performs internet searches.

![](https://substackcdn.com/image/fetch/$s_!cJpN!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8a14d98c-d718-4b80-8fd4-ce0086a620ab_976x782.png)

Worfklow for building an LlM-as-Judge evaluator.

### Defining the Right Metrics (What to Measure)

Effective measurement begins by defining precise, quantifiable metrics for each failure mode identified during our error analysis.

To illustrate, the following table lists several categories of failures we might have uncovered for our real estate CRM assistant during error analysis.

![](https://substackcdn.com/image/fetch/$s_!vQSM!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1108c8ef-2c73-417a-a247-9b11240a4ee1_820x556.png)

After listing the failure modes, we can identify which ones can be simple to fix, due to ambiguity in our prompt specifications.

Gulf of Specification errors, stemming from ambiguous or incomplete instructions we provided to the LLM, can be easy to resolve if we edit the prompt. The evals that we write should mainly target the Gulf of Generalization.

In other words, we want to fix ambiguity first, then measure generalization.

**There are two reasons for this.**

First, for efficiency reasons: many specification failures can be resolved rapidly, often by simply adding clarity or detail to an existing prompt. It can feel like a waste of time to build an automated evaluator for a failure mode that is easily resolved by a modification to a prompt.

Second, more fundamentally, we want our evaluation efforts to accurately reflect the LLM's ability to generalize correctly from clear instructions, not its capacity to decipher our potentially ambiguous intents.

Consider an example from Table 2: "Incomplete Email Content" might be a Specification Failure if our email generation prompt doesn't clearly instruct the LLM on mandatory fields to include based on the context. We would need to improve our prompt. In contrast:

- "Missing SQL Constraints," if the prompt clearly stated the constraint (e.g., "max\_price: $600k") but the LLM still omitted it, points to a Generalization Failure. This is a good candidate for an automated evaluator.
- "Persona-Tone Mismatch," assuming the client persona was clearly provided to the LLM, would also be a Generalization Failure.
- "Invalid Tool Usage" (calling a non-existent tool) is almost always a Generalization Failure (or a more fundamental model issue) if the available tools are well-defined to the LLM.

Once we have this refined list of Generalization Failures, we design specific, automatable metrics for each.

We try to design both a reference-based and a reference-free metric for each significant failure mode.

For reference-based metrics, first, we need to curate input-output pairs where the LLM output exemplifies the desired failing behavior. The automated evaluator will then measure how closely the pipeline's actual output aligns with this "golden" reference.

For example, if a failure mode is "Missing SQL Constraints," our reference data would consist of user queries and the corresponding ideal SQL, which does include all necessary constraints.

Reference-based metrics are invaluable during iterative development, such as prompt engineering or model fine-tuning, and are often key components of Continuous Integration (CI) checks.

For reference-free metrics, we define intrinsic properties or rules related to the failure mode. The evaluator measures adherence to these defined properties.

For instance, continuing with "Missing SQL Constraints," a reference-free check might involve parsing the generated SQL to verify the presence of keywords associated with expected constraints.

For "Persona-Tone Mismatch," a reference-free approach might involve using an external judgment process to classify the tone of the generated email and then check if this classification aligns with the target persona's known preferences.

Reference-free metrics are particularly powerful because they can often be adapted to run efficiently at scale on new, unlabeled data, enabling broader monitoring and assessment, potentially even in online settings.

As part of both types of metrics, we might incorporate executability checks. This means the metric goes beyond static analysis of the generated text to assess its functional correctness.

For instance, if the LLM generates a SQL query, the evaluator might execute it against a test database to ensure it runs without error and yields plausible results.

The following Table presents sample reference-based and reference-free metrics for some of the failure modes identified in Table 2.

![](https://substackcdn.com/image/fetch/$s_!86u5!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F306ac10b-d126-4e53-b6bd-2b13254e41f4_890x608.png)

Reference-Based and Reference-Free Metrics for Real Estate CRM Failures

### Implementing Metrics (How to Measure)

The goal of automated evaluators is to estimate the prevalence of each failure mode across a set of traces.

Manual labeling at this scale is too slow and expensive, so we turn to automation. The challenge is ensuring each evaluator is well-grounded in the human-defined failure criteria—otherwise, the metrics are meaningless.

Each failure mode should have its own dedicated evaluator.

Depending on the nature of the failure, this can be implemented either with code or with an LLM.

Code-based evaluators are ideal when the failure definition is objective and can be checked with rules. For example:

- Parsing structure (e.g., checking JSON validity or SQL syntax).
- Using regex or string matching to detect required or forbidden phrases.
- Counting or verifying structural constraints (e.g., a summary has 3 bullet points).
- Executing the tool call generated by an LLM, and checking that the execution did not raise any errors.
- Logical checks (e.g., if the query asks for a dog-friendly apartment, does the output mention "pets allowed"?)

Code evaluators are fast, cheap, deterministic, and interpretable.

They can support both reference-free checks (e.g., length limits) and reference-based ones (e.g., value extraction compared to a gold set).

LLM-as-Judge evaluators are used when the failure mode involves interpretation or nuance that code can't capture.

For instance: Was the tone appropriate? Is the summary faithful? Is the response helpful?

In these cases, we use a separate LLM—distinct from the main application—to judge outputs for a single failure mode. Each metric may require a different LLM-as-Judge evaluator, tailored to its specific failure definition.

This is expected—and desirable—when evaluating multiple aspects of quality. LLM judges work best for narrowly defined, binary tasks (e.g., when the answer can be PASS or FAIL).

However, using LLMs for evaluation comes with risks: bias, inconsistency, and inference cost. Prompt design, clear criteria, and calibration against human judgments are important.

**How do you know you can trust the LLM judge?** In a later section, we show you how to verify your judge against the human labels you collected in a previous step.

![](https://substackcdn.com/image/fetch/$s_!ZyJz!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd79ee83e-afc2-4d23-952b-fb3fa30ccab6_850x272.png)

Programmatic vs. LLMas-Judge Evaluators for Real Estate CRM Failures

### Writing LLM-as-Judge Prompts

The term "LLM-as-a-judge" was introduced by Zheng et al. (2023), who trained specialized LLM judges using large amounts of human preference data.

In practice, however, such fine-tuning is rarely feasible. Most applications lack sufficient labeled preference data, especially in early stages of development.

Instead, we use off-the-shelf LLMs as judges and rely on prompt engineering to align their outputs with our intended failure definitions.

Each evaluator corresponds to a single metric, which targets a specific failure mode identified during error analysis.

To make supervision tractable without fine-tuning, we restrict the task to binary outputs—PASS/FAIL or YES/NO.

A well-structured LLM-as-Judge prompt contains four essential components:

1. **Clear task and evaluation criterion.** Each prompt should focus on one well-scoped failure mode. Vague tasks lead to unreliable judgments. Instead of asking whether an email is "good," we ask whether "the tone is appropriate for a luxury buyer persona."
2. **Precise Pass/Fail definitions.** We define what counts as a Pass (failure absent) and a Fail (failure present), directly based on the failure descriptions developed during error analysis.
3. **Few-shot examples.** Examples help calibrate the judge's decision boundary. We include labeled outputs that clearly Pass and clearly Fail. These are best drawn from human-labeled traces. While we primarily focus on binary (Pass/Fail) judgments for clarity and alignment, if using finer-grained scales (e.g., 1–3 severity), it's critical to include examples for every point on the scale.
4. **Structured output format.** The judge should respond in a consistent, machine-readable format—typically a JSON object with two fields: reasoning (1–2 sentence explanation) and answer ("Pass" or "Fail"). This structure improves both accuracy and interpretability.

The example below shows a prompt template for evaluating tone appropriateness in a real estate CRM assistant. Each LLM-as-Judge evaluator follows this structure but is tailored to its specific failure mode.

**Sample Prompt**

```markup
You are an expert evaluator assessing outputs from a real estate assistant chatbot.

Your Task: Determine if the assistant-generated email to a client uses a tone appropriate for the specified client persona.

Evaluation Criterion: Tone Appropriateness

Definition of Pass/Fail:
- Fail: The email's tone, language, or level of formality is inconsistent with or unsuitable for the described client persona.
- Pass: The email's tone, language, and formality align well with the client persona's expectations.

Client Personas Overview:
- Luxury Buyers: Expect polished, highly professional, and deferential language. Avoid slang or excessive casualness.
- First-Time Homebuyers: Benefit from a friendly, reassuring, and patient tone. Avoid overly complex jargon.
- Investors: Prefer concise, data-driven, and direct communication. Avoid effusiveness.

Output Format: Return your evaluation as a JSON object with two keys:
1. reasoning: A brief explanation (1-2 sentences) for your decision.
2. answer: Either "Pass" or "Fail".

Examples:
–––
Input 1:
Client Persona: Luxury Buyer
Generated Email: "Hey there! Got some truly awesome listings for you in the high-end district. Super views, totally posh. Wanna check 'em out ASAP?"

Evaluation 1: {"reasoning": "The email uses excessive slang ('Hey there', 'awesome', 'totally posh', 'ASAP') and an overly casual tone, which is unsuitable for a Luxury Buyer persona.", "answer": "Fail"}

–––
Input 2:
Client Persona: First-Time Homebuyer
Generated Email: "Good morning! I've found a few properties that seem like a great fit for getting started in the market, keeping your budget in mind. They offer good value and are in nice, welcoming neighborhoods. Would you be interested in learning more or perhaps scheduling a visit?"

Evaluation 2: {"reasoning": "The email adopts a friendly, reassuring tone ('great fit for getting started', 'nice, welcoming neighborhoods') suitable for a First-Time Homebuyer, and clearly offers next steps.", "answer": "Pass"}

–––
Now, evaluate the following:
Client Persona: {{CLIENT_PERSONA_HERE}}
Generated Email: {{GENERATED_EMAIL_HERE}}

Your JSON Evaluation:
```

### Data Splits for Designing and Validating LLM-as-Judge

Designing an LLM-as-Judge closely resembles training a classifier—except the "training" happens through prompt engineering, not parameter tuning.

Instead of learning from data via gradient descent, we manually select examples and write instructions that guide the model's behavior in-context.

To ensure the resulting evaluator generalizes and doesn't overfit, we divide our labeled traces (from Section 3) into three disjoint sets:

- **Training Set.** A pool of labeled examples we may draw from when constructing the prompt. These examples are candidates for few-shot demonstrations—typically clear-cut Pass and Fail cases that illustrate the boundaries of the failure mode.
- **Development (Dev) Set.** A separate, larger set of labeled traces used to refine the prompt. After each edit—whether changing instructions, rewording criteria, or swapping few-shot examples—we evaluate judge outputs on the dev set by comparing them to human labels. Dev set examples must never appear in the prompt itself. This ensures we can measure how well the judge generalizes beyond the training examples.
- **Test Set.** A held-out set we use only to compute the alignment of the LLM judge, after finalizing the LLM judge prompt. We never look at this set during judge prompt development. It gives us an unbiased estimate of the judge's real-world accuracy—metrics like True Positive Rate and True Negative Rate—which we later use to adjust estimated success rates in production traces.

Reusing examples across splits—especially from Dev or Test in the prompt—leads to overfitting and inflated accuracy estimates.

Unlike traditional supervised learning, we don't need large training sets. In-context learning typically saturates after a small number of well-chosen examples. Studies suggest that LLM performance often plateaus after 1–8 examples. More examples can even degrade accuracy or exceed context length limits.

As a result, we allocate more data to evaluation. A typical split might assign 10-20% of labeled traces to the training set, and 40-45% each to dev and test.

To reliably estimate judge performance, both dev and test sets should include a balanced number of Pass and Fail examples—ideally 30–50 of each.

These proportions may not reflect real-world prevalence, especially when failures are rare. This imbalance is acceptable and deliberate.

## Iterative Prompt Refinement for the LLM-as-Judge

After splitting labeled data into training, development, and test sets, we enter the core of judge construction: iteratively refining the prompt to align the LLM's decisions with expert labels.

This process mirrors the tuning loop of a classifier, but instead of adjusting parameters, we revise prompt text and examples. The loop proceeds as follows:

1. **Write a Baseline Prompt.** Start with an initial prompt using the components outlined earlier: task description, clear definitions, structured output format, and a few-shot example set drawn from the training set.
2. **Evaluate on dev set.** Run the LLM-as-Judge over all examples in the development set. Compare each judgment (Pass or Fail) to the human-provided ground truth.
3. **Measure agreement.** Let P be the total number of dev examples labeled Pass, of which p were judged Pass; let F be the total number labeled Fail, of which f were judged Fail. Then compute:

TPR = p/P (true positive rate), TNR = f/F (true negative rate).

We refer to a positive as a pass, and a negative as a fail.

4. **Inspect disagreements.** Review false passes (judge said Pass but human said Fail) and false fails (judge said Fail but human said Pass) to identify ambiguous criteria or missing edge cases.
5. **Refine the Prompt.** Based on dev set errors:
- Clarify task wording or tighten Pass/Fail criteria.
- Swap in more illustrative few-shot examples from the training set.
- If the dev set has some failure modes that are not in the training set, add representative traces to the training set and consider using them in the prompt for the next round.
6. **Repeat.** Re-evaluate the revised prompt on the same dev set and re-calculate metrics. Continue until performance stabilizes or improves acceptably.

**When to Stop Refining**

We stop when TPR and TNR reach satisfactory levels (e.g., >90%). Thresholds depend on application needs—missing a real failure may be costlier than flagging a false one.

While tools like DSPy can automate this loop by optimizing prompts over a dev set, we recommend manual iteration first. It builds intuition about both the failure mode and the judge's behavior.

**If Alignment Stalls**

If the judge continues to perform poorly—e.g., low TPR and TNR—consider one of the following strategies:

We could use a more capable LLM: a larger or newer model may resolve subtle or context-sensitive errors.

We could also decompose the criterion, or break a complex failure mode into smaller, more atomic checks, each with its own judge.

Or, we could improve our labeled data, or add more diverse, high-quality examples to the training set—especially for edge cases.

It is important to make sure that we trust our labels. A common mistake companies make is to outsource labeling to people (or even LLMs) who do not have any context on the application.

## Estimating True Success Rates with Imperfect Judges

After achieving consistent, high TPR and TNR on the dev set, we fix the LLM-as-Judge prompt and run it on the test set.

This gives us two things. First, an estimated pass or success rate on the test set: the fraction of examples the judge labels as "Pass." Second, estimates of the judge's TPR and TNR, computed by comparing its predictions to ground-truth human labels.

But this only tells us how the judge behaves on the test split. In practice, we want to estimate how often a failure mode appears in a much larger (often unlabeled) dataset—such as new traces from a production pipeline.

The problem is that our judge is imperfect. If we run it over thousands of new outputs and simply count the "Pass" predictions, we'll get a biased estimate of the true pass rate, because the judge occasionally misses failures or flags passes incorrectly.

This section shows how to:

1. Use the judge's TPR and TNR to correct its raw predictions and estimate the true pass rate θ for a metric—that is, the fraction of examples a human would consider passing the evaluation criterion.
2. Quantify the uncertainty around this estimate by constructing a 95% confidence interval. If the upper bound is low, we can trust the LLM pipeline is performing acceptably. If the interval is wide, we may need to improve the TPR and TNR of the judge.

We now present a procedure to estimate the true pass or success rate θ of an evaluation metric over new, unlabeled traces.

![](https://substackcdn.com/image/fetch/$s_!jy91!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb7d678e0-938a-439c-9436-69703b10263a_912x710.png)

Workflow for estimating the true success rate with bias correction and confidence intervals.

**Step 1: Measure Judge Accuracy.** On our held-out test set, we compare judge predictions to human labels and compute TPR and TNR.

**Step 2: Observe Raw Success Rate.** We run the judge on *m* new, unlabeled traces and let k be the number it labels "Pass." The raw success rate is p\_obs = k/m.

**Step 3: Correct the Observed Success Rate.** Because the judge is imperfect, p\_obs is biased. We adjust it to estimate the true success rate:

θ̂ = (p\_obs + TNR - 1) / (TPR + TNR - 1) (clipped to \[0, 1\]).

If TPR + TNR - 1 ≈ 0 (e.g., 50% TPR and TNR), then the judge is no better than random chance, and the correction is invalid. In practice, θ̂ is clipped to the range \[0, 1\] to handle numerical noise.

**Step 4: Quantify Uncertainty with Bootstrap Sampling.** We quantify uncertainty in our corrected success rate estimate by bootstrapping over the test set's judge-vs-human labels: each iteration samples (with replacement) the full set of (human label, judge prediction) pairs, recomputes TPR and TNR on that sample, applies the correction to obtain a new θ̂\*, and records it. After B iterations, the 2.5th and 97.5th percentiles of these {θ̂\*} values form our 95% confidence interval.

Here is a Python code snippet that computes a point estimate of the LLM pipeline's success rate θ̂, as well as a 95% confidence interval for the true success rate θ.

```markup
import numpy as np

def estimate_success_rate(
    test_labels,
    test_preds,
    unlabeled_preds,
    B=20000
):
    """
    Args:
        test_labels: array-like of 0/1, human labels on test set (1 = Pass).
        test_preds: array-like of 0/1, judge predictions on test set (1 = Pass).
        unlabeled_preds: array-like of 0/1, judge predictions on unlabeled data (1 = Pass).
        B: number of bootstrap iterations.

    Returns:
        theta_hat: point estimate of true success rate.
        L, U: lower and upper bounds of a 95% bootstrap CI.
    """
    test_labels = np.asarray(test_labels, dtype=int)
    test_preds = np.asarray(test_preds, dtype=int)
    unlabeled_preds = np.asarray(unlabeled_preds, dtype=int)

    # Step 1: Judge accuracy on test set
    P = test_labels.sum()
    F = len(test_labels) - P
    TPR = ((test_labels == 1) & (test_preds == 1)).sum() / P
    TNR = ((test_labels == 0) & (test_preds == 0)).sum() / F

    # Step 2: Raw observed success rate
    p_obs = unlabeled_preds.sum() / len(unlabeled_preds)

    # Step 3: Correct estimate
    denom = TPR + TNR - 1
    if denom <= 0:
        raise ValueError("Judge accuracy too low for correction")
    theta_hat = (p_obs + TNR - 1) / denom
    theta_hat = np.clip(theta_hat, 0, 1)

    # Step 4: Bootstrap CI
    N = len(test_labels)
    idx = np.arange(N)
    samples = []
    for _ in range(B):
        boot_idx = np.random.choice(idx, size=N, replace=True)
        lbl_boot = test_labels[boot_idx]
        pred_boot = test_preds[boot_idx]
        P_boot = lbl_boot.sum()
        F_boot = N - P_boot
        if P_boot == 0 or F_boot == 0:
            continue
        TPR_star = ((lbl_boot == 1) & (pred_boot == 1)).sum() / P_boot
        TNR_star = ((lbl_boot == 0) & (pred_boot == 0)).sum() / F_boot
        denom_star = TPR_star + TNR_star - 1
        if denom_star <= 0:
            continue
        theta_star = (p_obs + TNR_star - 1) / denom_star
        samples.append(np.clip(theta_star, 0, 1))

    if not samples:
        raise RuntimeError("No valid bootstrap samples; check inputs")

    L, U = np.percentile(samples, [2.5, 97.5])
    return theta_hat, L, U
```

To build intuition for how the success rate estimate varies with different LLM-as-Judge TPR and TNR, we present a small synthetic experiment. We fix the "ground truth" success rate at 80% and assume 50 human-labeled successes and 50 human-labeled failures.

![](https://substackcdn.com/image/fetch/$s_!LCFH!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11be968f-01e9-4baf-a1d5-1264c93afe71_854x364.png)

How different judge errors bias the raw pass rate and how bias-correction recovers the true 80%.

In the left plot, we assume perfect failure classification (i.e., TNR = 100%) and vary the judge's success detection (i.e., TPR) from 50% to 100%. When detection is only 50%, the uncorrected success rate drops and its 95% CI is extremely wide. As the judge improves, the red curve climbs toward 80%, the CI contracts, and the bias-corrected estimate (blue) remains close to the true value.

In the right plot, we hold true success detection (i.e., TPR) at 100% and vary TNR from 50% to 100%. At 50%, half of real failures slip through as successes—driving the uncorrected rate toward 100% and widening uncertainty. Better TNR corrects this: the red curve falls back to 80%, its confidence interval tightens, and throughout, the bias-corrected line again tracks the true 80%.

Improving the TPR—the judge's ability to correctly identify true successes—tends to narrow the confidence interval for our estimated true success rate (θ̂) the most.

**Key Takeaway**: LLM-as-Judge Alignment Priorities

- The correction reliably removes bias in both extreme error modes.
- Judge errors mainly inflate uncertainty (wider confidence intervals), rather than shifting the corrected estimate.
- Improving TPR, or the judge's ability to identify true successes, narrows the confidence interval the most.

## Common Pitfalls

The most common mistake when implementing LLM-as-Judge evaluators is omitting examples from the prompt entirely.

Without concrete examples, the model lacks grounding in what constitutes a failure for the task at hand. This often leads to vague or inconsistent behavior, even when the task definition is otherwise clear.

A second pitfall is attempting to do too much in a single [prompt.](https://www.news.aakashg.com/p/pm-prompt-library?utm_source=publication-search)

Some teams try to evaluate multiple criteria at once—tone, content correctness, next steps—in a single Pass/Fail decision. This introduces ambiguity and makes it harder to diagnose errors. Breaking complex metrics into narrower, more specific metrics and prompts yields better alignment and more reliable judges.

Another common issue is skipping the alignment step altogether.

Teams often assume the LLM-as-Judge will "just work" out of the box. Sometimes, that is true—especially for simple or broadly familiar metrics like sentiment polarity (i.e., positive or negative). But many evaluation metrics are domain-specific or tied to the unique "vibe" of a product: tone alignment for luxury clients, completeness of a listing summary, justification of a tool call. These require effort to align. Judges don't come pretrained on a product's values—we have to teach them.

Prompt refinement and human-labeled validation are essential to ensure our evaluators actually reflects what matters in our pipelines. But aligning a judge—by refining prompts and validating its agreement with human labels—is an investment that pays off enormously. An aligned judge can replace expensive human evaluation across thousands of traces, making pipeline-wide monitoring feasible.

A related pitfall is overfitting the LLM-as-Judge prompt to their labeled traces.

This often happens when teams include those same traces as examples and as part of the evaluation set used to measure alignment. This contaminates the metrics: TPR and TNR may appear high, not because the judge is generalizing well, but because it has memorized specific examples. Any trace used in the prompt must be excluded from the evaluation set.

Moreover, even after alignment, many teams fail to revisit the process.

Production data can drift. New failure modes may emerge, LLM updates may shift behavior, and evaluation metrics may evolve. We recommend re-running the alignment process regularly (e.g., weekly): continue labeling a handful of traces, recomputing TPR and TNR, and checking whether confidence intervals remain acceptably tight. If not, retrain the judge.

This is not a one-off task—it's part of the ongoing lifecycle of LLM-powered applications, much like monitoring in MLOps. When observing new failure modes in production, we can add examples of them to all three splits (train, dev, and test).

Once we've identified failure modes, implementing evaluators allows us to measure them systematically and at scale.

We define precise, failure-mode-specific metrics, prefer code-based checks when possible, and rely on LLM-as-Judge setups for more complex, nuanced, or domain-specific judgments. By aligning our judges through prompt refinement and validation against human labels, we ensure that automated evaluations reflect what we actually care about.

Evaluation is not a one-time setup. Like any robust system, it must be maintained: revisited as data shifts, retrained as definitions evolve, and monitored for continued alignment. This work is essential for any LLM-powered product that aims to be reliable, interpretable, and improvable.

*Next up: Step 3: Improve - using our measurement insights to systematically enhance pipeline performance.*

---

## The Layer Deeper: Step 3 - Improve

Based on the error analysis and online monitoring insights, we implement changes to enhance the LLM pipeline. Common strategies for pipeline improvement include:

### Refine Prompts

This is often the first and most impactful area for improvement. Small changes in wording, structure, or instructions can yield significant differences in output quality. Consider techniques such as:

**Adding Clarity and Specificity:** If the LLM struggles with ambiguity (like the "West Berkeley" vs. "Berkeley West" example), try providing more explicit instructions on how to interpret such terms or include clarifying examples directly in the prompt.

**Using Few-Shot Examples:** For specific problematic scenarios, carefully chosen examples of correct input/output pairs embedded within the prompt can effectively guide the model. Of course, we have to ensure these few-shot examples are distinct from our CI golden set to prevent data leakage and maintain the integrity of our regression tests.

For the full tactical PM playbook on AI, see [The AI PM's Playbook](https://www.news.aakashg.com/p/ai-pm-playbook).

**Encouraging Step-by-Step Reasoning:** For tasks requiring complex logic or multi-step generation, explicitly asking the LLM to "think step by step" or to break down its reasoning process before providing the final answer can improve coherence and accuracy.

### Decompose Complex Tasks

If a single LLM call struggles with a complex task, break it down into a sequence of smaller, more manageable sub-tasks.

Each sub-task can then be handled by a separate, specialized LLM call, potentially with its own tailored prompt, different model settings, or even a different underlying model optimized for that specific step.

For instance, instead of asking the real estate assistant to "find suitable properties for a client based on their preferences and draft an email summarizing these options," we could decompose this into:

(a) An LLM call to analyze the client's unstructured request and extract key preferences (e.g., location, price range, number of bedrooms).

(b) A tool call to a database or [API](https://www.news.aakashg.com/p/the-ultimate-guide-to-building-your?utm_source=publication-search) (e.g., query\_listings) using the extracted structured criteria.

(c) An LLM call to review the retrieved listings, select the most relevant ones based on softer criteria or nuances, and perhaps summarize their key features.

(d) A final LLM call to draft a personalized email to the client, incorporating the selected properties and summaries.

### Adjust Retrieval Augmented Generation (RAG) Strategies

If our pipeline uses [RAG](https://www.news.aakashg.com/p/rag-vs-fine-tuning-vs-prompt-engineering?utm_source=publication-search) and we're encountering issues like hallucinations due to irrelevant retrieved context or outdated information, focus on the retrieval mechanism.

This might involve tuning the retrieval query formulation, adjusting the chunking strategy of our source documents to create more coherent context blocks, modifying the number of documents retrieved, or implementing a re-ranking step to prioritize the most relevant chunks before they are passed to the LLM.

### Improve Tool Schemas and Descriptions

When the LLM misuses tools or generates malformed arguments for tool calls, revisit the tool's definition.

Clarify tool descriptions to be unambiguous and comprehensive.

Ensure parameter names are intuitive, and their descriptions clearly define their purpose, expected data types, formats, and any constraints.

For example, if a search\_listings tool's neighborhood parameter is causing issues, its description should be refined to specify how to handle sub-regions, common abbreviations, or known ambiguous names.

### Add or Refine Guardrails

Based on new failure modes observed, introduce new guardrails or tighten existing ones.

These are typically fast, deterministic checks (e.g., regex, schema validation, blocklists) that run before output is finalized.

Remember to balance the strictness of guardrails against the risk of them blocking valid outputs too frequently (false positives), considering the cost-benefit of each.

### Consider Fine-Tuning (Judiciously)

If [prompt engineering](https://www.news.aakashg.com/p/prompt-engineering?utm_source=publication-search), task decomposition, RAG adjustments, and tool refinements haven't sufficiently addressed a persistent and well-defined failure mode, and we have a substantial dataset of high-quality examples demonstrating the desired behavior, fine-tuning a smaller, open-source model or a proprietary model (if the provider offers such services) might be an option.

This is generally a more resource-intensive approach and should be considered when other methods prove inadequate for reaching our quality targets for specific, repeatable patterns of failure.

### The Continuous Improvement Flywheel

The practices of CI and CD do not exist in isolation. They form components of a continuous improvement cycle—i.e., a "flywheel"—that drives the iterative refinement of LLM applications.

Understanding this cycle helps teams structure their workflow for sustained quality enhancement.

The flywheel can proceed as follows:

![](https://substackcdn.com/image/fetch/$s_!U-m_!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F20ecfe0a-26fa-4fd8-a31f-863386a08b52_3600x4500.png)

1. **Develop & Analyze:** Begin with initial pipeline development (e.g., prompts, logic, tool integration). Conduct thorough Error Analysis (Section 3) on early outputs or bootstrapped data to identify key failure modes.
2. **Measure & Build Evals:** Translate qualitative failure modes into quantitative metrics. Implement automated evaluators (code-based and LLM-as-Judge) and validate them (Section 4). Use collaborative methods (Section 5) if needed to refine subjective rubrics and build a high-quality golden dataset.
3. **CI Setup:** Integrate the golden dataset and automated evaluators into the CI pipeline. Configure automated checks to prevent regressions for known issues.
4. **Deploy (CD):** Ship the LLM pipeline with online monitoring components, including observability hooks and configurations for running evaluators on sampled production traffic. Ensure judge models are pinned.
5. **Monitor Online:** Actively track corrected failure rates (θ) with confidence intervals for key metrics using production data via the observability platform. Set up dashboards and alerts for anomalies or threshold breaches.
6. **Identify Drift / New Failures:** Analyze online monitoring data, user feedback, and flagged traces (i.e., those failing online evaluation). Look for significant increases in known failure rates (drift) or new, previously unseen problems.

Example (Real Estate Agent Assistant): Monitoring reveals a spike in the "Location Ambiguity" failure rate after a new neighborhood targeting feature is deployed. Manual review shows the LLM frequently confuses "West Berkeley" with "Berkeley West" (a non-existent area).

7. **Re-Analyze:** Perform targeted Error Analysis (Section 3) on the newly identified issues. For example, confirm that the LLM struggles with directional qualifiers—terms like "West," "North," or "Upper" used to specify parts of a location (e.g., "West Berkeley")—introduced by the new feature's prompt.
8. **Update Artifacts:**
- Add examples of the new failure (e.g., "West Berkeley" confusion) to the golden dataset.
- Refine or add evaluators to detect the failure mode. Update rubrics and re-validate LLM judges (Section 4.3).
- Update CI checks to test for the new failure using the augmented golden set.
- Periodically re-run the judge alignment loop (Section 8.3).
9. **Improve Pipeline:** Based on the error analysis and online monitoring insights, implement changes to enhance the LLM pipeline.

Example (Continuing Real Estate Assistant): After observing the "West Berkeley" confusion, the team first attempts to improve the main prompt with clearer instructions for handling directional qualifiers in location names and adds a negative example (an example of what not to do). They also add "West Berkeley" vs. "Berkeley West" to their golden dataset to ensure CI catches regressions. If this prompt change isn't sufficient, they might consider decomposing the location understanding part into a separate LLM call that specifically resolves location entities before the main property search.

10. **Re-deploy:** Ship the improved pipeline and updated evaluation artifacts. Resume monitoring (Step 5) and expect failure rates to decrease.

This flywheel emphasizes that evaluation is not a one-time phase but an ongoing, iterative process. Discoveries during online monitoring feed back into error analysis, refinement of evaluation artifacts, and ultimately, pipeline improvements.

Cycling through Analyze, Measure, and Improve (Figure 2) creates a powerful feedback loop. It uses structured evaluation to systematically navigate the complexities posed by the Three Gulfs, leading to more reliable and effective LLM applications.

*This completes our deep dive into the Analyze-Measure-Improve evaluation lifecycle. Building reliable, high-quality LLM applications demands treating evaluation as an ongoing, integrated engineering discipline, not a one-off task.*

---

This was but a taste of what’s covered in Hamel’s excellent course, *[AI Evals for Engineers & PMs course](https://maven.com/parlance-labs/evals?promoCode=ag-product-growth).*

![](https://substackcdn.com/image/fetch/$s_!OrDC!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53218ddb-85bf-4f5b-8d33-4a1538184990_960x760.png)

*If you want to go further, use my code [ag-product-growth](https://maven.com/parlance-labs/evals?promoCode=ag-product-growth) to get over $800 off the course.*

*We’re also recording a podcast soon. What questions should we cover there? Sound off in the comments.*

---

POLL

### What did you think of today's post?

Awesome - 5/5

Okay - 3/5

Bad - 1/5

*Yes, you can reply to this email with more detailed questions, and we’ll answer them!*

*P.S. Consider asking your employer to [expense](https://docs.google.com/document/d/19sd2D2qdBzplZoqELn6lAWmeeLPQxMmI-bqtMS6M_xg/edit?tab=t.0#heading=h.da8c34wr6olz) an annual subscription.*

---

## Additional AI PM Content

If you’re on the journey to becoming a better AI PM, you’ll love these:

*Newsletter - AI PM Skills*

1. [Your Guide to AI Product Strategy](https://www.news.aakashg.com/p/ai-product-strategy)
2. [Ultimate Guide to AI Prototyping Tools (Lovable, Bolt, Replit, v0)](https://www.news.aakashg.com/p/ai-prototyping-tutorial)
3. [Most People are Building AI Products Wrong - Here's How to do it Right](https://www.news.aakashg.com/p/how-to-build-ai-products)
4. [The AI PM's Playbook: How Top Product Managers Are 10x-ing Their Impact](https://www.news.aakashg.com/p/ai-pm-playbook)

*Newsletter - Becoming an AI PM*

1. [How to Become an AI PM](http://how%20to%20become%20an%20ai%20product%20manager/)
2. [How to Land Your Dream Job at OpenAI](https://www.news.aakashg.com/p/how-to-break-into-openai)
3. [How to Become an AI Product Manager with No Experience](https://www.news.aakashg.com/p/become-an-ai-pm-no-experience)
4. [How to Write a Killer AI Product Manager Resume (With Examples)](https://www.news.aakashg.com/p/ai-product-manager-resume)

*Podcast - AI PM Skills*

1. [Tutorial of Top 5 AI Prototyping Tools](https://www.news.aakashg.com/p/ai-prototyping-for-pms)
2. [Complete Course: AI Product Management](https://www.news.aakashg.com/p/complete-course-ai-product-management)
3. [We Built an AI Agent to Automate PM in 73 mins (ZERO CODING)](https://open.spotify.com/episode/5NpxUr9RmY7DEGFuhCADJI)
4. [15 Steps to Build a $100M+ AI Company (From Someone Who Has Done It)](https://podcasts.apple.com/kw/podcast/15-steps-to-build-a-%24100m-ai-company-from-someone/id1763555775?i=1000708181201)
5. [We Built an AI Product Manager in 58 mins (Claude, ChatGPT, Loom, Notion AI)](https://www.youtube.com/watch?v=sLI4KCjGXdQ)
	---
	## FAQ
	**What are AI evals?**
	AI evaluations (evals) are the systematic measurement of LLM pipeline quality. Unlike traditional software testing, evals assess probabilistic outputs for accuracy, tone, completeness, and generalization failures.
	**Why do Product Managers need AI evals?**
	Just like you can't be a Product Manager without analytics, you can't be a Product Manager on AI products without evals. They're how you measure and improve LLM pipeline quality. If you're starting from zero, [How to Become an AI PM With No Experience](https://www.news.aakashg.com/p/become-an-ai-pm-no-experience) covers the full roadmap.
	**What’s the best AI evals course for Product Managers?**
	Hamel Husain’s AI Evals for Engineers & Product Managers is the most recognized course in the industry. Use code ag-product-growth for $800 off.
	**How do AI evals differ from regular software testing?**
	Regular software is deterministic — same input, same output. LLMs are probabilistic. Evals handle this by measuring failure rates across representative data, not pass/fail on single cases.
	**What are the three types of AI evals?**
	Background monitoring (passive), guardrails (in the critical path), and improvement evals (for fine-tuning and prompt refinement).

---
*Clipped from [aakashg.com](https://www.news.aakashg.com/p/ai-evals) on 2026-05-12T16:06:43-04:00*
