#!/usr/bin/env python3
"""
Validate Claude Code Superuser Pack structure and content.
Checks JSON validity, required files, markdown headings, and no secrets.
"""

import json
import os
import re
import sys
from pathlib import Path

# Sensitive patterns that should not appear in committed files
SENSITIVE_PATTERNS = [
    r'password\s*[:=]\s*["\']?[^"\'\s]+',
    r'api[_-]?key\s*[:=]\s*["\']?[^"\'\s]+',
    r'secret\s*[:=]\s*["\']?[^"\'\s]+',
    r'aws[_-]?access[_-]?key',
    r'aws[_-]?secret[_-]?key',
    r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
]

def validate_json(file_path):
    """Validate that a JSON file is valid."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        return True, None
    except json.JSONDecodeError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def has_markdown_headings(file_path):
    """Check if markdown file has at least one heading."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for markdown headings (# ## ### etc.)
            if re.search(r'^#+\s+.+', content, re.MULTILINE):
                return True
            return False
    except Exception:
        return False

def check_for_secrets(file_path):
    """Check if file contains sensitive patterns."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for pattern in SENSITIVE_PATTERNS:
                if re.search(pattern, content, re.IGNORECASE):
                    return True, pattern
        return False, None
    except Exception:
        return False, None

def validate_pack(pack_dir, check_required_files=True):
    """Validate a single pack directory."""
    errors = []
    warnings = []
    
    pack_dir = Path(pack_dir)
    if not pack_dir.exists():
        return [f"Pack directory does not exist: {pack_dir}"], []
    
    # Check required files (skip for plugin directory)
    if check_required_files:
        required_files = [
            pack_dir / "CLAUDE.md",
            pack_dir / ".gitignore",
            pack_dir / ".claude" / "settings.json",
            pack_dir / ".claude" / "settings.local.json.example",
        ]
        
        for req_file in required_files:
            if not req_file.exists():
                errors.append(f"Missing required file: {req_file}")
    
    # Validate JSON files
    json_files = list(pack_dir.rglob("*.json"))
    for json_file in json_files:
        # Skip node_modules and other common exclusions
        if 'node_modules' in str(json_file) or '.git' in str(json_file):
            continue
        
        is_valid, error = validate_json(json_file)
        if not is_valid:
            errors.append(f"Invalid JSON in {json_file}: {error}")
    
    # Check markdown files have headings
    md_files = list(pack_dir.rglob("*.md"))
    for md_file in md_files:
        if '.git' in str(md_file):
            continue
        
        if not has_markdown_headings(md_file):
            warnings.append(f"Markdown file has no headings: {md_file}")
    
    # Check for secrets
    all_files = list(pack_dir.rglob("*"))
    for file_path in all_files:
        if file_path.is_file() and '.git' not in str(file_path):
            # Skip binary files
            try:
                with open(file_path, 'rb') as f:
                    content = f.read(1024)
                    # Check if it's likely text
                    if b'\x00' in content:
                        continue
            except Exception:
                continue
            
            has_secret, pattern = check_for_secrets(file_path)
            if has_secret:
                warnings.append(f"Potential secret pattern '{pattern}' found in {file_path}")
    
    return errors, warnings

def main():
    """Main validation function."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    packs_dir = repo_root / "packs"
    
    if not packs_dir.exists():
        print(f"Error: packs directory not found at {packs_dir}")
        sys.exit(1)
    
    all_errors = []
    all_warnings = []
    
    # Validate each pack
    for pack_name in ["starter", "power", "enterprise"]:
        pack_path = packs_dir / pack_name
        if pack_path.exists():
            print(f"\nValidating {pack_name} pack...")
            errors, warnings = validate_pack(pack_path)
            all_errors.extend([f"[{pack_name}] {e}" for e in errors])
            all_warnings.extend([f"[{pack_name}] {w}" for w in warnings])
        else:
            all_errors.append(f"Pack directory missing: {pack_path}")
    
    # Validate plugin directory (skip required files check)
    plugin_dir = repo_root / "plugin"
    if plugin_dir.exists():
        print(f"\nValidating plugin directory...")
        errors, warnings = validate_pack(plugin_dir, check_required_files=False)
        all_errors.extend([f"[plugin] {e}" for e in errors])
        all_warnings.extend([f"[plugin] {w}" for w in warnings])
    
    # Print results
    print("\n" + "="*60)
    if all_errors:
        print(f"❌ Found {len(all_errors)} error(s):")
        for error in all_errors:
            print(f"  - {error}")
    else:
        print("✅ No errors found!")
    
    if all_warnings:
        print(f"\n⚠️  Found {len(all_warnings)} warning(s):")
        for warning in all_warnings:
            print(f"  - {warning}")
    else:
        print("\n✅ No warnings found!")
    
    print("="*60)
    
    if all_errors:
        sys.exit(1)
    else:
        print("\n✅ Validation passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
