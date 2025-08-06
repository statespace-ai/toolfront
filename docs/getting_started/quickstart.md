---
hide:
  - toc
---

# Quickstart

## 1. Install ToolFront

Install ToolFront with support for your specific database:

```bash
pip install toolfront[postgres]
```

## 2. Setup your model provider API key

```bash
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

## 3. Ask about your data

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

That's it! ToolFront returns results in the format you need.

!!! tip
    **Need more options?** Check the [Databases section](../documentation/data_sources/databases.md) for connection examples with Snowflake, BigQuery, Athena, and more. See the [AI Models section](../documentation/ai_models/) for configuration examples with OpenAI, Anthropic, Google, and other providers.
