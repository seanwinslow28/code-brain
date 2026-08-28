# AI Quiz

## Question 1
According to 2026 practitioner discourse, which component is identified as the primary bottleneck in a real AI loop?

- [ ] The reasoning capability of the underlying model.
- [x] The verifier or evaluator within the system.
- [ ] The latency of the tool-calling interface.
- [ ] The size of the context window.

**Hint:** Consider the key claim made by the 'AI Builder Club' regarding what prevents a loop from closing effectively.

## Question 2
In the context of 'Loop Engineering,' which three factors define the 'Stop Condition' for an autonomous improvement system?

- [x] Target, Budget, and Stall detector.
- [ ] Accuracy, Latency, and Cost-per-token.
- [ ] Human review, Model version, and Prompt length.
- [ ] Memory, Context, and Tool availability.

**Hint:** The stop condition is designed to prevent a system from becoming an 'automated billing machine' without progress.

## Question 3
Why is the use of a 'Holdout Set' critical in the Champion/Challenger pattern of AI product development?

- [ ] It provides a larger volume of data for synthetic generation.
- [x] It prevents the system from optimizing for the grading set (Goodhart's Law).
- [ ] It allows engineering to skip the manual labeling phase.
- [ ] It is used to store historical model weights for rollbacks.

**Hint:** Think about the risk of 'teaching mimicry' of the practice cases rather than general quality.

## Question 4
Which metric is recommended as the 'target' for calibrating an LLM-as-a-judge against human expert verdicts?

- [ ] A raw agreement rate of $100\%$.
- [x] A Pearson correlation coefficient ($r$) above $0.7$.
- [ ] A minimum p99 latency under $200$ ms.
- [ ] A token-usage efficiency ratio of $1.5$.

**Hint:** Look for the specific mathematical threshold cited in the Galtea and Hamel Husain sources for human-judge alignment.

## Question 5
The 'Agentic AI Institute' suggests that 2026 products are 'harnesses' rather than just models. How is 'Harness Quality' calculated?

- [ ] Model Parameters $\times$ Dataset Size.
- [x] Plan quality $\times$ Context quality $\times$ Eval quality.
- [ ] Prompt length $\times$ Tool availability $\times$ User feedback.
- [ ] Latency $\times$ Cost $\times$ Throughput.

**Hint:** Think of the three named pillars that distinguish a sophisticated AI system from a simple prompt-response slot machine.

## Question 6
Which common evaluation practice is cited as 'weak' because it is easily gamed by models seeking to please the evaluator?

- [ ] Binary checks on specific factual criteria.
- [x] Likert scales (e.g., 'rate this 1–10').
- [ ] Exact string matching for JSON keys.
- [ ] Embedding-based similarity scores.

**Hint:** This evaluation style is described as 'a vibe with a number attached' in the M7 curriculum.

## Question 7
In the context of metrics architecture, what is 'Proxy Decay'?

- [ ] The degradation of model weights over repeated fine-tuning.
- [x] The phenomenon where an offline metric no longer correlates with real-world product outcomes.
- [ ] A failure in the vector database causing retrieval scores to drop.
- [ ] The reduction in user engagement when an AI feature is too slow.

**Hint:** Consider how the relationship between offline 'simulations' and online 'reality' might change over time.

## Question 8
According to the 'Agent Development Lifecycle (ADLC),' where do evals primarily do the 'heavy lifting'?

- [ ] During model training and pre-training data collection.
- [x] During testing (to catch regressions) and monitoring (to catch drift).
- [ ] In the legal review phase and marketing launch prep.
- [ ] Solely in the initial ideation and PRD writing phase.

**Hint:** Think about the repeating loop of building, testing, deploying, and monitoring.

## Question 9
What is the 'one-change rule' in professional loop engineering and why is it enforced?

- [ ] Changing one user persona at a time to keep the dataset small.
- [x] Proposing exactly one change per round to isolate what caused a score to move.
- [ ] Restricting the model to one tool call per session to save on costs.
- [ ] Updating the golden dataset only once per quarter to maintain stability.

**Hint:** This discipline is part of the Champion/Challenger pattern used to ensure scientific iteration.

## Question 10
A Senior Google AI PM describes a 'real loop' as having specific anatomy. Which of the following is NOT one of those parts?

- [ ] Guardrails
- [ ] Stop condition
- [ ] Memory
- [x] Static PRD

**Hint:** The anatomy focuses on the active system components: goal, context, actions, tools, evals, memory, guardrails, and stop logic.
