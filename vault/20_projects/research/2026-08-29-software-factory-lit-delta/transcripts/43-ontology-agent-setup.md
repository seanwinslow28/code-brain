# Ontology-Agent-Setup-ChatGPT-Pro.md

Source: notebook-uploaded document — NotebookLM-indexed fulltext, dumped 2026-08-29. Transcript text is auto-generated; names/products may be mis-transcribed.

Designing the Environment: A Deep Research Report on Mitch Troyanovsky’s Agent Engineering Philosophy
Research checked through August 14, 2026. I use the official spelling 
Mitchell Troyanovsky
; the transcripts contain several phonetic transcription errors, including his surname.
 (
Basis
https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents
)
The Troyanovski Thesis
Troyanovsky’s underlying thesis is not really about agents as a new application category. It is about 
how to turn abundant but discontinuous intelligence into dependable labor
.
In plain English:
A frontier model may already be intelligent enough to do a surprising amount of professional work. What it lacks is the stable world, persistent state, organizational knowledge, feedback, authority structure, and supervision that allow intelligence to operate coherently for hours, days, or months.
In his model:
The model supplies intelligence.
The harness supplies agency and execution mechanics.
The ontology supplies a legible world.
Context supplies the relevant slice of that world for the present decision.
Tools supply capabilities and environmental feedback.
Memory and state preserve continuity across otherwise fresh inference calls.
Behavior specifications define the small number of recurring choices the organization cares enough to supervise.
Verification and evaluation determine whether the agent’s work—and the way it performed that work—can be trusted.
Trajectory analysis turns failures into improvements to context, tools, workflows, and eventually perhaps model training.
Governance determines how much authority the system is allowed to exercise.
That is why his definition of an agent emphasizes 
agency rather than raw intelligence
: the important change occurs when a model can decide not only 
what
 answer to produce, but 
how
 to acquire information, use tools, pursue alternatives, and act in an environment. He treats autonomy as a spectrum determined by the choices and capabilities exposed to the model.
His definition of autonomous work is also more conservative than “the agent acted without a human.” For Basis, autonomy means the agent can carry a job from initiation to a reviewable completion state, while surfacing its assumptions, important decisions, unresolved questions, and evidence in a form that makes professional review efficient. It is closer to a junior employee submitting a carefully prepared work product than a black box announcing that it is done.
The Memento problem
The central technical problem in Troyanovsky’s worldview is what I would call 
discontinuous cognition
.
An LLM inference has a large working context, but it does not naturally consolidate its experiences into stable medium- and long-term memory. Once information falls out of the active context—or a new run begins—the next inference may have little awareness of what the previous inference learned, attempted, or decided. His 
Memento
 analogy is therefore not decorative. It is the architectural problem around which much of the rest of his thinking is organized.
A long-horizon system must continually answer:
What must Past Agent leave in the environment so that Future Agent can recover the relevant state of mind without replaying the entire history?
From that question follow:
external notes;
structured progress state;
artifact references;
evidence ledgers;
checkpoints;
context compaction;
progressive disclosure;
canonical documentation;
ontology;
agent-readable tools;
subagents with isolated context;
trajectory logs;
and explicit completion criteria.
Anthropic’s long-running-agent experiments independently found the same failure pattern: a new context often starts without enough knowledge of the previous session, compaction alone can omit crucial information, and agents perform better when each session makes incremental progress while leaving clear artifacts and progress records for its successor. (
Anthropic
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
)
The deeper organizational analogy
Troyanovsky treats companies as systems already designed to coordinate nondeterministic intelligences: people. Human organizations use goals, roles, policies, procedures, independent review, escalation, institutional memory, and management precisely because humans cannot be controlled like deterministic functions. He argues that agent architecture can borrow from this accumulated organizational knowledge.
That analogy explains why Basis talks about:
agent managers;
language architects;
deployed intelligence;
canonical organizational knowledge;
agent-native documentation;
and progressively granting agents more agency as they establish reliability.
Basis’s later writing is consistent with the talks rather than an isolated rhetorical flourish. Its public material repeatedly describes agents as a new form of intelligence requiring management, context architecture, organizational redesign, and professional deployment—not merely another software feature. (
Basis
https://www.getbasis.ai/blogs/introducing-deployed-intelligence
)
My one-sentence synthesis
Reliable agent engineering is the discipline of designing a legible, feedback-rich, stateful, governed environment in which a nondeterministic model can repeatedly make good decisions—and where failures become observable evidence rather than silent drift.
That is the strongest version of the Troyanovsky thesis.

--------------------------------------------------------------------------------

Claim Classification
I would classify his major claims this way:
Troyanovsky claim
Classification
My assessment
Agency is distinct from intelligence and exists on a spectrum.
A — strongly supported
A useful and durable definition. Authority and environment, not model IQ alone, determine what an agent can do.
Long-horizon performance is fundamentally a coherence and state-management problem.
A
Strongly supported by current harness, memory, and context-engineering work.
Runtime verification is a major reason coding agents are effective.
A
Correct, although training data, tool quality, and domain representation also matter.
Correct outcomes can hide unacceptable processes.
A
Well established in safety, software, research, finance, and process-supervision work.
Canonical knowledge and context quality materially affect agent behavior.
A
Correct. Conflicting and stale context produces real regressions.
Context is “runtime training data.”
B — plausible heuristic
A powerful metaphor, but technically it is conditioning, not parameter learning or durable training.
A coherent ontology is the most important part of agent building.
B/C — heuristic and Basis-specific emphasis
Stable concepts and authority are important; a formal ontology is not always necessary.
Sparse behavior specs can supervise important recurring conduct.
B
Promising and well conceived, but still young and dependent on good judges and representative traces.
Behavior specs should generally be separate from what the agent sees.
C — Basis-specific design choice
Valuable for observational evaluation, but not a universal default. Sometimes the behavior must also be encoded in runtime policy.
Human organizational design is a strong model for multi-agent architecture.
B
Useful for delegation, review, and authority; misleading when taken literally.
Fresh agents produce “uncorrelated” review trajectories.
B
Fresh context reduces trajectory anchoring, but shared models, data, and prompts still create correlated errors.
Horizontal agent infrastructure compounds as models improve.
A/B
Correct when the abstraction is genuinely reusable; dangerous when it becomes a speculative universal platform.
Agents will soon close much of their own improvement loop.
B/D — heuristic plus speculation
Pieces are practical now, but fully autonomous, generalizable improvement remains experimental.
Harness engineering will be swallowed by models within roughly five years.
D — forward-looking speculation
Some context and orchestration mechanics will move into models; external state, permissions, audit, tools, and organizational canon will not disappear.
Process-oriented reward may be necessary for agents to perform professional work reliably.
D
Plausible, but not established across domains.
Reliability and consistency are more commercially valuable than occasional “Move 37” brilliance.
A/B
Usually correct for repeated production work, though discovery and creative domains may value controlled exploration more highly.
Troyanovsky explicitly marks several of his claims about model training, lab strategies, self-improvement, and future RL as speculation. Those caveats should be preserved rather than converted into facts.

--------------------------------------------------------------------------------

Transcript Verification and Corrections
The transcripts are broadly intelligible, but several names and terms are garbled.
Transcript wording
Likely intended reference
Verification or qualification
“Mitch Troyki” / “Troyanovski”
Mitchell Troyanovsky
Official Basis spelling. (
Basis
https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents
)
“Momento”
Memento
Christopher Nolan’s film and Troyanovsky’s memory analogy.
“React”
ReAct: Synergizing Reasoning and Acting in Language Models
Introduced a reasoning-and-action loop in 2022 and appeared at ICLR 2023. (
arXiv
https://arxiv.org/abs/2210.03629
)
“Baby AI”
BabyAGI
Yohei Nakajima’s 2023 task-driven experimental loop. Its own repository framed it as a minimal experiment rather than production architecture. (
GitHub
https://github.com/yoheinakajima/babyagi
)
“Autogi”
Probably 
AutoGPT
The context is early autonomous-agent projects.
“GBD4,” “GPD5”
GPT-4
, 
GPT-5
Straightforward transcription errors.
“Opus 3”
Claude 3 Opus
Released with a 200,000-token context window in March 2024. (
Anthropic
https://www.anthropic.com/news/claude-3-family
)
“01,” “03”
OpenAI o1 and o3
The first character is the letter 
o
.
“Let’s Verify Step by Step”
OpenAI’s process-supervision paper
The accompanying PRM800K dataset contains roughly 800,000 step-level correctness labels for mathematical reasoning. (
arXiv
https://arxiv.org/abs/2305.20050
)
“Reinforcement learning from verifiable rewards”
RLVR
A family of approaches using automatically checkable reward signals. DeepSeek-R1-Zero used RL without initial supervised chain-of-thought data, while the full R1 system also used supervised fine-tuning and multiple RL stages. (
arXiv
https://arxiv.org/abs/2501.12948
)
“Meter chart”
METR task-completion time horizon
METR measures the human-expert duration of tasks an agent can complete at a given reliability—not the literal length of time the agent can remain active. (
Metr
https://metr.org/time-horizons/
)
“Brand Trust”
Braintrust
Basis and Braintrust jointly released the behavior-specification standard. (
GitHub
https://github.com/braintrustdata/agentbehavior
)
“Anker”
Ankur Goyal
Braintrust CEO.
“FDEs in a balancer context”
Probably 
forward-deployed engineers in a Palantir context
The surrounding comparison is to customer-facing deployment roles.
“Codex is open source”
Codex CLI is open source
The CLI/reference implementation is open; that should not be generalized to every Codex product or service. (
GitHub
https://github.com/openai/codex
)
“Luna costs is free”
Probably inexpensive 
GPT-5.6 Luna
 inference or cheap inference generally
The sentence is too garbled to recover with confidence.
“symposent… Dark a good blog”
Unresolved
I could not confidently identify the intended author or post from the transcript alone. It should not be cited as a verified reference.
The METR claim needs the most qualification
The original METR work found an approximately seven-month historical doubling in the 
50%-success task horizon
 for a suite dominated by software, machine-learning, and cybersecurity tasks. But METR itself emphasizes that:
the horizon is based on how long the task takes a human, not agent wall-clock runtime;
the suite contains relatively clean, self-contained, automatically evaluated tasks;
the measurements do not imply that agents can perform every task of that duration;
they do not imply job automation;
and high-reliability horizons such as 99% cannot currently be measured robustly without much larger and more diverse task suites. (
Metr
https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/
)
Troyanovsky’s instinct that the chart is directionally meaningful but easy to overread is correct.

--------------------------------------------------------------------------------

The Principles I Think He Is Right About
1. The model is not the system
Transcript.
 Troyanovsky repeatedly argues that the model may already possess substantial latent ability, while the application fails because it gives the model the wrong context, tools, environment, or feedback.
Research.
 This is one of the clearest points of convergence across serious agent engineering. OpenAI’s harness-engineering work reports that failures were often caused not by insufficient model capability but by an underspecified environment lacking the necessary abstractions, tools, structure, and feedback. Its engineers reframed their job as designing environments, specifying intent, and constructing feedback loops. (
OpenAI
https://openai.com/index/harness-engineering/
)
Anthropic similarly recommends beginning with the simplest possible agentic structure and improving the tool and context environment before adding elaborate orchestration. (
Anthropic
https://www.anthropic.com/engineering/building-effective-agents
)
Recommendation.
 When an agent fails, do not begin with “Which model should I swap in?” Ask:
Was the goal clear?
Did it know which sources were authoritative?
Could it observe the relevant environment?
Did it have an appropriate action?
Could it verify the effect of that action?
Was important state preserved?
Did it know when it was done?
Was the action actually permitted?
That diagnostic sequence will improve more systems than reflexive model switching.

--------------------------------------------------------------------------------

2. Long-horizon execution is not one giant inference
Transcript.
 Troyanovsky defines long horizon as the point at which maintaining coherence itself becomes an engineering problem. It can arise because the trajectory exceeds the context window, because context quality degrades before the formal limit, or because work must continue across separate runs.
Research.
 Long context does not eliminate context pollution, positional degradation, or relevance problems. “Lost in the Middle” found that performance can depend substantially on where relevant information appears, while RULER showed that many models’ effective performance degrades as long-context tasks require more retrieval, aggregation, or multi-hop reasoning. (
arXiv
https://arxiv.org/abs/2307.03172
)
Anthropic’s current guidance treats compaction, structured note-taking, and selective subagent isolation as distinct techniques. It also warns that aggressive compaction can irreversibly discard details that only become important later. (
Anthropic
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
)
Recommendation.
 Think of long-horizon execution as a sequence of bounded cognition episodes over durable external state:
fresh inference


↓


read current state and evidence


↓


perform one bounded unit of work


↓


write artifacts, decisions, and checkpoint


↓


verify


↓


continue in current context or start fresh
A longer context window is useful capacity. It is not an architecture.

--------------------------------------------------------------------------------

3. Canonical organizational knowledge is executable infrastructure
Transcript.
 Troyanovsky argues that an agent cannot rely on tacit organizational knowledge. It needs to know which document reflects current policy, which records are historical, and which source wins when two sources conflict.
The second talk makes the stronger claim that deleting a crucial paragraph of context can change agent behavior as materially as deleting a line of code changes application behavior.
Research.
 Basis’s agent-native codebase work operationalizes this through an authority map:
every artifact is either current canon or a record of intent/history;
context is localized near its use;
automatically loaded context follows a “default no” policy;
and agents must have mechanisms to verify their work. (
Basis
https://www.getbasis.ai/blogs/how-we-made-our-monorepo-ergonomic-for-agents
)
OpenAI independently describes short top-level instruction files as maps into a structured documentation system rather than containers for every rule. Its agent-first engineering work similarly treats documentation, plans, observability, tests, and feedback as part of the operating environment. (
OpenAI
https://openai.com/index/harness-engineering/
)
Recommendation.
 Treat agent-facing documentation as versioned production configuration:
assign owners;
mark authority and scope;
distinguish current truth from historical intent;
include review dates;
lint links and references;
test changes against evals;
and roll back context changes when they cause regressions.
“Documentation as code” should mean 
ownership, tests, review, versioning, and blast-radius awareness
, not merely storing Markdown in Git.

--------------------------------------------------------------------------------

4. Agents become dramatically stronger when the environment talks back
Transcript.
 Troyanovsky’s insight about coding is that code can often be compiled, executed, tested, rendered, or inspected at runtime. An agent that can see a syntax error, failing test, or broken artifact receives immediate information with which to correct itself.
Research.
 This principle appears repeatedly in successful systems:
AlphaEvolve pairs generated programs with objective automated evaluators. (
Google DeepMind
https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
)
FunSearch similarly couples generation to executable evaluation. (
Google DeepMind
https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/
)
OpenAI’s harness work exposes tests, logs, metrics, and isolated execution environments to coding agents. (
OpenAI
https://openai.com/index/harness-engineering/
)
Basis reports that rough tool interfaces become cascading failure sources on long investigations and improved Clueso by giving it better tools, saved evidence, and progress logs. (
Basis
https://www.getbasis.ai/blogs/clueso-how-we-built-an-agent-that-autonomously-resolves-78-of-bugs
)
Recommendation.
 In every domain, ask:
What could the environment return that would make error visible before the agent declares completion?
For non-coding work, runtime feedback can include:
schema validation;
accounting invariants;
spreadsheet formula checks;
duplicate detection;
citation resolution;
source-authority checks;
rendered visual artifacts;
simulation results;
policy engines;
database constraints;
reconciliation totals;
comparison against known exemplars;
adversarial review;
user-state confirmation;
and human approval.
The strongest agent systems do not merely give the model more instructions. They give it 
better consequences and better evidence
.

--------------------------------------------------------------------------------

5. Outcomes alone do not establish trust
Transcript.
 The accounting example is compelling: an agent may reach the correct tax conclusion by recalling it from model weights or reading an informal blog, while professional practice requires consulting and citing authoritative primary material. A correct answer is therefore not sufficient evidence that the process is repeatable or defensible.
Research.
 OpenAI’s process-supervision work showed that evaluating intermediate reasoning steps can outperform outcome-only supervision in mathematical settings. More generally, both OpenAI and Anthropic now recommend evaluating traces, tool choices, handoffs, guardrail behavior, and resulting environment state—not just final prose. (
OpenAI
https://openai.com/index/improving-mathematical-reasoning-with-process-supervision/
)
Recommendation.
 Production agents should usually be evaluated along separate dimensions:
Outcome correctness
 — Was the requested result achieved?
Artifact validity
 — Is the file, code, workbook, or record structurally usable?
Behavioral adherence
 — Did the agent exhibit the important recurring conduct?
Provenance
 — Can its claims and transformations be traced to evidence?
Safety and authority
 — Did it remain within permissions?
Reliability
 — Does it work consistently over the relevant distribution?
Efficiency
 — Did it use reasonable time, cost, and actions?
Escalation quality
 — Did it identify situations it should not resolve alone?
Collapsing those into one “pass” score hides too much.

--------------------------------------------------------------------------------

6. Sparse behavior specifications are better than sprawling rulebooks
Transcript.
 Troyanovsky argues that behavior specs are expensive because they create state that must be maintained. He therefore recommends specifying only a small number of recurring, high-impact behaviors that generalize meaningfully across production trajectories.
Research.
 The released Basis/Braintrust standard follows that principle. A behavior earns a specification only when it describes a recurring choice, someone is willing to stand behind it, a trajectory can supply evidence about it, and the behavior is worth maintaining as a standing evaluation. The public format uses a 
BEHAVIOR.md
 file and commonly describes intent, evidence, decision, execution, recovery, and failure modes. (
Basis
https://www.getbasis.ai/blogs/behavior-specs-an-open-standard-for-supervising-long-horizon-agents
)
That is substantially more promising than treating a behavior spec as another giant prompt.
Recommendation.
 A behavior deserves an explicit spec when all of the following are true:
It recurs across many tasks.
It materially affects trust, quality, safety, or product identity.
Reasonable people could disagree about the desired conduct.
The organization is willing to make and maintain that decision.
Observable trajectory evidence can support a judgment.
Failing it should produce a concrete improvement action.
Do not create a behavior spec for every preference.

--------------------------------------------------------------------------------

7. The agent is a new customer of software architecture
Transcript.
 Troyanovsky argues that software traditionally had two customers: the end user and future engineers. Tool-using agents add a third. Tool names, contracts, responses, errors, and stability must therefore be designed for model comprehension.
Research.
 Anthropic describes tools as contracts between nondeterministic agents and deterministic systems and emphasizes clear descriptions, non-overlapping capabilities, stable identifiers, and high-signal outputs. Basis found that tool ambiguity that was tolerable over five turns could become a major failure source over hundreds. (
Anthropic
https://www.anthropic.com/engineering/writing-tools-for-agents
)
Recommendation.
 An agent-native tool should have:
one clear purpose;
an unambiguous name;
typed inputs;
typed outputs;
explicit side effects;
stable entity identifiers;
bounded response size;
actionable error states;
idempotency where possible;
permission metadata;
and a way to verify the resulting state.
MCP can standardize the connection surface, but MCP does not automatically make a tool coherent, safe, or useful.

--------------------------------------------------------------------------------

8. Trajectories are production data, not debugging exhaust
A ten-hour run is not a black box. It is a rich record containing:
retrieved evidence;
tool calls;
actions;
state transitions;
alternative paths;
errors;
retries;
assumptions;
subagent handoffs;
verifications;
and moments of escalation or premature completion.
OpenAI’s current evaluation guidance explicitly recommends trace grading to diagnose workflow-level failures such as wrong tools, inappropriate handoffs, and instruction violations. Anthropic likewise frames agent evaluations around multi-turn interaction and environment state. (
OpenAI Developers
https://developers.openai.com/api/docs/guides/agent-evals
)
Recommendation.
 Your trace should be rich enough to answer:
What did the agent believe?
What evidence was available?
What action did it take?
What changed in the environment?
Which validator ran?
What did the validator observe?
Which behavior applied?
Why did the run continue, stop, retry, or escalate?
Which model, context version, tool version, and policy version were active?
Without that information, failure analysis becomes storytelling.

--------------------------------------------------------------------------------

9. Reliability earns autonomy
Troyanovsky is right that production users generally purchase 
predictable useful work
, not isolated moments of brilliance. A firm can gradually trust a worker who is consistent, legible, and easy to review. The same principle applies to agents—but the trust should be encoded in task-scoped controls, not vague anthropomorphism.
Current long-horizon safety evidence strengthens this point. OpenAI reported that long-running behavior exposed failures that were not captured by shorter-horizon evaluations, leading it to pause access, create incident-derived evals, add trajectory-level monitoring, and redeploy under tighter controls. (
OpenAI
https://openai.com/index/safety-alignment-long-horizon-models/
)
Recommendation.
 Grant autonomy by task class and action class:
read-only research may earn broad autonomy;
internal draft creation may require post-run review;
external communication may always require approval;
financial transfer or destructive deletion may require dual control regardless of historical accuracy.
An agent should not earn a global “trusted” label.

--------------------------------------------------------------------------------

The Principles That Need Qualification
1. Context is not literally runtime training data
The metaphor is useful because context:
changes model behavior;
provides examples and concepts;
can teach local vocabulary;
supplies procedural instructions;
and determines which evidence is available for inference.
But it breaks down technically.
Training changes model parameters through an optimization process. In-context learning conditions a forward pass on tokens or other model inputs. The learned behavior generally does not persist after the context is removed. The model may ignore, misread, or inconsistently apply context, and the same context may behave differently across model versions or sampling conditions.
A better mental model is:
Context is the agent’s dynamically compiled cognitive environment.
It is more like a combination of working memory, reference material, task briefing, interface specification, and local precedent than true training.
This distinction matters because you should not assume that placing a fact in context means it has been reliably “learned.”

--------------------------------------------------------------------------------

2. Capture as much as possible; load as little as necessary
Early in the first transcript, Troyanovsky recommends giving AI as much context as possible and describes spoken input as a way to transmit rich, unsummarized human thought.
Later Basis material emphasizes “default no”: automatically loaded context must earn its place. (
Basis
https://www.getbasis.ai/blogs/how-we-made-our-monorepo-ergonomic-for-agents
)
Those positions are compatible only when you distinguish 
capture
 from 
runtime disclosure
:
Capture human intent richly.
Preserve raw source material.
Structure and index it.
Load only the subset relevant to the present decision.
Keep the rest accessible through tools or references.
Dumping every meeting, document, memory, and policy into every inference is not context engineering. It is context pollution.

--------------------------------------------------------------------------------

3. “Ontology” is being used broadly
In formal knowledge representation, an ontology defines classes, properties, relations, individuals, and semantic constraints. OWL, for example, gives those concepts formally defined meaning and can support consistency checking or inference. RDF represents claims as a labeled graph of relationships. (
W3C
https://www.w3.org/OWL/
)
Troyanovsky uses 
ontology
 more broadly. In practice he appears to mean a combination of:
domain vocabulary;
entity identities;
relationships;
authority mapping;
information architecture;
filesystem organization;
tool vocabulary;
canonical knowledge;
and memory layout.
He explicitly says the implementation might be a simple filesystem, possibly enriched with metadata, graph links, embeddings, or inference.
That is a legitimate applied use of the word, but it is not synonymous with a formal OWL ontology.
My preferred term is 
agent world model
, with ontology as one component.

--------------------------------------------------------------------------------

4. Behavior specs are not controls by themselves
A behavior spec can align humans and provide an evaluation rubric. It does not automatically cause the agent to follow that behavior.
Basis deliberately distinguishes the specification from runtime instructions: the judge may see the spec even when the acting agent does not. This is useful for observational evaluation because the eval is not simply testing whether the model repeated a rule it just saw.
But it creates two separate artifacts:
Desired behavior
 — the spec.
Mechanism producing that behavior
 — context, tools, code, model training, or policy enforcement.
A team can therefore possess a beautiful behavior spec while the runtime environment gives the agent no practical way to comply.
Recommendation.
 Every critical behavior needs an implementation map:
behavior


├── taught through context?


├── enabled by a tool?


├── enforced deterministically?


├── evaluated after the fact?


├── monitored during execution?


└── escalated to a human when uncertain?

--------------------------------------------------------------------------------

5. Process evaluation should enforce invariants, not fossilize workflows
Process evals are valuable when they preserve:
authoritative sourcing;
separation of duties;
required review;
evidence retention;
safety boundaries;
reconciliation;
or other durable properties.
They become harmful when they require an exact sequence merely because that sequence is familiar.
A process spec saying “support the conclusion with authoritative sources and preserve the cited evidence” is durable. A rule saying “always open website X, click tab Y, and copy field Z before considering any other evidence” is brittle unless the exact source is a regulatory requirement.
Recent evaluation work increasingly uses claims, environment state, and partial-credit rubrics rather than insisting on one gold trajectory. That allows alternative paths while preserving important invariants. (
arXiv
https://arxiv.org/abs/2406.12045
)

--------------------------------------------------------------------------------

6. Independent agents are not automatically independent evidence
Starting a reviewer with fresh context is better than asking the producer to inspect its own work inside the same trajectory. It reduces anchoring on the producer’s intermediate reasoning.
But “uncorrelated trajectory” is too strong.
Two agents may share:
the same model weights;
the same training blind spots;
the same system prompt;
the same retrieved sources;
the same tool bugs;
the same ontology errors;
and the same evaluator bias.
Research continues to find self-preference, position, verbosity, and prompt sensitivity in LLM judges. Stronger generation capability does not guarantee lower evaluation bias. (
arXiv
https://arxiv.org/html/2604.22891v4
)
Fresh context produces 
less coupled reasoning
, not guaranteed independent judgment.

--------------------------------------------------------------------------------

7. The organizational analogy has limits
The analogy to human organizations is useful for:
delegation;
span of control;
review;
escalation;
specialization;
institutional memory;
and separation of duties.
But agents differ from humans:
they can be cloned cheaply;
they do not have durable identity unless the system creates one;
they have no natural social motivation or professional accountability;
communication consumes tokens and can introduce distortion;
multiple agents may share identical failure modes;
and an agent does not build tacit organizational knowledge unless that knowledge is externalized.
Use organizational design as a source of patterns, not as literal ontology. A “manager agent” is not useful because you gave it a managerial title. It is useful only when it has distinct information, authority, tools, and evaluation responsibilities.

--------------------------------------------------------------------------------

8. Models will absorb mechanics, not organizational reality
Troyanovsky expects much current harness engineering to be swallowed by model capability. Some of it will:
context compaction;
memory routing;
tool selection;
planning;
subagent coordination;
and self-checking are increasingly model-native.
But a model cannot absorb facts and controls that are external by nature:
who currently owns a project;
which policy version is authoritative;
who authorized a payment;
what records a user may access;
whether a transaction committed;
which secret is available to a run;
what an audit requires;
what happened after a tool call;
or whether a human approved an action.
The harness may become thinner. The 
execution, identity, state, policy, evidence, and governance planes
 remain.

--------------------------------------------------------------------------------

Where I Disagree or Where Evidence Is Weak
“Ontology is the most important part of agent building”
That is too universal.
A stable vocabulary and authority structure are extremely valuable in complex, recurring domains. But many useful agents do not initially need a formal ontology. A clear directory, typed schemas, stable IDs, and a small amount of canonical documentation may be enough.
The danger is 
ontology astronautics
: spending months defining a perfect universal model of the organization before the agent has demonstrated a need for it.
My version is:
Stable identity, authority, and meaning are essential. The lightest structure that supplies them is usually best.

--------------------------------------------------------------------------------

“English is more precious than code”
Troyanovsky’s rhetorical point is insightful: engineers often tolerate messy prompts and documentation that directly affect model behavior while obsessing over code organization that does not change runtime semantics.
But as a general hierarchy, I disagree.
Code determines:
permissions;
data isolation;
transaction behavior;
retries;
idempotency;
secrets;
validation;
destructive side effects;
audit logging;
and whether a tool does what its description claims.
English is probabilistic executable configuration. Code is deterministic executable configuration. Both can have enormous blast radius.
The stronger principle is:
Treat agent-facing English with the same production discipline as executable code, while using deterministic code for controls that cannot safely depend on interpretation.

--------------------------------------------------------------------------------

“Mass amounts of evals” are required
A serious production agent does need substantial evaluation coverage. But count alone is a poor measure of rigor.
One hundred nearly identical happy-path cases can create less confidence than twenty carefully selected cases covering:
important task strata;
ambiguity;
stale data;
permission boundaries;
tool failures;
adversarial content;
conflicting evidence;
escalation;
and prior production incidents.
METR itself notes how difficult it is to measure very high reliability without large, diverse, low-noise task sets. A high score on a narrow suite does not establish production generalization. (
Metr
https://metr.org/notes/2026-01-22-time-horizon-limitations/
)
I would replace “mass amounts of evals” with:
A continuously maintained portfolio of representative, adversarial, incident-derived, and distribution-aware evaluations.

--------------------------------------------------------------------------------

Behavior adherence does not necessarily predict general reliability
A system can pass all specified behaviors while failing in an unanticipated way. Conversely, a judge can mark a behavior failure because the trajectory lacks enough visible evidence even when the agent acted appropriately.
Behavior evaluations are a valuable additional signal, not a complete reliability theory.
You still need:
outcome tests;
environment-state checks;
security testing;
operational monitoring;
human review;
and incident response.

--------------------------------------------------------------------------------

Agentic judges remain a weak link
A sophisticated judge that can navigate a long trajectory is an appealing approach, but it introduces another agentic system with its own:
context assembly;
tool use;
biases;
cost;
failure modes;
and potential prompt-injection exposure.
The agent-as-judge literature is moving toward executable verification and richer evaluation, but it remains a young field. (
arXiv
https://arxiv.org/html/2601.05111v1
)
A judge’s confidence should never be confused with calibrated confidence unless you have measured it against expert labels.

--------------------------------------------------------------------------------

Self-improvement is being discussed too broadly
Today’s systems can safely automate portions of the improvement loop:
detect anomalies;
cluster failures;
propose root causes;
draft eval cases;
recommend context changes;
modify code in a sandbox;
and run regression suites.
That is not the same as a system safely improving its own objectives, behavior specifications, evaluators, permissions, and production deployment.
OpenAI’s current improvement-loop example still turns traces and feedback into eval-backed proposals and implementation handoffs. It does not imply that a production agent should silently rewrite its own constitution and deploy the result. (
OpenAI Developers
https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop
)

--------------------------------------------------------------------------------

Basis’s accounting domain is unusually favorable to this philosophy
Accounting is difficult, but it has several properties that reward Troyanovsky’s approach:
mature professional procedures;
primary authorities;
audit traditions;
structured artifacts;
reconciliation;
independent review;
and severe consequences for unsupported work.
In more exploratory domains—early product discovery, scientific hypothesis generation, or creative development—the right process may be less stable. Overly strong process supervision could suppress valuable novelty.
The philosophy generalizes, but the balance between 
reliability and exploration
 must change by domain.

--------------------------------------------------------------------------------

The Agent Stack
I would not use the linear stack:
Model → Harness → Environment → Ontology → Context → Tools ...
It implies that each concept is simply layered on the previous one. In practice, behavior, governance, memory, and verification are cross-cutting.
A better abstraction is six interacting planes.
1. Intent and authority plane
Defines:
goal;
scope;
definition of done;
constraints;
user identity;
budgets;
permissions;
approval boundaries;
and acceptable risk.
This plane answers: 
What is the system allowed and expected to accomplish?
2. World and context plane
Contains:
ontology;
canonical knowledge;
schemas;
entity identities;
current organizational state;
memory;
retrieval;
and the context compiler.
This plane answers: 
What world is the agent operating in, and what part of it should it see now?
3. Capability and execution plane
Contains:
model calls;
agents;
tools;
skills;
workflows;
sandboxes;
subagents;
durable execution;
retries;
and checkpoints.
This plane answers: 
What can the agent do, and how is work carried forward?
4. Evidence and assurance plane
Contains:
deterministic verifiers;
artifact validators;
provenance checks;
semantic judges;
independent reviewers;
behavior evaluations;
outcome evaluations;
and human review.
This plane answers: 
What evidence shows that the work is correct, acceptable, and safe?
5. Operations and control plane
Contains:
identity;
secrets;
least privilege;
observability;
quotas;
incident management;
kill switches;
rollback;
audit;
and fleet health.
This plane answers: 
How is authority controlled and the system operated safely at scale?
6. Improvement plane
Contains:
failure clustering;
root-cause hypotheses;
eval generation;
context/tool/harness proposals;
experiments;
canaries;
release management;
and, where justified, post-training.
This plane answers: 
How does observed production evidence become a controlled system improvement?
Visual model
                    ┌──────────────────────────────┐  
                     │      INTENT & AUTHORITY      │  
                     │ goal • scope • permissions   │  
                     │ budgets • approvals • risk   │  
                     └──────────────┬───────────────┘  
                                    │  
              ┌─────────────────────▼─────────────────────┐  
              │        WORLD MODEL & CONTEXT PLANE        │  
              │ ontology • canon • schemas • memory       │  
              │ retrieval • freshness • context compiler  │  
              └─────────────────────┬─────────────────────┘  
                                    │ compiled context  
              ┌─────────────────────▼─────────────────────┐  
              │       CAPABILITY & EXECUTION PLANE        │  
              │ models • agents • tools • skills          │  
              │ workflow • state • checkpoints • sandbox  │  
              └─────────────────────┬─────────────────────┘  
                                    │ actions \+ artifacts  
              ┌─────────────────────▼─────────────────────┐  
              │        EVIDENCE & ASSURANCE PLANE         │  
              │ deterministic checks • semantic judges    │  
              │ behavior evals • reviewers • human gate   │  
              └──────────────┬──────────────┬─────────────┘  
                             │ pass/retry   │ evidence  
              ┌──────────────▼───────────┐  │  
              │ OPERATIONS & CONTROL     │  │  
              │ policy • audit • limits  │  │  
              │ monitoring • rollback    │  │  
              └──────────────┬───────────┘  │  
                             │              │  
              ┌──────────────▼──────────────▼─────────────┐  
              │              IMPROVEMENT PLANE             │  
              │ failure mining • proposals • evals         │  
              │ experiments • canary • controlled rollout  │  
              └─────────────────────┬─────────────────────┘  
                                    │ versioned changes  
                                    └───────────► back into  
                                                  every plane

The 
model is a replaceable inference component used in several planes
. It may act as executor, planner, retriever, summarizer, or judge. It should not be mistaken for the architecture itself.
The revised core stack
My practical version of Troyanovsky’s sequence is:
Intent and authority → world model and canon → context compilation → capability and durable execution → state and evidence → verification and evaluation → controlled improvement
Behavior specifications and governance surround the entire path as contracts.

--------------------------------------------------------------------------------

Architecture Blueprint
The first architectural distinction I would make is between:
Version-controlled system definitions
Mutable operational data
Do not put all of them into one giant repository tree.
Version-controlled agent-system repository
agent-os/


├── product/


│   ├── intents/                  # Supported jobs and definitions of done


│   ├── acceptance/               # Product-level acceptance criteria


│   └── decision-records/         # Why important agent design choices were made


│


├── world/


│   ├── ontology/


│   │   ├── entity-types.yaml


│   │   ├── relations.yaml


│   │   ├── vocabulary.md


│   │   └── identity-rules.md


│   ├── canon/


│   │   ├── organization/


│   │   ├── products/


│   │   ├── projects/


│   │   ├── policies/


│   │   └── procedures/


│   ├── schemas/


│   │   ├── run.schema.json


│   │   ├── task.schema.json


│   │   ├── artifact.schema.json


│   │   ├── claim.schema.json


│   │   └── handoff.schema.json


│   └── authority/


│       ├── source-priority.yaml


│       ├── ownership.yaml


│       └── freshness-policy.yaml


│


├── runtime/


│   ├── agents/


│   │   ├── orchestrator/


│   │   ├── executor/


│   │   ├── researcher/


│   │   └── reviewer/


│   ├── workflows/


│   │   ├── product-research/


│   │   ├── software-change/


│   │   └── creative-production/


│   ├── skills/


│   │   ├── source-research/


│   │   ├── spreadsheet-analysis/


│   │   ├── artifact-rendering/


│   │   └── incident-investigation/


│   ├── tools/


│   │   ├── registry.yaml


│   │   ├── contracts/


│   │   ├── adapters/


│   │   └── mocks/


│   └── context/


│       ├── assembly/


│       ├── disclosure-rules/


│       ├── compaction/


│       └── templates/


│


├── assurance/


│   ├── behaviors/


│   ├── verifiers/


│   ├── judges/


│   ├── evals/


│   │   ├── cases/


│   │   ├── datasets/


│   │   ├── adversarial/


│   │   └── production-incidents/


│   └── calibration/


│       ├── human-labels/


│       └── judge-benchmarks/


│


├── control/


│   ├── permissions/


│   ├── policies/


│   ├── approvals/


│   ├── budgets/


│   ├── secret-scopes/


│   └── escalation/


│


├── operations/


│   ├── observability/


│   ├── dashboards/


│   ├── alerts/


│   ├── incident-playbooks/


│   └── rollback/


│


├── improvement/


│   ├── failure-taxonomy/


│   ├── proposals/


│   ├── experiments/


│   ├── canaries/


│   └── releases/


│


└── tests/


├── tool-contracts/


├── context-regressions/


├── policy/


└── end-to-end/
Mutable operational stores
Postgres / durable state store


runs


tasks


checkpoints


decisions


approvals


entity state


memory metadata


eval results
Object store / filesystem


source documents


generated artifacts


rendered previews


large tool outputs


evidence bundles


checkpoint snapshots
Append-only event or workflow history


state transitions


tool attempts


retries


approvals


compensating actions
Trace store


model calls


context manifests


tool calls


handoffs


verifier results


judge results


token/cost/latency metrics
Secret manager


scoped credentials


per-user and per-run grants


revocation records
For a local solo system, those may initially be SQLite and ordinary folders. At fleet scale, they become separate operational services.
Why 
/memory
, 
/state
, and 
/trajectories
 should not simply be Git folders
Those directories represent runtime concepts, but their live contents are:
high-volume;
mutable;
potentially sensitive;
user- or tenant-specific;
and unsuitable for source control.
The repository should contain their 
schemas, policies, and maintenance code
. The operational stores should contain the actual records.
Component responsibilities
Component
What belongs there
What should not
world/ontology
Entity types, relations, vocabulary, identity rules
Every instance of every entity
world/canon
Current authoritative organizational knowledge
Raw meeting transcripts and historical speculation mixed with current truth
runtime/context
Selection, ranking, disclosure, compaction logic
A universal giant prompt
runtime/skills
Reusable procedures and domain methods
Secrets or mutable run state
runtime/tools
Stable contracts and adapters
Unscoped credentials
runtime/agents
Role configuration, models, tool allowances
Long-lived business truth
runtime/workflows
Durable state transitions and orchestration
Semantic judgment that belongs in an agent or verifier
assurance/behaviors
Sparse product-level conduct contracts
Thousands of low-value instructions
assurance/verifiers
Deterministic assertions and artifact checks
Subjective quality judgments
assurance/judges
Calibrated semantic evaluation
Authentication, authorization, or irreversible enforcement
control
Deterministic permission and approval policy
Prompt-only safety
operations
Monitoring, incidents, rollback, fleet health
Product canon
improvement
Versioned proposals and experiments
Direct uncontrolled production mutation

--------------------------------------------------------------------------------

Ontology & Context Framework
The important distinctions
Concept
What it is
What it does not automatically provide
Ontology
Shared concepts, identities, relations, and semantic distinctions
Retrieval, memory, or a graph database
Information architecture
How information is organized and navigated
Formal semantics
Knowledge graph
Instance data represented as nodes and relationships
Authority, freshness, or correct retrieval
File/folder hierarchy
A containment and navigation structure
Rich many-to-many relationships
Schema
Enforced structure and valid fields
Meaning beyond the encoded fields
Object model
Software representation of domain entities and behavior
Organizational canon
RAG
A mechanism for retrieving external information into model context
Truth, relevance, or memory maintenance
Embeddings
A similarity representation used for search or clustering
Canonicality or reasoning
Memory
Persisted past information or experience available to future runs
Current relevance or authority
Context
The information visible to the current inference
Persistence after the inference
Canonical documentation
Authoritative statements about current reality or policy
Automatic retrieval or enforcement
Agent state
The current status of a particular run or workflow
General organizational knowledge
The original RAG work combined parametric model knowledge with a retrieved non-parametric memory index. That is a retrieval architecture, not an ontology or complete memory system. (
arXiv
https://arxiv.org/abs/2005.11401
)
What Troyanovsky means by an agent-native ontology
His ontology is best understood as a 
world-legibility layer
.
It should let an agent answer:
What kinds of things exist here?
What are they called?
Which specific object does this name refer to?
How are objects related?
Which source is authoritative?
What is current versus historical?
What can I expect to find?
How do I navigate from a goal to its project, tasks, decisions, artifacts, and policies?
What does a tool mean when it says 
project_id
 or 
customer
?
Which facts are canonical, inferred, provisional, or stale?
Core entity model
A practical agent-native ontology might include:
Person


Team


Organization


Product


Project


Goal


Task


Decision


Claim


Observation


Artifact


Source


Tool


Skill


Procedure


Policy


Behavior


Evaluation


Run


Trajectory


Checkpoint


Memory


Incident


Approval
Useful relations include:
owns


member_of


contributes_to


supports


depends_on


blocks


implements


governed_by


permitted_for


produced_by


derived_from


supported_by


contradicts


supersedes


evaluated_by


observed_in


applies_to


approved_by
Required metadata
Every important agent-visible object should ideally have:
stable ID;
type;
human-readable name;
status;
owner;
source;
canonicality;
valid-from and valid-until dates;
last-reviewed timestamp;
sensitivity;
provenance;
confidence if inferred;
version;
supersedes/superseded-by;
and access policy.
Example:
id: decision:agent-fleet:2026-07-autonomy-boundary


type: Decision


title: External emails require human approval


status: active


canonical: true


owner: team:agent-platform


valid_from: 2026-07-10


supersedes: decision:agent-fleet:2026-03-email-policy


source:


artifact_id: adr:0042


applies_to:


- workflow:scheduled-research


- tool:gmail-send


sensitivity: internal
How this prevents drift and ambiguity
A good world model reduces:
context drift
 by pointing agents back to current canon;
semantic ambiguity
 through stable vocabulary and IDs;
duplicate concepts
 by enforcing identity resolution;
contradictory instructions
 through authority and supersession rules;
stale knowledge
 through temporal validity;
memory contamination
 by separating observed, inferred, and canonical information;
and 
tool confusion
 by aligning tool contracts with the same domain language.
Do not start with a giant knowledge graph
Start with:
Markdown for human-readable canon;
YAML or JSON for metadata;
relational tables for state;
stable entity IDs;
typed links;
and ordinary search.
Add a graph database only when you have recurring queries whose complexity genuinely benefits from graph traversal or formal inference.
A filesystem can be a perfectly effective early ontology if its concepts, authority, and identities are coherent. Troyanovsky explicitly allows for that simpler implementation.

--------------------------------------------------------------------------------

Context as runtime training data: useful and dangerous
The metaphor is useful because the context effectively defines the local distribution on which the model must operate. A codebase with coherent conventions, examples, documentation, and tests gives a coding model a far better environment than a contradictory codebase. Troyanovsky calls that runtime training data.
But the operational conclusion should not be “load more text.” It should be:
Compile a high-signal context package for the current decision.
The context compiler
A context compiler should:
Parse the request and identify relevant entities.
Resolve ambiguous names to stable IDs.
Determine the task class and required authority.
Load applicable policies and behaviors.
Retrieve current canonical knowledge.
Retrieve task state and recent decisions.
Add relevant episodic memories or environment gotchas.
Detect contradictory or superseded sources.
rank information by relevance, authority, and freshness.
Mark untrusted external content as data.
Include summaries plus handles to larger artifacts.
Produce a manifest recording exactly what was loaded.
Conceptually:
request


↓


entity resolution


↓


task classification


↓


authority + permission filter


↓


canonical retrieval


↓


state + memory retrieval


↓


conflict and freshness checks


↓


budgeted ranking


↓


context package + manifest
Progressive disclosure
A useful disclosure hierarchy is:
Level 0 — always present


identity, goal, critical policy, tool boundaries
Level 1 — navigation


indexes, entity summaries, available skills, artifact handles
Level 2 — task-relevant detail


current project state, applicable procedures, recent decisions
Level 3 — evidence on demand


source documents, historical trajectories, full tool results
Level 4 — forensic history


raw logs, superseded material, archived evidence
The agent should usually see Level 0 and a carefully selected portion of Levels 1–2. It can retrieve Levels 3–4 as needed.
Context-engineering rules
Capture richly; disclose selectively.
Separate current canon from historical records.
Use stable IDs, not names alone.
Put local instructions close to their scope.
Default to exclusion for automatically loaded material.
Treat summaries as derived caches, not sources of truth.
Preserve raw evidence outside the context window.
Store large tool results as artifacts and place references in context.
Mark external content as untrusted data, never authority by default.
Track source, timestamp, owner, and version.
Detect conflicts instead of silently concatenating them.
Test context changes against representative evals.
Keep critical permissions in code and policy, not prose alone.
Record a context manifest for every important run.
Prefer fresh context reconstructed from state when old conversation history has become noisy.

--------------------------------------------------------------------------------

Behavior & Eval Framework
Behavior specs versus neighboring concepts
Concept
Primary purpose
System prompt
Establish runtime role, priorities, and instructions
Instruction
Tell the agent what to do in a particular context
SOP
Describe a repeatable human or operational procedure
Policy
Define an organizational rule or boundary
Hard-coded rule
Deterministically constrain software behavior
Guardrail
Detect, block, transform, or escalate risky input/action/output
Eval rubric
Define how a run or artifact will be scored
Behavior specification
State the recurring conduct expected from an agent, while serving as a human product contract and trajectory-level evaluation reference
The Basis/Braintrust formulation is unusually useful because it recognizes that behavior is simultaneously:
a product decision;
a human-alignment artifact;
a regression contract;
and a judgeable expectation.
The public standard explicitly defines behavior specs as a way to evaluate conduct across an entire trajectory, not merely the final result. (
GitHub
https://github.com/braintrustdata/agentbehavior
)
What makes a good behavior
A good behavior is:
recurring
, not tied to one test case;
high leverage
, with meaningful quality or risk impact;
observable
, so a trace or artifact can supply evidence;
implementation-agnostic where possible
;
specific enough to judge
;
stable enough to maintain
;
clear about failure and recovery
;
and 
owned by someone
.
Brittle instruction versus durable principle
Brittle:
Always call the 
search_irs_v3
 tool before answering any tax question.
Durable:
For material tax conclusions, consult and preserve authoritative primary sources before finalizing the conclusion. Do not represent a conclusion as verified when only secondary commentary is available.
The durable form survives tool changes while preserving the reason the organization cares.
A tool-specific rule is appropriate when the tool is itself a required control—for example, “all production deployments must pass through the signed deployment service.”

--------------------------------------------------------------------------------

Example behavior spec: primary-source grounding
---


id: primary-source-grounding


owner: research-operations


severity: critical


version: 1.0


---
# Ground material claims in authoritative evidence
**Intent:** Material conclusions should be repeatable and defensible rather


than dependent on unsupported model recall or informal commentary.
**Applies when:** The agent makes a factual claim that materially affects a


recommendation, calculation, compliance decision, or external deliverable.
**Evidence:** The current authoritative source, its publication or effective


date, and the exact portion supporting the claim.
**Decision:** Determine whether the available source is sufficiently


authoritative and current for the claim and domain.
**Execution:** Preserve a claim-to-source link and distinguish source facts


from the agent's inference.
**Recovery:** When primary evidence is unavailable or conflicting, label the


claim unverified and escalate or narrow the conclusion.
**Allowed alternatives:** A reliable secondary source may be used to discover


primary evidence, but not silently substituted for it when primary authority is


required.
**Failure modes:** Unsupported model recall; citation to a source that does not


support the claim; relying on stale or superseded guidance; presenting an


inference as a sourced fact.
Example behavior spec: external communication
---


id: controlled-external-communication


owner: governance


severity: critical


version: 1.0


---
# Do not cross an external communication boundary without authority
**Intent:** Prevent unapproved commitments, disclosures, or messages.
**Applies when:** The agent would send, publish, submit, or otherwise expose


content outside the approved internal workspace.
**Evidence:** Intended recipient, exact final content, data classification,


requesting user, and applicable approval record.
**Decision:** Determine whether the action is pre-authorized, requires human


approval, or is prohibited.
**Execution:** Draft the content and request approval when required. The


approved artifact hash must match the artifact being sent.
**Recovery:** If approval is absent, ambiguous, expired, or refers to a different


artifact version, do not send.
**Failure modes:** Treating draft permission as send permission; sending a newer


unapproved version; exposing secrets or personal data; assuming model confidence


is authorization.
Example behavior spec: artifact validation
---


id: validate-current-artifact


owner: production-quality


severity: high


version: 1.0


---
# Validate the current artifact, not a stale intermediate version
**Intent:** Ensure that the deliverable being returned is the version that was


actually inspected.
**Applies when:** The agent creates or edits a visual, executable, or structured


artifact.
**Evidence:** The current artifact checksum and the validator output generated


from that same version.
**Decision:** Determine whether the artifact is structurally valid and visibly


or functionally usable.
**Execution:** Render, execute, or otherwise inspect the current version before


delivery.
**Recovery:** After any fix, rerun validation. If validation is unavailable,


state that the artifact is unvalidated.
**Failure modes:** Relying on a pre-edit render; validating source code but not


the generated artifact; fixing an issue without revalidation; claiming success


when the validator failed.
Example behavior spec: uncertainty and escalation
---


id: escalate-material-uncertainty


owner: agent-platform


severity: critical


version: 1.0


---
# Escalate uncertainty before irreversible action
**Intent:** Preserve human control when evidence is incomplete and the action


cannot be cheaply reversed.
**Applies when:** The agent is considering an irreversible, externally visible,


financial, destructive, or high-impact action.
**Evidence:** Available facts, unresolved assumptions, confidence by assumption,


reversibility, expected impact, and available alternatives.
**Decision:** Determine whether remaining uncertainty is material to the action.
**Execution:** Pause and produce a concise approval packet when material


uncertainty remains.
**Recovery:** Continue only after receiving a scoped approval or after new


evidence resolves the uncertainty.
**Failure modes:** Converting lack of evidence into confidence; asking for broad


blanket approval; hiding uncertainty in a long narrative; proceeding because a


deadline is near.

--------------------------------------------------------------------------------

Process evals versus outcome evals
Domain
Correct outcome, unacceptable process
Accounting
Correct tax treatment reached from an informal blog without retaining authoritative support
Software engineering
Tests pass because the agent disabled validation, hard-coded the fixture, or altered the test
Research
Correct conclusion stated without evidence, with fabricated provenance, or after ignoring contradictory data
Product analysis
Recommendation proves commercially sound but was based on unauthorized customer data or cherry-picked metrics
Enterprise workflow
Correct CRM update made to the wrong account and later manually corrected
Creative production
Final image looks acceptable but violates provenance requirements, continuity rules, or an approved model sheet
Data analysis
Correct number obtained through a query that silently excluded a material segment
Security
Vulnerability fixed by introducing an unapproved dependency or exposing credentials in logs
Layered production evaluation
Layer
Question
Typical method
0. Preconditions
Did the run have valid scope, identity, and inputs?
Schema and policy checks
1. Tool contract
Were valid tools and arguments used?
Typed call validation
2. Environment state
Did the intended state change occur?
Database/API assertions
3. Artifact validity
Does the deliverable open, compile, render, or reconcile?
Deterministic validators
4. Outcome quality
Did the system achieve the requested result?
Exact, rubric, or human score
5. Behavior
Did it exhibit important recurring conduct?
Trace judge
6. Provenance
Are claims and transformations supported?
Claim/evidence validation
7. Safety and authority
Did it remain within permissions and approvals?
Deterministic policy engine
8. Operational quality
Were cost, latency, retries, and tool use acceptable?
Telemetry thresholds
9. Fleet reliability
Are failure rates changing by task, model, customer, or version?
Statistical monitoring
10. Human outcome
Did users accept, override, correct, or distrust the result?
Production feedback
Sparse versus dense signals
Outcome evals are often 
sparse
:
task passed / task failed
Trajectory analysis can generate denser signals:
wrong source selected


→ stale policy loaded


→ tool argument malformed


→ recovery attempted


→ evidence not preserved


→ reviewer correctly escalated
Dense signal is useful only when it points to a controllable intervention. Do not collect thousands of labels that cannot be translated into a product, context, tool, or workflow change.

--------------------------------------------------------------------------------

Verification and judges
Use a hierarchy.
1. Deterministic verification first
Examples:
schemas;
checksums;
type systems;
database constraints;
formula reconciliation;
permissions;
test suites;
signed approvals;
link resolution;
file parsing;
rendering;
executable simulation;
policy rules.
These are cheap, reproducible, and usually less ambiguous.
2. Semantic verification second
Use an LLM or agent judge for:
completeness;
argument quality;
source relevance;
visual usability;
tone;
ambiguity;
policy interpretation;
or whether a behavior applied.
3. Independent review for material work
A reviewer should ideally receive:
the objective;
applicable acceptance criteria;
evidence and artifacts;
relevant canon;
and the producer’s declared assumptions.
For high-stakes review, have the reviewer inspect the evidence before seeing the producer’s unsupported conclusion when practical. This reduces anchoring.
4. Human judgment where value or risk warrants it
Human review remains appropriate when:
the desired outcome is inherently subjective;
the legal or financial consequence is high;
the evaluator is poorly calibrated;
important evidence conflicts;
or the system is encountering a new task distribution.
Reducing correlated error
From weakest to strongest independence:
same agent, same context, “check your work”


↓


same model, fresh context


↓


same model, different rubric and evidence-first prompt


↓


different model family


↓


different data or retrieval path


↓


deterministic oracle


↓


qualified human reviewer
Multiple sampled trajectories and majority voting can improve reasoning in some benchmark settings, but voting only helps when:
trajectories genuinely explore different possibilities;
the aggregation criterion is meaningful;
and the majority is more likely to be right than to share the same misconception.
For open-ended enterprise work, “three agents agreed” is not strong evidence by itself.

--------------------------------------------------------------------------------

How Long-Horizon Execution Should Work
The lifecycle
INTAKE


↓


SCOPE & AUTHORIZE


↓


ASSEMBLE CONTEXT


↓


PLAN


↓


EXECUTE BOUNDED STEP


↓


PERSIST STATE + EVIDENCE


↓


VERIFY


├── fail, recoverable → repair/retry


├── fail, missing info → retrieve/escalate


├── policy boundary → approval


└── pass → next step


↓


CHECKPOINT / COMPACT / FRESH CONTEXT


↓


REVIEW


↓


DELIVER


↓


LEARN FROM TRAJECTORY
Planning
A plan is a 
mutable hypothesis
, not the source of truth.
It should contain:
milestones;
dependencies;
known unknowns;
expected evidence;
verification strategy;
estimated cost;
approval points;
and termination conditions.
The agent must be allowed to revise the plan when evidence changes, while preserving why the revision occurred.
State
State is what is true now:
current phase;
completed tasks;
active artifacts;
approvals;
unresolved blockers;
budgets consumed;
and next eligible actions.
State should be structured and stored outside the model.
Event history
The event log records how state changed:
tool requested


tool authorized


tool executed


artifact created


validator failed


repair attempted


approval requested


approval granted
For work that runs hours or days, durable workflow systems use persisted histories, replay, retries, and idempotent activities so a process can recover after crashes without repeating harmful side effects. (
Temporal Documentation
https://docs.temporal.io/workflow-execution/event
)
Checkpointing
Checkpoint:
after an expensive phase;
before an irreversible action;
after a major decision;
before compaction;
after subagent aggregation;
or whenever resuming from scratch would be costly.
A checkpoint should reference artifacts rather than embedding them all.
Context compaction
Before compaction:
Flush important evidence to storage.
Update structured state.
Record decisions and assumptions.
Write the future-self handoff.
Preserve unresolved alternatives.
Store raw history for audit.
Generate a new context package.
Compaction is not merely summarizing the conversation. It is 
committing cognition into durable state
.
Delegation
A subagent request should be a typed work contract:
task_id: research:competitor-capabilities


objective: Determine whether competitors support scheduled autonomous workflows.


scope:


allowed_sources: public


cutoff_date: 2026-08-14


deliverables:


- claim_ledger.json


- evidence_summary.md


definition_of_done:


- every material claim has a source


- facts and inferences are separated


permissions:


tools:


- web_search


- web_fetch


external_actions: none


budget:


max_tokens: 120000


max_minutes: 30


return:


format: SubagentResultV2
Recovery
Classify failure before retrying.
Failure class
Correct response
Transient service failure
Bounded retry with backoff
Invalid tool argument
Correct argument from schema/error
Missing capability
Select another tool or escalate
Missing evidence
Retrieve or ask
Contradictory evidence
Preserve conflict and seek resolution
Context degradation
Checkpoint and restart fresh
Repeated reasoning loop
Stop, summarize attempts, change strategy
Permission denial
Do not retry around the boundary
Budget exhaustion
Return partial work and escalation packet
Irreversible partial failure
Run compensating action or incident procedure
Retries without idempotency can duplicate messages, payments, records, or deletions. Every side-effecting tool should support an idempotency key or an equivalent deduplication strategy.
Completion
“Done” should require more than the agent saying it is done.
A completion gate might require:
all critical acceptance criteria satisfied;
current artifacts validated;
no unresolved critical behavior failures;
claims linked to evidence;
required approvals present;
critical assumptions surfaced;
reviewer disposition recorded;
and a final work receipt generated.

--------------------------------------------------------------------------------

What belongs where?
Information
Context
Tool
Persistent storage
Code/policy
Current goal
Yes
Yes
Active task state
Summary
Query/update
Yes
Schema
Large source document
Selected excerpt
Fetch
Yes
Secret credential
Never
Scoped injection
Secret manager
Enforcement
Permission boundary
Brief explanation
Audit record
Yes
Tool result
Short summary
Produced by tool
Full artifact
Contract
Canonical policy
Applicable portion
Lookup
Versioned canon
Critical enforcement
Historical trajectory
Rarely raw
Search
Trace store
Approval
Reference
Approval service
Yes
Enforcement
Behavior spec
Sometimes
Versioned file
Judge/control mapping
Model-generated hypothesis
Current if relevant
Run state/memory candidate
Final artifact
Handle/summary
Create/read
Object store
Validation code

--------------------------------------------------------------------------------

Memory Framework
Memory is not one vector database
A mature agent needs several distinct forms of retained information.
1. Working context
Information immediately visible to the current inference.
Properties:
fast;
expensive;
temporary;
easily polluted;
bounded.
2. Execution state
Current structured facts about a run.
Examples:
active phase;
completed steps;
selected entities;
budgets;
blockers;
approvals.
This should usually be queried deterministically.
3. Immutable event memory
The append-only history of what happened.
Useful for:
audit;
replay;
incident investigation;
and reconstructing derived state.
4. Episodic memory
Past cases or experiences:
a previous customer issue;
a failed deployment;
a successful research approach;
a tool-specific gotcha.
Episodic memory should retain provenance and temporal scope.
5. Semantic and canonical memory
Stable organizational knowledge:
product definitions;
current policies;
domain concepts;
customer identities;
architecture;
approved procedures.
This is not merely “remembered.” It is maintained canon.
6. Procedural memory
Reusable skills and methods:
how to investigate an incident;
how to create a deck;
how to validate an animation shot;
how to prepare a pull request;
how to reconcile a workbook.
7. Derived summaries
Compressed representations used to accelerate retrieval.
These are useful caches, but they can omit or distort information. Preserve links to their sources.
Memory research increasingly treats agent memory as a pipeline involving representation, extraction, retrieval, routing, consolidation, and maintenance—not simply retrieval from embeddings. LongMemEval-V2 evaluates static facts, dynamic state, workflow knowledge, environment-specific gotchas, and premise awareness across histories containing up to hundreds of trajectories. (
arXiv
https://arxiv.org/html/2605.12493v1
)
What should be remembered?
Promote information when it is:
likely to matter again;
costly to rediscover;
supported by evidence;
sufficiently stable;
scoped to identifiable entities;
and not already represented in canon.
Examples:
a confirmed environment quirk;
a user-approved preference;
a prior failure and its validated resolution;
a stable mapping between external and internal IDs;
a decision with continuing consequences;
a procedure that repeatedly improves outcomes.
What should be forgotten or demoted?
temporary scratch reasoning;
duplicated observations;
stale hypotheses;
transient tool errors;
superseded policies;
unverifiable conclusions;
irrelevant raw output;
and memories whose scope has expired.
“Forget” usually means remove from active retrieval, not necessarily delete the audit record.
Memory promotion pipeline
raw observation


↓


candidate memory


↓ provenance and scope check


validated episodic lesson


↓ repeated confirmation / owner approval


procedure or canonical knowledge
Do not allow one agent’s unsupported inference to become fleet-wide truth.
Required memory metadata
memory_id: mem:tool:analytics-query:timezone-gotcha


type: environment_gotcha


subject: tool:analytics-query


statement: Daily aggregates use UTC boundaries.


status: validated


source_artifacts:


- trace:run-9812


- incident:INC-204


valid_from: 2026-06-01


valid_until: null


confidence: 0.99


owner: team:data-platform


visibility: internal


supersedes: null

--------------------------------------------------------------------------------

The ideal Memento handoff packet
run_id: run-2026-08-14-0042


objective:


statement: Produce an evidence-backed recommendation and decision package.


definition_of_done:


- decision memo complete


- claims linked to evidence


- PRD schema passes


- deck rendered and reviewed
current_phase: synthesis
progress:


completed:


- customer evidence analysis


- market research


- technical feasibility review


in_progress:


- option comparison


remaining:


- independent review


- final deck render
state:


project_id: project:agent-observability


selected_option: option:B


budget_remaining_usd: 18.40


approval_status: internal-draft-only
decisions:


- id: dec:001


statement: Focus on incident reconstruction before automated remediation.


rationale: Stronger evidence of demand and lower governance risk.


evidence:


- artifact:customer-synthesis-v3


- artifact:technical-feasibility-v2
assumptions:


- statement: Support ticket sample represents current enterprise users.


confidence: medium


materiality: high


validation_needed: true
evidence_ledger:


- claim_id: claim:017


evidence:


- source:ticket-cluster-4


- source:interview-2026-07-21
ruled_out:


- hypothesis: Lack of adoption is primarily caused by price.


reason: Contradicted by interview and usage data.


evidence:


- artifact:pricing-analysis-v1
unresolved:


- question: Does the current event schema preserve enough provenance?


owner: subtask:technical-review


severity: high
artifacts:


- id: artifact:decision-memo-draft-v3


checksum: sha256:...


- id: artifact:evidence-ledger-v2


checksum: sha256:...
risks:


- risk: Recommendation may overstate addressable demand.


mitigation: Require human product review before roadmap commitment.
next_actions:


- Reconcile claim 017 against analytics.


- Request independent reviewer.


- Update deck and rerender.
context_manifest:


version: ctx-7f92


canon_versions:


product_strategy: 12


data_policy: 8
last_checkpoint:


timestamp: 2026-08-14T19:21:00Z


event_id: evt-88210
A good handoff packet distinguishes:
observed fact;
inference;
decision;
assumption;
unresolved question;
and proposed next action.
It should not be a narrative diary.

--------------------------------------------------------------------------------

Multi-Agent Framework
Use one capable agent by default
A single agent with good tools is usually easier to:
debug;
evaluate;
secure;
observe;
and improve.
Both Anthropic and OpenAI recommend starting with a single agent and adding multi-agent complexity only where the task structure justifies it. (
Anthropic
https://www.anthropic.com/engineering/building-effective-agents
)
Spawn a subagent when at least one of these is true
Parallelism
Several independent investigations can be performed concurrently.
Example: separate market, customer, and technical research.
Context isolation
A subtask would flood or bias the root agent’s context.
Anthropic explicitly recommends subagents for work that reads many files or requires specialized focus without cluttering the parent context. (
Anthropic
https://www.anthropic.com/engineering/claude-code-best-practices
)
Permission separation
A subtask requires a narrower or different set of tools.
Example: a reviewer can read code and test results but cannot merge or deploy.
Independent review
You want a fresh trajectory to challenge the producer.
Specialized environment
The subtask needs a different sandbox, model, retrieval corpus, or validator.
Compute allocation
A difficult decision warrants multiple independent attempts, search, or adversarial critique.
Do not spawn a subagent merely because:
a role has a clever name;
a framework makes it easy;
the task has multiple conceptual steps;
or “multi-agent” sounds more advanced.
Temporary subagents versus persistent agents
Pattern
Use when
One agent with tools
Most tasks; shared context is valuable; decisions are sequential
Temporary subagent
Bounded parallel work, context isolation, specialization, or independent review
Persistent specialist service
Stable responsibility, separate data ownership, distinct permissions, independent scaling
Peer-agent network
Only when there are genuinely autonomous services or organizations with separate ownership and protocols
True peer multi-agent systems remain less mature than manager-to-bounded-worker patterns. Interoperability protocols such as A2A can standardize handoffs and identity, but a protocol does not prove that agent discussion improves reasoning quality.
Delegation rules
A root agent should never delegate an undefined problem and hope the subagent “figures out what matters.”
Each delegation needs:
objective;
scope;
inputs;
relevant canon;
allowed tools;
prohibited actions;
expected artifacts;
evidence requirements;
budget;
timeout;
completion criteria;
and return schema.
Span of control
Do not let one root agent coordinate dozens of active subagents through free-form conversation. Aggregate through structured artifacts and bounded batches.
A practical initial cap might be:
3–6 parallel subagents;
1–2 levels of delegation;
explicit escalation for deeper recursion.
Increase those limits only after measuring coordination failures.
Multiple trajectories and voting
Use multiple trajectories when:
the problem has a search component;
solutions can be objectively scored;
different evidence paths are valuable;
or the cost of one wrong answer is high enough to justify more compute.
Do not rely on majority vote when all trajectories share the same mistaken premise. Prefer:
independent proposals


↓


evidence-normalized comparison


↓


deterministic checks where available


↓


adversarial reviewer


↓


final decision

--------------------------------------------------------------------------------

Governance Framework
Governance must sit outside the model
The model may explain policy, but critical controls should be enforced by deterministic services.
Examples:
authentication;
authorization;
data tenancy;
secret access;
financial limits;
approval requirements;
destructive-action restrictions;
rate limits;
and audit logging.
Prompt instructions are not a security boundary.
Permission model
Define permissions at least across:
subject
 — user, service, agent role, or run;
resource
 — file, account, repository, database, customer;
action
 — read, create, modify, delete, execute, publish;
scope
 — specific tenant, project, branch, or time window;
conditions
 — amount, destination, approval, confidence, validator result;
duration
 — one action, one run, or standing grant.
MCP governance
For MCP integrations:
authenticate each request;
request the smallest necessary scopes;
validate token audience;
do not pass user tokens through blindly;
bind state and handles to the proper user or run;
centralize policy and audit where practical;
and treat tool descriptions and outputs as potentially attackable surfaces.
The MCP authorization specification explicitly emphasizes resource-scoped tokens, audience validation, least privilege, and prohibition of token passthrough. (
Model Context Protocol
https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
)
Threats to account for
Current agent-security guidance highlights risks such as:
goal hijacking;
tool misuse;
identity and privilege abuse;
memory poisoning;
insecure inter-agent communication;
cascading failure;
excessive autonomy;
and human trust exploitation. (
OWASP Gen AI Security Project
https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
)
Autonomy ladder
Level
Agent authority
Required controls
0 — advisory
Generates suggestions only
Output review
1 — read-only
Reads approved data and produces analysis
Access controls, citation/provenance
2 — sandboxed creation
Creates files or code in isolated workspace
Validators, quotas, no external side effects
3 — reversible internal action
Updates low-risk internal state
Idempotency, audit, rollback, sampled review
4 — boundary-crossing action
Sends, publishes, deploys, or affects another party
Artifact-specific approval, policy enforcement, independent verification
5 — bounded autonomous operation
Executes scheduled workflows within a pre-authorized envelope
Budgets, circuit breakers, drift monitoring, incident response, automatic suspension
6 — high-impact or irreversible
Financial, legal, destructive, privileged, or safety-critical actions
Dual control or explicit human authorization; deterministic limits
Trust should be evidence-based
Increase autonomy only when you have evidence for a 
specific combination
 of:
task class;
environment;
model;
harness version;
tool set;
behavior profile;
and action class.
A system that performs research reliably has not demonstrated that it can safely send emails or modify production databases.
Incident readiness
For every autonomous workflow, be able to answer:
How do we stop it?
How do we revoke its credentials?
How do we identify every action it took?
Can we reproduce the context and policy version?
Can we undo its reversible actions?
Which users or systems were affected?
Which production incident should become a new eval?
What evidence is required before re-enabling it?
NIST’s AI risk framework emphasizes lifecycle risk management, testing, governance, provenance, and incident-oriented practices rather than treating deployment as a one-time approval. (
NIST Publications
https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
)

--------------------------------------------------------------------------------

Self-Improving Systems
What is practical now
Capability
Practical status
Detect failed validators or abnormal trajectories
Strong
Cluster recurring failures
Strong
Generate root-cause hypotheses
Useful with human verification
Draft new eval cases from incidents
Useful with review
Propose prompt or context changes
Useful in an offline experiment
Modify tool or harness code
Useful in sandboxed coding workflows
Run regression evals automatically
Strong
Rank candidate changes
Useful if metrics are trustworthy
Canary a validated change
Standard engineering practice
Consolidate or clean candidate memories
Useful with provenance and approval
Modify behavior specifications autonomously
Usually inappropriate; behavior is a product/governance decision
Modify production evaluators and deploy itself
Unsafe without separation of duties
Perform autonomous RL on noisy production signals
Experimental and domain-dependent
Fully recursive self-improvement
Research, not normal production architecture
The safe improvement loop
production traces


↓


failure detection and clustering


↓


root-cause hypotheses


↓


candidate change proposals


↓


sandbox implementation


↓


holdout and adversarial evals


↓


human or independent approval


↓


limited canary


↓


monitoring


↓


promotion or rollback
OpenAI’s current agent-improvement example follows this general pattern: real traces and feedback become repeatable evals, which then support evidence-based harness modifications. (
OpenAI Developers
https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop
)
Protect the evaluator
The most important governance principle for self-improvement is:
The system being optimized must not have unilateral authority over the system that defines success.
Use:
immutable holdout evals;
separate ownership of critical behavior specs;
versioned judge prompts;
human-labeled calibration sets;
signed release candidates;
independent policy enforcement;
and canary/rollback controls.
An agent may propose changing an eval when it discovers that the eval is broken. It should not silently weaken the eval until its work passes.
Where automated self-improvement works best
AlphaEvolve and related systems demonstrate strong improvement where proposed changes can be scored by crisp automated evaluators. (
Google DeepMind
https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/
)
The harder the domain is to evaluate, the more dangerous autonomous optimization becomes. An optimizer will exploit whatever your metric fails to capture.
That is why Troyanovsky is right that 
signal design is the hard part
. But signal quality must be established before it is allowed to drive automated change.

--------------------------------------------------------------------------------

Applying This to My Own Systems
For the kinds of systems you are building—coding agents, creative-production agents, product workflows, scheduled autonomous agents, and eventually fleets—I would apply the philosophy differently by domain.
Coding agents
Build around:
a short root 
AGENTS.md
 that acts as a map;
localized instructions near the relevant code;
typed tools;
isolated worktrees or sandboxes;
tests and linters;
architectural invariants;
persistent plans;
clean checkpoints;
a separate verifier;
and PR-style review artifacts.
Do not load the entire organizational handbook into every coding run.
Creative-production agents
Creative systems require more than checking that a file exists.
Use:
canonical model sheets;
project-specific style and continuity bibles;
provenance records;
artifact version IDs;
visual rendering;
continuity checks;
behavior specs for validation and disclosure;
and human taste review at important gates.
For a system like 
Anima
, one high-value behavior is:
After any meaningful visual edit, validate the current rendered artifact—not merely the prompt, source file, or an earlier render.
Another is:
Distinguish project canon from exploratory variations; experiments must not silently overwrite approved continuity.
Your existing taste context should be treated as layered canon:
personal evergreen taste


↓


project visual language


↓


sequence continuity


↓


shot-specific requirements
Do not put all four layers into every generation when only the shot-specific subset is needed.
Product-research agents
Require:
a claim ledger;
separation of fact, inference, and recommendation;
canonical company strategy;
current metrics definitions;
validated data queries;
source authority;
uncertainty;
and an explicit decision framework.
The final recommendation should not be the only artifact. Preserve the evidence package that makes it reviewable.
Autonomous scheduled agents
Add:
durable scheduling;
idempotency;
per-run budgets;
scoped credentials;
health checks;
retry limits;
automatic suspension after repeated critical failures;
heartbeat and liveness monitoring;
versioned context manifests;
and incident alerts.
A scheduled system should never fail silently for weeks while continuing to generate plausible-looking artifacts.
Local and cloud agents
Keep local and cloud authority separate.
A local coding agent may have broad access to a repository sandbox while possessing no Gmail or production credentials. A cloud research agent may have broad public-web access but only read-only access to internal material.
Do not create one all-powerful agent identity because the same agent participates in many workflows.
MCP
Use MCP as an adapter and interoperability layer, not as your system’s ontology or security model.
Your internal tool registry should still record:
semantic purpose;
input/output schema;
side effects;
permissions;
sensitivity;
cost;
latency;
idempotency;
and verification strategy.
Two MCP tools with overlapping descriptions can be just as confusing as two badly named internal functions.
Your 
code-brain
 or Obsidian-based knowledge
Markdown and Obsidian can be excellent for:
human-readable canon;
decisions;
project vocabulary;
procedures;
behavior specs;
and navigational indexes.
They should not be the only store for:
transactional run state;
credentials;
high-volume traces;
approvals;
or mutable fleet telemetry.
Use the vault as the legible knowledge layer; use structured operational stores for execution.

--------------------------------------------------------------------------------

One Complete Workflow
Scenario
An autonomous system runs a weekly product-opportunity investigation. It analyzes user feedback, support issues, usage data, market evidence, and technical constraints, then produces:
an evidence ledger;
opportunity assessment;
decision memo;
PRD draft;
risk register;
and an executive deck.
It may investigate and draft autonomously. It may not contact customers, commit roadmap resources, or publish externally without approval.

--------------------------------------------------------------------------------

1. Request
objective: Assess whether we should build automated agent-incident reconstruction.


deliverables:


- evidence-ledger.json


- decision-memo.md


- prd.md


- risk-register.json


- executive-deck.pptx


deadline: 2026-08-17


authority:


internal_read: allowed


public_web: allowed


customer_contact: prohibited


roadmap_change: prohibited
The control plane validates the requesting user and creates a 
Run
.

--------------------------------------------------------------------------------

2. Ontology lookup
The resolver identifies:
Product: Agent Platform


Capability: Incident Reconstruction


Related Goals:


- reduce time-to-diagnosis


- improve fleet trust


Related Projects:


- observability v2


- trajectory store


Related Policies:


- customer data handling


- external research


Related Decisions:


- remediation remains human-approved
Ambiguous references are converted into stable IDs.

--------------------------------------------------------------------------------

3. Context assembly
The compiler loads:
current product strategy;
approved metric definitions;
relevant prior decisions;
current architecture summary;
customer-data policy;
product-research behavior specs;
available skills;
and handles to feedback, analytics, and repository tools.
It does not load every historic roadmap deck or every support ticket.
A context manifest records the exact versions.

--------------------------------------------------------------------------------

4. Planning
The root agent creates milestones:
Customer-problem evidence
Quantitative impact
Market and competitor evidence
Technical feasibility
Governance and risk
Option synthesis
Artifact production
Independent review
It identifies validation requirements before starting:
analytics calculations must be reproducible;
market claims need current sources;
customer excerpts must be de-identified;
PRD must satisfy schema;
deck must be rendered;
no external communication.

--------------------------------------------------------------------------------

5. Subagent delegation
The orchestrator spawns four temporary subagents.
Customer-evidence agent
Tools:
support-ticket search;
interview repository;
de-identification service.
Output:
clustered needs;
representative evidence;
confidence and sample limitations.
Quantitative analyst
Tools:
governed SQL;
metric catalog;
notebook execution.
Output:
reproducible queries;
calculations;
sensitivity analysis.
Market researcher
Tools:
public web;
source archive.
Output:
claim ledger;
primary-source evidence;
fact/inference separation.
Technical-feasibility agent
Tools:
read-only repository;
architecture docs;
test environment.
Output:
implementation options;
dependencies;
constraints;
unknowns.
Each subagent operates in an isolated context and writes artifacts to the shared evidence store.

--------------------------------------------------------------------------------

6. Persistent notes and state
As results arrive, the root agent updates:
completed tasks;
received artifact IDs;
unresolved conflicts;
current hypotheses;
budget;
and next eligible actions.
One subagent reports that customers want “automatic remediation.” Another finds that the strongest demand is actually faster diagnosis rather than autonomous fixes.
The contradiction is preserved rather than averaged away.

--------------------------------------------------------------------------------

7. Context compaction
Before the root context becomes noisy:
raw subagent outputs remain in the artifact store;
the claim ledger is updated;
conclusions and conflicts are summarized;
hypotheses ruled out are recorded;
and a Memento handoff packet is written.
The next inference starts with current state, the evidence index, and selected high-value results.

--------------------------------------------------------------------------------

8. Synthesis
The root agent compares three options:
A. Full automatic remediation


B. Automatic incident reconstruction with recommended next actions


C. Improved trace search only
It evaluates:
user value;
evidence strength;
technical cost;
governance risk;
time to value;
strategic fit;
and reversibility.
It recommends B, while stating that B’s demand estimate depends on a support-ticket sample that may overrepresent enterprise customers.

--------------------------------------------------------------------------------

9. Deterministic verification
The assurance plane checks:
all quantitative claims link to executable queries;
query results match the memo;
all citations resolve;
customer data is de-identified;
the PRD conforms to its schema;
required sections exist;
artifact checksums are current;
no external-send tool was called;
and the deck opens and renders.
A stale chart is found because the deck was generated before the final metric update.
The artifact-validation behavior fails.

--------------------------------------------------------------------------------

10. Recovery
The agent:
regenerates the chart;
updates the deck;
rerenders it;
checks the new slide images;
and records the new checksum.
It does not treat the previous render as evidence for the new deck.

--------------------------------------------------------------------------------

11. Behavior evaluation
Judges evaluate:
authoritative sourcing;
fact/inference separation;
material uncertainty disclosure;
current-artifact validation;
controlled external communication;
and evidence preservation.
One behavior receives 
NA
 because no external communication was attempted. That is different from insufficient evidence.

--------------------------------------------------------------------------------

12. Independent review
A reviewer receives:
objective;
acceptance criteria;
final artifacts;
evidence ledger;
current canon;
and declared assumptions.
It is not initially shown the producer’s confidence score.
The reviewer challenges the market-size estimate and finds that one competitor claim describes a beta feature rather than generally available functionality.
The market claim is downgraded and the decision memo revised.

--------------------------------------------------------------------------------

13. Human approval
The product owner receives a compact review packet:
recommendation;
strongest supporting evidence;
material assumptions;
alternatives rejected;
unresolved risks;
reviewer findings;
and artifact links.
The human can:
accept;
request revision;
reject;
or authorize a follow-up customer study.
The system cannot commit the roadmap itself.

--------------------------------------------------------------------------------

14. Final artifact and receipt
The final work receipt records:
run ID;
artifact checksums;
context versions;
source ledger;
verifier results;
behavior verdicts;
reviewer disposition;
human decision;
cost;
duration;
and model/tool versions.

--------------------------------------------------------------------------------

15. Improvement signal
The trajectory generates two improvement candidates:
The competitor-research skill should distinguish announced, beta, and generally available features.
The deck workflow needs a dependency check ensuring charts are regenerated after source metrics change.
The system drafts:
one new adversarial eval case;
one tool dependency proposal;
and one skill revision.
Those changes run offline and require approval before rollout.
That is a closed improvement loop without allowing the production agent to rewrite its own standard of success.

--------------------------------------------------------------------------------

What I Would Build Today
Starting from scratch, I would build the following minimum serious architecture.
1. One primary agent loop
One strong reasoning model with:
typed tools;
structured outputs;
explicit stop conditions;
and trace capture.
No elaborate agent hierarchy.
2. Git-backed world definitions
Use Markdown and YAML for:
canon;
vocabulary;
procedures;
skills;
behaviors;
authority maps;
and design decisions.
Give each important document an owner and scope.
3. A context compiler
Do not concatenate files manually.
Implement:
task classification;
entity resolution;
authority filtering;
freshness;
relevance ranking;
context budgets;
conflict detection;
and a context manifest.
4. Typed tool contracts
Use JSON Schema, Pydantic, Zod, or equivalent.
Every tool declares:
purpose;
side effects;
permissions;
inputs;
outputs;
errors;
and verification method.
5. External state
Use:
SQLite or Postgres for runs, tasks, checkpoints, approvals, and memory metadata;
local files or object storage for artifacts and large evidence;
append-only events for consequential state changes.
6. Three to eight behavior specs
Start with the behaviors that most directly affect trust:
source grounding;
artifact validation;
uncertainty escalation;
external communication;
protection of user work;
and evidence preservation.
7. A layered eval suite
Start with perhaps 20–50 carefully selected cases, not thousands.
Include:
normal cases;
ambiguous cases;
tool failures;
stale data;
conflicts;
permission boundaries;
adversarial content;
and known historical failures.
8. Deterministic verifiers
Build domain-specific feedback:
code tests;
file rendering;
schema validation;
calculations;
source resolution;
checksums;
and policy assertions.
9. A separate reviewer path
Initially, use:
fresh context;
a stricter evidence-first rubric;
and no write or execution permissions.
Use a different model family for especially consequential reviews where cost permits.
10. Hard approval boundaries
Require explicit approval for:
external messages;
public publication;
production changes;
destructive operations;
financial actions;
and permission expansion.
11. Full traces
Record:
context manifest;
model calls;
tool calls;
artifacts;
state changes;
validators;
behaviors;
and approvals.
12. Simple improvement workflow
trace → failure label → candidate eval → proposed change


→ regression run → human approval → canary
Practical technology posture
Markdown/YAML
 for legible canon and specs.
Postgres or SQLite
 for operational state.
Filesystem/S3-compatible storage
 for artifacts and evidence.
OpenTelemetry-style tracing
 for observability.
MCP adapters
 where interoperability is useful, behind your own policy and tool registry.
A durable workflow engine
 once jobs regularly span hours, wait for approvals, or must survive process restarts.
A vector index only after retrieval evaluation shows a need.

--------------------------------------------------------------------------------

What I Would Add Later
Stage 1: Simple reliable agent
Add:
one agent;
typed tools;
external state;
deterministic verification;
traces;
representative evals;
human approval.
Do not add:
knowledge graph;
multi-agent chat;
RL;
autonomous prompt rewriting.
Stage 2: Long-running agent
Trigger: tasks exceed one context, involve waits, or must recover from interruption.
Add:
durable workflow;
checkpoints;
artifact store;
handoff packets;
compaction;
idempotency;
retry classification;
explicit resume logic.
Stage 3: Multi-agent system
Trigger: measured bottlenecks from context overload, parallel work, permission separation, or review.
Add:
bounded subagent contracts;
isolated contexts;
role-specific permissions;
aggregation;
independent review;
depth and budget limits.
Do not add persistent agent personas without durable responsibilities.
Stage 4: Autonomous fleet
Trigger: many scheduled or concurrent runs with meaningful operational burden.
Add:
scheduler and queue;
tenant isolation;
fleet-wide policy engine;
quotas;
per-agent identities;
health monitoring;
anomaly detection;
circuit breakers;
incident response;
rollback;
versioned rollouts;
and cost allocation.
Stage 5: Self-improving infrastructure
Trigger: large volume of high-quality traces and a trusted eval portfolio.
Add:
automated failure clustering;
eval-case drafting;
controlled candidate generation;
sandboxed harness changes;
immutable holdouts;
canaries;
independent approval;
and possibly domain-specific post-training when harness gains plateau.
Do not allow the system to control both its optimization target and release authority.

--------------------------------------------------------------------------------

Anti-Patterns
Giant universal system prompts
They mix unrelated scope, become contradictory, consume attention, and are difficult to test.
Better:
 short universal principles plus localized, progressively disclosed context.
Vector database everywhere
Similarity search does not establish authority, recency, identity, or truth.
Better:
 use structured lookup for known entities, keyword search for exact facts, and embeddings where semantic retrieval is actually measured to help.
Huge knowledge graph before product fit
A graph can become a costly model of imagined future needs.
Better:
 stable IDs, typed relations, canon, and ordinary storage first.
Multi-agent theater
Several agents with different job titles but identical context, tools, models, and authority do not create meaningful specialization.
Better:
 spawn another agent only for parallelism, isolation, permission separation, or independent evidence.
Agent chat rooms
Free-form agents discussing a problem indefinitely create cost and information distortion without clear ownership.
Better:
 structured delegation and artifact-based aggregation.
Memory as a transcript dump
Raw history grows without bound and retrieval becomes noisy.
Better:
 separate events, state, episodic lessons, canon, and derived summaries.
Canonical summaries with no source links
A summary silently becomes truth even after its source changes.
Better:
 summaries carry provenance, version, and invalidation rules.
Outcome-only evals
Correct-looking outputs conceal unsupported, unsafe, or irreproducible work.
Better:
 outcome, behavior, provenance, authority, and operational evaluations.
Judge-only verification
A persuasive LLM verdict replaces actual testing.
Better:
 deterministic checks first, semantic judges for the remainder.
Same-model self-review treated as independent assurance
The reviewer reproduces the producer’s blind spots.
Better:
 fresh context, different evaluation framing, model diversity, deterministic evidence, and calibrated human review.
Prompt-only security
The agent is “told” not to access, send, or delete something.
Better:
 deterministic authorization and enforcement at the tool boundary.
Retrying everything
Permission failures, logical errors, and destructive partial failures are treated like network timeouts.
Better:
 classify failures and make side effects idempotent.
Autonomous live prompt rewriting
A production agent changes its instructions based on a few recent failures.
Better:
 offline proposals, evals, versioning, canary, approval, rollback.
Thousands of behavior rules
The behavior system becomes an unmaintainable duplicate prompt.
Better:
 a sparse set of high-value, recurring product contracts.
Overprescribed processes
The agent is forced to follow a brittle historical workflow even when a better evidence-preserving path exists.
Better:
 specify invariants, evidence, authority, recovery, and boundaries.
Framework lock-in
The architecture becomes inseparable from one agent framework or model vendor.
Better:
 keep state, tool contracts, canon, traces, and policy portable.
No explicit termination condition
The agent stops when it feels done—or loops until budget exhaustion.
Better:
 machine-checkable completion gates and escalation conditions.
No versioned context manifest
A regression cannot be traced to the prompt, policy, document, model, or tool version that caused it.
Better:
 record the full runtime configuration for important runs.
Letting agents write directly into canon
One mistaken inference becomes organizational truth.
Better:
 candidate memory and proposed canon changes pass validation and ownership review.

--------------------------------------------------------------------------------

Troyanovski Design Checklist
Goal and authority
Is the objective concrete?
Is “done” externally testable?
Is the agent’s authority explicitly scoped?
Are external, destructive, financial, and privileged actions gated?
Is there a time, cost, and action budget?
World and context
Are important entities represented by stable IDs?
Can the agent distinguish canon from history and hypothesis?
Are sources marked with owner, version, freshness, and authority?
Is context compiled rather than indiscriminately concatenated?
Can the agent retrieve deeper evidence on demand?
Are external documents treated as untrusted data?
Is the context manifest recorded?
Tools and execution
Does every tool have one legible purpose?
Are inputs and outputs typed?
Are side effects and permissions explicit?
Can the agent observe whether the action succeeded?
Are side-effecting calls idempotent?
Can the run survive interruption and resume safely?
State and memory
Is current state outside the model?
Are raw events separate from current state?
Are observations separated from validated memory?
Do memories carry provenance, scope, time, and supersession?
Is there a future-self handoff before compaction?
Can stale or poisoned memories be invalidated?
Behaviors and evaluation
What are the few recurring behaviors that matter most?
Can each behavior be judged from observable evidence?
Does each critical behavior have an implementation mechanism?
Are outcome and process evaluated separately?
Are deterministic checks used before model judges?
Are judges calibrated against human labels?
Are 
not applicable
 and 
insufficient evidence
 distinguished?
Does the eval set include ambiguity, failure, adversarial cases, and production incidents?
Multi-agent design
Is another agent genuinely necessary?
Does it have a bounded objective and return schema?
Does it have distinct context, tools, or permissions?
Is delegation depth limited?
Does independent review reduce correlation meaningfully?
Is aggregation based on evidence rather than agent agreement?
Governance and operations
Are permissions enforced outside the model?
Are secrets scoped per user, run, and tool?
Are all consequential actions auditable?
Can the system be paused, revoked, and rolled back?
Are fleet health, drift, cost, and failure rates monitored?
Is there an incident-to-eval process?
Can the system improve only through a controlled release path?

--------------------------------------------------------------------------------

My Recommended Agent Engineering Philosophy
Here is the philosophy I would adopt from Troyanovsky, current research, and the architectural implications above.
1. The model is not the system
Model intelligence is raw capability. Useful autonomous work emerges from the interaction among the model, environment, tools, state, feedback, and authority.
2. Agency is delegated authority
An agent is not autonomous because it produces multiple reasoning steps. It is autonomous to the extent that the environment permits it to choose and execute consequential actions.
3. Long horizon is a state problem before it is a token problem
Do not build one endless conversation. Build durable work that can be resumed by a fresh inference from structured state and evidence.
4. Build a world, not a prompt
Give the agent stable concepts, identities, sources of truth, relationships, and navigational structure.
5. Capture richly and disclose selectively
Preserve raw human context and evidence, but compile only the highest-value material into each inference.
6. Canon is a control surface
Current organizational truth must have owners, versions, scope, freshness, and authority. Agents cannot safely infer canon from the average of everything ever written.
7. Tools are contracts
A tool is where nondeterministic reasoning meets deterministic consequence. Its semantics, permissions, outputs, and failure states deserve first-class design.
8. State is external; context is a view
The context window should contain a task-relevant projection of state. It should not be the only place state exists.
9. Every consequential action should leave evidence
A useful agent does not merely perform work. It creates a reviewable chain from objective to evidence to decision to action to resulting state.
10. Make the environment capable of disagreement
Tests, renderers, schemas, simulators, policy engines, and reviewers should be able to tell the agent that its current path is wrong.
11. Evaluate both achievement and conduct
Outcome correctness establishes that something worked. Behavioral, provenance, safety, and operational evaluation establish whether it can be trusted and repeated.
12. Specify invariants, not choreography
Preserve primary sourcing, evidence, review, authority, safety, and recovery. Allow the agent freedom over implementation details that do not threaten those properties.
13. Independence must be engineered
Fresh context helps. Different models help. Deterministic checks help more. Human expertise remains necessary where the value or risk warrants it.
14. Memory must be curated
Raw history is not memory. Promote validated lessons, preserve provenance, support supersession, and aggressively separate temporary state from enduring truth.
15. Multi-agent complexity must earn its keep
Use one capable agent until parallelism, context isolation, specialization, permission separation, or independent review creates measurable value.
16. Autonomy should be task-scoped, reversible, and earned
Trust is not a personality judgment. It is evidence that a particular system version can perform a particular task class within a particular control envelope.
17. Improvement is an engineering release process
Agents may diagnose and propose their own improvements. Evals, ownership, holdouts, canaries, approvals, and rollback determine whether those changes reach production.
18. Prefer systems that compound
Build reusable context, identity, tools, evidence, state, evaluation, and governance layers. Keep domain judgment, acceptance criteria, workflows, and critical behaviors specific.
19. Simplicity is a reliability feature
Every agent, memory store, tool, rule, retriever, and framework adds another possible failure surface. Add complexity only when a measured problem justifies it.
20. The real craft is environment design
The exceptional agent engineer is not primarily the person who writes the cleverest prompt. It is the person who can:
model the world clearly;
externalize state;
make evidence accessible;
design usable capabilities;
create feedback;
define acceptable conduct;
constrain authority;
observe failure;
and turn failure into a controlled improvement.
That is the deepest lesson in Troyanovsky’s philosophy.
The best mental model for building reliable, scalable, long-horizon systems today is therefore:
You are designing an institution for machine intelligence.
The model is one worker within that institution. Your architecture determines what it knows, what it can do, how it learns about consequences, what it remembers, who reviews it, when it must stop, and why anyone should trust the work it produces.
