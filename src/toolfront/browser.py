import asyncio
import json
import logging
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_ai import Agent, UnexpectedModelBehavior, models
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.messages import (
    FunctionToolCallEvent,
    FunctionToolResultEvent,
    PartDeltaEvent,
    PartStartEvent,
    TextPart,
    TextPartDelta,
    ThinkingPart,
    ThinkingPartDelta,
)
from pydantic_ai.settings import ModelSettings
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from toolfront.environment import Environment
from toolfront.utils import history_processor

DEFAULT_TEMPERATURE = 0.0
DEFAULT_CONTEXT_WINDOW = 20
DEFAULT_TIMEOUT_SECONDS = 10
DEFAULT_MAX_RETRIES = 3

logger = logging.getLogger("toolfront")


class Browser(BaseModel):
    """Interface for navigating and interacting with environments."""

    model: models.Model | models.KnownModelName | str | None = Field(None, description="AI model to use.")
    temperature: float = Field(default=DEFAULT_TEMPERATURE, description="Model temperature.")
    context_window: int = Field(default=DEFAULT_CONTEXT_WINDOW, description="Model context window.")
    params: dict[str, str] | None = Field(
        None, description="Authentication parameters for the filesystem protocol", exclude=True
    )
    env: dict[str, str] | None = Field(
        None, description="Additional environment variables to include in requests.", exclude=True
    )

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        model: models.Model | models.KnownModelName | str | None = None,
        temperature: float = DEFAULT_TEMPERATURE,
        context_window: int = DEFAULT_CONTEXT_WINDOW,
        params: dict[str, str] | None = None,
        env: dict[str, str] | None = None,
        **kwargs,
    ):
        super().__init__(
            model=model,
            temperature=temperature,
            context_window=context_window,
            params=params,
            env=env,
            **kwargs,
        )

    def ask(
        self,
        prompt: str,
        url: str,
        output_type: Any = str,
        verbose: bool = False,
    ) -> Any:
        """Ask natural language questions about an environment and get structured responses.

        Parameters
        ----------
        prompt : str
            Natural language question or instruction
        url : str
            Starting URL/path to environment (file://, https://, s3://, etc.)
        output_type : Any | None, optional
            Desired output type (str, int, list, Pydantic model, etc.)
        verbose : bool, default False
            Whether to show live AI reasoning and tool calls

        Returns
        -------
        Any
            Response in the requested output_type format. If no type specified,
            uses type hint from caller or defaults to string.

        Example
        -------
        Simple string response:

        ```python
        result = browser.ask("Who is best customer?", "s3://path/to/site", output_type=str)
        # Returns: "Chimex Inc. seems to have the highest revenue"
        ```

        Example
        -------
        Typed response:

        ```python
        count = browser.ask("What's our Q3 revenue?", "s3://analytics-bucket/path/to/reports", output_type=float|None)
        # Returns: 225000.3
        ```

        Example
        -------
        Structured response:

        ```python
        from pydantic import BaseModel

        class Author(BaseModel):
            name: str

        authors = browser.ask("List all authors in this project", "git://path/to/site", output_type=list[Author])

        # Returns: [Author(name="Alice Smith"), Author(name="Bob Jones"), Author(name="Carol Lee")]
        ```
        """

        environment = Environment(url=url, params=self.params, env=self.env)

        server = MCPServerStdio(
            "uv",
            args=["run", "toolfront", "browser", "serve", url, "--transport", "stdio"],
            env=environment.env,
            max_retries=DEFAULT_MAX_RETRIES,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

        instructions = f"""
        Answer the user's question using only data explicitly retrieved through the provided tools.
        Never make assumptions, hallucinate data, or supplement answers with general knowledge.
        Always follow file and tool instructions.
        Return once you have found what you're looking for.
        If no relevant data can be found after exhaustive attempts, clearly explain why
        The following environment variables are available: {self.env}
        Your environment root URL is: {environment.url}
        Your environment home page URL is: {environment.home_page}
        """

        agent = Agent(
            model=self.model,
            system_prompt=instructions,
            toolsets=[server],
            output_retries=DEFAULT_MAX_RETRIES,
            output_type=output_type,
            retries=DEFAULT_MAX_RETRIES,
            model_settings=ModelSettings(
                temperature=self.temperature,
            ),
            history_processors=[history_processor(context_window=self.context_window)],
        )

        return asyncio.run(Browser._browse_async(prompt, agent, verbose))

    @staticmethod
    async def _browse_async(
        prompt: str,
        agent: Agent,
        verbose: bool = False,
    ) -> Any:
        """Execute the AI agent with optional live streaming display.

        This internal method handles the actual agent execution with two modes:
        - Verbose: Shows live AI reasoning, tool calls, and responses in terminal
        - Quiet: Runs silently and returns only the final result

        Parameters
        ----------
        prompt : str
            The user's natural language query
        agent : Agent
            Configured AI agent with tools and system prompt
        verbose : bool, default False
            Whether to show live updates during execution

        Returns
        -------
        Any
            The final agent response in the requested output format

        Raises
        ------
        RuntimeError
            If there's unexpected model behavior during execution
        """

        console = Console()

        try:
            if verbose:
                # Streaming mode with Rich Live display
                with Live(
                    console=console,
                    vertical_overflow="visible",
                    auto_refresh=True,
                ) as live:
                    accumulated_content = ""

                    def update_display(content: str):
                        live.update(Markdown(content))

                    async with agent.iter(prompt) as run:
                        async for node in run:
                            if Agent.is_model_request_node(node):
                                async with node.stream(run.ctx) as model_stream:
                                    async for event in model_stream:
                                        if isinstance(event, PartStartEvent):
                                            if isinstance(event.part, (TextPart | ThinkingPart)):
                                                accumulated_content += f"\n{event.part.content}"
                                                update_display(accumulated_content)
                                        elif isinstance(event, PartDeltaEvent) and isinstance(
                                            event.delta, (TextPartDelta | ThinkingPartDelta)
                                        ):
                                            accumulated_content += event.delta.content_delta or ""
                                            update_display(accumulated_content)

                            elif Agent.is_call_tools_node(node):
                                async with node.stream(run.ctx) as handle_stream:
                                    async for event in handle_stream:
                                        if isinstance(event, FunctionToolCallEvent):
                                            try:
                                                args_str = (
                                                    event.part.args
                                                    if isinstance(event.part.args, str)
                                                    else str(event.part.args)
                                                )
                                                accumulated_content += f"\n\n>Called tool `{event.part.tool_name}` with args:\n\n```yaml\n{yaml.dump(json.loads(args_str))}\n```\n\n"
                                            except Exception:
                                                accumulated_content += str(event.part.args)
                                            update_display(accumulated_content)
                                        elif isinstance(event, FunctionToolResultEvent):
                                            accumulated_content += f"\n\n>Tool `{event.result.tool_name}` returned:\n\n{event.result.content}\n\n"
                                            update_display(accumulated_content)

                            elif Agent.is_end_node(node):
                                return node.data.output
            else:
                # Quiet mode
                async with agent.iter(prompt) as run:
                    async for node in run:
                        if Agent.is_end_node(node):
                            return node.data.output
        except UnexpectedModelBehavior as e:
            logger.error(f"Unexpected model behavior: {e}", exc_info=True)
            raise RuntimeError(f"Unexpected model behavior: {e}")
