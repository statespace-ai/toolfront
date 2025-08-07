# PySpark

## Installation

```bash
pip install "toolfront[pyspark]"
```

## Connection URL

```
pyspark://
```

## Connection Parameters

| Name                     | Type                                        | Description                                                                                                                                                                                                                                                                                                                                 | Default           |
|--------------------------|---------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|
| `session`                | `SparkSession | None`                       | A SparkSession instance.                                                                                                                                                                                                                                                                                                                   | `None`            |
| `mode`                   | `str`                                       | Can be either "batch" or "streaming". If "batch", every source, sink, and query executed within this connection will be interpreted as a batch workload. If "streaming", every source, sink, and query executed within this connection will be interpreted as a streaming workload.                                                     | `'batch'`         |
| `kwargs`                 | `Any`                                       | Additional keyword arguments used to configure the SparkSession.                                                                                                                                                                                                                                                                           | `{}`              |

## Examples

**Using Connection Parameters:**
```python
from toolfront import Database
from pyspark.sql import SparkSession

# Create PySpark SparkSession
session = SparkSession.builder.getOrCreate()

db = Database(
    url="pyspark//", # REQUIRED (1)
    session=session,
    mode="batch"
)
revenue = db.ask("What's our total revenue this month?")
```

1. You must always pass `pyspark` or `pyspark://` as the URL when creating a PySpark `Database` from parameters. This is required for proper backend selection.