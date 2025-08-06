# DeepSeek

Configure ToolFront to use DeepSeek's reasoning-focused language models.

## Setup

Export your DeepSeek API key as an environment variable:

```bash
export DEEPSEEK_API_KEY=<YOUR_DEEPSEEK_API_KEY>
```

Get your API key from the [DeepSeek Platform](https://platform.deepseek.com/).

## Model Selection

ToolFront supports DeepSeek's advanced reasoning models:

### Latest Models
Use the latest version of DeepSeek models for optimal performance:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# DeepSeek Chat for general reasoning
result = db.ask("Analyze customer behavior patterns", model="deepseek:deepseek-chat")

# DeepSeek Reasoner for complex logical tasks
result = db.ask("Solve multi-step analytical problems", model="deepseek:deepseek-reasoner")
```

!!! note
    All DeepSeek models must be prefixed with `deepseek:` when using with ToolFront.