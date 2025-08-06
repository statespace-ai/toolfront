# xAI

Configure ToolFront to use xAI's Grok models for analysis and insights.

## Setup

Export your xAI API key as an environment variable:

```bash
export XAI_API_KEY=<YOUR_XAI_API_KEY>
```

Get your API key from the [xAI Console](https://console.x.ai/).

## Model Selection

ToolFront supports xAI's Grok models:

### Latest Models
Use the latest version of Grok models for optimal performance:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Always gets the latest Grok version
result = db.ask("What are the most interesting patterns in our data?", model="xai:grok-beta")
```

!!! note
    All xAI models must be prefixed with `xai:` when using with ToolFront.