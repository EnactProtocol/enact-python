from enact import EnactClient
import asyncio


async def main():
    client = EnactClient("https://api.enactprotocol.com")
    try:
        # Search for data analysis tasks
        results = await client.search_tasks("A task that processes a text input and returns various text analytics")
        print("\nSearch Results:")

        # Find the best matching task
        best_task = None
        for result in results:
            print(f"\nTask ID: {result.id}")
            print(f"Description: {result.description}")
            print(f"Similarity Score: {result.similarity}")

            if result.similarity > 0.8:
                if best_task is None or result.similarity > best_task.similarity:
                    best_task = result

        # Execute only the best matching task
        if best_task:
            print(f"\nExecuting task {best_task.id}...")
            task_result = await client.execute_task(best_task.id, {
                "text": "Sample text for processing"
            })
            print("Task output:", task_result)
        else:
            print("\nNo tasks found with similarity score above 0.8")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
