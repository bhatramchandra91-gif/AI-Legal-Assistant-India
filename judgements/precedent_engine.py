from judgments.scraper_bs4 import scrape_indian_kanoon

def get_precedents(case):
    results = scrape_indian_kanoon(case)
    return results
