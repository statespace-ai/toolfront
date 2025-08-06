# Groq

Configure ToolFront to use Groq's ultra-fast inference for lightning-quick responses.

## Setup

Export your Groq API key as an environment variable:

```bash
export GROQ_API_KEY=<YOUR_GROQ_API_KEY>
```

Get your API key from the [Groq Console](https://console.groq.com/).

## Model Selection

ToolFront supports Groq's high-performance models:

### Latest Models
Use the latest version of Groq models for optimal speed:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Llama 3.3 70B for complex reasoning
result = db.ask("Analyze customer behavior patterns", model="groq:llama-3.3-70b-versatile")

# Llama 3.1 8B for fast queries
result = db.ask("Get total sales", model="groq:llama-3.1-8b-instant")
```

!!! note
    All Groq models must be prefixed with `groq:` when using with ToolFront.