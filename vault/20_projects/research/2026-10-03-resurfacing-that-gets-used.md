---
title: "Resurfacing that gets used: pull, timing, and idea work in a second brain"
date: 2026-10-03
source: claude-agent-research
status: draft
---

# Resurfacing that gets used

What makes stored knowledge get *used*, by a person and by agents, instead of piling up in unread digests? Written for a second-brain redesign whose nightly synthesis, critique and morning briefing go unread. Tiers: **A** academic (peer-reviewed, or an arXiv preprint marked as such), **B** primary (author or organization speaking for itself), **C** trade, **D** forum. *[measured]* marks a measured result. Everything else is design argument or opinion. Pre-2025 work is labeled *background*.

## What this means for the redesign

1. **Stop producing for the inbox.** No source found here measures a scheduled digest getting knowledge reused. The measured wins all come from material surfaced *inside the task it serves*.
2. **Timing matters more than relevance.** Suggestions shown at workflow boundaries got 52% engagement. Mid-task ones were dismissed 62% of the time [measured; Kuo et al. 2026].
3. **Anchor to the owner's own artifacts.** A suggestion tied to the ticket, draft or plan he is working on gets acted on. Generic "interesting" items don't [measured/qualitative; Omakase 2026, PITCH CHI 2026].
4. **Silence is a feature.** A memory agent that *chooses* when to inject beat both always-on injection and a passively available memory bank [measured; Wu et al. 2026].
5. **Agents need instructions, not overviews.** Whole-repo context files raised cost about 20% and didn't raise success. Instructions were followed, but overviews didn't help [measured; Gloaguen et al. 2026]. Retrieve notes when a ticket needs them. Don't preload them all.
6. **Make the morning queue a batch of decisions, not a reading list.** Batching interruptions helps well-being (*background*, Fitz 2019). Prose summaries swap in for the source and end engagement [measured; Pew 2025].
7. **Hook resurfacing into three moments:** writing a ticket (evening), reviewing a finished ticket (morning), and starting or closing a work session. Never use a standalone feed.
8. **Keep the owner writing.** Fully automated notes gave the *worst* learning, even though users preferred them [measured; Chen et al. CSCW 2025]. The machine proposes and he writes the one-line "why".
9. **Use his notes as the cure for AI sameness.** LLM ideas cluster together [measured; Wenger & Kenett 2026]. His own corpus is the one input other people don't have.
10. **Instrument "used," not "delivered".** Log whether a surfaced note was opened, cited in a ticket, edited or linked. Cut any surface that stays under a set threshold after two weeks.

## 0. What the Gemini report got wrong

The Gemini Deep Research report (same folder, 2026-10-03) recommends daily, weekly and quarterly scheduled synthesis, but its resurfacing table gives no engagement data for any mechanism. Its "93% measured reuse" figure comes from a GPU-cluster study of agent sessions reusing earlier context: cache continuity, not a person acting on a note. The digest advice rests on practitioner claims.

## 1. Push vs pull: when resurfaced knowledge gets consumed

**The lineage (background).** Rhodes and Maes (2000, A) defined *just-in-time information retrieval agents*: software that watches your local context and offers related material "in an easily accessible yet non-intrusive manner". The Remembrance Agent and Margin Notes showed past documents beside the one being written. The design idea has lasted: retrieval is driven by the current task, and a suggestion has to be cheap to ignore.

**The 2025–2026 measured work is about timing.**

- *Workflow boundaries win.* Kuo, Sergeyuk, Chen and Izadi ran a five-day field study with 15 professional developers in a production IDE (IUI '26, A). They logged 229 proactive interventions across 5,732 interaction points. Suggestions at boundaries, such as just after a commit, got **52% engagement**. Mid-task suggestions were **dismissed 62%** of the time. Well-timed suggestions took less than half the time to interpret (45s vs 101s, p=.0016) [measured].
- *Proactivity speeds work up but disrupts flow.* Pu et al. (Codellaborator, N=18, CHI '25, A): more efficient than prompt-only, but with disruptions and costs to control and code understanding; presence indicators reduced them [measured].
- *State-timed help beats random timing.* Liu et al. (N=32, preprint Jan 2026, A): support aligned to the person's state raised accuracy 21% and cut missed-help errors from 50.9% to 22.9% [measured].
- *Scheduled check-ins decay.* PITCH (CHI '26, A) sent 12 students two proactive check-ins a day for two weeks (336 conversations). About **32% of conversations ended without a reply**, and 9 of 12 participants dropped conversations mid-thread. Evening reflections anchored to the person's *own* morning plan drew more engagement than generic prompts [measured]. This is the closest analogue to a morning briefing, and it shows the digest problem in miniature.
- *Long reports don't get acted on; anchored suggestions do.* Omakase (Siangliulue et al., preprint Apr 2026, A) began from the finding that deep-research reports were "overwhelming" and hard to turn into action. In an 8-week probe (N=28), median click-through was 9%; low-engagement users found items "interesting" but "not super relevant", and only half kept the required interests document current. The redesign read documents researchers already keep, tied each suggestion to the project's stage and the exact passage, and **discarded open loops with no follow-up for several weeks**. N=42 rated it significantly more actionable than the reports [measured, self-report].
- *Summaries end engagement with the source.* Pew (Jul 2025, B) tracked the browsing of 900 adults. With an AI summary on the page, 8% clicked a link, against 15% without one. Sessions ended on 26% of summary pages vs 16% [measured]. A summary satisfies the reader, and the underlying note never gets opened.

**For agents, the same pattern holds.** Wu et al. (preprint Jul 2026, A): a memory agent that decides whether to inject a reminder or stay silent raised pass@1 by +8.3 (Terminal-Bench 2.0) and +6.8 (τ²-Bench), and *selective* injection beat always-on injection and a passive memory bank [measured]. Liu et al. (preprint, rev. Sep 2026, A): a small temporal-graph trigger anchored on entities that recur in the user's activity chose *when* to act better than LLM triggers (+16.7 F1 across 14 backbones, 4–7× faster) [measured]. Gloaguen et al. (ETH, rev. Sep 2026, A): repository context files did not raise coding-agent success and added over 20% cost; instructions were followed, overviews didn't help [measured]. Khatri (preprint Jul 2026, A, single author; 288 runs, Claude Code and Codex): none vs always-on vs on-demand wiki retrieval moved correctness by no more than 10–15 points; failures were implementation skill, not missing knowledge [measured]. Lulla et al. (Jan 2026, A): curated files cut runtime 28.6% and output tokens 16.6% at similar correctness [measured]. So: instructions up front, facts on demand.

**Opinion, not evidence:** the CHIIR 2026 workshop report (A, Aug 2026) wants proactivity "appropriately timed, transparent, contestable"; Bui and Evangelopoulos (position, May 2026, A) propose judging agents on an "insight policy". A trade post (Tian Pan, May 2026, C) claims a 3–5 notifications/day ceiling without a study; treat it as a rule of thumb.

## 2. The classic PKM methods in 2026

| Method | What it claims makes notes get reused | Evidence |
|---|---|---|
| **Ahrens, *How to Take Smart Notes*** (2017; 2nd ed. 2022, B, *background*) | Own-words notes, linked to existing ones *at writing time*, so writing becomes assembly from the slip-box. | No controlled study; rests on learning research (elaboration, generation effect) and Luhmann's output. His 2025 Obsidian course (B) changes tooling, not the claim. |
| **Forte, *Building a Second Brain*** (2022, B, *background*); "Introducing the AI Second Brain" (Mar 2026, B) | Organize by *actionability* (PARA) so notes return when a project is active; reuse "intermediate packets". In 2026: "personal context management", giving agents the right context at the right time. | Anecdote and testimony; the 2026 essay cites no studies. Its *project-anchoring* idea is the one §1's evidence backs. |
| **Matuschak, evergreen notes** (working notes, ongoing, B, *background*) | Most people take only transient notes; notes compound when atomic, concept-oriented, densely linked, and written to think. | Personal practice. His measured work, the *mnemonic medium* (Quantum Country, 2019–20, B, *background*), embedded review prompts in the text: detailed recall for weeks at 35–50% extra reading time [measured]. Resurfacing built into the material, not a separate feed. |

**2025–2026 academic signal.** Ferreira et al. (INTERACT 2025, A; Obsidian users in an industry lab): a person's *retrieval strategy* shaped how they built and maintained notes [qualitative]; people maintain what they pull from. Chen et al. (CSCW 2025, A, N=30): *intermediate* AI help in note-taking gave the best post-test scores, *automated* notes the worst, yet participants **preferred** automation [measured]. That supports Ahrens' and Matuschak's core claim: the writing is the thinking.

**Read-across:** none of the three relies on digests. Each puts reuse at *writing* (Ahrens), *project work* (Forte) or *thinking* (Matuschak). Automate the filing and finding, not the writing.

## 3. Idea generation: connections, serendipity, and the offloading critique

**Where AI connection-finding has measured benefit.** These are lab studies with researchers working on *their own* ideas:

- **Scideator** (Radensky et al., v6 Mar 2026, A, N=22) recombines facets (purpose, mechanism, evaluation) drawn from papers. Creativity Support Index: median 70.5 vs 61.0 for the baseline (p<.01). The biggest gains were in exploration. Users favored near facets over far ones, so "far" serendipity was the least used [measured].
- **IdeaSynth** (Pu et al., CHI '25, A) put idea facets as nodes on a canvas, with feedback grounded in literature. Participants explored more directions and fixated less [measured, mostly self-report].
- **Asta** logs (Haddad et al., Feb 2026, A; 200k+ queries): users revisit AI research outputs as work artifacts and check citations more with experience [measured].

None of these measures whether ideas were *acted on* weeks later. That outcome is still unmeasured.

**The costs.**

- *Sameness.* Wenger and Kenett (PNAS Nexus, Mar 2026, A) tested 22 LLMs against 102 humans. The models matched individual originality but showed much less variety across the population. Raising temperature or changing the prompt helped little [measured]. Azad and Baten (preprint May 2026, A) found three frontier models produce more redundant ideas than unaided humans, though targeted design reduced the crowding [measured]. *Background:* Doshi and Hauser (Science Advances 2024, A) found AI raised individual story quality but cut collective diversity.
- *Shallower knowledge.* Melumad and Yun (PNAS Nexus, Oct 2025, A; 7 experiments, n=10,462) found that learning from LLM syntheses produced shallower knowledge, less invested advice and lower adoption than web search, even with the same facts [measured].
- *Offloading.* Lee et al. (CHI '25, A; 319 knowledge workers): more confidence in AI went with *less* critical thinking [measured, self-report]. Gerlich (Societies, Jan 2025, A; N>600): AI use correlated negatively with critical thinking via offloading [correlational]. Yu et al. (preregistered, N=1,237, May 2026, A): people *expected* AI to be faster and *felt* less effort, but completion times were the same [measured].
- *Contested.* Kosmyna et al. ("Your Brain on ChatGPT", Jun 2025 preprint, A) reported weaker EEG connectivity and recall; Stankovic et al. (Dec 2025, A) challenged its sample size, EEG analysis and reporting. Suggestive at most.

**Read-across:** AI connection-finding helps when it widens the owner's own exploration and he still does the synthesis. It hurts when it hands him finished conclusions. The synthesizer and critic produce finished conclusions. Their output is unread, so the cost so far is waste, not deskilling. But "read the synthesis" is the wrong fix.

## 4. Design implications: where resurfacing should hook in

**(a) Evening: when a ticket is written.** The highest-leverage moment. Attach the 1–3 most related notes *to the ticket*, each with one line on why it matched. The overnight agent gets task-scoped context instead of the whole index (§1), and the owner sees the link at a boundary moment, while deciding what the ticket is. Flag any note that *contradicts* the ticket's premise; that is the most decision-useful link there is.

**(b) Morning: the review queue.** Every finished-ticket card shows the notes the agent used or touched, plus any note the result now contradicts or updates. A card offers at most one "connection worth a thought", phrased as a question tied to the card. It never offers a summary (Omakase, Pew, Chen). Synthesizer output enters the queue only as **proposed edits to notes linked to an active project**, or as **candidate tickets**. Each is one click to accept, reject or defer. Prose syntheses with no attached decision stop being produced. Deferred items expire after about three weeks with no follow-up (Omakase's open-loop rule).

**(c) Live sessions with Claude Code or Codex.** Resurface at the start and end of a session, not mid-task (Kuo: 52% vs 62% dismissed). At session start: a short "notes related to what you're about to do", keyed on the branch, ticket or first prompt. At wrap-up or commit: "this session touched X; update note Y?". That is also the cheapest capture point. The repo already injects the whole concept index at session start; the agent evidence (§1) says to ablate that against on-demand retrieval before assuming it helps.

**(d) Keep him writing.** When the system finds a link, he writes the one-sentence why, and the machine writes the rest (filing, linking, metadata). That is the "intermediate assistance" level that tested best (Chen et al.). For idea work, ask the multi-vendor council to *widen* the space from his notes (far facets, contradictions). Never ask it for a finished essay.

**(e) Measure use.** Log every surfaced item with its outcome: opened, cited in a ticket, note edited, link accepted, or ignored. Hand-label two weeks of it. Any surface below an agreed threshold is cut. Engagement falls off quietly (PITCH: about a third of check-ins got no reply).

## Gaps

- No 2025–2026 study measures the open or read rate of a personal AI-generated daily digest. The case against digests is indirect: check-in decay, summary substitution, and the success of timed, anchored alternatives.
- No study tracks AI-surfaced connections through to ideas a person *shipped*. The creativity results are lab self-reports.
- Most 2026 items are arXiv preprints. Kuo (IUI '26), PITCH (CHI '26), the CHI/CSCW 2025 papers and the PNAS Nexus papers are peer-reviewed.

## Sources

**Academic (A)**
- Kuo, Sergeyuk, Chen, Izadi. "Developer Interaction Patterns with Proactive AI: A Five-Day Field Study." IUI '26; arXiv:2601.10253 (Jan 2026). https://arxiv.org/abs/2601.10253
- Pu, Lazaro, Arawjo, Xia, Xiao, Grossman, Chen. "Assistance or Disruption? … Proactive AI Programming Support." CHI '25 (Apr 2025). https://arxiv.org/abs/2502.18658
- Liu, Karoui, Draxler, Kreuter, Chiossi. "Sensing What Surveys Miss." arXiv:2602.00880 (Jan 2026, preprint). https://arxiv.org/abs/2602.00880
- "'Having Lunch Now': … a Proactive Agent for Daily Planning and Self-Reflection." CHI '26; arXiv:2509.24073. https://arxiv.org/abs/2509.24073
- Siangliulue, Bragg, Downey, Chang, Weld. "Omakase: proactive assistance with actionable suggestions…" arXiv:2604.08898 (Apr 2026, preprint). https://arxiv.org/abs/2604.08898
- Wu et al. "Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents." arXiv:2607.08716 (Jul 2026, preprint). https://arxiv.org/abs/2607.08716
- Liu et al. "Do Proactive Agents Need an LLM to Decide When to Act?" arXiv:2605.30152 (May 2026, rev. Sep 2026, preprint). https://arxiv.org/abs/2605.30152
- Gloaguen, Mündler-Sasahara, Müller, Raychev, Vechev. "Evaluating AGENTS.md." arXiv:2602.11988 (Feb 2026, rev. Sep 2026). https://arxiv.org/abs/2602.11988
- Khatri. "Do Context Files Help Coding Agents? A Two-Agent Ablation Study." arXiv:2607.27250 (Jul 2026, preprint). https://arxiv.org/abs/2607.27250
- Lulla et al. "On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents." arXiv:2601.20404 (Jan 2026). https://arxiv.org/abs/2601.20404
- Bui, Evangelopoulos. "Agentic Coding Needs Proactivity, Not Just Autonomy." arXiv:2605.06717 (May 2026, position). https://arxiv.org/abs/2605.06717
- "Report on the 1st Workshop on Human-Centered Proactive and Personalized Agents… CHIIR 2026." arXiv:2608.18638 (Aug 2026). https://arxiv.org/abs/2608.18638
- Haddad et al. "Understanding Usage and Engagement in AI-Powered Scientific Research Tools: The Asta Interaction Dataset." arXiv:2602.23335 (Feb 2026). https://arxiv.org/abs/2602.23335
- Chen, Ruan, Ju, Yap, Wang. "More AI Assistance Reduces Cognitive Engagement… AI-Supported Note-Taking." CSCW 2025; arXiv:2509.03392. https://arxiv.org/abs/2509.03392
- Ferreira, Segura, Souza, Brasil. "How People Manage Knowledge in their 'Second Brains'…" INTERACT 2025; arXiv:2509.20187. https://arxiv.org/abs/2509.20187
- Radensky, Shahid, Fok, Siangliulue, Hope, Weld. "Scideator." arXiv:2409.14634 v6 (Mar 2026). https://arxiv.org/abs/2409.14634
- Pu et al. "IdeaSynth." CHI '25 (Apr 2025). https://dl.acm.org/doi/10.1145/3706598.3714057
- Wenger, Kenett. "Large language models are homogeneously creative." PNAS Nexus 5(3) (Mar 2026). https://academic.oup.com/pnasnexus/article/5/3/pgag042/8529001
- Azad, Baten. "Ex Ante Evaluation of AI-Induced Idea Diversity Collapse." arXiv:2605.06540 (May 2026, preprint). https://arxiv.org/abs/2605.06540
- Melumad, Yun. "Experimental evidence of the effects of LLMs versus web search on depth of learning." PNAS Nexus 4(10) (Oct 2025). https://academic.oup.com/pnasnexus/article/4/10/pgaf316/8303888
- Lee, Sarkar, Tankelevitch, Drosos, Rintel, Banks, Wilson. "The Impact of Generative AI on Critical Thinking." CHI '25 (Apr 2025). https://www.microsoft.com/en-us/research/wp-content/uploads/2025/01/lee_2025_ai_critical_thinking_survey.pdf
- Gerlich. "AI Tools in Society: Impacts on Cognitive Offloading…" Societies 15(1):6 (Jan 2025). https://www.mdpi.com/2075-4698/15/1/6
- Yu, Cheng, Jabbar, Sucholutsky, Collins, Jurafsky, Hawkins. "Cognitive offloading and the speedup illusion in human-AI interaction." arXiv:2605.23177 (May 2026, preregistered preprint). https://arxiv.org/abs/2605.23177
- Kosmyna et al. "Your Brain on ChatGPT." MIT Media Lab preprint (Jun 2025). https://www.media.mit.edu/publications/your-brain-on-chatgpt/
- Stankovic, Hirche, Kollatzsch, Doetsch. "Comment on: Your Brain on ChatGPT." arXiv:2601.00856 (Dec 2025). https://arxiv.org/abs/2601.00856
- Tankelevitch et al. "Understanding, Protecting, and Augmenting Human Cognition with Generative AI: CHI 2025 Tools for Thought Workshop." arXiv:2508.21036 (Aug 2025). https://arxiv.org/abs/2508.21036
- *Background:* Rhodes, Maes. "Just-in-time information retrieval agents." IBM Systems Journal 39(3–4) (2000). https://doi.org/10.1147/sj.393.0685
- *Background:* Fitz, Kushlev et al. "Batching smartphone notifications can improve well-being." Computers in Human Behavior (2019). https://doi.org/10.1016/j.chb.2019.07.016
- *Background:* Doshi, Hauser. "Generative AI enhances individual creativity but reduces the collective diversity of novel content." Science Advances (Jul 2024).

**Primary (B)**
- Pew Research Center. "Google users are less likely to click on links when an AI summary appears in the results" (Jul 22, 2025). https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/
- Forte. "Introducing The AI Second Brain." Forte Labs (Mar 2026, upd. Apr 2026). https://fortelabs.com/blog/introducing-the-ai-second-brain/
- *Background:* Forte. *Building a Second Brain* (2022).
- *Background:* Ahrens. *How to Take Smart Notes* (2017; 2nd ed. 2022). Obsidian course, 2025: https://www.soenkeahrens.de/en/home
- *Background:* Matuschak. "Evergreen notes" (working notes, ongoing). https://notes.andymatuschak.org/z5E5QawiXCMbtNtupvxeoEX
- *Background:* Matuschak, Nielsen. "Effects of the mnemonic medium on reader memory" / Quantum Country (2019–2020). https://notes.andymatuschak.org/zt1TyUANyt84UkQVBJjWEGZ3JUd2HP92r65

**Trade (C)**
- Tian Pan. "Background Agents and the Notification Budget" (May 2026). Opinion; its 3–5/day figure is not sourced to a study. https://tianpan.co/blog/2026-05-13-background-agents-notification-budget-attention-economy

**Internal**
- Gemini Deep Research report, `vault/20_projects/research/2026-10-03-as-of-october-2026-what-does-current-evidence-show-about-des.md` (2026-10-03).
