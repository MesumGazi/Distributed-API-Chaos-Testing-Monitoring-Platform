import httpx
import asyncio

async def fetch_check():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/check")
        print(response.status_code)
        print(response.json())

asyncio.run(fetch_check())
