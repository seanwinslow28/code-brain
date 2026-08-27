---
title: YouTube watch-list — AI PM System Design Thinking
type: reference
created: 2026-08-27
status: curated
note: Deliberately NOT in the NotebookLM notebook. Sean curates this as a YouTube playlist.
---

# YouTube watch-list

Built 2026-08-27 with `yt-dlp` searches across all five modules. Every entry below was returned by a real search — title, channel, duration and view count are as reported by YouTube at build time, not from memory.

**Coverage is uneven, and the unevenness is itself informative.** M3 (architecture) and M5 (evals) are richly covered by credible sources. M1 (error economics) is covered only in its statistics half. M2 (labeling) is dominated by annotation vendors marketing their services. M4 (interaction and trust) is the thinnest — which matches the council's finding that the human half of AI product work is under-served everywhere.

---

## M1 — Problem, Users & Decision Economics

The statistics are well covered. The *product* framing barely exists on YouTube.

| Watch | Length | Channel · views |
|---|---|---|
| [Precision vs Recall with a Clear Example](https://www.youtube.com/watch?v=qWfzIYCvBqo) — **start here**, the clearest short explanation of the trade-off | 5:24 | Kimberly Fessel · 177k |
| [Confusion Matrix Solved Example: Accuracy, Precision, Recall, F1](https://www.youtube.com/watch?v=_CGTbkHwUHQ) | 5:50 | Mahesh Huddar · 727k |
| [How To Find Optimal Threshold For Binary Classification](https://www.youtube.com/watch?v=_AjhdXuXEDE) — **the most M1-relevant of the four**; threshold choice is where the product decision physically lives | 15:10 | Krish Naik · 83k |
| [How to evaluate ML models — evaluation metrics](https://www.youtube.com/watch?v=LbX4X71-TFI) | 10:05 | AssemblyAI · 127k |
| [When Not to Use Machine Learning](https://www.youtube.com/watch?v=giRJLdwVmAE) — tiny channel, but it is the only hit on M1's actual opening move | 4:22 | StrataScratch · 665 |

**Gap worth naming:** nothing on YouTube covers "what does a false positive cost versus a false negative, and who pays." That's the module's core and it exists in writing, not video.

---

## M2 — Data, Feedback & the Model Path

**Read the vendor warning.** Six of the eight labeling results were annotation companies selling annotation services. Their explainers are competent and structurally can't tell you when *not* to buy labels.

| Watch | Length | Channel · views |
|---|---|---|
| [Is RAG Still Needed? Choosing the Best Approach for LLMs](https://www.youtube.com/watch?v=UabBYexBD4k) — **best of the module**; the retrieval-vs-alternatives fork, credibly done | 11:10 | IBM Technology · 956k |
| [Why RAG Fails in Production — And How To Actually Fix It](https://www.youtube.com/watch?v=j0d68suEaS4) | 20:01 | CodeRash · 2.4k |
| [Why most RAG systems fail at Retrieval (not Generation)](https://www.youtube.com/watch?v=TOFnW5UdiEg) | 4:39 | Beyond Tokens · 145 |
| [AI data annotation explained in under 2 minutes](https://www.youtube.com/watch?v=YJnnxitraac) — vendor, but a clean 2-minute orientation | 1:49 | Moveworks · 161k |

**Gap worth naming:** nothing credible on inter-rater agreement, labeling instruction design, or selection effects — the three things M2 actually teaches. The Zillow mechanism has no good video treatment at all.

---

## M3 — Architecture Under Constraints

**The strongest module by far.** Watch these even if you skip the rest.

| Watch | Length | Channel · views |
|---|---|---|
| [How We Build Effective Agents — Barry Zhang, Anthropic](https://www.youtube.com/watch?v=D7_ipDqhtwk) — **the canonical talk**, and the source behind M3's §1 | 15:09 | AI Engineer · 524k |
| [Agentic AI: Workflows vs. agents](https://www.youtube.com/watch?v=Qd6anWv0mv0) — the whole fork in five minutes | 5:30 | Google Cloud Tech · 129k |
| [Tips for building AI agents](https://www.youtube.com/watch?v=LP5OCa20Zpg) | 18:20 | Anthropic · 580k |
| [Building more effective AI agents](https://www.youtube.com/watch?v=uhJJgc-0iTQ) | 18:58 | Anthropic · 94k |
| [AI agent design patterns](https://www.youtube.com/watch?v=GDm_uH6VxPY) | 8:21 | Google Cloud Tech · 440k |
| [Building Effective Agents with LangGraph](https://www.youtube.com/watch?v=aHCDrAbH_go) — the five patterns, implemented | 31:50 | LangChain · 247k |
| [Guide to Architect Secure AI Agents](https://www.youtube.com/watch?v=UMYtqHptYvA) — **pairs with M3 §6**, the threat-modelling section | 13:45 | IBM Technology · 78k |
| [Agentic AI Frameworks Explained: Workflows, Multi-Agent, Production](https://www.youtube.com/watch?v=ZVPlLaehjLk) | 11:54 | IBM Technology · 52k |
| [What is Tool Calling? Connecting LLMs to Your Data](https://www.youtube.com/watch?v=h8gMhXYAv1k) | 4:57 | IBM Technology · 50k |

*Note: [You Can Learn AI Agent System Design In 19 Min](https://www.youtube.com/watch?v=CyLYY_xb5bQ) (135k) is already a source in your notebook — same channel also has a [harness/loop-engineering version](https://www.youtube.com/watch?v=GrNbuWWJYiI) at 185k.*

---

## M4 — Interaction, Trust & Control

**The thinnest module, and the Google Design material is the only substantial thing here.** Most results were talks with double-digit view counts. This scarcity is consistent with why the retired curriculum skipped the human half entirely — it is genuinely harder to find.

| Watch | Length | Channel · views |
|---|---|---|
| [Designing Human-Centered AI Products (Google I/O '19)](https://www.youtube.com/watch?v=rf83vRxLWFQ) — **the one to watch**; it is the PAIR Guidebook presented by its authors, and PAIR is M1's and M2's source too | 38:20 | Google Design · 38k |
| [Stanford Seminar — Designing Human-Centered AI Systems for Human-AI Collaboration](https://www.youtube.com/watch?v=JcI7V6Rs7cA) | 58:36 | Stanford Online · 6.8k |
| [Creating people-centered AI experiences: Google's People + AI Guidebook](https://www.youtube.com/watch?v=0ZJBwP4n-bE) | 55:24 | awwwards · 4.3k |
| [Getting Started with the People + AI Guidebook](https://www.youtube.com/watch?v=n3HsvqBJrlY) — 4-minute orientation | 4:25 | Google Design · 2.4k |
| [The UX of AI: Designing Interfaces Around Uncertainty and Confidence](https://www.youtube.com/watch?v=DZcg4d6g33M) — 57 views, and the single most on-topic title found | 23:54 | DDD Melbourne · 57 |

---

## M5 — Evidence & Operations

Second-strongest, and it has the best single video on this entire list.

| Watch | Length | Channel · views |
|---|---|---|
| [Why AI evals are the hottest new skill for product builders — Hamel Husain & Shreya Shankar](https://www.youtube.com/watch?v=BsWxPI9UM4c) — **watch this one first, before anything else on this page.** Explicitly framed for product people, by M5's anchor author | 1:46:33 | Lenny's Podcast · 138k |
| [Complete Beginner's Course on AI Evaluations in 50 Minutes — Aman Khan](https://www.youtube.com/watch?v=TL527yTpxlk) | 51:48 | Peter Yang · 48k |
| [Error Analysis: The Highest ROI Technique In AI Engineering](https://www.youtube.com/watch?v=e2i6JbU2R-s) | 12:08 | Hamel Husain · 8.8k |
| [How To Build AI Evals](https://www.youtube.com/watch?v=mF4CaijvJos) | 33:39 | Hamel Husain · 4.4k |
| [How to Automate AI Evals (Correctly)](https://www.youtube.com/watch?v=tqUDjc1HzO4) | 27:19 | Hamel Husain · 5.5k |
| [Mastering AI Evals: the missing skill in AI product management](https://www.youtube.com/watch?v=WjTysfxi5CE) — Hamel again, PM-framed | 33:25 | Product Founder · 3.2k |
| [ML Drift: Identifying Issues Before You Have a Problem](https://www.youtube.com/watch?v=uOG685WFO00) | 15:25 | Fiddler AI · 33k |
| [Evidently AI Tutorial — ML Model Monitoring and Observability](https://www.youtube.com/watch?v=cgc3dSEAel0) | 30:13 | Krish Naik · 32k |

---

## If you only watch three

1. **[Hamel Husain & Shreya Shankar on Lenny's Podcast](https://www.youtube.com/watch?v=BsWxPI9UM4c)** (1:46) — evals for product people, from the person M5 is built on.
2. **[Barry Zhang, Anthropic — How We Build Effective Agents](https://www.youtube.com/watch?v=D7_ipDqhtwk)** (15 min) — the workflow-vs-agent fork from the people who wrote the piece M3 cites.
3. **[Designing Human-Centered AI Products, Google I/O '19](https://www.youtube.com/watch?v=rf83vRxLWFQ)** (38 min) — the PAIR Guidebook from its authors, and the only substantial video on M4's material.

## Extending this

```bash
yt-dlp --flat-playlist --no-warnings \
  --print "%(duration)s|%(channel)s|%(view_count)s|%(id)s|%(title)s" \
  "ytsearch8:<your query>"
```

Two things learned building it: query phrasing matters more than expected — *"when not to use machine learning"* and *"confusion matrix business cost"* returned completely different quality than *"AI product management"*, which returned almost entirely sub-100-view channels. And view count is a rough but real filter here: below about 1,000 views in this subject area, most results are either vendor content or conference talks nobody attended.
