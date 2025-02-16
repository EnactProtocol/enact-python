import httpx
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
            # Convert response to EnactTask model
            return EnactTask.model_validate(response.json())

    async def execute_task(self, task_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task locally with given inputs"""
        task = await self.get_task(task_id)
        script = self.executor.create_script(task, inputs)
        return self.executor.execute_locally(script)
