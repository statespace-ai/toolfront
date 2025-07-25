# ToolFront Examples

This directory contains examples demonstrating ToolFront's capabilities.

## Examples

### 1. basic.py
Basic database querying with natural language using ToolFront's `ask()` method.

```bash
python basic.py
```

### 2. pdf_extraction.py
Simple PDF invoice extraction example:
- Basic invoice data extraction from PDF
- Shows type annotation usage with Pydantic models
- Good starting point for understanding ToolFront document processing

```bash
python pdf_extraction.py
```

### 3. invoice_processing_workflow.py
Complete invoice processing workflow demonstrating ToolFront in production:
- **Batch processing**: Handle multiple PDF invoices automatically
- **Business validation**: Apply rules like amount limits and vendor checks
- **File organization**: Auto-sort processed/failed files into folders
- **CSV export**: Generate accounting-system-ready data exports
- **Reporting**: Detailed processing summaries with financial totals
- **Error handling**: Production-ready exception handling

```bash
python invoice_processing_workflow.py
```

This example shows how ToolFront PDF extraction fits into a complete business automation pipeline.

## Getting Started

1. Install ToolFront:
```bash
# For PDF processing
pip install toolfront[document-pdf]

# For Office documents (Word, PowerPoint, Excel)
pip install toolfront[document-office]

# For all document formats (includes cloud services)
pip install toolfront[document-all]
```

2. Set up your environment variables in `.env`:
```env
# For AI features (required)
ANTHROPIC_API_KEY=your-api-key
# or
OPENAI_API_KEY=your-api-key

# For database examples (optional)
POSTGRES_URL=postgresql://user:pass@host/database
SNOWFLAKE_URL=snowflake://user:pass@account/database
```

3. Run the examples:
```bash
python examples/pdf_extraction.py
```

## Key Features Demonstrated

### Document Processing
- Extract structured data from PDFs automatically
- Convert unstructured documents to JSON/Pydantic models
- Perfect for invoice processing, contract analysis, etc.

### Database Analysis  
- Natural language queries across any database
- Cross-database analytics
- Automated reporting

## Important: Type Annotations

**ToolFront uses Python type annotations to determine return types:**

```python
# Returns dict by default (new in v0.2.0)
result = doc.ask("Extract data")

# Returns validated Pydantic model
invoice: Invoice = doc.ask("Extract invoice data")

# Returns list of dictionaries  
items: list[dict] = doc.ask("Extract line items")
```

**This type annotation requirement isn't well documented yet** - it's a known UX issue we're working on.

## Tips

1. **Always use type annotations** when you want structured output
2. **Be specific in prompts**: The more detailed your request, the better the extraction
3. **Handle errors**: Wrap extraction in try/catch for production use

## Need Help?

Check out the [ToolFront documentation](https://github.com/toolfront/toolfront) for more details.