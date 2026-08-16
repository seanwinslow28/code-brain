# AI Quiz

## Question 1
According to the Scrum.org article, why has the discipline of 'writing as little code as possible' become more urgent with the rise of AI?

- [ ] AI coding tools have increased the cost of human-written code compared to generated output.
- [x] Generation cost has collapsed, but the cost of validating and maintaining that code has not.
- [ ] AI models are currently incapable of writing complex logic, requiring humans to simplify their codebases.
- [ ] Technical debt is easier to manage when AI generates the majority of the documentation.

**Hint:** Consider the relationship between implementation speed and the scarcity of product judgment.

## Question 2
In the context of Systems Thinking for AI PMs, which layer of the Iceberg Model is addressed when resolving a conflict by investigating foundational beliefs about safety versus speed?

- [ ] Events
- [ ] Patterns
- [ ] Underlying Structures
- [x] Mental Models

**Hint:** Think about the level that deals with the fundamental 'why' behind organizational architectures.

## Question 3
What does the 'RAG Triad' metric 'Faithfulness' specifically measure in an LLM application?

- [ ] Whether the generated answer addresses the specific intent of the user's query.
- [ ] The percentage of relevant documents found within the top-$k$ results of a vector search.
- [x] Whether the generated answer is derived solely from the provided retrieved context.
- [ ] The semantic similarity between the user's query and the final response.

**Hint:** Focus on the relationship between the final output and the grounding source material.

## Question 4
Which stage of the 'Promptware' kill chain is defined by the model's willingness to bypass safety constraints it was trained to follow?

- [ ] Initial Access
- [x] Privilege Escalation
- [ ] Reconnaissance
- [ ] Command and Control

**Hint:** Think of the process of 'liberating' the model from its safety training boundaries.

## Question 5
According to Realm Labs, why do many AI projects fail despite having strong guardrails and observability?

- [x] Current tools only see behavior from the outside and cannot explain the internal reasoning process.
- [ ] AI models are fundamentally incompatible with legacy cloud authentication layers.
- [ ] The 95% failure rate is primarily driven by content that users find uninteresting or irrelevant.
- [ ] Most guardrails introduce too much latency, causing users to abandon the application.

**Hint:** Consider the difference between watching what an AI does versus understanding why it did it.

## Question 6
In the Promptware kill chain, how does 'Retrieval-Independent Persistence' differ from 'Retrieval-Dependent Persistence'?

- [ ] It requires the attacker to manually re-inject the payload during every user session.
- [x] It relies on the model's memory features to infect every subsequent interaction regardless of the query.
- [ ] It only triggers when a user searches for a specific keyword that is semantically similar to the poisoned document.
- [ ] It is characterized by the use of images and audio rather than textual prompts.

**Hint:** Look for the mechanism that ensures a payload is active even without a specific search query.

## Question 7
Which Systems Thinking archetype explains why optimizing local data center efficiency can paradoxically lead to higher overall energy consumption?

- [ ] Success to the Successful
- [x] The Rebound Effect (Meadows' Leverage Points)
- [ ] Shifting the Burden
- [ ] Limits to Growth

**Hint:** Think about a concept where a shallow intervention results in unintended systemic expansion.

## Question 8
In LLM observability, what is a primary advantage of the 'SDK approach' over the 'Proxy approach'?

- [ ] It requires zero code changes to implement, making it faster to deploy across large teams.
- [x] It provides visibility into internal variables and control flow decisions that never cross the network.
- [ ] It acts as a centralized gateway for managing multiple model providers and API keys.
- [ ] It is less likely to be affected by prompt drift compared to network-based solutions.

**Hint:** Consider which method has deeper access to the logic occurring before an API call is made.

## Question 9
The 2021 collapse of Zillow Offers is cited as a failure of systemic AI governance due to which specific system dynamic?

- [ ] Model Monoculture
- [ ] Degenerate Feedback Loops
- [x] Concept Drift and Adverse Selection
- [ ] Reward Hacking

**Hint:** Focus on the gap between historical training data and a rapidly cooling real-world market.

## Question 10
How does 'Comprehension Debt' impact a development team according to the Comet and Scrum.org sources?

- [ ] It occurs when the cost of API tokens exceeds the project's allocated budget.
- [x] It happens when teams merge AI-generated code that they cannot explain or reason through.
- [ ] It refers to the time lost while waiting for an LLM to generate a complex pull request.
- [ ] It is a measure of the statistical uncertainty in a model's output given a new prompt.

**Hint:** Think about the consequence of increasing code volume without increasing understanding.
