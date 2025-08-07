# Flink

## Installation

```bash
pip install "toolfront[flink]"
```

## Connection URL

```
flink://
```

## Connection Parameters

| Name        | Type           | Description                           | Default      |
|-------------|----------------|---------------------------------------|--------------|
| `table_env` | `TableEnvironment` | PyFlink TableEnvironment instance    | **required** |

## Examples

**Using Connection Parameters:**
```python
from toolfront import Database
from pyflink.table import EnvironmentSettings, TableEnvironment

# Create PyFlink TableEnvironment
table_env = TableEnvironment.create(EnvironmentSettings.in_streaming_mode())

db = Database(
    url="flink://", # REQUIRED (1)
    table_env=table_env
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `flink` or `flink://` as the URL when creating a Flink `Database` from parameters. This is required for proper backend selection.