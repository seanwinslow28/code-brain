"""Tests for logging_setup module."""

from __future__ import annotations

from pathlib import Path

from lib.logging_setup import record_run, setup_logger


class TestSetupLogger:
    def test_creates_log_file(self, tmp_path: Path):
        logger = setup_logger("test-agent", tmp_path, log_level="DEBUG")
        logger.info("Test message")

        log_files = list(tmp_path.glob("test-agent-*.log"))
        assert len(log_files) == 1

        content = log_files[0].read_text(encoding="utf-8")
        assert "Test message" in content

    def test_mode_suffix(self, tmp_path: Path):
        logger = setup_logger("daily-driver", tmp_path, mode="morning")
        logger.info("Morning log")

        log_files = list(tmp_path.glob("daily-driver-*-morning.log"))
        assert len(log_files) == 1


class TestRecordRun:
    def test_creates_csv_with_header(self, tmp_path: Path):
        record_run(
            log_dir=tmp_path,
            agent_name="daily-driver",
            mode="morning",
            status="success",
            cost_usd=0.12,
            duration_ms=45000,
            turns=8,
            notes="Created daily note",
        )

        csv_file = tmp_path / "agent-run-history.csv"
        assert csv_file.exists()

        content = csv_file.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert len(lines) == 2  # Header + 1 row
        assert "date,time,agent,mode,status" in lines[0]
        assert "daily-driver" in lines[1]
        assert "morning" in lines[1]
        assert "success" in lines[1]

    def test_appends_to_existing_csv(self, tmp_path: Path):
        record_run(tmp_path, "agent1", None, "success", 0.10, 1000, 5)
        record_run(tmp_path, "agent2", "mode", "error", 0.05, 500, 2, "Failed")

        csv_file = tmp_path / "agent-run-history.csv"
        lines = csv_file.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 3  # Header + 2 rows
