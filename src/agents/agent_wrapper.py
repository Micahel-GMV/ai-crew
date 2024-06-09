import os
import uuid
from typing import Any, Dict, List, Optional, Tuple

from langchain.agents.agent import RunnableAgent
from langchain.agents.tools import tool as LangChainTool
from langchain.tools.render import render_text_description
from langchain_core.agents import AgentAction
from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI
from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    InstanceOf,
    PrivateAttr,
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError

from crewai.agents import CacheHandler, CrewAgentExecutor, CrewAgentParser, ToolsHandler
from crewai.memory.contextual.contextual_memory import ContextualMemory
from crewai.utilities import I18N, Logger, Prompts, RPMController
from crewai.utilities.token_counter_callback import TokenCalcHandler, TokenProcess
from crewai.agent import Agent


class AgentWrapper(Agent):
    """Represents an agent in a system.

    Each agent has a role, a goal, a backstory, and an optional language model (llm).
    The agent can also have memory, can operate in verbose mode, and can delegate tasks to other agents.

    Attributes:
            agent_executor: An instance of the CrewAgentExecutor class.
            role: The role of the agent.
            goal: The objective of the agent.
            backstory: The backstory of the agent.
            config: Dict representation of agent configuration.
            llm: The language model that will run the agent.
            function_calling_llm: The language model that will the tool calling for this agent, it overrides the crew function_calling_llm.
            max_iter: Maximum number of iterations for an agent to execute a task.
            memory: Whether the agent should have memory or not.
            max_rpm: Maximum number of requests per minute for the agent execution to be respected.
            verbose: Whether the agent execution should be in verbose mode.
            allow_delegation: Whether the agent is allowed to delegate tasks to other agents.
            tools: Tools at agents disposal
            step_callback: Callback to be executed after each step of the agent execution.
            callbacks: A list of callback functions from the langchain library that are triggered during the agent's execution process
    """

    __hash__ = object.__hash__  # type: ignore
    _logger: Logger = PrivateAttr()
    _rpm_controller: RPMController = PrivateAttr(default=None)
    _request_within_rpm_limit: Any = PrivateAttr(default=None)
    _token_process: TokenProcess = TokenProcess()

    formatting_errors: int = 0
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: UUID4 = Field(
        default_factory=uuid.uuid4,
        frozen=True,
        description="Unique identifier for the object, not set by user.",
    )
    role: str = Field(description="Role of the agent")
    goal: str = Field(description="Objective of the agent")
    backstory: str = Field(description="Backstory of the agent")
    cache: bool = Field(
        default=True,
        description="Whether the agent should use a cache for tool usage.",
    )
    config: Optional[Dict[str, Any]] = Field(
        description="Configuration for the agent",
        default=None,
    )
    max_rpm: Optional[int] = Field(
        default=None,
        description="Maximum number of requests per minute for the agent execution to be respected.",
    )
    verbose: bool = Field(
        default=False, description="Verbose mode for the Agent Execution"
    )
    allow_delegation: bool = Field(
        default=True, description="Allow delegation of tasks to agents"
    )
    tools: Optional[List[Any]] = Field(
        default_factory=list, description="Tools at agents disposal"
    )
    max_iter: Optional[int] = Field(
        default=25, description="Maximum iterations for an agent to execute a task"
    )
    max_execution_time: Optional[int] = Field(
        default=None,
        description="Maximum execution time for an agent to execute a task",
    )
    agent_executor: InstanceOf[CrewAgentExecutor] = Field(
        default=None, description="An instance of the CrewAgentExecutor class."
    )
    crew: Any = Field(default=None, description="Crew to which the agent belongs.")
    tools_handler: InstanceOf[ToolsHandler] = Field(
        default=None, description="An instance of the ToolsHandler class."
    )
    cache_handler: InstanceOf[CacheHandler] = Field(
        default=None, description="An instance of the CacheHandler class."
    )
    step_callback: Optional[Any] = Field(
        default=None,
        description="Callback to be executed after each step of the agent execution.",
    )
    i18n: I18N = Field(default=I18N(), description="Internationalization settings.")
    llm: Any = Field(
        default_factory=lambda: ChatOpenAI(
            model=os.environ.get("OPENAI_MODEL_NAME", "gpt-4")
        ),
        description="Language model that will run the agent.",
    )
    function_calling_llm: Optional[Any] = Field(
        description="Language model that will run the agent.", default=None
    )
    callbacks: Optional[List[InstanceOf[BaseCallbackHandler]]] = Field(
        default=None, description="Callback to be executed"
    )

    _original_role: str | None = None
    _original_goal: str | None = None
    _original_backstory: str | None = None

    def __init__(__pydantic_self__, **data):
        config = data.pop("config", {})
        super().__init__(**config, **data)

    @field_validator("id", mode="before")
    @classmethod
    def _deny_user_set_id(cls, v: Optional[UUID4]) -> None:
        # if v:
        #     raise PydanticCustomError(
        #         "may_not_set_field", "This field is not to be set by the user.", {}
        #     )
        return

    @model_validator(mode="after")
    def set_attributes_based_on_config(self) -> "Agent":
        """Set attributes based on the agent configuration."""
        if self.config:
            for key, value in self.config.items():
                setattr(self, key, value)
        return self

    @model_validator(mode="after")
    def set_private_attrs(self):
        return self

    @model_validator(mode="after")
    def set_agent_executor(self) -> "Agent":
        return self

    def execute_task(
            self,
            task: Any,
            context: Optional[str] = None,
            tools: Optional[List[Any]] = None,
    ) -> str:
        return ""

    def set_cache_handler(self, cache_handler: CacheHandler) -> None:
        return
    def set_rpm_controller(self, rpm_controller: RPMController) -> None:
        return

    def create_agent_executor(self, tools=None) -> None:
        return

    def interpolate_inputs(self, inputs: Dict[str, Any]) -> None:
        return

    def increment_formatting_errors(self) -> None:
        return

    def format_log_to_str(
            self,
            intermediate_steps: List[Tuple[AgentAction, str]],
            observation_prefix: str = "Observation: ",
            llm_prefix: str = "",
    ) -> str:
        return ""

    def _parse_tools(self, tools: List[Any]) -> List[LangChainTool]:
        return None

    @staticmethod
    def __tools_names(tools) -> str:
        return ""

    def __repr__(self):
        return f"Agent(role={self.role}, goal={self.goal}, backstory={self.backstory})"
