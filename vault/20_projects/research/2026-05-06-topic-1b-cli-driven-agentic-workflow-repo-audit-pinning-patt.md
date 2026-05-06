---
type: research-report
date: 2026-05-06
question: "Topic 1b — CLI-driven agentic-workflow repo audit + pinning patterns + Gemini CLI extensions. Evaluate https://github.com/jackwener/OpenCLI.git and https://github.com/google-gemini/gemini-cli.git on (1) license, (2) maintenance signal (last commit, release cadence, open-issue velocity), (3) security-review surface — specifically does the repo execute model output as code, (4) fit for invocation from a Python wrapper script in the same pattern as the gemini-image-gen skill (subprocess CLI call, structured output parsing). Catalog Gemini CLI extensions from https://geminicli.com/extensions/ for relevance to research / agentic-workflow / data-tooling — including any Deep Research extension. Document patterns for pinning/vendoring third-party CLI repos so a repo update doesn't break a personal workflow: (a) git submodule pinned to commit SHA, (b) pip install from git URL with @sha pin, (c) vendored-copy approach (as used by last30days/scripts/lib/vendor/bird-search/). Recommend a concrete pinning recipe for invoking these CLIs from a personal autonomous agent fleet running on macOS launchd."
source: gemini-deep-research
cost_usd: 2.8000
wall_seconds: 406
interaction_id: v1_Chd3cHY3YWRXNURNVGpfdU1QczlUVmdRSRIXd3B2N2FkVzVETVRqX3VNUHM5VFZnUUk
agent_id: deep-research-preview-04-2026
created: 2026-05-06
tags: [research, gemini-deep-research, autogen]
---

# Topic 1b — CLI-driven agentic-workflow repo audit + pinning patterns + Gemini CLI extensions. Evaluate https://github.com/jackwener/OpenCLI.git and https://github.com/google-gemini/gemini-cli.git on (1) license, (2) maintenance signal (last commit, release cadence, open-issue velocity), (3) security-review surface — specifically does the repo execute model output as code, (4) fit for invocation from a Python wrapper script in the same pattern as the gemini-image-gen skill (subprocess CLI call, structured output parsing). Catalog Gemini CLI extensions from https://geminicli.com/extensions/ for relevance to research / agentic-workflow / data-tooling — including any Deep Research extension. Document patterns for pinning/vendoring third-party CLI repos so a repo update doesn't break a personal workflow: (a) git submodule pinned to commit SHA, (b) pip install from git URL with @sha pin, (c) vendored-copy approach (as used by last30days/scripts/lib/vendor/bird-search/). Recommend a concrete pinning recipe for invoking these CLIs from a personal autonomous agent fleet running on macOS launchd.

> Generated 2026-05-06 15:58 by `gemini-dr` (agent=deep-research-preview-04-2026 · tier=dr · wall=406s).

# Architecture and Security Audit of CLI-Driven Agentic Workflows

The rapid evolution of autonomous artificial intelligence systems has precipitated a fundamental paradigm shift in software architecture. Rather than relying exclusively on traditional Application Programming Interfaces (APIs), modern agentic workflows are increasingly utilizing Command Line Interfaces (CLIs) as their primary execution environments. This architectural pivot enables Large Language Models (LLMs) to interact with host operating systems, local file structures, and authenticated browser instances through standardized, deterministic shell commands. As these intelligent agents transition from supervised conversational interfaces to autonomous infrastructure operators, the foundational tooling they invoke must be subjected to rigorous auditing. Factors such as licensing compliance, maintenance velocity, execution security, and the reliability of machine-readable outputs dictate the viability of a CLI tool within an enterprise or personal agent fleet.

This comprehensive research report provides an exhaustive evaluation of two highly prominent CLI repositories currently utilized in agentic orchestration: `jackwener/OpenCLI` and `google-gemini/gemini-cli`. Furthermore, it categorizes the broader ecosystem of Gemini CLI extensions, critically analyzes dependency pinning patterns required for stabilizing autonomous architectures, and establishes a concrete, crash-tolerant deployment recipe for managing a local agent fleet utilizing macOS `launchd`.

## 1. Repository Evaluation: Licensing and Compliance

Software licensing dictates the legal and operational boundaries within which third-party tools can be integrated into proprietary, commercial, or personal agentic fleets. When an autonomous agent is granted the autonomy to install, execute, or modify external software, the underlying license of that software must align with the deployment strategy of the parent organization.

The comparative analysis of the licensing models for both OpenCLI and the Gemini CLI reveals a strong alignment toward permissive, enterprise-friendly open-source distribution. The `jackwener/OpenCLI` repository is licensed under the Apache-2.0 open-source license [cite: 1, 2, 3]. Repository telemetry and historical data indicate that the license was intentionally migrated from the BSD-3-Clause to Apache-2.0 to foster broader adoption [cite: 1]. The Apache-2.0 license is highly permissive; it grants explicit patent rights alongside standard copyright usage, making it exceptionally well-suited for integration into commercial AI pipelines. This ensures that integrating OpenCLI into a proprietary AI agent does not legally force the resulting derivative works to become open-source.

Similarly, the `google-gemini/gemini-cli` repository is distributed under the Apache-2.0 license [cite: 4]. This structural alignment in licensing simplifies compliance for systems architects. Developers can orchestrate workflows that invoke both tools sequentially—for instance, using Gemini CLI for data analysis and OpenCLI for browser execution—without navigating conflicting legal obligations or copyleft viral clauses. 

## 2. Maintenance Signals and Development Velocity

Evaluating the maintenance signal of a repository is a critical prerequisite when deploying autonomous agents. An agent dependent on an abandoned or poorly maintained CLI will experience catastrophic failures as upstream web APIs, Document Object Model (DOM) structures, or operating system dependencies evolve. Evaluating commit history, release cadence, and issue velocity provides a proxy for a tool's resilience.

| Metric | `jackwener/OpenCLI` | `google-gemini/gemini-cli` |
| :--- | :--- | :--- |
| **Project Backing** | Independent / Community-driven | Corporate (Google) / Enterprise-backed |
| **Total Commits** | 565+ | 6,071+ |
| **Latest Commit** | Highly recent (within hours/days) | Highly recent (within 24 hours) |
| **Total Releases** | 93 (Latest: v1.7.12) | 486 (Latest: v0.41.1) |
| **Release Cadence** | Continuous, agile iteration | Structured (Nightly, Preview, Stable) |
| **Open Issues** | ~33 | ~2,100 |

The `jackwener/OpenCLI` repository exhibits the rapid iteration and agile maintenance velocity typical of early-stage, high-impact AI orchestration tools. The project maintains a highly active commit pipeline, with numerous files and directories updated continuously [cite: 1, 3]. The project has published 93 releases, demonstrating a commitment to shipping fixes and new built-in adapters for various social media and web platforms [cite: 1, 5]. With over 8,300 stars and approximately 33 open issues, the repository demonstrates a tightly managed feedback loop where issues are likely addressed swiftly by the core maintainer and active community contributors [cite: 1, 3]. This profile is ideal for developers seeking cutting-edge capabilities, though it carries the inherent risks of single-maintainer bottlenecks.

Conversely, the maintenance footprint of the `google-gemini/gemini-cli` repository is indicative of a mature, enterprise-backed software lifecycle. The repository manages a massive volume of activity, boasting over 6,071 commits and 486 releases [cite: 4]. The release cadence is highly regimented and structured to protect production environments. It is divided into three distinct channels: a Nightly build published daily for experimental features, a Preview build published weekly on Tuesdays, and a Stable build that promotes the previous week's preview, also published on Tuesdays [cite: 4]. The presence of over 2,100 open issues highlights widespread global adoption and rigorous bug tracking [cite: 4]. This massive issue backlog is not necessarily a negative signal; rather, it confirms that the tool is subjected to continuous stress-testing across diverse enterprise environments, and that feature requests are systematically cataloged.

## 3. Security-Review Surface: Execution of Model Output as Code

The security surface of a CLI-driven agent is fundamentally defined by its execution privileges. When an LLM generates a command, the CLI acts as the execution kernel. If the CLI fails to sandbox this execution, prompt injection vulnerabilities can escalate directly to Remote Code Execution (RCE) on the host machine. AI coding agents must be treated as highly privileged execution environments, not mere conversational interfaces [cite: 6, 7].

### 3.1 OpenCLI Security Architecture and Vulnerability Vectors

OpenCLI presents a highly elevated and complex security risk surface due to its core architectural premise: transforming live, authenticated browser sessions into programmatic CLI endpoints [cite: 5, 8]. It utilizes a "Browser Bridge" extension to interface with Google Chrome or Chromium via the Chrome DevTools Protocol (CDP), bypassing the need for separate authentication handling [cite: 3, 5]. 

While the documentation touts the system as "Account-safe" because user credentials never leave the browser and LLM tokens are not consumed at runtime, this architecture fundamentally allows the AI agent to act with the exact privileges of the authenticated user [cite: 5, 8]. The most critical security concern within OpenCLI is the explicit provision of an `opencli browser eval` primitive [cite: 1, 5, 8]. This command allows AI agents—particularly those equipped with the `opencli-adapter-author` skill—to execute arbitrary JavaScript directly within the context of a live webpage [cite: 1, 5]. 

The repository currently lacks a documented `SECURITY.md` policy or a formalized sandboxing architecture to constrain this execution [cite: 9]. If an autonomous agent is directed to summarize an untrusted webpage containing a hidden prompt injection payload, the model could be maliciously coerced into using the `eval`, `click`, or `type` primitives to initiate unauthorized financial transactions, exfiltrate private data from other active tabs, or manipulate cloud infrastructure consoles [cite: 6, 7]. Historically, underlying JavaScript environments handling user-provided `eval` inputs have been acutely vulnerable to sandbox escapes via prototype pollution, which can result in total losses of confidentiality and system availability [cite: 10]. When an AI agent possesses the autonomy to dynamically generate, verify, and execute new web adapters using `eval` without a human-in-the-loop buffer, the boundary between benign data parsing and destructive code execution dissolves entirely [cite: 5, 7].

### 3.2 Gemini CLI Security Architecture and Sandboxing

In stark contrast, the Gemini CLI treats execution security and process isolation as foundational architectural pillars. Recognizing the extreme risks of unattended agent execution, the CLI implements multiple defensive layers to mitigate supply chain attacks and prompt injections [cite: 4, 11, 12, 13].

The first line of defense is the "Trusted Folders" protocol. This feature prevents malicious repository content from hijacking the agent upon initialization. When the CLI is invoked in a new directory, it intercepts the loading of project-specific `.gemini/settings.json` files and local environment variables [cite: 11]. The user is prompted via a trust dialog to approve the workspace [cite: 11, 14]. If a folder is deemed untrusted, the CLI operates in a restricted "safe mode." In this state, custom tools are strictly disabled, extension management is locked, and auto-acceptance of tool execution is universally denied, ensuring the model cannot act autonomously [cite: 11, 14]. 

The second line of defense is multi-tier containerized sandboxing, which explicitly isolates potentially dangerous operations such as shell commands or file modifications [cite: 12, 13]. On macOS, the CLI utilizes `sandbox-exec` to enforce a Seatbelt `permissive-open` profile, which allows outbound network access but strictly restricts write operations to the current project directory [cite: 13, 15]. For complete process isolation across operating systems, the CLI natively supports Docker and Podman environments. The sandbox mounts the current working directory seamlessly, allowing the AI to read and modify project files while remaining cryptographically and structurally isolated from the host operating system's root files and background processes [cite: 12, 13].

Despite these robust protections, vulnerabilities can still emerge in headless Continuous Integration/Continuous Deployment (CI/CD) environments. If an automation pipeline utilizes the `--skip-trust` flag or sets `GEMINI_CLI_TRUST_WORKSPACE=true` to bypass the interactive trust dialog, the system assumes inherent trust [cite: 6, 14]. In such configurations, an attacker can use malicious issue comments or Pull Request titles to execute prompt injections against the agent, potentially leaking API keys, executing unauthorized shell commands, or abusing the runner's access privileges [cite: 6, 14]. Security analysts strongly advise against granting agents real-time access to production environments without human-in-the-loop verification, emphasizing that no amount of filtering can overcome the inherent risks of processing untrusted third-party inputs within a privileged execution shell [cite: 6, 7].

## 4. Invocation from Python Wrappers: Subprocess and Structured Output

Autonomous agent fleets are rarely orchestrated entirely in raw bash scripts. Professional deployments typically rely on a primary control loop written in Python, enabling complex state management, memory retrieval, and sequential reasoning. This control loop must invoke CLI tools via the Python `subprocess` module, capture the standard output (`stdout`), and parse the resulting data. For this pattern to be resilient—replicating the robust architecture seen in tools like the `gemini-image-gen` skill—the CLI must guarantee deterministic, machine-readable output schemas, typically formatted as JSON [cite: 16, 17]. 

Both OpenCLI and the Gemini CLI provide extensive support for structured output, making them exceptionally well-suited for Python subprocess integration.

### 4.1 OpenCLI Subprocess Integration

OpenCLI is inherently designed for programmatic use and pipeline integration [cite: 1]. The architecture provides deterministic interfaces, ensuring that identical commands will consistently yield the exact same output schema every time they are executed [cite: 1, 5]. This predictability is paramount for Python wrapper scripts, which crash if output schemas mutate unexpectedly. 

All built-in OpenCLI commands natively support the `--format json` or `-f json` flags [cite: 1, 8]. For example, a Python orchestrator can execute `subprocess.run(["opencli", "hackernews", "top", "--limit", "5", "-f", "json"], capture_output=True, text=True)`. The resulting JSON string captured from `stdout` can be instantly deserialized using Python's native `json.loads()` [cite: 1, 18]. Because OpenCLI adapters rely on structured DOM snapshots rather than stochastic LLM parsing to extract data, this execution path consumes zero LLM tokens and operates with absolute programmatic determinism, heavily reducing the fragility of the agentic workflow [cite: 3, 5, 8].

### 4.2 Gemini CLI Subprocess Integration

The Gemini CLI was specifically updated to support robust non-interactive automation, resolving earlier limitations where plain-text output created bottlenecks for parsing logic in CI/CD integrations [cite: 19, 20]. The CLI achieves this through a structured JSON output mode, establishing a clear API contract for developers [cite: 19].

Developers can pass the `--output-format json` flag to receive a single, structured JSON object containing the complete result of the session, including the model's response, execution errors, and performance statistics [cite: 4, 19]. To ensure the CLI does not hang waiting for user input during automated execution, the Python wrapper must utilize headless mode by providing the prompt alongside the `-p` flag (e.g., `subprocess.run(["gemini", "-p", "Analyze this data", "--output-format", "json"], capture_output=True, text=True)`) [cite: 4, 17]. 

For long-running research tasks or complex code generation operations, the Gemini CLI supports real-time monitoring via the `--output-format stream-json` flag, which emits newline-delimited JSON events [cite: 4, 21]. A Python wrapper can read this output line-by-line using `subprocess.Popen`, allowing the orchestrator to monitor the agent's progress dynamically.

Furthermore, the Gemini ecosystem natively supports JSON Schema enforcement via the Model Context Protocol and direct API integrations [cite: 16, 22]. Python wrappers can utilize libraries like Pydantic to strictly define the expected data types and hierarchical structure of the desired output [cite: 16, 22, 23]. By passing a Pydantic model directly into the API configuration (or structuring the CLI prompt to demand strict adherence to a provided JSON schema), the model guarantees that the response will match the schema exactly [cite: 16, 24, 25]. Recent updates ensure that the output preserves the exact property ordering specified in the schema, eliminating the need for fragile string manipulation or regex parsing within the Python wrapper [cite: 22]. 





## 5. Catalog of Gemini CLI Extensions

The Gemini CLI serves as a foundational execution environment, but its true utility within autonomous workflows is unlocked via its modular extension ecosystem. These extensions equip the underlying model with specialized domain knowledge, deep research capabilities, and the capacity to interact with databases and external APIs. Based on the official extension directory, the tools most critical for research, orchestration, and data analytics are cataloged below.

### 5.1 Deep Research Capabilities
Deep Research extensions transform the CLI from a simple query respondent into a long-context synthesis engine capable of scouring the web, aggregating academic literature, and analyzing social media trends over extended temporal windows.

| Extension Name | Package Identifier | Operational Capability |
| :--- | :--- | :--- |
| **Deep Research** | `@allenhutchison/gemini-cli-deep-research` | The standard implementation for broad-spectrum deep research and context synthesis [cite: 26]. |
| **Research CLI** | `@rmedranollamas/research-cli` | An advanced variant utilizing the experimental Gemini v1alpha Interactions API for nuanced query formulation [cite: 26]. |
| **Co-Researcher** | `@poemswe/co-researcher` | A PhD-level analytical suite optimized for academic writing, systematic literature reviews, and critical analysis [cite: 26]. |
| **Last30Days Skill** | `@mvanhorn/last30days-skill` | A multi-source intelligence aggregator that scans X, Reddit, YouTube, TikTok, Hacker News, and Polymarket to synthesize current discourse [cite: 26, 27]. |
| **Nagomi** | `@avivlyweb/pubmed-gemini-extension` | A highly specialized medical research engine featuring automated hallucination detection and evidence grading against the PubMed corpus [cite: 26]. |
| **Papersflow MCP** | `@papersflow-ai/papersflow-mcp` | An academic tool dedicated to literature search, citation verification, and related-paper discovery algorithms [cite: 26]. |
| **Autoresearch** | `@wjgoarxiv/autoresearch-skill` | Provides continuous, autonomous research loops for any designated technical or market domain [cite: 26]. |

### 5.2 Agentic-Workflow Orchestration
Agentic-workflow extensions upgrade the LLM into a project manager. Instead of writing isolated blocks of code, the model uses these tools to plan software architecture, delegate tasks to specialized sub-agents, and verify the successful completion of complex engineering pipelines.

| Extension Name | Package Identifier | Operational Capability |
| :--- | :--- | :--- |
| **Conductor** | `@gemini-cli-extensions/conductor` | A foundational orchestrator allowing users to specify, plan, and autonomously implement software features [cite: 26]. |
| **Maestro** | `@josstei/maestro-orchestrate` | A massive development platform featuring 39 distinct specialist profiles and a rigorous 4-phase orchestration process [cite: 26]. |
| **Gemini Swarm** | `@tmdgusya/gemini-swarm` | Enables "swarm mode," orchestrating multiple autonomous agents into a collaborative team to tackle parallel tasks [cite: 26]. |
| **SDD Flow** | `@nushey/sdd-flow` | A Spec-Driven Development coordinator that manages simulated Tech Lead, Developer, and Verifier subagents [cite: 26]. |
| **AgenticFlow** | `@PixelML/agenticflow-skill` | A vast automation connector linking the CLI to over 2,500 distinct SaaS integrations and APIs [cite: 26]. |
| **HelloAgents** | `@hellowind777/helloagents` | A quality-driven orchestration kernel designed explicitly for managing AI CLI operations reliably [cite: 26]. |

### 5.3 Data-Tooling and Database Interaction
Data-tooling extensions leverage the Model Context Protocol (MCP) to securely connect the agent to external data warehouses, relational databases, and analytics engines, allowing the model to write and execute SQL natively.

| Extension Name | Package Identifier | Operational Capability |
| :--- | :--- | :--- |
| **MCP Toolbox** | `@googleapis/mcp-toolbox` | A comprehensive, open-source server facilitating direct connections to over 30 distinct database systems [cite: 26]. |
| **Data Agent Kit** | `@gemini-cli-extensions/data-agent-kit-starter-pack`| A suite for data engineers to architect complex pipelines, transform data using dbt, and execute BigQuery SQL notebooks [cite: 26]. |
| **MongoDB** | `@mongodb/agent-skills` | The official integration for managing collections, connecting to clusters, and optimizing complex NoSQL queries [cite: 26]. |
| **MotherDuck** | `@motherduckdb/agent-skills` | Interfaces with live schemas, allowing the agent to write DuckDB SQL for rapid, local analytics applications [cite: 26]. |
| **Relational DBs** | `postgres`, `mysql` | Direct integrations permitting the agent to read schemas and interact with PostgreSQL and MySQL environments [cite: 26]. |
| **Data Commons** | `@gemini-cli-extensions/datacommons` | Enables natural language querying and synthesis of massive public datasets maintained by the Data Commons project [cite: 26]. |

## 6. Dependency Pinning Patterns for Third-Party CLIs

When constructing an autonomous agent fleet, the architectural stability of external dependencies is paramount. Agent workflows rely on strict structural contracts; if a third-party CLI repository updates and inadvertently alters a command structure, deprecates a flag, or mutates a JSON output schema, the dependent Python orchestrator will crash. To mitigate this fragility, developers employ various dependency pinning patterns to permanently lock the third-party repository to a known, functional state.

### 6.1 Git Submodules Pinned to a Commit SHA

A Git submodule operates by embedding a secondary repository as a literal subdirectory within the parent repository. Instead of tracking the individual files of the dependency, the parent repository records a specific, immutable commit hash (SHA) of the foreign repository within a `.gitmodules` file [cite: 28, 29]. 

This approach maintains a strict architectural boundary between the parent project and the dependency, preventing the commingling of distinct codebases [cite: 28, 30]. By explicitly relying on a Git tree hash, submodules provide a degree of cryptographic immunity against supply chain subversion; malicious actors cannot silently swap the dependency without altering the hash and triggering an alert [cite: 31]. Furthermore, submodules facilitate rapid upstream bug fixing. A developer can seamlessly change directories into the submodule, correct a flaw in the dependency, commit the fix, and push it back to the origin repository without leaving the primary workspace [cite: 28, 29].

However, the implementation of Git submodules is notoriously fragile, particularly within automated CI/CD environments and collaborative workflows. Submodules severely disrupt standard branching operations. When switching branches in the parent repository from a branch that contains a submodule to one that does not, Git frequently fails to clean up the directory, leaving untracked files on disk and generating persistent `unable to rmdir` errors [cite: 32, 33]. This forces developers and automated pipelines to incessantly execute `git submodule update --init --recursive` to forcibly sync the tree state [cite: 32]. More critically, submodules fundamentally break Git's `worktree` feature—a mechanism heavily utilized in advanced deployment pipelines to maintain multiple parallel checkouts of a single repository—rendering them highly unsuitable for complex orchestration fleets [cite: 32].

### 6.2 Pip Install from Git URL with `@sha` Pin

Python's package manager, `pip`, allows for the direct installation of dependencies from a Git repository URL, explicitly pegged to a specific commit hash (e.g., `pip install git+https://github.com/organization/repo.git@abcdef123456`). 

This pattern is the native, expected deployment mechanism for Python-centric environments. It resolves dependencies automatically and installs the target package directly into the virtual environment's `site-packages` directory [cite: 30]. This keeps the primary repository clean, entirely avoiding the tracking of foreign code within the parent version control system [cite: 30, 31]. 

Despite its elegance for pure Python libraries, this method is highly suboptimal for agentic workflows that rely on diverse CLIs and mixed-language binaries. If the target repository contains necessary Makefiles, bash shell scripts, YAML configurations, or specialized binaries (like Node.js execution environments) that are not explicitly packaged via a standard `setup.py` or `pyproject.toml`, `pip` will fail to extract and place them accurately in the working directory [cite: 30]. Consequently, the agent will crash when attempting to invoke shell scripts that were left behind during the installation process.

### 6.3 The Vendored-Copy Approach

Vendoring involves entirely bypassing package managers and submodule references by physically copying the required source code of the dependency directly into the parent repository, committing the files as native assets [cite: 31, 34]. 

This pattern provides absolute architectural stability. Collaborators, deployment servers, and autonomous agent containers simply execute a `git pull` and immediately receive the dependency. There is no requirement for secondary initialization commands (unlike submodules) or package manager resolutions (unlike `pip`), guaranteeing that the code executes natively within the project's relative path [cite: 34]. Vendoring also allows for granular file filtering; developers can surgically extract only the necessary execution scripts while discarding upstream documentation, unit tests, and CI/CD configurations, streamlining the overall footprint [cite: 34].

A prime operational example of this approach is demonstrated within the `last30days` skill repository, which hosts a vendored X (Twitter) search client. The dependency is isolated deeply within the directory structure at `skills/last30days/scripts/lib/vendor/bird-search/` [cite: 35, 36, 37]. The main Python research engine (`last30days.py`) orchestrates the workflow and invokes the vendored JavaScript client directly via `subprocess` (e.g., `node ~/.claude/skills/last30days/scripts/lib/vendor/bird-search/bird-search.mjs`) [cite: 27, 35]. By vendoring this specific asset, the project ensures that the critical search functionality remains permanently bound to the agent's logic, entirely insulated from upstream breaking changes or package registry outages.

While vendoring artificially inflates the parent repository's codebase size and requires manual intervention to pull upstream updates, it remains the superior pattern for autonomous agent fleets. It eliminates the execution risks associated with failed submodule initializations and incomplete `pip` installations, ensuring maximum resilience during unattended deployment [cite: 31, 34].

## 7. Concrete Deployment Recipe: macOS `launchd` Agent Fleet

To deploy a persistent, crash-tolerant autonomous agent fleet on macOS, standard `cron` jobs are insufficient. `Cron` lacks built-in process supervision, fails to trigger tasks immediately upon boot without extensive secondary configuration, and struggles to manage complex environment variables gracefully [cite: 38, 39]. The native macOS service management framework, `launchd`, provides the robust supervision required. `Launchd` is capable of executing scripts at timed intervals, capturing standard output, managing dependencies, and automatically restarting crashed agents, ensuring continuous operation [cite: 38, 39, 40].

The following deployment recipe utilizes the **Vendored-Copy** pattern alongside a **Bash Watchdog Script** to ensure a Python orchestrator can securely invoke vendored CLIs.

### 7.1 Architectural Prerequisites

1.  Vendor the target CLIs (e.g., Gemini CLI extensions or OpenCLI) into a dedicated subdirectory within the fleet repository: `/Users/agent/fleet/vendor/`.
2.  Develop the primary Python orchestrator script (`agent_loop.py`) that utilizes the `subprocess.run()` module to call the vendored CLIs and parses their JSON output.
3.  Establish an isolated Python virtual environment specifically for the fleet at `/Users/agent/fleet/.venv`.

### 7.2 The Watchdog Wrapper Script

`Launchd` executes in a bare system environment, entirely devoid of the standard user variables typically loaded via `.zshrc` or `.bashrc` [cite: 41, 42]. Attempting to invoke a Python script directly from `launchd` frequently results in import errors and path resolution failures [cite: 42, 43]. To circumvent this limitation, the `launchd` service must invoke an intermediary Bash "watchdog" script. This watchdog is responsible for establishing process locks, injecting necessary environment variables, and invoking the Python orchestrator.

Create a script file at `/Users/agent/fleet/watchdog.sh` and make it executable (`chmod +x watchdog.sh`):

```bash
#!/bin/bash
# Fleet Watchdog - Crash-tolerant execution for Python Agent Wrappers
# Executed via macOS launchd. 

# 1. Establish absolute paths (launchd requires absolute paths for reliability)
FLEET_DIR="/Users/agent/fleet"
VENV_PYTHON="$FLEET_DIR/.venv/bin/python"
AGENT_SCRIPT="$FLEET_DIR/agent_loop.py"
LOCK_FILE="$FLEET_DIR/agent.lock"

# 2. Crash Tolerance: Lock File Management
if [ -f "$LOCK_FILE" ]; then
    lock_pid=$(cat "$LOCK_FILE" 2>/dev/null)
    # Layer 1 Liveness Check: Is the process ID in the lock file actually running?
    if [ -n "$lock_pid" ] && kill -0 "$lock_pid" 2>/dev/null; then
        # Prevent parallel execution collisions
        exit 0
    fi
    # If the process is dead but the lock file persists, it is a zombie lock. Remove it.
    rm -f "$LOCK_FILE"
fi

# Establish a new lock with the current PID and ensure cleanup upon exit
echo $$ > "$LOCK_FILE"
trap 'rm -f "$LOCK_FILE"' EXIT

# 3. Inject Context and Environment Variables
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

# Required for headless Gemini CLI execution in CI/CD or Agent environments
export GEMINI_CLI_TRUST_WORKSPACE=true 

# 4. Execute the Python Wrapper
cd "$FLEET_DIR" || exit 1
"$VENV_PYTHON" "$AGENT_SCRIPT" >> "$FLEET_DIR/logs/agent.log" 2>&1
```

> **Editor's note (2026-05-06, Sean):** The DR-rendered output had `cd "$FLEET_DIR" || exit 1` mangled across three lines as a markdown-table-cell artifact (`||` adjacent to a code block). Restored to the intended one-liner above so the recipe is copy-pasteable.

The watchdog implements a critical lock file mechanism utilizing the `kill -0` check. This ensures that `launchd` does not blindly spawn parallel, overlapping instances of the agent if a single execution loop becomes hung or takes longer to complete than the designated scheduling interval [cite: 38].

### 7.3 The launchd Plist Configuration

To register the watchdog script with the macOS operating system, a Property List (`.plist`) XML file must be authored [cite: 39, 40, 44]. Because the agent requires access to standard user environment variables, browser cookies, and potentially GUI frameworks (if utilizing OpenCLI's Chrome integration), the configuration must be installed as a **User Agent** located in `~/Library/LaunchAgents`, rather than a System Daemon [cite: 39, 41, 45]. User Agents execute within the context of the logged-in user, granting them the necessary permissions to interface with user-level applications [cite: 45].

Create the configuration file at `~/Library/LaunchAgents/com.fleet.agent.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Unique Identifier for the agent service -->
    <key>Label</key>
    <string>com.fleet.agent</string>

    <!-- Absolute path array to execute the Bash Watchdog -->
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/agent/fleet/watchdog.sh</string>
    </array>

    <!-- Execute immediately upon user login -->
    <key>RunAtLoad</key>
    <true/>

    <!-- Relaunch the watchdog every 120 seconds -->
    <key>StartInterval</key>
    <integer>120</integer>

    <!-- Establish working directory -->
    <key>WorkingDirectory</key>
    <string>/Users/agent/fleet</string>

    <!-- Logging outputs for system-level debugging -->
    <key>StandardOutPath</key>
    <string>/Users/agent/fleet/logs/launchd.stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/agent/fleet/logs/launchd.stderr.log</string>
</dict>
</plist>
```

**Activation Sequence**:
To deploy the agent fleet without requiring a complete system reboot, developers must interact with the `launchctl` command-line utility within the target user's active GUI session [cite: 39, 44]:

1.  Load the configuration into the system manager: `launchctl load ~/Library/LaunchAgents/com.fleet.agent.plist`
2.  Initiate the service manually (optional, as `RunAtLoad` handles initial boot): `launchctl start com.fleet.agent`

By utilizing this deployment architecture, the macOS host operating system autonomously supervises the agent fleet. The `StartInterval` continually prompts the watchdog, the watchdog prevents parallel execution collisions, and the Python orchestrator successfully invokes the vendored CLI tools, establishing a highly resilient, enterprise-grade autonomous workflow [cite: 38, 39, 40].



**Sources:**
1. [Link](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGmxQBqNkqjJAvFaO1YoCo0Ur7RNjFvQsjJs8WA8aiSrZ1StbUUgy5V5IxDV7lP3xm70vfxrdktpqb_WgB4MsCHqiVzdevqoc_kbWZAVQGDwXbHcPuySJ7DfIU=)
2. [skillsllm.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQER2_5KtrNUC6FsRpHZeyaX6U0fLIEnnoJhCw2Iqby4K-nUccwX-fWlry7GRyOiRN_q802XH6To57GKqvb46PPbaRoLzFE2pwWQDYic0hSO8LU-KLDBA3b8zMamPSfzyWN0atc=)
3. [apiyi.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE-TDJcBlUHTBdVzRu-cZXiCjVjRHEzoTHNKA9A_UHBfXgH5W3rQfJxlSGD-RjUC_AcVqJktM2NyJPULqvwcfFvL7zz-hkZPOb7wjBHPk-u7-k1cPn8ZFIJNx7IaNAupzMTOm4ZuNbDZWE9kAE5nDl1vIU047yGjMMka2WB6bkcdqb_1kcYXJpQKWd6MhwS_LNU5w==)
4. [Link](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFUsFrALxdH70DFiHM25J2SfnlV5qS1OpLir_w7D_Afjsk43Knt2sd8J3gQS1wsQ7zdVdUYzf3ruSuk0WLTWUyHpT0yU5GDxhPaaw9kp_2iBMaFJpBtqzWtOBLUgiVB0ro=)
5. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_iKVy3vSFFhYuc-rYlQMMpv0SrvsxIeQvnuUh3i8Mp3ObjtNH9ohI-BLaMT6-96xvYNmpTakk6xaOt78fmf69v_7_LCMsZOv_IrOyIh0DcJp6fOvOEvWBQw==)
6. [penligent.ai](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGdsB-cE-E0i66LafJ-5FsxL_kyDt_8YmiXhPD21TkIJ5obUrXvwtHxL749rdfhuwtXJJ5tnLnrIz_MRR2aBt87rGLgHOfiE7RswLW_9fk5VxB8lvVR3HEOXpVULkJ5yFDeCsvw8k3oYf-IFj4q2orX1qChSF0uCfzwtQarSUQk9B0aDQBnDGbysVErHGKnfq79Yxm84pIZ01R5QkHT)
7. [ycombinator.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGCCey7wCvg5Z2FX1zSZ3bHkIIveocwUoL-p0wAGfVZRyXkgAYwn1HWR5r1v0g7vznyYDP32hyZs_6pVsP3cnIiHtco0ju5ku3ZSRIRzu5XHk4u2-uPK8gtTSOJqdlWxGp_Iwc=)
8. [Link](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHjaTAOHyGx6yCLyFhbtsIBydYz3pnQHcFu7KmzDr6Rve-d8YTdpEQhQjVTez0Z0KasHMOJwQURfUMb36D5tH9rvrnKgCdWpJqUO2HoYC4nw2leIKjryjiI-HadGDaHh7k2bHkkfrvkI_YyCrjbGw==)
9. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHzzjp831Z-Y6PzjLObBE3XrjViFPHThXaj-AIfgCGI94Pu5LZp6QHB4PMKfaCp6TsExs6DRcSztf4s7r4PqCySuMSdJhxe-MFrz2grguSYHwbFtrhF6CWDmvIZ_Z-bCXaMEzM=)
10. [snyk.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFO_QLZe3TBD5eWAhZFRA7IpwZphp-GUQhaanMEpzGSSEsJ7hNsrMrVmZbjhqglF3j5wKD9t3lktCYLU4JkWe4_wZYqKIeaPIYXXw5rBLkOtVkeEspu10eMe8uXeiFpjuBz0x5TzIjBZ1LxIYs=)
11. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEgKUPAikiFxqutC8zhOP1VZLlzpShdnbPcNigr3KDEoyACuD3VKeh7aG1_u6yZVm8uxkFQ9qK1Iq-5du7xb-LpzU102PLgELCIRLbbbT2ysroLp3hZYB99QAD1QkDLTYmapYV01DzyoUezKavnBOzsp-fwTrgQld5HGKKmVC4=)
12. [geminicli.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH6MI9jacxDCpC4HOo54vXzd4qkUJguIkRoLkuQJAhfdjEDWsM04Czyc6erd27pbICSBkXu0wpIr1DcrhMPovevH7YVAaHuaxIn3GFWi954Inkdig8GfWQV1oekq4Q=)
13. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGcvQkgVM5GocGLU97H3k0aGxR5Pnn4Mkh8opLym5jwI4NWtPKjw4l_T4m-cUFseC0gz58j7vnO4_ocHO3dNDfF4ZG99zi0TAqwERx-BjyMDaBJgBtAQHcMCi4PyNKBMJOxHJMvQLVcJ1s2-DzumPy1w-784uuw)
14. [geminicli.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFr6nOASIZeTj1CuzxCqw9ZeRCyM1G8B7fLddT_SR9KA7De_zcDpsAfRM6ryq0gCO4Zhogr7fv8qtuzXo2Gd7ijAO-cRr78E-KVpp0Ndj6J3Uqw2LIthf0BCO-ZAkJzss_378-6PA==)
15. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHjDJqVAUFVRa8jO80kEos1-A3hiSxGVFWabRbDuHjtBDQP1C28-gyKLufgQaj0X7e_H5nGchTvBBqw388XKPsPLNKdghex7LPfseL_B1MTVGfuNXkzXBTGorIxwA4aJS7JKscgea2LhxC5vzATdkvlSKLgQtCYcig=)
16. [google.dev](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFOzS-TZOYtxjLlf953ug3pSY9mpw8UGqFYu3aC4sYLVtJNvEJv61dPkvNRFBY1bI-Zehur-HGd59a1LlweT0PsjMpfqW2WAW63HfkZAjcyanwL70OMaMtajC61bG_xC1XFuj-AkHAqB8OCS2o-)
17. [geminicli.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFn8lgZgVsClw9nAYNVBqcE-bu7x_KGKGMylz_TNOYT6nZJ-C2PkxKAdXsbCIMJl2CdWqqu2puVbG8avjo-XDJa-pu_sVuF1C32_G4r68ogINlXKgV0CbNbDcaEOOhfm2Rm40HL25F5x8E4)
18. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE-zt_pj0BpuGkwOA6GWWI_P1KNa3Be-xJIKg_riDuz2caisSpVWB8hmtqYQgittwL8IRPJ5qfknTRfcfnK2g4BVBMCOwGSFcvx6iBOsEuzBhBhWZYjH4Ps97QspZ8pRwTZCP4nw4Qalg3wcdNC-YWVIRiprDLE-dnVqazA_LiYgbVV)
19. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHMTQyiaJlhyPcbCQ_DkwbIptNen75xbqiIFqXxQO0cfO0k5wH-4NVeIBlmCQDQHfqBnDqCJJNHXbOF7ApWCY3P01t-t0y4uEM6Iq2NwrQhS1bJk-4Sa_7TunuRFFF9n0wOZqpPDWJDHj0oY06N)
20. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH8z6GDmqyKVhNktDjMojHYgg3lcRYfNd3edx-WrRoeFYa8C6F2YecdXRWjvgcVJxDJi1j_ucO9UjXwduBc6A8bgYWC1VHh0bHh3Jgp1QijlrXRImJSepsL9hcpJ_8d86fz5Zxwuq1k-Vt3pVBx)
21. [Link](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZWiGR76UkH3VGlH6iRMxECCBb1lwTHqEqtsGskCgBbxtjJRVhZ9762BR2IugzUs5WEWW7bSPTNt-kaSt2GBaXQ2P1TVek0qDwqBusyBCcsoiuzKiwGcIsByFD2RK5CNz_uYPJGiMoVHotI2UgtRdBwDkXzoU=)
22. [blog.google](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFeuO7wKEwlESx21_mLS1WofzfHpLuSlw0Xav2BZxti_8OYTpW31dJ5bNobDSYw40WbcnKajD0jlKkhvI_e-RXVzg6IXp-AytE5NZbolXkyRlgnE1w--ua0SAYEOJNwKjRVr7a9XaiXmuH1XWAGHgLduVBtCQAS3oOpTIh-DFZL9m8wN8ehpPwIP1ozuDxSzwNE-OapPdo=)
23. [openai.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFBJVAUw4QWTANrJfUKJHSwqXyWP3aCDginV6S-HcbL1xZaZhWGqs1NepOJSn0hga6iiKk89bGVo46mXJmVl75i2S-Eem5epAZek6O4HYYLfPWoSoJUFc0tqfNluy7mcpT9hyv2jHL1KBVFOvAQbA72c1xOu2IS)
24. [google.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFwGJRefUAlNj2PEBDZTSMzKleeZ-tC_6d9ksUh7dptkNXcDfQazpPDylF3bpZQLxDkJnUqvcyhu55UM6_ZxMjh3hvT3_SQ0VYDOY-lK7VGKtI47Hz4NyCtAr1R8s1j6CiqEH2DzQivQ2m7-49N7xEDAhfjIMYel_S--w==)
25. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEurbjmLNqn1xPWiHd_aPEF-42HpukzkBx87knsNb0Hjl-adZABipgX-m1Xv1271MP0igWY_DI-zF5_RReHKKvGXOa1FachEzmHhoYaquFP0_pQ8uImE_b9d7JLRY6INqoFTTjZvrKw8pB-Cz1BqLCYc0451r-53cGlFTfWf3RNuAxpWD_H-rd9_zW3W6B5BAToS0vtKQ==)
26. [Link](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFhHbNPhDtGvgEMaT--AX7OPeh91RlK5vtlw-KiRSf2llm_G8TMP-t1sz1wJRtjovLpKSVFzmGATet2GIPWpHXol_52u6UsuKtvHD8LmFBXfJ2uVtyhxCs=)
27. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEysv4oZ_MakKOaSFBm9PjSZGFPOrGga8QZFNI0yaGdcHI01HXhJCY8-QAS1FoxqZTNJhmIVQ1u3uYl4NlYQklh7L7lE1coR2XwrabC_5zWny4m7G6ZlNWHP_mSHDMwtvKXw3l5UhDVi3sbBhTTDGGY33WniDoEMjyZzKk=)
28. [medium.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGVXFdwNnqh2j6-l6Qbk3nWk3F69IQZaMSn-ZileI1ZsBgCBFnB4r1luww1PWgcDfLWWn7J2oz43zMxfQmY7d4u0cLD34Qdekx5luyVjTzwlYlGTRMg9fB6Pz6KIfOK21rqQA-hts385YhVmlATGUKEx8v-2CmpntZy36tI_Rg0rvf6ZQMqdvv6Cg==)
29. [ycombinator.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFoguqB5nyMd6Pd1bqZy5FKzZ9lqI7j9NP_JAhRPn0oBVY6yFWL-Y8DKmBwP-r6o4zYJpSMdojYQ7Muh-WQriQuhUoIpezeZ60HMb0_5Fa1cHNEhIQy_dlPWjpJDcURetYjJw==)
30. [stackoverflow.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrShj-iQRf5XDiRkCmlu6xn_qG6PIr428ZHLTRmi_oKON9Jk8Fhncsdj4MwoT62udXZlq_nK-HNIUKeHTTn0T_Kgysg7nXoMjQlI502d-hId-CZnGxNiJAu9AQYmnNgwBKLgW3jP-UMwhRJj9tZ8WyEfvUdCzT4m3ZgsNXw9ProL3tvdl6td_M7LCdGVDty1_SkVsVeKxfp-vKT8xVkqh0bAOI6u9i0PqyVdK-X65Uxqle)
31. [github.io](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEsPpFoveuRb5mLT2-SqLbmfvaKRMIeyyLYUMLgaB99VrTjl8VmcNNeTVBptbJZkjRUYpzO4cDZgur5I6Gma0jfqcoyfTEcoaVlLlxMltA-5GUnCuPOoOHcvLdN5PK3OKNU7Fo4_JYOw5BQpsLlPLPqkp6H0Vjrs0-D8xTmow__yjUyFMInBj0zInDCOcCc6HfpbTVPoJ47n9D7vw==)
32. [timhutt.co.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFz0x0lJDiFpQsB0o9fGXlGsewNHD9o1nrc3XG2EVIAwTxIAed_uF8AY0MBMB2lPpamHVKMrdLWXy4OpniLfLn02whZmxG2DKlSMjkvSCKqaSe8lp8C-TiuRxReg7zy3nS4TILt)
33. [reddit.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG19WJ5E5PdsjxAarXfAL3DoKf724q7nBSvF3f1me4HLLQDKKUdPYqkEWpbgCRtPfbCHdWuB3PLMPaIow_ecEUylaybnPaPFqQTaFA9BdbGPMz62ItooiNyZvwbxOsaM9H9BCZoAzx9SQ4x5__nfvTK47FhFyVa5qnFRVcDIOlHrQc3xys3uwIpscwB)
34. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEWiHpytGZIPNJVKprLNVpqjiWMijcfmWM4JUnSqNiR5kCu_EV3eb_cukv3TeuVC2PaaJ9TiovDVeKx2LhTa-_LgEyJ0nJJWrhY3VuWAE2rItekBXtp2hGs9dE_FCDVGA==)
35. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEY4iqTSn7d4wAmcdd98wD6iMI2OTfQXFoJZzGW_uRpbMc9GEBNYTSoKjP48w9c6zUTffVZxV4iVnahKueNBpAM2Re9EbMGhbA2_vl8E4SImLKNaiLwpERPEKV3TvLgISZVNmUANimUjrUMvPcCpJpempr2GVE=)
36. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFpzf-dxAuOLeMgB_n4nTTt6rz9Cf5T3A7GpvzqiI-NQKCeXdkBy2b4n5ZHd0QonGXxHIY7xWLU61_lloJJHq7PT30tAFHqh1U7QZCWdamoXN2TKZviUb-U835oTbY5uBP1595RljdahZvxLZv70-U19Jx_RuJ7wEY=)
37. [lobehub.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE-WBe6kKAsSSsVTfp0QO_Zk17PodD4q_4o11iPTMlVmgoq0BKpTt8-ik1n436Raops-4S7GGaNhNI4DX5UjztOT4Oe8i0VrTT2LrXJ9TEm6nwfWR_HqoW_-Dw-gXauShdGS6FwGDVoDvACT-fjSYWYnLm3oVPXCg==)
38. [dev.to](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG8eRoRVphoPeqxJ_dMXGMRR1e63q_7dvAC7ImS8kI7Ic5d7HYx-hQuODXal28VX7Rkd5i19p5SUZHBdfDVHMqRFUIkzUqucmflaeaTL5iDu5sGXQVI9nuEJ5_HQSK3-tdAOhpdMNXHlPRGays2VujdgjKj3c_Xok_7P-U8-amjx1MGY1b1q6el89mOvsw3QgDF)
39. [davidhamann.de](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFxbBj9eadEIUoS8l26Ey6HexxpW3CKikZXBu_FdM5qo0GVeS9RNHoZ1aaQrafILKgm34bqyzYZQB6yAAc6BUGknroIS3sTeiHda399R6Lpy6u-Lm8RJOT84VCF9Cxl8yx1wVgQuChpY4ao8ok3eZ8Nji9ueg11ajLvP07a)
40. [tonygo.tech](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5hOBBOrR6DQHa9k1gfXXHqTWbiiLfG3bT3NbX2K3mjeq_wXY3npwub8IuDcbiexnzqaxc73hQJtOiLSzkvKAc1YupVt2wz2JblRK-8-32CdpEKUcbed9bDZZMlGOBBXTQH_hVZsPEjuJbbpKw918kRFt0-i_QFlud0t0F)
41. [launchd.info](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUL3nvRVIizJ5ah_gZ4hfr81Mr-cnHCwxmb_Ku0OuqGg8w_wMuBRdNfegtCp6fOMHGBIFppFBnm6_tPAyeOWaZJLhxWBJOGl18wJpOZCQx)
42. [andypi.co.uk](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGNa48hXiUdyeMZsripHlv3226sAj4RKBFgbelrUZk5C8LjW2ImkewExd9wCJi5wLP4uNsa79kd5DiY-rt2BJxW_i7BzqKUhLyBmALEaqJ9xBdfYlYBePPZIo6UUfYEOz1DmL06fQ8jtuyS6ia4ZZZVimoe9Q5qryhGOF9FB6n6NYnyn6gW8Hep)
43. [python.org](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEyjdJbvAIb4sVQtTCgBV5yItwWSGAAtwuIeD82WQLQSBn90hOykadeS_QKRnRnhJyfNySTtH_95-1ByM7_TBjUzwVVgL3RTP6o-UGuXh6Oojk6lrfGk8hWFNdqQtLMLj7aiJ-xkSZ1iaKvhUMGyoeiGNGFa8airHEb62ZtZiZfGoIHLLhOkHioAC9CLa-uTE3s8tWPW0SU1E89)
44. [github.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFAzdIUNFR3ik655pA3WaOFh1RyDcyT5I3FkV4-0WtB_gZNDw69CxJ5wKys42pF0BJpFcwkETF5ZSnM1RLC3y365ohlmxq1MYhBpA5_QGbLPVpOZBcjCZ1LYwsxxJJN9Zf9WzuB-Sk9W5qmw8DqGzwfOH3JHWw_BA==)
45. [apple.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEMVCerR7ZvDi1Sy5JFWV67E-AGOEUsqDuJs3unW51Drs8lXYHaFHppKi71OdZHFhfMe--QkcXqcQUxkVHc-_g8lsY_jbtu24sFTrwV4ZDToO_BwLGRUUWHp33JOc9Sa6dDDjm6NsX8xgS-dnQyXMJX4SzKt6FkcyvUYeBVxTvTb2AUtcZbth4VIAkOXxDpRxa2hbduaUuRk8CWRsFpx8sNfoAR1q2_rsBFBBDGlj6PTRgDpA==)
