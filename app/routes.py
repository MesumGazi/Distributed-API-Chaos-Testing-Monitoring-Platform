import httpx
import asyncio
from fastapi import FastAPI
from .services.services import url_validation
from .config.config import setting

#fast api instance
app=FastAPI()


urls=[setting.url]*setting.attempts

@app.get("/check")
async def is_google_up():

    semaphore = asyncio.Semaphore(setting.max_concurrency_limit)
    async with httpx.AsyncClient(timeout=5.0) as client:
        async def semaphore_limit(url):
            async with semaphore:
                return await url_validation(url,client)
        tasks=[semaphore_limit(url) for url in urls]
        results = await asyncio.gather(*tasks)
        healthy_count= sum( 1 for r in results if r.get("status_code",0)<500)
        response_time = [r["elapsed_time"] for r in results if "elapsed_time" in r]

    return {
        "summary":{
            "total_checks": len(results),
            "healthy_url_count": healthy_count,
            "unhealthy_url_count" : len(results) - healthy_count,
            "avg_response_time": sum(response_time)/len(response_time) if response_time else 0,
            "max_response_time": max(response_time) if response_time else 0


        },
    "results": results
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("routes:app", host="0.0.0.0", port=8000, reload=True)
