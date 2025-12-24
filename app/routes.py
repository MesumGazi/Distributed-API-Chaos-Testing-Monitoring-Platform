import httpx
import asyncio
from fastapi import FastAPI
from serivices.services import url_validation
from config.config import url,attempts
app=FastAPI()


urls=[url]*attempts

@app.get("/check")
async def is_google_up(max_concurrency_limit=10):
    semaphore = asyncio.Semaphore(max_concurrency_limit)
    async def semaphore_limit(url):
        async with semaphore:
            return await url_validation(url)
    tasks=[semaphore_limit(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


