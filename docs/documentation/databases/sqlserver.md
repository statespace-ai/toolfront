# SQL Server

Configure ToolFront to connect to Microsoft SQL Server databases.

## Installation

```bash
pip install toolfront[sqlserver]
```

## Connection

### Basic Connection
```python
from toolfront import Database

db = Database("mssql://user:password@server:1433/database")

# Query your SQL Server database
revenue: float = db.ask("What's our total quarterly revenue?")
print(f"Q4 Revenue: ${revenue:,.2f}")
```

### Connection String Format
```
mssql://[user[:password]@][host][:port][/database][?param1=value1&...]
```

### Examples
```python
# Local SQL Server with Windows Auth
db = Database("mssql://server/database?trusted_connection=yes")

# Named instance
db = Database("mssql://user:pass@server\\SQLEXPRESS:1433/database")

# Azure SQL Database
db = Database("mssql://user@server:pass@server.database.windows.net:1433/database")

# With encryption
db = Database("mssql://user:pass@server:1433/db?encrypt=true&TrustServerCertificate=true")
```

## Real-World Examples

### Enterprise Resource Planning
```python
from pydantic import BaseModel
from typing import List, Optional

class ERPMetrics(BaseModel):
    total_orders: int
    pending_shipments: int
    inventory_value: float
    top_customers: List[str]
    supply_chain_alerts: List[str]

db = Database("mssql://erp_user:pass@erp-sql:1433/ERP_Production")

# Comprehensive ERP analysis
metrics: ERPMetrics = db.ask("Analyze current ERP system performance and metrics")

print(f"Total Orders: {metrics.total_orders:,}")
print(f"Inventory Value: ${metrics.inventory_value:,.2f}")
```

### Financial Reporting
```python
# Financial database connection
db = Database("mssql://finance:pass@finance-sql:1433/FinancialReporting")

# Financial analysis
quarterly_report = db.ask("Generate comprehensive quarterly financial report")
cash_flow = db.ask("Analyze cash flow trends and projections")
budget_variance = db.ask("Calculate budget vs actual variance analysis")
```

### Data Warehouse Analytics
```python
# Data warehouse connection
dw_db = Database("mssql://analyst:pass@dw-sql:1433/DataWarehouse")

# Business intelligence queries
sales_trends = dw_db.ask("Analyze sales trends across all business units")
customer_segments = dw_db.ask("Perform customer segmentation analysis")
market_analysis = dw_db.ask("Generate market performance insights")
```

## SQL Server-Specific Features

### T-SQL Functions
```python
# Leverage T-SQL capabilities
tsql_analysis = db.ask("""
    Use T-SQL specific functions:
    - Window functions for analytics
    - Common table expressions (CTEs)
    - PIVOT and UNPIVOT operations
    - Advanced date/time functions
""")
```

### Columnstore Indexes
```python
# Columnstore performance
columnstore_query = db.ask("""
    Query columnstore tables for:
    - Fast aggregation performance
    - Compression benefits analysis
    - Batch mode execution
""")
```

### Always Encrypted Data
```python
# Query encrypted columns
encrypted_analysis = db.ask("""
    Analyze Always Encrypted data:
    - Deterministic encryption queries
    - Randomized encryption handling
    - Key management insights
""")
```

## Performance Optimization

### Connection Pooling
```python
# Optimized connection settings
db = Database(
    "mssql://user:pass@server:1433/database",
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    pool_recycle=3600
)
```

### Query Performance
```python
# Performance optimization
optimized_queries = db.ask("""
    Optimize SQL Server queries using:
    - Proper indexing strategies
    - Query plan analysis
    - Statistics optimization
    - Parameter sniffing solutions
""")
```

### Large Dataset Processing
```python
# Efficient large data handling
large_dataset: db.Table = db.ask("Export all customer transaction history")

# Process locally without additional API calls
df = large_dataset.to_dataframe()
print(f"Processing {len(df):,} records locally")

# Export for analysis
large_dataset.to_parquet("transactions.parquet")
```

## Azure SQL Database

### Azure-Specific Connection
```python
# Azure SQL Database
azure_db = Database(
    "mssql://username@servername:password@servername.database.windows.net:1433/database",
    driver="ODBC Driver 18 for SQL Server"
)

# Azure-specific features
azure_analysis = azure_db.ask("""
    Leverage Azure SQL features:
    - Elastic pool metrics
    - DTU consumption analysis
    - Geo-replication status
    - Automatic tuning recommendations
""")
```

### Managed Instance
```python
# Azure SQL Managed Instance
managed_db = Database("mssql://user:pass@managed-instance.sql.azuresynapse.net:1433/database")

managed_insights = managed_db.ask("Analyze managed instance performance and scaling")
```

## Security and Compliance

### Row-Level Security
```python
# RLS-enabled queries
security_analysis = db.ask("""
    Query with row-level security:
    - User-specific data access
    - Security policy compliance
    - Data isolation verification
""")
```

### Dynamic Data Masking
```python
# Masked data analysis
masked_query = db.ask("""
    Analyze masked sensitive data:
    - Email masking patterns
    - Credit card number protection
    - PII compliance reporting
""")
```

### SQL Server Authentication
```python
# Windows Authentication
windows_auth_db = Database("mssql://server/database?trusted_connection=yes")

# Mixed mode authentication
mixed_auth_db = Database("mssql://sql_user:pass@server:1433/database")
```

## High Availability

### Always On Availability Groups
```python
# Primary replica connection
primary_db = Database("mssql://user:pass@primary-sql:1433/database")

# Secondary replica for read-only queries
secondary_db = Database("mssql://user:pass@secondary-sql:1433/database")

# Analytics on secondary replica
readonly_analysis = secondary_db.ask("Perform resource-intensive analytical queries")
```

### Failover Clustering
```python
# Cluster-aware connection
cluster_db = Database("mssql://user:pass@sql-cluster:1433/database")

cluster_health = cluster_db.ask("Monitor failover cluster health and performance")
```

## Monitoring and Diagnostics

### Performance Monitoring
```python
# Performance insights
performance_data = db.ask("""
    Monitor SQL Server performance:
    - Wait statistics analysis
    - Resource utilization metrics  
    - Query execution plans
    - Index usage statistics
""")
```

### System Health
```python
# System diagnostics
health_check = db.ask("""
    Perform system health analysis:
    - Database file growth
    - Transaction log usage
    - Backup status verification
    - Error log analysis
""")
```

## Integration Patterns

### ETL Processing
```python
# ETL workflow analysis
etl_metrics = db.ask("""
    Analyze ETL processes:
    - Data pipeline performance
    - Transformation efficiency
    - Load operation metrics
    - Data quality assessment
""")
```

### Reporting Services
```python
# SSRS integration analysis
reporting_data = db.ask("""
    Analyze reporting data:
    - Report execution statistics
    - Data source performance
    - User access patterns
""")
```

## Troubleshooting

### Connection Issues
```bash
# Test SQL Server connectivity
sqlcmd -S server -U user -P password -d database

# Check SQL Server services
services.msc

# Test network connectivity  
telnet server 1433
```

### Performance Issues
```python
# Query performance analysis
perf_analysis = db.ask("""
    Diagnose performance issues:
    - Blocking and deadlock analysis
    - Resource bottleneck identification
    - Index fragmentation assessment
    - Statistics update recommendations
""")
```

### Memory and Storage
```python
# Resource utilization
resource_analysis = db.ask("""
    Analyze resource usage:
    - Memory allocation patterns
    - Storage I/O performance
    - CPU utilization trends
    - Connection pool efficiency
""")
```

## Migration Support

### Legacy System Migration
```python
# Migration assessment
migration_analysis = db.ask("""
    Assess migration readiness:
    - Data type compatibility
    - Feature parity analysis
    - Performance comparison
    - Migration effort estimation
""")
```

### Version Upgrade Analysis
```python
# Upgrade compatibility
upgrade_assessment = db.ask("""
    Analyze upgrade considerations:
    - Deprecated feature usage
    - Compatibility level impact
    - Performance improvements
    - Security enhancements
""")
```