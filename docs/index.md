---
title: "Quickstart"
---

<p align="center">
  <a href="https://github.com/statespace-tech/toolfront">
    <img src="assets/images/logo.png" alt="ToolFront" style="width:20%;">
  </a>
</p>
<div align="center">
    <h1 style="font-weight: 800;"><b>ToolFront</b></h1>
</div>
<p align="center">
    <em>Design AI Applications in Markdown</em>
</em>
</p>
<p align="center">
<a href="https://github.com/statespace-tech/toolfront/actions/workflows/test.yml" target="_blank">
    <img src="https://github.com/statespace-tech/toolfront/actions/workflows/test.yml/badge.svg" alt="Test Suite">
</a>
<a href="https://pypi.org/project/toolfront/" target="_blank">
    <img src="https://img.shields.io/pypi/v/toolfront?color=%2334D058&label=pypi%20package" alt="PyPI package">
</a>
<a href="https://discord.gg/rRyM7zkZTf" target="_blank">
    <img src="https://img.shields.io/discord/1323415085011701870?label=Discord&logo=discord&logoColor=white&style=flat-square" alt="Discord">
</a>
<a href="https://x.com/statespace_tech" target="_blank">
    <img src="https://img.shields.io/badge/Statespace-black?style=flat-square&logo=x&logoColor=white" alt="X">
</a>
</p>

---

**Source code: [https://github.com/statespace-tech/toolfront](https://github.com/statespace-tech/toolfront)**

---

ToolFront helps you design AI applications in Markdown. This way, you can develop agents the same way you develop regular software.

=== ":material-home: Entry Point"

    Start by creating a README with instructions to guide your agent's behavior.

    <div class="grid cards" markdown>

    ```bash hl_lines="5"
    project/
    ├── data/
    │   ├── catalog/
    │   └── spec.json
    ├── README.md
    └── src/
        ├── api.md
        ├── rag.md
        └── text2sql.md

    4 directories, 30 files
    ```

    ```markdown title="README.md"
    # Sales Analytics

    You are a business analyst.
    Answer questions using the available resources.

    Check out the following relevant files:
    - `./src/api.md` for tools to fetch API data.
    - `./src/rag.md` to retrieve product specs.
    - `./src/text2sql.md` to query product data
    ```

    </div>


=== ":material-tools: Tools & APIs"

    List tools in your frontmatters so your agents can take actions.

    <div class="grid cards" markdown>

    ```bash hl_lines="7"
    project/
    ├── data/
    │   ├── catalog/
    │   └── spec.json
    ├── README.md
    └── src/
        ├── api.md
        ├── rag.md
        └── text2sql.md

    4 directories, 30 files
    ```


    ```markdown title="api.md"
    ---
    tools:
      - [curl, -X, GET, "https://api.com/{endpoint}"]
    
    ---

    Call the API tool to retrieve order details.
    - Always pass the `{endpoint}` argument
    - See `/data/spec.json` for the full API spec
    ```

    </div>


=== ":material-file-document: Document RAG"

    Teach your agent how to retrieve and interpret documents within your repository.

    <div class="grid cards" markdown>

    ```bash hl_lines="8"
    project/
    ├── data/
    │   ├── catalog/
    │   └── spec.json
    ├── README.md
    └── src/
        ├── api.md
        ├── rag.md
        └── text2sql.md

    4 directories, 30 files
    ```


    ```markdown title="rag.md"
    # Document RAG

    Search through files for product information.
    Use built-in tools like `read`, `grep`, and `glob`

    Instructions:
    - Retrieve product specs under `/data/catalog/`
    - Search for product IDs, SKUs, or feature details
    - Cross-reference information across documents
    ```

    </div>


=== ":material-database: Text-to-SQL"

    Use the built-in **[database CLI](./pages/database_cli.md)** for text-to-SQL workflows, or build your own.

    <div class="grid cards" markdown>

    ```bash hl_lines="9"
    project/
    ├── data/
    │   ├── catalog/
    │   └── spec.json
    ├── README.md
    └── src/
        ├── api.md
        ├── rag.md
        └── text2sql.md

    4 directories, 30 files
    ```

    ```markdown title="text2sql.md"
    ---
    tools:
      - [toolfront, database, $POSTGRES_URL]
    
    ---

    Query the PostgreSQL database for product details.
    - Discover available parameters with `--help`
    - Available tables: `products` and `categories`
    ```

    </div>

You can run AI applications directly with the **[Python SDK](./pages/python_sdk.md)**, or power them with your own agents via the **[MCP Server](./pages/mcp_server.md)**.

=== ":simple-python:{ .middle } &nbsp; Python SDK"

    ```python
    from toolfront import Application

    app = Application(url="file:///path/to/project")

    result = app.run("What's the status of order 66?", model="openai:gpt-5")
    ```

=== ":simple-modelcontextprotocol:{ .middle } &nbsp; MCP Server"

    ```json
    {
      "mcpServers": {
        "toolfront": {
          "command": "uvx",
          "args": ["toolfront", "mcp", "file:///path/to/project"],
        }
      }
    }
    ```

To get started, install `toolfront` with your favorite PyPI package manager.

=== ":fontawesome-brands-python:{ .middle } &nbsp; pip"

    ```bash
    pip install toolfront
    ```

=== ":simple-uv:{ .middle } &nbsp; uv"

    ```bash
    uv add toolfront
    ```

=== ":fontawesome-brands-python:{ .middle } &nbsp; poetry"

    ```bash
    poetry add toolfront
    ```


!!! toolfront "Deploy with ToolFront Cloud 🔥"

    Deploy your AI applications with **[ToolFront Cloud](pages/toolfront_cloud.md)**.

    ```bash
    toolfront deploy ./path/to/project
    ```

    This gives you an application URL you can run from anywhere.

    ```python
    app = Application(url="https://cloud.toolfront.ai/user/project", params={"API_KEY": ...})
    ```

    ToolFront Cloud is in beta. To request access, join our **[Discord](https://discord.gg/rRyM7zkZTf)** or email `esteban[at]kruskal[dot]ai`.