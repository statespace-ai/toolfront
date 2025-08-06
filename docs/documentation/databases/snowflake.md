# Snowflake

Configure ToolFront to connect to Snowflake data warehouse.

## Installation

```bash
pip install toolfront[snowflake]
```

## Connection

### Basic Connection
```python
from toolfront import Database

db = Database("snowflake://user:password@account/database/schema")

# Query your data warehouse
revenue: int = db.ask("What's our total revenue across all regions?")
print(f"Total Revenue: ${revenue:,}")
```

### Connection String Format
```
snowflake://[user[:password]@]account[/database[/schema]][?param1=value1&...]
```

### Examples
```python
# Standard connection
db = Database("snowflake://analyst:password@company123/ANALYTICS_DB/PUBLIC")

# With warehouse specification
db = Database("snowflake://user:pass@account123/DB/SCHEMA?warehouse=COMPUTE_WH")

# Multi-factor authentication
db = Database("snowflake://user@account123/DB/SCHEMA", authenticator='externalbrowser')
```

## Configuration Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `account` | Snowflake account identifier | `company123`, `xy12345.us-east-1` |
| `database` | Database name | `ANALYTICS_DB`, `SALES_DATA` |
| `schema` | Schema name | `PUBLIC`, `PRODUCTION` |
| `warehouse` | Virtual warehouse | `COMPUTE_WH`, `ANALYTICS_WH` |
| `role` | Role to assume | `ANALYST`, `DATA_SCIENTIST` |
| `authenticator` | Auth method | `externalbrowser`, `oauth` |

## Real-World Examples

### Data Warehouse Analytics
```python
from toolfront import Database
from pydantic import BaseModel

class SalesAnalysis(BaseModel):
    total_revenue: float
    units_sold: int
    avg_order_value: float
    top_region: str
    growth_rate: float

db = Database("snowflake://analyst:pass@company/SALES_DW/ANALYTICS")

# Comprehensive sales analysis
analysis: SalesAnalysis = db.ask(
    "Analyze sales performance across all dimensions for Q4"
)

print(f"Revenue: ${analysis.total_revenue:,.2f}")
print(f"Growth: {analysis.growth_rate:.1%}")
```

### Customer Data Platform
```python
# Connect to customer data warehouse
db = Database("snowflake://cdp_user:pass@company/CUSTOMER_360/PROD")

# Customer segmentation
segments = db.ask("Segment customers by lifetime value and engagement")
churn_risk = db.ask("Identify customers at risk of churning")
campaign_targets = db.ask("Find best customers for upsell campaign")
```

### Financial Reporting
```python
# Financial data warehouse
db = Database("snowflake://finance:pass@company/FINANCE_DW/REPORTING")

# Generate executive dashboard
executive_metrics = db.ask("""
    Generate executive dashboard with:
    - Revenue by business unit
    - Profit margins by product line  
    - Cash flow trends
    - Budget vs actual variance
""")
```

## Large Data Processing

### Efficient Data Exports
```python
# Snowflake excels at large data processing
db = Database("snowflake://user:pass@account/DATA_LAKE/RAW")

# Export millions of rows efficiently (zero additional tokens)
large_dataset: db.Table = db.ask("Get all customer transaction data for ML training")

# Process locally
df = large_dataset.to_dataframe()
print(f"Exported {len(df):,} transactions")

# Save for ML pipeline
large_dataset.to_parquet("ml_training_data.parquet")
```

### Time Series Analysis
```python
# Historical trend analysis
time_series_data = db.ask("""
    Analyze 3 years of daily sales data:
    - Identify seasonal patterns
    - Calculate growth trends
    - Detect anomalies
    - Forecast next quarter
""")
```

## Performance Optimization

### Warehouse Selection
```python
# Use appropriate warehouse size
small_queries = Database("snowflake://user:pass@account/DB?warehouse=XS_WH")
large_analytics = Database("snowflake://user:pass@account/DB?warehouse=XL_WH")

# Simple queries on small warehouse
daily_count = small_queries.ask("How many orders today?")

# Complex analytics on large warehouse  
deep_analysis = large_analytics.ask("Perform comprehensive customer analysis")
```

### Query Optimization
```python
# Leverage Snowflake's capabilities
optimized_query = db.ask("""
    Use Snowflake's window functions to calculate:
    - Running totals by month
    - Rank customers by revenue
    - Calculate moving averages
""")
```

## Security Configuration

### Role-Based Access
```python
# Connect with specific role
db = Database(
    "snowflake://analyst:pass@company/SENSITIVE_DATA/PROD",
    role="DATA_ANALYST_ROLE"
)

# ToolFront respects Snowflake's role permissions
authorized_data = db.ask("Show data I'm authorized to see")
```

### Network Policies
```python
# Connect through private link
db = Database("snowflake://user:pass@company.privatelink/DB/SCHEMA")

# With network timeout
db = Database(
    "snowflake://user:pass@company/DB/SCHEMA",
    login_timeout=30,
    network_timeout=300
)
```

### MFA Authentication
```python
# Browser-based MFA
db = Database(
    "snowflake://user@company/DB/SCHEMA",
    authenticator='externalbrowser'
)

# OAuth authentication
db = Database(
    "snowflake://user@company/DB/SCHEMA", 
    authenticator='oauth',
    token='your_oauth_token'
)
```

## Advanced Features

### Snowpark Integration
```python
# Leverage Snowpark for complex processing
snowpark_analysis = db.ask("""
    Use Snowpark to:
    - Process large datasets in Snowflake
    - Apply ML models to data
    - Perform advanced transformations
""")
```

### Semi-Structured Data
```python
# Query JSON/VARIANT columns
json_insights = db.ask("Analyze JSON event data for user behavior patterns")

# XML data processing  
xml_analysis = db.ask("Extract insights from XML transaction logs")
```

### Cross-Database Queries
```python
# Query across multiple databases
cross_db_analysis = db.ask("""
    Join data from SALES_DB and MARKETING_DB to analyze:
    - Campaign effectiveness
    - Customer journey analysis
    - Attribution modeling
""")
```

## Troubleshooting

### Connection Issues

**Account identifier problems**
```python
# Try different account formats
db = Database("snowflake://user:pass@xy12345/DB/SCHEMA")  # Legacy
db = Database("snowflake://user:pass@xy12345.us-east-1/DB/SCHEMA")  # Regional
db = Database("snowflake://user:pass@xy12345.us-east-1.azure/DB/SCHEMA")  # Cloud
```

**Authentication failures**
```bash
# Test connection with SnowSQL
snowsql -a account -u username -d database -s schema

# Check MFA settings
snowsql -a account -u username --authenticator externalbrowser
```

### Performance Issues

**Warehouse sizing**
```python
# Monitor warehouse usage
warehouse_stats = db.ask("Show warehouse utilization and costs")

# Auto-suspend configuration
db = Database(
    "snowflake://user:pass@account/DB?warehouse=AUTO_WH",
    warehouse_timeout=300  # Auto-suspend after 5 minutes
)
```

**Query optimization**
```python
# Use clustering for large tables
clustered_analysis = db.ask("Analyze data using clustered columns for better performance")

# Leverage result caching
cached_result = db.ask("Get frequently requested metrics")  # Uses cached results
```

## Cost Management

### Warehouse Auto-Scaling
```python
# Configure auto-scaling warehouse
db = Database(
    "snowflake://user:pass@account/DB",
    warehouse="AUTO_SCALE_WH",
    warehouse_size="X-Small",
    auto_suspend=60,  # Suspend after 1 minute
    auto_resume=True
)
```

### Query Cost Monitoring
```python
# Monitor query costs
cost_analysis = db.ask("Show credit usage and costs for my queries this month")

# Optimize expensive queries
optimization_tips = db.ask("Suggest optimizations for high-cost queries")
```

## Migration Examples

### From Traditional Databases
```python
# Migrate from PostgreSQL patterns
# PostgreSQL
pg_result = "SELECT DATE_TRUNC('month', order_date), SUM(amount) FROM orders GROUP BY 1"

# Snowflake equivalent using ToolFront
sf_result = db.ask("Show monthly revenue totals using Snowflake date functions")
```

### ETL Integration
```python
# Post-ETL analysis
etl_validation = db.ask("Validate data quality after ETL pipeline run")
data_lineage = db.ask("Show data freshness and lineage for key tables")
```