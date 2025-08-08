# MCP Server

ToolFront includes a built-in Model Context Protocol (MCP) server for seamless integration with MCP-compatible AI clients like Claude Desktop.

## Setup Instructions

1. Create an MCP configuration file
2. Add ToolFront as a server with your data source URL
3. Connect your AI client

## Configuration

Add to your MCP configuration file:

```json
{
  "mcpServers": {
    "toolfront": {
      "command": "uvx",
      "args": ["toolfront[postgres]", "postgresql://user:pass@host:port/db"]
    }
  }
}
```

## Compatible Clients

- **Claude Desktop**: Direct integration via MCP configuration
- **Cursor**: MCP server support
- **Other MCP-enabled applications**: Any application supporting the Model Context Protocol

## Usage

Once configured, the MCP server provides:

- **Context retrieval**: Get schema and metadata about your data sources
- **Query execution**: Execute queries through the MCP interface
- **Tool integration**: Access all ToolFront tools through MCP-compatible clients