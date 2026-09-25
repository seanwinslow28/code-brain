---
title: "Voice transfer: are personal stories enough, or does a voice library need stances?"
date: 2026-09-24
type: research
status: draft
tags:
  - research
  - writing
  - llm-style-imitation
  - personalization
  - few-shot
  - voice
---

# Voice transfer: are personal stories enough, or does a voice library need stances?

## Takeaway

**Probably not enough, and there are two separate reasons.**

1. **Register gap (style).** Stories do carry the markers of style that hold across topics: function words, syntax, punctuation and rhythm. Those markers survive a *topic* change better than a *genre* change, though. An opinion piece is a different genre from a memoir essay. No study has tested few-shot LLM imitation across genres for one author; the main 2025 benchmark says outright that cross-genre transfer "remains unexplored." What evidence exists suggests the model will copy his sentences and then fall back on its own default way of building an argument.
2. **Viewpoint gap (content).** In the research, "slop" comes from missing substance as much as from style. The best predictors of readers calling text slop are relevance and information density. Homogenization in co-written essays comes from the *ideas the model contributes*. When a model isn't given the writer's positions, it supplies its own. Stories let a model guess the direction of his stance. They don't give it his argument.

**Practical answer:** keep the stories as the base. Add a small number of argumentative pieces in his voice (on any topic) and a stance file on the target topics. Don't bother matching the samples to the topic. **Diversity of genre beats volume within one genre**; the evidence for this is moderate and from 2025. Test it with the two-question blind test in section 6.

---

## 1. What transfers across topic and genre

**Stylometry (the classical evidence).**
- Function words are the standard topic-independent style marker because authors use them "in a largely unconscious manner" ([Stamatatos 2009 survey, JASIST; tier A, author preprint](https://icsdweb.aegean.gr/stamatatos/papers/survey.pdf)). The same survey warns that attribution corpora need to control for genre and topic, because both contaminate the author signal.
- Topic words get in the way: masking nouns and proper nouns improves cross-domain attribution. Syntax helps most in *cross-genre* attribution, and lexical information helps most in *cross-topic* attribution ([Sundararajan & Woodard, COLING 2018; tier A](https://aclanthology.org/C18-1238.pdf)). Put simply, a topic change mostly swaps vocabulary, while a genre change also rearranges structure.
- Cross-genre verification is measurably harder. One test used the same five authors writing both prose and plays, and verification worked on the prose but broke down on the theatre texts ([Kestemont et al. 2012, *English Studies*; tier A](https://www.tandfonline.com/doi/abs/10.1080/0013838X.2012.668793)).

**LLM imitation of individual writers (2024–2026).**
- *Catch Me If You Can? Not Yet* covers 400+ real authors in news, email, forum and blog writing ([Wang et al., EMNLP 2025 Findings; tier A](https://arxiv.org/abs/2509.14543)). The prompt held content fixed with a summary. Few-shot examples beat zero-shot for every author. Models did reasonably well on structured genres (news, email) and poorly on informal ones (blogs, forums). The authors limited the study to same-genre prompting: cross-genre style transfer "remains unexplored due to the lack of multi-genre corpora" ([PDF, §Limitations](https://aclanthology.org/2025.findings-emnlp.532.pdf)). **So nobody has directly tested the question asked here (memoir samples, op-ed target).**
- *PersonalBench* ran five-shot, profile-extraction and contrastive methods on 50 blog authors. Every method scored *below* the similarity between two random human authors (LUAR 0.48–0.51 against a human cross-author floor of 0.63). The authors conclude the LLM's own fingerprint dominates ([Sawant, arXiv 2608.19746, Aug 2026; tier A, preprint, not peer-reviewed](https://arxiv.org/html/2608.19746)).
- A forensic study used ChatGPT to imitate 300 product-review authors. Its outputs gave "little to no useful" same-author evidence. It overused formulaic openers ("let me tell you") and dropped the specific brands, digits and first-person detail that the humans used ([Ishihara, *Digital Scholarship in the Humanities*, 2026; tier A](https://academic.oup.com/dsh/advance-article/doi/10.1093/llc/fqag079/8703383)).
- On a narrower academic-essay set, few-shot prompting improved style-matching accuracy up to 23.5x over zero-shot. Even the matched outputs were far more predictable than human text (perplexity 15.2 vs 29.5) ([Jemama & Kumar, IEEE UEMCON 2025; tier A](https://arxiv.org/abs/2509.24930)).
- Prompting with 20 excerpts plus a style description, in the voice of 50 literary authors, lost badly to MFA writers with expert judges (odds ratio 0.16 for fidelity). Fine-tuning on the author's complete works flipped that result (OR 8.16). Experts described the in-context outputs as clichéd, purple and over-explained ([Chakrabarty, Ginsburg & Dhillon, arXiv 2510.13939, 2025; tier A, preprint](https://arxiv.org/html/2510.13939v3)).

**Read-across for the question.** Examples carry style, and they beat rules and zero-shot. Genre is the weak joint in both the stylometry and the LLM results, and the one direct test of genre mismatch hasn't been run. A library that is all memoir, asked for an argument, is exactly that untested case.

## 2. Content vs. style: is slop a missing-viewpoint failure?

**Nicolas Cole's claim** is that AI writing goes generic because the model "does not know you." He says the missing input is what he calls "Personality Content": personal stories, specific life facts, chosen opinions and lessons ([Cole, *The Right Way To Write With AI*, Sept 2026; tier D, Substack, no research cited](https://artandbiz.substack.com/p/the-right-way-to-write-with-ai)). His list includes opinions alongside stories.

**Research support: real, but partial.**
- **Slop is judged heavily on content.** Experts rated slop across info-utility, info-quality and style axes. All seven codes predicted a slop label, and the strongest were **Relevance** (β=0.06), **Density** (β=0.05) and Tone (β=0.05). Text "lacking relevance and information" was labeled slop in every domain ([Shaib, Chakrabarty, Garcia-Olano & Wallace, arXiv 2509.19163; tier A, preprint under review](https://arxiv.org/abs/2509.19163)).
- **Homogenization comes from the model's ideas.** In argumentative essays co-written with InstructGPT, the loss of diversity was "mainly attributable to InstructGPT contributing less diverse text," measured at the key-point level. User-contributed text was unaffected ([Padmakumar & He, ICLR 2024; tier A](https://arxiv.org/pdf/2309.05196)).
- **Without the writer's opinions, the model supplies its own.** An assistant configured to favor one side shifted what 1,506 participants wrote, and their stated views ([Jakesch et al., CHI 2023; tier A](https://arxiv.org/pdf/2302.00560)).
- **Telling a model who you are doesn't fix sameness.** In 30,000 admissions essays, identity-prompted and unprompted LLM essays were more similar to each other than to human essays ([Lee, Alvero, Joachims & Kizilcec, arXiv 2503.20062; tier A, preprint](https://arxiv.org/abs/2503.20062)).
- **Off-topic writing yields only a coarse stance.** GPT-4o predicted a user's binary stance on a target from 50 tweets that never mentioned it, at 68–85% balanced accuracy depending on the topic ([Loh et al., arXiv 2409.14395; tier A, preprint](https://arxiv.org/html/2409.14395)). That covers a direction of agreement. It doesn't cover an argument.
- Personalization evaluation now scores **content and style separately**, treating them as distinct things a personalized text must match ([ExPerT, Salemi et al., ACL 2025 Findings; tier A](https://arxiv.org/abs/2501.14956)).

**Counter-evidence (style failure is also real).** Catch Me and Chakrabarty both *specified the content* and still found clear style failures. So slop is both a style failure and a viewpoint failure, and the two can happen independently. Cole is right that viewpoint is necessary. The research doesn't show it is sufficient.

**Evidence gap.** I found no study showing that adding a writer's *stated opinions* to a few-shot prompt improves perceived voice on a new topic. That link is inferred, not tested.

## 3. How much text, and diversity vs. volume

- **In-context quantity plateaus early.** Going from 2 to 10 examples barely moved attribution, verification, style-model or detector scores ([Wang et al. 2025, Fig. 5](https://aclanthology.org/2025.findings-emnlp.532.pdf)). Anthropic's own guidance suggests 3–5 examples ([Claude prompting best practices; tier B](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)).
- **Topic-matched examples hurt style.** Picking the 5 examples from the same topic cluster as the target *reduced* attribution. The authors' explanation is that a narrow cluster reduces stylistic diversity. Length matching also lowered style-model accuracy ([Wang et al. 2025, §6.2](https://aclanthology.org/2025.findings-emnlp.532.pdf)). This is the most direct evidence that **diversity beats topical relevance for voice**.
- **Topic-relevant retrieval helps content metrics.** In LaMP, retrieving the user's relevant items (BM25/Contriever) beat random items on every task, but those tasks are scored on content overlap (ROUGE) and accuracy ([Salemi et al., ACL 2024; tier A](https://aclanthology.org/2024.acl-long.399/)). So on-topic material helps with *what* gets said, not *how* it's said.
- Anthropic's docs ask for examples that are both **relevant** ("mirror your actual use case") and **diverse** ([tier B](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)). For this question, "relevant" is best read as matching the *genre*, since matching the topic hurt style in the study above.
- **Floor for measurement, not prompting.** Reliable stylometric attribution needs roughly 5,000 words per sample for English ([Eder, DSH 2015; tier A](https://academic.oup.com/dsh/article-abstract/30/2/167/390738)). Any "does this sound like me" metric run on one 800-word draft will be noisy.
- **Past a certain library size, the evidence points to fine-tuning.** When there is a lot of text, fine-tuning on complete works beat in-context prompting by a wide margin ([Chakrabarty et al.](https://arxiv.org/html/2510.13939v3)).

## 4. Practitioner reports (tier C/D; anecdotal)

- **Every / Spiral (tier C; vendor, product marketing).** The product pairs uploaded style examples with an **interviewer agent** that questions the user about what they mean before drafting ([Spiral v3 launch](https://every.to/on-every/introducing-spiral-v3-an-ai-writing-partner-with-taste)). Its GM says in an interview that drafts go flat when context is thin, not because style is missing, and that hard rubrics failed ([podcast transcript](https://every.to/podcast/transcript-spiral-s-creator-on-why-better-writing-means-better-thinking)). The design choice amounts to style from examples plus ideas from an interview.
- **Andrew Eddie (tier D).** He built a profile from 169 posts and reported that a mix of tutorials, *opinion pieces*, announcements and informal writing "reveals different facets of the same voice." He suggests 20–30 substantial pieces across content types ([dev.to, 2024](https://dev.to/eddieajau/teaching-ai-to-write-like-you-3aae)).
- **Jeremy Morgan (tier D).** With about 255 posts, output on his home topic (technical tutorials) was close to his own. Off-voice quirks crept in: more enthusiasm and cheese from one model, profanity he never uses from another ([blog, Oct 2024](https://www.jeremymorgan.com/blog/generative-ai/hey-ai-write-like-me/)).
- **Ran Isenberg (tier D).** He adds an about-me context file and a rule to "ask clarifying questions instead of filling gaps with generic filler" ([blog, Apr 2026](https://ranthebuilder.cloud/blog/how-i-use-claude-cowork-to-write-with-ai-in-my-voice/)). He uses a rulebook, which is the opposite of the examples-only setup here, so it's weaker evidence on style. It points the same way on content.
- **Post-editing study (tier A, but relevant here).** In a pre-registered study of 81 people, participants editing LLM drafts to sound like themselves reported that the main obstacle was **lack of originality in the draft**, not the editing itself ([Baumler et al., arXiv 2604.24444, 2026; preprint](https://arxiv.org/html/2604.24444v1)).

The practitioners who got past generic output all added one of two things: **the author's ideas, supplied per piece** (an interview, a brief, clarifying questions), or **a wider mix of genres, including opinion pieces**. None reported stories alone as sufficient for new-topic argument, though none tested that directly either.

## 5. Recommended library mix

| Material | Role | Recommendation | Confidence |
|---|---|---|---|
| **Personal stories / memoir essays** | Carry the voice markers that hold across topics (rhythm, function words, syntax, humor timing) | Keep as the base. Rotate varied samples; don't pick by topic. | **High** that they carry voice; **low** that they alone carry argument structure |
| **Argumentative / opinion pieces in his voice (any topic)** | Close the register gap: show how he makes a claim, concedes, escalates and lands a point | Add 3–6. Topic doesn't matter; genre does. Include 1–2 in every op-ed prompt. | **Medium–high** (genre effects are well supported; this exact transfer is untested) |
| **Stance notes on target topics** (his positions, in his own rough words) | Supply the viewpoint; prevent the model defaulting to its own opinions | A short file per topic of bullets or transcribed voice notes. It's content, not style rules, so it fits an examples-only setup. It can live in the per-piece brief rather than the sample pool. | **Medium** (indirect support from slop, homogenization and opinion-shift studies; no direct test) |
| **On-topic essays** | Vocabulary and substance for the domain | 1–2 helps content. Don't over-select by topic, since it reduced style fidelity in one study. | **Low–medium** |
| **Short-form posts** | Voice at high compression; register match *for short-form targets* | Include only when the target is short-form. Weak signal for long op-eds, and short texts carry little stylometric signal. | **Low–medium** |
| **Signature lines / phrases** | Recognizable tics | At most a few, and embedded in real samples rather than listed. Models already overuse formulaic phrases, and a list invites parody. | **Low** (thin evidence either way) |

About volume: 5 examples per call is the tested range and more barely helps in context. A larger library is still worth having so examples can rotate across genres. If the library passes about 50k words and in-context quality stalls, fine-tuning is the evidence-backed next step.

## 6. One cheap blind test: two questions, two failure modes

1. **Hold out 2–3 real opinion pieces** he has written (if none exist, he writes one by hand on the AI and creative work topic first; it later joins the library). Remove them from the library.
2. **Summarize each into a neutral content brief.** This mirrors the benchmark setup: the brief fixes the content so the test isolates voice.
3. **Generate two versions per brief:** **A** from the current library (stories only); **B** from the library plus 3 argumentative pieces and a stance note (none of them the held-out piece).
4. **Blind the trio** (real, A, B): same formatting, random order. Give it to 3 people who know his writing, or to him after at least a week.
5. **Ask two separate questions:**
   - *Q1: Which one did he write?* This tests the style/register gap.
   - *Q2: Does any version claim something he wouldn't say, or make a generic point he'd never bother making?* This tests the viewpoint gap.
6. **Read the result.** If readers pick the real piece far above chance (1 in 3) and pick A as the fake more often than B, the library is not "enough" and the added material helps. If Q2 flags A but not B, the missing ingredient is stance, not style. With about 3 briefs × 3 readers = 9 judgments per question this is a smoke test, not statistics. A clear pattern is still informative.

## Evidence gaps

- No study tests cross-genre few-shot imitation for one author. The central question rests on inference from stylometry and same-genre LLM work.
- No study tests whether adding stated opinions to few-shot samples improves perceived voice.
- Most LLM-imitation papers are 2025–2026 preprints. Only Wang et al., LaMP, ExPerT, Padmakumar & He, Jakesch et al., Ishihara and the stylometry classics are peer-reviewed.

## Sources

- Wang et al., *Catch Me If You Can? Not Yet*, EMNLP 2025 Findings (A): https://arxiv.org/abs/2509.14543 · https://aclanthology.org/2025.findings-emnlp.532.pdf
- Sawant, *PersonalBench*, arXiv 2608.19746 (A, preprint): https://arxiv.org/html/2608.19746
- Ishihara, ChatGPT style imitation and forensic text comparison, DSH 2026 (A): https://academic.oup.com/dsh/advance-article/doi/10.1093/llc/fqag079/8703383
- Jemama & Kumar, *How Well Do LLMs Imitate Human Writing Style?*, IEEE UEMCON 2025 (A): https://arxiv.org/abs/2509.24930
- Chakrabarty, Ginsburg & Dhillon, *Readers Prefer Outputs of AI Trained on Copyrighted Books…*, arXiv 2510.13939 (A, preprint): https://arxiv.org/html/2510.13939v3
- Salemi et al., *LaMP*, ACL 2024 (A): https://aclanthology.org/2024.acl-long.399/
- Salemi, Killingback & Zamani, *ExPerT*, ACL 2025 Findings (A): https://arxiv.org/abs/2501.14956
- Shaib et al., *Measuring AI "Slop" in Text*, arXiv 2509.19163 (A, preprint): https://arxiv.org/abs/2509.19163
- Padmakumar & He, *Does Writing with Language Models Reduce Content Diversity?*, ICLR 2024 (A): https://arxiv.org/pdf/2309.05196
- Jakesch et al., *Co-Writing with Opinionated Language Models Affects Users' Views*, CHI 2023 (A): https://arxiv.org/pdf/2302.00560
- Lee et al., *Poor Alignment and Steerability of LLMs: College Admission Essays*, arXiv 2503.20062 (A, preprint): https://arxiv.org/abs/2503.20062
- Loh et al., *Predicting User Stances from Target-Agnostic Information*, arXiv 2409.14395 (A, preprint): https://arxiv.org/html/2409.14395
- Baumler et al., *Can You Make It Sound Like You?*, arXiv 2604.24444 (A, preprint): https://arxiv.org/html/2604.24444v1
- Stamatatos, *A Survey of Modern Authorship Attribution Methods*, JASIST 2009 (A): https://icsdweb.aegean.gr/stamatatos/papers/survey.pdf
- Sundararajan & Woodard, *What represents "style" in authorship attribution?*, COLING 2018 (A): https://aclanthology.org/C18-1238.pdf
- Kestemont et al., *Cross-Genre Authorship Verification Using Unmasking*, English Studies 2012 (A): https://www.tandfonline.com/doi/abs/10.1080/0013838X.2012.668793
- Eder, *Does size matter?*, DSH 2015 (A): https://academic.oup.com/dsh/article-abstract/30/2/167/390738
- Anthropic, Claude prompting best practices (B): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Every, Spiral v3 launch and podcast transcript (C, vendor): https://every.to/on-every/introducing-spiral-v3-an-ai-writing-partner-with-taste · https://every.to/podcast/transcript-spiral-s-creator-on-why-better-writing-means-better-thinking
- Cole, *The Right Way To Write With AI* (D): https://artandbiz.substack.com/p/the-right-way-to-write-with-ai
- Eddie (D): https://dev.to/eddieajau/teaching-ai-to-write-like-you-3aae · Morgan (D): https://www.jeremymorgan.com/blog/generative-ai/hey-ai-write-like-me/ · Isenberg (D): https://ranthebuilder.cloud/blog/how-i-use-claude-cowork-to-write-with-ai-in-my-voice/
