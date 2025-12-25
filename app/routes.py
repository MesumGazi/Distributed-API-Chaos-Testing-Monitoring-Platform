import httpx
import asyncio
from fastapi import FastAPI
from .services.services import url_validation
from .config.config import setting
app=FastAPI()


urls=[setting.url]*setting.attempts

@app.get("/check")
async def is_google_up():

    semaphore = asyncio.Semaphore(setting.max_concurrency_limit)
    async with httpx.AsyncClient(timeout=0.5) as client:
        async def semaphore_limit(url):
            async with semaphore:
                return await url_validation(url,client)
        tasks=[semaphore_limit(url) for url in urls]
        results = await asyncio.gather(*tasks)

    return results



if __name__ == "__main__":
    asyncio.run(is_google_up())

