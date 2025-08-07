# Databricks

## Installation

```bash
pip install "toolfront[databricks]"
```


## Connection URL
```
databricks://
```



## Connection Parameters

| Name      | Type            | Description                                                                 | Default   |
|-----------|-----------------|-----------------------------------------------------------------------------|-----------|
| `name`    | `str`           | Name of the database to create.                                             | **required**  |
| `catalog` | `str | None` | Name of the catalog in which to create the database. If None, the current catalog is used. | None      |
| `force`   | `bool`          | If False, an exception is raised if the database exists.                    | False     |

## Examples

**Using Connection Parameters:**

```python
from toolfront import Database

db = Database(
    url="databricks://", # REQUIRED (1)
    server_hostname="workspace.databricks.com", 
    http_path="/sql/1.0/warehouses/warehouse-id",
    access_token="token",
    catalog="sales",
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `databricks` or `databricks://` as the URL when creating a Databricks `Database` from parameters. This is required for proper backend selection.
