import requests
from bs4 import BeautifulSoup

def scrape_indian_kanoon(query):
    url=f"https://indiankanoon.org/search/?formInput={query}"
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'html.parser')

    results=[]
    for a in soup.select(".result_title")[:5]:
        results.append(a.text.strip())

    return results

