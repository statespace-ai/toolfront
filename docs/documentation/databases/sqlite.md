# SQLite

## Installation

```bash
pip install "toolfront[sqlite]"
```

## Connection URL

=== "In-Memory Database"
    ```
    sqlite://
    ```

=== "File-based database Database"
    ```
    sqlite://relative/path/to/mydb.sqlite
    ```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `database`               | `str | Path | None`                         | File path to the SQLite database file. If None, creates an in-memory transient database and you can use attach() to add more files                                                                                                                                                                                                       | `None`            |
| `type_map`               | `dict[str, str | dt.DataType] | None`       | An optional mapping from a string name of a SQLite "type" to the corresponding Ibis DataType that it represents. This can be used to override schema inference for a given SQLite database.                                                                                                                                              | `None`            |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

# File-based database
db = Database("sqlite:///path/to/mydb.sqlite")
revenue = db.ask("What's our total revenue this month?")

# In-memory database
db = Database("sqlite://")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="sqlite://", # REQUIRED (1)
    database="/path/to/mydb.sqlite"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `sqlite` or `sqlite://` as the URL when creating a SQLite `Database` from parameters. This is required for proper backend selection.