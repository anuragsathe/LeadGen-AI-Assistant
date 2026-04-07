import requests
from bs4 import BeautifulSoup
import re
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

def scrape_website(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return re.sub(r"\s+", " ", text)[:4000]
    except Exception as e:
        return str(e)


def search_and_scrape(query: str) -> str:
    try:
        results = search.run(query)
        urls = re.findall(r'https?://[^\s]+', results)

        if not urls:
            return f"No URLs found in search results. Raw results: {results[:1000]}"

        return scrape_website(urls[0])

    except Exception as e:
        return f"Search error: {str(e)}"