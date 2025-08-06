# Cohere

Configure ToolFront to use Cohere's enterprise-focused language models.

## Setup

Export your Cohere API key as an environment variable:

```bash
export COHERE_API_KEY=<YOUR_COHERE_API_KEY>
```

Get your API key from the [Cohere Dashboard](https://dashboard.cohere.ai/).

## Model Selection

ToolFront supports two approaches for Cohere model selection:

### Latest Models
Use the latest version of any model family. These automatically update to the newest release:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Always gets the latest Command R+ version
result = db.ask("Generate business intelligence analysis", model="cohere:command-r-plus")

# Always gets the latest Command R version  
result = db.ask("Analyze sales trends", model="cohere:command-r")
```

### Pinned Snapshots
Pin to specific model snapshots for reproducible results in production:

```python
# Pinned to a specific Command R+ snapshot
result = db.ask("Generate business intelligence analysis", model="cohere:command-r-plus-08-2024")

# Pinned to a specific Command R snapshot
result = db.ask("Analyze sales trends", model="cohere:command-r-08-2024")
```

!!! note
    All Cohere models must be prefixed with `cohere:` when using with ToolFront.