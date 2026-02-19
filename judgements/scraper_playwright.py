from playwright.sync_api import sync_playwright

def scrape_court_live(query):
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()
        page.goto(f"https://www.google.com/search?q={query}+judgement+india")
        data=page.content()
        browser.close()
        return data[:500]
