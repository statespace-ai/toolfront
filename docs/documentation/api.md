# API Integration

ToolFront connects to any API that provides an [OpenAPI](https://swagger.io/specification/) (formerly known as Swagger) specification. OpenAPI/Swagger specs are standardized, machine-readable descriptions of REST APIs. You can load these specs from URLs, local files, or Python dictionaries.

=== ":fontawesome-solid-link:{ .middle } &nbsp; URL Spec"

    ```python linenums="1"
    from toolfront import API

    # OpenAPI spec from URL
    api = API("http://localhost:8000/openapi.json")
    
    summary = api.ask("Get summary of Python programming language")
    ```

=== ":fontawesome-solid-folder:{ .middle } &nbsp; Local File"

    ```python linenums="1"
    from toolfront import API

    # Local OpenAPI spec file
    api = API("file:///path/to/openapi.yaml")
    
    users = api.ask("List all active users")
    ```

=== ":fontawesome-solid-code:{ .middle } &nbsp; Dictionary Spec"

    ```python linenums="1"
    from toolfront import API

    # Direct spec dictionary
    spec = {
        "openapi": "3.0.0",
        "servers": [{"url": "https://api.example.com"}],
        "paths": {
            "/users": {"get": {"summary": "Get users"}}
        }
    }
    api = API(spec)
    
    result = api.ask("Get user information")
    ```

## Authentication

Pass authentication details (like API keys or headers) using the `headers` and `params` arguments when creating the `API` object:

```python linenums="1"
api = API(
    "https://api.example.com/openapi.json",
    headers={"Authorization": "Bearer your-token"},
    params={"version": "v2"}
)
```

