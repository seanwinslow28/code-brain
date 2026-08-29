# EXPLANATION.md

A 4Q comprehension artifact (Nate B. Jones) for Code Brain. The explanation that travels with the work: what this is, why this approach, what would break, what I learned.

---

## What is this?

One engineer's working second brain, in daily production since February 2026. The public half is machinery: 133 skills, 13 subagents, 16 hooks and a Claude Agent SDK layer, all auto-loaded (counts measured 2026-08-29 with `ls .claude/{skills,agents,hooks}/`; the numbers drift, the command doesn't). The private half is an Obsidian vault the machinery reads and writes. Between them an autonomous fleet runs on launchd schedules: it indexes the vault at 2am, synthesizes concept and connection articles out of whatever changed, critiques them with two rival CLIs, writes the morning note, and reports on its own health. 218 concepts, 694 connections, and 152 concept expansions plus 178 connection expansions from the critic have accumulated that way, all of them tracked in the repo (`git ls-files vault/knowledge/`).

The loop is the point. Every Claude Code session ends by flushing its decisions into the vault, and every session opens on what the fleet synthesized overnight. The repo is both the running system and the record of building it, incident write-ups and disabled-agent post-mortems included.

## Why this approach?

**Skills are prompts; agents are runners.** SKILL.md files load as system prompts into the autonomous agents instead of being reimplemented in Python, so improving a skill in an interactive session improves the 2am agent that uses it, with no second copy to drift. The alternative, prompt text embedded in each runner, is the version that rots quietly and gets discovered when two agents disagree about their own instructions.

**Local models on the default path, paid models as the exception.** Almost everything that runs unattended here runs free: the indexer, the synthesizer, the researcher, the job feed and the session flush all cost $0.00 a night on local models. Only the morning note bills a metered API, and the nightly critic rides on two subscriptions I already pay for. The rule got tested on the inbox-triage agent, which worked on cloud Sonnet and was switched off anyway at six SDK invocations, six files moved, $6.97, or $1.16 a file. Working is not the bar. Working at a price that survives running every night is the bar, and a fleet that only runs when I feel rich is not a fleet. I am still paying for that call. The local rewrite was scoped at three or four hours in April and never written, so inbox triage has simply been off since then.

**Hooks enforce; subagents judge.** Anything binary is a deterministic shell hook that exits 2 and blocks. Anything subjective is a subagent that writes an opinion and blocks nothing. I rejected the tidier-sounding single LLM gate for everything, because a nondeterministic gate on a binary rule fails open in precisely the cases you built it for, and I rejected all-hooks because no regex reviews taste.

**Machinery public, operating data private, enforced structurally.** Financial, health, employer and job-search material lives in a gitignored local layer that public skills read at runtime, so the repo ships the skill and never the profile. The cheap version was one repo plus care, and care is not a control. This is a gitignore block, a validator, and a history rewrite. It is also the boundary that has already failed, below.

## What would break?

These are live, knowingly accepted risks, not fixed defects.

**1. The fleet cannot page me, and never has.** The alert path is built and switched on: `agents-sdk/lib/pushover.py` ships and `[notifications.push_strong_fits]` reads `enabled = true`. The credentials resolve on this MacBook and are absent from the Mac Mini that actually runs the nightly jobs, so every send from the machine that matters has failed. The Mini's synthesizer stderr log holds 369 of those failures, most recent 2026-08-28, with no successful send in any Mini log ever. I could not reproduce that count from here, which is the problem rather than a footnote to it: the evidence lives on the machine I am not watching. A quiet night and a dead fleet look identical from where I sit, and the health agent built to tell them apart reports through the channel that has never delivered.

**2. Half the leak is fixed and half is not mine to fix.** A `git filter-repo` scrub in August removed 69 company names from history, and a normal `git clone` is clean, verified against a fresh clone pulled from GitHub rather than the local repo. GitHub keeps `refs/pull/*` forever. Re-checked while writing this: 143 pull refs still resolve on origin, and `refs/pull/141/head` fetches commit `3335772`, which exists nowhere in the rewritten history. Anyone running `git clone --mirror` still gets pre-rewrite objects. No client-side remedy exists, so the last step is GitHub Support ticket #4659070, open since 2026-08-12 and fileable only from the account owner. The gate closes on a clean mirror clone, not on a Support reply.

**3. The consumer half of the knowledge loop reads a fifth of the graph and says nothing about it.** The SessionStart hook injects `vault/knowledge/index.md` under a 15,000-character cap. The index is now 106,066 characters, alphabetically ordered, concepts before connections. Measured today, that window carries 190 of 218 concepts and 0 of 694 connections; the Connections heading begins at character 17,427, past the cap. Truncation appends no notice, so the injected block reads as the whole index and stops mid-wikilink. Connections used to come through, and the share getting in fell as the concept list above them grew. On 2026-07-22 the heading crossed to character 15,053, fifty-three characters past the cap, and the half of the graph that the synthesizer and the typed-edge work exist to produce has been absent from every session since. Nothing failed, because nothing was checking. It degraded by growing.

**4. Every quality gate here is a person remembering.** The synthesizer eval suite is a manual pre-ship gate and it sat unrun across a 192-line change to the agent it guards; re-running found no regression, which is luck reported honestly rather than a control working. Fleet health is the same shape: the last 30 manifests in `vault/health/` read 25 ok, 2 deferred and 3 errors (2026-07-29 to 2026-08-28), which is better than this repo's own May write-up claims, and is still only as true as my willingness to open the file. One operator is the throughput ceiling and the only reviewer, and nobody else would notice if I stopped looking.

## What did I learn?

**Most of what an unattended fleet needs is a way to be wrong out loud.** The expensive failures here were never crashes. They were an agent reporting `ok` over empty output for nine nights, a history scrub that passed every check I thought to run and failed the one I hadn't, an index that shrank its own coverage by growing. Each stayed invisible because the thing being checked, exit status or clean clone or hook fired, was not the thing that mattered.

**Value is the number worth auditing; cost is the easy one.** The April audit disabled 8 of 10 agents, and the finding was not that they were expensive. Two of them were free and still worthless. What did this produce that anyone used is a harder question than what did it spend, and it is the one that shrank the fleet.

**A system that documents itself will document things that were never true.** CLAUDE.md claimed 6 agents were disabled and named two that had never existed as code, until an archaeology pass ran `git log --diff-filter=AD` and got nothing back. The fix was not better memory. It was grepping the claim before repeating it, which is why this document names its commands.
