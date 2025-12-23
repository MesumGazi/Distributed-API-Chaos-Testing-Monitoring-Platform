from fastapi import FastAPI
import asyncio
from playwright.async_api import async_playwright,Playwright



app =FastAPI()

async def url_check(url,browser):
    page =await  browser.new_page()
    try :
        response = await page.goto(url,timeout=500000)
        return {
            "url":url,
            "up": response is not None and response.status < 500,
            "status": response.status
        }
    except Exception as e:
        return {
            "url":url,
            "up":False,
            "error":str(e)
        }




@app.get("/check")
async def link_check_function():
    urls=["https://www.google.com"]*100
    async with async_playwright() as p:
        browser =await  p.chromium.launch(headless=True)
        tasks=[
            url_check(url,browser)
            for url in urls
            ]
        results = await asyncio.gather(*tasks)
        await browser.close()
        return results
        
        
        


