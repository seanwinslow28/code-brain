# Install a Claude Code Superuser Pack into a target project

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetDir,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("starter", "power", "enterprise")]
    [string]$PackName
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackDir = Split-Path -Parent $ScriptDir
$PackPath = Join-Path $PackDir "packs\$PackName"

if (-not (Test-Path $TargetDir)) {
    Write-Error "Error: Target directory does not exist: $TargetDir"
    exit 1
}

if (-not (Test-Path $PackPath)) {
    Write-Error "Error: Pack '$PackName' not found at $PackPath"
    exit 1
}

Write-Host "Installing '$PackName' pack to $TargetDir..." -ForegroundColor Green

# Copy CLAUDE.md
$ClaudeMd = Join-Path $PackPath "CLAUDE.md"
if (Test-Path $ClaudeMd) {
    Copy-Item $ClaudeMd (Join-Path $TargetDir "CLAUDE.md") -Force
    Write-Host "✓ Copied CLAUDE.md" -ForegroundColor Green
}

# Copy .gitignore (merge with existing if present)
$Gitignore = Join-Path $PackPath ".gitignore"
if (Test-Path $Gitignore) {
    $TargetGitignore = Join-Path $TargetDir ".gitignore"
    if (Test-Path $TargetGitignore) {
        Add-Content $TargetGitignore "`n# Claude Code Superuser Pack"
        Get-Content $Gitignore | Add-Content $TargetGitignore
        Write-Host "✓ Merged .gitignore" -ForegroundColor Green
    } else {
        Copy-Item $Gitignore $TargetGitignore -Force
        Write-Host "✓ Copied .gitignore" -ForegroundColor Green
    }
}

# Copy .claude directory
$ClaudeDir = Join-Path $PackPath ".claude"
if (Test-Path $ClaudeDir) {
    $TargetClaudeDir = Join-Path $TargetDir ".claude"
    if (-not (Test-Path $TargetClaudeDir)) {
        New-Item -ItemType Directory -Path $TargetClaudeDir | Out-Null
    }
    
    # Copy settings.json
    $SettingsJson = Join-Path $ClaudeDir "settings.json"
    if (Test-Path $SettingsJson) {
        Copy-Item $SettingsJson (Join-Path $TargetClaudeDir "settings.json") -Force
        Write-Host "✓ Copied .claude/settings.json" -ForegroundColor Green
    }
    
    # Copy settings.local.json.example
    $SettingsExample = Join-Path $ClaudeDir "settings.local.json.example"
    if (Test-Path $SettingsExample) {
        Copy-Item $SettingsExample (Join-Path $TargetClaudeDir "settings.local.json.example") -Force
        Write-Host "✓ Copied .claude/settings.local.json.example" -ForegroundColor Green
    }
    
    # Copy skills directory
    $SkillsDir = Join-Path $ClaudeDir "skills"
    if (Test-Path $SkillsDir) {
        Copy-Item $SkillsDir (Join-Path $TargetClaudeDir "skills") -Recurse -Force
        Write-Host "✓ Copied .claude/skills/" -ForegroundColor Green
    }
    
    # Copy agents directory
    $AgentsDir = Join-Path $ClaudeDir "agents"
    if (Test-Path $AgentsDir) {
        Copy-Item $AgentsDir (Join-Path $TargetClaudeDir "agents") -Recurse -Force
        Write-Host "✓ Copied .claude/agents/" -ForegroundColor Green
    }
    
    # Copy hooks directory
    $HooksDir = Join-Path $ClaudeDir "hooks"
    if (Test-Path $HooksDir) {
        $TargetHooksDir = Join-Path $TargetClaudeDir "hooks"
        if (-not (Test-Path $TargetHooksDir)) {
            New-Item -ItemType Directory -Path $TargetHooksDir | Out-Null
        }
        Copy-Item (Join-Path $HooksDir "*") $TargetHooksDir -Recurse -Force
        Write-Host "✓ Copied .claude/hooks/" -ForegroundColor Green
    }
    
    # Copy templates directory
    $TemplatesDir = Join-Path $ClaudeDir "templates"
    if (Test-Path $TemplatesDir) {
        Copy-Item $TemplatesDir (Join-Path $TargetClaudeDir "templates") -Recurse -Force
        Write-Host "✓ Copied .claude/templates/" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Review $(Join-Path $TargetDir 'CLAUDE.md')"
Write-Host "2. Review $(Join-Path $TargetDir '.claude\settings.json')"
Write-Host "3. Copy $(Join-Path $TargetDir '.claude\settings.local.json.example') to $(Join-Path $TargetDir '.claude\settings.local.json') for local-only tweaks"
Write-Host "4. Start using Claude Code with your new pack!"
