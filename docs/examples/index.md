# Examples

Explore complete workflows and real-world use cases with ToolFront.

## Database Examples

### Basic Natural Language Queries

```python
from toolfront import Database

db = Database("postgresql://user:pass@localhost:5432/mydb")

# Simple aggregation
total_sales: int = db.ask("What's our total sales this month?")
print(f"Total sales: ${total_sales:,}")

# Complex analysis with business context
context = "Our company sells electronics. Revenue is tracked in the 'sales' table."
top_products: list[str] = db.ask("What are our top 5 performing products?", context=context)
```

### Large Dataset Export

Export large datasets efficiently without token consumption:

```python
from toolfront import Database

db = Database("postgresql://user:pass@localhost:5432/mydb")

# Export 50k+ rows with zero additional tokens
sales_data: db.Table = db.ask("Get all sales transactions from last year")

# Process the data locally
df = sales_data.to_dataframe()
print(f"Exported {len(df):,} rows")

# Export to various formats
sales_data.to_csv("sales_2023.csv")
sales_data.to_excel("sales_report.xlsx")

# Filter and analyze locally (no API calls)
high_value = df[df['amount'] > 1000]
monthly_totals = df.groupby('month')['amount'].sum()
```

### Structured Data Extraction

```python
from pydantic import BaseModel
from toolfront import Database

class Customer(BaseModel):
    name: str
    revenue: int
    growth_rate: float

db = Database("postgresql://user:pass@localhost:5432/mydb")

# Get structured customer data
top_customer: Customer = db.ask("Who's our fastest growing customer?")
print(f"Customer: {top_customer.name}, Revenue: ${top_customer.revenue:,}")

# Get multiple customers
customers: list[Customer] = db.ask("Show me our top 5 customers by revenue")
for customer in customers:
    print(f"{customer.name}: ${customer.revenue:,} ({customer.growth_rate:.1%} growth)")
```

## API Examples

### Stock Price Lookup

```python
from toolfront import API

# Connect to a financial API
api = API("https://api.example.com/openapi.json")

# Simple price lookup
price: float = api.ask("What's AAPL's current stock price?")
print(f"Apple stock price: ${price}")

# Multiple stocks
stocks: dict[str, float] = api.ask("Get current prices for AAPL, GOOGL, MSFT")
```

### Weather Data

```python
from toolfront import API
from pydantic import BaseModel

class Weather(BaseModel):
    temperature: float
    humidity: int
    description: str

api = API("https://api.weather.com/openapi.json")

weather: Weather = api.ask("What's the current weather in New York?")
print(f"NYC: {weather.temperature}°F, {weather.description}")
```

## Document Examples

### PDF Invoice Processing

Extract structured data from PDF invoices:

```python
from toolfront import Document
from pydantic import BaseModel
from typing import List

class InvoiceItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor: str
    items: List[InvoiceItem]
    total_amount: float

# Process a single invoice
doc = Document("/path/to/invoice.pdf")
invoice: Invoice = doc.ask("Extract all invoice details")

print(f"Invoice {invoice.invoice_number} from {invoice.vendor}")
print(f"Total: ${invoice.total_amount}")
for item in invoice.items:
    print(f"  {item.description}: {item.quantity} × ${item.unit_price} = ${item.total}")
```

### Batch Document Processing

Process multiple documents in a production pipeline:

```python
from toolfront import Document
from pathlib import Path
import pandas as pd

# Process all PDFs in a directory
invoice_dir = Path("/path/to/invoices/")
results = []

for pdf_file in invoice_dir.glob("*.pdf"):
    try:
        doc = Document(str(pdf_file))
        
        # Extract key information
        data: dict = doc.ask("Extract invoice number, vendor, date, and total amount")
        data['filename'] = pdf_file.name
        results.append(data)
        
        print(f"Processed: {pdf_file.name}")
        
    except Exception as e:
        print(f"Error processing {pdf_file.name}: {e}")

# Save results to CSV
df = pd.DataFrame(results)
df.to_csv("invoice_summary.csv", index=False)
print(f"Processed {len(results)} invoices")
```

### Research Paper Analysis

```python
from toolfront import Document
from pydantic import BaseModel
from typing import List

class Author(BaseModel):
    name: str
    affiliation: str

class Paper(BaseModel):
    title: str
    authors: List[Author]
    abstract: str
    key_findings: List[str]
    methodology: str

doc = Document("/path/to/research_paper.pdf")

# Extract structured paper information
paper: Paper = doc.ask("Extract all paper details including authors, methodology, and key findings")

print(f"Title: {paper.title}")
print(f"Authors: {', '.join([f'{a.name} ({a.affiliation})' for a in paper.authors])}")
print(f"Key findings: {len(paper.key_findings)} findings identified")
```

## Advanced Examples

### Multi-Source Data Analysis

Combine data from multiple sources:

```python
from toolfront import Database, API, Document

# Set up data sources
db = Database("postgresql://user:pass@localhost:5432/sales_db")
api = API("https://api.marketdata.com/openapi.json")
doc = Document("/path/to/market_report.pdf")

# Get internal sales data
internal_sales: float = db.ask("What was our Q4 revenue?")

# Get external market data
market_size: float = api.ask("What's the total market size for our industry?")

# Get analyst insights
insights: list[str] = doc.ask("What are the key market trends mentioned?")

# Combine insights
market_share = (internal_sales / market_size) * 100
print(f"Our market share: {market_share:.2f}%")
print(f"Market insights: {', '.join(insights)}")
```

### Error Handling

Robust error handling with union types:

```python
from toolfront import Database
from pydantic import BaseModel

class DatabaseError(BaseModel):
    error_type: str
    message: str
    suggestion: str

db = Database("postgresql://user:pass@localhost:5432/mydb")

# Use union types for graceful error handling
result: list[str] | DatabaseError = db.ask("Show me products that don't exist")

if isinstance(result, DatabaseError):
    print(f"Error: {result.message}")
    print(f"Suggestion: {result.suggestion}")
else:
    print(f"Found {len(result)} products")
```

## Repository Examples

For more complete examples, check out the [`examples/`](https://github.com/kruskal-labs/toolfront/tree/main/examples) directory in our repository:

- **[Basic Database Query](https://github.com/kruskal-labs/toolfront/blob/main/examples/basic.py)** - Simple natural language SQL
- **[Large Dataset Export](https://github.com/kruskal-labs/toolfront/blob/main/examples/large_dataset_export.py)** - Export 50k+ rows with zero token consumption
- **[Natural Language Demo](https://github.com/kruskal-labs/toolfront/blob/main/examples/natural_language_sqlite_demo.py)** - Complete DataFrame workflow
- **[PDF Invoice Extraction](https://github.com/kruskal-labs/toolfront/blob/main/examples/pdf_extraction.py)** - Extract structured data from documents  
- **[Complete Invoice Workflow](https://github.com/kruskal-labs/toolfront/blob/main/examples/invoice_processing_workflow.py)** - Production-ready batch processing pipeline

!!! tip "Stream Mode"
    Use `stream=True` to see real-time AI reasoning and tool execution: `data.ask("question", stream=True)`. This is helpful for debugging and understanding how ToolFront processes your queries.