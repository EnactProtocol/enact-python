from enact.dependency_manager import DependencyManager
import json
from typing import Any, Dict
from .models import EnactTask
from .dependency_manager import DependencyManager  # New import


class TaskExecutor:
    def __init__(self):
        self.dependency_manager = DependencyManager()

    def create_script(self, task: EnactTask, inputs: Dict[str, Any]) -> str:
        python_task = next(
            (t for t in task.tasks if t.language == "python"),
            None
        )
        if not python_task:
            raise ValueError("No Python task found in Enact definition")

        return f"""import json

# Input values
inputs = {json.dumps(inputs, indent=2)}

# Main task code
{python_task.code}"""

    def execute_locally(self, task: EnactTask, script: str) -> Dict[str, Any]:
        """Execute a task with its dependencies"""
        try:
            # Get dependencies
            dependencies = task.dependencies.model_dump() if task.dependencies else {}

            # Execute in managed environment
            output = self.dependency_manager.execute_in_venv(
                script, dependencies)

            try:
                return json.loads(output.strip())
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse output as JSON: {output}")

        except Exception as e:
            raise RuntimeError(f"Task execution failed: {str(e)}")
