# Druid

## Installation

```bash
pip install "toolfront[druid]"
```

## Connection URL

```
druid://{host}:{port}/{path}
```

## Connection Parameters

| Name     | Type     | Description                                      | Default     |
|----------|----------|--------------------------------------------------|-------------|
| `host`   | `str`    | Hostname or IP address of the Druid broker node. | None |
| `port`   | `int`    | Port number for the Druid broker node.           | None      |
| `path`   | `str`    | Path to the Druid endpoint (if needed).          | None        |

## Examples

**Using Connection URL:**
```python
from toolfront import Database

db = Database("druid://localhost:8082/druid/v2/sql")
revenue = db.ask("What's our total revenue this month?")
```

**Using Connection Parameters:**
```python
from toolfront import Database

db = Database(
    url="druid://", # REQUIRED (1)
    host="hostname",
    port=8082,
    path="druid/v2/sql",
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `druid` or `druid://` as the URL when creating a Druid `Database` from parameters. This is required for proper backend selection.

