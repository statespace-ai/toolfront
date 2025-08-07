# Oracle

## Installation

```bash
pip install "toolfront[oracle]"
```

## Connection URL

```
oracle://{user}:{password}@{host}:{port}/{database}
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `user`                   | `str`                                       | Username                                                                                                                                                                                                                                                                                                                                    | **required**      |
| `password`               | `str`                                       | Password                                                                                                                                                                                                                                                                                                                                    | **required**      |
| `host`                   | `str`                                       | Hostname                                                                                                                                                                                                                                                                                                                                    | `'localhost'`     |
| `port`                   | `int`                                       | Port                                                                                                                                                                                                                                                                                                                                        | `1521`            |
| `database`               | `str | None`                                | Used as an Oracle service name if provided.                                                                                                                                                                                                                                                                                                | `None`            |
| `sid`                    | `str | None`                                | Unique name of an Oracle Instance, used to construct a DSN if provided.                                                                                                                                                                                                                                                                   | `None`            |
| `service_name`           | `str | None`                                | Oracle service name, used to construct a DSN if provided. Only one of database and service_name should be provided.                                                                                                                                                                                                                      | `None`            |
| `dsn`                    | `str | None`                                | An Oracle Data Source Name. If provided, overrides all other connection arguments except username and password.                                                                                                                                                                                                                          | `None`            |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database("oracle://user:pass@localhost:1521/sales")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="oracle://", # REQUIRED (1)
    user="user",
    password="pass",
    host="localhost",
    port=1521,
    database="sales"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `oracle` or `oracle://` as the URL when creating an Oracle `Database` from parameters. This is required for proper backend selection.