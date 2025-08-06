---
hide:
  - title
  - header
  - footer
  - navigation
  - toc
  
title: "ToolFront"
description: "TBD" 
---

<div class="grid header" style="padding-top: 10%; padding-bottom: 10%;" markdown>

<div style="padding-right: 5%;" markdown>


<h1 style="font-size: 50px">
  <b>Run ETL and retrieval pipelines in plain English</b>
</h1>

<h2> ToolFront ETL and retrieval pipelines in plain English </h2>


[Quickstart](getting_started/quickstart.md){ .md-button .md-button--primary }
[Learn more](documentation/index.md){ .md-button .md-button--secondary }

</div>

<div class="tabbed-set" markdown="1">

=== ":fontawesome-solid-database:{ .middle } &nbsp; Databases"

    ```python linenums="1"
    from toolfront import Database

    # Load databases/warehouses
    db = Database("postgresql://user:pass@localhost:5432/mydb")

    answer = db.ask("What's the revenue of the top 5 products")
    print(answer)
    ```

=== ":fontawesome-solid-code:{ .top } &nbsp; APIs"

    ```python linenums="1"
    from toolfront import API

    # Load internal/external APIs
    api = API("http://localhost:8000/openapi.json")

    answer = api.ask("Close the ticket for user_id=42")
    print(answer)
    ```

=== ":fontawesome-solid-file:{ .top } &nbsp; Documents"

    ```python linenums="1"
    from toolfront import Document

    # Load any document
    doc = Document("/path/to/annual_report.pdf")

    answer = doc.ask("Summarize the key financial results.")
    print(answer)
    ```

</div>

</div>

<h2 align="center"><b>Work with your favorite databases</b></h2>

<div class="db-marquee">
  <div class="db-marquee-track">
    <div class="db-marquee-item" data-db="postgresql">
      <img src="assets/icons/databases/postgres.svg" alt="PostgreSQL" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="mysql">
      <img src="assets/icons/databases/mysql.svg" alt="MySQL" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="sqlite">
      <img src="assets/icons/databases/sqlite.svg" alt="SQLite" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="snowflake">
      <img src="assets/icons/databases/snowflake.svg" alt="Snowflake" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="bigquery">
      <img src="assets/icons/databases/bigquery.svg" alt="BigQuery" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="databricks">
      <img src="assets/icons/databases/databricks.svg" alt="Databricks" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="duckdb">
      <img src="assets/icons/databases/duckdb.svg" alt="DuckDB" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="postgresql">
      <img src="assets/icons/databases/supabase.svg" alt="Supabase" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="oracle">
      <img src="assets/icons/databases/oracle.svg" alt="Oracle" class="db-marquee-icon">
    </div>
    <div class="db-marquee-item" data-db="sqlserver">
      <img src="assets/icons/databases/mssql.svg" alt="SQL Server" class="db-marquee-icon">
    </div>
  </div>
</div>

<br>

<div class="main-container-right" markdown>

<div class="tabbed-set" markdown="1">

=== ":fontawesome-solid-cube:{ .middle } &nbsp; Primitives"

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    best_seller: str = db.ask("What's our best-seller?")
    # Returns: "Laptop Pro"

    total_orders: int = db.ask("How many orders do we have?")
    # Returns: 125

    has_inventory: bool = db.ask("Do we have pending refunds?")
    # Returns: True
    ```


=== ":fontawesome-solid-layer-group:{ .middle } &nbsp; Collections"

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    monthly_sales: list[int] = db.ask("Monthly sales this year?")
    # Returns: [15000, 18000, 22000]

    sales_by_region: dict[str, int] = db.ask("Sales by region?")
    # Returns: {"North": 45000, "South": 38000}

    unique_brands: set[str] = db.ask("What brands do we carry?")
    # Returns: {"Apple", "Dell", "HP"}
    ```

=== ":fontawesome-solid-chain:{ .middle } &nbsp; Union Types"

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    price: int | float = db.ask("Price of product XYZ?")
    # Returns: 29.99, 30

    result: str | list[str] = db.ask("Best-sellers this month?")
    # Returns: ["Product A", "Product B"] or "No data found"

    error: str | None = db.ask("What was the the error message?")
    # Returns: "Connection timeout" or None
    ```


=== ":fontawesome-solid-sitemap:{ .middle } &nbsp; Pydantic Objects"

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    from pydantic import BaseModel
    class Customer(BaseModel):
        name: str
        revenue: int

    top_customers: list[Customer] = db.ask("Top 2 customers?")
    # Returns: [Customer(name='Acme Corp', revenue=50000), 
    #           Customer(name='Beta LLC', revenue=42000)]
    ```

</div>

<div class="grid-item-text" markdown>

## **Structure Your Outputs**

Raw data is often messy and inconsistent. With ToolFront, you get structured, type-safe outputs that match exactly what your application expects.

[Learn more](/docs/concepts/structured_outputs){ .md-button .md-button--secondary }


</div>

</div>

<h2 align="center"><b>Bring your own models</b></h2>

<div class="models-marquee">
  <div class="models-marquee-track">
    <div class="models-marquee-item" data-model="openai">
      <img src="assets/icons/models/chatgpt.svg" alt="ChatGPT" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="anthropic">
      <img src="assets/icons/models/claude.svg" alt="Claude" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="google">
      <img src="assets/icons/models/gemini.svg" alt="Gemini" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="mistral">
      <img src="assets/icons/models/mistral.svg" alt="Mistral" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="xai">
      <img src="assets/icons/models/xai.svg" alt="xAI Grok" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="huggingface">
      <img src="assets/icons/models/huggingface.svg" alt="Hugging Face" class="models-marquee-icon">
    </div>    
    <div class="models-marquee-item" data-model="deepseek">
      <img src="assets/icons/models/deepseek.svg" alt="DeepSeek" class="models-marquee-icon">
    </div>
    <div class="models-marquee-item" data-model="groq">
      <img src="assets/icons/models/groq.svg" alt="Groq" class="models-marquee-icon">
    </div>    
  </div>
</div>


<div class="main-container-left" markdown>

<div class="grid-item-text" markdown>

## **Plug n' Play**

AI frameworks often create vendor lock-in and force you to rebuild existing workflows. ToolFront works with any agent framework or AI tool you're already using.

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
            "postgresql://user:pass@host/db"
          ]
        }
      }
    }
    ```

=== ":simple-langchain:{ .middle } &nbsp; LangChain"

    ```python linenums="1" hl_lines="1 6-8"
    from toolfront import Database
    from langchain.chat_models import init_chat_model
    from langchain.agents import (create_tool_calling_agent,
                                  AgentExecutor)

    data = Database("postgresql://user:pass@localhost/mydb")
    tools = data.tools()
    prompt = data.instructions()

    model = init_chat_model("anthropic:claude-3-5-sonnet-latest")
    agent = create_tool_calling_agent(model, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    ```

=== ":simple-ollama:{ .middle } &nbsp; LlamaIndex"

    ```python linenums="1" hl_lines="1 5-7"
    from toolfront import Database
    from llama_index.core.agent.workflow import FunctionAgent
    from llama_index.llms.openai import OpenAI

    data = Database("postgresql://user:pass@localhost/mydb")
    tools = data.tools()
    system_prompt = data.instructions()

    llm = OpenAI(model="gpt-4o")  
    agent = FunctionAgent(tools, llm, system_prompt=prompt)
    response = agent.chat("What's our top selling product?")
    print(response)
    ```

</div>

</div>

</div>

