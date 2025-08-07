# ClickHouse

## Installation

```bash
pip install "toolfront[clickhouse]"
```

## Connection URL

=== "Basic"
    ```
    clickhouse://{user}:{password}@{host}:{port}/{database}
    ```

=== "With Secure Connection"
    ```
    clickhouse://{user}:{password}@{host}:{port}/{database}?secure=true
    ```

=== "With Compression"
    ```
    clickhouse://{user}:{password}@{host}:{port}/{database}?compression=lz4
    ```

## Connection Parameters

| Name           | Type         | Description                                                                                                                                                                                                                   | Default        |
|----------------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|
| `host`         | `str`        | Host name of the ClickHouse server.                                                                                                                                                                                           | `'localhost'`  |
| `port`         | `int | None`| ClickHouse HTTP server's port. If not passed, the value depends on whether `secure` is `True` or `False`.                                                                                                                   | `None`         |
| `database`     | `str`        | Default database when executing queries.                                                                                                                                                                                      | `'default'`    |
| `user`         | `str`        | User to authenticate with.                                                                                                                                                                                                    | `'default'`    |
| `password`     | `str`        | Password to authenticate with.                                                                                                                                                                                                | `''`           |
| `client_name`  | `str`        | Name of client that will appear in ClickHouse server logs.                                                                                                                                                                    | `'ibis'`       |
| `secure`       | `bool | None`| Whether or not to use an authenticated endpoint.                                                                                                                                                                              | `None`         |
| `compression`  | `str | bool`| The kind of compression to use for requests. See [ClickHouse Python Compression Docs](https://clickhouse.com/docs/en/integrations/python#compression) for more information.                                                | `True`         |
| `kwargs`       | `typing.Any` | Client specific keyword arguments.                                                                                                                                                                                            | `{}`           |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database("clickhouse://user:pass@localhost:9000/sales")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="clickhouse://", # REQUIRED (1)
    host="localhost",
    port=9000,
    database="sales",
    user="user",
    password="pass",
    secure=False
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `clickhouse` or `clickhouse://` as the URL when creating a ClickHouse `Database` from parameters. This is required for proper backend selection.