# Anthropic

Configure ToolFront to use Anthropic's Claude models for analysis and reasoning.

## Setup

Export your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY=<YOUR_ANTHROPIC_API_KEY>
```

Get your API key from the [Anthropic Console](https://console.anthropic.com/).

## Model Selection

ToolFront supports two approaches for Anthropic model selection:

### Latest Models
Use the latest version of any model family. These automatically update to the newest release:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Always gets the latest Claude 3.5 Sonnet version
result = db.ask("Analyze our sales data", model="anthropic:claude-3-5-sonnet-latest")

# Always gets the latest Claude 3.5 Haiku version  
result = db.ask("Count active customers", model="anthropic:claude-3-5-haiku-latest")
```

### Pinned Snapshots
Pin to specific model snapshots for reproducible results in production:

```python
# Pinned to a specific Claude 3.5 Sonnet snapshot
result = db.ask("Analyze our sales data", model="anthropic:claude-3-5-sonnet-20241022")

# Pinned to a specific Claude 4 snapshot
result = db.ask("Complex strategic analysis", model="anthropic:claude-4-sonnet-20250514")
```

!!! note
    All Anthropic models must be prefixed with `anthropic:` when using with ToolFront.