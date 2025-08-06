# AWS Bedrock

Configure ToolFront to use AWS Bedrock's foundational models through Amazon's managed AI service.

## Setup

Export your AWS credentials as environment variables:

```bash
export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=<YOUR_AWS_REGION>
```

Configure AWS credentials through the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html) or IAM roles.

## Model Selection

ToolFront supports AWS Bedrock foundational models:

### Latest Models
Use the latest version of any model family available on Bedrock:

```python
from toolfront import Database

db = Database("postgresql://user:pass@host/db")

# Claude 3.5 Sonnet via Bedrock
result = db.ask("Analyze our sales data", model="bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0")

# Claude 3 Haiku via Bedrock  
result = db.ask("Count active customers", model="bedrock:anthropic.claude-3-haiku-20240307-v1:0")
```

### Pinned Snapshots
Pin to specific model versions for reproducible results in production:

```python
# Pinned to a specific Claude 3.5 Sonnet version
result = db.ask("Analyze our sales data", model="bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0")

# Pinned to a specific Llama 3.1 version
result = db.ask("Generate insights", model="bedrock:meta.llama3-1-70b-instruct-v1:0")
```

!!! note
    All AWS Bedrock models must be prefixed with `bedrock:` when using with ToolFront.

## Available Models

### Anthropic Claude Models
Access Claude models through AWS infrastructure:

```python
# Claude 3.5 Sonnet for complex analysis
analysis = db.ask(
    "Provide comprehensive business insights",
    model="bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0"
)

# Claude 3 Haiku for fast queries
metrics = db.ask(
    "Calculate monthly revenue",
    model="bedrock:anthropic.claude-3-haiku-20240307-v1:0"
)
```

### Meta Llama Models
Use Meta's Llama models via Bedrock:

```python
# Llama 3.1 70B for reasoning
reasoning = db.ask(
    "Analyze customer behavior patterns",
    model="bedrock:meta.llama3-1-70b-instruct-v1:0"
)

# Llama 3.1 8B for efficient processing
summary = db.ask(
    "Summarize quarterly performance",
    model="bedrock:meta.llama3-1-8b-instruct-v1:0"
)
```

## Key Advantages

- **Enterprise security** with AWS compliance
- **Regional deployment** for data residency
- **Cost management** through AWS billing
- **Scalable infrastructure** with AWS auto-scaling

## Best Use Cases

```python
# Enterprise data analysis with compliance
enterprise_analysis = db.ask(
    "Analyze sensitive customer data with full audit trail",
    model="bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0"
)

# Multi-region deployment
global_insights = db.ask(
    "Generate insights for global operations",
    model="bedrock:meta.llama3-1-70b-instruct-v1:0"
)
```

## Configuration Examples

### Cost-Optimized Setup
```python
# Use smaller models for routine queries
daily_metrics = db.ask(
    "Today's key performance indicators",
    model="bedrock:anthropic.claude-3-haiku-20240307-v1:0"
)

# Use larger models for strategic analysis
strategy = db.ask(
    "Comprehensive market analysis and recommendations",
    model="bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0"
)
```

### Multi-Model Approach
```python
# Use different models for different tasks
quick_summary = db.ask(
    "Quick sales summary",
    model="bedrock:meta.llama3-1-8b-instruct-v1:0"
)

detailed_analysis = db.ask(
    "Detailed customer segmentation analysis",
    model="bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0"
)
```