# DuckDB

## Installation

```bash
pip install "toolfront[duckdb]"
```

## Connection URL

=== "In-memory Database"
    ```
    duckdb://
    ```

=== "File-based Database"
    ```
    duckdb://path/to/database.db
    ```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `database`               | `str | Path`                                | Path to a duckdb database.                                                                                                                                                                                                                                                                                                                 | `':memory:'`      |
| `read_only`              | `bool`                                      | Whether the database is read-only.                                                                                                                                                                                                                                                                                                         | `False`           |
| `extensions`             | `Sequence[str] | None`                      | A list of duckdb extensions to install/load upon connection.                                                                                                                                                                                                                                                                               | `None`            |
| `config`                 | `Any`                                       | DuckDB configuration parameters. See the DuckDB configuration documentation for possible configuration values.                                                                                                                                                                                                                             | `{}`              |

## Examples

**Using Connection Parameters:**
```python
from toolfront import Database

# In-memory database
db = Database(
    url="duckdb", # REQUIRED (1)
    database=":memory:"
)
revenue = db.ask("What's our total revenue this month?")

# File-based database and extensions
db = Database(
    url="duckdb://", # REQUIRED (2)
    database="mydata.duckdb",
    extensions=["httpfs", "parquet"],
    read_only=False,
    config={"threads": 4}
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `duckdb` or `duckdb://` as the URL when creating a DuckDB `Database` from parameters. This is required for proper backend selection.
2. You must always pass `duckdb` or `duckdb://` as the URL when creating a DuckDB `Database` from parameters. This is required for proper backend selection.