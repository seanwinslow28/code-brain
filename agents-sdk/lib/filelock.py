"""fcntl-based advisory file lock with exclusive/shared + timeout support.

Why: vault writers (flush.py, vault_synthesizer.py, knowledge_lint.py) must
serialize on `vault/daily/.lock` / `vault/knowledge/.lock`. Python's stdlib
provides `fcntl.flock` but not a context manager with LOCK_EX + LOCK_SH +
timeout semantics. This module is that wrapper.

POSIX `flock` is advisory and per-file-descriptor. Each process opens its own
fd on the same lock file; the kernel tracks whose fd holds the lock.
"""

from __future__ import annotations

import errno
import fcntl
import time
from pathlib import Path
from types import TracebackType
from typing import IO


class LockTimeout(Exception):
    """Raised when a FileLock acquisition exceeds its timeout."""


class FileLock:
    """Context-manager file lock.

    Args:
        path: Path to the lock file. Created (with parent dirs) if missing.
        exclusive: True → LOCK_EX (writer). False → LOCK_SH (reader).
        timeout: Max seconds to wait. None (default) blocks indefinitely.
            If reached, raises LockTimeout and the file is released.

    Usage:
        with FileLock(Path("vault/daily/.lock"), exclusive=True):
            ...

        with FileLock(path, exclusive=False):  # shared reader
            ...
    """

    _POLL_INTERVAL = 0.05  # seconds between non-blocking retries under timeout

    def __init__(
        self,
        path: Path,
        *,
        exclusive: bool = True,
        timeout: float | None = None,
    ) -> None:
        self.path = Path(path)
        self.exclusive = exclusive
        self.timeout = timeout
        self._fh: IO[bytes] | None = None

    def __enter__(self) -> FileLock:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Open for read+write so both modes can share the same file.
        self._fh = open(self.path, "a+b")

        op = fcntl.LOCK_EX if self.exclusive else fcntl.LOCK_SH

        if self.timeout is None:
            # Blocking acquire.
            try:
                fcntl.flock(self._fh.fileno(), op)
            except Exception:
                self._fh.close()
                self._fh = None
                raise
            return self

        # Non-blocking poll loop until timeout.
        deadline = time.monotonic() + self.timeout
        while True:
            try:
                fcntl.flock(self._fh.fileno(), op | fcntl.LOCK_NB)
                return self
            except OSError as exc:
                if exc.errno not in (errno.EAGAIN, errno.EACCES, errno.EWOULDBLOCK):
                    self._fh.close()
                    self._fh = None
                    raise
                if time.monotonic() >= deadline:
                    self._fh.close()
                    self._fh = None
                    raise LockTimeout(
                        f"Timed out after {self.timeout:.3f}s acquiring "
                        f"{'exclusive' if self.exclusive else 'shared'} "
                        f"lock on {self.path}"
                    ) from exc
                time.sleep(self._POLL_INTERVAL)

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._fh is None:
            return
        try:
            fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
        finally:
            self._fh.close()
            self._fh = None
