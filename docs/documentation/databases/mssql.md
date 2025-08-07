# SQL Server

## Installation

```bash
pip install "toolfront[mssql]"
```

## Connection URL

```
mssql://{user}:{password}@{host}:{port}
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `host`                   | `str`                                       | Address of MSSQL server to connect to.                                                                                                                                                                                                                                                                                                     | `'localhost'`     |
| `user`                   | `str | None`                                | Username. Leave blank to use Integrated Authentication.                                                                                                                                                                                                                                                                                    | `None`            |
| `password`               | `str | None`                                | Password. Leave blank to use Integrated Authentication.                                                                                                                                                                                                                                                                                    | `None`            |
| `port`                   | `int`                                       | Port of MSSQL server to connect to.                                                                                                                                                                                                                                                                                                        | `1433`            |
| `database`               | `str | None`                                | The MSSQL database to connect to.                                                                                                                                                                                                                                                                                                          | `None`            |
| `driver`                 | `str | None`                                | ODBC Driver to use. On Mac and Linux this is usually 'FreeTDS'. On Windows, it is usually one of: - ODBC Driver 11 for SQL Server - ODBC Driver 13 for SQL Server (for both 13 and 13.1) - ODBC Driver 17 for SQL Server - ODBC Driver 18 for SQL Server See https://learn.microsoft.com/en-us/sql/connect/odbc/windows/system-requirements-installation-and-driver-files | `None`            |
| `kwargs`                 | `Any`                                       | Additional keyword arguments to pass to PyODBC.                                                                                                                                                                                                                                                                                            | `{}`              |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database("mssql://user:pass@localhost:1433/sales")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="mssql://", # REQUIRED (1)
    host="localhost",
    port=1433,
    database="sales",
    user="user",
    password="pass"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `mssql` or `mssql://` as the URL when creating a SQL Server `Database` from parameters. This is required for proper backend selection.