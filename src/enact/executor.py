# src/enact/executor.py
import json
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

        # Note: We don't hardcode the output structure anymore
        return f"""
import json

# Input values
inputs = {json.dumps(inputs, indent=2)}

# Main task code
{python_task.code}
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

            # Run the script
            result = subprocess.run(
                ['python', tmp.name],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                raise RuntimeError(f"Task execution failed: {result.stderr}")

            try:
                # Strip any whitespace and try to parse JSON
                output = result.stdout.strip()
                return json.loads(output)
            except json.JSONDecodeError:
                raise ValueError(
                    f"Failed to parse output as JSON: {result.stdout}")
