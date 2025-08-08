# Invoice Processing

Extract structured data from PDF invoices automatically.

## Sample Invoice

Download a sample invoice to test with:
```bash
curl -o sample-invoice.pdf https://github.com/excid3/receipts/raw/main/examples/invoice.pdf
```

## Extract Invoice Data

```python linenums="1"
from toolfront import Document
from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_number: str
    vendor_name: str
    client_name: str
    total_amount: float
    due_date: str
    line_items: list[str]

# Extract structured data from PDF
doc = Document("sample-invoice.pdf")
invoice: Invoice = doc.ask(
    "Extract all invoice information from this PDF",
    model="anthropic:claude-3-5-sonnet-latest"
)

print(f"Invoice: {invoice.invoice_number}")
print(f"From: {invoice.vendor_name}")
print(f"Amount: ${invoice.total_amount}")
print(f"Due: {invoice.due_date}")
```

## Batch Processing

Process multiple invoices in a folder:

```python linenums="21"
from pathlib import Path

def process_invoices_batch(folder_path: str):
    invoices_folder = Path(folder_path)
    results = []
    
    for pdf_file in invoices_folder.glob("*.pdf"):
        print(f"Processing {pdf_file.name}...")
        
        try:
            doc = Document(str(pdf_file))
            invoice: Invoice = doc.ask("Extract invoice data from this PDF")
            
            results.append({
                "file": pdf_file.name,
                "status": "success", 
                "data": invoice
            })
            print(f"  ✅ {invoice.vendor_name} - ${invoice.total_amount}")
            
        except Exception as e:
            results.append({
                "file": pdf_file.name,
                "status": "failed",
                "error": str(e)
            })
            print(f"  ❌ Failed: {e}")
    
    return results

# Process all PDFs in invoices/ folder
results = process_invoices_batch("invoices/")
print(f"Processed {len(results)} invoices")
```

## Export to CSV

```python linenums="49"
import csv

def export_invoices_to_csv(results, output_file="invoices.csv"):
    successful = [r for r in results if r["status"] == "success"]
    
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Invoice #", "Vendor", "Client", "Amount", "Due Date"])
        
        for result in successful:
            inv = result["data"]
            writer.writerow([
                inv.invoice_number,
                inv.vendor_name, 
                inv.client_name,
                inv.total_amount,
                inv.due_date
            ])
    
    print(f"Exported {len(successful)} invoices to {output_file}")

# Export results to CSV
export_invoices_to_csv(results)
```

!!! tip "Business Rules"
    Add validation like `total_amount: float = Field(gt=0, lt=50000)` to catch errors or flag invoices for review.