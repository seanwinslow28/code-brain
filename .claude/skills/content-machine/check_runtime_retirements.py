#!/usr/bin/env python3
"""Check the Content Machine operating surface for retired instructions.

The registry is the policy. This module is the single scanner used both at
resolution time and by the Sunday Knowledge Lint job.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

REGISTRY_RELATIVE_PATH = Path(".claude/skills/content-machine/runtime-retirements.toml")
TEXT_SUFFIXES = {".json", ".md", ".py", ".toml", ".txt", ".yaml", ".yml"}


class RegistryError(ValueError):
    """The registry cannot be scanned safely or completely."""


@dataclass(frozen=True)
class Finding:
    retirement_id: str
    retirement_name: str
    source: str
    path: str
    line: int
    pattern: str


@dataclass(frozen=True)
class ScanResult:
    retirements: int
    files_scanned: int
    patterns_checked: int
    findings: tuple[Finding, ...]

    @property
    def clean(self) -> bool:
        return not self.findings

    def to_dict(self) -> dict:
        return {
            "status": "clean" if self.clean else "findings",
            "retirements": self.retirements,
            "files_scanned": self.files_scanned,
            "patterns_checked": self.patterns_checked,
            "findings": [asdict(finding) for finding in self.findings],
        }


def _repo_path(repo_root: Path, relative: str) -> Path:
    root = repo_root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise RegistryError(f"scan path escapes the repository: {relative}") from exc
    return candidate


def _scan_files(repo_root: Path, scan_paths: list[str], registry_path: Path) -> list[Path]:
    files: set[Path] = set()
    for relative in scan_paths:
        target = _repo_path(repo_root, relative)
        if not target.exists():
            raise RegistryError(f"scan path does not exist: {relative}")
        if target.is_file():
            files.add(target)
            continue
        for candidate in target.rglob("*"):
            if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
                files.add(candidate.resolve())
    files.discard(registry_path.resolve())
    return sorted(files)


def _allowed(entry: dict, relative_path: str, line: str, pattern: str) -> bool:
    for allowance in entry.get("allow", []):
        path_pattern = allowance.get("path")
        line_contains = allowance.get("line_contains")
        allowed_pattern = allowance.get("pattern")
        if not isinstance(path_pattern, str) or not isinstance(line_contains, str):
            raise RegistryError(
                f"{entry['id']}: every allow entry needs path and line_contains strings"
            )
        if allowed_pattern is not None and allowed_pattern != pattern:
            continue
        if fnmatch.fnmatch(relative_path, path_pattern) and line_contains in line:
            return True
    return False


def scan_registry(
    repo_root: Path,
    registry_path: Path | None = None,
) -> ScanResult:
    repo_root = repo_root.resolve()
    registry_path = (registry_path or repo_root / REGISTRY_RELATIVE_PATH).resolve()
    if not registry_path.is_file():
        raise RegistryError(f"registry does not exist: {registry_path}")

    with registry_path.open("rb") as handle:
        document = tomllib.load(handle)
    if document.get("version") != 1:
        raise RegistryError("registry version must be 1")

    entries = document.get("retirement")
    if not isinstance(entries, list) or not entries:
        raise RegistryError("registry must contain at least one [[retirement]] entry")

    seen_ids: set[str] = set()
    scanned_files: set[Path] = set()
    findings: list[Finding] = []
    patterns_checked = 0

    for entry in entries:
        retirement_id = entry.get("id")
        retirement_name = entry.get("name")
        source = entry.get("source")
        scan_paths = entry.get("scan_paths")
        patterns = entry.get("pattern")
        if not all(isinstance(value, str) and value for value in (retirement_id, retirement_name, source)):
            raise RegistryError("every retirement needs non-empty id, name, and source strings")
        if retirement_id in seen_ids:
            raise RegistryError(f"duplicate retirement id: {retirement_id}")
        seen_ids.add(retirement_id)
        if not isinstance(scan_paths, list) or not scan_paths or not all(
            isinstance(path, str) and path for path in scan_paths
        ):
            raise RegistryError(f"{retirement_id}: scan_paths must be a non-empty string list")
        if not isinstance(patterns, list) or not patterns:
            raise RegistryError(f"{retirement_id}: at least one [[retirement.pattern]] is required")

        files = _scan_files(repo_root, scan_paths, registry_path)
        scanned_files.update(files)
        for pattern_entry in patterns:
            literal = pattern_entry.get("literal") if isinstance(pattern_entry, dict) else None
            if not isinstance(literal, str) or not literal:
                raise RegistryError(f"{retirement_id}: every pattern needs a non-empty literal")
            patterns_checked += 1
            for file_path in files:
                relative_path = file_path.relative_to(repo_root).as_posix()
                try:
                    lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
                except OSError as exc:
                    raise RegistryError(f"cannot read scan target: {relative_path}") from exc
                for line_number, line in enumerate(lines, start=1):
                    if literal not in line:
                        continue
                    if _allowed(entry, relative_path, line, literal):
                        continue
                    findings.append(
                        Finding(
                            retirement_id=retirement_id,
                            retirement_name=retirement_name,
                            source=source,
                            path=relative_path,
                            line=line_number,
                            pattern=literal,
                        )
                    )

    return ScanResult(
        retirements=len(entries),
        files_scanned=len(scanned_files),
        patterns_checked=patterns_checked,
        findings=tuple(findings),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    try:
        result = scan_registry(args.repo_root, args.registry)
    except (OSError, tomllib.TOMLDecodeError, RegistryError) as exc:
        if args.as_json:
            print(json.dumps({"status": "error", "error": str(exc)}))
        else:
            print(f"Runtime retirement check error: {exc}", file=sys.stderr)
        return 2

    if args.as_json:
        print(json.dumps(result.to_dict(), sort_keys=True))
    elif result.clean:
        print(
            "Runtime retirement check: clean "
            f"({result.retirements} retirements, {result.files_scanned} files, "
            f"{result.patterns_checked} patterns)."
        )
    else:
        print(f"Runtime retirement check: {len(result.findings)} finding(s).")
        for finding in result.findings:
            print(
                f"- {finding.path}:{finding.line}: {finding.retirement_name} "
                f"still matches {finding.pattern!r} ({finding.source})"
            )
    return 0 if result.clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
