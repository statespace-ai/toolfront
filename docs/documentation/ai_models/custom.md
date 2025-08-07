# Custom & Self-Hosted Models

Use custom or self-hosted AI models with ToolFront.

## Supported Backends

ToolFront supports any model compatible with Pydantic AI, including:

- **Local models** via Ollama
- **Self-hosted models** via HTTP APIs
- **Custom model implementations**

## Ollama (Local Models)

Run models locally using Ollama:

```bash
# Install and run Ollama
ollama run llama2
```

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Use local Ollama model
result = db.ask(
    "What's our revenue?", 
    model="ollama:llama2"
)
```

## Custom HTTP APIs

Connect to custom model endpoints:

```python
from pydantic_ai.models import HttpModel

# Define custom model
custom_model = HttpModel(
    base_url="http://localhost:8080/v1/",
    model_name="custom-model"
)

# Use with ToolFront
result = db.ask(
    "What's our revenue?", 
    model=custom_model
)
```

## Configuration

For detailed configuration options, refer to the [Pydantic AI models documentation](https://ai.pydantic.dev/models/).