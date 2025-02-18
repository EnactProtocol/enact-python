# examples/hello_world.py
from enact import EnactClient
from enact.models import EnactTask
import asyncio
import json

# Simulate a task definition (normally this would come from your registry)
HELLO_TASK = {
    "enact": "1.0.0",
    "id": "HelloWorld",
    "name": "Hello World",
    "description": "A simple hello world task",
    "version": "1.0.0",
    "type": "atomic",
    "authors": [
        {"name": "Test User"}
    ],
    "inputs": {
        "name": {
            "type": "string",
            "description": "Name to greet"
        }
    },
    "tasks": [
        {
            "id": "greet",
            "type": "script",
            "language": "python",
            "code": """
name = inputs['name']
message = f"Hello, {name}!"
print(json.dumps({"greeting": message}))
"""
        }
    ],
    "flow": {
        "steps": [
            {"task": "greet"}
        ]
    },
    "outputs": {
        "greeting": {
            "type": "string",
            "description": "The greeting message"
        }
    }
}


class MockRegistry:
    async def get_task(self, task_id):
        if task_id == "HelloWorld":
            return HELLO_TASK
        raise ValueError(f"Task {task_id} not found")


class MockClient(EnactClient):
    async def get_task(self, task_id: str):
        # Mock the registry response
        response = await MockRegistry().get_task(task_id)
        # Convert dictionary to EnactTask model
        return EnactTask.model_validate(response)


async def main():
    # Create client with dummy URL (won't be used due to our mock)
    client = MockClient("http://dummy-url")

    try:
        # Execute the hello world task
        result = await client.execute_task("HelloWorld", {
            "name": "World"
        })
        print("Task output:", result)
    except Exception as e:
        print(f"Error executing task: {e}")

if __name__ == "__main__":
    asyncio.run(main())
