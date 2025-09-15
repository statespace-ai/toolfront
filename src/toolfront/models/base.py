import asyncio
import json
import logging
from abc import ABC, abstractmethod
from importlib.resources import files
from typing import Any

import yaml
from pydantic import BaseModel
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
from pydantic_ai.settings import ModelSettings
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown

from toolfront.config import MAX_RETRIES
from toolfront.utils import get_model_from_env, get_output_type_hint, history_processor, prepare_tool_for_pydantic_ai

logger = logging.getLogger("toolfront")
console = Console()


class DataSource(BaseModel, ABC):
    """Abstract base class for all datasources."""

    def __repr__(self) -> str:
        dump = self.model_dump()
        args = ", ".join(f"{k}={repr(v)}" for k, v in dump.items())
        return f"{self.__class__.__name__}({args})"

    def __str__(self) -> str:
        return self.__repr__()

    @abstractmethod
    def tools(self) -> list[callable]:
        raise NotImplementedError("Subclasses must implement tools")

    def instructions(self, context: str | None = None) -> str:
        """Generate system instructions for AI agents.

        Parameters
        ----------
        context : str, optional
            Additional business context to include in instructions.

        Returns
        -------
        str
            System instructions for AI interaction with this datasource.
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

    def ask(
        self,
        prompt: str,
        model: models.Model | models.KnownModelName | str | None = None,
        context: str | None = None,
        output_type: BaseModel | None = None,
        temperature: float = 0.0,
        context_window: int = 10,
        verbose: bool = False,
    ) -> Any:
        """Ask natural language questions and get structured responses.

        Parameters
        ----------
        prompt : str
            Natural language question or instruction.
        model : str, optional
            AI model to use (e.g., 'openai:gpt-4', 'anthropic:claude-3-5-sonnet').
        context : str, optional
            Additional business context for better responses.
        output_type : BaseModel, optional
            Pydantic model for structured responses.
        context_window : int, optional
            Number of messages to keep in memory.
        verbose : bool, optional
            Show live AI reasoning in terminal.

        Returns
        -------
        Any
            Response matching the requested output type.
        """
        # Get the model from the environment or use the default model
        model = model or get_model_from_env()

        # Get the output type from the caller or use the default output type
        output_type = get_output_type_hint() or output_type or str

        system_prompt = self.instructions(context=context)
        tools = [Tool(prepare_tool_for_pydantic_ai(tool), max_retries=MAX_RETRIES) for tool in self.tools()]

        agent = Agent(
            model=model,
            tools=tools,
            system_prompt=system_prompt,
            output_retries=MAX_RETRIES,
            output_type=output_type,
            retries=MAX_RETRIES,
            model_settings=ModelSettings(
                temperature=temperature,
            ),
            history_processors=[history_processor(context_window=context_window)],
        )

        return asyncio.run(self._ask_async(prompt, agent, verbose))

    async def _ask_async(
        self,
        prompt: str,
        agent: Agent,
        verbose: bool = False,
    ) -> Any:
        """
        Run the agent and optionally stream the response with live updating display.
        Returns the final result from the agent.
        """

        console = Console()

        try:
            if verbose:
                # Streaming mode with Rich Live display
                with Live(
                    console=console,
                    vertical_overflow="visible",
                    auto_refresh=False,
                ) as live:
                    accumulated_content = ""

                    def update_display(content: str):
                        live.update(Markdown(content))
                        live.refresh()

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
                                async with node.stream(run.ctx) as handle_stream:
                                    async for event in handle_stream:
                                        if isinstance(event, FunctionToolCallEvent):
                                            try:
                                                accumulated_content += f"\n\n>Called tool `{event.part.tool_name}` with args:\n\n```yaml\n{yaml.dump(json.loads(event.part.args))}\n```\n\n"
                                            except Exception:
                                                accumulated_content += event.part.args
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
