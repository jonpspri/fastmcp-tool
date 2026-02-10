"""Tests for the fastmcp-tool CLI."""

import json
import logging
from pathlib import Path
from unittest.mock import patch

import pytest
from asyncclick.testing import CliRunner

from fastmcp_tool import __version__
from fastmcp_tool.main import fastmcp_tool

ECHO_SERVER = f"uv run {Path(__file__).parent / 'echo_server.py'}"


def test_version() -> None:
    """Test that version is defined."""
    assert __version__ == "0.1.2"


async def test_version_command() -> None:
    """Test that the version command prints the version without requiring --server."""
    runner = CliRunner()
    result = await runner.invoke(fastmcp_tool, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output
    assert "No server specified" not in result.output


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


async def test_call_with_params() -> None:
    """Test calling a tool with --params."""
    runner = CliRunner()
    result = await runner.invoke(
        fastmcp_tool,
        ["--server", ECHO_SERVER, "call", "echo", "--params", '{"message": "hello"}'],
    )
    assert result.exit_code == 0
    assert "hello" in result.output


async def test_call_with_params_file(tmp_path: Path) -> None:
    """Test that --params-file reads parameters from a JSON file."""
    params_file = tmp_path / "params.json"
    params_file.write_text(json.dumps({"message": "from file"}))

    runner = CliRunner()
    result = await runner.invoke(
        fastmcp_tool,
        ["--server", ECHO_SERVER, "call", "echo",
         "--params-file", str(params_file)],
    )
    assert result.exit_code == 0
    assert "from file" in result.output


async def test_call_params_and_params_file_mutually_exclusive(tmp_path: Path) -> None:
    """Test that --params and --params-file cannot be used together."""
    params_file = tmp_path / "params.json"
    params_file.write_text(json.dumps({"message": "x"}))

    runner = CliRunner()
    result = await runner.invoke(
        fastmcp_tool,
        ["--server", ECHO_SERVER, "call", "echo",
         "--params", '{"message": "y"}', "--params-file", str(params_file)],
    )
    assert result.exit_code != 0
    assert "mutually exclusive" in result.output


async def test_call_params_file_not_found() -> None:
    """Test that --params-file with a nonexistent file fails."""
    runner = CliRunner()
    result = await runner.invoke(
        fastmcp_tool,
        ["--server", ECHO_SERVER, "call", "echo",
         "--params-file", "/nonexistent/params.json"],
    )
    assert result.exit_code != 0
