<br>
<div align="center"> 
<img alt="toolfront" src="https://github.com/kruskal-labs/toolfront/blob/main/img/logo/toolfront_logo_light.png#gh-light-mode-only" width="80%">
<img alt="toolfront" src="https://github.com/kruskal-labs/toolfront/blob/main/img/logo/toolfront_logo_dark.png#gh-dark-mode-only" width="80%">

</div>

<br>
<br>

> AI agents lack context about your databases, while teams keep rewriting the same queries because past work often gets lost. 
> ToolFront connects agents to your databases and feeds them your team's proven query patterns, so both agents and teammates can learn from each other and ship faster.


## Features

- **⚡ One-step setup**: Connect coding agents like Cursor, GitHub Copilot, and Claude to all your databases with a single command.
- **🔒 Privacy-first**: Your data never leaves your machine, and is only shared between agents and databases through a secure MCP server.
- **🧠 Collaborative learning**: The more your team uses ToolFront, the better your AI agents understand your databases and query patterns.

## Quickstart

ToolFront runs on your computer through an [MCP](https://modelcontextprotocol.io/) server, a secure protocol that lets apps provide context to LLM models.

### Prerequisites
You'll need [uv](https://docs.astral.sh/uv/) or [Docker](https://www.docker.com/) to run the MCP server, and optionally an API key to activate collaborative learning.

---
### Running with UV:
[![Add to Cursor with UV](https://github.com/kruskal-labs/toolfront/blob/main/img/buttons/cursor_uv.png?raw=true)](https://cursor.com/install-mcp?name=toolfront&config=eyJjb21tYW5kIjoidXZ4IHRvb2xmcm9udCBEQVRBQkFTRS1VUkwtMSBEQVRBQkFTRS1VUkwtMiAtLWFwaS1rZXkgWU9VUi1BUEktS0VZIn0%3D)
[![Add to GitHub Copilot with UV](https://github.com/kruskal-labs/toolfront/blob/main/img/buttons/copilot_uv.png?raw=true)](https://insiders.vscode.dev/redirect/mcp/install?name=toolfront&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22toolfront%22%2C%22DATABASE-URL-1%22%2C%22DATABASE-URL-2%22%2C%22--API-KEY%22%2C%22YOUR_API_KEY%22%5D%7D)

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
[![Add to Cursor with Docker](https://github.com/kruskal-labs/toolfront/blob/main/img/buttons/cursor_docker.png?raw=true)](https://cursor.com/install-mcp?name=toolfront&config=eyJjb21tYW5kIjoiZG9ja2VyIHJ1biBhbnRpZG1nL3Rvb2xmcm9udCBEQVRBQkFTRS1VUkwtMSBEQVRBQkFTRS1VUkwtMiAtLWFwaS1rZXkgWU9VUi1BUEktS0VZIn0=)
[![Add to GitHub Copilot with Docker](https://github.com/kruskal-labs/toolfront/blob/main/img/buttons/copilot_docker.png?raw=true)](https://insiders.vscode.dev/redirect/mcp/install?name=toolfront&config=%7B%22command%22%3A%22docker%22%2C%22args%22%3A%5B%22run%22%2C%22antidmg%2Ftoolfront%22%2C%22DATABASE-URL-1%22%2C%22DATABASE-URL-2%22%2C%22--api-key%22%2C%22YOUR-API-KEY%22%5D%7D)

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

Alternatively, run the following command to download, pull, and run the ToolFront MCP container:

```bash
docker run antidmg/toolfront "DATABASE-URL-1" "DATABASE-URL-2" [...] --api-key "YOUR-API-KEY"
```

## Collaborative In-context Learning


Data teams keep rewriting the same queries because past work often gets siloed, scattered, or lost. ToolFront teaches AI agents how your team works with your databases through [in-context learning](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html#in-context-learning-key-concept). When provided with an API key, your agents will:

- Reason about historical query patterns
- Remember relevant tables and schemas
- Reference your and your teammates' work

## Model Context Protocol (MCP)

ToolFront's MCP server comes with seven database tools for AI agents.


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

More databases coming soon!

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
| `learn` | Retrieves relevant queries or tables for in-context learning |

## FAQ

<details>
<summary><strong>How is ToolFront different from other database MCPs?</strong></summary>
<br>

ToolFront has three key advantages: **multi-database support**, **privacy-first architecture**, and **collaborative learning**.

**Multi-database support**: While some general-purpose MCP servers happen to support multiple databases, most database MCPs only work with one database at a time, forcing you to manage separate MCP servers for each connection. ToolFront connects to all your databases in one place.

**Privacy-first architecture**: Other multi-database solutions route your data through the cloud, which racks up egress fees and creates serious privacy, security, and access control issues. ToolFront keeps everything local.

**Collaborative learning**: Database MCPs just expose raw database operations. ToolFront goes further by teaching your AI agents successful query patterns from your team's work, helping them learn your specific schemas and data relationships to improve over time.

</details>

<details>
<summary><strong>How is collaborative learning different from agent memory?</strong></summary>
<br>

Agent memory stores conversation histories for individuals, whereas ToolFront's collaborative learning remembers relational query patterns across your team and databases.

When one teammate queries a database, that knowledge becomes available to other team members using ToolFront. The system gets smarter over time by learning from your team's collective database interactions.

</details>

<details>
<summary><strong>What data is collected during collaborative learning?</strong></summary>
<br>

With an API key, ToolFront only logs the query syntax and their descriptions generated by your AI agents. It never collects your actual database content or personal information. For details, see the `query` and `learn` functions in [tools.py](src/toolfront/tools.py).

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
