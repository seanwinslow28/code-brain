"""CSV sanitizer for financial data — the Financial Data Airgap.

Strips account numbers, hashes transaction IDs, and outputs clean JSON.
Raw CSVs stay gitignored. The Spending Analysis agent only ever sees
the sanitized output.

Usage:
    from lib.csv_sanitizer import sanitize_chase_csv, sanitize_bilt_csv

    clean_data = sanitize_chase_csv("path/to/chase-statement.csv")
    # Returns list of sanitized transaction dicts
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

# Patterns to strip from descriptions (account numbers, card numbers)
_ACCOUNT_NUM_RE = re.compile(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b")
_PARTIAL_ACCOUNT_RE = re.compile(r"\b\d{4}$")  # Last 4 digits at end of string


def _hash_id(value: str) -> str:
    """Create a deterministic short hash for a transaction ID."""
    return hashlib.sha256(value.encode()).hexdigest()[:12]


def _clean_description(desc: str) -> str:
    """Remove account numbers and PII from a transaction description."""
    desc = _ACCOUNT_NUM_RE.sub("XXXX", desc)
    desc = _PARTIAL_ACCOUNT_RE.sub("XXXX", desc)
    return desc.strip()


def sanitize_chase_csv(filepath: str | Path) -> list[dict[str, Any]]:
    """Sanitize a Chase credit card CSV export.

    Chase format:
        Transaction Date,Post Date,Description,Category,Type,Amount,Memo

    Args:
        filepath: Path to the Chase CSV file.

    Returns:
        List of sanitized transaction dicts with keys:
        tx_hash, date, description, category, type, amount, is_charge, source
    """
    filepath = Path(filepath)
    transactions: list[dict[str, Any]] = []

    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_amount = float(row.get("Amount", "0"))
            tx_id = f"{row.get('Transaction Date', '')}-{row.get('Description', '')}-{raw_amount}"

            transactions.append({
                "tx_hash": _hash_id(tx_id),
                "date": row.get("Transaction Date", ""),
                "description": _clean_description(row.get("Description", "")),
                "category": row.get("Category", ""),
                "type": row.get("Type", ""),
                "amount": abs(raw_amount),
                "is_charge": raw_amount < 0,
                "source": "Chase",
            })

    return transactions


def sanitize_bilt_csv(filepath: str | Path) -> list[dict[str, Any]]:
    """Sanitize a Bilt credit card CSV export.

    Bilt format (no headers, quoted):
        "01/30/2026","-134.97","*","","SEED.COM 8446463586 CA"

    Args:
        filepath: Path to the Bilt CSV file.

    Returns:
        List of sanitized transaction dicts.
    """
    filepath = Path(filepath)
    transactions: list[dict[str, Any]] = []

    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5:
                continue

            date_str, amount_str, _, _, description = row[:5]
            raw_amount = float(amount_str)
            tx_id = f"{date_str}-{description}-{raw_amount}"

            transactions.append({
                "tx_hash": _hash_id(tx_id),
                "date": date_str.strip('"'),
                "description": _clean_description(description),
                "category": "",  # Bilt doesn't provide categories
                "type": "Sale" if raw_amount < 0 else "Payment",
                "amount": abs(raw_amount),
                "is_charge": raw_amount < 0,
                "source": "Bilt",
            })

    return transactions


def sanitize_to_json(
    filepath: str | Path,
    output_path: str | Path | None = None,
    source_type: str = "auto",
) -> Path:
    """Sanitize a CSV and write the result as JSON.

    Args:
        filepath: Path to the input CSV.
        output_path: Where to write the JSON. Defaults to input_path.sanitized.json.
        source_type: "chase", "bilt", or "auto" (detect from filename).

    Returns:
        Path to the sanitized JSON file.
    """
    filepath = Path(filepath)

    if source_type == "auto":
        name_lower = filepath.name.lower()
        if "chase" in name_lower:
            source_type = "chase"
        elif "bilt" in name_lower:
            source_type = "bilt"
        else:
            source_type = "chase"  # Default to Chase format

    if source_type == "chase":
        transactions = sanitize_chase_csv(filepath)
    elif source_type == "bilt":
        transactions = sanitize_bilt_csv(filepath)
    else:
        raise ValueError(f"Unknown source type: {source_type}")

    if output_path is None:
        output_path = filepath.with_suffix(".sanitized.json")
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "source_file": filepath.name,
                "sanitized_at": datetime.now().isoformat(),
                "transaction_count": len(transactions),
                "transactions": transactions,
            },
            f,
            indent=2,
        )

    return output_path
