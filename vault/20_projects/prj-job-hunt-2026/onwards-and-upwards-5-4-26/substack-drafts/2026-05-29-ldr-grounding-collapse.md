---
type: substack-draft
project: prj-job-hunt-2026
artifact: ldr-grounding-collapse
created: 2026-05-31
voice: sean-mode-sedaris-tuned
voice_mode: sedaris
target_length: 1500_words
status: draft
companion_artifact: github.com/seanwinslow28/ldr-grounding-collapse
substack_post_number: 1
ai-context: "Substack Post 1 (the announcement that gates Posts 2-3). Syndicates the LDR Grounding-Collapse post-mortem repo. Roadmap due 2026-05-29; drafted 2026-05-31 (2-day slip). Hook per Task 25 Step 6 — the moment Sean read 'PureMCPClient' and his Spidey-sense fired. Comedic Sean Mode (Sedaris-tuned), same register as 2026-05-10-the-night-my-vault-said-nothing.md — NOT Nate strategic-sober. Run writing-voice-modes pass before publish. Swap the repo URL once pushed; cadence: this is Post 1, publishes before Posts 2-3."
---

# The Day My Research Agent Invented Microsoft

There is a specific flavor of dread that arrives when something you built hands you a beautiful answer to a question you didn't realize it couldn't answer. It looks like pride for about four seconds. Then you read the third row of the table.

The third row of the table said **PureMCPClient**.

I want to be precise about what happened in my head, because it's the whole story. I did not think *that's wrong.* I thought *huh, I've never heard of PureMCPClient,* and then, a half-second later, with the unmistakable cold-water feeling of a man who has been gently lied to by his own infrastructure: *PureMCPClient does not exist.*

Let me back up.

## The setup

I run a small fleet of AI agents on a Mac Mini in my apartment. They do unglamorous things — index my notes, summarize my week, and, in this case, research. One of them is a local deep-researcher: a 14-billion-parameter open model named Qwen, wired up to a private search engine, told to go read the web and come back with a report. It runs at two in the morning. It costs me nothing, which is the entire point of running it locally instead of paying a cloud model by the token. Free research while I sleep. What could go wrong.

On May 5th I asked it a reasonable question. I wanted a survey of the tools people use to connect AI agents to other software — a little ecosystem named things like mcp-cli, mcp-bridge, mcp-proxy. I asked for a comparison table. License, how recently each was updated, how actively maintained, how well it'd run headless on a Mac. Rank them. Nine or ten tools, four columns each. The kind of thing a diligent intern produces in an afternoon and you trust because the formatting is good.

The formatting was *excellent.* It came back with an emoji-headed table, a clean 1-through-10 ranking, a section called "Critical Analysis," and a references list with ten numbered sources. It looked like a McKinsey slide that had found religion. It looked, in every visible respect, more rigorous than I had any right to expect for free.

And then, row three. PureMCPClient. Ranked above the real tools. Scored a perfect five out of five. Given a license (MIT) and a last-commit date (one month ago), the way you'd describe a coworker you'd definitely met.

## The receipts

Once you catch one, you can't stop. It's like finding a typo in a wedding invitation — suddenly the whole thing is suspect and you're reading it with a pen.

There was **MCPCatalog (Central)**, also fictional, also scored a five. There was **MCP ADK** — and this one I want to frame, because it's not a simple invention, it's a *confident blend of two unrelated true things into one false thing.* ADK is a real product: it's Google's Agent Development Kit. It is not an MCP tool. My agent listed it as an MCP tool, gave it a Microsoft Azure documentation URL, and cited that URL as a source. It took something Google makes, filed it under Microsoft, repackaged it as a third thing entirely, and provided a footnote. The footnote went to a page that does not exist.

The deepest cut was structural. The report declared that the home of this whole ecosystem — the canonical GitHub organization where the protocol lives — was `github.com/microsoft/mcp`. It isn't. It lives at `github.com/modelcontextprotocol`, no Microsoft involved. But once my agent decided Microsoft owned the neighborhood, every house on the street got the wrong address. Citation [1], over and over, pointing at the wrong front door.

It even left in its own out-loud thinking. At the very bottom, after the references, in the body of the report, was the sentence: *"Would you like me to update the original comparison table with this new information?"* The model talking to itself, and nobody — no human, no second agent — there to answer. The report had been filed unread. By me. Because I was asleep, which was the plan.

Here is the number I keep coming back to. The agent had a fifteen-minute budget. It finished in **under five.** It did not run out of time. It did not throw an error. It did not, anywhere, say *I'm not sure.* It used a third of its allotted time to produce something confidently, fluently, decoratively wrong, and reported complete success. If I hadn't happened to know that PureMCPClient was nonsense, I would have acted on it.

## The good twin

A failure isn't a story until you can prove it was the system's fault and not the question's. So the next morning I ran the **exact same prompt** through a grown-up — Gemini's Deep Research, the cloud one, the one that costs money. Two dollars and eighty cents and seven and a half minutes later, it came back with the real ecosystem. Real maintainers, named: Phil Schmid, IBM, a developer named brrock. Real repositories. No PureMCPClient. No Microsoft land-grab. ADK nowhere near the MCP section, because the cloud model knew they were different things.

But that's not the part that stuck with me. The part that stuck with me is that the good report *flagged its own soft spots.* It said, in effect: these specific version numbers I'm citing are precise enough that if I've got one wrong it'll mislead you, so verify them before you bet on them. It told me which of its own claims to distrust. It modeled its own uncertainty.

The free one had no uncertainty at all. It was exactly as confident about the tools it invented as about the tools that exist. That, right there, is the difference between an answer you can use and an answer that's just shaped like one — and it has nothing to do with whether the words sound smart.

## What I actually did about it

The tempting fix is "use the better model for everything." That's also the dumb fix, because it throws away the whole reason I run things locally, and because most of my research is simple enough that the free agent grounds it perfectly well. The failure wasn't *the model is bad.* The failure was *I gave one small model a question shaped like a spreadsheet — evaluate nine things across four dimensions and cite every cell — and citation-grounding is the first thing that snaps when you stretch a model that wide.* The table had ten slots. The model filled ten slots. Whether ten real tools existed was, to the model, somebody else's problem.

So the fix is a rule, and the rule is about *shape, not quality.* If a research question is compound — three or more sub-questions, a rank-these-N-things matrix, a due-diligence grid — it goes to the cloud model that can ground it. If it's single-shape — one thing, one question — it stays local and free. I wrote that boundary into the config file my whole fleet reads, so the system can't quietly default back to "try the free one first" on exactly the kind of question the free one can't handle. That default *was* the bug. Not the model. The missing rule.

And then I did the thing that turns a lesson into infrastructure: I wrote a test. A little regression check that reads a research report and fails it if it names the tools I now know are fictional, or cites the URLs I now know are fake. It fails on the bad report. It passes on the good one. So "I fixed it" is a thing I can run, not a thing I have to remember.

I kept the bad report, too. Preserved it, annotated every lie, and put the whole thing in a public repo — the failure, the diagnosis, the fix, the test. Because the most senior thing I know how to say in an interview isn't *look what I built.* It's *here's how my own system fooled me, here's exactly how I caught it, and here's the boundary I put up so it can't happen the same way twice.*

PureMCPClient doesn't exist. But the discipline it cost me to figure that out — that part's real, and it's the part I'd bring to your team.

---

*The full post-mortem — the preserved bad output with every fabrication annotated, the side-by-side, the routing rule, and the eval — is at [github.com/seanwinslow28/ldr-grounding-collapse](https://github.com/seanwinslow28/ldr-grounding-collapse).*
