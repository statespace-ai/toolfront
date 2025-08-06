# MySQL

## Installation

```bash
pip install toolfront[mysql]
```

## Basic Connection

```python
from toolfront import Database

db = Database("mysql://user:password@host:port/database")
answer = db.ask("What's our total revenue this month?")
```

## Connection String Format

```
mysql://[user[:password]@][host][:port][/database]
```

## Configuration Parameters

- `host`: Hostname (default: 'localhost')
- `user`: Username (default: None)
- `password`: Password (default: None)
- `port`: Port (default: 3306)
- `autocommit`: Autocommit mode (default: True)
- `kwargs`: Additional keyword arguments passed to MySQLdb.connect

## Connection Examples

```python
from toolfront import Database

# Basic connection
db = Database("mysql://root:password@localhost:3306/myapp")

# Remote connection
db = Database("mysql://user:pass@db.example.com:3306/production")

# With SSL
db = Database("mysql://user:pass@host:3306/db?ssl=true")
```