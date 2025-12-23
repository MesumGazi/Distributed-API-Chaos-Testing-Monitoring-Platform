import asyncio
from fastapi import FastAPI
from playwright.async_api import async_playwright

from serivices.services import url_check

app=FastAPI()


@app.get("/check")
async def link_is_up_check():
    urls=["https://www.Google.com"]*100
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks =[
            url_check(url,browser)
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
        await browser.close()
        return results

