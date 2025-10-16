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
    <em>Data environments for AI agents</em>
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

ToolFront helps you organize AI workflows into independent tasks with **environments**. 

<!-- Markdown pages can contain instructions and tools for different tasks. -->

<!-- tasks. Each task is defined by a Markdown with instructions, tools, and data. -->

<!-- ToolFront helps you build and deploy environments for AI agents. Environments let you organize AI workflows into tasks, each defined by a Markdown with instructions, tools, and data. -->


=== ":material-home:{ .middle } &nbsp; Landing Page"

    Declare task instructions and tools in Markdown files.

    <div class="grid cards" markdown>

    ```bash hl_lines="2"
    environment/
    ├── index.md
    ├── pages/
    │   ├── text2sql.md
    │   ├── document.md
    │   └── api.md
    └── data/
        ├── invoices/
        └── logs/

    5 directories, 15 files
    ```

    ```markdown
    ---
    tools:
      - [date, +%Y-%m-%d]
    ---

    # Landing Page

    - Add links to other [pages](./pages)
    - Include tool commands in headers
    - Agents learn tools with `--help`
    ```

    </div>

=== ":material-database:{ .middle } &nbsp; Text-to-SQL"

    Create text-to-SQL tasks with ToolFront's built-in `database` CLI.

    <div class="grid cards" markdown>

    ```bash hl_lines="4"
    environment/
    ├── index.md
    ├── pages/
    │   ├── text2sql.md
    │   ├── document.md
    │   └── api.md
    └── data/
        ├── invoices/
        └── logs/

    5 directories, 15 files
    ```


    ```markdown
    ---
    tools:
      - [toolfront, database, $DB_URL]
    ---

    # Text-to-SQL

    - Add database metadata and context
    - Agents can list and inspect tables
    - All queries are read-only
    ```

    </div>


=== ":material-file-document:{ .middle } &nbsp; Document RAG"

    Retrieve information from data files like `.txt`, `.csv`, and `.json`.
      
    <div class="grid cards" markdown>

    ```bash hl_lines="5 7-9"
    environment/
    ├── index.md
    ├── pages/
    │   ├── text2sql.md
    │   ├── document.md
    │   └── api.md
    └── data/
        ├── invoices/
        └── logs/

    5 directories, 15 files
    ```


    ```markdown
    ---
    tools:
      - [python, extract.py]
    ---

    # Document RAG

    - Add data files and descriptions
    - Agents read and search documents
    - Use custom tools to process data
    ```

    </div>



=== ":material-api:{ .middle } &nbsp; API Integration"

      Fetch live data with calls to external APIs.

      <div class="grid cards" markdown>

      ```bash hl_lines="6"
      environment/
      ├── index.md
      ├── pages/
      │   ├── text2sql.md
      │   ├── document.md
      │   └── api.md
      └── data/
          ├── invoices/
          └── logs/

      5 directories, 15 files
      ```

      ```markdown
      ---
      tools:
        - [curl, "https://api.com/v1/user"]
      ---

      # API Integration

      - Define API endpoints as tools
      - Pass env `$VARS` for secrets
      - Agents fetch live external data
      ```

      </div>

Agents browse environments to get work done, using tools and following instructions as needed.

=== ":simple-python:{ .middle } &nbsp; Python SDK"

    Run Python agents on your environments.

    ```python
    from toolfront import Environment

    environment = Environment(url="file:///path/environment")

    answer = environment.run("What's our best-seller?", model="openai:gpt-5")
    ```

=== ":simple-modelcontextprotocol:{ .middle } &nbsp; MCP Server"

    Connect your own agents to environments.

    ```json
    {
      "mcpServers": {
        "toolfront": {
          "command": "uvx",
          "args": ["toolfront", "mcp", "file:///path/toolsite"],
          "env": {}
        }
      }
    }
    ```

Agents interact with environments using six core tools:

- :material-play:{ .middle } `execute` - Execute tools commands in headers, optionally passing parameters
- :material-eye:{ .middle } `read` - Read the content of a specific file
- :material-file-tree:{ .middle } `tree` - View directory structure
- :material-folder-search:{ .middle } `glob` - List files matching a glob pattern
- :material-regex:{ .middle } `grep` - Search files using regex patterns
- :material-magnify:{ .middle } `search` - Find relevant documents with BM25[^1]

[^1]: `search` requires indexing environment files.

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

    Instantly deploy your environments with **ToolFront Cloud**.
    
    ```bash
    toolfront deploy ./path/environment --api-key "my-api-key"
    ```
    
    Would give you a secure environment URL your agents can browse from anywhere.

    ```python
    environment = Environment(url="https://cloud.toolfront.ai/user/environment")
    ```

    Environments deployed with **ToolFront Cloud** are automatically indexed and get access to the powerful `search` tool.

    ```
    Let me search for documents relevant to "ticket pricing API"...

    Found 3 relevant pages:
      - ./api/pricing.md (highly relevant)
      - ./guides/analytics.md (relevant)
      - ./examples/queries.md (somewhat relevant)

    I'll start by reading ./api/pricing.md...
    ```

    **ToolFront Cloud** is currently in beta. To request access, join our [Discord](https://discord.gg/rRyM7zkZTf) or email `esteban[at]kruskal[dot]ai`.