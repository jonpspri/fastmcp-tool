"""Minimal MCP server for integration tests."""

from fastmcp import FastMCP

mcp = FastMCP("test-echo")


@mcp.tool()
def echo(message: str) -> str:
    """Echo back the message."""
    return message


if __name__ == "__main__":
    mcp.run()
