# Database Examples

Real-world examples for connecting to and querying different database systems.

## PostgreSQL

```python
from toolfront import Database

# Connect to PostgreSQL
db = Database("postgresql://user:password@localhost:5432/mydb")

# Natural language queries
revenue: int = db.ask("What's our total revenue this month?")
top_customers: list[str] = db.ask("Who are our top 10 customers by spending?")

print(f"Monthly revenue: ${revenue:,}")
```

## Snowflake

```python
from toolfront import Database

# Connect to Snowflake
db = Database("snowflake://user:password@account/database/schema")

# Query data warehouse
sales_data: db.Table = db.ask("Get all sales data for Q4 analysis")
df = sales_data.to_dataframe()

# Export large datasets with zero tokens
sales_data.to_csv("q4_sales.csv")
```

## BigQuery

```python
from toolfront import Database

# Connect to BigQuery
db = Database("bigquery://project-id/dataset-id")

# Analytics queries
monthly_trends: dict = db.ask("Show monthly user growth trends")
conversion_rate: float = db.ask("What's our conversion rate this quarter?")
```

## MySQL

```python
from toolfront import Database

# Connect to MySQL
db = Database("mysql://user:password@localhost:3306/database")

# E-commerce queries
inventory: list[dict] = db.ask("Show products with low inventory")
best_sellers: list[str] = db.ask("What are our top selling products?")
```

## SQLite

```python
from toolfront import Database

# Connect to SQLite file
db = Database("sqlite:///path/to/database.db")

# Local database queries
user_count: int = db.ask("How many users are registered?")
recent_activity: list[dict] = db.ask("Show recent user activity")
```

## ClickHouse

```python
from toolfront import Database

# Connect to ClickHouse
db = Database("clickhouse://user:password@host:9000/database")

# High-performance analytics
page_views: dict = db.ask("Aggregate page views by hour for last week")
real_time_metrics: dict = db.ask("Show real-time performance metrics")
```

## Databricks

```python
from toolfront import Database

# Connect to Databricks
db = Database("databricks://", 
              server_hostname="your-workspace.cloud.databricks.com",
              http_path="/sql/1.0/warehouses/warehouse-id",
              access_token="your-token")

# Data lake queries
ml_features: db.Table = db.ask("Extract features for ML model training")
data_quality: dict = db.ask("Run data quality checks on recent ingests")
```

## Oracle

```python
from toolfront import Database

# Connect to Oracle
db = Database("oracle://user:password@host:1521/service")

# Enterprise queries
financial_summary: dict = db.ask("Generate monthly financial summary")
compliance_report: list[dict] = db.ask("Show compliance violations")
```

## Advanced Examples

### Structured Data Extraction

```python
from pydantic import BaseModel
from toolfront import Database

class CustomerInsight(BaseModel):
    name: str
    total_spent: float
    last_purchase_date: str
    segment: str

db = Database("postgresql://user:pass@host/db")

# Get structured customer data
insights: list[CustomerInsight] = db.ask("Analyze our top 20 customers")

for customer in insights:
    print(f"{customer.name}: ${customer.total_spent:,.2f} ({customer.segment})")
```

### Large Dataset Processing

```python
from toolfront import Database

db = Database("snowflake://user:pass@account/db")

# Export millions of rows with zero additional tokens
all_transactions: db.Table = db.ask("Get all transaction data from 2024")

# Process locally
df = all_transactions.to_dataframe()
print(f"Exported {len(df):,} transactions")

# Analyze without API calls
monthly_totals = df.groupby(df['date'].dt.month)['amount'].sum()
high_value = df[df['amount'] > 10000]
```

### Multi-Database Analysis

```python
from toolfront import Database

# Connect to multiple databases
sales_db = Database("postgresql://user:pass@host/sales")
analytics_db = Database("bigquery://project/analytics")

# Compare data across systems
postgres_revenue: float = sales_db.ask("What's our total revenue?")
bigquery_revenue: float = analytics_db.ask("What's our total revenue?")

if abs(postgres_revenue - bigquery_revenue) > 1000:
    print("Revenue mismatch detected between systems!")
```