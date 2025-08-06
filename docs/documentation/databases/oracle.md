# Oracle Database

Configure ToolFront to connect to Oracle Database.

## Installation

```bash
pip install toolfront[oracle]
```

## Connection

```python
from toolfront import Database

db = Database("oracle://user:password@host:1521/service")

# Enterprise database queries
financial_summary: dict = db.ask("Generate monthly financial summary")
print(f"Financial data: {financial_summary}")
```

## Connection Formats

```python
# With service name
db = Database("oracle://hr_user:pass@oracle.company.com:1521/PROD")

# With SID
db = Database("oracle://user:pass@host:1521", sid="ORCL")

# With TNS
db = Database("oracle://user:pass@", dsn="your_tns_entry")
```

## Enterprise Features

```python
# Complex financial queries
financial_analysis = db.ask("Perform complex financial calculations and reporting")

# Data warehouse analytics
warehouse_insights = db.ask("Analyze enterprise data warehouse metrics")

# Compliance reporting
compliance_report = db.ask("Generate compliance and audit reports")
```

## Best Use Cases

- **Enterprise applications**
- **Financial systems**
- **Data warehousing**
- **Compliance reporting**
- **High-volume OLTP**

```python
# Enterprise analytics
enterprise_metrics = db.ask("Calculate enterprise KPIs and performance metrics")

# Regulatory compliance
compliance_data = db.ask("Generate regulatory compliance reports")
```