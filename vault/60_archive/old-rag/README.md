# RAG Knowledge Chunks

Store RAG-ready documents here for retrieval-augmented generation via MCP.

## Format Guidelines
- Keep each file focused on one topic
- Use clear headings and structure
- Include metadata in frontmatter (title, tags, domain)
- Aim for 500-2000 tokens per chunk for optimal retrieval
- Use markdown formatting for consistency

## How It Works
1. Add knowledge documents to this directory
2. Configure an MCP server (e.g., obsidian-mcp) to index this vault
3. Claude Code can then retrieve relevant context during conversations

## File Naming
`{domain}-{topic}.md` — e.g., `pm-sprint-planning.md`, `gamedev-phaser-scenes.md`
