---
title: "Use plugins in Claude Cowork"
source: "https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork"
author:
published: 2026-04-09
created: 2026-05-05
description:
tags:
  - "source/web-clip"
type: "source"
status: "unprocessed"
domain:
---
Plugins are available to all Claude Cowork users on paid plans (Pro, Max, Team, Enterprise).

Plugins customize how Claude works for your role, team, and company in Cowork. Each plugin bundles together skills, connectors, and sub-agents into a single package—so instead of setting up each piece individually, you get a ready-to-go setup from the first conversation.

Claude also connects to services like Google Drive, Gmail, Slack, DocuSign, and many more. Plugins can bundle the right connectors for a given workflow so you don't have to set them up individually.

**Note:** Connectors in Cowork reach external services through Anthropic's cloud, not through your local network. Even though Cowork runs on your computer, a custom connector must point to a server that's reachable over the public internet from Anthropic's IP ranges. If your organization's MCP servers are behind a firewall or on a private network, see **[Network requirements for custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp#h_b66e88c454)**.

---

Cowork includes a growing library of plugins for common knowledge work—including sales, finance, legal, marketing, HR, engineering, design, operations, data analysis, and more. Each one comes pre-configured with the skills and connectors relevant to that function.

We also provide **Plugin Create**, a plugin that helps you build custom plugins from scratch.

For the full collection of Anthropic-built plugins, visit **[GitHub](https://github.com/anthropics/knowledge-work-plugins)**.

**Note:** Plugins may include local MCP servers that run on your computer with the same permissions as any other program you run. Only install plugins from sources you trust. If your organization is on an Enterprise plan, your admin may have restricted which plugins you can install, or disabled local MCP servers entirely.

---

1. Open the Claude Desktop app and switch to the “Cowork” tab.
2. Click the “Customize” menu in the left sidebar, which brings together your plugins, skills, and connectors in one place.
3. Click “Browse plugins” to open a modal where you can view all the available options.
4. Click “Install” on your selected plugin.
5. You can also upload a custom plugin file if you've built one yourself or received one from a colleague.

Plugins you add yourself are saved locally to your machine.

[![](https://downloads.intercomcdn.com/i/o/lupk8zyo/2100409211/fc01614dde1a616fa31ffaa9cb04/47bacf5b-a810-45b5-a468-9769f1a58ef8?expires=1778013000&signature=4f4c726ecc1c8d933723f46f8137fd73325ae145859ed6a2dd6a156c07aefe63&req=diEnFs1%2BlINeWPMW1HO4zZF3LR3dMvZVxakFVfq5WwzvD2kYwzGYMQZlwznd%0ATvkKx9uSljXh1Fejcfc%3D%0A)](https://downloads.intercomcdn.com/i/o/lupk8zyo/2100409211/fc01614dde1a616fa31ffaa9cb04/47bacf5b-a810-45b5-a468-9769f1a58ef8?expires=1778013000&signature=4f4c726ecc1c8d933723f46f8137fd73325ae145859ed6a2dd6a156c07aefe63&req=diEnFs1%2BlINeWPMW1HO4zZF3LR3dMvZVxakFVfq5WwzvD2kYwzGYMQZlwznd%0ATvkKx9uSljXh1Fejcfc%3D%0A)

---

Each plugin you install adds Skills you can use while working in Cowork. Type "/" or click the "+" button to see available Skills from your installed plugins.

[![](https://downloads.intercomcdn.com/i/o/lupk8zyo/2157396844/4a790e10f5b88df770783df1d7e9/image.png?expires=1778013000&signature=1526e907bf1b4799bc3fab02c4788b3ca9b024d0e21e2f107e9d16fa5ca54e76&req=diEiEcp3m4lbXfMW1HO4zf4NC%2F78gkOUmKUxugP2BQuL37DsOK%2Fak9bnC%2FZ1%0Appaqd7apr751R0WBISg%3D%0A)](https://downloads.intercomcdn.com/i/o/lupk8zyo/2157396844/4a790e10f5b88df770783df1d7e9/image.png?expires=1778013000&signature=1526e907bf1b4799bc3fab02c4788b3ca9b024d0e21e2f107e9d16fa5ca54e76&req=diEiEcp3m4lbXfMW1HO4zf4NC%2F78gkOUmKUxugP2BQuL37DsOK%2Fak9bnC%2FZ1%0Appaqd7apr751R0WBISg%3D%0A)

---

After installing a plugin, you can tailor it to better fit your workflow:

1. While viewing an installed plugin, click “Customize” in the upper right corner.
2. This opens a new Cowork task with a prompt asking Claude to customize the plugin you chose.
3. Click “Let's go” to start working with Claude to adjust the plugin's Skills and connectors to match how you work.

---

Want to create something from scratch? Cowork includes **Plugin Create**, a built-in plugin that walks you through the process. You can also start from any of the Anthropic-built templates and modify them.

For details on plugin structure and formatting, see the **[Plugins reference](https://code.claude.com/docs/en/plugins-reference)** in our Claude Code docs.

---

If you're on a Team or Enterprise plan, an owner can distribute plugins across your organization through plugin marketplaces. These work the same as any other plugin, with a couple of differences:

- You can't edit organization-managed plugins. This keeps shared tooling consistent across your team.
- Some plugins may be auto-installed or required for you. You can uninstall auto-installed plugins if you don't need them, but required plugins can't be removed.
- Available organization plugins show up when you browse the plugin catalog, and you can install them yourself.

On Enterprise plans, your admin may customize which plugins are available to your group. This means the plugins you see in the catalog may differ from what colleagues in other groups see.

For guidance on setting up and managing plugins organization-wide, see **[Manage Cowork plugins for your organization](https://support.claude.com/en/articles/13837433-manage-cowork-plugins-for-your-organization)**.

---
*Clipped from [claude.com](https://support.claude.com/en/articles/13837440-use-plugins-in-claude-cowork) on 2026-05-05T16:00:25-04:00*
