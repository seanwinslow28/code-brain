## Adobe Creative Cloud Automation

Adobe app automation via the adb-mcp server. Two-layer system: Creative Director plans and critiques, then app-specific skills execute via MCP tool calls.

### Available Skills
- **creative-director**: Plan creative projects, propose routes, critique work-in-progress, generate handoff docs
- **adobe-photoshop-mcp**: Image editing, compositing, sprite sheets, generative fill via UXP plugin
- **adobe-premiere-mcp**: Video editing, timeline assembly, transitions, audio, export via UXP plugin
- **adobe-aftereffects-mcp**: Motion graphics, animation, keyframes, expressions, ExtendScript via CEP plugin
- **adobe-illustrator-mcp**: Vector graphics, SVG export, icon sets, character sheets, ExtendScript via CEP plugin
- **adobe-cross-app-workflows**: Cross-app pipelines, MCP architecture, shared guardrails, troubleshooting

### Architecture
```
Claude Code <-> MCP Server (Python, stdio) <-> Proxy Server (Node.js, WebSocket) <-> Adobe Plugin <-> Adobe App
```

### Conventions
- Small-batch execution: 2-3 operations, then pause for verification
- Non-destructive patterns: masks over erasers, adjustment layers over direct adjustments
- Naming: `YYMMDD_ProjectName_Element_v01`
- Checkpoint reviews at 30% (concept), 60% (structure), 90% (polish)
