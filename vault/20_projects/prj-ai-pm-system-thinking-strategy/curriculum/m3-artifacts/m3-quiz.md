# AI Quiz

## Question 1
According to the systems thinking hierarchy for FinOps, which intervention point is considered the least effective for fundamentally changing system behavior?

- [x] Constants and Parameters (e.g., setting targets for 100\% cost tagging)
- [ ] Information Flows (e.g., providing team-level split-up bills)
- [ ] Rules and Guidelines (e.g., hosting policies for IaaS vs. PaaS)
- [ ] Mental Models and Paradigms (e.g., shifting from 'cost' to 'value')

**Hint:** Consider the order of leverage points where the most tangible, numerical items often provide the least lasting impact.

## Question 2
The collapse of Zillow Offers is attributed by experts to a failure in managing which specific AI-specific dynamic?

- [ ] Reward hacking within the model's objective function
- [x] Concept drift due to macroeconomic shifts
- [ ] The 'Success to the Successful' archetype
- [ ] Degenerate feedback loops in the pricing algorithm

**Hint:** Think about what happens when the future no longer resembles the past data used for training.

## Question 3
In the 'cost-quality-latency triangle,' what is a common 'death spiral' associated with attempting to fix quality issues in an LLM-backed product?

- [x] Adding verification passes leading to increased latency and user abandonment
- [ ] Switching to cheaper models leading to unmanaged model drift
- [ ] Implementing semantic caching leading to outdated responses
- [ ] Scaling context windows leading to uncapped token spend

**Hint:** Focus on the negative feedback loop triggered by adding complexity to the inference chain.

## Question 4
What is the primary danger of implementing 'Model Routing' (dispatching to cheaper models) without a continuous evaluation gate?

- [ ] High latency overhead from the routing layer
- [x] Silent quality regression that surfaces only after a delay
- [ ] Immediate 100x increase in input token costs
- [ ] Provider rate-limiting on frontier model endpoints

**Hint:** Consider the gap between immediate financial metrics and long-term user trust.

## Question 5
In the context of AI product management, how is the 'Verification Tax' defined?

- [x] The hidden labor cost of human auditing for probabilistic outputs
- [ ] The 5\% surcharge added by routing providers like OpenRouter
- [ ] The cost of using LLMs-as-judges for automated quality assurance
- [ ] The compute cost associated with RLHF retraining loops

**Hint:** Think about the manual effort required to ensure that a 'free' machine-generated output is actually usable.

## Question 6
Which classical systems thinking framework was used to analyze the competing organizational priorities at OpenAI during its 2023 leadership crisis?

- [ ] Meadows' Leverage Points
- [x] The Iceberg Model
- [ ] Senge's System Archetypes
- [ ] Stock-and-Flow Modeling

**Hint:** This model is often used to distinguish between surface-level events and deep-seated mental frameworks.

## Question 7
What is the 'Transfer Property' of a well-designed model router, as noted in the RouteLLM research?

- [ ] The router can instantly move data from IaaS to SaaS environments
- [x] The router maintains performance even if the underlying models are swapped
- [ ] The router allows users to transfer credits between different cloud providers
- [ ] The router can automatically transfer prompts from text to multimodal models

**Hint:** Consider how a router remains useful in a market where technology updates happen monthly.

## Question 8
Which term describes a model confidently providing incorrect information because it fundamentally lacks the necessary data to provide a factual answer?

- [ ] Aleatoric uncertainty
- [x] Epistemic uncertainty
- [ ] Semantic drift
- [ ] Reward hacking

**Hint:** This type of uncertainty is often contrasted with 'aleatoric' or statistical randomness.

## Question 9
Why is 'Semantic Caching' described as a 'loop-breaker' in the context of AI cost management?

- [x] It removes repeated calls from the billing meter entirely
- [ ] It identifies and stops recursive agent loops
- [ ] It prevents model drift by ensuring outputs remain constant
- [ ] It replaces expensive frontier models with cheaper local models

**Hint:** Consider what happens to the 'meter' when an answer is retrieved from memory rather than generated.

## Question 10
In Senge's system archetypes, the reliance on 'prompt engineering' to fix usability issues instead of building structured UIs is an example of:

- [ ] Success to the Successful
- [x] Shifting the Burden
- [ ] The Rebound Effect
- [ ] Tragedy of the Commons

**Hint:** This archetype involves a symptomatic 'fix' that makes the long-term solution harder to implement.
