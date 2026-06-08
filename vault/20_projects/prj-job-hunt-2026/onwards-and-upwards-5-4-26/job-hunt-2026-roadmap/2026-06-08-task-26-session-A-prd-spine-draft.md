---
title: "Task 26 — Session A working draft: PRD spine"
type: working-draft
project: prj-job-hunt-2026
created: 2026-06-08
status: "DRAFT — Steps 1-3 drafted by Claude for Sean to refine; Steps 5-6 built interactively"
becomes: "Sections of PRD.md when the enterprise-ap-agent-spec repo is created"
related:
  - "[[2026-06-08-task-26-enterprise-ap-agent-spec-execution-plan]]"
  - "[[2026-06-08-task-26-research-reference-brief]]"
---

# Session A — PRD Spine (working draft)

> This is a draft for Sean to own and edit. Numbers and claims are grounded in the research reference brief. The example company is named **Meridian** for concreteness (placeholder — change if you prefer).

---

## Step 1 — Problem statement

Meridian is a 200-person B2B SaaS company. Its three-person Accounts Payable (AP) team processes about **5,000 supplier invoices a month** — recurring cloud and software bills, contractor payments, marketing spend, travel and office reimbursements. Today every invoice is reviewed by hand: a clerk opens it, matches it to a purchase order, checks the vendor and the math, and clicks approve. Average handling time is roughly **8 minutes per invoice**. At that rate the team spends about 80% of its capacity on invoices that are clean, recurring, and unambiguous — the boring ~95% — and is chronically too rushed to give real scrutiny to the ~5% that are genuinely risky.

That imbalance is expensive in two directions. **On cost:** industry benchmarks put fully-loaded cost-per-invoice at a median of **$5.83** (APQC), with best-in-class automated teams at ~$2.78 versus ~$9.40 for laggards (Ardent Partners, 2025) — Meridian sits on the wrong side of that line. **On risk:** AP is the most-attacked financial function in the company. In 2024, **79% of organizations** faced attempted or actual payments fraud (AFP); business email compromise and vendor-bank-detail-change fraud alone drove **$2.77B** in reported U.S. losses (FBI IC3); and **0.8–2% of disbursements** leak to duplicate or erroneous payments (APQC). A rushed human reviewing ~60 invoices a day is exactly the condition under which those losses happen.

We will deploy an **AP invoice-approval agent** that auto-approves the clean ~95% within seconds and escalates the risky ~5% to the right human **in under 30 seconds** — with hard, auditable guardrails on what it is allowed to do on its own. The goal is not to remove humans; it is to move human attention off the boring bulk and onto the small set of decisions where judgment and fraud detection actually matter.

*(~310 words.)*

---

## Step 2 — User stories (8)

**1. AP clerk** — *As an AP clerk, I want the agent to auto-approve clean, in-tolerance invoices and hand me only the ones that need a human look (with the reason and evidence attached), so that I spend my day on judgment calls instead of rubber-stamping recurring bills.*
- Agent auto-approves invoices meeting all Level-1 criteria with no clerk action required.
- Every escalated invoice arrives with a structured reason code, the matched PO, and the specific discrepancy highlighted.
- Clerk can approve / reject / return-to-vendor from a single screen.

**2. AP manager** — *As an AP manager, I want to see why the agent made each auto-approval and to set the thresholds it runs under, so that I can trust it without re-checking everything and tighten it if something looks off.*
- Every auto-approval exposes a viewable reasoning trace.
- Manager can adjust dollar thresholds and match tolerances through a change-controlled config (not code).
- A dashboard shows auto-approval rate, escalation rate, and override rate over time.

**3. Vendor (supplier)** — *As a supplier, I want my correct invoices paid on time and a clear status when something is held, so that I'm not chasing payment or resubmitting blindly.*
- In-tolerance invoices move to "approved for payment" within the agent's SLA.
- A held invoice produces a specific, vendor-safe status reason (no internal detail leaked).
- Status is queryable without contacting AP directly.

**4. Controller** — *As the controller, I want high-value and policy-exception invoices to always reach me before payment, and a complete audit trail for everything below that, so that I keep control over material spend and can defend it at close.*
- Any invoice over the controller threshold, or flagged as a policy exception, hard-routes to the controller.
- No payment is released on those without explicit controller approval.
- Every decision (agent or human) is immutably logged.

**5. Auditor** — *As an internal/external auditor, I want every approval decision reconstructable — who or what approved it, on what basis, against which controls — so that I can test the control environment without manual sampling pain.*
- Each decision record carries timestamp, actor (agent+version or named human), inputs, rule(s) applied, decision, and reviewer.
- Logs are write-once / tamper-evident.
- I can export the full decision population for any period.

**6. CFO** — *As the CFO, I want the program to measurably cut cost-per-invoice and fraud loss without introducing uncontrolled risk, so that the investment is defensible to the board.*
- Cost-per-invoice and cycle-time are tracked pre/post deployment.
- Worst-case loss per autonomous decision is bounded by a stated dollar cap.
- A quarterly metrics pack ties the agent to dollar outcomes.

**7. IT security** — *As IT security, I want the agent to operate under least-privilege access and to be hardened against malicious invoice content, so that automating AP doesn't open a new attack surface into our financial systems.*
- Agent authenticates with scoped, least-privilege credentials (read invoices, write decisions — no direct payment-rail or vendor-master write).
- Invoice content is treated as untrusted data, never as executable instruction.
- Adversarial inputs are blocked and logged.

**8. Model risk officer** — *As the model risk officer, I want the agent governed as a model — inventoried, independently validated, and proportionate to its materiality — so that we meet model-risk expectations and can challenge it effectively.*
- Agent is entered in the model inventory with a named owner and a materiality rating.
- Independent validation (separate from the build team) signs off before production.
- Performance is monitored on an ongoing basis, with defined thresholds that trigger re-validation.

---

## Step 3 — Success metrics (6)

Two value metrics (is it earning its keep?) and two guardrail metrics (is it safe?), plus adoption and trust. Read false-positive rate *with* escalation rate — they move against each other.

| # | Metric | What it measures | How it's computed | Target | Why it matters |
|---|---|---|---|---|---|
| 1 | **Adoption rate** | Share of eligible invoices actually routed through the agent | agent-handled ÷ total invoices | ≥90% by day 90 | If people route around it, nothing else matters. |
| 2 | **Fallback-to-human (escalation) rate** | Share the agent escalates instead of auto-approving | escalated ÷ total handled | ~5% steady state | Too high = not earning its keep; too low = possibly over-approving (read with #5). |
| 3 | **Override rate** | Share of agent decisions a human reverses on review | human-reversed ÷ agent decisions reviewed | <2% and falling | The trust signal — high override means the agent's judgment isn't right or isn't trusted. |
| 4 | **Time-to-Trust** | How long until AP managers stop double-checking auto-approvals | days from go-live until manager spot-checks on auto-approvals fall below ~10% sampled | ≤30 days | The human-adoption outcome; the product fails if people never relax. |
| 5 | **False-positive rate on auto-approval** | Share of auto-approvals that should NOT have been (caught later by audit, dup-detection, or reversal) | bad auto-approvals ÷ total auto-approvals | <0.5%; zero tolerance for >cap or fraud | The dangerous metric — the agent's safety record on money. The whole trust boundary exists to keep this near zero. |
| 6 | **Cost-per-invoice processed** | Fully-loaded processing cost per invoice (human time + system/LLM cost) | total AP processing cost ÷ invoices | move from laggard toward best-in-class (~$2.78) | The headline business case; ties the agent to a dollar the CFO recognizes. |

---

## Step 5 — Escalation decision tree

**Locked design parameters:** Balanced posture (auto-approve ceiling **$5,000**) · **5 levels** · hard overrides = adversarial signal, vendor bank-detail change, suspected duplicate.

### Decision inputs (the signals the tree reads)

For every invoice the agent computes:
- **Integrity check** — adversarial content (prompt injection, SQL injection, authority-spoof), vendor-not-in-master, sanctions/blocklist hit.
- **Bank-detail-change flag** — did this invoice/vendor record change banking details vs. the master?
- **Duplicate check** — fuzzy match on (vendor + amount + invoice# + date).
- **PO match status** — clean within tolerance / out-of-tolerance / missing PO. (Tolerance is the AP-manager-configured price/qty band, e.g. within X% or $Y.)
- **Vendor status** — known-and-unchanged / brand-new (first-ever invoice).
- **Amount band** — ≤$5K / $5K–$25K / $25K–$100K / >$100K.

### Two rules that make the tree unambiguous

1. **Evaluation order — integrity and override checks run FIRST, before the dollar/match logic.** Security gates precede business logic; a malicious invoice is never "small enough to auto-approve."
2. **Highest-level-wins.** When multiple conditions apply, the invoice routes to the **most conservative** applicable level. (An $80K suspected duplicate is L3 by amount and floored by the duplicate override — it lands at the higher of the two.)

### The tree

**Pre-checks (short-circuit overrides — evaluated first, bypass the dollar logic):**

| Trigger | Routes to | Why |
|---|---|---|
| Any adversarial/injection signal · vendor not in master · sanctions hit | **L5 — Hard-block + audit-log** | Never auto-approve a malicious or unknown-entity invoice; fire security review. |
| Vendor **bank-detail change** (any amount, even $50) | **L4 — Controller** + out-of-band callback to on-file number | Largest fraud category ($2.77B BEC); requires dual control + verification. |
| **Suspected duplicate** (fuzzy-match hit) | **floor at L2 — AP-clerk** (never L1; escalates higher if amount/match also triggers) | Duplicate/erroneous payments leak 0.8–2% of disbursements; a human confirms before release. |

**Base logic (if no override fires):**

| Level | Action | Criteria | Human can | Logged |
|---|---|---|---|---|
| **L1** | **Auto-approve** | Clean 2-/3-way match within tolerance · vendor known & unchanged · **amount ≤ $5,000** · no override | — (agent acts) | full reasoning trace |
| **L2** | **Flag for AP-clerk** | Clean match, **amount $5,000.01–$25,000** · OR minor in-tolerance anomaly · OR **brand-new vendor's first invoice ≤$5K** *(locked)* | approve / reject / return | reason code + evidence + clerk decision |
| **L3** | **Escalate to AP-manager** | **Out-of-tolerance mismatch** · **missing PO** · amount **$25,000.01–$100,000** | investigate / approve / reject | discrepancy detail + manager decision |
| **L4** | **Escalate to controller** | Amount **>$100,000** · vendor bank-detail change (from pre-check) · policy-exception request | approve / reject (no payment without this) | full case file + controller decision |
| **L5** | **Hard-block + audit-log** | From pre-check (adversarial / unknown vendor / sanctions) | security review only | immutable incident record |

**SLA:** the routing decision (which level) is produced in **<30 seconds**.

### Locked decision — brand-new vendor handling

A brand-new vendor's **first** invoice can never be L1 auto-approved — it **floors at L2 clerk review** even when clean and ≤$5K. After that first clean invoice clears a human, the vendor becomes "known" and flows through the normal logic. Rationale: this closes the shell-vendor opening (fake-vendor billing schemes are ~20% of fraud cases, ~$100K median loss) without sending routine new-supplier onboarding all the way to senior staff. *(Decided 2026-06-08.)*

---

## Step 6 — Trust-boundary review

The four questions that decide how much autonomy is safe. Each is answered with a number, not a vibe — and together they justify classifying the agent as a **moderate-materiality (Tier-2-equivalent) model** under SR 11-7.

**Blast radius — worst-case damage from one wrong autonomous action.** Capped at **$5,000.** The only thing the agent does alone is L1 auto-approval, which requires a clean in-tolerance match, a known-and-unchanged vendor, no duplicate, no adversarial flag, and amount ≤$5K. The highest-loss fraud vectors are *structurally excluded from autonomy*: bank-detail changes (→L4), brand-new vendors (→L2), unknown vendors and adversarial content (→L5). So a single missed bad auto-approval cannot move more than $5K, and cannot be the BEC or shell-vendor attack at all.

**Reversibility — can a wrong action be undone?** Yes, within a **24-hour window.** An L1 approval routes the invoice into the next scheduled payment batch, not an instant irreversible wire; a flagged auto-approval can be pulled via a payment-hold before the run executes. The settlement lag is the recovery window.

**Frequency — how often it acts autonomously.** ~5,000 invoices/month ≈ **~200/day**, ~95% auto ≈ **~190 autonomous decisions/day.** This volume is *both* the justification for autonomy (humans cannot meaningfully review 190 clean invoices a day) *and* the reason monitoring must itself be automated — which is exactly the SOC 2 CC7.2 control in the governance mapping.

**Verifiability — can every action be audited?** Yes. Every decision (agent or human) writes an immutable, **write-once / tamper-evident** record: timestamp, actor (agent+version or named human), input references, rule(s) applied, decision, reasoning trace, confidence, reviewer, and reversal status. Every autonomous decision is fully reconstructable.

**Synthesis.** A bounded $5K blast radius + a 24h reversibility window + automated monitoring of a high-frequency stream + a complete immutable audit trail = an autonomy envelope a model risk officer can sign off on. The same decision log is the shared evidentiary backbone for CC7.2 (monitoring), CC8.1 (change provenance), and SR 11-7 (outcomes analysis) — built once in Step 6, cited three times in Session D.
