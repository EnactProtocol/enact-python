from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel


class Author(BaseModel):
    name: str


class TaskInput(BaseModel):
    type: str
    description: str
    default: Optional[str] = None


class TaskOutput(BaseModel):
    type: str
    format: Optional[str] = None
    description: str


class Task(BaseModel):
    id: str
    type: str
    language: str
    code: str


class FlowStep(BaseModel):
    task: str


class Flow(BaseModel):
    steps: List[FlowStep]


class EnactTask(BaseModel):
    enact: str
    id: str
    name: str  # Added this field
    description: str
    version: str
    type: Literal["atomic", "composite"]
    authors: List[Author]
    inputs: Dict[str, TaskInput]
    tasks: List[Task]
    flow: Flow
    outputs: Dict[str, TaskOutput]
