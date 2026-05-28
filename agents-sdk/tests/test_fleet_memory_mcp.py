"""Tests for the fleet-memory MCP-server bridge used by daily_driver."""

from __future__ import annotations

from pathlib import Path

import pytest


def test_factory_returns_a_server_object(tmp_path: Path):
    """Factory returns whatever create_sdk_mcp_server returns — we don't
    assert on its internal shape, only that the call succeeds and that
    side effects (mount bootstrap) happen."""
    from lib.custom_tools import create_fleet_memory_mcp_server
    mount = tmp_path / "fleet-memory"
    server = create_fleet_memory_mcp_server(
        agent_id="daily_driver", mount_root=mount,
    )
    assert server is not None
    # Side effect: ensure_mount fired
    assert (mount / "daily_driver").is_dir()
    assert (mount / "shared").is_dir()
    assert (mount / "MEMORY_INDEX.md").exists()


@pytest.mark.asyncio
async def test_memory_create_tool_writes_to_namespace(tmp_path: Path):
    """The memory_create handler routes through FleetMemoryTool._create_path
    and produces the standard MCP success envelope."""
    from lib.custom_tools import _build_memory_handlers
    mount = tmp_path / "fleet-memory"
    from lib.fleet_memory import ensure_mount
    ensure_mount(mount, agent_ids=["daily_driver"])
    handlers = _build_memory_handlers(agent_id="daily_driver", mount_root=mount)
    result = await handlers["memory_create"](
        {"path": "/memories/daily_driver/note.md", "file_text": "hello"}
    )
    assert "is_error" not in result
    assert result["content"][0]["type"] == "text"
    assert (mount / "daily_driver/note.md").read_text() == "hello"


@pytest.mark.asyncio
async def test_memory_view_returns_text_envelope(tmp_path: Path):
    from lib.custom_tools import _build_memory_handlers
    mount = tmp_path / "fleet-memory"
    from lib.fleet_memory import ensure_mount
    ensure_mount(mount, agent_ids=["daily_driver"])
    (mount / "daily_driver" / "x.md").write_text("body")
    handlers = _build_memory_handlers(agent_id="daily_driver", mount_root=mount)
    result = await handlers["memory_view"]({"path": "/memories/daily_driver/x.md"})
    assert "is_error" not in result
    assert result["content"][0]["text"] == "body"


@pytest.mark.asyncio
async def test_path_escape_returns_error_envelope_not_raise(tmp_path: Path):
    """When the underlying _resolve_path raises PathEscapeError, the MCP
    handler must catch it and return is_error=True — never let the SDK
    process crash."""
    from lib.custom_tools import _build_memory_handlers
    mount = tmp_path / "fleet-memory"
    from lib.fleet_memory import ensure_mount
    ensure_mount(mount, agent_ids=["daily_driver"])
    handlers = _build_memory_handlers(agent_id="daily_driver", mount_root=mount)
    result = await handlers["memory_view"]({"path": "/memories/../../etc/passwd"})
    assert result.get("is_error") is True
    assert "PathEscapeError" in result["content"][0]["text"]
