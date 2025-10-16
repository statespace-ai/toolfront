# Python SDK

ToolFront SDK comes with a simple `Environment` class to launch AI agents on your environments. 

---

## Basic Usage

Ask questions and an AI agent will browse your environment to find answers.

```python
from toolfront import Environment

environment = Environment(url="file:///path/toolsite")

result = environment.run(prompt="What's our total revenue this quarter?", 
                        model="openai:gpt-5")
# Returns: "Total revenue for Q4 2024 is $2.4M"
```

---

## Structured Output

Use `output_type` to get back structured data in any format you need.

=== ":fontawesome-solid-cube:{ .middle } &nbsp; Scalars"

    ```python
    from toolfront import Environment

    environment = Environment(url="file:///path/toolsite")

    avg_price = environment.run(
        prompt="What's our average ticket price?",
        model="openai:gpt-5",
        output_type=float
    )
    # Returns: 29.99

    has_inventory = environment.run(
        prompt="Do we have any monitors in stock?",
        model="openai:gpt-5",
        output_type=bool
    )
    # Returns: True
    ```

=== ":fontawesome-solid-layer-group:{ .middle } &nbsp; Collections"

    ```python
    from toolfront import Environment

    environment = Environment(url="file:///path/toolsite")

    product_names = environment.run(
        "What products do we sell?",
        model="openai:gpt-5",
        output_type=list[str]
    )
    # Returns: ["Laptop Pro", "Wireless Mouse", "USB Cable"]

    sales_by_region = environment.run(
        "Sales by region",
        model="openai:gpt-5",
        output_type=dict[str, int]
    )
    # Returns: {"North": 45000, "South": 38000, "East": 52000}
    ```

=== ":fontawesome-solid-chain:{ .middle } &nbsp; Unions"

    ```python
    from toolfront import Environment

    environment = Environment(url="file:///path/toolsite")

    result = environment.run(
        "Best-sellers this month?",
        model="openai:gpt-5",
        output_type=str | list[str]
    )
    # Returns: ["Product A", "Product B"] or "No data found"

    error = environment.run(
        "What was the error message?",
        model="openai:gpt-5",
        output_type=str | None
    )
    # Returns: "Connection timeout" or None
    ```

=== ":fontawesome-solid-sitemap:{ .middle } &nbsp; Objects"

    ```python
    from toolfront import Environment
    from pydantic import BaseModel, Field

    environment = Environment(url="file:///path/toolsite")

    class Product(BaseModel):
        name: str = Field(description="Product name")
        price: float = Field(description="Product price in USD")
        in_stock: bool = Field(description="Whether product is in stock")


    product = environment.run(
        "What's our best-selling product?",
        model="openai:gpt-5",
        output_type=Product
    )
    # Returns: Product(name="Blue Headphones", price=300.0, in_stock=True)
    ```

=== ":fontawesome-solid-percent:{ .middle } &nbsp; Functions"

    ```python
    from toolfront import Environment

    environment = Environment(url="file:///path/toolsite")

    def my_func(price: float, quantity: int):
        """
        Returns a product's revenue of based on price and quantity sold
        """
        return price * quantity

    # Returns the output of the provided function
    product = environment.run(
        "Compute the revenue of our best-seller",
        model="openai:gpt-5",
        output_type=my_func
    )
    # Returns: 127.000
    ```

---

## Environment Variables

Markdown pages may reference environment variables for authentication or configuration:

``` hl_lines="3-4"
---
tools:
  - [curl, -X, GET, "https://api.com/data", -H, "Authorization: Bearer $TOKEN"]
  - [curl, -X, POST, "https://api.com/submit", -H, "X-API-Key: $API_KEY"]
---

# My Markdown page
...
```

You must pass these variables to the Environment using the `env` parameter:

```python
from toolfront import Environment

environment = Environment(
    url="file:///path/toolsite",
    env={"TOKEN": "token123", "API_KEY": "key456"}
)

result = environment.run("Fetch latest data", model="openai:gpt-5")
```

!!! warning "Working with Secrets"
    Environment variables are never exposed to AI agents.

---

## Verbose Mode

Enable verbose mode to see live AI reasoning and tool calls during execution:

```python
from toolfront import Environment

environment = Environment(url="file:///path/toolsite")

result = environment.run(
    "What's our total revenue this quarter?",
    model="openai:gpt-5",
    verbose=True
)
```

---

::: toolfront.environment.Environment.run
    options:
      show_root_heading: true
      show_source: true