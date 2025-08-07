# Azure OpenAI

Use OpenAI models through Microsoft Azure's OpenAI service.

## Setup

Set your Azure OpenAI credentials:

```bash
export AZURE_OPENAI_API_KEY=your_api_key
export AZURE_OPENAI_ENDPOINT=your_endpoint
```

## Usage

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Use Azure OpenAI model
result = db.ask(
    "What's our revenue?", 
    model="azure_openai:gpt-4"
)
```

## Configuration

Azure OpenAI requires additional configuration for endpoint and API version. Refer to the [Pydantic AI Azure OpenAI documentation](https://ai.pydantic.dev/models/#azure-openai) for detailed setup instructions.