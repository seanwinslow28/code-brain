---
type: substack-draft
project: prj-job-hunt-2026
artifact: vault-synthesizer-evals
created: 2026-05-10
voice: sean-mode-sedaris-tuned
target_length: 1300_words
status: draft
companion_artifact: 2026-05-10-evals-error-analysis-real-logs.md
ai-context: "Substack post syndicating the eval-suite portfolio artifact. Hook is the actual error analysis finding: 9 nights of silent zero-output runs the status field reported as 'ok'. Tone per roadmap Decision 4 — comedic Sean Mode, not Nate's strategic-sober register."
---

# The Night My Vault Said Nothing

There is a moment, somewhere around the eighth night that an automated system has been quietly producing nothing while reporting that everything is fine, when you start to wonder which of you is the real problem.

I had been reading about AI evals all week. Five thousand words from Hamel Husain. Another four from Shreya Shankar. A long, patient Anthropic engineering post titled *Demystifying Evals for AI Agents* that I'd printed and underlined like a freshman with a highlighter and something to prove. I had downloaded two deep-research reports — one from Gemini, one from Perplexity — that triangulated the canon for me into a tidy seven-section primer.

The theme of all of it, repeated until it became a kind of liturgy, was this: **evals are the new PRDs.** A product manager who can't write evals is a product manager who can't specify what their AI is supposed to do. The skill that mattered most a year ago was prompt engineering. The skill that matters most now is rubric engineering. Both research reports landed on the same first principle, attributed to Hamel: *you cannot write meaningful evals for failure modes you haven't first observed in data.*

This is the kind of advice that sounds impossible to disagree with and turns out to be devastating in practice.

---

I had a system already. A vault synthesizer — the third agent in a fleet of fourteen I'd been building since January, when I still had a job and the time horizon for "agents that quietly improve my second brain at 2:30 in the morning" felt like the most luxurious thing I owned. Every night, the synthesizer was supposed to wake up, find the files in my Obsidian vault that had changed in the last 24 hours, ask a 14-billion-parameter local language model to synthesize concept articles and connection articles and a small graph of typed reasoning edges, and then go quietly to sleep again.

It had been doing this for ninety-eight nights. According to the manifest files it dutifully wrote each morning, 70% of those nights were `partial` — meaning it ran out of its 45-minute budget — and 30% of those nights were `ok`, meaning everything went fine.

I sat down to write hallucination cases. The pre-drafted YAML from the research reports gave me thirteen of them, ready to paste in. *vs-001: Synthesizer must not invent concepts not present in source notes.* *vs-008: Synthesizer must accurately map and preserve direct contradictions between concepts.* *vs-013: Synthesizer must forcibly decay the relevance of highly-linked but obsolete architectural documents.* All of these were reasonable things to test.

But Hamel's first principle was sitting on my desk, underlined twice. *Look at the data first.* So I opened the manifest files.

---

Here is what I found, in seven JSON blobs spanning the last nine nights.

`concepts_written: 0`. `connections_written: 0`. `edges_written: 0`. `model_used: ""`. Across every single run.

The directory the synthesizer was supposed to write into — `vault/knowledge/concepts/` — was empty. The other directory — `vault/knowledge/connections/` — was also empty. The auto-generated `index.md` file that the rest of my system reads on session start said *"(none yet)"* under both headers, which I now realized had been *the* state, not *a* state, for at least a week.

Two of those seven runs had reported `status: "ok"`.

I scrolled through the stderr log. There were forty-three identical lines, repeated like a Greek chorus in poor health: *Health check failed for macbook_pro.* And under each one, like a chaperone confirming the calamity, *Pushover notify_wol_failure send failed: Missing Pushover credentials in Keychain.*

So the chain went like this. The MacBook Pro was asleep, which meant the local language model wasn't reachable. The synthesizer noticed. It tried to alert me through Pushover. Pushover required credentials, which weren't loaded. The alert silently failed. The synthesizer caught the LLM-call exception, appended a warning to a list nobody would ever read, and moved on to the next file. After 30 files of this, it wrote a manifest that said `status: "ok"`. The Daily Driver morning agent — another piece of automation I had personally written — read the manifest, saw `status: "ok"`, and the next morning told me, in cheerful preamble at the top of my brief, that vault synthesis had run cleanly.

This had been happening for nine days.

I had built three layers of automation to monitor a system. All three were lying to me in synchrony.

---

Anthropic's eval post has a section about something they call the **Swiss Cheese Model**, borrowed from safety engineering. The idea is that no single layer of evaluation catches every issue. You stack automated evals, production monitoring, A/B tests, manual transcript review, and human studies on top of one another, and trust that the holes in each layer don't line up.

What I had built was the inverse. A *correlated* Swiss cheese — three monitoring layers whose holes had quietly drifted into perfect alignment over time, each one inheriting its assumptions about reality from the layer below it. The synthesizer's status field assumed that if the loop completed, the loop succeeded. The morning briefing trusted the status field. I trusted the morning briefing.

Hamel says, somewhere in his FAQ: *delegating error analysis to an LLM prematurely results in generic, unactionable failure categories.* I had not delegated my error analysis to an LLM. I had delegated it to my own system. Which is, I am realizing, slightly worse — because the system was doing exactly what I'd told it to do, with the cheerful obedience of an intern who had not yet been informed that the office was on fire.

---

The Gemini and Perplexity research reports had, between them, drafted fifteen YAML eval cases. Eleven of those cases — the hallucination ones, the relation-tag drift ones, the temporal confusion ones — were aimed at a synthesizer that was running. They are good cases. They will be useful when the synthesizer is running again.

But the case I needed was the one that had been sitting at position fifteen in Perplexity's draft, almost as an afterthought: *"For a corpus of 5+ notes mentioning a named system, synthesizer must emit at least one concept article."* The failure mode was listed as *"silent omission — synthesizer fails to emit a concept article for a well-documented system component, leaving it invisible in the knowledge graph."*

That case wasn't an afterthought. That case was the *whole show.*

So the eval suite I'm shipping — the one that becomes a directory called `evals/vault-synthesizer/` in my Code-Brain repo by the end of the week — opens with the silent-empty-output case. Then it adds five more I wrote myself, every one of them grounded in a specific failure I just open-coded out of nine nights of real logs. Then it defers the eleven hallucination cases to a `deferred-cases.yaml` file with a one-line note: *"Re-enable when synthesizer produces ≥1 concept article in a clean run."*

The sixth case is the one I'm proudest of. It checks that when the synthesizer's `model_used` field is the empty string, the run does not get reported as `ok`. In the schema as it stands today, `model_used: ""` is ambiguous between three states: not yet set, intentionally blank, and unset because the LLM call never fired. I am collapsing those three into an enum with four explicit values, and writing the eval that catches any future drift back to ambiguity.

This is, I realize as I write it down, exactly what Hamel and Anthropic both kept telling me. **Evals aren't really about hallucinations.** Evals are about the things your system silently lies to itself about. Hallucinations are the easy case — the model said something wrong and you can see it. Silent regression is the hard case — the model said nothing, and your monitoring agreed that nothing was the right thing to say.

---

One last thing.

The pre-drafted YAML was generous. Two AI deep-research agents had spent maybe forty cents of compute writing me thirteen reasonable test cases for a system they had never observed. If I'd skipped the error analysis and shipped those thirteen cases, I would have had a working eval suite that passed every test it ran, because every test it ran would have been an assertion about an output that did not exist.

I would have committed that to GitHub. I would have pinned it on my profile. I would have written a Loom narrating it. I would have done all of this very confidently.

This is the part of the canon I hadn't really understood until tonight. The reason error analysis goes first isn't that it's the most rigorous step. The reason error analysis goes first is that without it, every step that follows is a kind of theater.

I stayed up later than I meant to and rewrote the spec. The synthesizer, somewhere in the next room, was probably still asleep.

---

*The eval suite ships this week at `github.com/seanwinslow28/code-brain/tree/main/evals/vault-synthesizer/`. The error-analysis-first methodology is the [Hamel Husain / Shreya Shankar canon](https://hamel.dev/blog/posts/evals/), refined by [Anthropic's eval engineering team](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). The Swiss cheese metaphor is theirs, not mine. The lying chaperone is mine.*
