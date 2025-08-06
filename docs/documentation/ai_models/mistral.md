# Mistral

Configure ToolFront to use Mistral's efficient European AI models.

## Setup

Export your Mistral API key as an environment variable:

```bash
export MISTRAL_API_KEY=<YOUR_MISTRAL_API_KEY>
```

Get your API key from the [Mistral AI Platform](https://console.mistral.ai/).

## Model Selection

ToolFront supports Mistral's European AI models:

### Latest Models
Use the latest version of Mistral models for optimal performance:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Always gets the latest Mistral Large version
result = db.ask("Perform comprehensive analysis", model="mistral:mistral-large-latest")

# Always gets the latest Mistral Small version  
result = db.ask("Quick metrics calculation", model="mistral:mistral-small-latest")
```

!!! note
    All Mistral models must be prefixed with `mistral:` when using with ToolFront.

## Key Advantages

- **European data privacy compliance**
- **Multilingual capabilities**
- **Cost-effective**
- **Fast inference**

## Best Use Cases

```python
# Multilingual analysis
global_insights = db.ask(
    "Analyze sales data from European markets",
    model='mistral:mistral-large-latest'
)

# Privacy-compliant processing
sensitive_analysis = db.ask(
    "Analyze customer data with GDPR compliance",
    model='mistral:mistral-large-latest'
)
```