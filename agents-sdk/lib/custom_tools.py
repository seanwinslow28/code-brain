"""Custom MCP tools for autonomous agents.

These tools are registered as in-process MCP servers via the Agent SDK's
create_sdk_mcp_server() function, giving Claude access to domain-specific
operations during autonomous runs.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

from .vault_io import inject_at_anchor


@tool(
    "vault_inject",
    "Inject content below an HTML comment anchor in an Obsidian vault note. "
    "Finds <!-- anchor_name --> and appends content on the next line. "
    "This is a PATCH operation: the anchor comment is preserved for future writes.",
    {"file_path": str, "anchor_name": str, "content": str},
)
async def vault_inject_tool(args: dict[str, Any]) -> dict[str, Any]:
    """Inject content at an anchor point in a vault note."""
    file_path = Path(args["file_path"])
    anchor = args["anchor_name"]
    content = args["content"]

    success = inject_at_anchor(file_path, anchor, content)

    if success:
        return {
            "content": [
                {"type": "text", "text": f"Injected content below <!-- {anchor} --> in {file_path}"}
            ]
        }
    else:
        return {
            "content": [
                {"type": "text", "text": f"Anchor <!-- {anchor} --> not found in {file_path}"}
            ],
            "is_error": True,
        }


def create_vault_mcp_server():
    """Create an MCP server with vault-related tools.

    Returns:
        An MCP server config that can be passed to ClaudeAgentOptions.mcp_servers.
    """
    return create_sdk_mcp_server(
        name="vault-tools",
        version="1.0.0",
        tools=[vault_inject_tool],
    )
