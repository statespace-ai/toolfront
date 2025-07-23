# Toolfront SDK Design Document

## Executive Summary

This document outlines the architectural transformation of the Toolfront MCP server into a more accessible product consisting of:
1. A lightweight open-source agent
2. An ergonomic SDK for developers
3. Modular, reusable libraries extracted from the existing MCP tooling logic

The goal is to democratize access to powerful data tools by removing the MCP barrier while maintaining compatibility with the existing ecosystem.

## Current State

### Architecture Overview
The current system is an MCP (Model Context Protocol) server that exposes tools for:
- Database operations (inspection, querying, searching)
- API interactions (endpoint discovery, requests)
- Document/library management (reading, searching)

### Limitations
- **Accessibility**: MCP is not widely known, creating adoption barriers
- **Complexity**: Developers need to understand MCP protocol to use the tools
- **Monolithic**: Tools are tightly coupled to the MCP server implementation

## Proposed Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Applications Layer                    │
├─────────────────────┬───────────────┬──────────────────┤
│   Toolfront Agent   │ Toolfront SDK │    MCP Server    │
├─────────────────────┴───────────────┴──────────────────┤
│                 Toolfront Core Libraries                 │
├──────────────┬────────────────┬────────────────────────┤
│ Database Lib │    API Lib     │    Document Lib        │
├──────────────┴────────────────┴────────────────────────┤
│                    Common Utilities                      │
│        (Search, Serialization, Caching, Types)         │
└─────────────────────────────────────────────────────────┘
```

### Component Descriptions

#### 1. Toolfront Core Libraries
Extracted, modular libraries that encapsulate the tool logic:

**@toolfront/database**
- Database connection management
- Table inspection and sampling
- Query execution with safety checks
- Search capabilities

**@toolfront/api**
- HTTP client abstraction
- Endpoint discovery and inspection
- Request execution with authentication
- Response parsing and validation

**@toolfront/documents**
- Document loading and parsing
- Full-text search implementation
- Format conversion utilities
- Chunking strategies

**@toolfront/common**
- Shared types and interfaces
- Search algorithms (BM25, fuzzy matching)
- Serialization utilities
- Caching layer

#### 2. Toolfront SDK
A developer-friendly SDK that provides simple APIs:

```python
from toolfront import Toolfront

# Initialize in one line
tf = Toolfront(database="postgresql://...", api="https://api.example.com")

# Use tools with simple methods
results = await tf.database.query("SELECT * FROM users LIMIT 10")
response = await tf.api.request("GET", "/users")
content = await tf.documents.search("authentication")
```

#### 3. Toolfront Agent
A lightweight, open-source agent that:
- Uses the SDK internally
- Provides natural language interface
- Handles tool orchestration
- Manages conversation context

```python
from toolfront import Agent

# Initialize agent
agent = Agent(
    database="postgresql://...",
    api="https://api.example.com",
    model="gpt-4"  # or any LLM
)

# Natural language interface
response = await agent.run("Find all users who signed up last month")
```

#### 4. MCP Server (Maintained)
The existing MCP server continues to work by importing the core libraries:
- No breaking changes for existing users
- Benefits from improvements to core libraries
- Minimal code changes required

## Implementation Plan

### Phase 1: Library Extraction (Weeks 1-2)

1. **Create package structure**
   ```
   packages/
   ├── @toolfront/common/
   ├── @toolfront/database/
   ├── @toolfront/api/
   ├── @toolfront/documents/
   └── @toolfront/sdk/
   ```

2. **Extract common utilities**
   - Move types.py → @toolfront/common/types
   - Move utils.py → @toolfront/common/utils
   - Move cache.py → @toolfront/common/cache
   - Create unified configuration system

3. **Extract tool-specific logic**
   - Database tools → @toolfront/database
   - API tools → @toolfront/api
   - Document tools → @toolfront/documents
   - Maintain backward compatibility

### Phase 2: SDK Development (Weeks 3-4)

1. **Design SDK API surface**
   - Intuitive method names
   - Consistent error handling
   - Comprehensive typing
   - Async-first with sync wrappers

2. **Implement core SDK features**
   ```python
   class Toolfront:
       def __init__(self, database=None, api=None, documents=None):
           # Initialize components
       
       async def connect(self):
           # Establish connections
       
       @property
       def database(self) -> DatabaseTools:
           # Database tool access
       
       @property
       def api(self) -> APITools:
           # API tool access
   ```

3. **Add convenience methods**
   - Batch operations
   - Transaction support
   - Progress callbacks
   - Result streaming

### Phase 3: Agent Development (Weeks 5-6)

1. **Agent architecture**
   ```python
   class Agent:
       def __init__(self, toolfront: Toolfront, model: str):
           self.tools = toolfront
           self.llm = LLMProvider(model)
           self.memory = ConversationMemory()
       
       async def run(self, query: str) -> str:
           # Parse intent
           # Select tools
           # Execute plan
           # Format response
   ```

2. **Core agent features**
   - Tool selection based on query
   - Multi-step planning
   - Error recovery
   - Result synthesis

3. **LLM integration**
   - Support multiple providers (OpenAI, Anthropic, etc.)
   - Prompt engineering for tool use
   - Token optimization

### Phase 4: MCP Server Migration (Week 7)

1. **Update imports**
   - Replace internal imports with library imports
   - Maintain existing tool signatures
   - Update dependencies

2. **Testing and validation**
   - Ensure backward compatibility
   - Performance benchmarking
   - Integration tests

## Technical Decisions

### Package Management
- **Monorepo**: Use a monorepo with workspaces for easier development
- **Publishing**: Publish packages independently to PyPI/npm
- **Versioning**: Semantic versioning with coordinated releases

### Language Support
- **Primary**: Python (existing codebase)
- **Future**: TypeScript/JavaScript SDK for broader adoption

### Testing Strategy
- Unit tests for each package
- Integration tests for SDK
- End-to-end tests for agent
- Compatibility tests for MCP server

### Documentation
- API reference for each package
- Getting started guides
- Example applications
- Migration guide from MCP

## Success Metrics

1. **Developer Experience**
   - Time to first successful query < 5 minutes
   - SDK initialization in ≤ 3 lines of code
   - Clear error messages and debugging

2. **Performance**
   - No regression in tool execution speed
   - Minimal memory overhead
   - Efficient connection pooling

3. **Adoption**
   - Number of SDK downloads
   - GitHub stars and community engagement
   - Third-party integrations

## Risks and Mitigations

### Risk 1: Breaking Changes
**Mitigation**: Comprehensive test suite, careful API design, beta testing period

### Risk 2: Performance Regression
**Mitigation**: Benchmark suite, profiling, optimization passes

### Risk 3: Adoption Challenges
**Mitigation**: Excellent documentation, example projects, community outreach

## Future Enhancements

1. **Hosted API Service**
   - Managed infrastructure
   - Authentication and rate limiting
   - Usage analytics

2. **Additional Tool Categories**
   - File system operations
   - Cloud service integrations
   - Monitoring and observability

3. **Advanced Agent Features**
   - Multi-agent coordination
   - Custom tool creation
   - Fine-tuning support

## Conclusion

This transformation will make Toolfront's powerful data tools accessible to a broader audience while maintaining compatibility with existing MCP users. The modular architecture ensures flexibility and enables future growth in multiple directions.