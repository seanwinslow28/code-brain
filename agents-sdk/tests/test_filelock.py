"""Tests for lib.filelock — fcntl-based exclusive/shared file locking."""

from __future__ import annotations

import multiprocessing as mp
import time
from pathlib import Path

import pytest

from lib.filelock import FileLock, LockTimeout


def _child_exclusive(lock_path: str, hold_secs: float, result_q: mp.Queue) -> None:
    """Child process: acquire EX lock, hold it, release."""
    with FileLock(Path(lock_path), exclusive=True):
        result_q.put(("acquired", time.monotonic()))
        time.sleep(hold_secs)
        result_q.put(("released", time.monotonic()))


def _child_shared(lock_path: str, hold_secs: float, result_q: mp.Queue) -> None:
    """Child process: acquire SH lock, hold it, release."""
    with FileLock(Path(lock_path), exclusive=False):
        result_q.put(("acquired", time.monotonic()))
        time.sleep(hold_secs)
        result_q.put(("released", time.monotonic()))


def _child_try_ex_with_timeout(
    lock_path: str, timeout_secs: float, result_q: mp.Queue
) -> None:
    """Child process: try to acquire EX with timeout. Report outcome."""
    start = time.monotonic()
    try:
        with FileLock(Path(lock_path), exclusive=True, timeout=timeout_secs):
            result_q.put(("acquired", time.monotonic() - start))
    except LockTimeout as exc:
        result_q.put(("timeout", time.monotonic() - start, str(exc)))


class TestFileLock:
    def test_ex_blocks_ex(self, tmp_path: Path) -> None:
        """Two exclusive locks on the same file must serialize."""
        lock_path = tmp_path / "x.lock"
        q1: mp.Queue = mp.Queue()
        q2: mp.Queue = mp.Queue()

        # Start first process, it holds the lock for 0.5s
        p1 = mp.Process(target=_child_exclusive, args=(str(lock_path), 0.5, q1))
        p1.start()
        # Wait until p1 has actually acquired the lock before starting p2
        evt = q1.get(timeout=2.0)
        assert evt[0] == "acquired"
        p1_acquired_at = evt[1]

        # Now p2 tries to acquire — should block until p1 releases
        p2 = mp.Process(target=_child_exclusive, args=(str(lock_path), 0.0, q2))
        p2.start()

        p1.join(timeout=5.0)
        p2.join(timeout=5.0)
        assert p1.exitcode == 0 and p2.exitcode == 0

        # Drain p1's "released" event
        rel = q1.get(timeout=1.0)
        assert rel[0] == "released"
        p1_released_at = rel[1]

        # p2's acquire must come at or after p1 release (serialized)
        p2_acquired = q2.get(timeout=1.0)
        assert p2_acquired[0] == "acquired"
        p2_acquired_at = p2_acquired[1]
        assert p2_acquired_at >= p1_released_at - 0.05, (
            f"p2 acquired at {p2_acquired_at} before p1 released at {p1_released_at}"
        )
        # And p1 held at least ~0.5s
        assert p1_released_at - p1_acquired_at >= 0.4

    def test_sh_allows_concurrent_sh(self, tmp_path: Path) -> None:
        """Two shared locks on the same file should hold concurrently."""
        lock_path = tmp_path / "sh.lock"
        q1: mp.Queue = mp.Queue()
        q2: mp.Queue = mp.Queue()

        p1 = mp.Process(target=_child_shared, args=(str(lock_path), 0.4, q1))
        p2 = mp.Process(target=_child_shared, args=(str(lock_path), 0.4, q2))
        p1.start()
        p2.start()

        a1 = q1.get(timeout=2.0)
        a2 = q2.get(timeout=2.0)
        assert a1[0] == "acquired" and a2[0] == "acquired"

        # Both should be acquired within a small window (no serialization)
        gap = abs(a1[1] - a2[1])
        assert gap < 0.3, f"Shared locks serialized (gap={gap:.3f}s)"

        p1.join(timeout=5.0)
        p2.join(timeout=5.0)
        assert p1.exitcode == 0 and p2.exitcode == 0

    def test_context_manager_releases_on_exception(self, tmp_path: Path) -> None:
        """Lock must be released even when the with-block raises."""
        lock_path = tmp_path / "ex.lock"

        class BoomError(Exception):
            pass

        with pytest.raises(BoomError):
            with FileLock(lock_path, exclusive=True):
                raise BoomError("boom")

        # Second acquire must succeed immediately since prior released
        with FileLock(lock_path, exclusive=True, timeout=1.0):
            pass  # no hang

    def test_blocking_timeout(self, tmp_path: Path) -> None:
        """Second EX with a short timeout must raise LockTimeout."""
        lock_path = tmp_path / "to.lock"
        q1: mp.Queue = mp.Queue()
        q2: mp.Queue = mp.Queue()

        # p1 holds EX for 1.5s
        p1 = mp.Process(target=_child_exclusive, args=(str(lock_path), 1.5, q1))
        p1.start()
        assert q1.get(timeout=2.0)[0] == "acquired"

        # p2 tries EX with 0.3s timeout — should raise LockTimeout
        p2 = mp.Process(
            target=_child_try_ex_with_timeout, args=(str(lock_path), 0.3, q2)
        )
        p2.start()
        p2.join(timeout=5.0)
        assert p2.exitcode == 0

        outcome = q2.get(timeout=1.0)
        assert outcome[0] == "timeout", f"expected timeout, got {outcome}"
        # Elapsed should be ~0.3s (give generous upper bound for CI jitter)
        assert 0.2 <= outcome[1] <= 1.2

        p1.join(timeout=5.0)

    def test_creates_missing_lock_file(self, tmp_path: Path) -> None:
        """FileLock should create the lock file (and parent dir) if missing."""
        lock_path = tmp_path / "nested" / "deeper" / "x.lock"
        assert not lock_path.exists()
        with FileLock(lock_path, exclusive=True):
            assert lock_path.exists()

    def test_sh_blocks_ex(self, tmp_path: Path) -> None:
        """A held shared lock must block an exclusive acquire from another process."""
        lock_path = tmp_path / "shex.lock"
        q_sh: mp.Queue = mp.Queue()
        q_ex: mp.Queue = mp.Queue()

        p_sh = mp.Process(target=_child_shared, args=(str(lock_path), 0.5, q_sh))
        p_sh.start()
        assert q_sh.get(timeout=2.0)[0] == "acquired"
        sh_acquired_at = time.monotonic()

        # EX should wait for SH release
        p_ex = mp.Process(
            target=_child_try_ex_with_timeout, args=(str(lock_path), 2.0, q_ex)
        )
        p_ex.start()
        p_ex.join(timeout=5.0)
        assert p_ex.exitcode == 0

        outcome = q_ex.get(timeout=1.0)
        assert outcome[0] == "acquired"
        # EX should have waited at least ~0.3s (SH held 0.5s starting at sh_acquired_at)
        assert outcome[1] >= 0.3, f"EX acquired too quickly: {outcome[1]:.3f}s"

        p_sh.join(timeout=5.0)
        # sh_acquired_at only used to assert causality, not a hard equality
        del sh_acquired_at
