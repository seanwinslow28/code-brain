---
title: "Making agent eval review easier to learn: primary-source evidence"
date: 2026-09-14
type: research
status: research-complete
tags:
  - evals
  - learning
  - annotation
  - research
---

# Making agent eval review easier to learn

Research for an approval plan, not an implementation. This note uses nine core primary sources: one practitioner account, three official product/framework documents, and five original experimental papers. Product documentation establishes available patterns, not educational effectiveness. The experiments studied algebra, prose, and science explanations; applying their findings to agent-evaluation review is a design inference that needs local testing.

The supplied context is an existing local viewer for 18 agent-trace entries, with deterministic checks, machine-auditor findings, and empty human labels. It already provides visual summaries and navigation. The incremental opportunity is therefore clearer evidence and instruction inside the review flow. No private target-project contents were read or used in web searches for this note. No viewer, labels, audio, or external service was changed.

## Findings from original learning research

### 1. Show how to make one judgment before asking for independent judgments

Sweller and Cooper's five-experiment study found that studying worked algebra examples reduced time spent during acquisition and improved speed and errors on later problems with the same structure. The benefits did not establish broad transfer across different problem structures. This is evidence for teaching a recognizable procedure through examples, with an explicit boundary on generalization. [Sweller & Cooper, 1985, original paper, pp. 59–89](https://onderwijs.felienne.nl/vakdidactiek/materiaal/sweller_worked_examples.pdf)

**Design inference:** Teach one complete review: criterion → observable evidence → interpretation → decision. Then give a similar case for the person to judge. Use varied cases over time. Since the 18 human labels are empty, a worked example must be visibly synthetic or separately adjudicated by a human; a machine verdict cannot silently become the answer key. This paper does not identify an optimal number of examples for eval review.

### 2. A small recall prompt can be more useful than another explanation

In two experiments, students studied prose and either restudied or took free-recall tests without feedback. Restudy helped at five minutes; retrieval produced better retention after two days or a week. Repeated study also increased confidence, illustrating that feeling familiar with material can diverge from later recall. [Roediger & Karpicke, 2006, original publication and abstract](https://journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x)

**Design inference:** After a worked case, invite the learner to explain which observation supports the criterion, or what evidence would be missing, before revealing the teaching explanation. Revisit that distinction on a later case. This is a learning interaction, separate from saving a production label. The study measured recall, not agent-review judgment accuracy; a click-through quiz alone would not establish learning.

### 3. Let the learner control the pace of an explanation

Mayer and Chandler tested narrated animations about lightning in two experiments. Learner-controlled, segmented presentations improved problem-solving transfer relative to the relevant continuous-presentation comparisons, but not retention. The intervention changed pacing and opportunities to process parts, not just total clip length. [Mayer & Chandler, 2001, original paper, pp. 390–397](https://tecfa.unige.ch/tecfa/teaching/methodo/Mayer_Chandler01.pdf)

**Design inference:** A short explanation can have three manually navigable beats: intended outcome, decisive event, and what the evidence does or does not establish. Provide pause, replay, and direct access to each beat. A proposed 60–90-second duration is a practical first prototype, not a scientifically demonstrated optimum. These results do not show that audio is superior to a well-written static case explanation.

### 4. Make the structure visible, with selective cues

Mautone and Mayer tested lessons about airplane lift in printed, spoken, and narrated-animation formats. Structural signals such as previews, headings, and connecting language improved performance on transfer questions. The signals clarified organization without adding more substantive lesson content. [Mautone & Mayer, 2001, original article abstract and author-provided record](https://www.researchgate.net/publication/232494695_Signaling_as_a_Cognitive_Guide_in_Multimedia_Learning)

**Design inference:** Place short labels beside the material they explain: “criterion,” “observed evidence,” “machine interpretation,” and “your judgment.” During a narrated case, highlight the relevant trace event when discussing it. Do not highlight every field or convert the existing viewer into a larger visual summary. The study does not demonstrate that a particular color, tooltip, or glossary will improve this user's review.

### 5. More simultaneous media can add work

Mayer, Heiser, and Lonn ran four experiments with narrated lightning animations. Concurrent text summarizing or duplicating narration worsened retention and transfer in the relevant experiments. Interesting but irrelevant additions also reduced transfer. [Mayer, Heiser & Lonn, 2001, original article and author-provided text](https://www.researchgate.net/publication/232530555_Cognitive_Constraints_on_Multimedia_Learning_When_Presenting_More_Material_Results_in_Less_Understanding)

**Design inference:** Narration should explain why a small amount of visible evidence matters, rather than read a large process note while the learner scans a trace. Keep the complete transcript and user-controlled captions available. The findings are not a reason to remove accessibility support, required evidence text, or a readable alternative. They do not test optional transcripts, agent trace tables, or this user's context. No claim about fixed “visual” or “auditory” learning styles follows from these studies.

## Practitioner workflow and current UI patterns

### 6. Hamel Husain and Shreya Shankar: learn from actual cases

Their jointly authored guide recommends reviewing traces, writing open-ended observations, and grouping recurring failures into an application-specific taxonomy. It advocates simple pass/fail judgments, product-specific rendering, collapsed secondary detail, and bounded review progress. It also distinguishes inexpensive objective checks from judgments that require human interpretation. The authors explicitly frame their advice as practitioner opinions, not universal truths. [Husain & Shankar, *AI Evals: Everything You Need to Know*, updated September 1, 2026](https://hamel.dev/blog/posts/evals-faq/)

**Implication:** Put the actual output and supporting evidence beside a small rubric. Allow a short observation before demanding a category. The existing visualizations are useful context; the missing teaching material is a concrete explanation of a judgment. Numerical claims about review speed or prescribed sample sizes in this practitioner guide should not be presented as experimental evidence or a requirement for beginning with 18 entries.

### 7. LangSmith: one case, persistent rubric, deliberate completion

The current annotation-queue documentation describes a focused item-by-item view, instructions and category descriptions beside each item, rubric feedback, and reviewer progress. Run items support reviewer notes and acceptance assertions; capabilities differ for full-thread items. [LangSmith, *Use annotation queues*](https://docs.langchain.com/langsmith/annotation-queues)

**Implication:** An existing local viewer can borrow the interaction pattern without adopting the platform: one clearly identified review target, its evidence, short category definitions, and an explicit next step. Queue progress is a count of completed reviews, not a quality score.

### 8. Braintrust: distinguish human judgments and expose detail conditionally

Braintrust describes human review as structured judgment used to assess automated scores and establish reference feedback. Its current configuration supports categorical and free-form inputs, explanatory descriptions, and conditions that show a more detailed rubric only when relevant. [Braintrust, *Set up human review*](https://www.braintrust.dev/docs/annotate/human-review)

**Implication:** Keep human labels visibly separate from automated results. Present the core judgment first, with deeper questions available when a case needs them. This is evidence of an implemented progressive-disclosure pattern, not proof it reduces novice anxiety. It is not a recommendation to purchase a service.

### 9. Inspect: investigate the scorer as well as the result

Inspect's log viewer provides separate access to message history, scoring, and metadata. Its documentation explains that a scorer can fail while extracting an answer or while comparing it with the reference; filtering by score can help determine whether an apparent incorrect result is a scorer issue. [Inspect, *Log Viewer*](https://inspect.aisi.org.uk/log-viewer.html)

**Implication:** A review should name its target explicitly. “Is the artifact acceptable?” and “Is the auditor's finding justified?” require different evidence. An auditor can correctly detect a defective artifact; the artifact would fail while the finding would be supported. A wrong or unsupported finding does not, by itself, prove that the artifact is good. This distinction is a proposed application of Inspect's scorer-inspection principle, not a result tested by its documentation.

## Concrete implications for the 18-entry report

The following are proposed review semantics and teaching devices, not new findings about the private data.

| Item | Proposed treatment | Basis |
|---|---|---|
| Review target | State whether the person is judging the artifact, an auditor finding, or both under separate criteria. | Inspect's distinction between output and scoring inspection. |
| Deterministic result | Show the rule tested, result, and relevant evidence. “Rule passed” establishes only that rule's result. | Task-specific evaluation in Husain and Shankar; scorer limits in Inspect. |
| Machine finding | Identify it as machine analysis; show the claimed defect and exact supporting excerpt or a clear evidence-missing state. | Inspect's scoring view and review-target distinction. |
| Human decision | Preserve empty labels until deliberately supplied by a person. Allow “come back later” as workflow state, rather than silently recording a pass or fail. | Human-review patterns; required label provenance in the task brief. |
| Summary | Show “0 of 18 reviewed” initially. Human pass rate and machine–human agreement are unavailable until the relevant human judgments exist. | Arithmetic and provenance, not a research claim. |
| Teaching example | A separately marked synthetic or human-adjudicated case, followed by a similar independent case. | Worked-example research; transfer limits apply. |
| Process explanation | A short plain-language explanation beside the needed evidence, with the longer process note available on demand. | Signaling and segmentation research; product patterns for conditional detail. |

Do not convert counts of clean checker categories into artifact accuracy, reviewer confidence, or auditor reliability. Even after labels exist, aggregate metrics need a named target, denominator, rubric, and sampling context. Eighteen selected cases can support learning and discovery; the supplied brief does not establish a representative sample of all agent behavior.

## Optional audio experiment

Prototype only after approval: one source-grounded case explanation, approximately 60–90 seconds, with three visual beats and an equivalent transcript. The proposed sequence is:

1. State the review target and acceptance criterion.
2. Show the exact evidence and explain what it supports.
3. Identify the unresolved inference, then invite the learner's judgment or a small recall response.

An explanation of a machine-auditor finding should say what the auditor claimed and why its cited evidence may matter; it must not narrate an unreviewed verdict as settled human truth. If a real case becomes the worked answer, obtain its human adjudication first. Use no autoplay. Support text-only use, pause, replay, and captions. The rationale is learner control, relevant visual cues, and avoiding competing content, inferred from the three multimedia experiments above.

The first check should be modest: can the learner identify the review target, locate decisive evidence, distinguish a passed rule from a correct artifact, and explain their own choice on a similar case? Observe where they hesitate and whether they need the long process note. Confidence and liking the audio can be recorded separately, but do not substitute for demonstrated understanding. The exact duration, number of example cases, default disclosure state, and benefit of audio over text remain untested design choices.

## Source and access notes

- Sources were inspected on September 14, 2026. Official documentation can change; the observations above describe the pages retrieved on this date.
- Original papers were read through publisher abstracts, original PDF copies, or author-provided ResearchGate records. The APA site was unavailable to this browsing session; the signaling claim is limited to the original article's abstract, not an independently inspected methods analysis. No secondary summary was used as evidence for the experimental findings.
- This is a focused set of primary studies, not a systematic review or meta-analysis. It supports a low-cost design hypothesis; it does not establish learning gains, anxiety reduction, or durable reviewer competence for the proposed viewer.
