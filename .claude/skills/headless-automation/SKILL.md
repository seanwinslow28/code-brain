---
name: headless-automation
description: Claude Code headless mode and CI/CD automation guide. Covers the -p flag for non-interactive execution, --output-format stream-json for structured output, GitHub Actions integration with anthropics/claude-code-action, GitLab CI and Jenkins pipeline patterns, batch processing with parallel instances, CLAUDE_CODE_TASK_LIST_ID for multi-instance coordination, and output parsing with jq. Use when automating Claude Code, setting up CI/CD pipelines, running batch processing, or scripting non-interactive workflows.
---

# Headless Mode and Automation

## Purpose

Automate Claude Code for CI/CD pipelines, batch processing, and scripted workflows using headless mode (-p flag), structured output formats, and multi-instance coordination. Build reliable automation that integrates with GitHub Actions, GitLab CI, Jenkins, and shell scripts.

## When to Use

- Running Claude Code in CI/CD pipelines (GitHub Actions, GitLab, Jenkins)
- Batch processing files or tasks with parallel instances
- Piping data into Claude Code for automated analysis
- Parsing structured output from headless runs
- Coordinating multiple Claude Code instances on the same project
- Setting up automated PR reviews or test generation

## Examples

**Example 1: Automated PR review**
```
User: "Set up Claude Code to review PRs automatically in GitHub Actions"
Claude: [Uses headless-automation] Creates .github/workflows/claude-review.yml:

name: Claude PR Review
on: pull_request
jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this PR for security and performance issues."
          claude_args: "--max-turns 5"
```

**Example 2: Batch file analysis**
```
User: "Analyze all TypeScript files for type safety issues"
Claude: [Uses headless-automation] Creates a fan-out script:

for file in $(find src -name "*.ts"); do
  claude -p "Check @$file for 'any' types and suggest fixes" \
    --output-format json \
    --max-turns 3 > "$file.audit.json" &
done
wait
```

**Example 3: Piping logs for analysis**
```
User: "Analyze my build log for the root cause"
Claude: [Uses headless-automation]
cat build.log | claude -p "Identify the root cause of this build failure" --output-format text
```

## Headless Mode Basics

The `-p` (print) flag runs Claude Code non-interactively: execute a prompt, print the result, exit.

```bash
# Basic headless execution
claude -p "Summarize README.md"

# Pipe input
cat error.log | claude -p "What caused this crash?"

# Structured output
claude -p "List all TODO comments" --output-format json | jq -r '.result'

# With permission bypass (sandboxed environments only)
claude -p "Fix linting errors in src/" --dangerously-skip-permissions
```

## Output Formats

| Format | Flag | Output | Best For |
|--------|------|--------|----------|
| text | `--output-format text` | Raw assistant response | Human-readable output, piping to files |
| json | `--output-format json` | Structured object with result, cost, metadata | Script parsing, CI integration |
| stream-json | `--output-format stream-json` | NDJSON events in real-time | Long-running tasks, progress monitoring |

### Parsing JSON Output

```bash
# Extract just the result
claude -p "Summarize changes" --output-format json | jq -r '.result'

# Extract cost
claude -p "Review code" --output-format json | jq '.cost'
```

### Parsing Stream JSON

```bash
# Real-time text extraction
claude -p "Write documentation" --output-format stream-json | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

### Stream Chaining

Pipe one agent's output directly into another, maintaining full context:

```bash
claude -p "Analyze dataset" --output-format stream-json | \
claude -p "Review analysis" --input-format stream-json --output-format stream-json | \
claude -p "Generate report" --input-format stream-json
```

## GitHub Actions Integration

The official `anthropics/claude-code-action` handles environment setup and intelligent mode detection.

### Automated PR Review

```yaml
name: Claude Code PR Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - name: Claude Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this PR for security vulnerabilities and performance issues."
          claude_args: "--max-turns 5 --model claude-sonnet-4-5-20250929"
```

### On-Demand Test Generation

Triggered by commenting `/gen-tests` on a PR:

```yaml
name: Generate Tests
on:
  issue_comment:
    types: [created]
jobs:
  generate:
    if: contains(github.event.comment.body, '/gen-tests')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate unit tests for the changed files in this PR."
          claude_args: "--max-turns 10"
```

## GitLab CI Integration

```yaml
stages: [ai-review]

claude-review:
  stage: ai-review
  image: node:20
  variables:
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
  script:
    - npm install -g @anthropic-ai/claude-code
    - git diff origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME...$CI_COMMIT_SHA > diff.txt
    - cat diff.txt | claude -p "Review this diff for critical bugs" --output-format text > review.md
    - |
      curl --request POST --header "PRIVATE-TOKEN: $GL_TOKEN" \
      --data-urlencode "body=$(cat review.md)" \
      "https://gitlab.com/api/v4/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID/notes"
```

## Jenkins Pipeline

```groovy
pipeline {
    agent any
    environment {
        ANTHROPIC_API_KEY = credentials('anthropic-api-key')
    }
    stages {
        stage('Setup') {
            steps { sh 'npm install -g @anthropic-ai/claude-code' }
        }
        stage('AI Analysis') {
            steps {
                sh 'claude -p "Analyze project structure and suggest improvements" --output-format json > analysis.json'
            }
        }
    }
}
```

## Batch Processing Patterns

### Fan-Out (Parallel File Processing)

```bash
find src -name "*.ts" | while read file; do
  claude -p "Add JSDoc comments to exported functions in @$file" \
    --dangerously-skip-permissions \
    --output-format json > "$file.audit.json" &
done
wait
echo "All files processed."
```

### Sequential Pipeline

```bash
# Step 1: Analyze
claude -p "List all security issues in src/" --output-format json > issues.json

# Step 2: Fix
cat issues.json | jq -r '.result' | claude -p "Fix these security issues" --dangerously-skip-permissions

# Step 3: Verify
claude -p "Verify all security issues are resolved" --output-format json > verification.json
```

## Multi-Instance Coordination

Use `CLAUDE_CODE_TASK_LIST_ID` to share task state across parallel sessions:

```bash
export CLAUDE_CODE_TASK_LIST_ID="feature-xyz-migration"

# Session A: Frontend work
claude -p "Update React components for the new API" &

# Session B: Backend work (shares task list with A)
claude -p "Update API endpoints" &

wait
echo "Both sessions completed."
```

Instances with the same ID read/write to a shared task list in `~/.claude/tasks/`.

## Automation Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Required for headless authentication |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | Disable telemetry and auto-updates (CI firewalls) |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Prevent background processes (serverless runners) |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Cap response size (prevent runaway loops) |
| `MAX_THINKING_TOKENS` | Thinking budget (0 to disable, saves latency) |
| `CLAUDE_CODE_TASK_LIST_ID` | Shared task state across instances |

## Essential CLI Flags for Automation

| Flag | Description |
|------|-------------|
| `-p "prompt"` | Headless mode |
| `--output-format json\|stream-json` | Structured output |
| `--max-turns N` | Hard loop limit (prevents cost overruns) |
| `--max-budget-usd N` | Strict cost cap |
| `--dangerously-skip-permissions` | YOLO mode (sandboxed only) |
| `--allowedTools "Read,Bash"` | Whitelist specific tools |
| `--no-session-persistence` | Clean slate per run |
| `--add-dir path` | Scope to specific directories |

## Best Practices

1. **Always sandbox** `--dangerously-skip-permissions` runs in containers or ephemeral environments
2. **Set --max-turns** to prevent infinite loops and cost overruns in CI
3. **Use --max-budget-usd** as a safety net for cost control
4. **Pin action versions** (`@v1`) to prevent upstream breaking changes
5. **Use CLAUDE.md** in CI to enforce linting/testing rules Claude must follow
6. **Set --no-session-persistence** in CI to prevent context bleed between runs

## Success Criteria

- [ ] Headless command runs without interactive prompts
- [ ] Output format is parseable by downstream scripts
- [ ] CI pipeline completes within cost and turn limits
- [ ] Permission bypass is only used in sandboxed environments
- [ ] Multi-instance coordination shares task state correctly

## Copy/Paste Ready

```
"Set up Claude Code in GitHub Actions for PR reviews"
"Run Claude Code headless to analyze this file"
"Create a batch processing script for all TypeScript files"
"Set up GitLab CI with Claude Code"
"How do I parse Claude Code's JSON output?"
```
