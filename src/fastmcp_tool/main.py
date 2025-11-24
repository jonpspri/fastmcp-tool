"""Command line tool for interacting with an MCP server."""
import json
import os
import sys
from logging import getLogger

import asyncclick as click
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport

logger = getLogger("fastmcp_tool")

@click.group()
@click.option("--server", "server_str", default=None, help="MCP Server - eiter a URL or a stream to run stdio")
@click.option("--debug", is_flag=True, help="Enable debug logging incuding stdio server stderr output")
@click.pass_context

def fastmcp_tool(ctx, server_str, debug):  # noqa: ARG001  # debug needed for FastMCP Commit 05a73e1
    """Command line tool for interacting with an MCP server."""
    if not isinstance(server_str, str):
        logger.error("No server specified. Use --server to specify an MCP server.")
        return
    if server_str.startswith(("http://", "https://")):
        transport = StreamableHttpTransport(url=server_str)
    else:
        transport = StdioTransport(
                command="bash",
                args=["-c", server_str],
                # Waiting for FastMCP Commit 05a73e1 to be released
                # log_file = sys.stderr if debug else os.devnull
                )
    ctx.obj = ctx.with_async_resource(Client(transport=transport))

@fastmcp_tool.command()
@click.pass_context
async def tools(ctx):
    """List available tools."""
    async with await ctx.obj as client:
        tools = await client.list_tools()
        click.echo( json.dumps([tool.model_dump(mode="json") for tool in tools]))

@fastmcp_tool.command()
@click.argument("tool_name")
@click.option("--params", default="{}", help="JSON string of parameters to pass to the tool")
@click.pass_context
async def call(ctx, tool_name, params):
    """Call a tool with parameters."""
    async with await ctx.obj as client:
        params = json.loads(params)
        result = await client.call_tool(tool_name, params)
    if result.structured_content:
        click.echo(json.dumps(result.structured_content))
    else:
        for item in result.content:
            if item.type == "text":
                click.echo(item.text)
            else:
                click.echo(f"[{item.type} content]")

@fastmcp_tool.command()
@click.pass_context
async def resources(ctx):
    """List available resources."""
    async with await ctx.obj as client:
        resources = await client.list_resources()
        click.echo( json.dumps([resource.model_dump(mode="json") for resource in resources]))

@fastmcp_tool.command()
@click.pass_context
async def prompts(ctx):
    """List available prompts."""
    async with await ctx.obj as client:
        prompts = await client.list_prompts()
        click.echo( json.dumps([prompt.model_dump(mode="json") for prompt in prompts]))

if __name__ == "__main__":
    fastmcp_tool()
