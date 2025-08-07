# MySQL

## Installation

```bash
pip install "toolfront[mysql]"
```

## Connection URL

```
mysql://{user}:{password}@{host}:{port}/{database}
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `host`                   | `str`                                       | Hostname                                                                                                                                                                                                                                                                                                                                    | `'localhost'`     |
| `user`                   | `str | None`                                | Username                                                                                                                                                                                                                                                                                                                                    | `None`            |
| `password`               | `str | None`                                | Password                                                                                                                                                                                                                                                                                                                                    | `None`            |
| `port`                   | `int`                                       | Port                                                                                                                                                                                                                                                                                                                                        | `3306`            |
| `autocommit`             | `bool`                                      | Autocommit mode                                                                                                                                                                                                                                                                                                                             | `True`            |
| `kwargs`                 | `Any`                                       | Additional keyword arguments passed to MySQLdb.connect                                                                                                                                                                                                                                                                                     | `{}`              |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database("mysql://user:pass@localhost:3306/sales")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="mysql://", # REQUIRED (1)
    host="localhost",
    port=3306,
    database="sales",
    user="user",
    password="pass"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `mysql` or `mysql://` as the URL when creating a MySQL `Database` from parameters. This is required for proper backend selection.