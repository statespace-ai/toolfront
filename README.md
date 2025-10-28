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

## Quickstart

**ToolFront is a declarative framework for building AI agents in Markdown.**

Write tools and instructions in `.md` files. Run the project and get a live AI application.

### Create it

Start with **one file**: `README.md`

```markdown
---
tools:
  - [curl, -X, GET, "https://httpbin.org/status/200"]
---

# Status Checker
- Use `curl` to check if the service is up
```

### Run it

Run the application with:

```bash
toolfront run .
```

### Ask it

Ask your agents about the application:

<details open>
<summary><b>Python SDK</b></summary>

```python
from toolfront import Application

app = Application(url="http://127.0.0.1:8000")

result = app.ask("Is the service up?", model="openai:gpt-5")

print(result)
# Answer: yes
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

---

## Upgraded Example

Your full project can grow like this:

```bash
project/
├── README.md
├── src/
│   ├── api.md
│   ├── rag.md
│   ├── text2sql.md
│   └── toolkit.md
├── data/
└── tools/
```

### Add Navigation

Update `README.md` with tools to explore the project

```markdown
---
tools:
  - [curl, -X, GET, "https://httpbin.org/status/200"]
  - [ls]
  - [cat]
---

# Status Checker
- Use `curl` to check if the service is up
- Use `ls` and `cat` to browse other files
```

### Add Document RAG

Give your agent tools to search documents

```markdown
---
tools:
  - [grep]
---

# Search Docs
- Use `grep` to search files in `/data/`
```

### Add Text-to-SQL

Connect your databases for SQL workflows

```markdown
---
tools:
  - [psql, -U, $USER, -d, $DATABASE, -c, {query}]
---

# Database Access
- Call the `psql` tool to query the PostgreSQL database
```

### Add Custom Tools

Build custom tools in any programming language

```markdown
---
tools:
  - [python, tools/status.py, --delayed]
---

# Custom Tools
- Run `status.py` to check delayed orders
```

---

## Installation

Install `toolfront` with your favorite PyPI package manager.

```bash
pip install toolfront
```

---

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