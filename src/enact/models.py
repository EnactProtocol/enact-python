# src/enact/models.py
from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field


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
    name: str
    description: str
    version: str
    # Make type optional with default value
    type: str = Field(default="atomic")
    authors: List[Author]
    inputs: Dict[str, TaskInput]
    tasks: List[Task]
    flow: Flow
    outputs: Dict[str, TaskOutput]

    class Config:
        extra = "allow"  # Allow extra fields in the input data
