# Raw Dataframes

Export massive datasets without LLM token costs using DataFrame type hints.

```python linenums="1"
import pandas as pd
from toolfront import Database

# Connect to your database
db = Database("postgresql://user:pass@host/db")

# DataFrame type hint = zero token export
sales_data: pd.DataFrame = db.ask("Get all sales data from 2024")

print(f"Exported {len(sales_data):,} rows")
print(f"Columns: {list(sales_data.columns)}")
```

!!! info "How it Works"
    With `pd.DataFrame` type hints, the LLM only generates the SQL query. The actual data flows directly from database to pandas without consuming tokens.

## Data Analysis

Analyze exported data with standard pandas operations:

```python linenums="9"
# Basic statistics
total_revenue = sales_data['amount'].sum()
avg_order = sales_data['amount'].mean()

print(f"Total revenue: ${total_revenue:,.2f}")
print(f"Average order: ${avg_order:.2f}")

# Group by analysis
monthly_sales = (sales_data
                 .groupby(sales_data['date'].dt.month)['amount']
                 .sum()
                 .head())

top_customers = (sales_data
                 .groupby('customer_name')['amount']
                 .sum()
                 .sort_values(ascending=False)
                 .head(5))

print("Monthly sales:", monthly_sales.to_dict())
print("Top customers:", top_customers.to_dict())
```

## Export Data

Save to multiple formats:

```python linenums="27"
# Save to CSV  
sales_data.to_csv("sales_2024.csv", index=False)

# Save to Excel (requires openpyxl)
sales_data.to_excel("sales_2024.xlsx", index=False)

# Save to Parquet (most efficient, requires pyarrow)
sales_data.to_parquet("sales_2024.parquet")

print("Data exported to CSV, Excel, and Parquet formats")
```

## Memory Management

For huge datasets, process in chunks:

```python linenums="37"
def export_in_chunks(chunk_size=100000):
    # Get total count first
    total_rows: int = db.ask("How many sales records do we have?")
    chunks_needed = (total_rows // chunk_size) + 1
    
    print(f"Processing {total_rows:,} rows in {chunks_needed} chunks")
    
    all_data = []
    for i in range(chunks_needed):
        offset = i * chunk_size
        
        chunk: pd.DataFrame = db.ask(
            f"Get sales data LIMIT {chunk_size} OFFSET {offset}"
        )
        
        if len(chunk) == 0:
            break
            
        all_data.append(chunk)
        print(f"Processed chunk {i+1}: {len(chunk):,} rows")
    
    # Combine all chunks
    final_df = pd.concat(all_data, ignore_index=True)
    return final_df

# Use for very large exports
large_dataset = export_in_chunks()
```

!!! tip "Performance"
    DataFrame exports can handle millions of rows efficiently. Only the SQL generation uses tokens - the data transfer is direct.