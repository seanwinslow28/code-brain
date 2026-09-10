# Productcraft

The product leadership studio: a seven-seat bench that plans, executes, and audits product work as a sequential pipeline of owned artifacts. This glossary holds the studio's language as it gets resolved; the ratified decisions themselves live on the build map's tickets.

## Language

### Artifacts and the train

**Seat**:
One of the seven specialist identities in the bench, each owning exactly one artifact, one lane manifest, one audit duty, and a baseline model.
_Avoid_: agent, persona, role

**Artifact**:
The single named document a seat owns and hands forward in full, never as a summary.
_Avoid_: deliverable, output, bundle

**Packet**:
An artifact with fixed, named parts that ships as one unit (the Discovery packet, the Leadership packet). Audits cover the whole packet, with the stake anchored on one named part.
_Avoid_: bundle, set

**Train**:
The seven seats running in pipeline order on a full-train engagement, each receiving every artifact above it.
_Avoid_: panel, pipeline run

**Loopback**:
A downstream seat returning an upstream artifact to its drafting seat with evidence, instead of rewriting it in place.
_Avoid_: override, edit, rewrite

### Checks

**Co-sign**:
A fresh-context pass by a second seat over one named section of another seat's artifact, passing or bouncing each claim, required before that artifact is done. Three exist in the train: Insights on Discovery's evidence, Insights' own stage-three check on the Strategist's outcomes, the Strategist on Delivery's OKR translation.
_Avoid_: review, approval, sign-off

**Audit**:
A fresh-context invocation by a peer seat over a complete artifact, never the drafting conversation, with a one-sentence stake. Every seat audits exactly one artifact and is audited by exactly one peer, in two closed cycles.
_Avoid_: review, critique, QA

**Stake**:
The one question an auditor is adversarially responsible for answering about the artifact it audits.
_Avoid_: checklist, criteria

**Evidence-strength grade**:
The label the Insights seat attaches to each claim in a Discovery evidence section, judged against raw-evidence pointers rather than summaries.
_Avoid_: confidence score, rating

**Red-team gate**:
A milestone check run as a stateless protocol, not by a seat, on the vendor that did not last write its anchor artifact; fires at strategy sign-off, before the handoff crosses, and at close.
_Avoid_: audit, review

**Anchor artifact**:
The one artifact a gate or a packet audit is answerable for: the Strategy & POV doc at strategy sign-off, the handoff brief before it crosses, the whole train at close. It decides which vendor runs the gate.
_Avoid_: primary artifact, focus

### Engagements

**Engagement**:
One unit of studio work, typed at Open as one of five kinds: full train, audit, execution breakdown, one-off, or support landing a role.
_Avoid_: project, session, run

**Execution breakdown**:
The Delivery-only engagement that turns a design returned from the Systemcraft handoff into buildable work: epics, stories in a design set and an implementation set, and a first sprint plan, filed as tracker issues. It creates the implementation candidate that Systemcraft's pre-launch gate waits for.
_Avoid_: sprint planning, grooming, ticketing

**Handoff brief**:
The typed packet the Delivery seat produces after its roadmap is co-signed, carrying the ask, referenced artifacts by id, constraints, and a return date across to Systemcraft. It never carries reasoning.
_Avoid_: spec, handoff doc, PRD

**Ledger**:
The private, accreting record of every material decision the studio makes, one entry per decision, each with its "from the canon" line.
_Avoid_: log, changelog, history

### People and parties

**Stakeholder**:
Anyone who can block, fund, use, or judge the thing being designed. Appears on the stakeholder map, one row per party, with Sean split by hat (decider, builder, funder) and absent classes stated.
_Avoid_: user, teammate, audience

**Teammate**:
Whoever does the work, human or agent. Appears in the team topology, never on the stakeholder map; agents are their own entity type there and are never presented as people.
_Avoid_: stakeholder, resource, collaborator

**Gatekeeper**:
A stakeholder that can block release without being a user: app-store review, a payment processor, a platform's terms.
_Avoid_: blocker, dependency

**Judge**:
A stakeholder that assesses the outcome after the fact: hiring managers for portfolio work, customers or investors for a business.
_Avoid_: audience, reviewer

**Canon line**:
The one-breath statement of which title and idea a seat leaned on for a material choice. Names the book and the idea; never quotes the book.
_Avoid_: citation, source, reference

### Models

**Baseline**:
The runtime a seat runs on unless a named trigger fires: vendor, model, and reasoning effort, declared in the seat file. It names what actually runs, never a nominal tier.
_Avoid_: default model, preferred model, tier

**Deviation**:
A per-pass change from a seat's baseline, made against a named trigger and recorded with a one-line why. Never silent, never per-engagement.
_Avoid_: override, swap, exception

**Escalation**:
A deviation one tier up, made only on evidence of failure: a gate FAIL, an audit that bounced substance, or the seat's own thin-corpus flag. Never at draft time, and never because the artifact feeds a gate.
_Avoid_: upgrade, bump, boost

**Escalation target**:
The runtime an escalation lands on. The top of the ladder is a different vendor from the seat's baseline, so a redraft gets a different brain; the ceiling model is never entered without the owner's say-so.
_Avoid_: fallback, backup model

**Downshift**:
A deviation one tier down, for mechanical work only: transforms of existing substance, single-source lookups, checklist application, clerical filing. The file-or-defer decision itself stays at baseline.
_Avoid_: downgrade, cheap mode

**Pass budget**:
The integer count of funded invocations an engagement declares at Open: the base manifest plus two pre-authorized rounds per scheduled gate, the coordinator's own session included. Exhaustion is a stop and a question to the owner, never a silent overrun.
_Avoid_: token budget, cost cap

**Meter line**:
What every invocation records about itself: runtime, runtime-reported tokens, and wall-clock, or UNMEASURED. A partial total is stated as a known subtotal plus the number of unmeasured passes, never as a precise figure.
_Avoid_: cost line, usage

**Substitution**:
A dated, owner-approved change of vendor for a pass whose planned runtime is unavailable, preserving the seat's identity: same seat contract, lane, target, and audit duty, in a fresh invocation.
_Avoid_: fallback, reroute

**Deferral**:
A dated stop of one seat's branch when its runtime is unavailable and no substitution is approved. The dependent work waits; lanes are never merged to keep moving.
_Avoid_: skip, pause
