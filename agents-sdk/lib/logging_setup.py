"""Structured logging and run history tracking for autonomous agents."""

from __future__ import annotations

import csv
import logging
import sys
from datetime import date, datetime
from pathlib import Path


def setup_logger(
    agent_name: str,
    log_dir: Path,
    log_level: str = "INFO",
    mode: str | None = None,
) -> logging.Logger:
    """Create a logger that writes to both stderr and a per-run log file.

    Args:
        agent_name: Name of the agent (e.g., "daily-driver").
        log_dir: Directory for log files (vault/90_system/agent-logs/).
        log_level: Logging level string (DEBUG, INFO, WARNING, ERROR).
        mode: Optional mode suffix (e.g., "morning", "evening").

    Returns:
        Configured logger instance.
    """
    log_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    suffix = f"-{mode}" if mode else ""
    log_file = log_dir / f"{agent_name}-{today}{suffix}.log"

    logger = logging.getLogger(f"agent.{agent_name}")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Clear existing handlers to avoid duplicates on re-init
    logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    )
    logger.addHandler(file_handler)

    # Stderr handler (for launchd capture)
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(
        logging.Formatter("[%(levelname)s] %(message)s")
    )
    logger.addHandler(stderr_handler)

    return logger


def record_run(
    log_dir: Path,
    agent_name: str,
    mode: str | None,
    status: str,
    cost_usd: float | None,
    duration_ms: int | None,
    turns: int | None,
    notes: str = "",
) -> None:
    """Append a row to the agent run history CSV.

    Args:
        log_dir: Directory containing agent-run-history.csv.
        agent_name: Name of the agent.
        mode: Agent mode (e.g., "morning") or None.
        status: Run status ("success", "error", "cancelled").
        cost_usd: API cost in USD.
        duration_ms: Total duration in milliseconds.
        turns: Number of conversation turns.
        notes: Free-text notes about the run.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    history_file = log_dir / "agent-run-history.csv"

    write_header = not history_file.exists()

    with open(history_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow([
                "date", "time", "agent", "mode", "status",
                "cost_usd", "duration_ms", "turns", "notes",
            ])
        writer.writerow([
            date.today().isoformat(),
            datetime.now().strftime("%H:%M:%S"),
            agent_name,
            mode or "",
            status,
            f"{cost_usd:.4f}" if cost_usd is not None else "",
            duration_ms or "",
            turns or "",
            notes,
        ])
