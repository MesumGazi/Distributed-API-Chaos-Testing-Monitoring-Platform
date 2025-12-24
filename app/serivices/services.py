import asyncio
import httpx


async def url_validation(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            return {
                "url": url,
                "is up": url is not None,
                "status": response.status_code
            }
        except Exception as e:
            return {
                "url": url,
                "status": False,
                "error":str(e)
            }
        