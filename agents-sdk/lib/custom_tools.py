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


from lib.fleet_memory import FleetMemoryTool, ensure_mount


def _ok(text: str) -> dict[str, Any]:
    return {"content": [{"type": "text", "text": text}]}


def _err(exc: Exception) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}],
        "is_error": True,
    }


def _build_memory_handlers(
    *,
    agent_id: str,
    mount_root: Path,
) -> dict[str, Any]:
    """Return a dict of six async handlers, one per memory command.

    Extracted from `create_fleet_memory_mcp_server` so unit tests can call
    the handlers directly without spinning up an MCP server. Each handler
    catches every exception and returns the MCP error envelope — the SDK
    process must never crash on bad model input.
    """
    ensure_mount(mount_root, agent_ids=[agent_id])
    fmt = FleetMemoryTool(mount_root=mount_root, agent_id=agent_id)

    async def memory_view(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._view_path(args["path"]))
        except Exception as exc:
            return _err(exc)

    async def memory_create(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._create_path(args["path"], args["file_text"]))
        except Exception as exc:
            return _err(exc)

    async def memory_str_replace(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._str_replace_path(
                args["path"], args["old_str"], args["new_str"],
            ))
        except Exception as exc:
            return _err(exc)

    async def memory_insert(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._insert_path(
                args["path"], args["insert_line"], args["insert_text"],
            ))
        except Exception as exc:
            return _err(exc)

    async def memory_delete(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._delete_path(args["path"]))
        except Exception as exc:
            return _err(exc)

    async def memory_rename(args: dict[str, Any]) -> dict[str, Any]:
        try:
            return _ok(fmt._rename_path(args["old_path"], args["new_path"]))
        except Exception as exc:
            return _err(exc)

    return {
        "memory_view": memory_view,
        "memory_create": memory_create,
        "memory_str_replace": memory_str_replace,
        "memory_insert": memory_insert,
        "memory_delete": memory_delete,
        "memory_rename": memory_rename,
    }


def create_fleet_memory_mcp_server(*, agent_id: str, mount_root: Path):
    """Expose six memory-protocol tools as an in-process MCP server.

    Mirrors create_vault_mcp_server's shape. Each tool maps 1:1 onto an
    Anthropic memory_20250818 command, routed into the namespace-scoped
    FleetMemoryTool built in lib/fleet_memory.py.

    Tool names visible to the CLI (`allowed_tools` matchers):
        mcp__fleet-memory__memory_view
        mcp__fleet-memory__memory_create
        mcp__fleet-memory__memory_str_replace
        mcp__fleet-memory__memory_insert
        mcp__fleet-memory__memory_delete
        mcp__fleet-memory__memory_rename
    """
    handlers = _build_memory_handlers(agent_id=agent_id, mount_root=mount_root)

    view_tool = tool(
        "memory_view",
        "View a memory file or list a directory under /memories/. "
        "Paths must stay inside the fleet-memory mount; escapes raise an error.",
        {"path": str},
    )(handlers["memory_view"])

    create_tool = tool(
        "memory_create",
        "Create or overwrite a memory file. Writes are restricted to "
        f"/memories/{agent_id}/** and /memories/shared/**.",
        {"path": str, "file_text": str},
    )(handlers["memory_create"])

    str_replace_tool = tool(
        "memory_str_replace",
        "Replace a unique substring in a memory file. Fails if `old_str` "
        "is missing or appears more than once.",
        {"path": str, "old_str": str, "new_str": str},
    )(handlers["memory_str_replace"])

    insert_tool = tool(
        "memory_insert",
        "Insert text at a 0-indexed line number in a memory file.",
        {"path": str, "insert_line": int, "insert_text": str},
    )(handlers["memory_insert"])

    delete_tool = tool(
        "memory_delete",
        "Delete a memory file. Only files inside the agent's namespace "
        "or /memories/shared/ can be deleted.",
        {"path": str},
    )(handlers["memory_delete"])

    rename_tool = tool(
        "memory_rename",
        "Rename or move a memory file. Both source and destination must "
        "be inside the agent's namespace or /memories/shared/.",
        {"old_path": str, "new_path": str},
    )(handlers["memory_rename"])

    return create_sdk_mcp_server(
        name="fleet-memory",
        version="1.0.0",
        tools=[
            view_tool, create_tool, str_replace_tool,
            insert_tool, delete_tool, rename_tool,
        ],
    )
