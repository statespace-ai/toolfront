# Database CLI

ToolFront's built-in `database` CLI provides text-to-SQL capabilities for AI agents through  [Ibis](https://ibis-project.org/).

```markdown
---
tools:
  - [toolfront, database, $POSTGRES_URL]

---

# Database Page

Query the database for information about users, products, or transactions.
```


---

## Installation

Install ToolFront with any of the 15+ database backends supported by [Ibis](https://ibis-project.org/).


=== ":simple-postgresql:{ .middle } &nbsp; PostgreSQL"

    ```bash
    pip install "toolfront[postgres]"
    ```

=== ":simple-mysql:{ .middle } &nbsp; MySQL"

    ```bash
    pip install "toolfront[mysql]"
    ```

=== ":simple-sqlite:{ .middle } &nbsp; SQLite"

    ```bash
    pip install "toolfront[sqlite]"
    ```

=== ":simple-snowflake:{ .middle } &nbsp; Snowflake"

    ```bash
    pip install "toolfront[snowflake]"
    ```

=== ":simple-googlebigquery:{ .middle } &nbsp; BigQuery"

    ```bash
    pip install "toolfront[bigquery]"
    ```

=== ":simple-databricks:{ .middle } &nbsp; Databricks"

    ```bash
    pip install "toolfront[databricks]"
    ```

---

## Available Commands

Agents use three sub-commands to explore and query databases:

| Command | Description | Example |
|---------|-------------|---------|
| `list-tables` | List all tables available in the database | `toolfront database $DB_URL list-tables` |
| `inspect-table` | Inspect table schema and view sample data | `toolfront database $DB_URL inspect-table users` |
| `query` | Execute read-only SQL queries | `toolfront database $DB_URL query "SELECT * FROM users LIMIT 10"` |

---

!!! tip "Database Secrets"

    Use environment variables to keep database credentials private, e.g. `$POSTGRES_URL`. See [tools](./tools.md) for more details.