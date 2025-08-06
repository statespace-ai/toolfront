# HuggingFace

Configure ToolFront to use any HuggingFace model for analysis and insights.

## Setup

Export your HuggingFace API key as an environment variable:

```bash
export HUGGINGFACE_API_KEY=<YOUR_HUGGINGFACE_API_KEY>
```

Get your API key from [HuggingFace](https://huggingface.co/settings/tokens).

## Model Selection

ToolFront supports any HuggingFace model by using the model name directly:

### Using Any HuggingFace Model
You can use any model available on HuggingFace by prefixing with `huggingface:`:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Use any HuggingFace model
result = db.ask("Analyze our sales data", model="huggingface:microsoft/DialoGPT-large")

# Another example with a different model
result = db.ask("Generate insights", model="huggingface:meta-llama/Llama-2-7b-chat-hf")
```

### Popular Models
Some commonly used models include:

```python
# For conversation and analysis
result = db.ask("Customer behavior analysis", model="huggingface:microsoft/DialoGPT-large")

# For code-related tasks  
result = db.ask("Optimize database queries", model="huggingface:codellama/CodeLlama-7b-Python-hf")
```

!!! note
    All HuggingFace models must be prefixed with `huggingface:` when using with ToolFront. You can use any model available on the HuggingFace Hub.