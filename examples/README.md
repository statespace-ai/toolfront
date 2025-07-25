# ToolFront Examples

This directory contains examples demonstrating ToolFront's capabilities.

## Examples

### 1. basic.py
Basic database querying with natural language using ToolFront's `ask()` method.

```bash
python basic.py
```

### 2. pdf_extraction.py
Extract structured data from PDFs using ToolFront's document processing:
- Dictionary output (simple and flexible)
- Pydantic model output (structured and validated)
- Automatic sample PDF download

```bash
python pdf_extraction.py
```

## Getting Started

1. Install ToolFront:
```bash
pip install toolfront[document]
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

## Tips

1. **New dict default**: `ask()` now returns dictionaries by default - perfect for data extraction!
2. **Type hints**: Use type annotations to get Pydantic models, lists, or other structured output
3. **Be specific**: The more specific your prompt, the better the extraction results

## Need Help?

Check out the [ToolFront documentation](https://github.com/toolfront/toolfront) for more details.