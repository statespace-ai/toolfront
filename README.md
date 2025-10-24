<p align="center">
  <a href="https://github.com/statespace-tech/toolfront">
    <img src="https://raw.githubusercontent.com/statespace-tech/toolfront/main/docs/assets/images/logo.png" width="150" alt="ToolFront Logo">
  </a>
</p>

<div align="center">

# ToolFront

*Design AI Applications in Markdown*

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

ToolFront helps you design AI applications in Markdown. This way, you can develop agents the same way you develop regular software.

```bash
project/
├── README.md
├── src/
│   ├── api.md
│   ├── rag.md
│   └── text2sql.md
└── data/
    ├── catalog/
    └── spec.json

4 directories, 30 files
```

<details open>
<summary><b>Entry Point</b></summary>

Start by creating a README with instructions to guide your agent's behavior.

```markdown
# Sales Analytics

You are a business analyst.
Answer questions using the available resources.

Check out the following relevant files:
- `./src/api.md` for tools to fetch API data.
- `./src/rag.md` to retrieve product specs.
- `./src/text2sql.md` to query product data
```

</details>

<details>
<summary><b>Tools & APIs</b></summary>

List tools in your frontmatters so your agents can take actions.

```markdown
---
tools:
  - [curl, -X, GET, "https://api.com/{endpoint}"]

---

Call the API tool to retrieve order details.
- Always pass the `{endpoint}` argument
- See `/data/spec.json` for the full API spec
```

</details>

<details>
<summary><b>Document RAG</b></summary>

Teach your agent how to retrieve and interpret documents within your repository.

```markdown
# Document RAG

Search through files for product information.
Use built-in tools like `read`, `grep`, and `glob`

Instructions:
- Retrieve product specs under `/data/catalog/`
- Search for product IDs, SKUs, or feature details
- Cross-reference information across documents
```

</details>

<details>
<summary><b>Text-to-SQL</b></summary>

Use the built-in [database CLI](https://docs.toolfront.ai/pages/database_cli/) for text-to-SQL workflows, or build your own.

```markdown
---
tools:
  - [toolfront, database, $POSTGRES_URL]

---

Query the PostgreSQL database for product details.
- Discover available parameters with `--help`
- Available tables: `products` and `categories`
```

</details>

You can run AI applications directly with the [Python SDK](https://docs.toolfront.ai/pages/python_sdk/), or power them with your own agents via the [MCP Server](https://docs.toolfront.ai/pages/mcp_server/).

<details open>
<summary><b>Python SDK</b></summary>

```python
from toolfront import Application

app = Application(url="file:///path/to/project")

result = app.run("What's the status of order 66?", model="openai:gpt-5")
```

</details>

<details>
<summary><b>MCP Server</b></summary>

```json
{
  "mcpServers": {
    "toolfront": {
      "command": "uvx",
      "args": ["toolfront", "mcp", "file:///path/to/project"]
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

This gives you a URL to your project that works from anywhere. The project runs on your machine.

```python
app = Application(url="https://cloud.toolfront.ai/user/project", params={"API_KEY": ...})
```

ToolFront Cloud is in beta. To request access, join our [Discord](https://discord.gg/rRyM7zkZTf) or email `esteban[at]kruskal[dot]ai`.


## Community & Contributing

- **Discord**: Join our [community server](https://discord.gg/rRyM7zkZTf) for real-time help and discussions
- **X**: Follow us [@toolfront](https://x.com/toolfront) for updates and news
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/statespace-tech/toolfront/issues)

## License

This project is licensed under the terms of the MIT license.