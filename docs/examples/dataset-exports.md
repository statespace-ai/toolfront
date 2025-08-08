# Dataset Exports

Export structured data with field validation using `db.Table` and Pydantic models.

```python linenums="1"
from toolfront import Database
from pydantic import BaseModel

class Customer(BaseModel):
    customer_id: int
    name: str
    email: str
    total_orders: int
    lifetime_value: float

# Connect to database
db = Database("postgresql://user:pass@host/db")

# Export only specific fields defined in the model
customers: db.Table[Customer] = db.ask(
    "Get customer data with ID, name, email, order count, and total spent"
)

print(f"Exported {len(customers)} customers")
```

!!! info "Field Selection"
    `db.Table[Model]` exports only the fields defined in your Pydantic model, reducing data transfer and ensuring consistency.

## Process Structured Data

Iterate through validated objects or convert to DataFrame:

```python linenums="17"
# Direct iteration with type safety
high_value_customers = []

for customer in customers:
    if customer.lifetime_value > 5000:
        high_value_customers.append(customer)
        print(f"{customer.name}: ${customer.lifetime_value:,.2f}")

print(f"Found {len(high_value_customers)} high-value customers")

# Or convert to DataFrame for pandas operations
df = customers.to_dataframe()
avg_ltv = df['lifetime_value'].mean()
print(f"Average customer LTV: ${avg_ltv:.2f}")
```

## Multiple Table Exports

Export different data models in one workflow:

```python linenums="30"
class Product(BaseModel):
    product_id: int
    name: str
    category: str
    units_sold: int
    revenue: float

# Export products with performance metrics
products: db.Table[Product] = db.ask(
    "Get product data with sales units and revenue by product"
)

# Export customers from specific segment
vip_customers: db.Table[Customer] = db.ask(
    "Get VIP customers with lifetime value over $10,000"
)

print(f"Products: {len(products)}")
print(f"VIP customers: {len(vip_customers)}")
```

## Export to Files

Save structured data to CSV with guaranteed field consistency:

```python linenums="47"
# Convert tables to DataFrames and save
customers_df = customers.to_dataframe()
products_df = products.to_dataframe()

customers_df.to_csv("customers.csv", index=False)
products_df.to_csv("products.csv", index=False)

# Generate summary
total_revenue = products_df['revenue'].sum()
top_category = products_df.groupby('category')['revenue'].sum().idxmax()

print(f"Exported {len(customers_df)} customers and {len(products_df)} products")
print(f"Total revenue: ${total_revenue:,.2f}")
print(f"Top category: {top_category}")
```

!!! tip "Validation Benefits"
    Pydantic automatically validates data types and can catch inconsistencies before they reach your analysis code.