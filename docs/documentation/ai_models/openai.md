# OpenAI

Configure ToolFront to use OpenAI's powerful language models.

## Setup

Export your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

Get your API key from the [OpenAI Platform](https://platform.openai.com/api-keys).

## Model Selection

ToolFront supports two approaches for OpenAI model selection:

### Latest Models
Use the latest version of any model family. These automatically update to the newest release:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Always gets the latest GPT-4o version
result = db.ask("Analyze our sales data", model="openai:gpt-4o")

# Always gets the latest GPT-4 version  
result = db.ask("Generate a report", model="openai:gpt-4")
```

### Pinned Snapshots
Pin to specific model snapshots for reproducible results in production:

```python
# Pinned to a specific GPT-4o snapshot
result = db.ask("Analyze our sales data", model="openai:gpt-4o-2024-11-20")

# Pinned to a specific o1 snapshot
result = db.ask("Solve complex reasoning", model="openai:o1-2024-12-17")
```

!!! note
    All OpenAI models must be prefixed with `openai:` when using with ToolFront.