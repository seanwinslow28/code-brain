---
type: operating-model
artifact: operating-model
domain: [the-block]
status: confirmed
last_interviewed: 2026-04-19
created: 2026-04-18
review-date: null
ai-context: "Synthesized one-file operating model for The Block. Cross-references HEARTBEAT, USER, SOUL, schedule-recommendations. Loaded by agents at the start of any Block-domain work."
---

# Operating Model — The Block

## TL;DR
Sean is an Associate Product Manager at The Block (crypto/ETF media + data + education company) on a ~5-month ramp as of 2026-04-19. He operates on an early-Boston schedule (wake 5:15 AM → gym → work 8:45 AM – 5:15 PM with a sacred first hour, a 9–2 deep-work block, a hard 2–3 PM decompression, and a 3–5:15 PM execution + Slack sweep). His leverage model is "Claude as a senior-PM stand-in" — he delegates aggressively with a tight review pass, uses Ed Rupkus as his human north star and tiebreaker, and builds skills / automations into `.claude/skills/` as the primary way to increase his output. The org is in an executive transition: Larry Cermak is President + interim CEO through 2026-04-30; **Steve W. Chung starts as CEO on 2026-05-01** (tech + media + global executive, ex-CJ ENM / FOX / Azuki).

## Identity in This Domain
- **Role:** Associate Product Manager, reporting to Ed Rupkus (Product Manager, Portland OR / Pacific).
- **Stakes:** Career pivot into PM from 10 yrs of multimedia management; still in "learn everything, attend every meeting" mode.
- **Stated goals:** Become a hard-working PM like Ed, with his own creative + technical edge. Drive the pre-CEO roadmap prep (with The Block Pro revamp as the flagship pitch). Champion future crypto×AI product surface (x402 protocol, agent-wallet intersections).
- **Organizational moment:** Larry Cermak is President and interim CEO through 2026-04-30; **Steve W. Chung** starts as CEO on 2026-05-01 — he brings a tech + media + global-scale lens (CJ ENM, FOX Corporation's LiveNOW / FOX SOUL, Frankly, Azuki). His arrival likely reshapes the Pro-revamp pitch and could pull Sean's media-team interests closer to Block revenue strategy.

## Operating Rhythm Summary
Morning is sacred: 8:45 AM Daily Driver SDK agent pre-seeds the Obsidian day note, Sean re-runs `daily-driver` in Claude Code to pull Gmail / Slack / Granola / Calendar / prior-day notes, and protects 8:45–9:45 from meetings. Deep work 9–2; lunch 11:30–12:30 doubles as AI-tooling learning time. 2–3 PM is an off-computer decompression walk. 3–5:15 PM is execution + Slack sweep + Obsidian prioritization for tomorrow. Tue/Wed/Thu 10 AM Daily Standups (he leads) are non-negotiable. The bi-weekly P&E update (Claude + `jira-automation` → Ed edits → CPO approves → `@here` post to `#ask-product-management` at 4 PM ET) is the rhythmic capstone. ETF coverage is event-driven off `#research-etf`. Seasonal crypto cycles haven't registered yet — too new. See [[HEARTBEAT]].

## Decision Pattern Summary
Prioritization stack (what actually wins, in order): Ed-signal → closest-to-shipping → unblock-someone-else → deadline pressure → leverage R&D (Claude skills, PM automation, crypto×AI product research). Auto-yes to anything from Ed or Matt (CPO), any ticket Sean wrote with an open dev/designer question, and meeting invites in general (new-hire mode). Auto-defer on RevOps/AdOps favors and Salesforce Campus emails (always done eventually, never high-priority). Agent delegation is aggressive with a mandatory review pass — except for two hard nevers: write access to The Block's **GitHub** and **WordPress** backend. Tiebreaker: write both options to Obsidian, review after meetings, ask Ed for strategy / Slack the dev or designer for tactical, default to whatever unblocks someone else. See [[USER]].

## Dependency Map Summary
**Critical human-path:** Ed (manager, daily overlap), Matt Vitebsky (CPO, bi-weekly sign-off), Larry Cermak (President / interim CEO through 2026-04-30), Steve W. Chung (incoming CEO from 2026-05-01), Mike Price (Lead Dev, gated access to the Block API), David (Sr. Mgr Course Design & Compliance — Campus), Josh + Claudine + Serena (design), Cesar (DevOps), Koray (SEO), plus a go-to dev bench (Mike, Brian Mendoza, Nikola Pivcevic, Ramuald Vishneuski). **Tools (hard-collapse):** Jira, Confluence, Slack, Google Calendar, Gmail, Obsidian, Claude Code. **APIs:** TwelveData, TradingView, SEC.gov, CoinGecko, RWA.xyz, and the Block's internal API (access pending from Mike). **AI primaries:** Claude > Perplexity > Gemini; Ollama (phi4-mini, Qwen3-14B) growing. Anthropic outage = largest single-point-of-failure. **Three-machine topology:** Mac Mini is primary (all domains + SDK agents + Prototype-Lab); MacBook Pro handles meetings / couch / travel with 48 GB unified memory; Alienware has no Block work yet (potential NemoClaw experimentation). **Source of truth:** Slack + Jira + Confluence + Granola are canonical; G-Suite is runner-up fabric; Obsidian is Sean's private processing layer, not a company source. See [[SOUL]] Part A.

## Institutional Context Summary
Internal vocabulary spans `.Co`, `Campus`, the `Pro` tier and its sub-products, `Sponsored Courses`, the `Block iOS app`, `Election Hub` / `Voting Block Index`, `Knowledge Token Taxonomy`, `Crypto IQ`, and `x402 protocol` (Sean's push, not yet implemented). Sacred cows: the Figma simple-slides template, `Context → Problem → Solution` presentation structure, user-journey-first for every new page / product, `jira-automation`-compliant ticket format, and calibrated roadmap ambition (Matt reined in the first pass — pitch "revamp a product that already makes money," not moonshots). Communication is Slack-default with Jira/Figma/Confluence comments for paper-trail; Ed's DM is ASAP; `@here` is reserved for the bi-weekly P&E post only. The David ↔ devs misalignment (two incidents) is the live landmine — remediated by the new weekly Campus team sync (Tue 09:30 ET, starting 2026-04-28). The team knows Sean as the AI-tools person who responds quickly on his phone even mid-break; they don't know he uses Granola or that Claude drafts his Slack / comments before he edits. See [[SOUL]] Part B.

## Active Leverage Points
- **The 9 AM – 2 PM deep-work block.** Unmatched for PRD writing, skill building, Prototype-Lab iteration.
- **Skill building as throughput multiplier.** `.claude/skills/` is the dominant channel for turning one-off Block learnings into durable output.
- **Ed as a force multiplier.** He knows the org deeply; surfacing the right question to him outperforms solo research.
- **Media team untapped.** Sean's 10 yrs of multimedia experience + the media team's ideas backlog (`vault/30_domains/product-management/media-team-ideas/`) is latent revenue leverage — and Steve Chung's CJ ENM / FOX / OTT background means this might become a first-class strategic lane post-2026-05-01.
- **The CEO-transition window (through 2026-05-01 + the first 90 days after).** The Pro-revamp roadmap prep with Ed + Matt is the chance to set Steve's first-impression agenda, not just react to it.

## Known Bottlenecks
- **Meeting → ticket/Slack backflow** is the single biggest context-switch drain; Claude hallucinates out-of-scope stack assumptions that require a scrub pass.
- **Three-machine hopping** during Agents-SDK experiments — unification is flaky. Open ask for a redesign.
- **`jira-automation` doesn't reconcile Slack/Granola "shipped" signals** with Jira state; Sean manually resolves every bi-weekly cycle.
- **Daily Driver SDK agent has no MCP access** → forces a re-run in interactive Claude Code every morning.
- **Figma Dev-Mode workaround** (download `.fig` → personal account) is a daily papercut. Declining to buy a company seat, so the automation has to route around it.
- **Zapier fragility** for colleague automations; desired pivot to Claude-Agents-SDK-built workflows.
- **No GA4 / Looker OAuth access** inside Claude Code yet.
- **Block API access pending** from Mike Price (deliberately not being pushed).
- **Self-blocking queue items:** `"Is this blocker real?"` triage, ticket writing, design-review approvals, P&E wording, ticket clean-up passes.
- See [[schedule-recommendations]] for the full friction + automation list.

## Cross-Domain Bleed
- **→ Creative Studio:** Prototype-Lab (UX user-journey tool), Claude-Design skill work, Block design-system skill, Nano-Banana-Pro diagrams, and media-team collaboration all sit at the Block ↔ Creative-Studio boundary.
- **← Creative Studio:** Sean's design + animation instincts keep leaking into Block work; he wants more of that, not less. Steve Chung's media / OTT background could legitimize this lane.
- **↔ Life Systems:** Boston move pushed wake time from 4:45 AM to 5:15–5:30 AM, which compresses the morning learning window. Gym-open time (7:00) anchors the day.
- **↔ Claude mastery layer:** Block skills (`jira-automation`, `etf-page-creator`, `prd-generator` for Block, and the forthcoming `sprint-health`) are the operational output of Sean's broader Claude-Code experimentation.

## Current Open Questions
- What direction does **Steve W. Chung** pick for The Block Pro revamp, and how does his media / OTT / global-expansion background reshape the 2026 roadmap Ed + Sean are prepping?
- Does Steve's arrival pull the media-team collaboration lane (`vault/30_domains/product-management/media-team-ideas/`) from "latent" to "strategic"?
- When does Mike Price unlock Block API access, and what agentic workflows become possible afterward?
- Is the weekly Campus team sync enough to fix the David ↔ devs misalignment pattern, or is a deeper process change needed?
- What's the cleanest three-machine topology that doesn't require mid-day display-swapping?
- Which `.claude/skills/` capability closes the Slack/Granola ↔ Jira reconciliation gap — extending `jira-automation` vs. a new `sprint-health` skill?
- Can Zapier be fully replaced by Claude-Agents-SDK for colleague-automation requests?
- What does the 6-month-mark (2026-05-10) re-evaluation of "accept every meeting" actually look like?

## Related Artifacts
- HEARTBEAT: [[HEARTBEAT]]
- USER: [[USER]]
- SOUL: [[SOUL]]
- Schedule rules: [[schedule-recommendations]]
- Tier-0 identity: [[Sean-Winslow-Full-Personal-Context-v2.0|Full Personal Context]]
