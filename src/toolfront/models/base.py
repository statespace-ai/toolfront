import ast
import asyncio
import inspect
import json
import linecache
import logging
from abc import ABC, abstractmethod
from contextvars import ContextVar
from importlib.resources import files
from typing import Any, Self

import pandas as pd
import yaml
from pydantic import BaseModel, Field
from pydantic_ai import Agent, Tool, UnexpectedModelBehavior, models
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
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from toolfront.config import MAX_RETRIES
from toolfront.utils import (
    deserialize_response,
    get_default_model,
    prepare_tool_for_pydantic_ai,
    type_allows_none,
)

logger = logging.getLogger("toolfront")
console = Console()

# Type alias for cleaner return type annotation
BasicTypes = str | bool | int | float
Collections = list | set | tuple | dict
AskReturnType = BasicTypes | Collections | BaseModel | pd.DataFrame

# Context variable to store datasources for the current context
_context_datasources: ContextVar[dict[str, "DataSource"] | None] = ContextVar("context_datasources", default=None)


class CallerContext(BaseModel):
    """Context information about the caller of a method."""

    var_name: str | None = Field(None, description="The name of the variable that will be assigned the response")
    var_type: Any = Field(None, description="The type of the variable that will be assigned the response")
    context: str | None = Field(None, description="Formatted caller context string")


class DataSource(BaseModel, ABC):
    """Abstract base class for all datasources."""

    def __repr__(self) -> str:
        dump = self.model_dump()
        args = ", ".join(f"{k}={repr(v)}" for k, v in dump.items())
        return f"{self.__class__.__name__}({args})"

    def __str__(self) -> str:
        return self.__repr__()

    @classmethod
    def from_url(cls, url: str) -> Self:
        if url.startswith("http"):
            from toolfront.models.api import API

            return API(spec=url)
        elif url.startswith("file"):
            if url.endswith(".json") or url.endswith(".yaml") or url.endswith(".yml"):
                from toolfront.models.api import API

                return API(spec=url)
            else:
                from toolfront.models.document import Library

                return Library(url=url)
        else:
            from toolfront.models.database import Database

            return Database(url=url)

    @classmethod
    def load_from_sanitized_url(cls, sanitized_url: str) -> Self:
        context_cache = _context_datasources.get() or {}
        if sanitized_url not in context_cache:
            raise ValueError(f"Datasource {sanitized_url} not found")

        obj = context_cache[sanitized_url]
        if not isinstance(obj, cls):
            raise ValueError(f"Datasource {sanitized_url} is not a {cls.__name__}")
        return obj

    @abstractmethod
    def tools(self) -> list[callable]:
        raise NotImplementedError("Subclasses must implement tools")

    def ask(
        self,
        prompt: str,
        model: models.Model | models.KnownModelName | str | None = None,
        context: str | None = None,
    ) -> AskReturnType:
        """
        Ask the datasource a question and display the response beautifully in the terminal.
        """

        if model is None:
            model = get_default_model()

        # Get caller context and add it to the system prompt
        output_type = str
        caller_context = self._get_caller_context()
        if caller_context.var_type:
            output_type = self._preprocess(caller_context.var_type)

        system_prompt = self.instructions(context=context)
        tools = [Tool(prepare_tool_for_pydantic_ai(tool), max_retries=MAX_RETRIES) for tool in self.tools()]

        agent = Agent(
            model=model,
            tools=tools,
            system_prompt=system_prompt,
            output_retries=MAX_RETRIES,
            output_type=output_type | None,
        )

        result = asyncio.run(self._ask_async(prompt, agent))

        if result is None and not type_allows_none(output_type):
            raise RuntimeError(
                f"ask() failed and returned None but output type {output_type.__name__} does not allow None values. "
                f"To fix this, update the type annotation to allow None e.g. answer: {output_type.__name__} | None = ask(...)"
            )

        return self._postprocess(result)

    def _preprocess(self, var_type: Any) -> Any:
        return var_type

    def _postprocess(self, result: Any) -> Any:
        return result

    def instructions(self, context: str | None = None) -> str:
        """
        Get the context for the datasource.
        """
        instruction_file = files("toolfront") / "instructions" / "ask.txt"

        with instruction_file.open() as f:
            agent_instruction = f.read()

        if context:
            agent_instruction += f"\n\nThe user has provided the following information:\n\n{context}"

        return (
            f"{agent_instruction}\n\n"
            f"Use the following information about the user's data to guide your response:\n\n"
            f"{yaml.dump(self.model_dump())}"
        )

    async def _ask_async(
        self,
        prompt: str,
        agent: Agent,
    ) -> AskReturnType:
        """
        Stream the agent response with live updating display.
        Returns the final result from the agent.
        """

        panel_title = f"[bold green]{str(self)}[/bold green]"

        try:
            with Live(
                Panel(
                    Text("Thinking...", style="dim white"),
                    title=panel_title,
                    border_style="green",
                ),
                refresh_per_second=10,
                vertical_overflow="crop",
            ) as live:
                accumulated_content = ""
                # live.stop()

                def update_display(content: str):
                    live.update(Panel(Markdown(content), title=panel_title, border_style="green"))

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
                                        accumulated_content += event.delta.content_delta
                                        update_display(accumulated_content)

                        elif Agent.is_call_tools_node(node):
                            # A handle-response node => The model returned some data, potentially calls a tool
                            async with node.stream(run.ctx) as handle_stream:
                                async for event in handle_stream:
                                    if isinstance(event, FunctionToolCallEvent):
                                        try:
                                            accumulated_content += f"\n\n>Called tool `{event.part.tool_name}` with args:\n\n```yaml\n{yaml.dump(json.loads(event.part.args))}\n```\n\n"
                                        except Exception:
                                            accumulated_content += event.part.args

                                        update_display(accumulated_content)
                                    elif isinstance(event, FunctionToolResultEvent):
                                        tool_result = deserialize_response(event.result.content)
                                        accumulated_content += (
                                            f"\n\n>Tool `{event.result.tool_name}` returned:\n\n{tool_result}\n\n"
                                        )
                                        update_display(accumulated_content)

                        elif Agent.is_end_node(node):
                            return node.data.output
        except UnexpectedModelBehavior as e:
            logger.error(f"Unexpected model behavior: {e}", exc_info=True)
            raise RuntimeError(f"Unexpected model behavior: {e}")

    def _get_caller_context(self) -> CallerContext:
        """
        Get the raw code that comes after the call to this method.
        Returns a CallerContext object with formatted context and filtered schema.
        """
        try:
            # Get the caller's frame (go up the call stack)
            frame = inspect.currentframe()
            caller_frame = frame.f_back.f_back  # ask() -> this method -> actual caller

            # Get the filename and line number where the call was made
            filename = caller_frame.f_code.co_filename
            call_line = caller_frame.f_lineno

            # Use linecache to get all lines at once (much more efficient)
            all_lines = linecache.getlines(filename)

            # Get the specific line where the call was made
            call_line_content = all_lines[call_line - 1] if call_line > 0 else ""

            # Extract variable assignment with type annotation
            var_name = None
            var_type = None

            try:
                tree = ast.parse(call_line_content.lstrip())
                for node in ast.walk(tree):
                    if isinstance(node, ast.AnnAssign):
                        # Handle annotated assignments like: var_name: Type = value
                        if isinstance(node.target, ast.Name):
                            var_name = node.target.id
                            annotation_str = ast.unparse(node.annotation)
                            var_type = eval(annotation_str, caller_frame.f_globals, caller_frame.f_locals)
                        break
            except SyntaxError:
                pass

            return CallerContext(var_name=var_name, var_type=var_type, context=None)

        except Exception as e:
            logger.debug(f"Could not get caller context: {e}")
            return CallerContext(var_name=None, var_type=None, context=None)
