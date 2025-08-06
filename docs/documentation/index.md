# Concepts

Learn the core concepts behind ToolFront's AI-powered data retrieval system.

## Overview

ToolFront simplifies data access by providing a unified interface for querying databases, APIs, and documents using natural language. The system is built around three main concepts:

## Core Concepts

### [Data Sources](datasources.md)
**Connect to your data wherever it lives**

ToolFront supports three types of data sources:

- **Databases** - SQL databases like PostgreSQL, MySQL, Snowflake, BigQuery, and more
- **APIs** - REST APIs with OpenAPI/Swagger specifications  
- **Documents** - PDF, Word, Excel, and other document formats

Each data source provides a consistent `ask()` interface while handling the complexities of connection, authentication, and data retrieval behind the scenes.

### [Asking](asking.md)  
**Natural language queries that understand your intent**

The `ask()` method is the heart of ToolFront. It takes your natural language question and:

- Understands the intent and context
- Generates appropriate queries/requests for your data source
- Executes the operations safely and efficiently
- Returns results in the format you specify

### [Structured Outputs](structured_outputs.md)
**Control response formats with Python type hints**

ToolFront uses Python type annotations to automatically structure responses:

- **Primitive types** (`str`, `int`, `float`, `bool`) for simple values
- **Pydantic models** for complex, validated data structures  
- **Collections** (`list`, `dict`, `set`) for multiple items
- **DataFrames** for raw data exports that bypass token limits

## How It All Works Together

```python
from toolfront import Database
from pydantic import BaseModel

# 1. Data Source: Connect to your database
db = Database("postgresql://user:pass@host:port/database")

# 2. Structured Output: Define your desired format
class Product(BaseModel):
    name: str
    revenue: float
    category: str

# 3. Asking: Query with natural language
top_products: list[Product] = db.ask("What are our top 5 products by revenue?")

# Result: Structured, validated data ready to use
for product in top_products:
    print(f"{product.name}: ${product.revenue:,.2f} ({product.category})")
```

## Key Benefits

- **Unified Interface**: Same `ask()` method works across all data sources
- **Type Safety**: Pydantic validation ensures data integrity
- **Natural Language**: No need to learn SQL, API endpoints, or document parsing
- **Efficient**: Smart caching and optimization reduce costs and latency
- **Secure**: Read-only operations and local execution protect your data

## Next Steps

- **[Data Sources](datasources.md)** - Learn how to connect to databases, APIs, and documents
- **[Asking](asking.md)** - Master natural language querying techniques
- **[Structured Outputs](structured_outputs.md)** - Control response formats with type hints