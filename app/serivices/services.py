from playwright.sync_api import sync_playwright, Playwright


def link_check_function(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        browser.close()

google = "https://www.google.com"

link_check_function(google)



