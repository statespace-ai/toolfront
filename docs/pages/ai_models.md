# AI Models

ToolFront's [Python SDK](./python_sdk.md) supports various AI model providers through [Pydantic AI](https://ai.pydantic.dev/models/overview/).

[OpenAI](https://ai.pydantic.dev/models/openai/), [Anthropic](https://ai.pydantic.dev/models/anthropic/), [Google](https://ai.pydantic.dev/models/gemini/), [Bedrock](https://ai.pydantic.dev/models/bedrock/), [Cohere](https://ai.pydantic.dev/models/cohere/), [Groq](https://ai.pydantic.dev/models/groq/), [Mistral](https://ai.pydantic.dev/models/mistral/), [HuggingFace](https://ai.pydantic.dev/models/openai/#hugging-face), [xAI](https://ai.pydantic.dev/models/openai/#xai), [DeepSeek](https://ai.pydantic.dev/models/openai/#deepseek), [Azure AI](https://ai.pydantic.dev/models/openai/#azure), [Fireworks AI](https://ai.pydantic.dev/models/openai/#fireworks), [Moonshot AI](https://ai.pydantic.dev/models/openai/#moonshot), [GitHub Models](https://ai.pydantic.dev/models/openai/#github-models), [Heroku AI](https://ai.pydantic.dev/models/openai/#heroku), [OpenRouter](https://ai.pydantic.dev/models/openai/#openrouter), [Ollama](https://ai.pydantic.dev/models/openai/#ollama), [Together AI](https://ai.pydantic.dev/models/openai/#together-ai)

---

## Basic Usage

Set your model provider's API key as an environment variable:

=== ":simple-openai:{ .middle } &nbsp; OpenAI"

    ```bash
    export OPENAI_API_KEY="your-api-key"
    ```

    Then, specify your model using the `provider:model-name` format.

    ```python hl_lines="5"
    from toolfront import Environment

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model="openai:gpt-5")
    ```

=== ":simple-anthropic:{ .middle } &nbsp; Anthropic"

    ```bash
    export ANTHROPIC_API_KEY="your-api-key"
    ```

    Then, specify your model using the `provider:model-name` format.

    ```python hl_lines="5"
    from toolfront import Environment

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model="anthropic:claude-sonnet-4-5")
    ```

=== ":simple-google:{ .middle } &nbsp; Google"

    ```bash
    export GOOGLE_API_KEY="your-api-key"
    ```

    Then, specify your model using the `provider:model-name` format.

    ```python hl_lines="5"
    from toolfront import Environment

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model="google-gla:gemini-2.5-pro")
    ```

=== ":simple-mistralai:{ .middle } &nbsp; Mistral"

    ```bash
    export MISTRAL_API_KEY="your-api-key"
    ```

    Then, specify your model using the `provider:model-name` format.

    ```python hl_lines="5"
    from toolfront import Environment

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model="mistral:mistral-large-latest")
    ```

=== ":simple-huggingface:{ .middle } &nbsp; HuggingFace"

    ```bash
    export HUGGINGFACE_API_KEY="your-api-key"
    ```

    Then, specify your model using the `provider:model-name` format.

    ```python hl_lines="5"
    from toolfront import Environment

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model="huggingface:Qwen/Qwen3-235B-A22B")
    ```

!!! tip "Default Model"

    Set a default model with the `TOOLFRONT_MODEL` environment variable:

    ```bash
    export TOOLFRONT_MODEL="openai:gpt-5"
    ```

---

## Custom Models

Use any [Pydantic AI model](https://ai.pydantic.dev/models/overview/) directly for local models and other providers, for example:

=== ":simple-ollama:{ .middle } &nbsp; Ollama"

    ```python
    from toolfront import Environment
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.ollama import OllamaProvider

    ollama_model = OpenAIChatModel(
        model_name='llama3.2',
        provider=OllamaProvider(base_url='http://localhost:11434/v1'),
    )

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model=ollama_model)
    ```

=== ":simple-vercel:{ .middle } &nbsp; Vercel"

    ```python
    from toolfront import Environment
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.vercel import VercelProvider

    vercel_model = OpenAIChatModel(
        'anthropic/claude-4-sonnet',
        provider=VercelProvider(api_key='your-vercel-ai-gateway-api-key'),
    )

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model=vercel_model)
    ```

=== ":simple-perplexity:{ .middle } &nbsp; Perplexity"

    ```python
    from toolfront import Environment
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider

    perplexity_model = OpenAIChatModel(
        'sonar-pro',
        provider=OpenAIProvider(
            base_url='https://api.perplexity.ai',
            api_key='your-perplexity-api-key',
        ),
    )

    environment = Environment(url="file:///path/to/toolsite")

    result = environment.ask(..., model=perplexity_model)
    ```