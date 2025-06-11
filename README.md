<br>
<div align="center"> 
<img alt="toolfront" src="img/logo/toolfront_logo_light.svg#gh-light-mode-only" width="80%">
<img alt="toolfront" src="img/logo/toolfront_logo_dark.svg#gh-dark-mode-only" width="80%">

</div>

<br>
<br>

> AI agents lack context about your databases, while teams keep rewriting the same queries because past work often gets lost. 
> ToolFront connects agents to your databases and feeds them your team's proven query patterns, so both agents and teammates can learn from each other and and ship faster.


## Features

- **⚡ One-step setup**: Connect coding agent like Cursor, GitHub Copilot, and Claude to all your databases with a single command.
- **🔒 Privacy-first**: Your data never leaves your machine, and is only shared between agents and databases through a secure MCP server.
- **🧠 Collaborative learning**: The more your team uses ToolFront, the better your AI agents understand your databases and query patterns.

## Quickstart

ToolFront runs on your computer through an [MCP](https://modelcontextprotocol.io/)  server, a secure protocol that lets apps provide context with LLMs models.

### Prerequisites
You'll need [uv](https://docs.astral.sh/uv/) or [Docker](https://www.docker.com/) to run the MCP server, and optionally an API key to activate collaborative learning.


### Running with UV:
[![Add to Cursor with UV](img/buttons/cursor_uv.png)](https://cursor.com/install-mcp?name=toolfront&config=eyJjb21tYW5kIjoidXZ4IHRvb2xmcm9udCBEQVRBQkFTRS1VUkwtMSBEQVRBQkFTRS1VUkwtMiAtLWFwaS1rZXkgWU9VUi1BUEktS0VZIn0%3D)
[![Add to GitHub Copilot with UV](img/buttons/copilot_uv.png)](https://insiders.vscode.dev/redirect/mcp/install?name=toolfront&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22toolfront%22%2C%22DATABASE-URL-1%22%2C%22DATABASE-URL-2%22%2C%22--API-KEY%22%2C%22YOUR_API_KEY%22%5D%7D)

<br>

Add this to your MCP config file to connect coding agents to ToolFront with UV:

```json
{
  # Rest of config file
  "toolfront": {
    "command": "uvx",
    "args": [
      "toolfront",
      "DATABASE-URL-1",
      "DATABASE-URL-2",
      # Add other database URLs here
      "--api-key", "YOUR-API-KEY"  // Optional
    ]
  }
}
```

Alternatively, run `uvx toolfront` to download and start the ToolFront MCP server:

```bash
uvx toolfront "DATABASE-URL-1" "DATABASE-URL-2" [...] --api-key "YOUR-API-KEY"
```

> [!TIP]
> **Version control**: Use `toolfront` to get the latest version automatically, or pin to a specific version e.g. `toolfront==0.1.0`. This applies to both direct commands and MCP configuration.

---

### Running with Docker
[![Add to Cursor with Docker](img/buttons/cursor_docker.png)](https://cursor.com/install-mcp?name=toolfront&config=eyJjb21tYW5kIjoiZG9ja2VyIHJ1biBhbnRpZG1nL3Rvb2xmcm9udCBEQVRBQkFTRS1VUkwtMSBEQVRBQkFTRS1VUkwtMiAtLWFwaS1rZXkgWU9VUi1BUEktS0VZIn0=)
[![Add to GitHub Copilot with Docker](img/buttons/copilot_docker.png)](https://insiders.vscode.dev/redirect/mcp/install?name=toolfront&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22antidmg%2Ftoolfront%22%2C%22DATABASE-URL-1%22%2C%22DATABASE-URL-2%22%2C%22--api-key%22%2C%22YOUR-API-KEY%22%5D%7D)

<br>

Add this to your MCP config file to connect coding agents to ToolFront with Docker:

```json
{
  # Rest of config file
  "toolfront": {
    "command": "docker",
    "args": [
      "run",
      "antidmg/toolfront",
      "DATABASE-URL-1",
      "DATABASE-URL-2",
      # Add other database URLs here
      "--api-key", "YOUR-API-KEY"  // Optional
    ]
  }
}
```

Alternatively, run the following command to download and pull and run the ToolFront MCP container:

```bash
docker run antidmg/toolfront "DATABASE-URL-1" "DATABASE-URL-2" [...] --api-key "YOUR-API-KEY"
```

## Collaborative In-context Learning


Data teams keep rewriting the same queries because past work often gets siloed, scattered, or lost. ToolFront teaches AI agents how your team works with your databases through [in-context learning](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html#in-context-learning-key-concept). When provided with an API key, your agents will:

- Reason about historical query patterns
- Remember relevant tables and schemas
- Reference your and your teammates' work

## Model Context Protocol (MCP)

ToolFront's' MCP server comes with seven database tools for AI agents.


### Databases

When configuring ToolFront, use the fully-specified connection URL for your databases:

| Database | URL Example |
|----------|-----|
| BigQuery | `bigquery://project/dataset` |
| DuckDB | `duckdb:///path/to/db.duckdb` |
| MySQL | `mysql://user:pass@host:port/db` |
| PostgreSQL | `postgresql://user:pass@host:port/db` |
| Snowflake | `snowflake://user:pass@account/db` |
| SQLite | `sqlite:///path/to/db.sqlite` |

More databses coming soon!

### Tools

ToolFront provides AI agents with the following database tools:

| Tool | Description |
|------|-------------|
| `test` | Tests whether a data source connection is working |
| `discover` | Discovers and lists all configured databases and file sources |
| `scan` | Searches for tables using regex, fuzzy matching, or TF-IDF similarity |
| `inspect` | Inspects table schemas, showing column names, data types, and constraints |
| `sample` | Retrieves sample rows from tables to understand data content and format |
| `query` | Executes read-only SQL queries against databases with error handling |
| `learn` | Retrieves relevant queries or tables for in-context learning|

## FAQ

<details>
<summary><strong>How is ToolFront different from other database MCPs?</strong></summary>
<br>

Two key advantages: collaborative learning, multi-database support. Most database MCPs just expose raw database operations, but ToolFront teaches your AI agents successful query patterns to help them agents understand your specific schemas. ToolFront works seamlessly across multiple database types with a unified interface, while other MCPs typically focus on single database types.

</details>

<details>
<summary><strong>How is collaborative learning different from agent memory?</strong></summary>

Agent memory stores conversation history for individual users. ToolFront creates a shared knowledge base that works across your entire team. When one team member successfully queries a database, that pattern helps other team members and AI agents with similar tasks. It's organization-wide learning instead of individual conversation memory.

</details>

<details>
<summary><strong>What data is collected during collaborative learning?</strong></summary>
<br>

Only query patterns and AI-generated descriptions are collected never your actual database content. Your personal information and sensitive data always stay on your machine. See the `query` and `learn` functions in [tools.py](src/toolfront/tools.py) for implementation details.

</details>

<details>
<summary><strong>How does ToolFront keep my data safe?</strong></summary>
<br>

- **Local execution**: All database connections and queries run on your machine
- **No secrets exposure**: Database credentials are never shared with AI agents
- **Read-only operations**: Only safe, read-only database queries are allowed
- **No data transmission**: Your database content never leaves your environment
- **Secure MCP protocol**: Direct communication between agents and databases with no third-party storage

</details>

<details>
<summary><strong>How do I troubleshoot connection issues?</strong></summary>
<br>

Run the `uvx toolfront` or `docker run` commands with your database URLs directly from the command line. ToolFront automatically tests all connections before starting and shows detailed error messages if any connection fails.

If you're still having trouble, double-check your database URLs using the examples in the [Databases section](#databases) above.

</details>

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to ToolFront.

## License

ToolFront is released under the [GPL License v3](LICENSE). This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the GPL v3 License. For the full license text, see the [LICENSE](LICENSE) file in the repository.
