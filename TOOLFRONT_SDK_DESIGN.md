# ToolFront SDK Design Document

## Executive Summary

ToolFront is a Python SDK that provides AI agents and developers with unified access to databases, APIs, and document libraries. Built on a flexible `DataSource` abstraction, it enables natural language queries against any data source while maintaining a privacy-first architecture where all operations run locally. The SDK supports multiple integration modes including direct Python usage, AI agent tools, and optional Model Context Protocol (MCP) server deployment.

## Architecture Overview

### Core Design Principles

1. **SDK-First Design**: Core functionality exists as a standalone Python SDK with multiple integration options
2. **Unified Abstraction**: Single `DataSource` interface for databases, APIs, and documents
3. **AI-Native**: Built-in natural language query capabilities via the `ask()` method
4. **Type Safety**: Strong typing with Pydantic models and runtime validation
5. **Privacy by Default**: All operations are local, read-only, and credentials are sanitized
6. **Protocol Agnostic**: MCP is just one of many possible integration methods

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Integration Layer                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐ │
│  │ Python SDK  │  │  MCP Server  │  │  Future: REST API │ │
│  │  (Direct)   │  │  (Optional)  │  │   gRPC, etc.     │ │
│  └──────┬──────┘  └──────┬───────┘  └─────────┬─────────┘ │
│         └─────────────────┴───────────────────┬─┘          │
│                                               │             │
├───────────────────────────────────────────────▼─────────────┤
│                      ToolFront SDK Core                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              DataSource Abstraction                  │  │
│  │                  (models/base.py)                    │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────┐  ┌───────▼────┐  ┌──────────┐              │
│  │ Database │  │    API     │  │ Library  │              │
│  │  Model   │  │   Model    │  │  Model   │              │
│  └─────┬────┘  └─────┬──────┘  └────┬─────┘              │
│        │              │               │                     │
│  ┌─────▼──────────────▼───────────────▼────┐              │
│  │         Tool Implementations            │              │
│  │  • inspect_table  • inspect_endpoint    │              │
│  │  • query         • request              │              │
│  │                  • glob_search_documents │              │
│  │                  • read_document         │              │
│  └──────────────────────────────────────────┘              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Supporting Components                   │  │
│  │  • Type-safe models  • AI integration (pydantic-ai) │  │
│  │  • Serialization    • Connection management         │  │
│  │  • Error handling   • Context tracking              │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Deep Dive

### 1. DataSource Abstraction (`models/base.py`)

The `DataSource` class is the foundation of the SDK, providing:

- **Unified Interface**: All data sources inherit from this abstract base class
- **Direct Tool Access**: `tools()` method returns callable functions for programmatic use
- **AI Integration**: Built-in `ask()` method for natural language queries using any LLM
- **Context Management**: Automatic context tracking for multi-datasource environments
- **URL-based Factory**: `from_url()` creates appropriate datasource type based on URL scheme

Key Methods:
- `ask(prompt, model)`: Natural language interface with typed responses
- `tools()`: Returns list of callable tool functions
- `from_url(url)`: Factory method for creating datasources
- `prompt(context)`: Generates system prompt for AI agents

Key Features:
- **CallerContext**: Introspects calling code to determine expected return types
- **Live Streaming**: Real-time display of AI agent's thinking process via Rich console
- **Type Inference**: Automatically adapts output format based on variable annotations
- **Model Agnostic**: Supports OpenAI, Anthropic, Google, and other LLM providers

### 2. Database Implementation (`models/database.py`)

Built on the Ibis framework for universal database connectivity:

- **Wide Support**: 15+ database types via optional dependencies (PostgreSQL, MySQL, BigQuery, Snowflake, etc.)
- **Schema Discovery**: Automatic table listing with regex pattern support
- **Read-Only Safety**: SQL query validation ensures no write operations
- **Connection Management**: Lazy initialization with automatic retry logic

Tool Methods:
- `inspect_table(table)`: Returns schema information and sample data
- `query(query)`: Executes read-only SQL with dialect awareness

Design Patterns:
- Uses Ibis for consistent API across different SQL dialects
- Hierarchical table naming (catalog.database.schema.table)
- Connection pooling and reuse for performance

### 3. API Implementation (`models/api.py`)

OpenAPI/Swagger-based REST API integration:

- **Spec Loading**: Supports file://, http://, or inline OpenAPI specifications
- **Dynamic Discovery**: Automatically extracts available endpoints
- **Authentication**: Runtime injection of API keys and headers
- **Request Building**: Type-safe request construction with path/query/body parameters

Tool Methods:
- `inspect_endpoint(endpoint)`: Returns endpoint schema and parameters
- `request(endpoint, params, body)`: Makes HTTP requests with automatic auth

Security Features:
- API keys stored separately and injected at runtime
- Credentials never exposed in logs or responses
- Support for various auth methods (headers, query params)

### 4. Library Implementation (`models/library.py`)

Document management with intelligent chunking:

- **Format Support**: PDF, DOCX, PPTX, Excel, Markdown, JSON, YAML, HTML, etc.
- **Smart Chunking**: 10KB sections with percentile-based navigation
- **Binary Conversion**: Uses MarkItDown for converting binary formats to text
- **Efficient Search**: Glob patterns for document discovery

Tool Methods:
- `glob_search_documents(pattern)`: Pattern-based document discovery
- `read_document(path, pagination)`: Chunked reading with section navigation

Navigation Features:
- Percentile-based access (0.0-0.99 for document position)
- Section-based access (1, 2, 3... for specific chunks)
- Metadata includes section context ("Section X of Y")

### 5. Integration Layers

#### Direct Python SDK Usage
```python
from toolfront import Database, API, Library

# Create datasources
db = Database("postgresql://localhost/mydb")
api = API(spec="https://api.example.com/openapi.json")
docs = Library("file:///path/to/docs")

# Use natural language
sales: list[dict] = db.ask("Show me Q4 sales by region")

# Or use tools directly
schema = await db.inspect_table(Table(path="public.orders"))
response = await api.request(endpoint=Endpoint(method="GET", path="/users"))
```

#### MCP Server Integration (`mcp.py`)
Minimal 47-line wrapper that:
- Creates DataSource from URL
- Registers tools with FastMCP framework
- Adds a `prompt()` tool for initial context
- Handles stdio/sse transport modes

```python
# Run as MCP server
toolfront postgresql://localhost/mydb --transport stdio
```

#### Future Integration Options
The architecture supports adding:
- REST API server mode
- gRPC service mode
- GraphQL endpoint
- Jupyter notebook extension
- VS Code extension

### 6. Supporting Components

#### Utilities (`utils.py`)
- **`prepare_tool_for_pydantic_ai()`**: Wraps tools with error handling
- **`serialize_response()`**: Converts Python objects to JSON with truncation
- **`sanitize_url()`**: Removes passwords from database URLs
- **`get_default_model()`**: Determines LLM from environment variables

#### Configuration (`config.py`)
- Environment-based configuration
- Timeout and retry settings
- Chunk size for document processing
- Optional telemetry for collaborative learning

## Data Flow Patterns

### 1. Direct SDK Usage Flow
1. User creates DataSource instance with URL
2. User calls `ask()` with natural language prompt
3. SDK creates pydantic-ai Agent with datasource tools
4. Agent determines which tools to call
5. Tools execute and return structured data
6. Response formatted according to type hint

### 2. Tool Invocation Flow
1. User calls tool method directly (e.g., `db.query()`)
2. Pydantic model validates inputs
3. Tool executes with error handling
4. Response serialized and returned
5. Automatic truncation for large results

### 3. MCP Integration Flow
1. MCP client sends tool request
2. MCP server routes to DataSource method
3. Method executes and returns result
4. Response serialized for MCP protocol
5. Client receives structured response

## Design Patterns

### 1. Abstract Factory Pattern
- `DataSource.from_url()` creates appropriate subclass
- URL scheme determines datasource type
- Enables seamless switching between sources

### 2. Strategy Pattern
- Each datasource implements its own tool methods
- Common interface allows polymorphic usage
- Easy to add new datasource types

### 3. Decorator Pattern
- `prepare_tool_for_pydantic_ai()` adds cross-cutting concerns
- Automatic serialization and error handling
- Consistent tool behavior across datasources

### 4. Template Method Pattern
- Base `DataSource` defines algorithm structure
- Subclasses implement specific behaviors
- Common functionality inherited by all

## Security Architecture

1. **Read-Only by Design**: All operations are read-only
2. **Local Execution**: No data leaves the local environment
3. **Credential Management**: Passwords sanitized in logs/displays
4. **Input Validation**: Pydantic models validate all inputs
5. **SQL Injection Prevention**: Query validation and parameterization

## Performance Optimizations

1. **Lazy Loading**: Connections created on-demand
2. **Connection Pooling**: Reuses database connections via Ibis
3. **Chunking**: Large documents/results automatically paginated
4. **Response Truncation**: Prevents memory issues with large results
5. **Streaming**: Live updates during AI processing

## Extensibility Guide

### Adding New Database Types
1. Ensure Ibis supports the database (or implement backend)
2. Add optional dependency group in `pyproject.toml`
3. Database automatically available via URL scheme

### Adding New DataSource Types
1. Create class inheriting from `DataSource`
2. Implement abstract `tools()` method
3. Add URL scheme handling in `from_url()`
4. Define Pydantic models for parameters

### Adding New Integration Modes
1. Import datasource classes
2. Create wrapper for target protocol/framework
3. Map tool methods to protocol requirements
4. Handle authentication and transport

### Custom Tools
1. Add async method to DataSource subclass
2. Use Pydantic models for parameters
3. Include in `tools()` return list
4. Document with clear docstrings

## Testing Strategy

- **Unit Tests**: Mock datasource connections
- **Integration Tests**: Real databases via Docker
- **Type Safety**: Pyright static analysis
- **Code Quality**: Ruff for linting/formatting
- **Coverage**: Track with pytest-cov

## Migration Path from MCP-Only

For users currently using ToolFront via MCP:

1. **No Breaking Changes**: MCP server continues to work
2. **Gradual Adoption**: Can use SDK directly alongside MCP
3. **Same Tools**: All MCP tools available as SDK methods
4. **Enhanced Features**: SDK offers more control and flexibility

## Conclusion

ToolFront's architecture achieves flexibility through its SDK-first design. The DataSource abstraction provides a consistent interface for any data source, while multiple integration layers ensure compatibility with different use cases. The modular design allows users to choose their preferred integration method - from direct Python usage to MCP servers to future protocols - without lock-in to any particular approach.

The separation of core SDK functionality from integration layers ensures that ToolFront can evolve with the AI ecosystem while maintaining stability for existing users. This architecture positions ToolFront as a foundational tool for AI-powered data access, regardless of how AI agents and frameworks evolve.