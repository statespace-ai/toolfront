# Tools

Tools are commands that your agent can call to take actions and interact with other applications.

```markdown
---
tools:
  - [curl, "https://api.com/products/{product_id}"]
  - [gh, issue, create]
  - [stripe, products, list, --api-key, $STRIPE_KEY]

---

Call the tools to ...
```


!!! example "Custom Tools"
    ToolFront comes with a **[database CLI](./database_cli.md)** for text-to-SQL workflows. You can build similar CLIs for your own use cases.


---

## Parameters

Tools can include parameter `{placeholders}` in curly braces. Agents automatically replace placeholders with actual values when calling tools. For example, `{product_id}` → `prod-123`:

```bash
Calling "curl https://api.com/products/prod-123"
```

---

## Arguments

Since tools are CLI commands, they accept additional arguments. Agents can append arguments like flags and options. For example, for the `gh issue create` tool:


```bash
Calling "gh issue create --title 'Bug report' --repo owner/repo"
```

!!! tip "Learning Tools"
    Agents learn how to use tools by passing the `--help` flag.

---

## Environment Variables

Tools can include environment variables (prefixed with `$`) to keep credentials and configurations private. For example, for the `stripe products list --api-key $STRIPE_KEY` tool:

```bash
Calling "stripe products list --api-key sk_fake_placeholder_key"
```

Don't forget to pass these variables to your application before running it!

=== ":simple-python:{ .middle } &nbsp; Python SDK"

    ```python hl_lines="7"
    from toolfront import Application


    app = Application(
        url="file:///path/to/project",
        env={
            "STRIPE_KEY": "sk_fake_placeholder_key"
        }
    )

    result = app.run("List all products", model="openai:gpt-5")
    ```

=== ":simple-modelcontextprotocol:{ .middle } &nbsp; MCP Server"

    ```json hl_lines="7"
    {
      "mcpServers": {
        "toolfront": {
          "command": "uvx",
          "args": ["toolfront", "mcp", "file:///path/to/project"],
          "env": {
            "STRIPE_KEY": "sk_fake_placeholder_key"
          }
        }
      }
    }
    ```


