# RisingWave

## Installation

```bash
pip install "toolfront[risingwave]"
```

## Connection URL

```
risingwave://
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `host`                   | `str | None`                                | Hostname                                                                                                                                                                                                                                                                                                                                    | `None`            |
| `user`                   | `str | None`                                | Username                                                                                                                                                                                                                                                                                                                                    | `None`            |
| `password`               | `str | None`                                | Password                                                                                                                                                                                                                                                                                                                                    | `None`            |
| `port`                   | `int`                                       | Port number                                                                                                                                                                                                                                                                                                                                 | `5432`            |
| `database`               | `str | None`                                | Database to connect to                                                                                                                                                                                                                                                                                                                      | `None`            |
| `schema`                 | `str | None`                                | RisingWave schema to use. If None, use the default search_path.                                                                                                                                                                                                                                                                            | `None`            |

## Examples

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="risingwave://", # REQUIRED (1)
    host="localhost",
    port=5432,
    database="sales",
    user="user",
    password="pass",
    schema="public"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `risingwave` or `risingwave://` as the URL when creating a RisingWave `Database` from parameters. This is required for proper backend selection.