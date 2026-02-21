# Claude Code Superuser Pack - Composable Installer v3.0.0 (Windows)
# Reads export-group manifests for skill/agent names, copies from canonical .claude/ sources

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$TargetDir,

    [Parameter()]
    [string]$Preset,

    [Parameter()]
    [ValidateSet("standard", "enterprise")]
    [string]$Security = "standard",

    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ExtraGroups,

    [switch]$List,
    [switch]$Help
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $ScriptDir

# ─── Help ────────────────────────────────────────────────────────────
if ($Help) {
    Write-Host @"
Claude Code Superuser Pack Installer v3.0.0

Usage:
  install.ps1 <target-dir> -Preset <name>
  install.ps1 <target-dir> <group> [<group>...] [-Security <profile>]
  install.ps1 <target-dir> -Preset <name> <extra-group> [...]

Examples:
  install.ps1 .\my-project -Preset starter
  install.ps1 .\my-project -Preset power
  install.ps1 .\my-project pm-workflows remotion-mastery
  install.ps1 .\my-project pm-workflows -Security enterprise
  install.ps1 -List

Options:
  -Preset <name>       Use a preset: starter, power, enterprise, creative
  -Security <profile>  Security profile: standard (default), enterprise
  -List                List available export groups and presets
  -Help                Show this help
"@
    exit 0
}

# ─── List ────────────────────────────────────────────────────────────
if ($List) {
    Write-Host "Available export groups:" -ForegroundColor Cyan
    Get-ChildItem (Join-Path $RepoDir "export-groups") -Directory | ForEach-Object {
        $manifest = Join-Path $_.FullName "playground.json"
        if (Test-Path $manifest) {
            $data = Get-Content $manifest -Raw | ConvertFrom-Json
            Write-Host ("  {0,-28} {1}" -f $_.Name, $data.description)
        }
    }
    Write-Host ""
    Write-Host "Available presets:" -ForegroundColor Cyan
    Get-ChildItem (Join-Path $RepoDir "presets") -Filter "*.json" | ForEach-Object {
        $data = Get-Content $_.FullName -Raw | ConvertFrom-Json
        Write-Host ("  {0,-16} {1}" -f $data.name, $data.description)
    }
    exit 0
}

# ─── Validate Target ─────────────────────────────────────────────────
if (-not (Test-Path $TargetDir)) {
    Write-Error "Target directory does not exist: $TargetDir"
    exit 1
}

# ─── Resolve Preset ──────────────────────────────────────────────────
$Groups = @()

if ($Preset) {
    $PresetFile = Join-Path $RepoDir "presets\$Preset.json"
    if (-not (Test-Path $PresetFile)) {
        Write-Error "Preset '$Preset' not found. Available: starter, power, enterprise, creative"
        exit 1
    }
    $presetData = Get-Content $PresetFile -Raw | ConvertFrom-Json
    $Groups = @($presetData.export_groups)
    $Security = $presetData.security
}

# Merge extra groups
if ($ExtraGroups) {
    foreach ($pg in $ExtraGroups) {
        if ($Groups -notcontains $pg) {
            $Groups += $pg
        }
    }
}

if ($Groups.Count -eq 0) {
    Write-Error "Specify -Preset <name> and/or one or more export group names."
    exit 1
}

# ─── Validate Export Groups ──────────────────────────────────────────
foreach ($pg in $Groups) {
    $pgDir = Join-Path $RepoDir "export-groups\$pg"
    if (-not (Test-Path $pgDir)) {
        Write-Error "Export group '$pg' not found in $RepoDir\export-groups\"
        exit 1
    }
}

# ─── Validate Security Profile ───────────────────────────────────────
$SecurityFile = Join-Path $RepoDir "shared\security\$Security.json"
if (-not (Test-Path $SecurityFile)) {
    Write-Error "Security profile '$Security' not found. Available: standard, enterprise"
    exit 1
}
$securityData = Get-Content $SecurityFile -Raw | ConvertFrom-Json

# ─── Resolve Dependencies ────────────────────────────────────────────
Write-Host "Resolving export groups..." -ForegroundColor Cyan
foreach ($pg in $Groups) {
    $pgJson = Join-Path $RepoDir "export-groups\$pg\playground.json"
    if (Test-Path $pgJson) {
        $pgData = Get-Content $pgJson -Raw | ConvertFrom-Json
        foreach ($dep in $pgData.dependencies) {
            $found = $false
            foreach ($existing in $Groups) {
                if ($existing -like "*$dep*") { $found = $true; break }
            }
            if (-not $found) {
                Write-Host "  Warning: '$pg' depends on '$dep' which is not in the install list." -ForegroundColor Yellow
            }
        }
    }
}

# ─── Collect Skill and Agent Names from Manifests ────────────────────
$SkillNames = @()
$AgentNames = @()

foreach ($pg in $Groups) {
    $pgJson = Join-Path $RepoDir "export-groups\$pg\playground.json"
    if (Test-Path $pgJson) {
        $pgData = Get-Content $pgJson -Raw | ConvertFrom-Json
        foreach ($s in $pgData.skills) { $SkillNames += $s }
        foreach ($a in $pgData.agents) { $AgentNames += $a }
    }
}

$SkillNames = $SkillNames | Select-Object -Unique | Sort-Object
$AgentNames = $AgentNames | Select-Object -Unique | Sort-Object

# ─── Begin Installation ──────────────────────────────────────────────
Write-Host ""
Write-Host "Installing to $TargetDir" -ForegroundColor Green
Write-Host "  Export groups: $($Groups -join ', ')"
Write-Host "  Security:      $Security"
Write-Host "  Skills:        $($SkillNames.Count)"
Write-Host "  Agents:        $($AgentNames.Count)"
Write-Host ""

$ClaudeDir = Join-Path $TargetDir ".claude"
New-Item -ItemType Directory -Path (Join-Path $ClaudeDir "skills") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $ClaudeDir "agents") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $ClaudeDir "hooks") -Force | Out-Null

# ─── Copy Skills from Canonical Source ───────────────────────────────
$skillsCopied = 0
foreach ($skill in $SkillNames) {
    $src = Join-Path $RepoDir ".claude\skills\$skill"
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $ClaudeDir "skills\$skill") -Recurse -Force
        $skillsCopied++
    } else {
        Write-Host "  Warning: Skill '$skill' not found in .claude/skills/" -ForegroundColor Yellow
    }
}
Write-Host "  Skills: $skillsCopied copied" -ForegroundColor Green

# ─── Copy Agents from Canonical Source ───────────────────────────────
$agentsCopied = 0
foreach ($agent in $AgentNames) {
    $src = Join-Path $RepoDir ".claude\agents\$agent.md"
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $ClaudeDir "agents\$agent.md") -Force
        $agentsCopied++
    } else {
        Write-Host "  Warning: Agent '$agent' not found in .claude/agents/" -ForegroundColor Yellow
    }
}
Write-Host "  Agents: $agentsCopied copied" -ForegroundColor Green

# ─── Copy Hooks from Security Profile ───────────────────────────────
$hooksCopied = 0
$hookFiles = @()
foreach ($eventType in @("preToolUse", "postToolUse", "postStop")) {
    $eventHooks = $securityData.hooks.$eventType
    if ($eventHooks) {
        foreach ($h in $eventHooks) {
            $cmd = $h.command
            if ($cmd -match "[/\\]([^/\\]+)$") {
                $hookFiles += $Matches[1]
            }
        }
    }
}
$hookFiles = $hookFiles | Select-Object -Unique

foreach ($hookFile in $hookFiles) {
    $src = Join-Path $RepoDir "shared\hooks\$hookFile"
    if (Test-Path $src) {
        Copy-Item $src (Join-Path $ClaudeDir "hooks\$hookFile") -Force
        $hooksCopied++
    }
}
Write-Host "  Hooks:  $hooksCopied copied" -ForegroundColor Green

# ─── Compose settings.json ───────────────────────────────────────────
$settings = @{
    permissions = $securityData.permissions
    hooks = $securityData.hooks
}
$settings | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $ClaudeDir "settings.json") -Encoding UTF8
Write-Host "  Generated .claude/settings.json" -ForegroundColor Green

# ─── Compose CLAUDE.md ───────────────────────────────────────────────
$claudeMd = @"
# CLAUDE.md

## Non-Negotiable Rules

1. **Plan Mode vs Extended Thinking**: Plan Mode = double ``Shift+Tab`` or ``/plan``. Extended Thinking = single ``Tab``. Never confuse the two.
2. **Agent tool restrictions**: Use ``disallowedTools`` (deny-list), not allow-list.
3. **Hooks enforce; subagents judge**: PreToolUse for binary allow/deny; subagents for subjective reviews.
4. **Hook blocking**: Exit code **2** to deny (not 0 or 1).
5. **Settings precedence** (highest wins): Enterprise managed > Project local > Project settings > User settings
6. **Permission evaluation** (first match wins): Deny > Ask > Allow

---

"@

foreach ($pg in $Groups) {
    $section = Join-Path $RepoDir "export-groups\$pg\CLAUDE.section.md"
    if (Test-Path $section) {
        $claudeMd += (Get-Content $section -Raw)
        $claudeMd += "`n`n---`n`n"
    }
}

$claudeMd += @"
## Configuration

- **Security profile**: $Security
- **Installed export groups**: $($Groups -join ', ')
- **Settings**: ``.claude/settings.json`` - permissions, hooks
- **Local overrides**: Copy ``.claude/settings.local.json.example`` to ``.claude/settings.local.json``

Installed by Claude Code Superuser Pack v3.0.0
"@

$claudeMd | Set-Content (Join-Path $TargetDir "CLAUDE.md") -Encoding UTF8
Write-Host "  Generated CLAUDE.md" -ForegroundColor Green

# ─── settings.local.json.example ─────────────────────────────────────
@'
{
  "// NOTE": "Rename this file to settings.local.json for local-only overrides.",
  "// INFO": "This file is gitignored and never committed.",
  "permissions": {
    "rules": []
  }
}
'@ | Set-Content (Join-Path $ClaudeDir "settings.local.json.example") -Encoding UTF8
Write-Host "  Created .claude/settings.local.json.example" -ForegroundColor Green

# ─── .gitignore ──────────────────────────────────────────────────────
$gitignorePath = Join-Path $TargetDir ".gitignore"
$gitignoreLines = ".claude/settings.local.json`n.claude/tool-use.log"

if (Test-Path $gitignorePath) {
    $content = Get-Content $gitignorePath -Raw
    if ($content -notmatch "settings\.local\.json") {
        Add-Content $gitignorePath "`n# Claude Code Superuser Pack`n$gitignoreLines"
        Write-Host "  Merged .gitignore entries" -ForegroundColor Green
    }
} else {
    "# Claude Code Superuser Pack`n$gitignoreLines" | Set-Content $gitignorePath -Encoding UTF8
    Write-Host "  Created .gitignore" -ForegroundColor Green
}

# ─── Report ──────────────────────────────────────────────────────────
Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Installed $skillsCopied skills, $agentsCopied agents, $hooksCopied hooks"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Review $(Join-Path $TargetDir 'CLAUDE.md')"
Write-Host "  2. Review $(Join-Path $TargetDir '.claude\settings.json')"
Write-Host "  3. Optionally create $(Join-Path $TargetDir '.claude\settings.local.json') for local overrides"
Write-Host "  4. Start using Claude Code!"
