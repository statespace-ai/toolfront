# Structured Outputs

ToolFront uses Python type annotations to automatically structure responses, export data, and handle errors. `ask()` will always return the exact output type you specify.


## Output Types

ToolFront supports all standard Python types and Pydantic models for structured data.

=== ":fontawesome-solid-cube:{ .middle } &nbsp; Primitives"

    Use Python's built-in types for simple values:

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    total_orders: int = db.ask("How many orders do we have?")
    # Returns: 1250

    avg_price: float = db.ask("What's our average product price?")
    # Returns: 29.99

    best_product: str = db.ask("What's our best-selling product?")
    # Returns: "Wireless Headphones Pro"

    has_inventory: bool = db.ask("Do we have any products in stock?")
    # Returns True
    ```

=== ":fontawesome-solid-layer-group:{ .middle } &nbsp; Collections"

    Use Python collections for multiple items:

    ```python linenums="1"
    from toolfront import API

    db = API("https://api.com/openapi.json")

    # Lists
    product_names: list[str] = db.ask("What products do we sell?")
    # Returns: ["Laptop Pro", "Wireless Mouse", "USB Cable"]

    # Dictionaries  
    sales_by_region: dict[str, int] = db.ask("Sales by region")
    # Returns: {"North": 45000, "South": 38000, "East": 52000}

    # Sets (unique values)
    active_regions: set[str] = db.ask("Which regions have sales?")
    # Returns: {"North America", "Europe", "Asia Pacific"}
    ```

=== ":fontawesome-solid-chain:{ .middle } &nbsp; Union Types"

    Handle multiple possible outcomes:

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    price: int | float = db.ask("Price of product XYZ?")
    # Returns: 29.99, 30

    result: str | list[str] = db.ask("Best-sellers this month?")
    # Returns: ["Product A", "Product B"] or "No data found"

    error: str | None = db.ask("What was the error message?")
    # Returns: "Connection timeout" or None

    status: bool | str = db.ask("Is the system healthy?")
    # Returns: True or "Database connection failed"
    ```

=== ":fontawesome-solid-sitemap:{ .middle } &nbsp; Pydantic Objects"

    For complex, structured data:

    ```python linenums="1"
    from toolfront import Document
    from pydantic import BaseModel, Field
    from typing import List

    db = Document("path/to/document.pdf")

    class Product(BaseModel):
        name: str = Field(..., description="Product name") # (1)
        price: float | int = Field(..., description="Product price in USD")
        in_stock: bool = Field(..., description="Product is in stock")

    products: List[Product] = db.ask("Rank our products by price")
    # Returns: [Product(name="Wireless Headphones", price=300, in_stock=True),
    #           Product(name="Laptop Pro", price=1299.0, in_stock=False),
    #           ...]
    ```
    
    1. Adding a Pydantic Field  description helps ToolFront extract data more accurately.

!!! tip
    All of ToolFront's data sources (databases, APIs, and documents) support output typed outputs.


## Table Exports

Use `Table` types to export large datasets without consuming LLM tokens. The database output is routed directly, bypassing the LLM entirely.

=== ":fontawesome-solid-table:{ .middle } &nbsp; Raw Tables"

    Export data as raw DataFrame:

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    # Export 50,000+ rows with zero tokens
    sales_data: db.Table = db.ask("Get all sales from 2024")

    # Process locally
    df = sales_data.to_dataframe()
    print(f"Retrieved {len(df):,} rows")

    # Export formats
    sales_data.to_csv("sales_2024.csv")
    sales_data.to_excel("report.xlsx")
    print(sales_data.columns)
    ```

=== ":fontawesome-solid-sitemap:{ .middle } &nbsp; Structured Tables"

    Export with Pydantic validation per row:

    ```python linenums="1"
    from toolfront import Database
    from pydantic import BaseModel

    db = Database("postgresql://user:pass@host/db")

    class Sale(BaseModel):
        customer_name: str
        amount: float
        date: str

    # Each row becomes a Sale object
    sales_data: db.Table[Sale] = db.ask("Get Q4 sales")

    for sale in sales_data:
        print(f"{sale.customer_name}: ${sale.amount}")
    ```


!!! note
    Table exports are currently supported for databases only.

## Error Handling

Handle failures and edge cases by including error strings in union types or using structured error models.

=== ":fontawesome-solid-exclamation-triangle:{ .middle } &nbsp; String Errors"

    Include error strings in union types:

    ```python linenums="1"
    from toolfront import Database

    db = Database("postgresql://user:pass@host/db")

    # Success returns data, failure returns error string
    result: list[dict] | str = db.ask("Complex query that might fail")
    # Returns: [{"id": 1, "name": "John"}] or "Error: table not found"

    # Boolean or error string
    status: bool | str = db.ask("Is the system healthy?")
    # Returns: True or "Database connection failed"

    if isinstance(result, str):
        print(f"Error: {result}")
    else:
        print(f"Found {len(result)} records")
    ```

=== ":fontawesome-solid-cog:{ .middle } &nbsp; Custom Error Models"

    Create structured error responses:

    ```python linenums="1"
    from toolfront import Database
    from pydantic import BaseModel

    db = Database("postgresql://user:pass@host/db")

    class DatabaseError(BaseModel):
        error_type: str
        message: str
        suggestion: str

    # Handle both success and error cases
    result: list[dict] | DatabaseError = db.ask("Complex query")

    if isinstance(result, DatabaseError):
        print(f"Error: {result.message}")
        print(f"Suggestion: {result.suggestion}")
    ```

=== ":fontawesome-solid-shield-alt:{ .middle } &nbsp; Data Validation"

    Automatically validate responses with Pydantic:

    ```python linenums="1"
    from toolfront import Database
    from pydantic import BaseModel, Field, validator

    db = Database("postgresql://user:pass@host/db")

    class Customer(BaseModel):
        name: str = Field(..., min_length=1)
        email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
        age: int = Field(..., ge=0, le=120)
        
        @validator('email')
        def validate_email(cls, v):
            return v.lower()

    customers: list[Customer] = db.ask("Get all customers")
    ```