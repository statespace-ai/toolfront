<p align="center">
  <a href="https://github.com/statespace-tech/toolfront">
    <img src="https://raw.githubusercontent.com/statespace-tech/toolfront/main/docs/assets/images/logo.png" width="150" alt="ToolFront Logo">
  </a>
</p>

<div align="center">

# ToolFront

*Build AI Applications in Markdown*

[![Test Suite](https://github.com/statespace-tech/toolfront/actions/workflows/test.yml/badge.svg)](https://github.com/statespace-tech/toolfront/actions/workflows/test.yml)
[![PyPI package](https://img.shields.io/pypi/v/toolfront?color=%2334D058&label=pypi%20package)](https://pypi.org/project/toolfront/)
[![Discord](https://img.shields.io/discord/1323415085011701870?label=Discord&logo=discord&logoColor=white&style=flat-square)](https://discord.gg/rRyM7zkZTf)
[![X](https://img.shields.io/badge/Statespace-black?style=flat-square&logo=x&logoColor=white)](https://x.com/statespace_tech)

</div>

---

**Documentation: [docs.toolfront.ai](http://docs.toolfront.ai/)**

**Source code: [https://github.com/statespace-tech/toolfront](https://github.com/statespace-tech/toolfront)**

---

## Installation

Install `toolfront` with your favorite PyPI package manager.

```bash
pip install toolfront
```

## Quickstart

ToolFront helps you build AI applications in Markdown. This way, you can develop agents the same way you develop regular software.

```bash
project/
├── data/
├── README.md
├── spec.json
├── src/
│   ├── api.md
│   ├── rag.md
│   ├── text2sql.md
│   └── toolkit.md
└── tools/

4 directories, 30 files
```

<details open>
<summary><b>Entry Point</b></summary>

Start by creating a README with general instructions and tools for your agent.

```markdown
---
tools:
  - [ls]
  - [cat]

---

# Agent Instructions
- Use `ls` and `cat` to browse the tool site
- Check out `./src` for specialized workflows
```

</details>

<details>
<summary><b>API Integration</b></summary>

Connect agents to external APIs and web services using HTTP tools like `curl`.

```markdown
---
tools:
  - [curl, -X, GET, "https://api.com/{endpoint}"]

---

# Web API
- Call external APIs to fetch real-time data.
- Pass `{endpoint}` to make GET requests
- Check `/data/spec.json` for available endpoints
```

</details>

<details>
<summary><b>Document RAG</b></summary>

Teach your agent how to search and interpret documents with tools like `grep`.

```markdown

---
tools
  - [grep]

---

# Document RAG
- Use `grep` to search through `/data/catalog/`
- Cross-reference information across documents
- Look for product IDs, SKUs, or feature details
```

</details>

<details>
<summary><b>Text-to-SQL</b></summary>

Connect agents to databases using CLI tools like `psql` for text-to-SQL workflows.

```markdown
---
tools:
  - [psql, -U, $USER, -d, $DATABASE, -c, {query}]

---

# Text-to-SQL
- Query the PostgreSQL DB for product details
- Pass a `{query}` to the `psql` tool
- Available tables: `products` and `categories`
```

</details>

<details>
<summary><b>Custom Tools</b></summary>

Build custom tools using scripts in any programming language.

```markdown
---
tools:
  - [python, tools/status.py, {id}]
  - [cargo, script, tools/check_delays.rs]

---

# Toolkit
- Run `status.py` with `{id}` to check statuses
- Use `check_delays.rs` to scan for delayed orders
```

</details>

You can run AI applications directly with the [Python SDK](https://docs.toolfront.ai/pages/python_sdk/), or power them with your own agents via the [MCP Server](https://docs.toolfront.ai/pages/mcp_server/).

<details open>
<summary><b>Python SDK</b></summary>

```python
from toolfront import Application

app = Application(url="http://127.0.0.1:8000")

result = app.ask("What's the status of order 66?", model="openai:gpt-5")
```

</details>

<details>
<summary><b>MCP Server</b></summary>

```json
{
  "mcpServers": {
    "toolfront": {
      "command": "uvx",
      "args": ["toolfront", "mcp", "http://127.0.0.1:8000"]
    }
  }
}
```

</details>

## Deploy with ToolFront Cloud

Deploy your AI applications with [ToolFront Cloud](https://docs.toolfront.ai/pages/toolfront_cloud/).

```bash
toolfront deploy ./path/to/project
```

This gives you a secure application URL you can access from anywhere.

```python
app = Application(url="https://cloud.toolfront.ai/user/project", params={"API_KEY": ...})
```

ToolFront Cloud is in beta. To request access, join our [Discord](https://discord.gg/rRyM7zkZTf) or email `esteban[at]statespace[dot]com`.


## Community & Contributing

- **Discord**: Join our [community server](https://discord.gg/rRyM7zkZTf) for real-time help and discussions
- **X**: Follow us [@toolfront](https://x.com/toolfront) for updates and news
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/statespace-tech/toolfront/issues)

## License

This project is licensed under the terms of the MIT license.