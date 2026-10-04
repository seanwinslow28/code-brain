---
title: "Reachable-User Product Opportunity Scan"
type: product-discovery
status: complete
domain: [product-management]
created: 2026-09-06
research-window: 2026-08-08 to 2026-09-07
methods: [last30days, product-trio-ideation, competitive-scan]
---

# Reachable-User Product Opportunity Scan

## Decision summary

**Recommended first concept: ClearLoop, an AI decision-packet compiler.** Start with creative-production feedback: a producer pastes comments from email, Slack, meeting notes, and an existing review tool; ClearLoop merges duplicates, surfaces contradictions and ambiguity, preserves the source of every request, and produces one reviewable action-and-approval packet tied to the current version.

The product should complement tools such as Frame.io and Ziflow rather than host video or replace their review workflows. The initial beta can also be tested on adjacent feedback-heavy work by two product managers and one CSM, giving the concept a plausible path to five reachable repeat users.

Do not implement yet. First run a concierge validation with real, redacted feedback bundles.

## Objective and constraints

- Find a real recurring problem among people Sean can reach directly.
- Produce a polished MVP in three to five weeks.
- Optimize for at least five people using it repeatedly without prompting.
- Make AI essential to the workflow rather than decorative.
- Create a strong PM interview story: discovery, segmentation, product judgment, human-in-the-loop AI, measurement, and iteration.
- Avoid handling sensitive tax, government, or customer data in the first validation.

## Reachable beta network

| Tester | Useful problem lens | Early constraint |
|---|---|---|
| Girlfriend, CSM | Sales-to-CS handoff, onboarding context, stakeholder follow-up | Customer data may be sensitive |
| Two cousins, accountants | Missing client inputs, inconsistent schedules, document chasing | Financial data and incumbent portals |
| Friend, VFX producer | Conflicting feedback, wrong versions, late approvers, revision loops | One direct specialist tester |
| Cousin, IRS | Administrative burden and procedural work | Government policy, procurement, and privacy make this a poor MVP wedge |
| Two PM friends | Stakeholder feedback, project-management tax, decisions without context | Crowded tool market |
| Sean, girlfriend, family/friends | Household coordination and mental load | Requires multi-person adoption |

## Research method and limitations

The scan used ten `last30days` passes: seven broad role/everyday-life searches and three deeper opportunity searches. It covered Reddit, X, YouTube, and supplemental web research. The research tool reported 30 Reddit threads, 23 X posts, and 24 YouTube videos across the passes.

The raw counts overstate usable evidence. Several broad searches had low-relevance X and YouTube results, and recent household and public-sector discussions were limited. Those results were filtered out of the conclusions instead of being treated as demand. Reddit discussions, direct product documentation, and recent workflow articles carried most of the useful signal.

## What the evidence says

### 1. Work stalls at human decision boundaries

The strongest cross-role pattern was not task generation. It was the coordination required before someone can act or approve:

- A recent agency discussion described losing a client over the feedback process; the most-supported workaround was a dated, shared feedback document.
- VFX and video workflow sources repeatedly described feedback arriving through different channels, reviewers commenting on different versions, late decision-makers, and contradictory requests.
- Product managers described pressure to manage the project in addition to the product.
- Approval workflows across industries break when the request, discussion, document, and final decision live in different systems.

This is a good AI problem when the model **compiles evidence for a human decision**. It is a bad AI problem when the model makes the approval autonomously.

### 2. Missing context creates avoidable rework before work begins

The CSM and accounting evidence converged on incomplete intake:

- Customer Success begins onboarding without the customer's desired outcome, promises made during sales, stakeholder ownership, constraints, or success criteria.
- Accountants chase client documents and then discover wrong periods, inconsistent versions, or schedules that cannot be trusted.
- The work is often represented as a checklist, while the actual problem is determining whether the submitted information is sufficient and internally consistent.

The opportunity is a readiness gate that says what is missing, why it matters, and the smallest next request needed to unblock work.

### 3. Household tools often relocate the mental load

Recent household discussions asked for built-in schedules rather than another blank task database. Other discussions explicitly warned that logging and assigning chores creates one more job for the person already carrying the mental load.

The category is active and crowded. Current products already advertise AI setup, fair rotation, neutral reminders, default templates, and low-friction onboarding. A new product would need to prove that it eliminates administration over multiple weeks, not merely that it can generate a chore plan.

### 4. Public-sector pain is real but is not the right first build

Recent posts showed burnout, policy frustration, workload pressure, and procedural burden. Those are meaningful problems, but the causal levers are management incentives, staffing, policy, and procurement. A five-week consumer-style MVP is unlikely to change them, and testing with government or tax data introduces unnecessary risk.

## Competitive boundary

The following spaces are already well served:

- Frame.io and Ziflow centralize versioned creative review, comments, proofs, and approvals. Ziflow also markets AI-assisted review checks.
- Financial Cents already provides passwordless client requests, secure uploads, automated email/SMS reminders, and recurring request lists.
- Demodesk already extracts meeting context and automates sales-to-CS handoffs and CRM updates.
- Household products such as ChoreLoop, FairlyDo, ChoreCycle, and Petal Home already offer shared schedules, rotation, reminders, and increasingly AI-assisted setup.

Therefore, the wedge should be an **overlay for messy inputs across existing tools**. It should not be another video host, CRM, accounting portal, household checklist, or general project-management workspace.

## Opportunity Solution Tree

**Desired outcome:** Within five weeks, five reachable users voluntarily use the product more than once.

```text
Desired outcome
├── Reduce time spent turning scattered feedback into an actionable decision
│   ├── Creative/VFX feedback compilation
│   ├── PM stakeholder-decision compilation
│   └── Cross-channel approval packet
├── Start client work with complete, consistent context
│   ├── Sales-to-CS handoff readiness
│   └── Accounting request/submission readiness
└── Reduce household coordination without appointing an administrator
    ├── Setup-free routine generation
    └── Neutral delivery through tools people already use
```

## Product-trio ideation

### Product Manager perspective

1. **ClearLoop** — Convert scattered feedback into a single version-aware action and approval packet.
2. **KickoffReady** — Grade a sales-to-CS handoff for outcomes, promises, owners, risks, and success criteria before onboarding begins.
3. **RequestReady** — Check an accountant's client request and submitted file set for missing, ambiguous, wrong-period, or conflicting inputs.
4. **Home Without a Manager** — Generate and maintain a shared household routine without making one partner the permanent administrator.
5. **Decision Debt Digest** — Turn stakeholder messages and meetings into a traceable log of decisions, reversals, assumptions, and unresolved questions.

### Product Designer perspective

1. **One-Link Review** — Give occasional reviewers one current-version link with voice or text input and no account setup.
2. **Conflict Room** — Show contradictory requests side by side and ask the correct decision-maker to resolve only the conflict.
3. **Plain-English Ask Builder** — Translate professional requests into short client-facing explanations, examples, and acceptance criteria.
4. **Zero-Setup Household Start** — Let a household describe its people, rooms, and routines by voice and immediately receive an editable first week.
5. **Current-Version Lock** — Make obsolete feedback visibly obsolete and redirect reviewers to the current artifact without blame or confusion.

### Software Engineer perspective

1. **Feedback Normalizer** — Classify each comment as action, question, preference, approval, or non-actionable context; merge semantic duplicates.
2. **Readiness Schema Engine** — Apply a role-specific schema to unstructured notes and identify only the missing fields that block the next step.
3. **Change Verification** — Compare a new version with the approved request list and flag likely completions, regressions, and unresolved changes for human review.
4. **Provenance Ledger** — Link every synthesized action to its original message, author, timestamp, and artifact version.
5. **No-New-App Delivery** — Accept input and deliver prompts through email, shared links, calendar, or chat so infrequent collaborators do not adopt another workspace.

## Prioritization model

Weights reflect this project's goals: pain frequency 25%, reachable testability 20%, five-week feasibility 15%, meaningful AI leverage 15%, differentiation 10%, and interview value 15%.

| Rank | Concept | Pain | Reach | Feasibility | AI | Differentiation | Interview | Weighted score |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | ClearLoop | 5 | 4 | 4 | 5 | 4 | 5 | **91/100** |
| 2 | KickoffReady | 5 | 3 | 4 | 4 | 3 | 5 | **82/100** |
| 3 | Home Without a Manager | 4 | 5 | 4 | 3 | 2 | 4 | **77/100** |
| 4 | Decision Debt Digest | 4 | 3 | 4 | 4 | 3 | 5 | **77/100** |
| 5 | RequestReady | 5 | 3 | 3 | 4 | 2 | 4 | **74/100** |

## Prioritized concepts

### 1. ClearLoop — recommended

**One sentence:** Paste or forward feedback from multiple channels and receive one source-linked packet of actions, conflicts, open questions, owners, and approvals for the current version.

**Why selected:** It addresses the clearest cross-role pattern, has a sharp first wedge in VFX/creative production, can be tested by VFX, PM, and CSM users, and gives AI a necessary but bounded job: semantic normalization and conflict detection. It also creates an unusually strong interview story around provenance, uncertainty, human authority, and measurable workflow outcomes.

**Key assumptions to validate:**

- Users spend meaningful time manually consolidating feedback at least twice per month.
- They will paste, forward, or export feedback instead of forcing every reviewer into a new tool.
- The model can distinguish actions, preferences, questions, duplicates, and contradictions accurately enough to earn trust.
- A source-linked packet is more useful than a polished summary.
- At least two users will bring a second feedback bundle within one week.

### 2. KickoffReady

**One sentence:** Turn sales calls and notes into a CSM-ready kickoff brief, then block or return the handoff when critical context is missing.

**Why selected:** Missing sales context appears repeatedly and has measurable downstream consequences: repeated customer questions, kickoff rework, expectation mismatch, and delayed time to value. A direct CSM tester is available.

**Key assumptions to validate:**

- The girlfriend's organization has access to usable sales-call notes or recordings.
- Existing CRM and meeting tools do not already produce an adequate handoff.
- A readiness decision is more valuable than another summary.
- The organization permits a prototype to process redacted or synthetic data.

### 3. Home Without a Manager

**One sentence:** Create and maintain a shared household routine through conversational setup, fair rotation, and neutral delivery in tools household members already check.

**Why selected:** It has the easiest recruitment path and a real recurring problem. It would demonstrate consumer discovery and multi-user behavior design.

**Key assumptions to validate:**

- The core problem is coordination overhead rather than disagreement about fairness or standards.
- A household will keep using the system after the initial novelty fades.
- Delivering through SMS/calendar/chat materially improves participation.
- The product can differentiate from several new competitors with nearly identical promises.

### 4. Decision Debt Digest

**One sentence:** Convert PM meetings and stakeholder messages into a traceable decision history that highlights reversals, unsupported scope changes, and unresolved dependencies.

**Why selected:** PMs repeatedly absorb project-management work, and the output is easy to test with two PM friends. Decision provenance and change detection create a sophisticated AI-product case study.

**Key assumptions to validate:**

- Decision rediscovery is a frequent pain, not merely an annoyance.
- Users will trust automatic links between a decision and its supporting evidence.
- The concept can avoid becoming another meeting summarizer or project-management database.

### 5. RequestReady

**One sentence:** Help accountants send clearer requests and detect missing or mismatched client submissions before review begins.

**Why selected:** Client document collection is a strong, concrete pain, and two accountants are available for interviews. The readiness-checking layer is more differentiated than reminders alone.

**Key assumptions to validate:**

- Wrong or incomplete submissions occur frequently even when portals and reminders are used.
- A prototype can prove value using synthetic or heavily redacted files.
- Firms would adopt an overlay rather than rely on incumbent practice-management suites.
- The privacy and accuracy burden remains feasible for a solo MVP.

## Recommended MVP boundary for ClearLoop

Build only after validation:

- Paste text or upload a simple exported notes file.
- Require a human-entered artifact name and version.
- Extract actions, questions, approvals, duplicates, ambiguities, and contradictions.
- Preserve a clickable source excerpt for every extracted item.
- Let the owner edit, accept, reject, and assign items.
- Produce one shareable, locked decision packet.
- Measure consolidation time, conflicts caught, packet edits, time to approval, and repeat use.

Explicitly exclude video hosting, frame-accurate playback, Slack/CRM integrations, automated approval, account hierarchies, and multi-version visual diffing from the first MVP.

## Validation before implementation

1. Interview the VFX producer, CSM, two PMs, and one accountant about the most recent real instance—not desired features.
2. Ask each person for a redacted feedback or handoff bundle they already processed.
3. Run a concierge test: manually feed each bundle through a structured prompt and return a source-linked decision packet.
4. Compare the packet with what the person actually did. Record omissions, false conflicts, edits, and time saved.
5. Offer the same workflow again on their next real bundle without reminding them.

**Evidence gate for building:**

- At least three of five users experienced the problem twice in the previous month.
- At least three provide a real redacted artifact.
- At least three say the packet clarified or caught something meaningful.
- At least two return with a second artifact within one week.
- Median consolidation time falls by at least 50% without a material accuracy failure.

## Ideas to reject for now

- A new general-purpose project-management workspace.
- A Frame.io replacement or video-hosting product.
- A generic sales-call summarizer.
- A generic accounting client portal or reminder engine.
- A chore tracker whose novelty is AI-generated tasks.
- Any first version that processes IRS, taxpayer, or live financial records.
- An autonomous agent that decides what feedback or compliance requirements can be ignored.

## Research coverage

---
✅ All agents reported back!
├─ 🟠 Reddit: 30 threads │ 1,862 upvotes │ 1,318 comments
├─ 🔵 X: 23 posts │ 1,107 likes │ 105 reposts
├─ 🔴 YouTube: 24 videos │ 6,609,772 views │ 12 with transcripts
├─ 🌐 Web: 79 search results — Sohonet, Financial Cents, Customer Onboarding Tools, AlphaMa, Automatic.co
└─ 🗣️ Top relevant voices: @ancrid_motion │ r/agencynewbies, r/ProductManagement, r/Accounting, r/CustomerSuccess
---

## Selected web references

- [Sohonet — Review bottlenecks in post production](https://www.sohonet.com/article/review-bottlenecks-in-post-production-2026-fixes)
- [Financial Cents — Client tasks and requests](https://help.financial-cents.com/en/articles/4213219-client-tasks-requests)
- [Customer Onboarding Tools — Sales-to-onboarding handoff](https://customeronboardingtools.com/guides/sales-to-onboarding-handoff/)
- [AlphaMa — Why household chore apps create marital friction](https://alphamothers.com/resources/household-chore-apps-create-marital-friction)
- [Automatic.co — The approval workflow from hell](https://automatic.co/blog/approval-workflow-from-hell)
- [Ziflow — ReviewAI](https://www.ziflow.com/reviewai)
- [Demodesk — AI agents](https://help.demodesk.com/en/articles/14490765-ai-agents)

