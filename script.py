#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import subprocess

def create_directory_structure():
    """Create the basic directory structure for the project"""
    directories = [
        "src/enact",
        "tests",
        "examples",
        "docs",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        Path(directory) / "__init__.py"
        
def create_pyproject_toml():
    """Create the pyproject.toml file with poetry configuration"""
    content = '''[tool.poetry]
name = "enact-python"
version = "0.1.0"
description = "Python SDK for the Enact protocol"
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "enact", from = "src"}]

[tool.poetry.dependencies]
python = "^3.9"
pydantic = "^2.0.0"
httpx = "^0.25.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"
pytest-asyncio = "^0.21.0"
black = "^23.0.0"
ruff = "^0.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
select = ["E", "F", "I"]
fix = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
'''
    
    with open("pyproject.toml", "w") as f:
        f.write(content)

def create_readme():
    """Create the README.md file"""
    content = '''# enact-python

Python SDK for the Enact protocol. Execute and manage protocol tasks locally or remotely.

## Installation

```bash
pip install enact-python
```

## Quick Start

```python
from enact import EnactClient

# Initialize client
client = EnactClient("https://api.myregistry.com")

# Execute a task
result = await client.execute_task("GetStockPrice", {
    "ticker": "AAPL",
    "api_key": "xxx"
})
print(result)
```

## Development

This project uses Poetry for dependency management. To get started:

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run tests:
   ```bash
   poetry run pytest
   ```

## License

MIT
'''
    
    with open("README.md", "w") as f:
        f.write(content)

def create_source_files():
    """Create the source files"""
    files = {
        "src/enact/__init__.py": '''from .client import EnactClient

__version__ = "0.1.0"
__all__ = ["EnactClient"]
''',
        
        "src/enact/models.py": '''from typing import List, Dict, Any, Literal
from pydantic import BaseModel

class Author(BaseModel):
    name: str

class TaskInput(BaseModel):
    type: str
    description: str

class TaskOutput(BaseModel):
    type: str
    format: str | None = None
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
    description: str
    version: str
    type: Literal["atomic", "composite"]
    authors: List[Author]
    inputs: Dict[str, TaskInput]
    tasks: List[Task]
    flow: Flow
    outputs: Dict[str, TaskOutput]
''',
        
        "src/enact/client.py": '''import httpx
from typing import Dict, Any

from .models import EnactTask
from .executor import TaskExecutor

class EnactClient:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.executor = TaskExecutor()

    async def get_task(self, task_id: str) -> EnactTask:
        """Fetch task definition from registry"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_base_url}/tasks/{task_id}")
            response.raise_for_status()
            return EnactTask.parse_obj(response.json())

    async def execute_task(self, task_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task locally with given inputs"""
        task = await self.get_task(task_id)
        script = self.executor.create_script(task, inputs)
        return self.executor.execute_locally(script)
''',
        
        "src/enact/executor.py": '''import json
import tempfile
from typing import Any, Dict
import uuid
import subprocess

from .models import EnactTask

class TaskExecutor:
    def create_script(self, task: EnactTask, inputs: Dict[str, Any]) -> str:
        python_task = next(
            (t for t in task.tasks if t.language == "python"),
            None
        )
        if not python_task:
            raise ValueError("No Python task found in Enact definition")

        return f"""
import json

# Input values
inputs = {json.dumps(inputs, indent=2)}

# Main task code
{python_task.code}

# Print output as JSON
print(json.dumps({{"price": price}}))
"""

    def execute_locally(self, script: str) -> Dict[str, Any]:
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            prefix=f'task-{uuid.uuid4()}',
            delete=True
        ) as tmp:
            tmp.write(script)
            tmp.flush()

            result = subprocess.run(
                ['python', tmp.name],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise RuntimeError(f"Task execution failed: {result.stderr}")

            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse output: {result.stdout}")
''',
        
        "tests/test_client.py": '''import pytest
from enact import EnactClient

@pytest.mark.asyncio
async def test_get_task():
    client = EnactClient("http://localhost:8000")
    # Add your tests here
    assert True

@pytest.mark.asyncio
async def test_execute_task():
    client = EnactClient("http://localhost:8000")
    # Add your tests here
    assert True
''',
        
        "examples/stock_price.py": '''from enact import EnactClient
import asyncio

async def main():
    client = EnactClient("https://api.myregistry.com")
    
    result = await client.execute_task("GetStockPrice", {
        "ticker": "AAPL",
        "api_key": "test-key"
    })
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
'''
    }
    
    for path, content in files.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)

def create_gitignore():
    """Create .gitignore file"""
    content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.coverage
htmlcov/
.pytest_cache/
'''
    
    with open(".gitignore", "w") as f:
        f.write(content)

def initialize_git():
    """Initialize git repository"""
    subprocess.run(["git", "init"])

def main():
    # Create project directory
    project_dir = "enact-python"
    if os.path.exists(project_dir):
        print(f"Directory {project_dir} already exists. Please remove it or choose a different location.")
        return
    
    os.makedirs(project_dir)
    os.chdir(project_dir)
    
    print("Creating project structure...")
    create_directory_structure()
    
    print("Creating pyproject.toml...")
    create_pyproject_toml()
    
    print("Creating README.md...")
    create_readme()
    
    print("Creating source files...")
    create_source_files()
    
    print("Creating .gitignore...")
    create_gitignore()
    
    print("Initializing git repository...")
    initialize_git()
    
    print(f"""
Project created successfully!

Next steps:
1. cd {project_dir}
2. Install poetry if you haven't: curl -sSL https://install.python-poetry.org | python3 -
3. Run 'poetry install' to install dependencies
4. Run 'poetry run pytest' to verify the setup

The project structure has been created and git has been initialized.
You can now start developing your SDK!
""")

if __name__ == "__main__":
    main()