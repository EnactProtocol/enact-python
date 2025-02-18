# src/enact/client.py
import httpx
from typing import Dict, Any
import json
from .models import EnactTask
from .executor import TaskExecutor


class EnactClient:
    def __init__(self, api_base_url: str):
        self.api_base_url = api_base_url
        self.executor = TaskExecutor()

    async def get_task(self, task_id: str) -> EnactTask:
        """Fetch task definition from registry"""
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.api_base_url}/api/yaml/tasks/{task_id}"
                print(f"Requesting URL: {url}")
                response = await client.get(url)
                response.raise_for_status()

                # Parse response
                data = response.json()

                # Extract protocolDetails
                if 'protocolDetails' not in data:
                    raise ValueError(
                        f"Response missing protocolDetails: {data}")

                protocol_details = data['protocolDetails']

                # Add type if missing (since it's in the parent object)
                if 'type' not in protocol_details and 'type' in data:
                    protocol_details['type'] = data['type']

                print("Protocol details to validate:",
                      json.dumps(protocol_details, indent=2))

                # Validate the protocolDetails part
                return EnactTask.model_validate(protocol_details)

        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            raise
        except json.JSONDecodeError as e:
            print(
                f"Failed to parse JSON response. Response text: {response.text}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    async def execute_task(self, task_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task locally with given inputs"""
        try:
            print(f"Fetching task: {task_id}")
            task = await self.get_task(task_id)

            print(f"Creating script with inputs: {inputs}")
            script = self.executor.create_script(task, inputs)

            print(f"Generated script:\n{script}")
            # Updated to pass both task and script
            return self.executor.execute_locally(task, script)
        except Exception as e:
            print(f"Error in execute_task: {e}")
            raise
