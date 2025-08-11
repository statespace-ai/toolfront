# Model Context Protocol (MCP)

ToolFront runs as an MCP server to integrate with AI applications like Claude Desktop, Cursor, and GitHub Copilot. Works with all ToolFront data sources: 15+ databases, APIs, and documents.

---

## Configuration

Configure by passing your data source URL in the `args` array:

```json linenums="1"
{
  "mcpServers": {
    "toolfront": {
      "command": "uvx",
      "args": [
        "toolfront[{database_extra}]",  // (1)!
        "{connection_url}"
      ]
    }
  }
}
```

1. Replace with your database extras and connection URL

<div class="tabbed-set" markdown="1">

=== ":fontawesome-solid-code:{ .middle } &nbsp; Cursor"

    1. Open Cursor settings
    2. Navigate to MCP configuration section
    3. Add the configuration above to your MCP settings file
    4. Replace placeholders with your database extras and connection URL

=== ":simple-claude:{ .middle } &nbsp; Claude Desktop"

    1. Open your home directory
    2. Navigate to `claude_desktop_config.json`
    3. Add the configuration above to the file
    4. Replace placeholders with your database extras and connection URL
    5. Restart Claude Desktop

=== ":simple-githubcopilot:{ .middle } &nbsp; GitHub Copilot"

    1. Open GitHub Copilot settings
    2. Navigate to MCP configuration section
    3. Add the configuration above to your MCP settings
    4. Replace placeholders with your data source URL (no extras needed for APIs/documents)

</div>

!!! tip "Database Extras"
    When connecting to databases, include the appropriate extra in brackets (e.g., `toolfront[postgres]`, `toolfront[snowflake]`) to install the required database drivers.

---

## Command Line

Run ToolFront MCP server directly:

```bash
uvx toolfront[{database_extra}] "{connection_url}" --transport {stdio|sse}
```