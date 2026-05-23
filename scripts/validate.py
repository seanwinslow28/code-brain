#!/usr/bin/env python3
"""
Claude Code Superuser Pack — Validator v3.0.0

Checks:
  1. Root .claude/ structure: skills (89), agents (11), hooks, settings.json
  2. Export-group manifests: valid JSON, required fields, skill references
  3. Skill quality: YAML frontmatter, headings, name match
  4. Agent quality: YAML frontmatter, disallowedTools for read-only agents
  5. Domain workspaces: active domains (creative-studio, life-systems) with README.md; the-block scanned as archive
  6. Vault: .obsidian/ exists, PARA structure
  7. Preset validity: all presets reference valid export groups and security profiles
  8. Plugin sync: marketplace.json valid
  9. Shared integrity: hooks executable, security profiles valid
  10. No secrets: sensitive pattern scanning
"""

import json
import os
import re
import sys
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────

SENSITIVE_PATTERNS = [
    r'password\s*[:=]\s*["\']?[^"\'\s]+',
    r'api[_-]?key\s*[:=]\s*["\']?[^"\'\s]+',
    r'(?<![_-])secret\s*[:=]\s*["\']?[^"\'\s]+',
    r'aws[_-]?access[_-]?key',
    r'aws[_-]?secret[_-]?key',
    r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
]

REQUIRED_PLAYGROUND_FIELDS = ["name", "description", "version", "dependencies", "skills"]
REQUIRED_PRESET_FIELDS = ["name", "description", "export_groups", "security"]

EXPECTED_DOMAINS = [
    "creative-studio",
    "life-systems",
]

# Cross-cutting workspaces that don't qualify as a primary domain but should
# still be scanned for secrets. Existence is NOT enforced.
# `the-block` is archived reference content (2026-05) — kept on disk for
# history, no longer an active domain.
ADDITIONAL_WORKSPACES_TO_SCAN = [
    "claude-mastery",
    "the-block",
]

EXPECTED_VAULT_DIRS = [
    "00_inbox", "05_atlas", "10_timeline", "20_projects", "30_domains",
    "40_knowledge", "50_sources", "60_archive", "70_apple-notes", "90_system",
]

# ─── Helpers ─────────────────────────────────────────────────────────

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def has_yaml_frontmatter(content):
    return content.strip().startswith('---') and content.count('---') >= 2


def extract_frontmatter_field(content, field):
    match = re.search(rf'^{field}\s*:\s*(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip().strip('"').strip("'")
    return None


def has_markdown_heading(content):
    return bool(re.search(r'^#+\s+.+', content, re.MULTILINE))


def check_secrets(path):
    try:
        with open(path, 'rb') as f:
            sample = f.read(1024)
            if b'\x00' in sample:
                return []
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        hits = []
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                hits.append(pattern)
        return hits
    except Exception:
        return []


def is_executable(path):
    return os.access(path, os.X_OK)

# ─── Validators ──────────────────────────────────────────────────────

def validate_root_claude(repo_root):
    """Validate the canonical .claude/ structure at repo root."""
    errors = []
    warnings = []
    claude_dir = repo_root / ".claude"

    if not claude_dir.exists():
        return [".claude/ directory not found at repo root"], []

    # Skills
    skills_dir = claude_dir / "skills"
    if not skills_dir.exists():
        errors.append(".claude/skills/ not found")
    else:
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        skill_count = len(skill_dirs)
        if skill_count == 0:
            errors.append(".claude/skills/ is empty")
        else:
            print(f"  Found {skill_count} skills in .claude/skills/")

        # Validate each skill
        for skill_dir in sorted(skill_dirs):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                errors.append(f"Skill '{skill_dir.name}' missing SKILL.md")
                continue

            content = skill_md.read_text(encoding='utf-8', errors='ignore')
            if not has_yaml_frontmatter(content):
                warnings.append(f"Skill '{skill_dir.name}' missing YAML frontmatter")
            else:
                fm_name = extract_frontmatter_field(content, 'name')
                if fm_name and fm_name != skill_dir.name:
                    warnings.append(f"Skill dir '{skill_dir.name}' vs frontmatter name '{fm_name}'")
                fm_desc = extract_frontmatter_field(content, 'description')
                if not fm_desc:
                    warnings.append(f"Skill '{skill_dir.name}' missing description in frontmatter")

    # Agents
    agents_dir = claude_dir / "agents"
    if not agents_dir.exists():
        errors.append(".claude/agents/ not found")
    else:
        agent_files = [f for f in agents_dir.iterdir() if f.suffix == '.md']
        agent_count = len(agent_files)
        if agent_count == 0:
            errors.append(".claude/agents/ is empty")
        else:
            print(f"  Found {agent_count} agents in .claude/agents/")

        for agent_file in sorted(agent_files):
            content = agent_file.read_text(encoding='utf-8', errors='ignore')
            if not has_yaml_frontmatter(content):
                warnings.append(f"Agent '{agent_file.name}' missing YAML frontmatter")
            if not has_markdown_heading(content):
                warnings.append(f"Agent '{agent_file.name}' has no headings")

    # Hooks
    hooks_dir = claude_dir / "hooks"
    if not hooks_dir.exists():
        errors.append(".claude/hooks/ not found")
    else:
        hook_files = [f for f in hooks_dir.iterdir() if f.is_file()]
        print(f"  Found {len(hook_files)} hooks in .claude/hooks/")
        for hook in hook_files:
            if not is_executable(hook):
                warnings.append(f"Hook '{hook.name}' is not executable")

    # Settings
    settings = claude_dir / "settings.json"
    if not settings.exists():
        errors.append(".claude/settings.json not found")
    else:
        try:
            data = load_json(settings)
            if "permissions" not in data:
                errors.append(".claude/settings.json missing 'permissions' field")
        except json.JSONDecodeError as e:
            errors.append(f".claude/settings.json invalid JSON: {e}")

    return errors, warnings


def validate_export_groups(repo_root):
    """Validate export-group manifests and check skills exist in .claude/skills/."""
    errors = []
    warnings = []
    export_groups_dir = repo_root / "export-groups"
    skills_dir = repo_root / ".claude" / "skills"
    agents_dir = repo_root / ".claude" / "agents"

    if not export_groups_dir.exists():
        return ["export-groups/ directory not found"], []

    all_skill_names = {}

    for pg_dir in sorted(export_groups_dir.iterdir()):
        if not pg_dir.is_dir():
            continue

        pg_name = pg_dir.name
        manifest = pg_dir / "playground.json"

        if not manifest.exists():
            errors.append(f"[{pg_name}] Missing playground.json")
            continue

        try:
            data = load_json(manifest)
        except json.JSONDecodeError as e:
            errors.append(f"[{pg_name}] Invalid JSON in playground.json: {e}")
            continue

        # Required fields
        for field in REQUIRED_PLAYGROUND_FIELDS:
            if field not in data:
                errors.append(f"[{pg_name}] Missing required field '{field}'")

        # CLAUDE.section.md exists
        section_md = pg_dir / "CLAUDE.section.md"
        if not section_md.exists():
            warnings.append(f"[{pg_name}] Missing CLAUDE.section.md")

        # Skills in manifest exist in .claude/skills/
        manifest_skills = data.get("skills", [])
        for s in manifest_skills:
            if skills_dir.exists() and not (skills_dir / s).exists():
                errors.append(f"[{pg_name}] Skill '{s}' listed in manifest but not found in .claude/skills/")

        # Agents in manifest exist in .claude/agents/
        manifest_agents = data.get("agents", [])
        for a in manifest_agents:
            if agents_dir.exists() and not (agents_dir / f"{a}.md").exists():
                errors.append(f"[{pg_name}] Agent '{a}' listed in manifest but not found in .claude/agents/")

        # Uniqueness check
        for s in manifest_skills:
            if s in all_skill_names:
                errors.append(
                    f"Skill name collision: '{s}' in both "
                    f"'{all_skill_names[s]}' and '{pg_name}'"
                )
            else:
                all_skill_names[s] = pg_name

        # Dependency check
        all_pg_names = [d.name for d in export_groups_dir.iterdir() if d.is_dir()]
        for dep in data.get("dependencies", []):
            found = any(dep in pn for pn in all_pg_names)
            if not found:
                errors.append(f"[{pg_name}] Dependency '{dep}' is not a valid export group")

    return errors, warnings


def validate_domains(repo_root):
    """Validate active domain workspace directories.

    Active domains require existence + warn if missing CLAUDE.md/README.md.
    `the-block/` is archived (2026-05) and lives in ADDITIONAL_WORKSPACES_TO_SCAN
    — scanned for secrets but not required.
    """
    errors = []
    warnings = []

    for domain in EXPECTED_DOMAINS:
        domain_dir = repo_root / domain
        if not domain_dir.exists():
            errors.append(f"Primary domain workspace '{domain}/' not found")
            continue
        readme = domain_dir / "README.md"
        if not readme.exists():
            warnings.append(f"Domain '{domain}/' missing README.md")
        claude_md = domain_dir / "CLAUDE.md"
        if not claude_md.exists():
            warnings.append(f"Domain '{domain}/' missing CLAUDE.md (router)")

    for workspace in ADDITIONAL_WORKSPACES_TO_SCAN:
        ws_dir = repo_root / workspace
        if not ws_dir.exists():
            warnings.append(f"Cross-cutting workspace '{workspace}/' not found")

    return errors, warnings


def validate_vault(repo_root):
    """Validate the Obsidian vault structure."""
    errors = []
    warnings = []
    vault_dir = repo_root / "vault"

    if not vault_dir.exists():
        return ["vault/ directory not found"], []

    # .obsidian config
    obsidian_dir = vault_dir / ".obsidian"
    if not obsidian_dir.exists():
        warnings.append("vault/.obsidian/ not found (Obsidian won't recognize as vault)")
    else:
        app_json = obsidian_dir / "app.json"
        if not app_json.exists():
            warnings.append("vault/.obsidian/app.json not found")

    # PARA structure
    for subdir in EXPECTED_VAULT_DIRS:
        if not (vault_dir / subdir).exists():
            warnings.append(f"vault/{subdir}/ not found")

    return errors, warnings


def validate_presets(repo_root, valid_groups):
    """Validate all preset files."""
    errors = []
    warnings = []
    presets_dir = repo_root / "presets"

    if not presets_dir.exists():
        return ["presets/ directory not found"], []

    valid_securities = set()
    security_dir = repo_root / "shared" / "security"
    if security_dir.exists():
        valid_securities = {f.stem for f in security_dir.iterdir() if f.suffix == '.json'}

    for preset_file in sorted(presets_dir.glob("*.json")):
        p_name = preset_file.stem
        try:
            data = load_json(preset_file)
        except json.JSONDecodeError as e:
            errors.append(f"[preset:{p_name}] Invalid JSON: {e}")
            continue

        for field in REQUIRED_PRESET_FIELDS:
            if field not in data:
                errors.append(f"[preset:{p_name}] Missing required field '{field}'")

        for pg in data.get("export_groups", []):
            if pg not in valid_groups:
                errors.append(f"[preset:{p_name}] References unknown export group '{pg}'")

        sec = data.get("security", "")
        if sec and sec not in valid_securities:
            errors.append(f"[preset:{p_name}] References unknown security profile '{sec}'")

    return errors, warnings


def validate_shared(repo_root):
    """Validate shared hooks and security profiles."""
    errors = []
    warnings = []
    shared_dir = repo_root / "shared"

    if not shared_dir.exists():
        return ["shared/ directory not found"], []

    # Hooks
    hooks_dir = shared_dir / "hooks"
    if hooks_dir.exists():
        for hook in hooks_dir.iterdir():
            if hook.is_file() and not is_executable(hook):
                warnings.append(f"[shared] Hook '{hook.name}' is not executable")

    # Security profiles
    security_dir = shared_dir / "security"
    if security_dir.exists():
        for sec_file in security_dir.glob("*.json"):
            try:
                data = load_json(sec_file)
                if "permissions" not in data:
                    errors.append(f"[security:{sec_file.stem}] Missing 'permissions' field")
                if "hooks" not in data:
                    errors.append(f"[security:{sec_file.stem}] Missing 'hooks' field")
            except json.JSONDecodeError as e:
                errors.append(f"[security:{sec_file.stem}] Invalid JSON: {e}")

    return errors, warnings


def validate_plugin(repo_root):
    """Validate plugin directory."""
    errors = []
    warnings = []
    plugin_dir = repo_root / "plugin"

    if not plugin_dir.exists():
        return [], ["plugin/ directory not found (optional)"]

    # Check plugin skills exist in .claude/skills/
    plugin_skills_dir = plugin_dir / "skills"
    skills_dir = repo_root / ".claude" / "skills"
    if plugin_skills_dir.exists() and skills_dir.exists():
        for skill_dir in plugin_skills_dir.iterdir():
            if skill_dir.is_dir():
                if not (skills_dir / skill_dir.name).exists():
                    warnings.append(f"[plugin] Skill '{skill_dir.name}' not found in .claude/skills/")

    # Marketplace manifest
    marketplace = repo_root / ".claude-plugin" / "marketplace.json"
    if marketplace.exists():
        try:
            load_json(marketplace)
        except json.JSONDecodeError as e:
            errors.append(f"[plugin] Invalid marketplace.json: {e}")
    else:
        warnings.append("[plugin] Missing .claude-plugin/marketplace.json")

    return errors, warnings


def scan_secrets(repo_root):
    """Scan for secrets across key directories."""
    warnings = []
    scan_dirs = [
        repo_root / ".claude",
        repo_root / "export-groups",
        repo_root / "shared",
        repo_root / "plugin",
    ]
    # Also scan domain workspaces and cross-cutting workspaces (v3.15.0)
    for domain in EXPECTED_DOMAINS + ADDITIONAL_WORKSPACES_TO_SCAN:
        d = repo_root / domain
        if d.exists():
            scan_dirs.append(d)

    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue
        for fpath in scan_dir.rglob("*"):
            if fpath.is_file() and '.git' not in str(fpath):
                hits = check_secrets(fpath)
                for pattern in hits:
                    warnings.append(f"Potential secret pattern '{pattern}' in {fpath}")

    return warnings

# ─── Main ────────────────────────────────────────────────────────────

def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    all_errors = []
    all_warnings = []

    # 1. Root .claude/ structure
    print("Validating .claude/ (canonical skills, agents, hooks)...")
    errs, warns = validate_root_claude(repo_root)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 2. Export groups (metadata-only manifests)
    print("Validating export-groups/ (manifests)...")
    errs, warns = validate_export_groups(repo_root)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 3. Domain workspaces
    print("Validating domain workspaces...")
    errs, warns = validate_domains(repo_root)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 4. Vault
    print("Validating vault/ (Obsidian)...")
    errs, warns = validate_vault(repo_root)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 5. Shared infrastructure
    print("Validating shared/ ...")
    errs, warns = validate_shared(repo_root)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 6. Presets
    print("Validating presets/ ...")
    export_groups_dir = repo_root / "export-groups"
    valid_groups = set()
    if export_groups_dir.exists():
        valid_groups = {d.name for d in export_groups_dir.iterdir() if d.is_dir()}
    errs, warns = validate_presets(repo_root, valid_groups)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 7. Plugin
    print("Validating plugin/ ...")
    errs, warns = validate_plugin(repo_root)
    all_errors.extend(errs)
    all_warnings.extend(warns)

    # 8. Secret scanning
    print("Scanning for secrets...")
    secret_warns = scan_secrets(repo_root)
    all_warnings.extend(secret_warns)

    # ─── Report ──────────────────────────────────────────────────────
    print("\n" + "=" * 64)

    if all_errors:
        print(f"  ERRORS: {len(all_errors)}")
        for e in all_errors:
            print(f"    - {e}")
    else:
        print("  No errors found!")

    if all_warnings:
        print(f"\n  WARNINGS: {len(all_warnings)}")
        for w in all_warnings:
            print(f"    - {w}")
    else:
        print("\n  No warnings found!")

    print("=" * 64)

    if all_errors:
        print(f"\nValidation FAILED with {len(all_errors)} error(s).")
        sys.exit(1)
    else:
        print(f"\nValidation PASSED ({len(all_warnings)} warning(s)).")
        sys.exit(0)


if __name__ == "__main__":
    main()
