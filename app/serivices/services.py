from playwright.async_api import async_playwright


async def url_check(url,browser):
        page =await  browser.new_page()
        try:
                response = await page.goto(url,timeout=50000)
  
                return {
                        "url":url,
                        "up": response is not None and response.status < 500,
                        "status": response.status
                }
        except Exception as e:
                return{
                        "url":url,
                        "up": False,
                        "error":str(e)
                }


