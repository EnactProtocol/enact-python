from enact import EnactClient
from enact.models import EnactTask
import asyncio
import yaml
import json
from pathlib import Path


class MockRegistry:
    async def get_task(self, task_id):
        if task_id == "DataAnalyzer":
            # Load the YAML file from the current directory
            yaml_path = Path(__file__).parent / "data_analyzer.yaml"
            with open(yaml_path, 'r') as f:
                return yaml.safe_load(f)
        raise ValueError(f"Task {task_id} not found")


class MockClient(EnactClient):
    async def get_task(self, task_id: str):
        # Mock the registry response
        response = await MockRegistry().get_task(task_id)
        # Debug print
        print(f"Loaded task definition: {json.dumps(response, indent=2)}")

        # Validate the task
        task = EnactTask.model_validate(response)
        # Debug print
        print(f"Validated task dependencies: {task.dependencies}")
        return task


async def main():
    # Create mock client
    client = MockClient("http://dummy-url")

    try:
        # Sample data for testing
        test_data = list(range(1, 101))  # Numbers 1 to 100

        print("Executing DataAnalyzer task...")
        result = await client.execute_task("DataAnalyzer", {
            "data": test_data
        })

        # Print statistics
        print("\nStatistics:")
        stats = result['statistics']
        for key, value in stats.items():
            if key != 'quartiles':
                print(f"{key}: {value}")
            else:
                print("\nQuartiles:")
                for q, v in value.items():
                    print(f"{q}: {v}")

        # Save histogram to file
        print("\nSaving histogram...")
        import base64
        histogram_data = result['histogram']
        image_path = Path(__file__).parent / "histogram.png"
        with open(image_path, 'wb') as f:
            f.write(base64.b64decode(histogram_data))
        print(f"Histogram saved to {image_path}")

    except Exception as e:
        print(f"Error executing task: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
