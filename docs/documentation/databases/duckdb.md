# DuckDB

Configure ToolFront to connect to DuckDB in-process analytics database.

## Installation

```bash
pip install toolfront[duckdb]
```

## Connection

### File Database
```python
from toolfront import Database

# Persistent DuckDB file
db = Database("duckdb:///path/to/analytics.duckdb")

# Fast analytical queries
monthly_revenue: float = db.ask("Calculate monthly recurring revenue trends")
print(f"MRR Growth: ${monthly_revenue:,.2f}")
```

### In-Memory Database
```python
# In-memory for maximum speed
db = Database("duckdb://")

# Lightning-fast analytics
real_time_metrics = db.ask("Analyze streaming data with sub-second response")
```

## Connection Formats

```python
# Persistent file
db = Database("duckdb:///data/warehouse.duckdb")

# Relative path
db = Database("duckdb:///./analytics.duckdb")

# In-memory (fastest)
db = Database("duckdb://")

# Read-only mode
db = Database("duckdb:///data.duckdb?access_mode=READ_ONLY")
```

## Key Advantages

- **Columnar storage** optimized for analytics
- **Vectorized execution** for maximum performance  
- **Zero-dependency** embedded database
- **SQL compatibility** with PostgreSQL syntax
- **Parallel processing** on multi-core systems
- **Direct file reading** (Parquet, CSV, JSON)

## Real-World Examples

### Data Science Workflows
```python
from pydantic import BaseModel
from typing import List

class DataScienceMetrics(BaseModel):
    dataset_size_gb: float
    processing_time_ms: float
    memory_usage_mb: float
    query_performance_score: float
    feature_count: int

# Analytics-optimized database
db = Database("duckdb:///ml_pipeline.duckdb")

# High-performance data science queries
metrics: DataScienceMetrics = db.ask("Analyze ML pipeline performance and data quality")

print(f"Dataset: {metrics.dataset_size_gb:.1f}GB in {metrics.processing_time_ms}ms")
```

### Business Intelligence
```python
# BI dashboard backend
bi_db = Database("duckdb:///business_intelligence.duckdb")

# Fast dashboard queries
sales_dashboard = bi_db.ask("Generate real-time sales dashboard metrics")
customer_insights = bi_db.ask("Perform customer segmentation analysis")
financial_kpis = bi_db.ask("Calculate key financial performance indicators")
```

### Log Analysis
```python
# Log analytics database
logs_db = Database("duckdb:///application_logs.duckdb")

# High-speed log processing
error_patterns = logs_db.ask("Identify error patterns and anomalies in application logs")
performance_metrics = logs_db.ask("Analyze application performance from log data")
security_alerts = logs_db.ask("Detect security threats from access logs")
```

## DuckDB-Specific Features

### Direct File Querying
```python
# Query files directly without importing
file_analysis = db.ask("""
    Query external files directly:
    - SELECT * FROM 'data.parquet'
    - SELECT * FROM 'logs.csv'
    - SELECT * FROM 'events.json'
""")
```

### Vectorized Operations
```python
# Leverage vectorized execution
vector_analysis = db.ask("""
    Use DuckDB's vectorized processing:
    - Complex aggregations on millions of rows
    - Window functions with high performance
    - Statistical functions and analytics
""")
```

### Advanced Analytics Functions
```python
# Built-in analytics capabilities
analytics_query = db.ask("""
    Use DuckDB's advanced analytics:
    - Percentile calculations
    - Moving averages and trends
    - Statistical distributions
    - Time series analysis
""")
```

### Array and List Processing
```python
# Native array support
array_analysis = db.ask("""
    Process arrays and lists efficiently:
    - Array aggregations and transformations
    - List operations and filtering
    - Nested data structure analysis
""")
```

## Performance Optimization

### Memory Configuration
```python
# Optimize memory settings
db = Database(
    "duckdb:///analytics.duckdb",
    memory_limit="8GB",
    threads=8
)
```

### Parallel Processing
```python
# Multi-threaded analytics
parallel_analysis = db.ask("""
    Leverage parallel processing:
    - Multi-core aggregations
    - Parallel joins and sorts
    - Concurrent query execution
""")
```

### Large Dataset Handling
```python
# Efficient large data processing
large_analysis: db.Table = db.ask("Process billion-row dataset efficiently")

# Local processing without API overhead
df = large_analysis.to_dataframe()
print(f"Processed {len(df):,} rows locally")

# Export optimized formats
large_analysis.to_parquet("optimized_results.parquet", compression="snappy")
```

## Data Import Patterns

### Bulk Data Loading
```python
# High-speed data ingestion
bulk_import = db.ask("""
    Import large datasets efficiently:
    - COPY FROM 'large_file.csv' WITH PARALLEL=TRUE
    - INSERT INTO table SELECT * FROM 'data.parquet'
    - Batch processing with optimal chunk sizes
""")
```

### Real-Time Streaming
```python
# Streaming data integration
streaming_db = Database("duckdb://")  # In-memory for speed

# Process streaming data
stream_analysis = streaming_db.ask("""
    Handle streaming data efficiently:
    - Real-time aggregations
    - Sliding window calculations
    - Event-driven analytics
""")
```

## Integration with Data Ecosystem

### Pandas Integration
```python
# Seamless pandas workflow
pandas_analysis = db.ask("Export analysis results for pandas processing")

# Convert to DataFrame for ML pipelines
df = pandas_analysis.to_dataframe()

# Continue with scikit-learn, matplotlib, etc.
```

### Apache Arrow Integration
```python
# Arrow-native processing
arrow_analysis = db.ask("""
    Leverage Apache Arrow integration:
    - Zero-copy data transfers
    - Columnar memory format
    - Cross-language compatibility
""")
```

### Cloud Storage Integration
```python
# Query cloud storage directly
cloud_analysis = db.ask("""
    Query cloud data sources:
    - S3: SELECT * FROM 's3://bucket/data.parquet'
    - HTTP: SELECT * FROM 'https://api.com/data.csv'
    - Remote databases via federation
""")
```

## Analytics Use Cases

### Time Series Analysis
```python
# Time series optimized queries
timeseries_db = Database("duckdb:///timeseries.duckdb")

time_analysis = timeseries_db.ask("""
    Perform time series analytics:
    - Seasonal decomposition
    - Trend analysis and forecasting
    - Anomaly detection in time data
    - Moving averages and smoothing
""")
```

### Geospatial Analytics
```python
# Geospatial data processing
geo_db = Database("duckdb:///geospatial.duckdb")

# Load spatial extension
spatial_analysis = geo_db.ask("""
    Use spatial functions:
    - Geographic distance calculations
    - Spatial joins and intersections
    - Coordinate system transformations
""")
```

### Financial Analytics
```python
# Financial modeling database
finance_db = Database("duckdb:///financial_models.duckdb")

financial_analysis = finance_db.ask("""
    Perform financial analytics:
    - Risk calculations and VaR
    - Portfolio optimization metrics
    - Options pricing models
    - Market volatility analysis
""")
```

## Development and Testing

### Rapid Prototyping
```python
# Quick prototype database
prototype_db = Database("duckdb://")

# Fast iteration cycles
prototype_results = prototype_db.ask("Test analytical hypotheses quickly")
```

### A/B Testing Analytics
```python
# A/B test analysis
ab_test_db = Database("duckdb:///ab_tests.duckdb")

test_results = ab_test_db.ask("""
    Analyze A/B test results:
    - Statistical significance testing
    - Conversion rate analysis
    - Cohort performance comparison
""")
```

### Data Quality Assessment
```python
# Data quality monitoring
quality_db = Database("duckdb:///data_quality.duckdb")

quality_metrics = quality_db.ask("""
    Assess data quality:
    - Completeness and accuracy metrics
    - Duplicate detection and analysis
    - Data distribution profiling
    - Outlier identification
""")
```

## Performance Benchmarking

### Query Performance
```python
# Performance testing
perf_analysis = db.ask("""
    Benchmark query performance:
    - Execution time analysis
    - Memory usage optimization
    - CPU utilization patterns
    - I/O efficiency metrics
""")
```

### Scalability Testing
```python
# Scale testing
scale_test = db.ask("""
    Test scalability limits:
    - Dataset size performance curves
    - Memory scaling characteristics
    - Multi-threading efficiency
    - Parallel processing benefits
""")
```

## Advanced Configuration

### Custom Settings
```python
# Advanced DuckDB configuration
advanced_db = Database(
    "duckdb:///advanced.duckdb",
    config={
        'default_order': 'ASC',
        'enable_progress_bar': True,
        'enable_profiling': 'json',
        'temp_directory': '/tmp/duckdb'
    }
)
```

### Extension Loading
```python
# Load DuckDB extensions
extension_analysis = db.ask("""
    Use DuckDB extensions:
    - INSTALL httpfs; LOAD httpfs; (for remote files)
    - INSTALL spatial; LOAD spatial; (for GIS)
    - INSTALL json; LOAD json; (for JSON processing)
""")
```

## Troubleshooting

### Memory Issues
```python
# Memory optimization
memory_analysis = db.ask("""
    Optimize memory usage:
    - Analyze memory consumption patterns
    - Implement streaming processing
    - Use memory-mapped files
    - Configure memory limits appropriately
""")
```

### Performance Debugging
```python
# Performance diagnostics
debug_analysis = db.ask("""
    Debug performance issues:
    - Query plan analysis
    - Execution profiling
    - Bottleneck identification
    - Optimization recommendations
""")
```

### Data Type Issues
```python
# Type handling
type_analysis = db.ask("""
    Handle data type challenges:
    - Automatic type inference
    - Type conversion optimization
    - Schema evolution support
    - NULL handling strategies
""")
```

## Best Practices

### Optimal Query Patterns
```python
# Efficient query design
optimized_queries = db.ask("""
    Design efficient queries:
    - Use columnar access patterns
    - Minimize data movement
    - Leverage vectorized operations
    - Optimize join orders
""")
```

### Data Organization
```python
# Optimal data layout
data_organization = db.ask("""
    Organize data for performance:
    - Partition by frequently filtered columns
    - Sort by commonly used columns
    - Use appropriate compression
    - Minimize schema changes
""")
```