# Google

Configure ToolFront to use Google's Gemini models with large context windows.

## Setup

Export your Google API key as an environment variable:

```bash
export GOOGLE_API_KEY=<YOUR_GOOGLE_API_KEY>
```

Get your API key from [Google AI Studio](https://aistudio.google.com/).

## Model Selection

ToolFront supports two approaches for Google model selection:

### Latest Models
Use the latest version of any model family. These automatically update to the newest release:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Always gets the latest Gemini 2.5 Pro version
result = db.ask("Perform comprehensive analysis", model="google-gla:gemini-2.5-pro")

# Always gets the latest Gemini 2.5 Flash version  
result = db.ask("Quick data insights", model="google-gla:gemini-2.5-flash")
```

### Pinned Snapshots
Pin to specific model snapshots for reproducible results in production:

```python
# Pinned to a specific Gemini Pro snapshot
result = db.ask("Comprehensive analysis", model="google-gla:gemini-2.5-pro-preview-05-06")

# Pinned to a specific Gemini Flash snapshot
result = db.ask("Quick insights", model="google-gla:gemini-2.5-flash-preview-05-20")
```

!!! note
    All Google models must be prefixed with `google-gla:` or `google-vertex:` when using with ToolFront.