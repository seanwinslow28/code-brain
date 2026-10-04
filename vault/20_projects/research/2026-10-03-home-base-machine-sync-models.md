---
title: "Home base, machine sync, and models for the brain redesign"
date: 2026-10-03
source: claude-agent-research
status: draft
---

# Home base, machine sync, and models for the brain redesign

## What this means for the redesign

1. **Always-on Mini:** set sleep to never and "Start up when power is connected" to Always (macOS 26.5+). Then decide FileVault vs. auto-login on purpose, because you can't have both. Add a dead-man's-switch ping per scheduled job and a small USB-connected UPS.
2. **Remote access:** install Tailscale (Standalone variant) on both Macs and use ordinary macOS Remote Login (SSH) over the tailnet. Before blaming the network for today's "No route to host," check the macOS Local Network permission for the terminal app.
3. **Sync:** use git only, with a private remote as the hub. Agents on the Mini pull with rebase, commit and push. The laptop auto-pulls. Do not layer iCloud, Syncthing or Obsidian Sync on the same folder.
4. **Grunt models:** on a 24GB Mini, keep small local models (Gemma 4 E4B, gpt-oss-20b, a small embedder). Send anything bigger to cheap hosted open-weight APIs, but only for non-private content. The routing table keys on privacy class first and cost second.
5. **Shared entry point:** make AGENTS.md the canonical instruction file, with CLAUDE.md importing it. The substrate is plain markdown plus git. One MCP server over the vault, running on the Mini, serves local tools. Cloud guests (Dots, Muse) get in only through GitHub or a tunnelled MCP endpoint, and they write to an inbox or branch, never straight to main.
6. Jev is a stateless classifier you call, not a guest that reads the brain. Use it (or a local decision model) inside the router, never as a store.
7. The biggest single-point risk is not the model or the sync. It is a power blip that leaves the Mini sitting at a FileVault unlock screen, so every agent fails silently. Solve that first.
8. An M5 Mini with 48GB or more would unlock Ollama's MLX backend (the preview needs more than 32GB) and the 35B-class MoE models the laptop runs today. That makes the "no laptop dependency" rule cheap to keep.
9. Dots, Muse and Jev all launched in the last four weeks; treat their capability claims as moving targets.
10. See Open questions for what to verify by hand before locking anything.

---

## 1. Always-on reliability of a Mac Mini

**Power and sleep.** Apple added a dedicated setting for Mac mini (2024 or later) on macOS 26.5+: System Settings > Energy > "Start up when power is connected" > Always. The Mac turns on whenever power returns after an outage [B: Apple Support 125517, 2026-06-15]. The command-line equivalents are `pmset -a sleep 0`, `autorestart 1` and `womp 1` [C: hometechops, reviewed 2026-06-02; C: nordicsilicon 2026 guide].

**The FileVault trap.** LaunchAgents and anything reading the login Keychain need a logged-in session, and auto-login is unavailable while FileVault is on, so after an outage a FileVault Mini waits at the unlock screen [C: hometechops]. macOS 26+ on Apple silicon can unlock FileVault over pre-boot SSH if Remote Login was on before the restart; that session only unlocks, it gives no shell [C: korben.info; C: texarxs; D: MacRumors forum]. But Tailscale isn't running pre-boot (§2), so this works only from the home LAN or via another always-on LAN device. Options:
- (a) Turn FileVault off on the Mini and turn auto-login on. Keep secrets in the Keychain and keep the Mini physically secure.
- (b) Keep FileVault and accept that an outage while you travel means a manual unlock.
- (c) Keep FileVault, run agents as LaunchDaemons (which start at boot with no session), and move credentials out of the login Keychain. Your agents currently resolve their OAuth token from the Keychain, so this option needs rework.

**launchd** remains the native scheduler; no 2026 source suggests replacing it. LaunchDaemons run at boot without a session; LaunchAgents and GUI apps need a logged-in user [C: hometechops server setup].

**Health checks and alerting.** Watch for silence, not just errors: Healthchecks.io-style monitors alert when an expected ping misses its grace window, which catches a dead machine, a launchd job that never fired, or a hang [B: Healthchecks.io docs]. The free tier is reported as 20 checks [C: dev.to; UNVERIFIED on the vendor page]. Give each nightly job one check (ping `/start`, then success or `/fail`), plus a 5-minute machine heartbeat. A self-hosted monitor on the Mini can't report the Mini being down, so the watcher must live off-box.

**UPS.** macOS reads a USB-HID UPS natively and exposes shutdown thresholds (`pmset -g ups`: haltlevel, haltafter, haltremain) [C: Macworld; C: Eclectic Light]. A UPS turns short blips into nothing and long outages into a clean shutdown followed by auto power-on. With option (a) above, the Mini then recovers unattended.

## 2. Remote access while traveling

**Tailscale (WireGuard mesh)** is the default answer for SSH and for reaching local services such as Ollama, an MCP server or dashboards. Nothing is exposed publicly, there is no port forwarding, and MagicDNS names work the same at home and away [C: Webteractive 2026; C: needtoknowit 2026]. The free Personal plan covers up to 6 users with unlimited personal devices, plus subnet routers, MagicDNS and ACLs [B: Tailscale pricing, retrieved 2026-10-03]. Two macOS details matter [B: Tailscale KB "macOS variants", validated 2026-01-05]:
- Only the open-source `tailscaled` variant can act as a **Tailscale SSH server** or run **before user login**. Tailscale recommends it only for experienced administrators.
- The recommended **Standalone** app does neither. On the Mini, run Standalone and use Apple's own Remote Login (OpenSSH) over the tailnet IP or MagicDNS name. That needs auto-login (§1 option a) so Tailscale is up after a reboot.

**Cloudflare Tunnel** is a reverse tunnel built HTTP-first. SSH works through `cloudflared access`, the Cloudflare One client, or a terminal rendered in the browser, with Access policies and short-lived certificates [B: Cloudflare docs, updated 2026-04-17]. All traffic passes through Cloudflare's edge, whereas Tailscale's coordination server sees metadata only [C: needtoknowit; C: intellizu]. Use it only when something must be reachable at a **public HTTPS URL**, for example an MCP endpoint for a cloud guest (§5). Always put Access authentication in front of it.

**OpenAI Secure MCP Tunnel** is an outbound-only client (Apache-2.0, runs on macOS) that connects a localhost MCP server to ChatGPT, Codex, the Responses API and AgentKit with no public listener [B: openai/tunnel-client]. Built-ins (Remote Login, Screen Sharing) ride on top of any of these.

**Today's "No route to host."** On macOS 15+, a missing **Local Network privacy** permission produces exactly this error; grant or toggle the terminal app under Privacy & Security > Local Network (sometimes a reinstall is needed) [D: Homebrew discussion #6076; D: JetBrains IJPL-160490; C: vdaluz.com]. Apple DTS also names a second cause: a route that isn't up yet just after wake [B: Apple Developer Forums 765513]. Check both before redesigning anything. Tailscale fixes the "away from home" half either way.

## 3. Two-machine sync of the repo and vault

**What is known to break:**
- **Git inside iCloud Drive.** iCloud treats `.git` internals as documents. It renames conflicting refs with a " 2" suffix and has been seen turning `.git` into a non-folder file [C: Archit Chandra; C: LSyncer; D: micro.blog]. Never do this.
- **Obsidian Sync alongside another sync service.** Obsidian warns against it outright and says "double-syncing" can make files disappear [B: Obsidian Help, Switch and Troubleshoot]. Obsidian Sync merges markdown with diff-match-patch and uses last-modified-wins for other files. Since v1.9.7 it can write conflict copies instead [B: Obsidian Help, Troubleshoot]. Its headless CLI (`ob sync --continuous`, open beta) is built for agents, but Obsidian also says to run only one sync method per device [B: Obsidian Help, Headless Sync].
- **Syncthing.** It renames the older side of a conflict to `.sync-conflict-<date>-<time>-<device>` and propagates that file to every peer [B: Syncthing docs]. That is safe for notes but wrong for `.git`, where ref and lock files then diverge. The Syncthing FAQ is silent on git, so this is an inference.
- **Obsidian Git with auto-pull** can push past conflicts without surfacing them [D: Hacker News 36610268]. Ignore `.obsidian/workspace*.json` so layout churn stops causing conflicts [C: 21obsidian].

**Recommendation: git only, with a private remote as the hub.**
- **Mini agents.** Each run does `git pull --rebase --autostash`, writes, commits and pushes; a rejected push retries once, then fails loudly through the health check. Agents write to **their own files or folders** so they rarely touch lines you edit.
- **Append-only logs.** For files several writers append to (tickets list, daily log), consider the `merge=union` driver in `.gitattributes`. Git documents that it keeps lines from both sides "in random order" and says to verify the result [B: git-scm gitattributes]. Use it only where line order doesn't matter.
- **Laptop.** Auto-pull on open and on a timer, auto-commit on a short interval (Obsidian Git or a launchd script); a real conflict halts visibly instead of overwriting.
- **Phone, later.** Obsidian Sync as the only engine on a separate capture vault that a Mini job imports into git. Never two engines on one folder.

## 4. Models for grunt work

**What fits in 24GB.** macOS reserves part of unified memory for itself, so a model that downloads at 17–24GB leaves no room for context.
- **Qwen3.6-35B-A3B** (Apache-2.0, released 2026-04-16, 3B active parameters) "loads on 24GB but with little room for long prompts" [B: Qwen blog; C: modelfit.io; C: aminrj.com]. It is the laptop's current fleet model, and it is borderline on the Mini.
- **Gemma 4** (2026-04-02, Apache-2.0) comes in E2B, E4B (128K context), a 26B-A4B MoE and a 31B dense model [B: Google blog; C: labellerr]. E4B is reported at about 57 tok/s on M4-class hardware [C: modelfit/compute-market, UNVERIFIED on your hardware]. It is a good fit for triage and tagging, and your fleet already uses it.
- **gpt-oss-20b** loads in about 14GB at an estimated 18–24 tok/s on an M4 [C: modelfit.io, estimate]. It is the strongest summarizer that fits with headroom.
- **Embeddings:** Qwen3-Embedding-0.6B is reported as the best quality per GB (about 1.5GB). nomic-embed-text (about 0.3GB, which you already run) remains fine [A: Qwen3 Embedding arXiv 2506.05176; C: morphllm].

**Runtime.** Ollama's MLX backend roughly doubled decode speed (58 to 112 tok/s on an M5 Max) but **requires more than 32GB of unified memory** [B: Ollama blog, 2026-03-30]. Later gains such as MTP for Gemma 4 (2026-06-29) were also measured on an M5 Max [B: Ollama blog]. On the 24GB Mini, expect the llama.cpp/GGUF path. This is the strongest hardware argument for a 48–64GB M5 Mini.

**Local decision models.** Ollama added a Jev-compatible `/v1/systemone` endpoint with local "decision models" (Nimble 9B, Tev1 4B and 0.8B). They return typed choice, boolean and score answers. Nimble averaged about 91ms per decision on an M5 Max [B: Ollama blog, 2026-09-29]. That makes a $0 local router classifier possible.

**Hosted open-weight prices.** These are live OpenRouter list prices, retrieved 2026-10-03, in USD per million tokens (input/output) [B: OpenRouter models API]:

| Model | Input/output per 1M tokens | Context |
|---|---|---|
| deepseek-v4-flash | $0.028 / $0.056 | 1M |
| gpt-oss-20b | $0.018 / $0.09 | 131K |
| gemma-4-26b-a4b | $0.068 / $0.225 | 262K |
| nemotron-3.5-lightning | $0.059 / $0.17 | 262K |
| qwen3.6-35b-a3b | $0.15 / $1.00 | 262K |

Some free variants may retain prompts for training [B: OpenRouter listing text]. A night of 1M input and 100K output tokens costs about 3–15 cents. Hosted wins on speed, long context and models that won't fit; local wins on privacy and zero marginal cost. Same weights, same quality.

**How a router chooses.** The pattern your config already follows holds up, in this order:
1. **Privacy class decides first.** Private or SOUL-derived content never leaves the house, so it stays local or is deferred.
2. **A deterministic task map** picks the default route per task.
3. **Escalation on evidence:** a schema-validation failure or low confidence escalates to hosted open-weight, then to frontier.
4. **A hard cost cap with `fallback = none`** applies where a surprise bill is worse than a deferral.

Typed decision models fit step 3. Vercel AI Gateway shows the pattern directly: evaluation fallbacks rerun a Jev answer on a frontier model when `confidenceBelow` a threshold [B: Vercel docs, updated 2026-09-21]. OpenRouter also listed a "TypeSafe: Jev Router" on 2026-09-25 that picks a model and reasoning effort per request. Its pricing is unlisted [B: OpenRouter models API], so treat it as an experiment, not the backbone.

## 5. The tool-neutral entry point

**Current practice:**
- **AGENTS.md** is the cross-tool standard, now stewarded by the Agentic AI Foundation under the Linux Foundation. The nearest file in the directory tree wins, and Codex, Jules, Cursor, Copilot and 20+ other tools read it [B: agents.md].
- **Claude Code** reads AGENTS.md from v2.1.277. By default it reads AGENTS.md **only when no CLAUDE.md exists**. To share one file, have CLAUDE.md import `@AGENTS.md`, or set Project instructions to `claude-md-and-agents-md` [B: Claude Code docs, memory page].
- **MCP** (spec revision 2026-07-28) supplies tools and resources over JSON-RPC, adds extensions such as Tasks and Skills-over-MCP, and requires user consent for each tool [B: modelcontextprotocol.io].
- **The consensus shape:** plain markdown plus git as the truth, AGENTS.md as the map, and an MCP server as the typed doorway for tools that cannot touch the filesystem. Vault MCP servers are plentiful but come mostly from community sources [C/D: glama, morphllm].

**Guest by guest:**

| | Reads/writes external files | MCP | Callable via API | Where its memory lives |
|---|---|---|---|---|
| **Claude Code, Codex** (local) | Yes, directly on the working copy | Yes | Yes (CLI/SDK) | Repo files and its own memory dirs |
| **OpenAI Dots** (2026-09-29; first dot included with Pro) | Via connectors: Google Drive, GitHub (issues, PRs), opt-in "connected computer" while the desktop app is open [C: Flavio Copes; C: DataCamp] | 4,000+ plugin apps. Custom MCP for dots **UNVERIFIED** (ChatGPT itself supports it via Developer Mode and Secure MCP Tunnel) | **No** dots API; the GPT-6 Astra model has one [C: DataCamp] | Own saved notes plus ChatGPT memory; not editable one by one, reset by deleting the dot [C: Flavio Copes] |
| **Meta Muse** (2026-09-08; Free/$20/$100) | Browser, email, built-in connectors (GitHub reported [C: TinyFish]); any public API with your credentials [C: TechCrunch] | **Conflicting**: builds its own HTTP MCP client [C: Parallel] vs. no MCP-URL field in consumer app [C: TinyFish]. Local servers unreachable either way | **No** agent API [C: Parallel]; Muse Spark model API exists [B: Meta AI blog] | "Muse Secure VM"; user-key Confidential VM promised later in 2026 [B: Meta newsroom] |
| **Jev** (TypeSafe; early access 2026-09-15) | **No**; stateless state-in, typed-probabilities-out | No | **Yes**: TypeSafe API, Vercel AI Gateway (`typesafe-ai/jev`), OpenRouter Jev Router; $0.042/1M input, output free, 70–500ms [B: TypeSafe; B: Vercel] | None; hosted only, no weights [C: TrueFoundry] |

**Design implication.** Local harnesses read the repo directly. Dots can reach the brain today through the **GitHub connector on the private repo**, which doubles as a pull-request review gate. Muse is aimed at personal-life tasks: give it a narrow, authenticated remote MCP endpoint or nothing. Jev is a function the router calls. Dots and Muse keep memory you can't fully inspect, so "the brain is the truth" needs a write-back rule: anything durable gets committed or PR'd, or it dies with the dot or VM.

---

## Open questions

1. Can a dot use a custom MCP connector, including one behind Secure MCP Tunnel? Test this directly in ChatGPT Pro.
2. Does Meta Muse accept a user-supplied MCP URL in the consumer app? Check the Meta Help Center page on custom connectors.
3. FileVault on the Mini: option a, b or c from §1? This decides whether Tailscale and the agents survive an unattended reboot.
4. Will Ollama's MLX backend support machines with 32GB or less before the M5 Mini purchase? The 2026-03-30 requirement may have moved.
5. Real tok/s for gpt-oss-20b and Gemma 4 E4B on *this* Mini. All figures above are third-party estimates.
6. Was today's SSH failure the Local Network permission, the mDNS name, or the network? A one-minute check settles it.
7. What does Jev Router cost on OpenRouter, and what data-retention terms apply?

## Sources

Tiers: A academic, B primary, C trade press or vendor blog, D forum or social.

- [B] Apple Support, "Turn on a Mac mini… without pressing its power button" (125517), 2026-06-15. https://support.apple.com/en-us/125517
- [B] Apple Developer Forums thread 765513 (DTS on "No route to host"), undated. https://developer.apple.com/forums/thread/765513
- [C] hometechops, "Mac mini auto power on after a power failure (Tahoe / 27)", reviewed 2026-06-02. https://hometechops.com/mac/mac-mini-auto-power-on-restart-tahoe
- [C] hometechops, "Set up a Mac mini as an always-on home server", 2026. https://hometechops.com/mac/mac-mini-home-server-setup
- [C] nordicsilicon, "Mac Mini as a Server: Complete 2026 Setup Guide", 2026. https://nordicsilicon.io/blog/mac-mini-as-a-server
- [C] Korben, "macOS Tahoe – FileVault can finally be unlocked remotely", 2025 (background). https://korben.info/en/macos-tahoe-filevault-remote-unlock.html
- [C] texarxs, "Unlocking FileVault over SSH in macOS Tahoe", 2025–26. https://texarxs.com/blog/unlocking-filevault-over-ssh-in-macos-tahoe-a-game-changer-for-remote-mac-administration/
- [D] MacRumors forum, "A pretty major overlooked improvement in Tahoe for remote systems", 2025 (background). https://forums.macrumors.com/threads/a-pretty-major-overlooked-improvement-in-tahoe-for-remote-systems.2466335/
- [B] Healthchecks.io docs, "Monitoring cron jobs", undated. https://healthchecks.io/docs/monitoring_cron_jobs/
- [C] dev.to / serverkueche, "Healthchecks: monitor cron jobs" (free-tier claim), 2026. https://dev.to/serverkueche/healthchecks-monitor-cron-jobs-backups-dead-mans-switch-2oo1
- [C] Macworld, "How to configure shutdown settings with a UPS on a Mac", undated. https://www.macworld.com/article/828279/how-to-configure-shutdown-settings-with-a-ups-on-a-mac.html
- [C] Eclectic Light, "Power management in detail: using pmset", 2017 (background). https://eclecticlight.co/2017/01/20/power-management-in-detail-using-pmset/
- [B] Tailscale KB, "macOS variants", validated 2026-01-05. https://tailscale.com/kb/1065/macos-variants
- [B] Tailscale pricing, retrieved 2026-10-03. https://tailscale.com/pricing
- [C] Webteractive, "Tailscale: How I reached my Mac mini without exposing a single port", 2026. https://webteractive.co/blog/tailscale-how-i-reached-my-mac-mini-without-exposing-a-single-port
- [C] needtoknowit, "Tailscale vs Cloudflare Tunnel (2026)", 2026. https://needtoknowit.com.au/blog/tailscale-vs-cloudflare-tunnels-for-remote-access/
- [C] intellizu, "Cloudflare Tunnel vs Tailscale", undated. https://intellizu.com/articles/cloudflare-tunnel-vs-tailscale/
- [B] Cloudflare docs, "SSH" (Cloudflare One), updated 2026-04-17. https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/use-cases/ssh/
- [B] openai/tunnel-client (Secure MCP Tunnel), GitHub, retrieved 2026-10-03. https://github.com/openai/tunnel-client
- [D] Homebrew discussion #6076, "ssh can't access LAN on macOS Sequoia", 2024–25 (background). https://github.com/orgs/Homebrew/discussions/6076
- [D] JetBrains YouTrack IJPL-160490, "no route to host on LAN under macOS 15", 2024 (background). https://youtrack.jetbrains.com/issue/IJPL-160490/no-route-to-host-on-LAN-under-macOS-15
- [C] vdaluz.com, "macOS said 'no route to host', and it meant 'permission denied'", undated. https://vdaluz.com/blog/macos-local-network-permissions-no-route-to-host
- [B] Obsidian Help, "Switch to Obsidian Sync", undated. https://obsidian.md/help/sync/switch
- [B] Obsidian Help, "Troubleshoot Obsidian Sync", undated (references v1.9.7). https://obsidian.md/help/sync/troubleshoot
- [B] Obsidian Help, "Headless Sync" (open beta; changelog 2026-02-27). https://obsidian.md/help/sync/headless
- [B] Syncthing docs, "Understanding synchronization: conflicting changes", undated. https://docs.syncthing.net/users/syncing.html
- [B] git-scm, gitattributes ("union" merge driver), current. https://git-scm.com/docs/gitattributes
- [C] Archit Chandra, "A side effect of storing a Git repository in iCloud Drive", undated. https://architchandra.com/articles/a-side-effect-of-storing-a-git-repository-in-icloud-drive
- [C] LSyncer blog, "Git repository in iCloud Drive", 2026. https://lsyncer.syntanea.com/blog/git-repository-icloud-drive/
- [D] micro.blog post on git in iCloud, undated (background). https://micro.blog/7robots/61307238
- [D] Hacker News thread 36610268 (Obsidian Git conflicts), 2023 (background). https://news.ycombinator.com/item?id=36610268
- [C] 21obsidian, "Obsidian Git sync tutorial", 2026. https://21obsidian.com/en/blog/obsidian-git-sync
- [B] Qwen blog, "Qwen3.6-35B-A3B", 2026-04-16. https://qwen.ai/blog?id=qwen3.6-35b-a3b
- [C] modelfit.io, "Qwen 3.6 on Mac" and "Best LLMs for Mac Mini M4 24GB", 2026. https://modelfit.io/blog/qwen-36-on-mac/ · https://modelfit.io/blog/best-llm-mac-mini-m4-24gb/
- [C] aminrj.com, "Qwen3.6 on 24GB VRAM", 2026. https://aminrj.com/posts/llamacpp-qwen36-35b/
- [B] Google blog, "Gemma 4", 2026-04-02. https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- [C] Labellerr, "Google Gemma 4: a technical overview", 2026. https://www.labellerr.com/blog/gemma-4-open-weight-ai-model-overview/
- [C] compute-market, "Mac Mini M4 for AI 2026", 2026. https://www.compute-market.com/blog/mac-mini-m4-for-ai-apple-silicon-2026
- [A] Qwen team, "Qwen3 Embedding" (arXiv 2506.05176), 2025 (background). https://arxiv.org/pdf/2506.05176
- [C] morphllm, "Best Ollama embedding models 2026", 2026. https://www.morphllm.com/ollama-embedding-models
- [B] Ollama blog, "Ollama is now powered by MLX on Apple Silicon in preview", 2026-03-30. https://ollama.com/blog/mlx
- [B] Ollama blog, "Faster Gemma 4 on MLX with multi-token prediction", 2026-06-29. https://ollama.com/blog/faster-gemma-4-mlx-mtp
- [B] Ollama blog, "Muse Glimmer…", 2026-08-10. https://ollama.com/blog/muse-glimmer
- [B] Ollama blog, "Ollama now supports Jev-style decision models", 2026-09-29. https://ollama.com/blog/ollama-now-supports-jev-style-decision-models
- [B] OpenRouter models API (prices, Jev Router entry), retrieved 2026-10-03. https://openrouter.ai/api/v1/models
- [B] OpenAI, "Introducing dots", 2026-09-29 (page returned 403; claims taken via search snippet and secondary sources). https://openai.com/index/introducing-dots/
- [C] Flavio Copes, "A deep dive into OpenAI dots", 2026-09-30. https://flaviocopes.com/openai-dots/
- [C] DataCamp, "OpenAI Dots: always-on agents in ChatGPT, explained", 2026-09/10. https://www.datacamp.com/blog/openai-dots
- [C] InfoQ, "OpenAI DevDay 2026 recap", 2026-10-02. https://www.infoq.com/news/2026/10/openai-devday-2026/
- [B] OpenAI Help, "Developer mode and MCP apps in ChatGPT", undated (not fetched; 403). https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
- [B] Meta Newsroom, "Introducing Muse", 2026-09-08. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- [C] TechCrunch, "Meta debuts its Muse AI agent", 2026-09-08. https://techcrunch.com/2026/09/08/meta-debuts-its-muse-ai-agent-will-consumers-trust-it/
- [B] Meta AI blog, "Introducing Muse Spark 1.1", 2026-07-09. https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/
- [C] Parallel, "Meta Muse custom integrations", mid-September 2026. https://parallel.ai/articles/meta-muse-custom-integrations
- [C] TinyFish, "Best MCP servers and connectors for Meta Muse", 2026-09-30 (vendor). https://www.tinyfish.ai/blog/best-mcp-servers-for-meta-muse
- [B] TypeSafe AI, "Introducing System One Models & Jev", 2026-09-15. https://typesafe.ai/blog/introducing-system-one-models-and-jev
- [B] Vercel docs, "TypeSafe API with AI Gateway", updated 2026-09-21. https://vercel.com/docs/ai-gateway/sdks-and-apis/typesafe
- [C] TrueFoundry, "TypeSafe AI's Jev", 2026-09-18. https://www.truefoundry.com/blog/typesafe-ai-jev
- [B] agents.md (Agentic AI Foundation), retrieved 2026-10-03. https://agents.md/
- [B] Claude Code docs, "How Claude remembers your project" (AGENTS.md section), retrieved 2026-10-03. https://code.claude.com/docs/en/memory
- [B] Model Context Protocol specification, revision 2026-07-28. https://modelcontextprotocol.io/specification/latest
- [C/D] glama.ai Obsidian MCP server directory, 2026. https://glama.ai/mcp/servers/integrations/obsidian
