# Kickoff: rule on the /craftwork recipe, then finish eng-005's Open

Paste everything below the line into a fresh Claude Code session at the code-brain root.

---

Two jobs this session, in this order. Do the first fully before starting the second. I'm a PM, not a dev: plain language, define any jargon before asking me to decide, **one question at a time with your recommendation**, and wait for my answer. Never name the startup in GitHub issues or tracked files; its name lives only in the private ledgers.

## Job 1 — my ruling on the `/craftwork` recipe (GitHub #328)

The craftwork build-5 ticket (#328 on seanwinslow28/code-brain) landed in commit 6df3c01a and is **held open for my review**. It is the last open ticket on the Productcraft build map (#264).

1. Read `.claude/skills/craftwork/SKILL.md` in full, `craftwork/README.md` § How a team is built, and #328's resolution comment (`gh issue view 328 --comments`).
2. Give me a short plain-language summary of what the recipe tells a future session to do. Then put these three items to me **one at a time**, each with a recommendation:
   - (a) Adopted by recommendation, not yet ruled: a rule that two teams both need moves to `craftwork/law.md` on its own ticket, with its origin named, and is never copied.
   - (b) Adopted by recommendation: `generic-drift` sits in a voice-bearing team's `taxonomy.md` as a sighted shape from scaffold.
   - (c) Left open: a team whose output is only *sometimes* voice-bearing. The earlier recommendation was to declare it voice-bearing and open its other engagements in a plain mode.
3. Then ask me for the verdict: **ship, amend, or reject**. Apply any amendments, run `python3 scripts/validate.py`, commit and push. Before pushing, run `git pull --rebase --autostash`, because the Mac Mini auto-commits the vault.
4. On ship: post a closing comment, close #328, and append its Decisions-so-far line to the map #264 body. The line is ready in #328's resolution comment. Move the "Review the `/craftwork` recipe text" ticket in `vault/00_inbox/tickets.md` to Done. #328 is the map's last ticket, so **ask me** before closing map #264 itself.

## Job 2 — finish eng-005's Open (Systemcraft)

Run it through the `systemcraft` skill's Open stage. The engagement folder is the one matching `systemcraft/ledger/engagements/eng-005-*`. That ledger is private and its own git repo, so commit there, never in code-brain. Only the intake has run; its state is `accepted`, and the return is due **2026-12-04**. **Stop when Open is ratified. Do not fire any seat this session.**

Read first: the folder's `open-brief.md`, `intake-check.md`, `open-amendment-shared-law.md`, the systemcraft skill, `craftwork/law.md`, and `craftwork/templates/runtime-registry.md`, especially § First trial round, § Standing and § The trial protocol. The inbox line "Finish eng-005's Open before its first seat runs" in `vault/00_inbox/tickets.md` lists what's owed.

Walk me through these as decisions, one at a time:

1. **Ratify `open-amendment-shared-law.md`.** Its status is `proposed`. Nothing else in Open applies until I rule it ratified, amended or rejected.
2. **Roster and runtimes.** The five seats pin `claude-opus-5-5` (Design Strategist, Architecture Advisor, Evals & Evidence Architect) and `claude-sonnet-5-5` (Interaction & Trust Designer, Ops & Economics Modeler). Run the alias probe at Route per the law. Also run the thin-lane check Open now owes.
3. **Pass budget.** Propose the funded cap. Separately, and outside the cap, declare the **first trial round** exactly as the registry's § First trial round rules it:
   - trial 1: GLM-5.3 shadowing the Design Strategist pass, Codex → OpenRouter (row 4);
   - trial 2: Kimi K3 shadowing Ops & Economics, Codex → OpenRouter (row 4);
   - trial 3: MiMo-V2.6-Pro shadowing Architecture, Pi → OpenRouter (row 6);
   - trial 4: Qwen3.8-27B (`qwen3.8-27b-64k`, local) shadowing Trust Designer, Pi → Ollama (row 6);
   - each with `shadow_of` naming the specific planned pass;
   - each OpenRouter trial carrying **$15 per trial** on the line.

   The key is ready: `OPENROUTER_TRIALS_API_KEY` in `.env`, $30 limit, verified 2026-10-03. Qwen is pulled and built on this MacBook, and runs at ~6 tokens per second. The Codex isolation check is trial 1's *setup* when that seat fires, not an Open task. Pi and Hermes aren't installed yet. Flag that as setup owed before trials 3–4, not a blocker for Open.
4. **Pre-register the P0-equivalent rule.**
5. **The intake's three scoping rulings:**
   - (a) pin the startup's build-map ticket files the asks read, by date and hash;
   - (b) allow a bounded desk check for the two outside facts (a no-per-message-charge subscriber email route; vendor model-snapshot lifetimes), or have both read `UNMEASURED`;
   - (c) state that eng-004's repairs were never re-verified (G-M10), so the audit baseline is repaired-but-unverified text.
6. **The intake's recommendation to return the three interim-surface answers early.** This one is time-sensitive: the startup decides its interim surface on **2026-10-09**. Help me decide whether and how those answers come back before the rest of the return.

When Open is ratified: commit the ledger, and update the eng-005 lines in `vault/00_inbox/tickets.md`. Leave the trial-related line pointing at the first seat's session.

## Also due soon — not this session's job, remind me at the end

The **memo-06 ruling** on pc-eng-002's held Leadership memos is due **before Mon 2026-10-05**. It's a separate inbox ticket; read `readout/leadership.md` in the Productcraft private ledger.
