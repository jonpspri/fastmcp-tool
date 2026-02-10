"""Command line tool for interacting with an MCP server."""

import json
from logging import getLogger

import asyncclick as click
from fastmcp.client import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport

from fastmcp_tool import __version__

logger = getLogger("fastmcp_tool")


@click.group()
@click.option(
    "--server",
    "server_str",
    default=None,
    help="MCP Server - either a URL or a stream to run stdio",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging including stdio server stderr output",
)
@click.option(
    "--bearer-token",
    default=None,
    help="Bearer token for HTTP server authentication",
)
@click.pass_context
def fastmcp_tool(
    ctx: click.Context,
    server_str: str | None,
    debug: bool,  # noqa: ARG001, FBT001  # debug needed for FastMCP Commit 05a73e1
    bearer_token: str | None,
) -> None:
    """Command line tool for interacting with an MCP server."""
    if not isinstance(server_str, str):
        logger.error("No server specified. Use --server to specify an MCP server.")
        return
    transport: StdioTransport | StreamableHttpTransport
    if server_str.startswith(("http://", "https://")):
        transport = StreamableHttpTransport(url=server_str, auth=bearer_token)
    else:
        if bearer_token is not None:
            logger.warning("--bearer-token is only supported for HTTP servers; ignoring.")
        transport = StdioTransport(
            command="bash",
            args=["-c", server_str],
            # Waiting for FastMCP Commit 05a73e1 to be released
            # log_file = sys.stderr if debug else os.devnull
        )
    ctx.obj = ctx.with_async_resource(Client(transport=transport))


@fastmcp_tool.command()
@click.pass_context
async def tools(ctx: click.Context) -> None:
    """List available tools."""
    async with await ctx.obj as client:
        tool_list = await client.list_tools()
        click.echo(json.dumps([tool.model_dump(mode="json") for tool in tool_list]))


@fastmcp_tool.command()
@click.argument("tool_name")
@click.option("--params", default="{}", help="JSON string of parameters to pass to the tool")
@click.pass_context
async def call(ctx: click.Context, tool_name: str, params: str) -> None:
    """Call a tool with parameters."""
    async with await ctx.obj as client:
        params_dict = json.loads(params)
        result = await client.call_tool(tool_name, params_dict)
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
async def resources(ctx: click.Context) -> None:
    """List available resources."""
    async with await ctx.obj as client:
        resource_list = await client.list_resources()
        click.echo(json.dumps([resource.model_dump(mode="json") for resource in resource_list]))


@fastmcp_tool.command()
@click.pass_context
async def prompts(ctx: click.Context) -> None:
    """List available prompts."""
    async with await ctx.obj as client:
        prompt_list = await client.list_prompts()
        click.echo(json.dumps([prompt.model_dump(mode="json") for prompt in prompt_list]))


@fastmcp_tool.command()
def version() -> None:
    """Print the version."""
    click.echo(f"fastmcp-tool {__version__}")


if __name__ == "__main__":
    fastmcp_tool()
