# ClickHouse

## Installation

```bash
pip install toolfront[clickhouse]
```

## Basic Connection

```python
from toolfront import Database

db = Database("clickhouse://user:password@host:9000/database")
answer = db.ask("What's our total revenue this month?")
```

## Connection String Format

```
clickhouse://[user[:password]@][host][:port][/database][?param1=value1&...]
```

## Configuration Parameters

- `host`: Host name of the clickhouse server (default: 'localhost')
- `port`: ClickHouse HTTP server's port. If not passed, the value depends on whether secure is True or False
- `database`: Default database when executing queries (default: 'default')
- `user`: User to authenticate with (default: 'default')
- `password`: Password to authenticate with (default: '')
- `client_name`: Name of client that will appear in clickhouse server logs (default: 'ibis')
- `secure`: Whether or not to use an authenticated endpoint
- `compression`: The kind of compression to use for requests. See https://clickhouse.com/docs/en/integrations/python#compression for more information (default: True)
- `kwargs`: Client specific keyword arguments

## Connection Examples

```python
from toolfront import Database

# Basic connection
db = Database("clickhouse://user:password@localhost:9000/analytics")

# Secure connection
db = Database("clickhouse://user:pass@host:8443/db?secure=true")

# With compression
db = Database("clickhouse://user:pass@host:9000/db?compression=lz4")
```