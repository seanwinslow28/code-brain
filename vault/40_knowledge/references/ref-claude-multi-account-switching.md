---
title: "Managing Multiple Claude Accounts — Claude Conversation"
source: "Claude conversation transcript (2026-04-02)"
created: 2026-05-05
tags:
  - "source/conversation"
  - "claude-account-management"
type: "reference"
status: processed
domain: [claude-mastery]
ai-context: "Saved Claude conversation answering whether/how to run two Claude accounts on the desktop app — same-email Pro+Team switcher works natively; separate emails require browser workaround until multi-account support ships."
---

## You said: The dev team at my company has access to a Claude Max subscription account that the product team is able to access and utilize for our PM tasks.

The dev team at my company has access to a Claude Max subscription account that the product team is able to access and utilize for our PM tasks. Is it possible for me to have 2 Claude accounts and switch between them on the desktop app? Or just in general?

Apr 2

## Claude responded: Good question — let me check the latest on that.

Identified product question and sought current account management details

Identified product question and sought current account management details

Good question — let me check the latest on that.

Consulted search results to address multi-account functionality question

Consulted search results to address multi-account functionality question

Yes, you can absolutely have two Claude accounts. Here's the breakdown:

**On claude.ai (web) and the desktop/mobile apps**, if you have both an individual account and a Team or Enterprise plan account tied to the same email, you can switch between them by clicking your initials in the bottom left corner, then selecting the desired account — a blue checkmark shows which one is active. Each account maintains its own separate conversations and projects. [Claude](https://support.claude.com/en/articles/9267400-can-individuals-with-pro-or-max-plan-accounts-migrate-them-to-team-or-enterprise-plan-organizations)

So the simplest path: if your company's Max subscription is set up as a Team plan and your personal account uses the same email, you'll get a built-in account switcher in the desktop app.

**If the accounts use different emails**, the experience is clunkier — there's no native multi-account switching in the desktop app for separate email accounts yet. That's a frequently requested feature but hasn't shipped. Your workaround options would be using the desktop app for one account and claude.ai in a browser for the other. [GitHub](https://github.com/anthropics/claude-code/issues/30565)

**For Claude Code specifically** (if you end up using it for prototyping), you can point Claude Code to different config directories for each account using the `CLAUDE_CONFIG_DIR` environment variable, so accounts never interfere with each other. But that's a terminal-based workflow, not the desktop chat app. [Medium](https://medium.com/@buwanekasumanasekara/setting-up-multiple-claude-code-accounts-on-your-local-machine-f8769a36d1b1)

**Bottom line for your situation:** Check with Matt or Mike Price on how the team's Max subscription is structured. If it's a Team plan and you can be added with your Block email, you'll get seamless switching in the desktop app alongside your personal account. That's the smoothest setup.

## You said: It's definitely a different email, so the desktop is out for now.

It's definitely a different email, so the desktop is out for now. I'll use the web app for certain tasks. The Claude Code config is definitely what I'd be using the most for prototyping/research/MCP usage etc. Please walk me through that process and how it would work exactly.

Apr 2

## Claude responded: Sure.

Architected beginner-friendly guide for Claude Code configuration setup

Architected beginner-friendly guide for Claude Code configuration setup

Sure. Let me put together a clear walkthrough for you. Since you're on Mac (based on your Claude Code prototyping setup), I'll tailor it accordingly.

The core concept is simple: Claude Code stores your login session and settings in a folder on your computer (by default `~/.claude`). By telling Claude Code to use a _different_ folder for each account, you get completely isolated sessions — separate logins, separate conversation history, separate configs.

Here's the step-by-step:

**Step 1 — Create two separate config directories**

Open your terminal and run:

bash

```bash
mkdir -p ~/.claude-personal ~/.claude-work
```

`mkdir -p` just means "make these folders, and don't complain if they already exist." You're creating two isolated homes for each account's session data.

**Step 2 — Add aliases to your shell config**

You need to edit your shell profile so you can launch each account with a simple command. Run:

bash

```bash
nano ~/.zshrc
```

(Mac uses `zsh` by default. `nano` is a simple terminal text editor — arrow keys to navigate, type to add text.)

Add these lines at the bottom of the file:

bash

```bash
# Claude Code multi-account setup
alias claude-personal="CLAUDE_CONFIG_DIR=~/.claude-personal claude"
alias claude-work="CLAUDE_CONFIG_DIR=~/.claude-work claude"
```

What's happening here: `alias` creates a shortcut command. When you type `claude-work`, it actually runs `claude` but with an environment variable (`CLAUDE_CONFIG_DIR`) pointing to your work-specific config folder. That variable tells Claude Code "use _this_ folder for everything instead of the default."

Save and exit nano: `Ctrl+O` → Enter → `Ctrl+X`

**Step 3 — Reload your shell**

bash

```bash
source ~/.zshrc
```

This reloads the config so your new aliases are available immediately without closing the terminal.

**Step 4 — Log in to each account**

Run each alias once to authenticate:

bash

```bash
claude-personal
```

This opens a browser window — sign in with your personal email. The session gets saved to `~/.claude-personal`. Exit Claude Code (`/exit` or Ctrl+C), then:

bash

```bash
claude-work
```

Sign in with your Block email. Session saves to `~/.claude-work`.

**Step 5 — Use them**

From now on, just launch whichever you need:

bash

```bash
claude-personal   # Your personal Max account
claude-work       # The Block's team account
```

They're completely independent — different sessions, different MCP configs, different conversation histories. You can even run both simultaneously in separate terminal windows.

**One thing to keep in mind for MCP:** Each config directory has its own MCP settings file. So if you've set up Atlassian, Slack, or other MCP servers on your personal account, you'd need to configure them separately in your work account's config too. The MCP config lives inside each respective `~/.claude-[account]/` directory.

**Quick reference once it's set up:**

|Command|Account|Config Location|
|---|---|---|
|`claude-personal`|Your personal email|`~/.claude-personal/`|
|`claude-work`|The Block team email|`~/.claude-work/`|

That's the whole thing. The reason this works so cleanly is that Claude Code was designed to respect that `CLAUDE_CONFIG_DIR` environment variable — it's essentially the same app, just pointing at different "identity folders." Want me to walk through configuring MCP servers for the work account once you've got both set up?

## You said: Can you provide me with a prompt that will have Claude Code execute all of the above for me?

Can you provide me with a prompt that will have Claude Code execute all of the above for me? I'll work on the MCP's later. Also, would I be able to change the launch commands to: claude-sean claude-block

Apr 2

## Claude responded: Absolutely — the alias names are just labels you pick, so claude-sean and claude-block work perfectly.

Synthesized request for executable prompt with personalized command aliases

Synthesized request for executable prompt with personalized command aliases

Absolutely — the alias names are just labels you pick, so `claude-sean` and `claude-block` work perfectly. Here's a prompt you can paste directly into Claude Code:

---

**Prompt:**

> Set up multi-account support for Claude Code on my Mac. I need two separate accounts with isolated config directories and shell aliases. Here's exactly what I need:
> 
> 1. Create two config directories: `~/.claude-sean` and `~/.claude-block`
> 2. Add the following aliases to my `~/.zshrc` file (append them, don't overwrite anything existing):
> 
> ```
> # Claude Code multi-account setup
> alias claude-sean="CLAUDE_CONFIG_DIR=~/.claude-sean claude"
> alias claude-block="CLAUDE_CONFIG_DIR=~/.claude-block claude"
> ```
> 
> 3. Source `~/.zshrc` to reload the config
> 
> Before making any changes, show me what you plan to do and ask for confirmation. After completing, verify the aliases are available by running `type claude-sean` and `type claude-block`.

---

The "show me what you plan to do and ask for confirmation" line is important — it prevents Claude Code from just running commands without letting you review first, which is a good habit anytime you're modifying shell config files.

After it completes, you'll need to run `claude-sean` and `claude-block` one time each to authenticate with the browser login. Then you're good to go.