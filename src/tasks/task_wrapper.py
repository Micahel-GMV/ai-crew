import threading
import uuid
from typing import Any, Dict, List, Optional, Type, Callable

from langchain_openai import ChatOpenAI
from pydantic import UUID4, BaseModel, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError

from crewai.agent import Agent
from crewai.tasks.task_output import TaskOutput
from crewai.utilities import I18N, Converter, ConverterError, Printer
from crewai.utilities.pydantic_schema_parser import PydanticSchemaParser
from crewai.task import Task

class TaskWrapper(Task):

    class Config:
        arbitrary_types_allowed = True

    __hash__ = object.__hash__  # type: ignore
    used_tools: int = 0
    tools_errors: int = 0
    delegations: int = 0
    i18n: I18N = I18N()
    thread: threading.Thread = None
    prompt_context: Optional[str] = None
    description: str = Field(description="Description of the actual task.")
    expected_output: str = Field(
        description="Clear definition of expected output for the task."
    )
    config: Optional[Dict[str, Any]] = Field(
        description="Configuration for the agent",
        default=None,
    )
    callback: Optional[Any] = Field(
        description="Callback to be executed after the task is completed.", default=None
    )
    agent: Optional[Agent] = Field(
        description="Agent responsible for execution the task.", default=None
    )
    context: Optional[List["Task"]] = Field(
        description="Other tasks that will have their output used as context for this task.",
        default=None,
    )
    async_execution: Optional[bool] = Field(
        description="Whether the task should be executed asynchronously or not.",
        default=False,
    )
    output_json: Optional[Type[BaseModel]] = Field(
        description="A Pydantic model to be used to create a JSON output.",
        default=None,
    )
    output_pydantic: Optional[Type[BaseModel]] = Field(
        description="A Pydantic model to be used to create a Pydantic output.",
        default=None,
    )
    output_file: Optional[str] = Field(
        description="A file path to be used to create a file output.",
        default=None,
    )
    output: Optional[TaskOutput] = Field(
        description="Task output, it's final result after being executed", default=None
    )
    tools: Optional[List[Any]] = Field(
        default_factory=list,
        description="Tools the agent is limited to use for this task.",
    )
    id: UUID4 = Field(
        default_factory=uuid.uuid4,
        frozen=True,
        description="Unique identifier for the object, not set by user.",
    )
    human_input: Optional[bool] = Field(
        description="Whether the task should have a human review the final answer of the agent",
        default=False,
    )
    string_function: Optional[Callable[[str, str], str]] = Field(
        description="A function that takes two strings and returns a string",
        default=None,
    )

    _original_description: str | None = None
    _original_expected_output: str | None = None

    def __init__(__pydantic_self__, **data):
        config = data.pop("config", {})
        super().__init__(**config, **data)

    @field_validator("id", mode="before")
    @classmethod
    def _deny_user_set_id(cls, v: Optional[UUID4]) -> None:
        return

    @model_validator(mode="after")
    def set_attributes_based_on_config(self) -> "Task":
        """Set attributes based on the agent configuration."""
        if self.config:
            for key, value in self.config.items():
                setattr(self, key, value)
        return self

    @model_validator(mode="after")
    def check_tools(self):
        return self

    @model_validator(mode="after")
    def check_output(self):
        return self

    def execute(
            self,
            agent: Agent | None = None,
            context: Optional[str] = None,
            tools: Optional[List[Any]] = None,
    ) -> str:
        print(f"\nContext: {context}\n Description: {self.description}\n string_function: {self.string_function}")
        if self.string_function == None: return context + self.description
        return self.string_function(context, self.description)

    def _execute(self, agent, task, context, tools):
        return None

    def prompt(self) -> str:
        return ""

    def interpolate_inputs(self, inputs: Dict[str, Any]) -> None:
        return

    def increment_tools_errors(self) -> None:
        print(f"Task:increment_tools_errors()")
        return

    def increment_delegations(self) -> None:
        return

    def _export_output(self, result: str) -> Any:
        return None

    def _is_gpt(self, llm) -> bool:
        return False

    def _save_file(self, result: Any) -> None:
        return None

    def __repr__(self):
        print(f"Task:__repr__()")
        return f"Task(description={self.description}, expected_output={self.expected_output})"
