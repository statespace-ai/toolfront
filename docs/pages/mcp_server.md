# Browser MCP

ToolFront's MCP server exposes the core tools to browse environments. Use it when you want full control over your agent.

---


## Basic Usage

Start the MCP server with `toolfront mcp URL [OPTIONS]` and connect it to your AI client:

```json
{
  "mcpServers": {
    "toolfront": {
      "command": "uvx",
      "args": ["toolfront", "mcp", "file:///path/environment"]
    }
  }
}
```

Available options:

- `--transport` - Communication protocol: `stdio` (default), `streamable-http`, or `sse`
- `--host` - Server host address (default: `127.0.0.1`)
- `--port` - Server port number (default: `8000`)
- `--params` - Authentication for remote storage (e.g., `--params AWS_ACCESS_KEY_ID=xxx`)

---

## Environment Variables

Environment tools may reference environment variables for authentication or configuration:

```
---
tools:
  - [curl, -X, GET, "https://api.com/data", -H, "Authorization: Bearer $TOKEN"]
  - [curl, -X, POST, "https://api.com/submit", -H, "X-API-Key: $API_KEY"]
---

# My Markdown page
...
```

Pass these variables when starting the MCP server:

```bash
toolfront mcp file:///path/environment --env "TOKEN=token" --env "API_KEY=key"
```

---

## API Reference

::: toolfront.cli.mcp.serve
    options:
      show_root_heading: true
      show_source: true