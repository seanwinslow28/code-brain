#!/usr/bin/env python3
"""Render the registered claim-6 launchd plist from its unarmed template."""

from __future__ import annotations

import argparse
import plistlib
from pathlib import Path
from typing import Mapping

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 support
    import tomli as tomllib

from agents.claim6_drill import DrillConfig, validate_registration


SDK_ROOT = Path(__file__).parent.parent
DEFAULT_TEMPLATE = Path(__file__).parent / "com.sean.agent.claim6-drill.plist.template"


def render_claim6_plist(
    *, template_path: Path, output_path: Path, config: Mapping[str, object]
) -> None:
    """Render and validate one registered monthly plist."""
    registered = DrillConfig.from_mapping(dict(config))
    validate_registration(registered)
    rendered = template_path.read_text(encoding="utf-8")
    rendered = rendered.replace("__CLAIM6_DRILL_DAY__", str(registered.day_of_month))
    rendered = rendered.replace("__CLAIM6_LAUNCHD_LABEL__", registered.launchd_label)
    data = rendered.encode("utf-8")
    plistlib.loads(data)  # refuse invalid XML before touching the install target
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render registered claim-6 plist")
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--config", type=Path, default=SDK_ROOT / "config.toml")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--check-enabled", action="store_true")
    args = parser.parse_args()

    with args.config.open("rb") as stream:
        raw = tomllib.load(stream)["agents"]["claim6_drill"]
    if args.check_enabled:
        raise SystemExit(0 if raw.get("schedule_enabled", False) else 1)
    if args.output is None:
        parser.error("output is required unless --check-enabled is used")
    render_claim6_plist(
        template_path=args.template,
        output_path=args.output,
        config=raw,
    )


if __name__ == "__main__":
    main()
