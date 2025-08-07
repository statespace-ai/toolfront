# Frequently Asked Questions

## How does ToolFront keep my data safe?

- **Local execution**: All database connections and queries run on your machine
- **No secrets exposure**: Database secrets are never shared with LLMs  
- **Read-only operations**: Only safe, read-only database queries are allowed

## How is ToolFront different from other MCP servers and agent frameworks?

ToolFront is purpose-built for **data retrieval** with native support for databases, APIs, and documents. Unlike general-purpose frameworks, it provides:

- **Zero-setup data connections** - Works with 15+ databases out of the box
- **Structured outputs** - Type-safe responses using Pydantic
- **Token-efficient exports** - Raw data bypasses LLM processing for large datasets
- **Built-in MCP server** - Ready for Claude Desktop and other MCP clients

## Which AI models can I use?

ToolFront is model-agnostic and supports all major providers: OpenAI, Anthropic, Google, Groq, Cohere, Mistral, xAI, DeepSeek, AWS Bedrock, and HuggingFace models.
