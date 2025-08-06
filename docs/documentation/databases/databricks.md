# Databricks

## Installation

```bash
pip install toolfront[databricks]
```

## Basic Connection

```python
from toolfront import Database

db = Database(
    "databricks://",
    server_hostname="your-workspace.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/your-warehouse-id", 
    access_token="your-access-token"
)
answer = db.ask("What's our total revenue this month?")
```

## Connection String Format

```
databricks://
```

## Configuration Parameters

- `server_hostname`: Databricks workspace hostname
- `http_path`: HTTP path to the SQL warehouse
- `access_token`: Databricks personal access token
- `catalog`: Catalog name (optional)
- `schema`: Schema name (default: 'default')
- `session_configuration`: Additional session configuration parameters (optional)
- `http_headers`: Custom HTTP headers (optional)
- `use_cloud_fetch`: Enable cloud fetch optimization (default: False)
- `memtable_volume`: Volume for storing temporary tables (optional)
- `staging_allowed_local_path`: Local path allowed for staging (optional)

## Connection Examples

```python
from toolfront import Database

# Basic connection
db = Database(
    "databricks://",
    server_hostname="company.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/abc123def456",
    access_token="dapi1234567890abcdef"
)

# With catalog and schema
db = Database(
    "databricks://",
    server_hostname="workspace.databricks.com",
    http_path="/sql/1.0/warehouses/warehouse-id",
    access_token="token",
    catalog="production",
    schema="sales_data"
)

# With session configuration
db = Database(
    "databricks://",
    server_hostname="workspace.databricks.com",
    http_path="/sql/1.0/warehouses/warehouse-id",
    access_token="token",
    session_configuration={"spark.sql.adaptive.enabled": "true"}
)
```