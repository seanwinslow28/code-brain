---
title: "Review-queue UI: how agent products show overnight work, review UX research, build options, public showcase"
date: 2026-10-03
source: claude-agent-research
status: draft
---

# Review-queue UI

UI research for the redesigned second brain and overnight fleet: one private repo on an always-on home machine, a laptop on a synced copy, and a morning queue with four lanes (Verified, Unverified-done, Blocked, Needs-decision) where every send, spend, delete or publish is a draft. Tiers: **A** academic, **B** primary (vendor docs, first-party), **C** trade press or vendor blog, **D** forum, social or hobby repo. Measured findings are tagged *[measured]*. Pre-2025 sources are labelled *background*.

## What this means for the redesign

1. **Recommended build: a small local web app on the home machine, reachable only over the private network (Tailscale Serve), that reads the brain repo's markdown directly and writes decisions back as markdown.** It is the only option that works on a phone while travelling, reads the live repo, and can trigger agent runs from a server process you control.
2. Run the public showcase from the same front end in **replay mode**: a static build fed a sanitized fixture bundle exported from real runs. That gives you one codebase with two data sources, and nothing private leaves the machine at runtime.
3. Keep Obsidian Bases as a free, read-mostly second view of the same files. Don't build an Obsidian plugin as the main surface, because plugins can't spawn processes on mobile.
4. Make it a queue, not a dashboard. Every 2026 product surveyed sends background results to an **inbox of runs that need you**. Runs with nothing to report stay out of sight (Codex), and an unread marker is what pulls you back in.
5. "Finished" is not "succeeded." Anthropic's own routines doc warns that a green run status only means no infrastructure error. That justifies the Unverified-done lane, and the UI should never colour it like Verified.
6. **Put evidence before the narrative.** Each card leads with machine-checked evidence (check output, a diff excerpt, a screenshot), then links the full transcript. The agent's summary comes last. A citation badge alone raises trust even when the citation is random [measured].
7. Spend attention by lane. Verified gets one batch-accept with a random spot-check sample. Needs-decision gets full cards with options and a recommendation. People approve 93% of permission prompts [measured], so per-item clicking on routine work is wasted vigilance.
8. **Design for keyboard and thumb.** Use single keys (approve, return with a note, defer, open evidence) and the matching swipes on a phone, with instant response. The lanes act as Superhuman-style "split inboxes."
9. Send one morning push: counts per lane plus the single biggest anomaly. An empty "nothing needs you" state counts as a success.
10. Track your own review behaviour as an anomaly signal: approval rate, seconds per card, and how often you send work back. If approvals run above ~90% and keep getting faster, the gates are too broad (opinion, vendor blog).

## 1. How 2026 agent products present background results

| Product | Where results land | Review actions | Notable detail |
|---|---|---|---|
| **Claude Code routines** (research preview; web launch Apr 2026) | Each run becomes a session in the session list. The routine page shows run history | Open the run, read the transcript, review changes, **create PR**, continue the conversation. A push to the phone fires when actions are required | "A green status… does not mean the task in your prompt succeeded." You can ask `/schedule why did my nightly review do nothing` and get a diagnosis of a run [B] |
| **OpenAI Codex app automations** | The **Scheduled view acts as an inbox**. Runs *with findings* appear with an unread indicator | Archive, pin (keeps the worktree), open the review pane with inline diff comments, "@codex fix it" | Runs are triaged like email. Housekeeping matters because "frequent schedules can create many worktrees" [B]. The app also has a task sidebar and an artifact viewer for non-code output (PDF, sheets) [C] |
| **GitHub Copilot coding agent / Agent HQ** | A pull request, plus a Mission Control page across repos | Approve or request changes on the PR. Every commit carries an `Agent-Logs-Url` trailer linking to the session log | Practitioner advice: read the session log before the diff [C]. Copilot reviews its own patch before tagging a human [B] |
| **Linear coding sessions** | A diff attached to the issue, then a Reviews tab | Inspect the diff, view **screenshots or recordings alongside the changes**, hand review comments back to the agent, merge from Linear | The human stays the issue owner and the agent is a "delegate" [B] |
| **Devin** | A session with a PR tab | Smart diffs, a file tree, a "lines left to review" counter, open in editor | A self-review pass runs before any human sees the work [B] |
| **Google Jules** | A plan, then a diff | **Approve the plan before code**, comment on the diff, ask for a revision | A "Planning Critic" checks plans that skip human approval. The vendor claims a 9.5% drop in failures [B, vendor claim] |
| **OpenAI Dots** (launched 2026-09-29) | Messaging (Slack, Teams). Always-on, cloud computer | Custom rules to **allow, require approval for, or block** actions. An automatic review checks tasks against your rules | Launch coverage doesn't describe the review UI itself. Password changes stay with the user [C] |

**Patterns worth copying:**

- **Inbox, not feed.** Codex surfaces only runs with findings and marks them unread. That is the "anomaly-driven, not metrics wall" stance the owner already wants, and a shipping product uses it.
- **Run status ≠ task status.** Anthropic separates infrastructure success from task success in its own docs. The four lanes encode exactly that split.
- **The transcript is evidence, one click away.** GitHub's permanent log link on every commit and Simon Willison's transcript-to-HTML tool both treat the run log as a citable object. Each card should carry one.
- **Send back with a note.** Every product has a cheap "fix this" loop: "@codex fix it", Jules diff comments, Linear handing comments back to the agent. In the queue that should be one key that re-files the ticket with your note attached.
- **Approve plans, not just results.** Jules and Linear let you approve the plan before any work runs. A fifth, evening "plans awaiting approval" view would catch bad tickets before they burn a night.
- **Visual evidence for non-code work.** Most of a PM brain's outputs are notes and drafts, not diffs; Linear's screenshots and Codex's artifact viewer show the way.

## 2. Human-in-the-loop review UX: what research says

**Approval fatigue is real and measured.** Claude Code users approved 93% of permission prompts. Anthropic's response was to automate the routine gate with a classifier, which misses 17% of real overeager actions and wrongly flags 0.4% of benign ones [measured, B, 2026-03-25]. Nielsen (2026-10-02) splits the failure in two: "watch duty" over sparse streams collapses within about 30 minutes, and "verdict duty" slides into reflex; route only low-confidence items to humans [C]. A vendor blog's rule of thumb: approval rates above 90% mean the triggers are too broad, and reviewers end up "batching approvals just to stay above water" [C, opinion].

**Implication:** batching is good when it groups *like* items so you can judge them as a set (Verified lane). It is harmful when it is a coping move to clear volume. Keep the Needs-decision lane small on purpose.

**Developers lean on checks as proof.** Interviewing 17 experienced developers, Dhanorkar, Passi and Vorvoreanu found four kinds of oversight (a priori control, co-planning, real-time monitoring, post-hoc review); reviewing agent output was hard, and developers used "test results as guarantees" [A, 2026-06]. So Verified must mean an *independent* check passed, and the card names which check.

**Oversight skill decays with use.** Mitchell, Ghosh and Passi argue overseers' judgement atrophies unless the interface supports it [A, position paper, 2026-08/09]. Design answer: show a random Verified item as a full card now and then (an audit sample) and record whether the owner agreed.

**Citations persuade before they inform.** In a 303-person experiment, answers with citations earned more trust, *even with random citations*. One citation worked as well as five. But each citation the reader actually checked lowered trust, and random citations that were checked lost their advantage [measured, A, AAAI 2025]. Attribution Gradients (rev. 2026-04) shows supporting and contradicting excerpts in place, and readers engaged more deeply with sources [A]. **Implication:** no "3 sources" badge; put the excerpt or check output on the card, contradicting evidence in its own colour. A 2026 *AI and Ethics* paper warns polished rationales can become the new target of automation bias [A, abstract only], another reason the agent's narrative goes last.

**Confidence display helps only when calibrated.** Older work finds that per-item confidence can support trust calibration, and that *miscalibrated* confidence lowers decision quality [A, background 2020/2024]. **Implication:** until a verifier's scores are checked against the owner's own labels, display the *evidence class* ("deterministic check passed", "cross-vendor judge passed", "unchecked") rather than a percentage.

**Speed and splits keep people in the queue.** Superhuman's design rule is that every action finishes under 100 ms, keyboard first. Its Split Inbox groups similar items so they are processed in batches [B, vendor, background]. Lanes map directly onto splits.

**What makes people open it daily** has thin 2026 evidence. Products converge on push: Claude Code's phone push "when actions required" (Apr 2026) [B/C] and Codex's unread indicator [B]. Opinion: one daily notification, lane counts, the anomaly in the subject line, minutes not an hour, an empty state that feels like a win.

## 3. Build options for a solo owner

| | (a) Local web app over Tailscale | (b) Obsidian plugin | (c) Obsidian-native (Bases/Dataview) | (d) Hosted page |
|---|---|---|---|---|
| Effort | Medium. One small server and one page set. A PM can direct an agent to build it | Medium-high. Plugin API, desktop packaging | **Low.** Frontmatter and `.base` files | Low-medium |
| Works on phone while travelling | **Yes.** `https://<machine>.<tailnet>.ts.net`, auto-TLS, no open ports [B] | **No** for running agents. Node and Electron APIs "aren't available on mobile" [B]. Agent-running plugins such as Agent Fleet ship desktop-only [B] | Read and lightly edit. Bases works on mobile [B]. No agent triggers | Yes |
| Reads the brain repo directly | **Yes**, the live copy on the home machine | Yes, but the *synced copy* on whatever device runs it | Yes, the synced copy | **No.** Data must be pushed out to a third party |
| Triggers headless runs safely | **Yes**, if the server exposes only an allowlist of named jobs (no free-text prompts) and binds to the tailnet | Desktop only, wherever Obsidian is open (usually the laptop) | No | Only by calling back into the home machine, which reopens (a) |
| Side-by-side evidence console | Full control | Possible, but constrained by Obsidian panes | Weak. Tables and cards, no diff view | Full control |

**Recommendation: (a)**, with (c) as a free secondary view. Write decisions back as plain markdown (frontmatter `decision:`, `decided_at:`, `note:` on the ticket file) so Obsidian, git and the agents all see one source of truth and the web app holds no state of its own. The "buttons that run skills" from the creator video belong in (a) as a fixed menu (re-run ticket, run verifier, run named routine), each mapped server-side to one headless command. Never wire a text box straight to the agent. Claude Code's routine API is the pattern here: fired text arrives wrapped and labelled as untrusted data [B].

## 4. Public showcase

Three patterns in use:

- **Static transcript publishing.** `claude-code-transcripts` (2025-12-25) turns real Claude Code sessions into multi-page HTML and can publish to a Gist [B]. It is cheap and honest, but it is reading, not playing.
- **Public trace links.** Observability tools (Langfuse since 2023) can make a single trace or session public [B, background]. That means you depend on a hosted vendor and share one run at a time.
- **Record-and-replay.** Hobby and open-source tools record every model call and tool call and replay the run step by step [D]. One 2026 personal-agent repo publishes a replay log and a recorded walkthrough but "no hosted interactive demo" [D].

**For a "people can open and use" showcase**, the strongest option is the (a) front end built static against a **fixture bundle**: real overnight runs exported, then put through the repo's privacy filters (the same ignore rules and private-prefix lists that already gate tracked files). Visitors get the real four-lane queue. They can approve, return or open evidence, and their clicks change only local state, with an honest "this is a replay of the night of …" banner. Seed it with a few deliberately chosen runs per lane (including a Blocked one and a caught false-done) so the mechanism shows, not just the happy path. Host it as a static site or a published page. Treat the bundle as a derived file that inherits the privacy class of its inputs: diff it before every publish.

## Open questions

- Evening plan approval in the same app, or would that double the habit cost?
- What Verified spot-check rate keeps judgement sharp without becoming a second queue?
- Should the phone *decide*, or only read and defer?

## Sources

**A: academic**
- Dhanorkar, Passi, Vorvoreanu. "Human oversight of agentic systems in practice." arXiv 2606.05391, 2026-06-03. https://arxiv.org/abs/2606.05391
- Mitchell, Ghosh, Passi. "AI Agents Push Humans Out of the Loop." arXiv 2608.23642, 2026-08-24 (rev. 2026-09-06). https://arxiv.org/abs/2608.23642
- Ding et al. "Citations and Trust in LLM Generated Responses." AAAI 2025 (arXiv 2501.01303). https://arxiv.org/abs/2501.01303
- Kambhamettu, Hwang, Laban, Head. "Attribution Gradients." arXiv 2510.00361, 2025-10-01 (rev. 2026-04-03). https://arxiv.org/abs/2510.00361
- "Designing meaningful human oversight in AI." *AI and Ethics*, 2026 (abstract only, paywalled). https://link.springer.com/article/10.1007/s43681-026-01147-7
- "Understanding the Effects of Miscalibrated AI Confidence on User Trust, Reliance, and Decision Efficacy." arXiv 2402.07632, 2024 (*background*). https://arxiv.org/abs/2402.07632
- Zhang, Liao, Bellamy. "Effect of Confidence and Explanation on Accuracy and Trust Calibration." arXiv 2001.02114, 2020 (*background*). https://arxiv.org/abs/2001.02114

**B: primary**
- Anthropic. "Automate work with routines." Claude Code docs, accessed 2026-10-03. https://code.claude.com/docs/en/routines
- Anthropic. Claude Code "What's new," week 16 (2026-04-13 to 17). https://code.claude.com/docs/en/whats-new/2026-w16
- Anthropic. "Continue local sessions from any device with Remote Control." Docs, accessed 2026-10-03. https://code.claude.com/docs/en/remote-control
- Anthropic Engineering. "Claude Code auto mode." 2026-03-25. https://anthropic.com/engineering/claude-code-auto-mode
- OpenAI. Codex app "Automations" docs, accessed 2026-10-03. https://learn.chatgpt.com/docs/automations?surface=app
- GitHub Changelog. "Trace any Copilot coding agent commit to its session logs." 2026-03-20. https://github.blog/changelog/2026-03-20-trace-any-copilot-coding-agent-commit-to-its-session-logs/
- GitHub Changelog. "Copilot Chat now sees your agent sessions." 2026-06-10. https://github.blog/changelog/2026-06-10-copilot-chat-now-sees-your-agent-sessions/
- GitHub Blog. "Introducing Agent HQ." 2025-10. https://github.blog/news-insights/company-news/welcome-home-agents/
- Linear. "Coding sessions" docs, accessed 2026-10-03. https://linear.app/docs/coding-sessions
- Linear. "AI Agents" docs, accessed 2026-10-03. https://linear.app/docs/agents-in-linear
- Cognition. Devin release notes 2026. https://docs.devin.ai/release-notes/2026
- Google. Jules changelog, "Planning Critic." 2026-01-26. https://jules.google/docs/changelog/2026-01-26-1/
- Obsidian. "Mobile development" (plugin docs), accessed 2026-10-03. https://docs.obsidian.md/Plugins/Getting+started/Mobile+development
- Obsidian. Changelog (Bases, Oct 2026). https://obsidian.md/changelog/
- Agent Fleet plugin listing, v0.20.x, 2026. https://community.obsidian.md/plugins/agent-fleet
- Tailscale. "Tailscale Serve examples," accessed 2026-10-03. https://tailscale.com/docs/reference/examples/serve
- Willison. "A new way to extract detailed transcripts from Claude Code." 2025-12-25. https://simonwillison.net/2025/Dec/25/claude-code-transcripts/
- Superhuman. "Built for speed: applying the 100ms rule to email." Undated (*background*). https://blog.superhuman.com/superhuman-is-built-for-speed/
- Langfuse. "Share traces via public link." 2023-09-14 (*background*). https://langfuse.com/changelog/2023-09-14-public-link-sharing

**C: trade or vendor blog**
- Nielsen. "UX Roundup: Vigilance Fatigue." UX Tigers, 2026-10-02. https://www.uxtigers.com/post/ux-roundup-20261002
- Waxell. "AI Agent Approval Workflows." 2026-06-25. https://waxell.ai/blog/ai-agent-approval-workflows
- Vaughan. "Inside the Codex App Workspace." 2026-04-17. https://codex.danielvaughan.com/2026/04/17/codex-app-workspace-pr-review-task-sidebar-artifact-viewer/
- gradually.ai. Codex App changelog, July 2026. https://www.gradually.ai/en/changelogs/codex-app/
- prlens. "How to review GitHub Copilot coding agent pull requests." Undated, 2026. https://prlens.dev/guides/how-to-review-copilot-coding-agent-pull-requests
- TechCrunch. "OpenAI launches Dots." 2026-09-29. https://techcrunch.com/2026/09/29/openai-launches-dots-its-bubbly-agentic-avatar/
- IT Brief Asia. "OpenAI launches dots, always-on AI agents for work." 2026-09. https://itbrief.asia/story/openai-launches-dots-always-on-ai-agents-for-work
- Digital Applied. "Factory AI: Multi-Agent Coding Platform Review 2026." https://www.digitalapplied.com/blog/factory-ai-multi-agent-coding-platform-review
- Mostly Copy and Paste. "Obsidian + Claude Code: Q2 2026 Update." 2026-05. https://mostlycopyandpaste.com/articles/2026/05/obsidian-claude-code-q2-2026-update/

**D: forum, social or hobby repo**
- OpenAI Developer Community. "Codex Cloud task completed… no diff / Create PR." 2026. https://community.openai.com/t/codex-cloud-task-completed-successfully-but-no-diff-create-pr-download-handoff-is-available/1391037
- builderz-labs/mission-control (self-hosted agent control plane), GitHub, 2026. https://github.com/builderz-labs/mission-control
- ManasVardhan/agent-replay, GitHub. https://github.com/ManasVardhan/agent-replay
- sungjin9288/personal-ai-agent (replay log, recorded walkthrough), GitHub, 2026. https://github.com/sungjin9288/personal-ai-agent
