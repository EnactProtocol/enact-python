from enact import EnactClient
import asyncio


async def main():
    # Create client pointing to your local server
    client = EnactClient("http://localhost:8080")

    try:
        # Execute the simple test task
        result = await client.execute_task("new-processor", {
            "text": "Keith"  # Even though we don't use this input in the task
        })

        print("Task output:", result['text_analysis']["reversed_text"])
    except Exception as e:
        print(f"Error executing task: {e}")

if __name__ == "__main__":
    asyncio.run(main())
