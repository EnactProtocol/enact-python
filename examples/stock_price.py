# examples/stock_price.py
from enact import EnactClient
import asyncio
import httpx


async def main():
    # Create client pointing to your local server
    client = EnactClient("http://localhost:8080")

    try:
        print("Attempting to execute task...")
        result = await client.execute_task("hello world", {
            "name": "World"
        })
        print("Task output:", result)
    except httpx.HTTPError as e:
        print(
            f"HTTP error occurred: {e.response.text if hasattr(e, 'response') else e}")
    except Exception as e:
        print(f"Error executing task: {type(e).__name__}: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
