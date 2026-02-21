---
name: figma-to-code-workflow
description: Figma-to-code conversion workflow using MCP servers. Extract design tokens, map Figma components to code, maintain design fidelity, and use icon library MCP servers (Lucide, Iconify, Icons8). Use when implementing designs from Figma, setting up Figma MCP server, extracting design tokens, finding icons, or maintaining design-code consistency.
---

# Figma-to-Code Workflow

## Purpose

Convert Figma designs to code using MCP server integrations for structured data extraction instead of pixel-guessing. Maintain fidelity through semantic token mapping, component reuse detection, and automated visual comparison.

## When to Use

- Implementing a component or page from a Figma design file
- Setting up Figma MCP server for Claude Code access
- Extracting design tokens (colors, spacing, typography) from Figma
- Finding the right icon from a library without hallucinating SVGs
- Establishing a feedback loop between design and code

## Examples

**Example 1: Implementing a Figma design**
```
User: "Implement this card from my Figma file [link]"
Claude: [Uses figma-to-code-workflow] Calls get_design_context for layout
metadata, get_variable_defs for tokens, get_code_connect_map to find
existing Button component in src/components/ui. Generates code using
project tokens, not hardcoded hex values.
```

**Example 2: Finding icons**
```
User: "I need a settings icon for this nav bar"
Claude: [Uses figma-to-code-workflow] Calls lucide-icons MCP search_icons
for "settings". Returns: import { Settings } from 'lucide-react'.
No hallucinated SVG paths.
```

## Figma MCP Server Setup

### Configuration

Add to your MCP client config (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your_figma_access_token"
      }
    }
  }
}
```

Requirements: Figma Desktop App, Dev Mode seat (Full or Dev seat on paid plans).

### Available Tools

| Tool | Purpose |
|---|---|
| get_design_context | Component hierarchy and styling (defaults to React + Tailwind) |
| get_variable_defs | Design tokens: colors, spacing, typography |
| get_code_connect_map | Links Figma components to existing code components |
| get_screenshot | Visual screenshot for comparison |

## Design-to-Code Conversion Workflow

### Step 1: Link and Fetch
Paste a Figma link. Call `get_design_context` to pull the node metadata.

### Step 2: Map Components
Call `get_code_connect_map` to check if a "Button" in Figma already exists as `src/components/Button.tsx`. Import the existing component instead of generating new JSX.

### Step 3: Apply Tokens
Call `get_variable_defs` to replace raw hex values with project CSS variables or Tailwind utilities.

### Step 4: Generate Code
Assemble the layout using existing components and tokens.

### Prompt Pattern for Fidelity

```
Implement the design at [Figma Link]. Use get_variable_defs to ensure all
colors and spacing use our design tokens. Check get_code_connect_map to
reuse existing components from @/components/ui. Do not hardcode hex values.
```

## Token Extraction Best Practice

Structure tokens with semantic intent so the AI knows WHEN to use them.

Bad: `blue-500: #0000FF` (AI cannot infer usage)
Good: `color.feedback.error: #FF0000` (AI knows this is for error states)

If legacy tokens lack semantic naming, create a companion file:

```markdown
# Token Usage Rules
- Buttons: Always use spacing-component-button-padding (not generic space-4)
- Errors: Use color-feedback-error for borders and text in validation states
- Dark Mode: Rely on [data-theme='dark'] alias resolution in tokens/semantic.json
```

## Icon Library MCP Servers

### Lucide (Open Source, React-optimized)

```json
"lucide-icons": {
  "command": "npx",
  "args": ["lucide-icons-mcp", "--stdio"]
}
```

Usage: "Find a settings icon" calls `search_icons` and returns:
`import { Settings } from 'lucide-react'`

### Iconify (150+ icon sets)

```json
"better-icons": {
  "command": "npx",
  "args": ["-y", "better-icons"]
}
```

Accesses Material, FontAwesome, Carbon, and more. Can auto-write SVG/Component to file.

### Icons8 (High fidelity)

```json
"icons8mcp": {
  "command": "npx",
  "args": ["mcp-remote", "https://mcp.icons8.com/mcp/"]
}
```

High-res PNGs (free) and specialized styles (3D, animated).

## CLAUDE.md Rules for Figma Fidelity

Add these rules to maintain design consistency:

```markdown
## Figma Implementation Flow
1. Fetch: Always run get_design_context on the provided Figma node ID
2. Context: Run get_variable_defs to identify required tokens
3. Map: Use get_code_connect_map to identify reusable React components
4. Verify: Compare rendered output with get_screenshot from Figma

## Styling Rules
- NEVER hardcode magic numbers (e.g., padding: 13px). Match nearest token
- Typography: Use semantic classes (text-display-lg) over raw font sizes
- Icons: Always use the lucide-icons MCP tool; do not generate raw SVG paths
```

## Maintaining Fidelity

### Visual Comparison Agent
1. Agent A generates code
2. Agent B renders it and takes a screenshot (via Playwright MCP)
3. Agent C compares the screenshot with the Figma screenshot from `get_screenshot`
4. Agent C reports specific discrepancies

### Bi-directional Token Sync
Use GitHub Actions to sync Figma variable changes to `tokens.json`, which regenerates CSS variables. Source of truth remains Figma.

## Success Criteria

- [ ] Figma MCP server is configured with access token
- [ ] Code uses get_variable_defs tokens, not hardcoded values
- [ ] Existing components are reused via get_code_connect_map
- [ ] Icons come from MCP server search, not hallucinated SVG
- [ ] CLAUDE.md includes Figma implementation flow rules

## Copy/Paste Ready

```
"Implement this design from Figma [paste link]"
"Extract the design tokens from my Figma file"
"Set up the Figma MCP server for Claude Code"
"Find an icon for [description] using the icon library"
"Match this component to the Figma design exactly"
```
