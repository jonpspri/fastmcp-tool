"""Tests for the fastmcp-tool CLI."""

from asyncclick.testing import CliRunner

from fastmcp_tool import __version__
from fastmcp_tool.main import fastmcp_tool


def test_version() -> None:
    """Test that version is defined."""
    assert __version__ == "0.1.0"


async def test_help() -> None:
    """Test that --help works."""
    runner = CliRunner()
    result = await runner.invoke(fastmcp_tool, ["--help"])
    assert result.exit_code == 0
    assert "Command line tool for interacting with an MCP server" in result.output


async def test_no_server_specified() -> None:
    """Test behavior when no server is specified."""
    runner = CliRunner()
    result = await runner.invoke(fastmcp_tool, ["tools"])
    # Exits with error when no server is provided
    assert result.exit_code == 1
