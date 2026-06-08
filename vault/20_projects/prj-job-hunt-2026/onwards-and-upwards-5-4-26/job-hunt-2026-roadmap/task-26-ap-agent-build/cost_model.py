#!/usr/bin/env python3
"""
cost_model.py — reproducible cost model for the AP invoice-approval agent.

Computes monthly and per-invoice cost for three deployment scenarios at a fixed
volume, so the numbers in cost-model.md are reproducible, not hand-waved. Edit
the ASSUMPTIONS / PRICES blocks and re-run to re-cost.

Prices are June 2026 published rates (sources in cost-model.md), STANDARD rates
(no batch discount, no prompt caching) unless you change them. Those two levers
are discussed in the markdown.
"""

# ---- Assumptions (edit + re-run) ----
INVOICES_PER_MONTH = 5000
INPUT_TOKENS = 3000       # system policy + instructions + invoice + PO + vendor record
OUTPUT_TOKENS = 500       # verdict + structured reasoning trace
CLASSIFIER_OUTPUT = 300   # Haiku first-pass output is terser
ESCALATION_RATE = 0.05    # fraction sent to the deeper (Sonnet) model in hybrid

# ---- Prices: USD per million tokens (June 2026, standard rates) ----
PRICES = {
    "opus":   {"in": 5.0,  "out": 25.0},   # Claude Opus 4.8
    "sonnet": {"in": 3.0,  "out": 15.0},   # Claude Sonnet 4.6
    "haiku":  {"in": 1.0,  "out": 5.0},    # Claude Haiku 4.5
}

# ---- Self-host (AWS) ----
G5_12XL_HOURLY = 5.672    # g5.12xlarge on-demand, us-east-1 (4x A10G, 96GB GPU)
HOURS_PER_MONTH = 730
RESERVED_FACTOR = 0.60    # ~40% off via 1-yr commitment (illustrative)

# ---- Reference: human cost it offsets ----
MANUAL_COST_PER_INVOICE = 5.83   # APQC cross-industry median, fully loaded


def call_cost(model, n, in_tok, out_tok):
    p = PRICES[model]
    return n * (in_tok * p["in"] + out_tok * p["out"]) / 1_000_000


def main():
    n = INVOICES_PER_MONTH

    # A) Frontier-only: Opus on every invoice
    a = call_cost("opus", n, INPUT_TOKENS, OUTPUT_TOKENS)

    # B) Hybrid: Haiku classifies/extracts ALL; Sonnet deep-passes the escalated slice
    b_haiku = call_cost("haiku", n, INPUT_TOKENS, CLASSIFIER_OUTPUT)
    escalated = round(n * ESCALATION_RATE)
    b_sonnet = call_cost("sonnet", escalated, INPUT_TOKENS, OUTPUT_TOKENS)
    b = b_haiku + b_sonnet

    # C) Self-host Llama 3.1 70B on g5.12xlarge — FIXED cost, volume-independent
    c_ondemand = G5_12XL_HOURLY * HOURS_PER_MONTH
    c_reserved = c_ondemand * RESERVED_FACTOR

    manual = MANUAL_COST_PER_INVOICE * n

    print(f"Assumptions: {n:,} invoices/mo | {INPUT_TOKENS} in / {OUTPUT_TOKENS} out tokens "
          f"| {ESCALATION_RATE:.0%} escalation\n")
    print(f"{'Scenario':40s}{'$/month':>12s}{'$/invoice':>12s}")
    print("-" * 64)
    print(f"{'A) Frontier-only (Opus 4.8)':40s}{a:>12,.2f}{a/n:>12.4f}")
    print(f"{'B) Hybrid (Haiku all + Sonnet ' + str(int(ESCALATION_RATE*100)) + '%)':40s}{b:>12,.2f}{b/n:>12.4f}")
    print(f"{'C) Self-host g5.12xlarge (on-demand)':40s}{c_ondemand:>12,.2f}{c_ondemand/n:>12.4f}")
    print(f"{'   Self-host g5.12xlarge (reserved ~40% off)':40s}{c_reserved:>12,.2f}{c_reserved/n:>12.4f}")
    print("-" * 64)
    print(f"{'(ref) Manual processing @ $5.83/invoice':40s}{manual:>12,.2f}{MANUAL_COST_PER_INVOICE:>12.4f}")

    print()
    print(f"* Hybrid is {a/b:.1f}x cheaper than frontier-only "
          f"(the Opus:Haiku price ratio is 5:1; the deeper-pass slice softens it slightly).")
    print(f"* Self-host (on-demand, ${c_ondemand:,.0f}/mo) only beats HYBRID above "
          f"{c_ondemand/(b/n):,.0f} invoices/mo,")
    print(f"  and beats FRONTIER-ONLY above {c_ondemand/(a/n):,.0f} invoices/mo "
          f"— i.e. {c_ondemand/(b/n)/n:.0f}x and {c_ondemand/(a/n)/n:.0f}x today's volume.")
    print(f"* All API options are {b/manual:.2%}-{a/manual:.2%} of the ${manual:,.0f}/mo manual labor they offset.")


if __name__ == "__main__":
    main()
