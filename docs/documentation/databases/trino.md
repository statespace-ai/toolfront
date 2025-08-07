# Trino

## Installation

```bash
pip install "toolfront[trino]"
```

## Connection URL

```
trino://{user}:{password}@{host}:{port}/{catalog}/{schema}
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `user`                   | `str`                                       | Username to connect with                                                                                                                                                                                                                                                                                                                    | `'user'`          |
| `password`               | `str | None`                                | Password to connect with. Mutually exclusive with auth.                                                                                                                                                                                                                                                                                    | `None`            |
| `host`                   | `str`                                       | Hostname of the Trino server                                                                                                                                                                                                                                                                                                               | `'localhost'`     |
| `port`                   | `int`                                       | Port of the Trino server                                                                                                                                                                                                                                                                                                                   | `8080`            |
| `database`               | `str | None`                                | Catalog to use on the Trino server                                                                                                                                                                                                                                                                                                         | `None`            |
| `schema`                 | `str | None`                                | Schema to use on the Trino server                                                                                                                                                                                                                                                                                                          | `None`            |
| `source`                 | `str | None`                                | Application name passed to Trino                                                                                                                                                                                                                                                                                                           | `None`            |
| `timezone`               | `str`                                       | Timezone to use for the connection                                                                                                                                                                                                                                                                                                          | `'UTC'`           |
| `auth`                   | `str | None`                                | Authentication method to use for the connection. Mutually exclusive with password.                                                                                                                                                                                                                                                         | `None`            |
| `kwargs`                 | `Any`                                       | Additional keyword arguments passed directly to the trino.dbapi.connect API.                                                                                                                                                                                                                                                               | `{}`              |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database("trino://user:pass@localhost:8080/sales/public")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="trino://", # REQUIRED (1)
    user="user",
    password="pass",
    host="localhost",
    port=8080,
    database="sales",
    schema="public"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `trino` or `trino://` as the URL when creating a Trino `Database` from parameters. This is required for proper backend selection.