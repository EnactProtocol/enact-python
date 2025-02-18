from enact import EnactClient
import asyncio

from enact import EnactClient
import asyncio


async def main():
    client = EnactClient("http://localhost:8080")
    try:
        # Search for data analysis tasks
        results = await client.search_tasks("A task that processes a text input and returns various text analytics")
        print("\nSearch Results:")
        for result in results:
            print(f"\nTask ID: {result.id}")
            print(f"Description: {result.description}")
            # Changed from similarity_score
            print(f"Similarity Score: {result.similarity}")

            # If we find a highly relevant task, we can execute it
            if result.similarity > 0.8:  # Changed from similarity_score
                print(f"\nExecuting task {result.id}...")
                # Changed input to match the text processing task
                task_result = await client.execute_task(result.id, {
                    "text": "Sample text for processing"
                })
                print("Task output:", task_result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
