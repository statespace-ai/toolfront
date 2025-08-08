# Basic Database Queries

Get structured data from your database with natural language queries.

```python linenums="1"
from toolfront import Database

# Connect to your database
db = Database("postgresql://user:pass@host/db")

# Simple string response (no type hint)
summary = db.ask("Summarize our sales performance this quarter")
print(summary)
# "Q3 sales reached $2.4M with 1,247 orders, up 15% from last quarter"
```

## Structured Responses

Add type hints to get exactly the data format you need:

```python linenums="8"
# Single values
total_revenue: int = db.ask("What's our total revenue this year?")
avg_order_value: float = db.ask("What's our average order value?")

print(f"Revenue: ${total_revenue:,}")
print(f"Average order: ${avg_order_value:.2f}")

# Lists and dictionaries  
top_products: list[str] = db.ask("What are our top 5 products?")
sales_by_region: dict[str, int] = db.ask("Show sales by region")

print("Top products:", top_products)
print("Regional sales:", sales_by_region)
```

## Boolean and Optional Results

```python linenums="20"
# Boolean responses
has_inventory: bool = db.ask("Do we have any products out of stock?")

# Handle missing data
last_order: str | None = db.ask("When was our most recent order?")

if last_order:
    print(f"Last order: {last_order}")
else:
    print("No orders found")
```

!!! tip "Pro Tip"
    Type hints work with any Python type: `int`, `float`, `str`, `bool`, `list`, `dict`, `set`, and even custom Pydantic models.