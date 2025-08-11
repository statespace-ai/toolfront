---
hide:
  - title
  - header
  - footer
  - navigation
  - toc
---

<div class="grid header" style="padding-top: 10%; padding-bottom: 10%;" markdown>

<div style="padding-right: 5%;" markdown>


<h1 style="font-size: 40px">
  <b>Data retrieval for AI agents</b>
</h1>

<h2>Simple, open-source data retrieval with unmatched control, precision, and speed.</h2>


[Quickstart](#quick-install){ .md-button .md-button--primary }
[Learn more](documentation/retrieval/){ .md-button .md-button--secondary }

</div>

<div class="tabbed-set" markdown="1">

=== ":fontawesome-solid-database:{ .middle } &nbsp; Databases"

    ```python
    from toolfront import Database

    # Connect +10 databases and warehouses
    db = Database("postgres://user:pass@localhost:5432/mydb")

    answer = db.ask("What's the revenue of our top-5 products")
    print(answer)
    ```

=== ":fontawesome-solid-code:{ .top } &nbsp; APIs"

    ```python
    from toolfront import API

    # Connect any API with a spec
    api = API("http://localhost:8000/openapi.json")

    answer = api.ask("Get the latest ticket for user_id=42")
    print(answer)
    ```

=== ":fontawesome-solid-file:{ .top } &nbsp; Documents"

    ```python
    from toolfront import Document

    # Connect any document
    doc = Document("/path/annual_report.pdf")

    answer = doc.retrieve("What were the montlhly payments?")
    print(answer)
    ```

</div>

</div>

<br>

<h2 align="center"><b>Bring your data and LLM.</b></h2>

<div class="db-marquee">
  <div class="db-marquee-track">
    <div class="db-marquee-item" data-db="postgres">
      <img src="assets/img/databases/postgres.svg" alt="PostgreSQL" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="mysql">
      <img src="assets/img/databases/mysql.svg" alt="MySQL" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="sqlite">
      <img src="assets/img/databases/sqlite.svg" alt="SQLite" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="snowflake">
      <img src="assets/img/databases/snowflake.svg" alt="Snowflake" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="bigquery">
      <img src="assets/img/databases/bigquery.svg" alt="BigQuery" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="databricks">
      <img src="assets/img/databases/databricks.svg" alt="Databricks" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="duckdb">
      <img src="assets/img/databases/duckdb.svg" alt="DuckDB" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="postgres">
      <img src="assets/img/databases/supabase.svg" alt="Supabase" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="oracle">
      <img src="assets/img/databases/oracle.svg" alt="Oracle" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="sqlserver">
      <img src="assets/img/databases/mssql.svg" alt="SQL Server" class="db-marquee-icon">
    </div>
  </div>
</div>


<div class="models-marquee">
  <div class="models-marquee-track">
    <div class="models-marquee-item" data-model="openai">
      <img src="assets/img/models/chatgpt.svg" alt="ChatGPT" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="anthropic">
      <img src="assets/img/models/claude.svg" alt="Claude" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="google">
      <img src="assets/img/models/gemini.svg" alt="Gemini" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="mistral">
      <img src="assets/img/models/mistral.svg" alt="Mistral" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="xai">
      <img src="assets/img/models/xai.svg" alt="xAI Grok" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="huggingface">
      <img src="assets/img/models/huggingface.svg" alt="Hugging Face" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="deepseek">
      <img src="assets/img/models/deepseek.svg" alt="DeepSeek" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="groq">
      <img src="assets/img/models/groq.svg" alt="Groq" class="models-marquee-icon">
    </div>
  </div>
</div>

<br>

<div class="main-container-left" markdown>

<div class="grid-item-text" markdown>

## **Zero Configuration** {#quick-install}

Skip config files and infrastructure setup. ToolFront works out of the box with all your data and models.

[Learn More](documentation/ai_models/openai.md){ .md-button .md-button--secondary }

</div>

<div class="tabbed-set" markdown="1">

<!-- === ":fontawesome-solid-download:{ .middle } &nbsp; pip"
    ```bash
    pip install "toolfront[postgres]"
    ```

    === "OpenAI"
        ```bash
        export OPENAI_API_KEY=<YOUR-KEY>
        ```

        <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

        ```python
        Database("postgres://...", model="openai:gpt-4o")
        ```

    === "Anthropic"
        ```bash
        export ANTHROPIC_API_KEY=<YOUR-KEY>
        ```

        <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

        ```python
        Database("postgres://...", model="anthropic:claude-3-5-sonnet")
        ```


=== ":simple-uv:{ .middle } &nbsp; uv"
    ```bash
    pip install "toolfront[postgres]"
    ```

    === "OpenAI"
        ```bash
        export OPENAI_API_KEY=<YOUR-KEY>
        ```

    === "Anthropic"
        ```bash
        export ANTHROPIC_API_KEY=<YOUR-KEY>
        ``` -->

=== ":fontawesome-solid-download:{ .middle } &nbsp; pip"

    ```bash
    pip install "toolfront[postgres]"
    ```

    <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

    ```bash
    export OPENAI_API_KEY=<YOUR-KEY>
    ```

    <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

    ```python
    Database("postgres://...", model="openai:gpt-4o")
    ```

=== ":simple-uv:{ .middle } &nbsp; uv"

    ```bash
    uv add "toolfront[snowflake]"
    ```

    <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

    ```bash
    export ANTHROPIC_API_KEY=<YOUR-KEY>
    ```

    <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

    ```python
    Database("snowflake://...", model="anthropic:claude-3-5-sonnet")
    ```

=== ":simple-poetry:{ .middle } &nbsp; poetry"

    ```bash
    poetry add "toolfront[bigquery]" 
    ```

    <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

    ```bash
    export GOOGLE_API_KEY=<YOUR-KEY>
    ```

    <center>:material-arrow-down:{ style="font-size: 24px;" }</center>

    ```python
    Database("bigquery://...", model="google:gemini-pro")
    ```

</div>

</div>

<div class="main-container-right" markdown>

<div class="tabbed-set" markdown="1">

=== ":fontawesome-solid-cube:{ .middle } &nbsp; Primitives"

    ```python
    from toolfront import Database

    db = Database("postgres://user:pass@host/db")

    best_seller: str = db.ask("What's our best-seller?")
    # Returns: "Laptop Pro"

    total_orders: int = db.ask("How many orders do we have?")
    # Returns: 125

    has_inventory: bool = db.ask("Do we have pending refunds?")
    # Returns: True
    ```


=== ":fontawesome-solid-layer-group:{ .middle } &nbsp; Collections"

    ```python
    from toolfront import Database

    db = Database("postgres://user:pass@host/db")

    monthly_sales: list[int] = db.ask("Monthly sales this year?")
    # Returns: [15000, 18000, 22000]

    sales_by_region: dict[str, int] = db.ask("Sales by region?")
    # Returns: {"North": 45000, "South": 38000}

    unique_brands: set[str] = db.ask("What brands do we carry?")
    # Returns: {"Apple", "Dell", "HP"}
    ```

=== ":fontawesome-solid-chain:{ .middle } &nbsp; Unions"

    ```python
    from toolfront import Database

    db = Database("postgres://user:pass@host/db")

    price: int | float = db.ask("Price of product XYZ?")
    # Returns: 30 or 29.99

    result: list[str] | str = db.ask("Best-sellers this month?")
    # Returns: ["Product A", "Product B"] or "Product C"

    error: str | None = db.ask("What was the the error message?")
    # Returns: "Connection timeout" or None
    ```


=== ":fontawesome-solid-sitemap:{ .middle } &nbsp; Pydantic Objects"

    ```python
    from toolfront import Database
    from pydantic import BaseModel

    db = Database("postgres://user:pass@host/db")

    class Customer(BaseModel):
        name: str
        seats: int
        is_active: bool

    top_customer: Customer = db.ask("Who's our latest customer?")
    # Returns: Customer(name='Acme', seats=5, is_active=True), 
    ```

</div>

<div class="grid-item-text" markdown>

## **Predictable Results**

Data is messy. ToolFront returns structured, type-safe responses that match exactly what you want.

[Learn more](documentation/retrieval.md){ .md-button .md-button--secondary }

</div>

</div>

<div class="main-container-left" markdown>

<div class="grid-item-text" markdown>

## **Use it Anywhere**

Avoid lock-ins and migrations. Run ToolFront standalone, as an MCP server, or with your favorite AI frameworks.

[Learn more](documentation/mcp.md){ .md-button .md-button--secondary }


</div>

<div class="tabbed-set" markdown="1">

=== ":simple-modelcontextprotocol:{ .middle } &nbsp; MCP"

    ```python linenums="1"
    # Add to Cursor/Copilot/Claude Desktop MCP config
    {
      "mcpServers": {
        "toolfront": {
          "command": "uvx",
          "args": [
            "toolfront[postgres]", 
            "postgres://user:pass@host/db"
          ]
        }
      }
    }
    ```

=== ":simple-langchain:{ .middle } &nbsp; LangChain"

    ```python hl_lines="1 6-8"
    from toolfront import Database
    from langchain.chat_models import init_chat_model
    from langchain.agents import (create_tool_calling_agent,
                                  AgentExecutor)

    data = Database("postgres://user:pass@localhost/mydb")
    tools = data.tools()
    prompt = data.instructions()

    model = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    agent = create_tool_calling_agent(model, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    ```

=== ":simple-ollama:{ .middle } &nbsp; LlamaIndex"

    ```python hl_lines="1 5-7"
    from toolfront import Database
    from llama_index.core.agent.workflow import FunctionAgent
    from llama_index.llms.openai import OpenAI

    data = Database("postgres://user:pass@localhost/mydb")
    tools = data.tools()
    prompt = data.instructions()

    llm = OpenAI(model="gpt-4o")  
    agent = FunctionAgent(tools, llm, system_prompt=prompt)
    response = agent.chat("What's our top selling product?")
    print(response)
    ```

</div>

</div>

</div>