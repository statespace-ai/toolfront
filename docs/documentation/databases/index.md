# Database Connections

ToolFront supports 15+ popular databases. Choose your database to get started with specific connection examples and configuration.

## Supported Databases

### Cloud Data Warehouses
- **[PostgreSQL](postgresql.md)** - Popular open-source relational database
- **[Snowflake](snowflake.md)** - Cloud data warehouse platform
- **[BigQuery](bigquery.md)** - Google's serverless data warehouse
- **[Databricks](databricks.md)** - Unified analytics platform

### Traditional Databases
- **[MySQL](mysql.md)** - World's most popular open-source database
- **[SQLite](sqlite.md)** - Lightweight embedded database
- **[Oracle](oracle.md)** - Enterprise database management system
- **[SQL Server](sqlserver.md)** - Microsoft's relational database

### Analytics & Performance
- **[ClickHouse](clickhouse.md)** - Fast columnar analytics database
- **[DuckDB](duckdb.md)** - In-process analytical database
- **[Trino](trino.md)** - Distributed SQL query engine

## Quick Start

1. **Install** the database-specific package:
   ```bash
   pip install toolfront[postgres]  # Replace with your database
   ```

2. **Set your AI API key**:
   ```bash
   export OPENAI_API_KEY=your_key
   ```

3. **Connect and query**:
   ```python
   from toolfront import Database
   
   db = Database("your_connection_string")
   result = db.ask("What data do you have?")
   ```

## Universal Examples

### Basic Connection Pattern
```python
from toolfront import Database

# Generic connection pattern
db = Database("protocol://user:password@host:port/database")

# Start asking questions
revenue: int = db.ask("What's our total revenue?")
customers: list[str] = db.ask("Who are our top customers?")
```

### With Business Context
```python
context = """
Our business context:
- E-commerce platform selling electronics
- 'orders' table contains purchase data
- 'customers' table has user information
- Revenue tracked in USD
"""

insights = db.ask(
    "What are our key business metrics?",
    context=context
)
```

### Structured Outputs
```python
from pydantic import BaseModel

class BusinessMetrics(BaseModel):
    total_revenue: float
    customer_count: int
    avg_order_value: float
    top_product: str

metrics: BusinessMetrics = db.ask("Calculate key business metrics")
```

## Connection Security

### Environment Variables
Store sensitive connection details in environment variables:

```bash
export DB_HOST=your_host
export DB_PASSWORD=your_password
```

```python
import os
from toolfront import Database

db = Database(f"postgresql://user:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/db")
```

### Read-Only Access
ToolFront only executes read-only queries for security:

```python
# These work (read operations)
data = db.ask("SELECT * FROM customers")
count = db.ask("COUNT(*) FROM orders")

# These are blocked (write operations)
# db.ask("DELETE FROM customers")  # ❌ Blocked
# db.ask("UPDATE orders SET ...")  # ❌ Blocked
```

## Performance Tips

### Table Filtering
Limit accessible tables for better performance:

```python
# Only access specific tables
db = Database(
    "postgresql://user:pass@host/db",
    match_tables="^(orders|customers|products)$"
)

# Only access production schemas
db = Database(
    "postgresql://user:pass@host/db", 
    match_schema=".*prod.*"
)
```

### Large Data Handling
Use Table types for large datasets:

```python
# Export large datasets with zero additional tokens
large_dataset: db.Table = db.ask("Get all historical sales data")

# Process locally
df = large_dataset.to_dataframe()
large_dataset.to_csv("export.csv")
```

## Troubleshooting

### Connection Issues
Common connection problems and solutions:

1. **Authentication**: Verify username/password
2. **Network**: Check host and port accessibility
3. **Database**: Ensure database exists and is accessible
4. **Permissions**: Verify user has read permissions

### Performance Issues
Optimize query performance:

1. **Use specific queries**: "Revenue for Q1" vs "All revenue data"
2. **Provide context**: Help AI understand your schema
3. **Filter tables**: Limit accessible tables with regex patterns
4. **Use appropriate models**: Simple queries don't need powerful models

## Next Steps

Choose your database from the list above for specific setup instructions, connection examples, and best practices.

Each database page includes:
- Installation commands
- Connection string format
- Configuration parameters
- Real-world examples
- Troubleshooting tips