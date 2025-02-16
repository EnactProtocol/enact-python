from enact import EnactClient
import asyncio


async def main():
    client = EnactClient("http://localhost:8080")

    result = await client.execute_task("hello world")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
