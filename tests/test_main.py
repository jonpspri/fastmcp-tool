"""Tests for the fastmcp-tool CLI."""

import logging
from unittest.mock import patch

import pytest
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


async def test_help_bearer_token() -> None:
    """Test that --bearer-token option appears in help."""
    runner = CliRunner()
    result = await runner.invoke(fastmcp_tool, ["--help"])
    assert result.exit_code == 0
    assert "--bearer-token" in result.output


async def test_bearer_token_passed_to_http_transport() -> None:
    """Test that --bearer-token is forwarded as auth to StreamableHttpTransport."""
    runner = CliRunner()
    with (
        patch("fastmcp_tool.main.StreamableHttpTransport") as mock_transport,
        patch("fastmcp_tool.main.Client"),
    ):
        await runner.invoke(
            fastmcp_tool,
            ["--server", "https://example.com/mcp", "--bearer-token", "secret", "tools"],
        )
        mock_transport.assert_called_once_with(url="https://example.com/mcp", auth="secret")


async def test_bearer_token_warning_on_stdio(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that --bearer-token with a stdio server logs a warning."""
    runner = CliRunner()
    with (
        patch("fastmcp_tool.main.StdioTransport"),
        patch("fastmcp_tool.main.Client"),
        caplog.at_level(logging.WARNING, logger="fastmcp_tool"),
    ):
        await runner.invoke(
            fastmcp_tool,
            ["--server", "some-command", "--bearer-token", "secret", "tools"],
        )
    assert any("only supported for HTTP servers" in r.message for r in caplog.records)


async def test_no_server_specified() -> None:
    """Test behavior when no server is specified."""
    runner = CliRunner()
    result = await runner.invoke(fastmcp_tool, ["tools"])
    # Exits with error when no server is provided
    assert result.exit_code == 1
