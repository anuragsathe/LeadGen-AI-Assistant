import requests
from bs4 import BeautifulSoup
import re
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
search_cache: dict[str, str] = {}

def scrape_website(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return re.sub(r"\s+", " ", text)[:4000]
    except Exception as e:
        return str(e)


def search_and_scrape(query: str) -> str:
    if query in search_cache:
        return search_cache[query]

    try:
        results = search.run(query)
        urls = re.findall(r'https?://[^\s"\']+', results)

        if urls:
            for url in urls[:3]:
                scraped = scrape_website(url)
                if scraped and not scraped.lower().startswith("error"):
                    search_cache[query] = scraped
                    return scraped

        fallback = f"SEARCH RESULTS:\n{results}"
        search_cache[query] = fallback
        return fallback

    except Exception as e:
        fallback = f"SEARCH ERROR: {str(e)}"
        search_cache[query] = fallback
        return fallback