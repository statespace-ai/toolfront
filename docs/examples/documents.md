# Document Examples

Examples for processing and extracting information from various document formats.

## PDF Invoice Processing

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

# Process invoice
doc = Document("/path/to/invoice.pdf")
invoice: Invoice = doc.ask("Extract all invoice details")

print(f"Invoice {invoice.invoice_number} from {invoice.vendor}: ${invoice.total_amount}")
```

## Research Paper Analysis

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

doc = Document("/path/to/research_paper.pdf")
paper: Paper = doc.ask("Extract paper metadata and key findings")

print(f"Title: {paper.title}")
print(f"Authors: {', '.join([a.name for a in paper.authors])}")
```

## Financial Report Processing

```python
from toolfront import Document

doc = Document("/path/to/quarterly_report.pdf")

# Extract financial metrics
revenue: float = doc.ask("What was the total revenue?")
profit_margin: float = doc.ask("What's the profit margin percentage?")
key_risks: list[str] = doc.ask("What are the main business risks mentioned?")

print(f"Revenue: ${revenue:,.2f}")
print(f"Profit Margin: {profit_margin:.1%}")
```

## Contract Analysis

```python
from toolfront import Document
from pydantic import BaseModel
from datetime import date

class Contract(BaseModel):
    parties: list[str]
    start_date: date
    end_date: date
    value: float
    key_terms: list[str]

doc = Document("/path/to/contract.pdf")
contract: Contract = doc.ask("Extract contract details")

print(f"Contract between: {', '.join(contract.parties)}")
print(f"Duration: {contract.start_date} to {contract.end_date}")
print(f"Value: ${contract.value:,.2f}")
```

## Excel Spreadsheet Processing

```python
from toolfront import Document

doc = Document("/path/to/sales_data.xlsx")

# Extract data insights
total_sales: float = doc.ask("What are the total sales?")
top_regions: list[str] = doc.ask("Which regions have the highest sales?")
monthly_trends: dict = doc.ask("Show monthly sales trends")
```

## Word Document Processing

```python
from toolfront import Document

doc = Document("/path/to/meeting_notes.docx")

# Extract meeting information
action_items: list[str] = doc.ask("What are the action items?")
decisions: list[str] = doc.ask("What decisions were made?")
next_meeting: str = doc.ask("When is the next meeting scheduled?")
```

## Batch Document Processing

```python
from toolfront import Document
from pathlib import Path
import pandas as pd

# Process multiple documents
results = []
doc_dir = Path("/path/to/documents/")

for pdf_file in doc_dir.glob("*.pdf"):
    try:
        doc = Document(str(pdf_file))
        
        # Extract key info from each document
        summary = doc.ask("Provide a 2-sentence summary")
        document_type = doc.ask("What type of document is this?")
        
        results.append({
            'filename': pdf_file.name,
            'type': document_type,
            'summary': summary
        })
        
    except Exception as e:
        print(f"Error processing {pdf_file.name}: {e}")

# Save results
df = pd.DataFrame(results)
df.to_csv("document_analysis.csv", index=False)
```

## Legal Document Review

```python
from toolfront import Document
from pydantic import BaseModel

class LegalReview(BaseModel):
    document_type: str
    jurisdiction: str
    compliance_issues: list[str]
    risk_level: str
    recommendations: list[str]

doc = Document("/path/to/legal_document.pdf")
review: LegalReview = doc.ask("Perform legal compliance review")

print(f"Document Type: {review.document_type}")
print(f"Risk Level: {review.risk_level}")
if review.compliance_issues:
    print(f"Issues Found: {len(review.compliance_issues)}")
```