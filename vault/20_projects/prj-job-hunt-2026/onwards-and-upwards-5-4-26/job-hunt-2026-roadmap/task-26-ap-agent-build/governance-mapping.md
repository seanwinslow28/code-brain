# Governance Mapping — AP Invoice-Approval Agent

How the agent satisfies the two governance regimes an enterprise buyer (and its auditors and model-risk function) will ask about: **SOC 2** (the security/controls audit every SaaS vendor faces) and **SR 11-7** (the bank-grade model-risk standard — quoting it signals you can sell into regulated buyers). Control language is quoted verbatim from primary sources, verified in the [research reference brief §4](../2026-06-08-task-26-research-reference-brief.md) (AICPA 2017 Trust Services Criteria; Federal Reserve SR 11-7).

The connective tissue for all of it is the **decision log** defined in the Session A trust-boundary review — one immutable record per decision that serves as evidence for three different controls at once.

---

## Part 1 — SOC 2 (Trust Services Criteria, Common Criteria)

Three controls carry this agent. The IDs are verified — **CC7.2 is monitoring and CC8.1 is change management** (the roadmap's original draft had these two transposed; corrected here).

### CC6.1 — Logical access controls
> *"The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events to meet the entity's objectives."* (AICPA 2017 TSC, CC6.1)

**How the spec satisfies it:** the agent is a first-class *identity*, not an ambient script. It authenticates with **scoped, least-privilege credentials** — read access to the invoice/PO/vendor systems it needs, write access only to its decision log. It has **no direct payment-rail or vendor-master write** (IT-security user story #7). It cannot move money; it can only route a decision that a downstream, separately-permissioned system acts on. That separation is also segregation-of-duties (the agent that recommends approval is not the system that disburses).

### CC7.2 — System monitoring / anomaly detection
> *"The entity monitors system components and the operation of those components for anomalies that are indicative of malicious acts, natural disasters, and errors affecting the entity's ability to meet its objectives; anomalies are analyzed to determine whether they represent security events."* (AICPA 2017 TSC, CC7.2)

**How the spec satisfies it:** the agent makes ~190 autonomous decisions/day — too many for human review, which is *why monitoring must be automated*. The system watches the decision stream for anomalies the spec already names: a spike in auto-approval rate, a new payee, a duplicate slipping through, a threshold breach, a cluster of L5 hard-blocks (a possible attack in progress). The metrics from Step 3 (false-positive rate, override rate, escalation rate) are the monitoring signals; the trust-boundary's verifiability log is the data they run on.

### CC8.1 — Change management
> *"The entity authorizes, designs, develops or acquires, configures, documents, tests, approves, and implements changes to infrastructure, data, software, and procedures to meet its objectives."* (AICPA 2017 TSC, CC8.1)

**How the spec satisfies it:** you cannot silently change the brain of a money-moving agent. Every change to the **model version, the system prompt, the escalation thresholds, or the match tolerances** flows through authorize → test → document → approve → deploy. Two spec hooks enforce this: the AP-manager adjusts thresholds through a **change-controlled config, not code** (user story #2), and **the eval suite (Session B) is the test gate** — no model-version bump or prompt change ships until it passes the suite. This is also the mitigation for the build-vs-buy memo's "silent capability degradation" failure mode.

### SOC 2 mapping table

| Control | Verbatim meaning | Spec mechanism | Evidence artifact |
|---|---|---|---|
| **CC6.1** | Logical access | Least-privilege agent identity; no payment-rail/vendor-master write | IAM scope config; access logs |
| **CC7.2** | Monitoring / anomaly detection | Automated anomaly detection on the decision stream; Step-3 metrics | The decision log + alerting |
| **CC8.1** | Change management | Model/prompt/threshold changes gated by review + the eval suite | Change records; eval-run results |

---

## Part 2 — SR 11-7 (Model Risk Management)

**Issuer:** "Supervisory Guidance on Model Risk Management," April 4 2011 — **Federal Reserve SR 11-7**, jointly **OCC Bulletin 2011-12**. Principles-based; the de facto U.S. model-governance standard.

**The agent is a "model" under SR 11-7.** Its qualitative inputs produce a decision output, which is squarely within the guidance's definition — so the model-inventory, validation, and effective-challenge expectations attach directly.

**Core principles, and how the spec meets them:**
- **Development, implementation, use** — *"Model risk management begins with robust model development, implementation, and use."* The PRD, the escalation tree, and the eval suite are the development-and-use documentation.
- **Independent validation** — *validation must be performed by parties separate from development.* The model risk officer (user story #8) signs off before production; the eval suite gives validation an objective instrument.
- **Effective challenge** — *"critical analysis by objective, informed parties who can identify model limitations and assumptions and produce appropriate changes."* The precision case in the eval suite (the keyword stub's documented over-flagging) is effective challenge in action — the spec names its own limitation rather than hiding it.
- **Governance** — model inventory entry with a named owner and a materiality rating; ongoing monitoring with defined re-validation triggers.

**Risk-tiering — stated precisely.** SR 11-7 **does not define numbered risk tiers**; it makes *materiality* the proportionality lever — *"where models and model output have a material impact… a bank's model risk-management framework should be more extensive and rigorous."* Numbered tiers are how **institutions operationalize** that principle. So: we classify this agent as a **moderate-materiality model (a "Tier 2" in a typical 3-tier inventory)**, and we can *defend the tier with a control we designed* — the financial blast radius is capped at **$5,000** by the auto-approve ceiling, with bank changes, new vendors, and adversarial content structurally excluded from autonomy. The materiality is bounded, so the validation rigor is proportionate.

> Saying it this way — "SR 11-7 sets principles, not tiers; we operationalize materiality with a dollar-bounded tier" — is the credibility signal to a regulator-literate reader. It shows you've read the guidance, not just the buzzword.

---

## Part 3 — The audit-trail schema (the shared backbone)

One immutable record per decision (agent *or* human), **write-once / read-many, tamper-evident**. This single artifact is the evidence for CC7.2 (monitoring), CC8.1 (change provenance), and SR 11-7 (ongoing monitoring + outcomes analysis) simultaneously — built once in the trust boundary, cited by every regime.

```json
{
  "record_id": "uuid (immutable)",
  "timestamp": "UTC ISO-8601",
  "invoice_id": "INV-1001",
  "actor": "agent:ap-approver@v1.4.2  |  human:jdoe (clerk)",
  "model": "claude-haiku-4.5  (+ claude-sonnet-4.6 on escalation)",
  "inputs_ref": ["invoice://INV-1001", "po://PO-771", "vendor://AWS"],
  "decision": "L1 auto_approve | L2 flag_clerk | ... | L5 hard_block",
  "rules_fired": ["match:clean", "amount<=5000", "vendor:known_unchanged"],
  "reasoning_trace": "string — why this level was chosen",
  "confidence": 0.0,
  "reviewer": "human id + action, if escalated",
  "reversal_status": "none | reversed_within_24h | settled"
}
```

| Field group | Satisfies |
|---|---|
| `timestamp`, `actor`, `model`, `reasoning_trace` | SR 11-7 outcomes analysis; CC7.2 monitoring |
| `model` version + `rules_fired` | CC8.1 change provenance (which version/rules produced this decision) |
| `decision`, `reviewer`, `reversal_status` | Auditor reconstruction (user story #5); the override/false-positive metrics (Step 3) |

## How this connects to the rest of the spec

- The **trust boundary (Session A, Step 6)** defines the blast radius that justifies the SR 11-7 materiality tier.
- The **eval suite (Session B)** is the CC8.1 test gate and the SR 11-7 validation instrument.
- The **build-vs-buy memo (Step 8)** chooses a platform whose own SOC 2 / ISO posture provides the substrate this application's controls sit on.

## Sources
Research reference brief §4 — AICPA 2017 Trust Services Criteria (CC6.1 p.29, CC7.2 p.34, CC8.1 p.38, verbatim); Federal Reserve SR 11-7 (federalreserve.gov/supervisionreg/srletters/sr1107.htm); audit-trail field consensus (FINOS AI governance framework; industry practice). ⏱ TSC point-of-focus language is from the 2017 criteria; confirm against the current edition at publish.
