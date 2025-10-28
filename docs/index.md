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
    <em>Build AI Agents in Markdown</em>
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

**ToolFront is a declarative framework for building AI agents in Markdown.**

Write tools and instructions in `.md` files. Run the project and get a live AI application.

---

## Simple Example

### Create it

  Start with **one file**: `README.md`


  ```markdown title="README.md"
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

Ask your agents about the application

=== ":simple-python:{ .middle } &nbsp; Python SDK"

    ```python
    from toolfront import Application

    app = Application(url="http://127.0.0.1:8000")

    result = app.ask("Is the service up?", model="openai:gpt-5")
    
    print(result)
    # Answer: yes
    ```

=== ":simple-modelcontextprotocol:{ .middle } &nbsp; MCP Server"

    ```json
    {
      "mcpServers": {
        "toolfront": {
          "command": "uvx",
          "args": ["toolfront", "mcp", "http://127.0.0.1:8000"],
        }
      }
    }
    ```

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

  ```markdown title="README.md" hl_lines="4-5 11"
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

  ```markdown title="src/rag.md"
  ---
  tools:
    - [grep]
  ---

  # Search Docs
  - Use `grep` to search files in `/data/`
  ```

### Add Text-to-SQL

  Connect your databases for SQL workflows


  ```markdown title="src/text2sql.md"
  ---
  tools:
    - [psql, -U, $USER, -d, $DATABASE, -c, {query}]
  ---

  # Database Access
  - Call the `psql` tool to query the PostgreSQL database
  ```

### Add Custom Tools

  Build custom tools in any programming language.

  ```markdown title="src/toolkit.md"
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

=== ":fontawesome-brands-python:{ .middle } &nbsp; pip"

    ```bash
    pip install toolfront
    ```

=== ":simple-uv:{ .middle } &nbsp; uv"

    ```bash
    uv add toolfront
    ```

=== ":simple-poetry:{ .middle } &nbsp; poetry"

    ```bash
    poetry add toolfront
    ```


!!! toolfront "Deploy to ToolFront Cloud 🔥"

    Instantly deploy your AI applications with **[ToolFront Cloud](pages/toolfront_cloud.md)**.

    ```bash
    toolfront deploy ./path/to/project
    ```

    This gives you a secure application URL you can access from anywhere.

    ```python
    app = Application(url="https://cloud.toolfront.ai/user/project", params={"API_KEY": ...})
    ```

    ToolFront Cloud is in beta. To request access, join our **[Discord](https://discord.gg/rRyM7zkZTf)** or email `esteban[at]statespace[dot]com`.