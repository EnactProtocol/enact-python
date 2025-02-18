# src/enact/models.py
from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field
from typing import Optional, List


class SearchResult(BaseModel):
    id: str
    description: str
    version: str
    type: str = Field(default="atomic")
    similarity: float = Field(
        description="Similarity score from vector search")
    name: Optional[str] = None  # Made optional since it's not in response
    inputs: Optional[Dict[str, Any]] = None
    outputs: Optional[Dict[str, Any]] = None


class PackageDependency(BaseModel):
    name: str
    version: str


class PythonDependencies(BaseModel):
    packages: List[PackageDependency]
    version: Optional[str] = None


class Dependencies(BaseModel):
    python: Optional[PythonDependencies] = None
    # Add other runtime dependencies as needed


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
    type: str = Field(default="atomic")
    authors: List[Author]
    inputs: Dict[str, TaskInput]
    tasks: List[Task]
    flow: Flow
    outputs: Dict[str, TaskOutput]
    dependencies: Optional[Dependencies] = None  # New field

    class Config:
        extra = "allow"  # Allow extra fields in the input data
