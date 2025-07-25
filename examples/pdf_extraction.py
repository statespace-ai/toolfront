"""
PDF Data Extraction with ToolFront

Simple example showing how to extract structured data from PDFs.
Perfect for turning documents into usable data.
"""

from typing import Any
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from toolfront import Document

# Load environment variables
load_dotenv()


# Define structured output model
class Invoice(BaseModel):
    invoice_number: str
    client_name: str
    client_email: str | None = None
    total_amount: float
    due_date: str


def extract_as_dict(pdf_path: str):
    """Extract data as a dictionary - simple and flexible."""
    
    doc = Document(filepath=pdf_path)
    
    # With ToolFront's new defaults, this returns a dict automatically!
    return doc.ask("""
        Extract invoice data:
        - Invoice number
        - Client name and email
        - Total amount (as a number)
        - Due date
    """, model="anthropic:claude-3-5-sonnet-latest")


def extract_as_pydantic(pdf_path: str) -> Invoice | None:
    """Extract data as a Pydantic model - structured and validated."""
    
    doc = Document(filepath=pdf_path)
    
    # Type annotation tells ToolFront to return an Invoice object
    invoice: Invoice | None = doc.ask("""
        Extract invoice information from this document.
        Make sure to include all required fields.
    """, model="anthropic:claude-3-5-sonnet-latest")
    
    return invoice  # type: ignore[return-value]


if __name__ == "__main__":
    # Check if sample PDF exists
    sample_pdf = Path(__file__).parent / "sample-invoice.pdf"
    
    if not sample_pdf.exists():
        print("Downloading sample invoice PDF...")
        import requests
        url = "https://github.com/excid3/receipts/raw/main/examples/invoice.pdf"
        response = requests.get(url)
        sample_pdf.write_bytes(response.content)
        print(f"Downloaded to {sample_pdf}\n")
    
    # Example 1: Simple dictionary output
    print("=== Dictionary Extraction ===")
    dict_result = extract_as_dict(str(sample_pdf))
    print(f"Result: {dict_result}\n")
    
    # Example 2: Structured Pydantic model
    print("=== Pydantic Model Extraction ===")
    pydantic_result = extract_as_pydantic(str(sample_pdf))
    if pydantic_result:
        print(f"Invoice #{pydantic_result.invoice_number}")
        print(f"Client: {pydantic_result.client_name}")
        print(f"Total: ${pydantic_result.total_amount}")
        print(f"Due: {pydantic_result.due_date}")
    else:
        print("Failed to extract invoice data")