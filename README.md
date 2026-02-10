# fastmcp-tool

A command line tool for interacting with MCP (Model Context Protocol) servers.

## Installation

```bash
pip install fastmcp-tool
```

Or with uv:

```bash
uv pip install fastmcp-tool
```

## Usage

### Connecting to a Server

Use the `--server` option to specify an MCP server. This can be either:

- An HTTP/HTTPS URL for streamable HTTP transport
- A shell command for stdio transport

```bash
# HTTP server
fastmcp-tool --server https://mcp.example.com/sse <command>

# Stdio server (runs command via bash)
fastmcp-tool --server "python my_mcp_server.py" <command>
```

### Commands

#### List Tools

List all available tools on the MCP server:

```bash
fastmcp-tool --server https://mcp.example.com/sse tools
```

#### Call a Tool

Call a specific tool with optional JSON parameters:

```bash
fastmcp-tool --server https://mcp.example.com/sse call my_tool --params '{"key": "value"}'
```

#### List Resources

List all available resources:

```bash
fastmcp-tool --server https://mcp.example.com/sse resources
```

#### List Prompts

List all available prompts:

```bash
fastmcp-tool --server https://mcp.example.com/sse prompts
```

### Options

| Option | Description |
|--------|-------------|
| `--server` | MCP server URL or stdio command |
| `--debug` | Enable debug logging |
| `--help` | Show help message |

## Examples

```bash
# List tools from a local stdio server
fastmcp-tool --server "uv run my_server.py" tools

# Call a tool with parameters
fastmcp-tool --server https://api.example.com/mcp call search --params '{"query": "hello"}'

# List resources with debug output
fastmcp-tool --server "python server.py" --debug resources
```

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.
