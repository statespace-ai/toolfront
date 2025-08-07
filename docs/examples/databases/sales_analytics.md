# Sales Analytics

Learn how to analyze sales performance and trends using natural language queries with ToolFront.

## Overview

This example demonstrates how to extract sales insights from a PostgreSQL database containing e-commerce transactions. We'll analyze sales trends, identify top products, and calculate performance metrics.

## Setup

First, install ToolFront with PostgreSQL support and set up your environment:

```bash
pip install toolfront[postgres]
export OPENAI_API_KEY=your_api_key_here
```

!!! info "Database Schema"
    This example assumes a `sales` table with columns: `product_id`, `product_name`, `category`, `sale_date`, `quantity`, `unit_price`, and `customer_id`.

## Basic Sales Analysis

Start with simple queries to understand your sales performance:

```python linenums="1"
from toolfront import Database

# Connect to your sales database
db = Database("postgresql://user:pass@localhost:5432/ecommerce")

# Get total sales for the current month
monthly_sales: int = db.ask("What's our total revenue this month?")
print(f"This month's revenue: ${monthly_sales:,}")

# Find best-selling products
top_products: list[str] = db.ask("What are our top 5 best-selling products?")
print("Top products:", ", ".join(top_products))
```

The natural language interface automatically translates your questions into optimized SQL queries.

## Structured Sales Data

For more complex analysis, use Pydantic models to structure your data:

```python linenums="1"
from pydantic import BaseModel
from typing import List

class ProductSales(BaseModel):
    product_name: str
    category: str
    units_sold: int
    revenue: float
    growth_rate: float

# Get structured product performance data
product_performance: List[ProductSales] = db.ask(
    "Show me product performance with growth rates for top 10 products"
)

for product in product_performance:
    print(f"{product.product_name}: {product.units_sold} units, "
          f"${product.revenue:,.2f} revenue ({product.growth_rate:+.1%})")
```

!!! tip "Type Safety"
    Using Pydantic models ensures type safety and provides automatic validation of the returned data structure.

## Trend Analysis

Analyze sales trends over time periods:

```python linenums="1"
from datetime import datetime

class MonthlySales(BaseModel):
    month: str
    revenue: float
    units_sold: int
    avg_order_value: float

# Get monthly sales trends for the past year
monthly_trends: List[MonthlySales] = db.ask(
    "Show monthly sales trends for the past 12 months with average order values"
)

# Print trend analysis
print("Monthly Sales Trends:")
print("-" * 50)
for month in monthly_trends:
    print(f"{month.month}: ${month.revenue:,.2f} revenue, "
          f"{month.units_sold:,} units, ${month.avg_order_value:.2f} AOV")
```

## Business Context

Provide business context to get more relevant insights:

```python linenums="1"
# Add business context for better analysis
context = """
Our company is a B2B electronics retailer. We have seasonal patterns with higher 
sales in Q4. Our main product categories are laptops, monitors, and accessories.
We track customer segments as Enterprise, SMB, and Individual.
"""

# Get contextual analysis
seasonal_insights: str = db.ask(
    "Analyze our seasonal sales patterns and recommend inventory planning strategies",
    context=context
)

print("Seasonal Analysis:")
print(seasonal_insights)
```

!!! note "Context Benefits"
    Providing business context helps ToolFront generate more relevant and actionable insights tailored to your specific industry and use case.

## Key Takeaways

- **Natural Language**: Query your database using plain English questions
- **Structured Data**: Use Pydantic models for type-safe, structured responses
- **Business Context**: Add domain knowledge to get more relevant insights
- **Complex Analysis**: Combine multiple queries for comprehensive reporting

This approach eliminates the need to write complex SQL while maintaining the power and flexibility of direct database access.