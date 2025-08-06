# PostgreSQL

## Installation

```bash
pip install toolfront[postgres]
```

## Basic Connection

```python
from toolfront import Database

db = Database("postgresql://user:password@host:port/database")
answer = db.ask("What's our total revenue this month?")
```

## Connection String Format

```
postgresql://[user[:password]@][host][:port][/database][/schema][?param1=value1&...]
```

## Configuration Parameters

- `host`: Hostname (default: None)
- `user`: Username (default: None) 
- `password`: Password (default: None)
- `port`: Port number (default: 5432)
- `database`: Database to connect to (default: None)
- `schema`: PostgreSQL schema to use. If None, use the default search_path (default: None)
- `autocommit`: Whether or not to autocommit (default: True)
- `kwargs`: Additional keyword arguments to pass to the backend client connection

## Connection Examples

```python
from toolfront import Database

# Basic connection
db = Database("postgresql://postgres:password@localhost:5432/myapp")

# With SSL
db = Database("postgresql://user:pass@host:5432/db?sslmode=require")

# With schema
db = Database("postgresql://user:pass@host:5432/database/public")
```